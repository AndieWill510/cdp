"""Domain services for the live CDP core.

create_decision_with_workflow is the smallest executable decision vertical
slice: create a decision, start its configured workflow, and open the
initial blocking review task, all inside one transaction with a matching
audit trail.

raise_challenge_for_decision is the second vertical slice: raise a governed
challenge against an existing decision, block its workflow instance, and
open an adjudication task, all inside one transaction with a matching audit
trail.

adjudicate_challenge is the third vertical slice: record a governed
judgment over a single raised challenge, update its status, complete its
adjudication task, and unblock the workflow instance when nothing else
remains open, all inside one transaction with a matching audit trail. This
is challenge-level adjudication only -- see the naming note in
db/ddl/007-challenge-adjudication.sql for why it is deliberately not the
broader, decision-level RFC-CDP-044 Adjudicate Protocol.

authorize_execution is the fourth vertical slice: authorize a decision to
proceed to execution once no blocking challenge work remains open,
completing the decision's original review task and advancing its workflow
instance, all inside one transaction with a matching audit trail. See the
naming note in db/ddl/008-execution-authorization.sql for why this is
deliberately not called "legitimation" -- it is an authorization gate, not
a declaration of final legitimacy, and it does not implement execution
itself.

record_execution_attempt is the fifth vertical slice: record one completed
execution attempt (succeeded, failed, or partial) against an authorized
decision, all inside one transaction with a matching audit trail. It
records an external act; it does not perform or orchestrate execution.
Critically, it never writes to cdp_core.workflow_instance on any outcome --
see the constitutional-invariant note in db/ddl/009-execution-record.sql:
repair is mandatory on every outcome, not conditional on failure, so
execution must not close the workflow or advance it toward learning.

register_actor, submit_identity_claim, recognize_identity_claim,
deny_identity_claim, contest_identity_claim, and attest_and_create_decision
are the Identity and Attestation slice (RFC-CDP-030, RFC-CDP-031): register
a governed actor, submit/recognize/deny/contest an identity claim without
ever deleting it, and attest a decision-creation act to an actor holding a
recognized, in-scope identity claim, all inside one transaction per
operation with a matching audit trail. See
db/ddl/010-identity-and-attestation.sql for the constitutional scope note
on what "verified" honestly means in this slice, and for why this
deliberately does not implement Authority, Standing, Legitimize, or Repair.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

import psycopg

from cdp.core import db
from cdp.core.repositories import actors as actors_repo
from cdp.core.repositories import adjudications as adjudications_repo
from cdp.core.repositories import attestations as attestations_repo
from cdp.core.repositories import audit as audit_repo
from cdp.core.repositories import challenges as challenges_repo
from cdp.core.repositories import decisions as decisions_repo
from cdp.core.repositories import execution_authorizations as execution_authorizations_repo
from cdp.core.repositories import execution_records as execution_records_repo
from cdp.core.repositories import identity_claims as identity_claims_repo
from cdp.core.repositories import workflows as workflows_repo

# No workflow_stage or rule_definition yet gates challenges through an
# explicit challenge stage/transition (see db/ddl/005-challenge-transition.sql).
# Until that exists, challengeability is permitted only for non-terminal
# workflow instances -- a transitional workflow-status gate, not a full
# challenge-policy model.
_TERMINAL_WORKFLOW_STATUSES = frozenset({"closed", "cancelled"})

# A challenge may be adjudicated again only while it remains in one of
# these statuses. Once it reaches a terminal status, further adjudication
# attempts are rejected (409) rather than silently accepted.
_TERMINAL_CHALLENGE_STATUSES = frozenset({"resolved", "dismissed", "withdrawn"})

# Outcome -> resulting challenge_status. Mirrored by a DB-level CHECK
# constraint on cdp_core.challenge_adjudication_record so the two cannot
# drift apart.
_OUTCOME_TO_CHALLENGE_STATUS = {
    "sustained": "resolved",
    "not_sustained": "dismissed",
    "referred_to_repair": "resolved",
    "deferred": "under_review",
}


class DecisionClassNotConfigured(Exception):
    """No active workflow is configured for the decision's registry/class."""


class WorkflowStageNotConfigured(Exception):
    """The resolved workflow has no stage_order = 1 stage."""


class DecisionNotFound(Exception):
    """No decision exists for the given registry_name/decision_id."""


class ChallengeNotPermitted(Exception):
    """The decision's workflow cannot currently accept a challenge."""


class ChallengeNotFound(Exception):
    """No challenge exists for the given decision and challenge_id."""


class ChallengeNotAdjudicable(Exception):
    """The challenge has already reached a terminal status."""


class ExecutionAuthorizationNotPermitted(Exception):
    """The decision cannot currently receive execution authorization."""


class ExecutionAlreadyAuthorized(Exception):
    """The decision already has an execution authorization record."""


class DecisionNotAuthorizedForExecution(Exception):
    """The decision has no execution authorization record yet."""


class ExecutionNotPermitted(Exception):
    """The decision's workflow cannot currently accept an execution record."""


class ExecutionAlreadySucceeded(Exception):
    """This authorization already has a succeeded execution record."""


class ActorAlreadyRegistered(Exception):
    """An actor with this actor_id is already registered."""


class ActorNotFound(Exception):
    """No governed actor exists for the given actor_id."""


class ActorNotActive(Exception):
    """The actor's actor_status is not 'active'."""


class IdentityClaimNotFound(Exception):
    """No identity claim exists for the given claim_id."""


class IdentityClaimActorMismatch(Exception):
    """The identity claim does not belong to the given actor."""


class IdentityClaimNotDecidable(Exception):
    """The claim is not in 'pending' or 'recognized' and cannot be decided again."""


class RecognitionAuthorityRequired(Exception):
    """The deciding actor is not the seeded identity-claim recognition authority."""


class SelfRecognitionForbidden(Exception):
    """An actor cannot recognize, deny, or contest its own identity claim."""


class IdentityClaimNotRecognized(Exception):
    """The identity claim is not currently recognized."""


class IdentityClaimScopeInsufficient(Exception):
    """The identity claim's purpose_scope does not cover the requested governed act."""


# A workflow that has been (re-)blocked by a new challenge raised after
# authorization, or that is already closed/cancelled, cannot accept an
# execution record -- authorization eligibility is not assumed to still
# hold just because an authorization row exists.
_INELIGIBLE_FOR_EXECUTION_WORKFLOW_STATUSES = frozenset({"blocked", "closed", "cancelled"})


@dataclass(frozen=True)
class DecisionInput:
    registry_name: str
    decision_id: str
    decision_class_id: str
    antecedent_text: str
    subject_actor_type: str
    subject_actor_id: str
    predicate_verb: str
    object_type: str
    object_id: str
    permission_source_type: str
    permission_source_id: str
    human_required: bool
    human_approver_id: str = "none"
    parent_decision_id: str | None = None
    parent_relation_type: str = "none"
    source_system: str = "api"
    source_ref: str | None = None
    created: datetime | None = None


def create_decision_with_workflow(decision_input: DecisionInput) -> dict[str, Any]:
    """Create a decision, start its configured workflow, and open its first task.

    Everything below runs inside exactly one transaction. Any failure -
    including an unconfigured decision class or workflow - rolls back all of
    it: the decision, the workflow instance, the task, and the audit events.
    """
    with db.transaction() as cursor:
        return _create_decision_with_workflow_in_transaction(cursor, decision_input)


def _create_decision_with_workflow_in_transaction(
    cursor: Any, decision_input: DecisionInput
) -> dict[str, Any]:
    """Cursor-based body of create_decision_with_workflow.

    Extracted so attest_and_create_decision (see the Identity/Attestation
    slice below) can run decision creation inside its own single
    caller-owned transaction, alongside attestation verification and the
    attestation record insert, without nesting a second db.transaction()
    connection.
    """
    created = decision_input.created or datetime.now(UTC)

    decision = decisions_repo.insert_decision(
        cursor,
        registry_name=decision_input.registry_name,
        decision_id=decision_input.decision_id,
        decision_class_id=decision_input.decision_class_id,
        antecedent_text=decision_input.antecedent_text,
        subject_actor_type=decision_input.subject_actor_type,
        subject_actor_id=decision_input.subject_actor_id,
        predicate_verb=decision_input.predicate_verb,
        object_type=decision_input.object_type,
        object_id=decision_input.object_id,
        permission_source_type=decision_input.permission_source_type,
        permission_source_id=decision_input.permission_source_id,
        human_required=decision_input.human_required,
        human_approver_id=decision_input.human_approver_id,
        parent_decision_id=decision_input.parent_decision_id,
        parent_relation_type=decision_input.parent_relation_type,
        created=created,
        source_system=decision_input.source_system,
        source_ref=decision_input.source_ref,
    )

    workflow_definition = workflows_repo.resolve_active_workflow_for_class(
        cursor,
        registry_name=decision_input.registry_name,
        decision_class_id=decision_input.decision_class_id,
    )
    if workflow_definition is None:
        raise DecisionClassNotConfigured(
            "No active workflow is configured for decision class "
            f"{decision_input.registry_name}.{decision_input.decision_class_id}"
        )

    first_stage = workflows_repo.resolve_first_stage(
        cursor, workflow_definition_id=workflow_definition["workflow_definition_id"]
    )
    if first_stage is None:
        raise WorkflowStageNotConfigured(
            "Workflow "
            f"{workflow_definition['workflow_code']} {workflow_definition['workflow_version']}"
            " has no stage_order = 1 stage configured"
        )

    workflow_instance = workflows_repo.insert_workflow_instance(
        cursor,
        registry_name=decision_input.registry_name,
        decision_id=decision_input.decision_id,
        workflow_definition_id=workflow_definition["workflow_definition_id"],
        current_stage_id=first_stage["workflow_stage_id"],
        lifecycle_stage=first_stage["lifecycle_stage"],
    )

    task = workflows_repo.insert_task(
        cursor,
        workflow_instance_id=workflow_instance["workflow_instance_id"],
        registry_name=decision_input.registry_name,
        decision_id=decision_input.decision_id,
    )

    decision_aggregate_id = f"{decision_input.registry_name}:{decision_input.decision_id}"

    audit_repo.append_event(
        cursor,
        event_type="decision.created",
        aggregate_type="decision",
        aggregate_id=decision_aggregate_id,
        payload={
            "registry_name": decision_input.registry_name,
            "decision_id": decision_input.decision_id,
            "decision_class_id": decision_input.decision_class_id,
        },
    )
    audit_repo.append_event(
        cursor,
        event_type="workflow.started",
        aggregate_type="workflow_instance",
        aggregate_id=str(workflow_instance["workflow_instance_id"]),
        payload={
            "registry_name": decision_input.registry_name,
            "decision_id": decision_input.decision_id,
            "workflow_definition_id": str(workflow_definition["workflow_definition_id"]),
            "workflow_code": workflow_definition["workflow_code"],
            "workflow_version": workflow_definition["workflow_version"],
            "current_stage_id": str(first_stage["workflow_stage_id"]),
            "stage_code": first_stage["stage_code"],
        },
    )
    audit_repo.append_event(
        cursor,
        event_type="task.created",
        aggregate_type="workflow_task",
        aggregate_id=str(task["task_id"]),
        payload={
            "registry_name": decision_input.registry_name,
            "decision_id": decision_input.decision_id,
            "workflow_instance_id": str(workflow_instance["workflow_instance_id"]),
            "task_type": task["task_type"],
            "assigned_role": task["assigned_role"],
            "blocking": task["blocking"],
        },
    )

    return {
        "decision": decision,
        "workflow_instance": workflow_instance,
        "task": task,
    }


@dataclass(frozen=True)
class ChallengeInput:
    registry_name: str
    decision_id: str
    raised_by_actor_id: str
    challenge_text: str
    challenge_type: str = "other"
    metadata: dict[str, Any] | None = None


def raise_challenge_for_decision(challenge_input: ChallengeInput) -> dict[str, Any]:
    """Raise a challenge against an existing decision.

    Everything below runs inside exactly one transaction. Any failure -
    including a missing decision or a workflow that can no longer accept a
    challenge - rolls back all of it: the challenge record, the workflow
    instance update, the task, and the audit events.

    Challengeability is currently gated only by workflow_instance.workflow_status
    (see _TERMINAL_WORKFLOW_STATUSES): a transitional workflow-status gate
    used until an explicit challenge stage/rule exists, not a full
    challenge-policy model.
    """
    with db.transaction() as cursor:
        decision = decisions_repo.fetch_decision(
            cursor,
            registry_name=challenge_input.registry_name,
            decision_id=challenge_input.decision_id,
        )
        if decision is None:
            raise DecisionNotFound(
                f"No decision {challenge_input.registry_name}.{challenge_input.decision_id}"
            )

        workflow_instance = workflows_repo.fetch_workflow_instance_for_decision(
            cursor,
            registry_name=challenge_input.registry_name,
            decision_id=challenge_input.decision_id,
        )
        if workflow_instance is None:
            raise ChallengeNotPermitted(
                "No workflow instance is configured for decision "
                f"{challenge_input.registry_name}.{challenge_input.decision_id}"
            )
        if workflow_instance["workflow_status"] in _TERMINAL_WORKFLOW_STATUSES:
            raise ChallengeNotPermitted(
                f"Workflow for decision {challenge_input.registry_name}."
                f"{challenge_input.decision_id} is {workflow_instance['workflow_status']} "
                "and can no longer accept a challenge"
            )

        updated_workflow_instance = workflows_repo.mark_workflow_instance_blocked(
            cursor,
            workflow_instance_id=workflow_instance["workflow_instance_id"],
            blocked_reason=(
                f"Challenge raised by {challenge_input.raised_by_actor_id}; "
                "pending adjudication"
            ),
        )

        task = workflows_repo.insert_task(
            cursor,
            workflow_instance_id=workflow_instance["workflow_instance_id"],
            registry_name=challenge_input.registry_name,
            decision_id=challenge_input.decision_id,
            task_type="adjudicate_challenge",
            assigned_role="adjudicator",
            blocking=True,
        )

        challenge = challenges_repo.insert_challenge(
            cursor,
            registry_name=challenge_input.registry_name,
            decision_id=challenge_input.decision_id,
            workflow_instance_id=workflow_instance["workflow_instance_id"],
            raised_by_actor_id=challenge_input.raised_by_actor_id,
            challenge_type=challenge_input.challenge_type,
            challenge_text=challenge_input.challenge_text,
            created_task_id=task["task_id"],
            metadata=challenge_input.metadata,
        )

        # Audit narrative order is challenge.raised -> workflow.transitioned ->
        # task.created (cause, then its consequences), independent of the
        # repository write order above, which inserts the task before the
        # challenge record so challenge_record.created_task_id has a real
        # value to reference.
        audit_repo.append_event(
            cursor,
            event_type="challenge.raised",
            aggregate_type="challenge",
            aggregate_id=str(challenge["challenge_id"]),
            payload={
                "registry_name": challenge_input.registry_name,
                "decision_id": challenge_input.decision_id,
                "raised_by_actor_id": challenge_input.raised_by_actor_id,
                "challenge_type": challenge["challenge_type"],
                "created_task_id": str(task["task_id"]),
            },
        )
        audit_repo.append_event(
            cursor,
            event_type="workflow.transitioned",
            aggregate_type="workflow_instance",
            aggregate_id=str(workflow_instance["workflow_instance_id"]),
            payload={
                "registry_name": challenge_input.registry_name,
                "decision_id": challenge_input.decision_id,
                "workflow_status": updated_workflow_instance["workflow_status"],
                "blocked": updated_workflow_instance["blocked"],
                "blocked_reason": updated_workflow_instance["blocked_reason"],
            },
        )
        audit_repo.append_event(
            cursor,
            event_type="task.created",
            aggregate_type="workflow_task",
            aggregate_id=str(task["task_id"]),
            payload={
                "registry_name": challenge_input.registry_name,
                "decision_id": challenge_input.decision_id,
                "workflow_instance_id": str(workflow_instance["workflow_instance_id"]),
                "task_type": task["task_type"],
                "assigned_role": task["assigned_role"],
                "blocking": task["blocking"],
            },
        )

    return {
        "challenge": challenge,
        "workflow_instance": updated_workflow_instance,
        "task": task,
    }


@dataclass(frozen=True)
class AdjudicationInput:
    registry_name: str
    decision_id: str
    challenge_id: uuid.UUID
    adjudicated_by_actor_id: str
    outcome: str
    rationale: str


def adjudicate_challenge(adjudication_input: AdjudicationInput) -> dict[str, Any]:
    """Record a judgment over a single raised challenge.

    Everything below runs inside exactly one transaction. Any failure rolls
    back all of it: the adjudication record, the challenge status change,
    the task completion, and the workflow unblock.

    A challenge may be adjudicated more than once only while it remains
    non-terminal (challenge_status in ('raised', 'under_review')); a
    'deferred' outcome preserves this adjudication and leaves the challenge
    open for a later, final adjudication. The workflow instance is
    unblocked only if no other challenge for the same decision is still
    'raised' or 'under_review' -- this preserves the invariant that a
    workflow stays blocked while any unresolved challenge remains. It is
    not repeat-challenge policy: it does not reject, merge, dedupe, or
    escalate repeat challenges.
    """
    with db.transaction() as cursor:
        decision = decisions_repo.fetch_decision(
            cursor,
            registry_name=adjudication_input.registry_name,
            decision_id=adjudication_input.decision_id,
        )
        if decision is None:
            raise DecisionNotFound(
                f"No decision {adjudication_input.registry_name}.{adjudication_input.decision_id}"
            )

        challenge = challenges_repo.fetch_challenge(
            cursor, challenge_id=adjudication_input.challenge_id
        )
        if (
            challenge is None
            or challenge["registry_name"] != adjudication_input.registry_name
            or challenge["decision_id"] != adjudication_input.decision_id
        ):
            raise ChallengeNotFound(
                f"No challenge {adjudication_input.challenge_id} for decision "
                f"{adjudication_input.registry_name}.{adjudication_input.decision_id}"
            )
        if challenge["challenge_status"] in _TERMINAL_CHALLENGE_STATUSES:
            raise ChallengeNotAdjudicable(
                f"Challenge {adjudication_input.challenge_id} is already "
                f"{challenge['challenge_status']} and cannot be adjudicated again"
            )

        resulting_challenge_status = _OUTCOME_TO_CHALLENGE_STATUS.get(adjudication_input.outcome)
        if resulting_challenge_status is None:
            raise ValueError(
                f"Unknown challenge adjudication outcome: {adjudication_input.outcome!r}"
            )
        set_resolved_at = resulting_challenge_status in ("resolved", "dismissed")

        updated_challenge = challenges_repo.update_challenge_status(
            cursor,
            challenge_id=challenge["challenge_id"],
            challenge_status=resulting_challenge_status,
            set_resolved_at=set_resolved_at,
        )

        task = None
        workflow_instance = None
        if resulting_challenge_status != "under_review":
            if challenge["created_task_id"] is not None:
                task = workflows_repo.complete_task(cursor, task_id=challenge["created_task_id"])

            remaining_open = challenges_repo.count_open_challenges_for_decision(
                cursor,
                registry_name=adjudication_input.registry_name,
                decision_id=adjudication_input.decision_id,
                exclude_challenge_id=challenge["challenge_id"],
            )
            if remaining_open == 0:
                workflow_instance = workflows_repo.unblock_workflow_instance(
                    cursor, workflow_instance_id=challenge["workflow_instance_id"]
                )

        adjudication = adjudications_repo.insert_adjudication(
            cursor,
            registry_name=adjudication_input.registry_name,
            decision_id=adjudication_input.decision_id,
            challenge_id=challenge["challenge_id"],
            adjudicated_by_actor_id=adjudication_input.adjudicated_by_actor_id,
            outcome=adjudication_input.outcome,
            rationale=adjudication_input.rationale,
            resulting_challenge_status=resulting_challenge_status,
            adjudicated_task_id=task["task_id"] if task is not None else None,
        )

        base_payload = {
            "registry_name": adjudication_input.registry_name,
            "decision_id": adjudication_input.decision_id,
            "challenge_id": str(challenge["challenge_id"]),
            "adjudication_id": str(adjudication["adjudication_id"]),
            "outcome": adjudication["outcome"],
            "challenge_status": updated_challenge["challenge_status"],
        }

        # Audit narrative order is challenge.adjudicated -> workflow.transitioned
        # -> task.completed (cause, then its consequences). For a 'deferred'
        # outcome, only challenge.adjudicated is emitted -- nothing else changed.
        audit_repo.append_event(
            cursor,
            event_type="challenge.adjudicated",
            aggregate_type="challenge_adjudication",
            aggregate_id=str(adjudication["adjudication_id"]),
            payload=dict(base_payload),
        )
        if workflow_instance is not None:
            audit_repo.append_event(
                cursor,
                event_type="workflow.transitioned",
                aggregate_type="workflow_instance",
                aggregate_id=str(challenge["workflow_instance_id"]),
                payload={
                    **base_payload,
                    "workflow_status": workflow_instance["workflow_status"],
                    "blocked": workflow_instance["blocked"],
                },
            )
        if task is not None:
            audit_repo.append_event(
                cursor,
                event_type="task.completed",
                aggregate_type="workflow_task",
                aggregate_id=str(task["task_id"]),
                payload={
                    **base_payload,
                    "task_status": task["task_status"],
                },
            )

    return {
        "adjudication": adjudication,
        "challenge": updated_challenge,
        "workflow_instance": workflow_instance,
        "task": task,
    }


@dataclass(frozen=True)
class ExecutionAuthorizationInput:
    registry_name: str
    decision_id: str
    authorized_by_actor_id: str
    rationale: str


def authorize_execution(authorization_input: ExecutionAuthorizationInput) -> dict[str, Any]:
    """Authorize a decision to proceed to execution.

    Everything below runs inside exactly one transaction. Any failure rolls
    back all of it: the authorization record, the completed review task,
    the workflow-status update, and the audit events.

    This does not implement execution itself, and it is not a declaration
    that a decision is finally/procedurally legitimate -- it only means the
    decision may proceed under the current workflow conditions. It does not
    create a task; it completes the decision's existing open
    review_decision task from create_decision_with_workflow. A decision may
    receive execution authorization only when no other challenge on it is
    still 'raised' or 'under_review' and no 'adjudicate_challenge' task
    remains open -- this gate must never be bypassed.

    Authorization is a one-time terminal gate-pass per decision, not a
    repeatable judgment like adjudication. A second attempt is rejected as
    ExecutionAlreadyAuthorized -- checked immediately after confirming the
    decision exists, before any eligibility check -- so a repeat call fails
    because the decision is already authorized, not because a downstream
    side effect (like the review task now being completed) happens to make
    it look ineligible. That keeps the failure reason truthful even if
    workflow-task behavior changes later. uq_execution_authorization_decision
    remains the DB-level backstop against a concurrent race between two
    requests that both pass this check before either commits.
    """
    with db.transaction() as cursor:
        decision = decisions_repo.fetch_decision(
            cursor,
            registry_name=authorization_input.registry_name,
            decision_id=authorization_input.decision_id,
        )
        if decision is None:
            raise DecisionNotFound(
                f"No decision {authorization_input.registry_name}.{authorization_input.decision_id}"
            )

        existing_authorization = execution_authorizations_repo.fetch_authorization_for_decision(
            cursor,
            registry_name=authorization_input.registry_name,
            decision_id=authorization_input.decision_id,
        )
        if existing_authorization is not None:
            raise ExecutionAlreadyAuthorized(
                f"Decision {authorization_input.registry_name}.{authorization_input.decision_id} "
                "already has an execution authorization"
            )

        workflow_instance = workflows_repo.fetch_workflow_instance_for_decision(
            cursor,
            registry_name=authorization_input.registry_name,
            decision_id=authorization_input.decision_id,
        )
        if workflow_instance is None:
            raise ExecutionAuthorizationNotPermitted(
                "No workflow instance is configured for decision "
                f"{authorization_input.registry_name}.{authorization_input.decision_id}"
            )

        open_challenge_count = challenges_repo.count_open_challenges_for_decision(
            cursor,
            registry_name=authorization_input.registry_name,
            decision_id=authorization_input.decision_id,
        )
        if open_challenge_count > 0:
            raise ExecutionAuthorizationNotPermitted(
                f"{open_challenge_count} blocking challenge(s) remain open for decision "
                f"{authorization_input.registry_name}.{authorization_input.decision_id}"
            )

        open_adjudication_task_count = workflows_repo.count_open_tasks_by_type(
            cursor,
            registry_name=authorization_input.registry_name,
            decision_id=authorization_input.decision_id,
            task_type="adjudicate_challenge",
        )
        if open_adjudication_task_count > 0:
            raise ExecutionAuthorizationNotPermitted(
                f"{open_adjudication_task_count} open adjudicate_challenge task(s) remain for "
                f"decision {authorization_input.registry_name}.{authorization_input.decision_id}"
            )

        review_task = workflows_repo.fetch_open_task_by_type(
            cursor,
            registry_name=authorization_input.registry_name,
            decision_id=authorization_input.decision_id,
            task_type="review_decision",
        )
        if review_task is None:
            raise ExecutionAuthorizationNotPermitted(
                "No open review_decision task exists for decision "
                f"{authorization_input.registry_name}.{authorization_input.decision_id} to complete"
            )

        authorization = execution_authorizations_repo.insert_authorization(
            cursor,
            registry_name=authorization_input.registry_name,
            decision_id=authorization_input.decision_id,
            workflow_instance_id=workflow_instance["workflow_instance_id"],
            authorized_by_actor_id=authorization_input.authorized_by_actor_id,
            rationale=authorization_input.rationale,
            completed_task_id=review_task["task_id"],
        )

        updated_workflow_instance = workflows_repo.mark_workflow_instance_advanced(
            cursor, workflow_instance_id=workflow_instance["workflow_instance_id"]
        )

        completed_task = workflows_repo.complete_task(cursor, task_id=review_task["task_id"])

        base_payload = {
            "registry_name": authorization_input.registry_name,
            "decision_id": authorization_input.decision_id,
            "authorization_id": str(authorization["authorization_id"]),
            "workflow_instance_id": str(workflow_instance["workflow_instance_id"]),
            "completed_task_id": str(completed_task["task_id"]),
        }

        # Audit narrative order is execution.authorized -> workflow.transitioned
        # -> task.completed (cause, then its consequences).
        audit_repo.append_event(
            cursor,
            event_type="execution.authorized",
            aggregate_type="execution_authorization",
            aggregate_id=str(authorization["authorization_id"]),
            payload=dict(base_payload),
        )
        audit_repo.append_event(
            cursor,
            event_type="workflow.transitioned",
            aggregate_type="workflow_instance",
            aggregate_id=str(workflow_instance["workflow_instance_id"]),
            payload={
                **base_payload,
                "workflow_status": updated_workflow_instance["workflow_status"],
            },
        )
        audit_repo.append_event(
            cursor,
            event_type="task.completed",
            aggregate_type="workflow_task",
            aggregate_id=str(completed_task["task_id"]),
            payload={
                **base_payload,
                "task_status": completed_task["task_status"],
            },
        )

    return {
        "authorization": authorization,
        "workflow_instance": updated_workflow_instance,
        "completed_task": completed_task,
    }


@dataclass(frozen=True)
class ExecutionRecordInput:
    registry_name: str
    decision_id: str
    executed_by_actor_id: str
    execution_status: str
    result_summary: str
    attempted_at: datetime
    completed_at: datetime


def record_execution_attempt(execution_input: ExecutionRecordInput) -> dict[str, Any]:
    """Record one completed execution attempt against an authorized decision.

    Everything below runs inside exactly one transaction. Any failure rolls
    back all of it: the execution record and the audit event.

    This records an external act; it does not perform or orchestrate
    execution. attempted_at/completed_at describe when that external act
    happened, not when this service ran. Retries are expected: multiple
    execution records may exist for the same authorization (a failed or
    partial attempt does not block a further attempt), but at most one may
    be 'succeeded' -- enforced here and backed by a DB-level partial unique
    index so a concurrent race cannot create two.

    This never writes to cdp_core.workflow_instance, on any outcome. CDP's
    governing invariant is that repair is mandatory, not conditional on
    failure or detected harm: execution succeeding does not close the
    workflow or exempt the decision from reparative obligation, so nothing
    here may advance the workflow toward closure or learning. That is left
    for a future, mandatory repair slice to act on.
    """
    with db.transaction() as cursor:
        decision = decisions_repo.fetch_decision(
            cursor,
            registry_name=execution_input.registry_name,
            decision_id=execution_input.decision_id,
        )
        if decision is None:
            raise DecisionNotFound(
                f"No decision {execution_input.registry_name}.{execution_input.decision_id}"
            )

        authorization = execution_authorizations_repo.fetch_authorization_for_decision(
            cursor,
            registry_name=execution_input.registry_name,
            decision_id=execution_input.decision_id,
        )
        if authorization is None:
            raise DecisionNotAuthorizedForExecution(
                f"Decision {execution_input.registry_name}.{execution_input.decision_id} "
                "has no execution authorization"
            )

        workflow_instance = workflows_repo.fetch_workflow_instance_for_decision(
            cursor,
            registry_name=execution_input.registry_name,
            decision_id=execution_input.decision_id,
        )
        if workflow_instance is None:
            raise ExecutionNotPermitted(
                "No workflow instance is configured for decision "
                f"{execution_input.registry_name}.{execution_input.decision_id}"
            )
        if workflow_instance["workflow_status"] in _INELIGIBLE_FOR_EXECUTION_WORKFLOW_STATUSES:
            raise ExecutionNotPermitted(
                f"Workflow for decision {execution_input.registry_name}."
                f"{execution_input.decision_id} is {workflow_instance['workflow_status']} "
                "and cannot currently accept an execution record"
            )

        if execution_input.completed_at < execution_input.attempted_at:
            raise ValueError("completed_at must not be before attempted_at")

        if execution_input.execution_status == "succeeded":
            existing_success = execution_records_repo.fetch_succeeded_execution_for_authorization(
                cursor, authorization_id=authorization["authorization_id"]
            )
            if existing_success is not None:
                raise ExecutionAlreadySucceeded(
                    f"Decision {execution_input.registry_name}.{execution_input.decision_id} "
                    "already has a succeeded execution record"
                )

        execution_record = execution_records_repo.insert_execution_record(
            cursor,
            registry_name=execution_input.registry_name,
            decision_id=execution_input.decision_id,
            authorization_id=authorization["authorization_id"],
            workflow_instance_id=workflow_instance["workflow_instance_id"],
            executed_by_actor_id=execution_input.executed_by_actor_id,
            execution_status=execution_input.execution_status,
            result_summary=execution_input.result_summary,
            attempted_at=execution_input.attempted_at,
            completed_at=execution_input.completed_at,
        )

        audit_repo.append_event(
            cursor,
            event_type="execution.recorded",
            aggregate_type="execution_record",
            aggregate_id=str(execution_record["execution_id"]),
            payload={
                "registry_name": execution_input.registry_name,
                "decision_id": execution_input.decision_id,
                "execution_id": str(execution_record["execution_id"]),
                "authorization_id": str(authorization["authorization_id"]),
                "execution_status": execution_record["execution_status"],
            },
        )

    return {
        "execution_record": execution_record,
        "workflow_instance": workflow_instance,
    }


# ---------------------------------------------------------------------------
# Identity and Attestation (RFC-CDP-030, RFC-CDP-031)
# ---------------------------------------------------------------------------
#
# Scope boundary for this slice, enforced by what is (and is not) below:
#   - No Authority (RFC-CDP-032) grant/evaluation is implemented. An actor's
#     ability to register itself or submit a claim is not gated by an
#     authority check here.
#   - No Standing (RFC-CDP-033) determination is implemented.
#   - No Legitimize, Repair, or workflow-advancement side effect is written
#     by any function below. attest_and_create_decision writes exactly the
#     same decision/workflow/task/audit rows create_decision_with_workflow
#     already writes, plus one attestation_record and one audit event.
#   - "Verified" in this slice means: the actor is active, and holds an
#     identity claim recognized for a purpose_scope that covers the
#     requested governed act. It is not cryptographic proof. See
#     db/ddl/010-identity-and-attestation.sql for the full note.

_DECISION_CREATION_PURPOSE_SCOPE = "decision_creation"

# The single, narrow, bounded governed actor authorized to recognize,
# deny, or contest an Identity Claim in this slice (seeded by
# db/ddl/010-identity-and-attestation.sql). This is not RFC-CDP-032
# Authority -- no grant, scope, or delegation model -- it exists solely to
# close the gap where any registered actor, including a claimant deciding
# its own claim, could otherwise produce a binding "recognized" status.
_IDENTITY_RECOGNITION_AUTHORITY_ACTOR_ID = "cdp_identity_recognition_authority"


@dataclass(frozen=True)
class ActorInput:
    actor_id: str
    actor_type: str
    display_label: str
    display_mode: str = "public"
    description: str | None = None


def register_actor(actor_input: ActorInput) -> dict[str, Any]:
    """Register a new governed actor.

    Runs inside exactly one transaction: the underlying identifier_registry
    row, the cdp_core.actor row, and the audit event all commit or roll
    back together. Raises ActorAlreadyRegistered if actor_id is already
    registered.
    """
    with db.transaction() as cursor:
        try:
            actor = actors_repo.insert_actor(
                cursor,
                actor_id=actor_input.actor_id,
                actor_type=actor_input.actor_type,
                display_label=actor_input.display_label,
                display_mode=actor_input.display_mode,
                description=actor_input.description,
            )
        except psycopg.errors.UniqueViolation as exc:
            raise ActorAlreadyRegistered(
                f"Actor {actor_input.actor_id!r} is already registered"
            ) from exc

        audit_repo.append_event(
            cursor,
            event_type="actor.registered",
            aggregate_type="actor",
            aggregate_id=actor_input.actor_id,
            payload={
                "actor_id": actor_input.actor_id,
                "actor_type": actor_input.actor_type,
                "display_mode": actor_input.display_mode,
            },
        )

    return {"actor": actor}


@dataclass(frozen=True)
class IdentityClaimInput:
    actor_id: str
    claimant_actor_id: str
    claimed_identity_descriptor: str
    purpose_scope: str
    evidence_refs: list[Any] | None = None
    supersedes_claim_id: uuid.UUID | None = None


def submit_identity_claim(claim_input: IdentityClaimInput) -> dict[str, Any]:
    """Submit an identity claim for a registered actor.

    Runs inside exactly one transaction. If supersedes_claim_id is given,
    the superseded claim's recognition_status is set to 'superseded' in the
    same transaction as the new claim's insert -- the superseded row is
    never deleted, only relinked (see cdp_core.identity_claim's
    forbid-delete trigger).
    """
    with db.transaction() as cursor:
        actor = actors_repo.fetch_actor(cursor, actor_id=claim_input.actor_id)
        if actor is None:
            raise ActorNotFound(f"No registered actor {claim_input.actor_id!r}")

        claimant = actors_repo.fetch_actor(cursor, actor_id=claim_input.claimant_actor_id)
        if claimant is None:
            raise ActorNotFound(f"No registered actor {claim_input.claimant_actor_id!r}")

        if claim_input.supersedes_claim_id is not None:
            superseded = identity_claims_repo.fetch_claim(
                cursor, claim_id=claim_input.supersedes_claim_id
            )
            if superseded is None or superseded["actor_id"] != claim_input.actor_id:
                raise IdentityClaimActorMismatch(
                    f"Claim {claim_input.supersedes_claim_id} does not belong to actor "
                    f"{claim_input.actor_id!r} and cannot be superseded by this submission"
                )

        claim = identity_claims_repo.insert_claim(
            cursor,
            actor_id=claim_input.actor_id,
            claimant_actor_id=claim_input.claimant_actor_id,
            claimed_identity_descriptor=claim_input.claimed_identity_descriptor,
            purpose_scope=claim_input.purpose_scope,
            evidence_refs=claim_input.evidence_refs,
            supersedes_claim_id=claim_input.supersedes_claim_id,
        )

        audit_repo.append_event(
            cursor,
            event_type="identity_claim.submitted",
            aggregate_type="identity_claim",
            aggregate_id=str(claim["claim_id"]),
            payload={
                "actor_id": claim_input.actor_id,
                "claimant_actor_id": claim_input.claimant_actor_id,
                "purpose_scope": claim_input.purpose_scope,
                "supersedes_claim_id": str(claim_input.supersedes_claim_id)
                if claim_input.supersedes_claim_id
                else None,
            },
        )
        if claim_input.supersedes_claim_id is not None:
            audit_repo.append_event(
                cursor,
                event_type="identity_claim.superseded",
                aggregate_type="identity_claim",
                aggregate_id=str(claim_input.supersedes_claim_id),
                payload={
                    "actor_id": claim_input.actor_id,
                    "superseded_by_claim_id": str(claim["claim_id"]),
                },
            )

    return {"identity_claim": claim}


@dataclass(frozen=True)
class IdentityClaimDecisionInput:
    claim_id: uuid.UUID
    decided_by_actor_id: str
    rationale: str


def _decide_identity_claim(
    decision_input: IdentityClaimDecisionInput,
    *,
    repo_fn: Any,
    event_type: str,
) -> dict[str, Any]:
    """Shared fetch/authorize/decide/audit body for recognize/deny/contest.

    Two authorization checks run before any write, in this order:

    1. the deciding actor must be the seeded
       _IDENTITY_RECOGNITION_AUTHORITY_ACTOR_ID -- an arbitrary registered
       actor cannot produce a binding recognition decision (fails closed
       with RecognitionAuthorityRequired otherwise);
    2. the deciding actor must not be the claim's own actor or claimant --
       even the recognition authority cannot decide a claim about itself
       (fails closed with SelfRecognitionForbidden otherwise). This is
       redundant with check 1 today, since the authority is a fixed,
       single, non-claimant actor, but it is kept as an explicit,
       independently-enforced invariant rather than an incidental
       consequence of check 1, so it keeps holding if the authority model
       is ever widened.
    """
    with db.transaction() as cursor:
        claim = identity_claims_repo.fetch_claim(cursor, claim_id=decision_input.claim_id)
        if claim is None:
            raise IdentityClaimNotFound(f"No identity claim {decision_input.claim_id}")

        decider = actors_repo.fetch_actor(cursor, actor_id=decision_input.decided_by_actor_id)
        if decider is None:
            raise ActorNotFound(f"No registered actor {decision_input.decided_by_actor_id!r}")

        if decision_input.decided_by_actor_id != _IDENTITY_RECOGNITION_AUTHORITY_ACTOR_ID:
            raise RecognitionAuthorityRequired(
                f"Actor {decision_input.decided_by_actor_id!r} is not the identity-claim "
                "recognition authority and cannot decide identity claims"
            )

        if decision_input.decided_by_actor_id in (claim["actor_id"], claim["claimant_actor_id"]):
            raise SelfRecognitionForbidden(
                f"Actor {decision_input.decided_by_actor_id!r} cannot decide its own "
                "identity claim"
            )

        updated_claim = repo_fn(
            cursor,
            claim_id=decision_input.claim_id,
            decided_by_actor_id=decision_input.decided_by_actor_id,
            rationale=decision_input.rationale,
        )
        if updated_claim is None:
            raise IdentityClaimNotDecidable(
                f"Identity claim {decision_input.claim_id} is {claim['recognition_status']} "
                "and cannot be decided again"
            )

        audit_repo.append_event(
            cursor,
            event_type=event_type,
            aggregate_type="identity_claim",
            aggregate_id=str(decision_input.claim_id),
            payload={
                "actor_id": claim["actor_id"],
                "decided_by_actor_id": decision_input.decided_by_actor_id,
                "recognition_status": updated_claim["recognition_status"],
            },
        )

    return {"identity_claim": updated_claim}


def recognize_identity_claim(decision_input: IdentityClaimDecisionInput) -> dict[str, Any]:
    """Recognize an identity claim. See _decide_identity_claim for the shared
    fetch/decide/audit shape; recognition never deletes or replaces the claim
    row, only transitions recognition_status on it."""
    return _decide_identity_claim(
        decision_input,
        repo_fn=identity_claims_repo.recognize_claim,
        event_type="identity_claim.recognized",
    )


def deny_identity_claim(decision_input: IdentityClaimDecisionInput) -> dict[str, Any]:
    """Deny an identity claim. The claim row is preserved, not erased --
    only recognition_status changes to 'denied'."""
    return _decide_identity_claim(
        decision_input,
        repo_fn=identity_claims_repo.deny_claim,
        event_type="identity_claim.denied",
    )


def contest_identity_claim(decision_input: IdentityClaimDecisionInput) -> dict[str, Any]:
    """Contest an identity claim (or its prior recognition). The claim row
    is preserved, not erased -- only recognition_status changes to
    'contested'."""
    return _decide_identity_claim(
        decision_input,
        repo_fn=identity_claims_repo.contest_claim,
        event_type="identity_claim.contested",
    )


@dataclass(frozen=True)
class AttestationInput:
    actor_id: str
    identity_claim_id: uuid.UUID
    attestation_method: str
    credential_reference: str
    issued_at: datetime


@dataclass(frozen=True)
class AttestedDecisionInput:
    decision_input: DecisionInput
    attestation_input: AttestationInput


def attest_and_create_decision(attested_input: AttestedDecisionInput) -> dict[str, Any]:
    """Attest a decision-creation act to an actor, then create the decision.

    attestation_input.actor_id is the actor who performed/submitted the
    governed act -- the attestor -- and is not required to equal, and is
    never inferred from, decision_input.subject_actor_id -- the actor or
    entity the decision is about. These are different roles: a clinician
    (attestor) may propose a decision about a patient (subject); an
    adjuster (attestor) may create a decision about a claimant (subject).
    Collapsing them would attribute the act to the governed subject rather
    than its actual author. Both are independently, durably recorded: the
    attestor via cdp_core.attestation_record.actor_id (immutable, FK'd to
    this decision, queryable via GET /decisions/{registry_name}/
    {decision_id}/attestations), the subject via cdp_core.decision_registry
    unchanged as before. subject_actor_id still has to satisfy
    decision_registry's own pre-existing identifier rules; it does not
    have to be a governed cdp_core.actor at all.

    Everything below runs inside exactly one transaction, reusing
    _create_decision_with_workflow_in_transaction so decision creation is
    not a nested/second transaction. Any failure - an unknown or inactive
    actor, a missing/unrecognized/out-of-scope identity claim, or any
    failure from decision creation itself - rolls back all of it: no
    decision, no workflow instance, no task, no attestation record, and no
    audit event survive.

    This is the proof path required by the Identity and Attestation slice.
    It is additive: POST /decisions (create_decision_with_workflow) is
    unchanged and continues to accept unattested decisions, exactly as
    every existing caller and test already expects. Only this new path
    requires attestation.
    """
    decision_input = attested_input.decision_input
    attestation_input = attested_input.attestation_input

    with db.transaction() as cursor:
        actor = actors_repo.fetch_actor(cursor, actor_id=attestation_input.actor_id)
        if actor is None:
            raise ActorNotFound(f"No registered actor {attestation_input.actor_id!r}")
        if actor["actor_status"] != "active":
            raise ActorNotActive(
                f"Actor {attestation_input.actor_id!r} is {actor['actor_status']}, not active"
            )

        claim = identity_claims_repo.fetch_claim(
            cursor, claim_id=attestation_input.identity_claim_id
        )
        if claim is None or claim["actor_id"] != attestation_input.actor_id:
            raise IdentityClaimActorMismatch(
                f"Identity claim {attestation_input.identity_claim_id} does not belong to "
                f"actor {attestation_input.actor_id!r}"
            )
        if claim["recognition_status"] != "recognized":
            raise IdentityClaimNotRecognized(
                f"Identity claim {attestation_input.identity_claim_id} is "
                f"{claim['recognition_status']}, not recognized"
            )
        if claim["purpose_scope"] != _DECISION_CREATION_PURPOSE_SCOPE:
            raise IdentityClaimScopeInsufficient(
                f"Identity claim {attestation_input.identity_claim_id} has purpose_scope "
                f"{claim['purpose_scope']!r}, which does not cover "
                f"{_DECISION_CREATION_PURPOSE_SCOPE!r}"
            )

        decision_result = _create_decision_with_workflow_in_transaction(cursor, decision_input)

        attestation = attestations_repo.insert_attestation(
            cursor,
            actor_id=attestation_input.actor_id,
            identity_claim_id=attestation_input.identity_claim_id,
            governed_act_type="decision_created",
            governed_act_registry_name=decision_input.registry_name,
            governed_act_decision_id=decision_input.decision_id,
            attestation_method=attestation_input.attestation_method,
            credential_reference=attestation_input.credential_reference,
            issued_at=attestation_input.issued_at,
            verifier_actor_id="cdp_attestation_service",
        )

        audit_repo.append_event(
            cursor,
            event_type="attestation.recorded",
            aggregate_type="attestation_record",
            aggregate_id=str(attestation["attestation_id"]),
            payload={
                "registry_name": decision_input.registry_name,
                "decision_id": decision_input.decision_id,
                "actor_id": attestation_input.actor_id,
                "identity_claim_id": str(attestation_input.identity_claim_id),
                "attestation_method": attestation_input.attestation_method,
            },
        )

    return {**decision_result, "attestation": attestation}
