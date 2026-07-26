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
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from cdp.core import db
from cdp.core.repositories import adjudications as adjudications_repo
from cdp.core.repositories import audit as audit_repo
from cdp.core.repositories import challenges as challenges_repo
from cdp.core.repositories import decisions as decisions_repo
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
    created = decision_input.created or datetime.now(UTC)

    with db.transaction() as cursor:
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
