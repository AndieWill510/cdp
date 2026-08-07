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

grant_authority, revoke_authority, and attest_and_create_decision's
Authority gate are the Authority slice (RFC-CDP-032), scoped to that RFC's
SS19 Minimal Compliance: a governed Authority Grant, a governed Authority
Evaluation Result, and a single bounded actor authorized to issue or
revoke grants -- no delegation, no quorum, no separation-of-duties
enforcement. See db/ddl/011-authority-and-delegation.sql for the full
boundary statement.

submit_affected_party_standing_claim, recognize_standing_claim,
deny_standing_claim, and attest_and_raise_challenge's optional Standing
gate are the Standing slice (RFC-CDP-033, session 035), scoped to
Constitutional Affected-Party Standing for the Challenge stage only: a
governed Standing Claim, a governed Standing Recognition Determination as
a separate append-only record, a single bounded actor authorized to
determine claims, and an optional (not mandatory) gate on
attest_and_raise_challenge. No Recusal. Only two of RFC-CDP-033 SS11.8's
five recognition outcomes are reachable (recognized, denied) -- 'narrowed'
is deferred until a future session adds an outcome_scope column, since
writing 'narrowed' without a recorded scope would be enforcement-
indistinguishable from 'recognized'. See
db/ddl/015-standing-and-recusal.sql for the full boundary statement.
"""

from __future__ import annotations

import hashlib
import secrets
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

import psycopg

from cdp.core import db
from cdp.core.repositories import actor_tokens as actor_tokens_repo
from cdp.core.repositories import actors as actors_repo
from cdp.core.repositories import adjudications as adjudications_repo
from cdp.core.repositories import attestations as attestations_repo
from cdp.core.repositories import audit as audit_repo
from cdp.core.repositories import authority as authority_repo
from cdp.core.repositories import challenges as challenges_repo
from cdp.core.repositories import decisions as decisions_repo
from cdp.core.repositories import execution_authorizations as execution_authorizations_repo
from cdp.core.repositories import execution_records as execution_records_repo
from cdp.core.repositories import identity_claims as identity_claims_repo
from cdp.core.repositories import standing as standing_repo
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


class BearerTokenMissing(Exception):
    """No (or a malformed) Authorization: Bearer header was presented."""


class BearerTokenInvalid(Exception):
    """The presented bearer token does not match any active token."""


class BearerTokenActorMismatch(Exception):
    """The presented bearer token belongs to a different actor than asserted."""


class NoActiveBearerToken(Exception):
    """The actor has no active bearer token to revoke."""


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
    """The identity claim's purpose_scope, or (session 030) its optional
    registry/decision-class scope, does not cover the requested governed
    act."""


class AuthorityGrantIssuerRequired(Exception):
    """The issuing/revoking actor is not the seeded authority-grant issuer."""


class AuthorityGrantNotFound(Exception):
    """No authority grant exists for the given grant_id."""


class AuthorityGrantNotActive(Exception):
    """The authority grant is not currently 'active' and cannot be revoked again."""


class AuthorityNotGranted(Exception):
    """No active, unexpired, in-scope authority grant covers this act."""


class StandingClaimNotFound(Exception):
    """No standing claim exists for the given claim_id."""


class StandingStageNotSupported(Exception):
    """This slice's service layer only accepts Standing Claims for the
    'challenge' stage -- see 015-standing-and-recusal.sql's header."""


class StandingTypeNotSupported(Exception):
    """This slice's service layer only accepts
    'constitutional_affected_party' Standing Claims -- see
    015-standing-and-recusal.sql's header."""


class StandingRecognitionAuthorityRequired(Exception):
    """The determining actor is not the seeded Standing recognition
    authority."""


class SelfStandingRecognitionForbidden(Exception):
    """An actor cannot determine its own standing claim, even if it is the
    seeded Standing recognition authority."""


class StandingClaimAlreadyDetermined(Exception):
    """This slice permits exactly one Standing Recognition Determination
    per claim -- see 015-standing-and-recusal.sql's header."""


class StandingClaimActorMismatch(Exception):
    """The standing claim referenced by an attested challenge does not
    belong to the attesting actor."""


class StandingClaimDecisionMismatch(Exception):
    """The standing claim referenced by an attested challenge does not
    match this decision and stage."""


class StandingClaimNotSufficient(Exception):
    """The standing claim referenced by an attested challenge has a
    'denied' determination against it and cannot ground participation.
    A 'recognized' outcome, and a claim with no determination yet (still
    provisional), both permit -- see attest_and_raise_challenge's
    docstring. ('narrowed' is not a reachable outcome in this slice -- see
    the module docstring's Standing paragraph above.)"""


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
        return _raise_challenge_for_decision_in_transaction(cursor, challenge_input)


def _raise_challenge_for_decision_in_transaction(
    cursor: Any, challenge_input: ChallengeInput
) -> dict[str, Any]:
    """Cursor-based body of raise_challenge_for_decision, extracted so
    attest_and_raise_challenge (see the Universal Attestation slice below)
    can run it inside its own single caller-owned transaction, alongside
    attestation/authority checks, without nesting a second
    db.transaction() connection."""
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
        "decision": decision,
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
        return _adjudicate_challenge_in_transaction(cursor, adjudication_input)


def _adjudicate_challenge_in_transaction(
    cursor: Any, adjudication_input: AdjudicationInput
) -> dict[str, Any]:
    """Cursor-based body of adjudicate_challenge, extracted so
    attest_and_adjudicate_challenge can reuse it inside its own single
    caller-owned transaction -- see
    _raise_challenge_for_decision_in_transaction's docstring for why."""
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
        "decision": decision,
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
        return _authorize_execution_in_transaction(cursor, authorization_input)


def _authorize_execution_in_transaction(
    cursor: Any, authorization_input: ExecutionAuthorizationInput
) -> dict[str, Any]:
    """Cursor-based body of authorize_execution, extracted so
    attest_and_authorize_execution can reuse it inside its own single
    caller-owned transaction -- see
    _raise_challenge_for_decision_in_transaction's docstring for why."""
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
        "decision": decision,
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
        return _record_execution_attempt_in_transaction(cursor, execution_input)


def _record_execution_attempt_in_transaction(
    cursor: Any, execution_input: ExecutionRecordInput
) -> dict[str, Any]:
    """Cursor-based body of record_execution_attempt, extracted so
    attest_and_record_execution_attempt can reuse it inside its own single
    caller-owned transaction -- see
    _raise_challenge_for_decision_in_transaction's docstring for why."""
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
        "decision": decision,
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


def _generate_bearer_token() -> tuple[str, str]:
    """Return (plaintext_token, sha256_hex_digest). The plaintext is
    generated here and returned to the caller exactly once (by
    register_actor, below); only the digest is ever persisted -- see
    db/ddl/014-caller-authentication.sql's header."""
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    return token, token_hash


def register_actor(actor_input: ActorInput) -> dict[str, Any]:
    """Register a new governed actor.

    Runs inside exactly one transaction: the underlying identifier_registry
    row, the cdp_core.actor row, a bearer token (session 032, see
    verify_bearer_token below), and the audit event all commit or roll
    back together. Raises ActorAlreadyRegistered if actor_id is already
    registered.

    The returned dict's "bearer_token" key holds the plaintext token --
    this is the only time it is ever available. Callers must record it
    immediately; this system stores only its SHA-256 hash and cannot
    recover the plaintext later.
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

        bearer_token, token_hash = _generate_bearer_token()
        actor_tokens_repo.insert_token(
            cursor, actor_id=actor_input.actor_id, token_hash=token_hash
        )

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

    return {"actor": actor, "bearer_token": bearer_token}


# ---------------------------------------------------------------------------
# Caller Authentication (session 032): binds an HTTP caller to the
# actor_id it asserts in a mutating request, closing the gap RFC-CDP-030
# SS6 and RFC-CDP-031 SS7 both name -- every prior session's proof paths
# accepted a submitted actor_id at face value. verify_bearer_token is a
# standalone boundary check, deliberately not called from inside any
# other service function (register_actor, submit_identity_claim,
# recognize/deny/contest_identity_claim, grant_authority, revoke_authority,
# or any attest_and_* function) so none of their existing signatures,
# behavior, or tests change. Callers -- the API layer, in
# cdp/api/identity.py, authority.py, and decisions.py -- call this first,
# before the underlying service function, on every route that accepts an
# actor-asserting field. See db/ddl/014-caller-authentication.sql and
# docs/session-032-caller-authentication.md for the full boundary
# statement, including what this does and does not prove.
# ---------------------------------------------------------------------------


def verify_bearer_token(*, authorization_header: str | None, expected_actor_id: str) -> None:
    """Verify authorization_header carries a valid, active bearer token
    belonging to expected_actor_id. Raises BearerTokenMissing,
    BearerTokenInvalid, or BearerTokenActorMismatch; returns None on
    success."""
    if not authorization_header or not authorization_header.startswith("Bearer "):
        raise BearerTokenMissing("Missing or malformed Authorization header")

    token = authorization_header[len("Bearer ") :].strip()
    if not token:
        raise BearerTokenMissing("Missing bearer token")

    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    with db.transaction() as cursor:
        token_row = actor_tokens_repo.fetch_token_by_hash(cursor, token_hash=token_hash)

    if token_row is None or token_row["status"] != "active":
        raise BearerTokenInvalid("Bearer token is invalid or has been revoked")

    if token_row["actor_id"] != expected_actor_id:
        raise BearerTokenActorMismatch(
            f"Bearer token does not belong to actor {expected_actor_id!r}"
        )


def revoke_actor_bearer_token(actor_id: str) -> dict[str, Any]:
    """Revoke actor_id's currently active bearer token. Callers must
    verify_bearer_token(expected_actor_id=actor_id) first -- only an
    actor presenting its own current token may revoke it (self-service,
    like a logout); this function itself performs no caller check.
    Raises NoActiveBearerToken if the actor has no active token."""
    with db.transaction() as cursor:
        token = actor_tokens_repo.revoke_active_token_for_actor(cursor, actor_id=actor_id)
        if token is None:
            raise NoActiveBearerToken(f"Actor {actor_id!r} has no active bearer token")

        audit_repo.append_event(
            cursor,
            event_type="actor_bearer_token.revoked",
            aggregate_type="actor",
            aggregate_id=actor_id,
            payload={"actor_id": actor_id, "token_id": str(token["token_id"])},
        )

    return {"actor_bearer_token": token}


@dataclass(frozen=True)
class IdentityClaimInput:
    actor_id: str
    claimant_actor_id: str
    claimed_identity_descriptor: str
    purpose_scope: str
    evidence_refs: list[Any] | None = None
    supersedes_claim_id: uuid.UUID | None = None
    # Optional registry/decision-class scope (session 030) -- see
    # db/ddl/013-identity-claim-scope.sql's header. Omitting both (the
    # default) preserves every pre-session-030 claim's exact behavior:
    # purpose_scope alone governs coverage.
    scope_registry_name: str | None = None
    scope_decision_class_id: str | None = None


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
            scope_registry_name=claim_input.scope_registry_name,
            scope_decision_class_id=claim_input.scope_decision_class_id,
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


# ---------------------------------------------------------------------------
# Authority (RFC-CDP-032), scoped to SS19 Minimal Compliance
# ---------------------------------------------------------------------------
#
# See db/ddl/011-authority-and-delegation.sql's header for the full
# boundary statement. In one line: a governed Authority Grant, a governed
# Authority Evaluation Result, and a single bounded actor who may issue or
# revoke grants -- no delegation, no quorum, no separation-of-duties
# enforcement, no grant types beyond RFC-CDP-032's implicit "direct".

_AUTHORITY_GRANT_ISSUER_ACTOR_ID = "cdp_authority_grant_issuer"
_PROPOSE_AUTHORITY = "PROPOSE"


@dataclass(frozen=True)
class GrantAuthorityInput:
    actor_id: str
    authority: str
    scope_registry_name: str
    expires_at: datetime
    issued_by_actor_id: str
    basis: str
    scope_decision_class_id: str | None = None
    issued_at: datetime | None = None
    effective_at: datetime | None = None


def grant_authority(grant_input: GrantAuthorityInput) -> dict[str, Any]:
    """Issue an Authority Grant. Only the seeded
    _AUTHORITY_GRANT_ISSUER_ACTOR_ID may issue one -- RFC-CDP-032 SS3: "No
    anonymous authority. No ambient authority." Runs inside exactly one
    transaction: the grant row and its audit event commit or roll back
    together.
    """
    if grant_input.issued_by_actor_id != _AUTHORITY_GRANT_ISSUER_ACTOR_ID:
        raise AuthorityGrantIssuerRequired(
            f"Actor {grant_input.issued_by_actor_id!r} is not the authority-grant issuer "
            "and cannot issue authority grants"
        )

    issued_at = grant_input.issued_at or datetime.now(UTC)
    effective_at = grant_input.effective_at or issued_at

    with db.transaction() as cursor:
        actor = actors_repo.fetch_actor(cursor, actor_id=grant_input.actor_id)
        if actor is None:
            raise ActorNotFound(f"No registered actor {grant_input.actor_id!r}")

        grant = authority_repo.insert_grant(
            cursor,
            actor_id=grant_input.actor_id,
            authority=grant_input.authority,
            scope_registry_name=grant_input.scope_registry_name,
            scope_decision_class_id=grant_input.scope_decision_class_id,
            issued_at=issued_at,
            effective_at=effective_at,
            expires_at=grant_input.expires_at,
            issuer_actor_id=grant_input.issued_by_actor_id,
            basis=grant_input.basis,
        )

        audit_repo.append_event(
            cursor,
            event_type="authority_grant.issued",
            aggregate_type="authority_grant",
            aggregate_id=str(grant["authority_grant_id"]),
            payload={
                "actor_id": grant_input.actor_id,
                "authority": grant_input.authority,
                "scope_registry_name": grant_input.scope_registry_name,
                "scope_decision_class_id": grant_input.scope_decision_class_id,
            },
        )

    return {"authority_grant": grant}


@dataclass(frozen=True)
class RevokeAuthorityInput:
    grant_id: uuid.UUID
    revoked_by_actor_id: str
    reason: str


def revoke_authority(revoke_input: RevokeAuthorityInput) -> dict[str, Any]:
    """Revoke an Authority Grant. Only the seeded issuer may revoke, and
    only a currently-'active' grant can be revoked -- revoking an
    already-revoked grant raises AuthorityGrantNotActive rather than
    silently succeeding again. Revocation is a status transition; the row
    is never deleted (cdp_core.authority_grant's forbid-delete trigger).
    """
    if revoke_input.revoked_by_actor_id != _AUTHORITY_GRANT_ISSUER_ACTOR_ID:
        raise AuthorityGrantIssuerRequired(
            f"Actor {revoke_input.revoked_by_actor_id!r} is not the authority-grant issuer "
            "and cannot revoke authority grants"
        )

    with db.transaction() as cursor:
        existing = authority_repo.fetch_grant(cursor, grant_id=revoke_input.grant_id)
        if existing is None:
            raise AuthorityGrantNotFound(f"No authority grant {revoke_input.grant_id}")

        revoked = authority_repo.revoke_grant(
            cursor,
            grant_id=revoke_input.grant_id,
            revoked_by_actor_id=revoke_input.revoked_by_actor_id,
            reason=revoke_input.reason,
        )
        if revoked is None:
            raise AuthorityGrantNotActive(
                f"Authority grant {revoke_input.grant_id} is {existing['status']}, not active"
            )

        audit_repo.append_event(
            cursor,
            event_type="authority_grant.revoked",
            aggregate_type="authority_grant",
            aggregate_id=str(revoke_input.grant_id),
            payload={
                "actor_id": existing["actor_id"],
                "revoked_by_actor_id": revoke_input.revoked_by_actor_id,
                "reason": revoke_input.reason,
            },
        )

    return {"authority_grant": revoked}


# ---------------------------------------------------------------------------
# Standing (RFC-CDP-033), scoped to the narrowest slice that reaches E4:
# Constitutional Affected-Party Standing for the Challenge stage only. See
# db/ddl/015-standing-and-recusal.sql's header for the full boundary
# statement -- in one line: a governed Standing Claim, a governed Standing
# Recognition Determination as a *separate* append-only record (never an
# in-place edit of the claim), a single bounded actor authorized to
# determine claims, and an optional (not mandatory) Standing gate on
# attest_and_raise_challenge -- see that function's docstring below for
# why mandatory would be constitutionally wrong for this slice's scope.
#
# No Recusal is implemented here at all -- RFC-CDP-033 SS7/SS10 remain
# unenforced code.

_STANDING_RECOGNITION_AUTHORITY_ACTOR_ID = "cdp_standing_recognition_authority"
_SUPPORTED_STANDING_STAGE = "challenge"
_SUPPORTED_STANDING_TYPE = "constitutional_affected_party"


@dataclass(frozen=True)
class StandingClaimInput:
    decision_registry_name: str
    decision_id: str
    actor_id: str
    claimed_impact: str
    standing_basis_role: str | None = None
    standing_basis_accountability: str | None = None
    standing_basis_contextual_relationship: str | None = None
    stage: str = _SUPPORTED_STANDING_STAGE
    standing_type: str = _SUPPORTED_STANDING_TYPE


def submit_affected_party_standing_claim(claim_input: StandingClaimInput) -> dict[str, Any]:
    """Submit a Constitutional Affected-Party Standing Claim for the
    Challenge stage of an existing decision.

    Minimal sufficiency (RFC-CDP-033 SS11.4, as clarified in Draft v0.7:
    "identifies a possible consequence and the relationship that makes the
    actor answerable to it") is enforced at the database layer by
    cdp_core.standing_claim's own CHECK constraints, not re-checked here --
    a row that inserts successfully is, by construction, minimally
    sufficient and grounds provisional Standing immediately, independent
    of whether a Standing Recognition Determination is ever made. See
    015-standing-and-recusal.sql's header.

    This slice's service layer accepts only stage='challenge' and
    standing_type='constitutional_affected_party' -- any other value
    raises StandingStageNotSupported / StandingTypeNotSupported rather
    than silently accepting a claim this slice cannot enforce anywhere.

    Runs inside exactly one transaction: the claim row and its audit event
    commit or roll back together.
    """
    if claim_input.stage != _SUPPORTED_STANDING_STAGE:
        raise StandingStageNotSupported(
            f"This slice only accepts Standing Claims for stage "
            f"{_SUPPORTED_STANDING_STAGE!r}, not {claim_input.stage!r}"
        )
    if claim_input.standing_type != _SUPPORTED_STANDING_TYPE:
        raise StandingTypeNotSupported(
            f"This slice only accepts standing_type {_SUPPORTED_STANDING_TYPE!r}, "
            f"not {claim_input.standing_type!r}"
        )

    with db.transaction() as cursor:
        actor = actors_repo.fetch_actor(cursor, actor_id=claim_input.actor_id)
        if actor is None:
            raise ActorNotFound(f"No registered actor {claim_input.actor_id!r}")

        decision = decisions_repo.fetch_decision(
            cursor,
            registry_name=claim_input.decision_registry_name,
            decision_id=claim_input.decision_id,
        )
        if decision is None:
            raise DecisionNotFound(
                f"No decision {claim_input.decision_registry_name}.{claim_input.decision_id}"
            )

        claim = standing_repo.insert_claim(
            cursor,
            decision_registry_name=claim_input.decision_registry_name,
            decision_id=claim_input.decision_id,
            stage=claim_input.stage,
            actor_id=claim_input.actor_id,
            standing_type=claim_input.standing_type,
            claimed_impact=claim_input.claimed_impact,
            standing_basis_role=claim_input.standing_basis_role,
            standing_basis_accountability=claim_input.standing_basis_accountability,
            standing_basis_contextual_relationship=claim_input.standing_basis_contextual_relationship,
        )

        audit_repo.append_event(
            cursor,
            event_type="standing_claim.submitted",
            aggregate_type="standing_claim",
            aggregate_id=str(claim["claim_id"]),
            payload={
                "actor_id": claim_input.actor_id,
                "decision_registry_name": claim_input.decision_registry_name,
                "decision_id": claim_input.decision_id,
                "stage": claim_input.stage,
                "standing_type": claim_input.standing_type,
            },
        )

    return {"standing_claim": claim}


@dataclass(frozen=True)
class StandingDeterminationInput:
    claim_id: uuid.UUID
    determined_by_actor_id: str
    outcome_basis: str


def _determine_standing_claim(
    determination_input: StandingDeterminationInput,
    *,
    outcome: str,
    event_type: str,
) -> dict[str, Any]:
    """Shared fetch/authorize/determine/audit body for
    recognize/deny_standing_claim.

    Two authorization checks run before any write, mirroring
    _decide_identity_claim exactly:

    1. the determining actor must be the seeded
       _STANDING_RECOGNITION_AUTHORITY_ACTOR_ID (fails closed with
       StandingRecognitionAuthorityRequired otherwise);
    2. the determining actor must not be the claim's own claimant (fails
       closed with SelfStandingRecognitionForbidden otherwise).

    This slice permits exactly one determination per claim
    (cdp_core.standing_recognition_determination's UNIQUE(claim_id)) --
    a second attempt raises StandingClaimAlreadyDetermined rather than
    silently overwriting the first (which the schema would not even
    permit, since determinations are never updated in place).
    """
    with db.transaction() as cursor:
        claim = standing_repo.fetch_claim(cursor, claim_id=determination_input.claim_id)
        if claim is None:
            raise StandingClaimNotFound(f"No standing claim {determination_input.claim_id}")

        determiner = actors_repo.fetch_actor(
            cursor, actor_id=determination_input.determined_by_actor_id
        )
        if determiner is None:
            raise ActorNotFound(
                f"No registered actor {determination_input.determined_by_actor_id!r}"
            )

        if determination_input.determined_by_actor_id != _STANDING_RECOGNITION_AUTHORITY_ACTOR_ID:
            raise StandingRecognitionAuthorityRequired(
                f"Actor {determination_input.determined_by_actor_id!r} is not the Standing "
                "recognition authority and cannot determine standing claims"
            )

        if determination_input.determined_by_actor_id == claim["actor_id"]:
            raise SelfStandingRecognitionForbidden(
                f"Actor {determination_input.determined_by_actor_id!r} cannot determine its "
                "own standing claim"
            )

        existing_determination = standing_repo.fetch_determination_for_claim(
            cursor, claim_id=determination_input.claim_id
        )
        if existing_determination is not None:
            raise StandingClaimAlreadyDetermined(
                f"Standing claim {determination_input.claim_id} already has a "
                f"{existing_determination['outcome']!r} determination"
            )

        determination = standing_repo.insert_determination(
            cursor,
            claim_id=determination_input.claim_id,
            outcome=outcome,
            outcome_basis=determination_input.outcome_basis,
            determined_by_actor_id=determination_input.determined_by_actor_id,
        )

        audit_repo.append_event(
            cursor,
            event_type=event_type,
            aggregate_type="standing_recognition_determination",
            aggregate_id=str(determination["determination_id"]),
            payload={
                "claim_id": str(determination_input.claim_id),
                "actor_id": claim["actor_id"],
                "determined_by_actor_id": determination_input.determined_by_actor_id,
                "outcome": outcome,
            },
        )

    return {"standing_recognition_determination": determination}


def recognize_standing_claim(determination_input: StandingDeterminationInput) -> dict[str, Any]:
    """Recognize a standing claim as presented. See
    _determine_standing_claim for the shared fetch/determine/audit shape."""
    return _determine_standing_claim(
        determination_input,
        outcome="recognized",
        event_type="standing_claim.recognized",
    )


# No narrow_standing_claim in this slice, deliberately (review finding on
# PR #53): RFC-CDP-033 SS9.2's determination schema includes outcome_scope
# to record what a 'narrowed' outcome actually narrows to, and this
# table's SS9.2 implementation omits that column. Writing a 'narrowed'
# determination without a recorded scope would be indistinguishable from
# 'recognized' at the attest_and_raise_challenge gate while still
# asserting a narrowing the system cannot describe -- a truth problem, not
# just a missing feature. 'narrowed' remains seeded in the
# standing_recognition_outcome vocabulary and forbidden by
# cdp_core.standing_recognition_determination's own CHECK constraint
# (015-standing-and-recusal.sql) until a future session adds outcome_scope
# and teaches the gate to honor it.


def deny_standing_claim(determination_input: StandingDeterminationInput) -> dict[str, Any]:
    """Deny a standing claim that cleared minimal sufficiency but is
    refused recognition (RFC-CDP-033 SS11.8's precise 'denied' meaning).
    This does NOT automatically generate a Breach Record -- RFC-CDP-033
    SS11.6's automatic Breach Record rule is explicitly deferred to a
    future session, since RFC-CDP-072 (Breach Record and Repair Agenda
    Schema) itself remains E0 in this repository. See
    docs/session-035-affected-party-standing-challenge.md for why this is
    a named non-goal, not a silent omission."""
    return _determine_standing_claim(
        determination_input,
        outcome="denied",
        event_type="standing_claim.denied",
    )


def _evaluate_authority(
    cursor: Any,
    *,
    actor_id: str,
    authority: str,
    scope_registry_name: str,
    scope_decision_class_id: str,
    at_time: datetime,
) -> tuple[str, uuid.UUID | None, str | None]:
    """Cursor-based authority evaluation, run inside an attest_and_*
    function's transaction. Returns (result, matched_grant_id,
    failure_reason) -- does not itself raise or persist anything; the
    caller decides both, since whether to persist depends on whether the
    governed act this evaluation gates ends up performed.
    """
    matches = authority_repo.fetch_active_grants_for_actor(
        cursor,
        actor_id=actor_id,
        authority=authority,
        scope_registry_name=scope_registry_name,
        scope_decision_class_id=scope_decision_class_id,
        at_time=at_time,
    )
    if not matches:
        return (
            "fail",
            None,
            f"No active, unexpired {authority} grant covers "
            f"{scope_registry_name}.{scope_decision_class_id} for actor {actor_id!r}",
        )
    return ("pass", matches[0]["authority_grant_id"], None)


def _check_actor_active(cursor: Any, actor_id: str) -> dict[str, Any]:
    """Shared actor-existence/activeness check used by every attest_and_*
    function. Raises ActorNotFound / ActorNotActive; returns the actor row
    on success."""
    actor = actors_repo.fetch_actor(cursor, actor_id=actor_id)
    if actor is None:
        raise ActorNotFound(f"No registered actor {actor_id!r}")
    if actor["actor_status"] != "active":
        raise ActorNotActive(f"Actor {actor_id!r} is {actor['actor_status']}, not active")
    return actor


def _check_claim_recognized_and_scoped(
    cursor: Any,
    *,
    claim_id: uuid.UUID,
    actor_id: str,
    required_purpose_scope: str,
    scope_registry_name: str,
    scope_decision_class_id: str,
) -> dict[str, Any]:
    """Shared identity-claim ownership/recognition/scope check used by
    every attest_and_* function. Raises IdentityClaimActorMismatch /
    IdentityClaimNotRecognized / IdentityClaimScopeInsufficient; returns
    the claim row on success.

    Beyond the purpose_scope check, if the claim itself carries a
    scope_registry_name (nullable -- see
    db/ddl/013-identity-claim-scope.sql), the governed act's
    scope_registry_name/scope_decision_class_id (the same values the
    caller separately passes to _evaluate_authority) must also match:
    exact registry, and exact decision class unless the claim's
    scope_decision_class_id is NULL (wildcard). A claim with
    scope_registry_name NULL is not scoped to any particular registry, so
    this additional check is skipped -- purpose_scope alone governs, the
    same behavior every claim had before session 030.
    """
    claim = identity_claims_repo.fetch_claim(cursor, claim_id=claim_id)
    if claim is None or claim["actor_id"] != actor_id:
        raise IdentityClaimActorMismatch(
            f"Identity claim {claim_id} does not belong to actor {actor_id!r}"
        )
    if claim["recognition_status"] != "recognized":
        raise IdentityClaimNotRecognized(
            f"Identity claim {claim_id} is {claim['recognition_status']}, not recognized"
        )
    if claim["purpose_scope"] != required_purpose_scope:
        raise IdentityClaimScopeInsufficient(
            f"Identity claim {claim_id} has purpose_scope {claim['purpose_scope']!r}, "
            f"which does not cover {required_purpose_scope!r}"
        )
    if claim["scope_registry_name"] is not None:
        if claim["scope_registry_name"] != scope_registry_name:
            raise IdentityClaimScopeInsufficient(
                f"Identity claim {claim_id} is scoped to registry "
                f"{claim['scope_registry_name']!r}, which does not cover "
                f"{scope_registry_name!r}"
            )
        if (
            claim["scope_decision_class_id"] is not None
            and claim["scope_decision_class_id"] != scope_decision_class_id
        ):
            raise IdentityClaimScopeInsufficient(
                f"Identity claim {claim_id} is scoped to decision class "
                f"{claim['scope_decision_class_id']!r} within registry "
                f"{claim['scope_registry_name']!r}, which does not cover "
                f"{scope_decision_class_id!r}"
            )
    return claim


def _persist_attestation_and_authority(
    cursor: Any,
    *,
    actor_id: str,
    identity_claim_id: uuid.UUID,
    governed_act_type: str,
    governed_act_registry_name: str,
    governed_act_decision_id: str,
    governed_act_ref_id: uuid.UUID | None,
    attestation_method: str,
    credential_reference: str,
    issued_at: datetime,
    required_authority: str,
    matched_authority_grant_id: uuid.UUID | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Shared attestation-record + authority-evaluation-result persist,
    each with its own audit event in that causal order, used by every
    attest_and_* function after its governed act has been performed. Both
    rows share the same governed_act_registry_name/decision_id/ref_id so
    both are discoverable together from the decision (or, via
    governed_act_ref_id, the specific sub-record)."""
    attestation = attestations_repo.insert_attestation(
        cursor,
        actor_id=actor_id,
        identity_claim_id=identity_claim_id,
        governed_act_type=governed_act_type,
        governed_act_registry_name=governed_act_registry_name,
        governed_act_decision_id=governed_act_decision_id,
        governed_act_ref_id=governed_act_ref_id,
        attestation_method=attestation_method,
        credential_reference=credential_reference,
        issued_at=issued_at,
        verifier_actor_id="cdp_attestation_service",
    )

    audit_repo.append_event(
        cursor,
        event_type="attestation.recorded",
        aggregate_type="attestation_record",
        aggregate_id=str(attestation["attestation_id"]),
        payload={
            "registry_name": governed_act_registry_name,
            "decision_id": governed_act_decision_id,
            "governed_act_type": governed_act_type,
            "governed_act_ref_id": str(governed_act_ref_id) if governed_act_ref_id else None,
            "actor_id": actor_id,
            "identity_claim_id": str(identity_claim_id),
            "attestation_method": attestation_method,
        },
    )

    authority_evaluation = authority_repo.insert_evaluation_result(
        cursor,
        actor_id=actor_id,
        required_authority=required_authority,
        governed_act_type=governed_act_type,
        governed_act_registry_name=governed_act_registry_name,
        governed_act_decision_id=governed_act_decision_id,
        governed_act_ref_id=governed_act_ref_id,
        matched_authority_grant_id=matched_authority_grant_id,
        result="pass",
        failure_reason=None,
    )

    audit_repo.append_event(
        cursor,
        event_type="authority.evaluated",
        aggregate_type="authority_evaluation_result",
        aggregate_id=str(authority_evaluation["authority_evaluation_id"]),
        payload={
            "registry_name": governed_act_registry_name,
            "decision_id": governed_act_decision_id,
            "governed_act_type": governed_act_type,
            "governed_act_ref_id": str(governed_act_ref_id) if governed_act_ref_id else None,
            "actor_id": actor_id,
            "required_authority": required_authority,
            "matched_authority_grant_id": str(matched_authority_grant_id),
            "result": "pass",
        },
    )

    return attestation, authority_evaluation


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

    Between the identity/attestation checks and decision creation, this
    function also evaluates whether the attesting actor holds an active,
    unexpired PROPOSE authority grant scoped to the decision's
    registry_name and decision_class_id (exact match, or a grant with
    scope_decision_class_id NULL as a registry-wide wildcard) -- see
    db/ddl/011-authority-and-delegation.sql. This completes the ordering
    architecture/001 prescribes (Identify + Attest -> Authority -> ...
    -> Propose) for this one proof path; it does not introduce a second,
    competing decision-creation route. Existing callers of this same
    function/route from before the Authority slice must now also hold a
    matching grant, or the call fails closed with AuthorityNotGranted --
    a deliberate, documented behavior change to the one proof path this
    project has been building across sessions 027 and 028, not a breaking
    change to a stable external contract.

    Everything below runs inside exactly one transaction, reusing
    _create_decision_with_workflow_in_transaction so decision creation is
    not a nested/second transaction. Any failure - an unknown or inactive
    actor, a missing/unrecognized/out-of-scope identity claim, missing
    authority, or any failure from decision creation itself - rolls back
    all of it: no decision, no workflow instance, no task, no attestation
    record, no authority evaluation record, and no audit event survive.

    This is the proof path required by the Identity and Attestation slice.
    It is additive: POST /decisions (create_decision_with_workflow) is
    unchanged and continues to accept unattested, unauthorized decisions,
    exactly as every existing caller and test already expects. Only this
    new path requires attestation and authority.
    """
    decision_input = attested_input.decision_input
    attestation_input = attested_input.attestation_input

    with db.transaction() as cursor:
        _check_actor_active(cursor, attestation_input.actor_id)
        _check_claim_recognized_and_scoped(
            cursor,
            claim_id=attestation_input.identity_claim_id,
            actor_id=attestation_input.actor_id,
            required_purpose_scope=_DECISION_CREATION_PURPOSE_SCOPE,
            scope_registry_name=decision_input.registry_name,
            scope_decision_class_id=decision_input.decision_class_id,
        )

        authority_result, matched_grant_id, authority_failure_reason = _evaluate_authority(
            cursor,
            actor_id=attestation_input.actor_id,
            authority=_PROPOSE_AUTHORITY,
            scope_registry_name=decision_input.registry_name,
            scope_decision_class_id=decision_input.decision_class_id,
            at_time=datetime.now(UTC),
        )
        if authority_result == "fail":
            raise AuthorityNotGranted(authority_failure_reason)

        decision_result = _create_decision_with_workflow_in_transaction(cursor, decision_input)

        attestation, authority_evaluation = _persist_attestation_and_authority(
            cursor,
            actor_id=attestation_input.actor_id,
            identity_claim_id=attestation_input.identity_claim_id,
            governed_act_type="decision_created",
            governed_act_registry_name=decision_input.registry_name,
            governed_act_decision_id=decision_input.decision_id,
            governed_act_ref_id=None,
            attestation_method=attestation_input.attestation_method,
            credential_reference=attestation_input.credential_reference,
            issued_at=attestation_input.issued_at,
            required_authority=_PROPOSE_AUTHORITY,
            matched_authority_grant_id=matched_grant_id,
        )

    return {
        **decision_result,
        "attestation": attestation,
        "authority_evaluation": authority_evaluation,
    }


# ---------------------------------------------------------------------------
# Universal Attestation (RFC-CDP-031 SS2: "All mutating acts MUST be
# attested"), extending the attest+authority proof path from decision
# creation alone to the other mutating governed acts this repository
# already implements: raising a challenge, adjudicating a challenge,
# authorizing execution, and recording an execution attempt.
#
# "Universal" means "every mutating act this repository's canonical
# implementation path already has a governed service function for" -- it
# does not reach Test/Legitimize/Learn (unimplemented) and it does not
# reach the Identity/Attestation/Authority slices' own mutations
# (register_actor, submit_identity_claim, recognize/deny/
# contest_identity_claim, grant_authority, revoke_authority), which would
# be circular: they are the foundation attestation depends on, not acts
# attestation can be layered on top of. See
# db/ddl/012-universal-attestation.sql and
# docs/session-029-universal-attestation.md for the full boundary
# statement.
#
# Each function below follows the exact shape attest_and_create_decision
# established: check actor, check identity claim (its own purpose_scope
# per act type), evaluate authority (its own authority type per act
# type), perform the underlying governed act via the extracted
# _..._in_transaction helper, then persist attestation + authority
# evaluation via _persist_attestation_and_authority, all inside one
# transaction. Each is additive: the underlying unattested route/function
# (raise_challenge_for_decision, adjudicate_challenge, authorize_execution,
# record_execution_attempt) is completely untouched, exactly like
# POST /decisions remained untouched by attest_and_create_decision.
# ---------------------------------------------------------------------------

_CHALLENGE_RAISING_PURPOSE_SCOPE = "challenge_raising"
_CHALLENGE_ADJUDICATION_PURPOSE_SCOPE = "challenge_adjudication"
_EXECUTION_AUTHORIZATION_PURPOSE_SCOPE = "execution_authorization"
_EXECUTION_RECORDING_PURPOSE_SCOPE = "execution_recording"

_CHALLENGE_AUTHORITY = "CHALLENGE"
_ADJUDICATE_AUTHORITY = "ADJUDICATE"
_AUTHORIZE_EXECUTION_AUTHORITY = "AUTHORIZE_EXECUTION"
_RECORD_AUTHORITY = "RECORD"


@dataclass(frozen=True)
class AttestedChallengeInput:
    challenge_input: ChallengeInput
    attestation_input: AttestationInput
    # Optional: a Standing Claim (see the Standing section above) the
    # attesting actor asserts grounds this specific challenge as an
    # affected party. Deliberately not required -- see
    # attest_and_raise_challenge's docstring below for why a mandatory
    # gate would be constitutionally wrong for this slice's scope.
    standing_claim_id: uuid.UUID | None = None


def attest_and_raise_challenge(attested_input: AttestedChallengeInput) -> dict[str, Any]:
    """Attest a challenge-raising act to an actor, then raise the challenge.

    Requires the attesting actor to hold a recognized identity claim
    scoped to 'challenge_raising' and an active, unexpired CHALLENGE
    authority grant scoped to the decision's registry_name/
    decision_class_id, evaluated before the challenge is raised so a
    failure leaves nothing persisted. See the Universal Attestation
    section header above for the shared shape every attest_and_* function
    follows.

    Standing gate (RFC-CDP-033, session 035), optional: RFC-CDP-033 SS6's
    stage-specific Standing matrix names several distinct bases for
    Challenge standing (affected party, domain expert, governance
    authority) -- this slice implements only Affected-Party Standing.
    Making a standing_claim_id mandatory for every caller would therefore
    functionally deny standing to every legitimate non-affected-party
    challenger this slice does not model, which is exactly what
    RFC-CDP-033 SS11.2 forbids (non-recognition must never be read as
    non-existence). So the gate only runs when attested_input.standing_claim_id
    is supplied -- an actor asserting a basis this slice doesn't track
    continues to rely solely on the Identity/Authority checks above,
    unchanged from before this slice existed.

    When a standing_claim_id IS supplied, three checks run, in order,
    before the challenge is raised:

    1. the claim must belong to the attesting actor
       (StandingClaimActorMismatch otherwise);
    2. the claim must match this decision and the 'challenge' stage
       (StandingClaimDecisionMismatch otherwise);
    3. the claim must not have a 'denied' determination against it
       (StandingClaimNotSufficient otherwise). A claim with no
       determination yet (still provisional -- RFC-CDP-033 SS11.4), or
       with a 'recognized' determination, both permit -- provisional
       Standing from a minimally sufficient claim is sufficient to raise
       this, the first protected act, without waiting on binding
       recognition. Minimal sufficiency itself is never re-checked here --
       it is already guaranteed by cdp_core.standing_claim's own CHECK
       constraints at claim-submission time (015-standing-and-recusal.sql).
       ('narrowed' is not a reachable outcome in this slice -- see the
       module docstring's Standing paragraph above and
       recognize_standing_claim's neighboring comment for why.)

    A successful exercise of a standing claim is recorded as its own audit
    event (standing_claim.exercised), linking the claim to the resulting
    challenge, in addition to the usual attestation/authority audit trail.
    """
    challenge_input = attested_input.challenge_input
    attestation_input = attested_input.attestation_input

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

        _check_actor_active(cursor, attestation_input.actor_id)
        _check_claim_recognized_and_scoped(
            cursor,
            claim_id=attestation_input.identity_claim_id,
            actor_id=attestation_input.actor_id,
            required_purpose_scope=_CHALLENGE_RAISING_PURPOSE_SCOPE,
            scope_registry_name=challenge_input.registry_name,
            scope_decision_class_id=decision["decision_class_id"],
        )

        standing_claim = None
        if attested_input.standing_claim_id is not None:
            standing_claim = standing_repo.fetch_claim(
                cursor, claim_id=attested_input.standing_claim_id
            )
            if standing_claim is None or standing_claim["actor_id"] != attestation_input.actor_id:
                raise StandingClaimActorMismatch(
                    f"Standing claim {attested_input.standing_claim_id} does not belong to "
                    f"actor {attestation_input.actor_id!r}"
                )
            if (
                standing_claim["decision_registry_name"] != challenge_input.registry_name
                or standing_claim["decision_id"] != challenge_input.decision_id
                or standing_claim["stage"] != _SUPPORTED_STANDING_STAGE
            ):
                raise StandingClaimDecisionMismatch(
                    f"Standing claim {attested_input.standing_claim_id} does not match "
                    f"decision {challenge_input.registry_name}.{challenge_input.decision_id} "
                    f"at stage {_SUPPORTED_STANDING_STAGE!r}"
                )
            determination = standing_repo.fetch_determination_for_claim(
                cursor, claim_id=attested_input.standing_claim_id
            )
            if determination is not None and determination["outcome"] == "denied":
                raise StandingClaimNotSufficient(
                    f"Standing claim {attested_input.standing_claim_id} has a 'denied' "
                    "determination and cannot ground this challenge"
                )

        authority_result, matched_grant_id, authority_failure_reason = _evaluate_authority(
            cursor,
            actor_id=attestation_input.actor_id,
            authority=_CHALLENGE_AUTHORITY,
            scope_registry_name=challenge_input.registry_name,
            scope_decision_class_id=decision["decision_class_id"],
            at_time=datetime.now(UTC),
        )
        if authority_result == "fail":
            raise AuthorityNotGranted(authority_failure_reason)

        challenge_result = _raise_challenge_for_decision_in_transaction(cursor, challenge_input)

        attestation, authority_evaluation = _persist_attestation_and_authority(
            cursor,
            actor_id=attestation_input.actor_id,
            identity_claim_id=attestation_input.identity_claim_id,
            governed_act_type="challenge_raised",
            governed_act_registry_name=challenge_input.registry_name,
            governed_act_decision_id=challenge_input.decision_id,
            governed_act_ref_id=challenge_result["challenge"]["challenge_id"],
            attestation_method=attestation_input.attestation_method,
            credential_reference=attestation_input.credential_reference,
            issued_at=attestation_input.issued_at,
            required_authority=_CHALLENGE_AUTHORITY,
            matched_authority_grant_id=matched_grant_id,
        )

        if standing_claim is not None:
            audit_repo.append_event(
                cursor,
                event_type="standing_claim.exercised",
                aggregate_type="standing_claim",
                aggregate_id=str(standing_claim["claim_id"]),
                payload={
                    "actor_id": attestation_input.actor_id,
                    "registry_name": challenge_input.registry_name,
                    "decision_id": challenge_input.decision_id,
                    "challenge_id": str(challenge_result["challenge"]["challenge_id"]),
                },
            )

    return {
        **challenge_result,
        "attestation": attestation,
        "authority_evaluation": authority_evaluation,
        "standing_claim": standing_claim,
    }


@dataclass(frozen=True)
class AttestedAdjudicationInput:
    adjudication_input: AdjudicationInput
    attestation_input: AttestationInput


def attest_and_adjudicate_challenge(attested_input: AttestedAdjudicationInput) -> dict[str, Any]:
    """Attest a challenge-adjudication act to an actor, then adjudicate the
    challenge. Requires a recognized identity claim scoped to
    'challenge_adjudication' and an active, unexpired ADJUDICATE authority
    grant -- see attest_and_raise_challenge's docstring for the shared
    shape."""
    adjudication_input = attested_input.adjudication_input
    attestation_input = attested_input.attestation_input

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

        _check_actor_active(cursor, attestation_input.actor_id)
        _check_claim_recognized_and_scoped(
            cursor,
            claim_id=attestation_input.identity_claim_id,
            actor_id=attestation_input.actor_id,
            required_purpose_scope=_CHALLENGE_ADJUDICATION_PURPOSE_SCOPE,
            scope_registry_name=adjudication_input.registry_name,
            scope_decision_class_id=decision["decision_class_id"],
        )

        authority_result, matched_grant_id, authority_failure_reason = _evaluate_authority(
            cursor,
            actor_id=attestation_input.actor_id,
            authority=_ADJUDICATE_AUTHORITY,
            scope_registry_name=adjudication_input.registry_name,
            scope_decision_class_id=decision["decision_class_id"],
            at_time=datetime.now(UTC),
        )
        if authority_result == "fail":
            raise AuthorityNotGranted(authority_failure_reason)

        adjudication_result = _adjudicate_challenge_in_transaction(cursor, adjudication_input)

        attestation, authority_evaluation = _persist_attestation_and_authority(
            cursor,
            actor_id=attestation_input.actor_id,
            identity_claim_id=attestation_input.identity_claim_id,
            governed_act_type="challenge_adjudicated",
            governed_act_registry_name=adjudication_input.registry_name,
            governed_act_decision_id=adjudication_input.decision_id,
            governed_act_ref_id=adjudication_result["adjudication"]["adjudication_id"],
            attestation_method=attestation_input.attestation_method,
            credential_reference=attestation_input.credential_reference,
            issued_at=attestation_input.issued_at,
            required_authority=_ADJUDICATE_AUTHORITY,
            matched_authority_grant_id=matched_grant_id,
        )

    return {
        **adjudication_result,
        "attestation": attestation,
        "authority_evaluation": authority_evaluation,
    }


@dataclass(frozen=True)
class AttestedExecutionAuthorizationInput:
    authorization_input: ExecutionAuthorizationInput
    attestation_input: AttestationInput


def attest_and_authorize_execution(
    attested_input: AttestedExecutionAuthorizationInput,
) -> dict[str, Any]:
    """Attest an execution-authorization act to an actor, then authorize
    execution. Requires a recognized identity claim scoped to
    'execution_authorization' and an active, unexpired AUTHORIZE_EXECUTION
    authority grant -- see attest_and_raise_challenge's docstring for the
    shared shape."""
    authorization_input = attested_input.authorization_input
    attestation_input = attested_input.attestation_input

    with db.transaction() as cursor:
        decision = decisions_repo.fetch_decision(
            cursor,
            registry_name=authorization_input.registry_name,
            decision_id=authorization_input.decision_id,
        )
        if decision is None:
            raise DecisionNotFound(
                f"No decision {authorization_input.registry_name}."
                f"{authorization_input.decision_id}"
            )

        _check_actor_active(cursor, attestation_input.actor_id)
        _check_claim_recognized_and_scoped(
            cursor,
            claim_id=attestation_input.identity_claim_id,
            actor_id=attestation_input.actor_id,
            required_purpose_scope=_EXECUTION_AUTHORIZATION_PURPOSE_SCOPE,
            scope_registry_name=authorization_input.registry_name,
            scope_decision_class_id=decision["decision_class_id"],
        )

        authority_result, matched_grant_id, authority_failure_reason = _evaluate_authority(
            cursor,
            actor_id=attestation_input.actor_id,
            authority=_AUTHORIZE_EXECUTION_AUTHORITY,
            scope_registry_name=authorization_input.registry_name,
            scope_decision_class_id=decision["decision_class_id"],
            at_time=datetime.now(UTC),
        )
        if authority_result == "fail":
            raise AuthorityNotGranted(authority_failure_reason)

        authorization_result = _authorize_execution_in_transaction(cursor, authorization_input)

        attestation, authority_evaluation = _persist_attestation_and_authority(
            cursor,
            actor_id=attestation_input.actor_id,
            identity_claim_id=attestation_input.identity_claim_id,
            governed_act_type="execution_authorized",
            governed_act_registry_name=authorization_input.registry_name,
            governed_act_decision_id=authorization_input.decision_id,
            governed_act_ref_id=authorization_result["authorization"]["authorization_id"],
            attestation_method=attestation_input.attestation_method,
            credential_reference=attestation_input.credential_reference,
            issued_at=attestation_input.issued_at,
            required_authority=_AUTHORIZE_EXECUTION_AUTHORITY,
            matched_authority_grant_id=matched_grant_id,
        )

    return {
        **authorization_result,
        "attestation": attestation,
        "authority_evaluation": authority_evaluation,
    }


@dataclass(frozen=True)
class AttestedExecutionRecordInput:
    execution_input: ExecutionRecordInput
    attestation_input: AttestationInput


def attest_and_record_execution_attempt(
    attested_input: AttestedExecutionRecordInput,
) -> dict[str, Any]:
    """Attest an execution-recording act to an actor, then record the
    execution attempt. Requires a recognized identity claim scoped to
    'execution_recording' and an active, unexpired RECORD authority grant
    -- see attest_and_raise_challenge's docstring for the shared shape."""
    execution_input = attested_input.execution_input
    attestation_input = attested_input.attestation_input

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

        _check_actor_active(cursor, attestation_input.actor_id)
        _check_claim_recognized_and_scoped(
            cursor,
            claim_id=attestation_input.identity_claim_id,
            actor_id=attestation_input.actor_id,
            required_purpose_scope=_EXECUTION_RECORDING_PURPOSE_SCOPE,
            scope_registry_name=execution_input.registry_name,
            scope_decision_class_id=decision["decision_class_id"],
        )

        authority_result, matched_grant_id, authority_failure_reason = _evaluate_authority(
            cursor,
            actor_id=attestation_input.actor_id,
            authority=_RECORD_AUTHORITY,
            scope_registry_name=execution_input.registry_name,
            scope_decision_class_id=decision["decision_class_id"],
            at_time=datetime.now(UTC),
        )
        if authority_result == "fail":
            raise AuthorityNotGranted(authority_failure_reason)

        execution_result = _record_execution_attempt_in_transaction(cursor, execution_input)

        attestation, authority_evaluation = _persist_attestation_and_authority(
            cursor,
            actor_id=attestation_input.actor_id,
            identity_claim_id=attestation_input.identity_claim_id,
            governed_act_type="execution_recorded",
            governed_act_registry_name=execution_input.registry_name,
            governed_act_decision_id=execution_input.decision_id,
            governed_act_ref_id=execution_result["execution_record"]["execution_id"],
            attestation_method=attestation_input.attestation_method,
            credential_reference=attestation_input.credential_reference,
            issued_at=attestation_input.issued_at,
            required_authority=_RECORD_AUTHORITY,
            matched_authority_grant_id=matched_grant_id,
        )

    return {
        **execution_result,
        "attestation": attestation,
        "authority_evaluation": authority_evaluation,
    }
