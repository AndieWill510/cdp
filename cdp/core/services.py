"""Domain services for the live CDP core.

create_decision_with_workflow is the smallest executable decision vertical
slice: create a decision, start its configured workflow, and open the
initial blocking review task, all inside one transaction with a matching
audit trail.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from cdp.core import db
from cdp.core.repositories import audit as audit_repo
from cdp.core.repositories import decisions as decisions_repo
from cdp.core.repositories import workflows as workflows_repo


class DecisionClassNotConfigured(Exception):
    """No active workflow is configured for the decision's registry/class."""


class WorkflowStageNotConfigured(Exception):
    """The resolved workflow has no stage_order = 1 stage."""


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

        task = workflows_repo.insert_initial_task(
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
