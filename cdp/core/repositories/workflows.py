"""Repository for cdp_core.workflow_definition/workflow_stage/workflow_instance/workflow_task.

Active workflow selection is entirely data-driven: callers resolve the
workflow applicable to a decision class through
workflow_definition.applies_to_registry_name /
applies_to_decision_class_id. Nothing here hardcodes a workflow_code.
"""

from __future__ import annotations

import uuid
from typing import Any

import psycopg
from psycopg.rows import DictRow


def resolve_active_workflow_for_class(
    cursor: psycopg.Cursor[DictRow], *, registry_name: str, decision_class_id: str
) -> dict[str, Any] | None:
    cursor.execute(
        """
        SELECT *
        FROM cdp_core.workflow_definition
        WHERE applies_to_registry_name = %(registry_name)s
          AND applies_to_decision_class_id = %(decision_class_id)s
          AND status = 'active'
        ORDER BY updated_at DESC
        LIMIT 1
        """,
        {"registry_name": registry_name, "decision_class_id": decision_class_id},
    )
    return cursor.fetchone()


def resolve_first_stage(
    cursor: psycopg.Cursor[DictRow], *, workflow_definition_id: uuid.UUID
) -> dict[str, Any] | None:
    cursor.execute(
        """
        SELECT *
        FROM cdp_core.workflow_stage
        WHERE workflow_definition_id = %(workflow_definition_id)s
          AND stage_order = 1
        """,
        {"workflow_definition_id": workflow_definition_id},
    )
    return cursor.fetchone()


def insert_workflow_instance(
    cursor: psycopg.Cursor[DictRow],
    *,
    registry_name: str,
    decision_id: str,
    workflow_definition_id: uuid.UUID,
    current_stage_id: uuid.UUID,
    lifecycle_stage: str,
    workflow_status: str = "active",
) -> dict[str, Any]:
    cursor.execute(
        """
        INSERT INTO cdp_core.workflow_instance (
            registry_name, decision_id, workflow_definition_id,
            current_stage_id, lifecycle_stage, workflow_status
        )
        VALUES (
            %(registry_name)s, %(decision_id)s, %(workflow_definition_id)s,
            %(current_stage_id)s, %(lifecycle_stage)s, %(workflow_status)s
        )
        RETURNING *
        """,
        {
            "registry_name": registry_name,
            "decision_id": decision_id,
            "workflow_definition_id": workflow_definition_id,
            "current_stage_id": current_stage_id,
            "lifecycle_stage": lifecycle_stage,
            "workflow_status": workflow_status,
        },
    )
    row = cursor.fetchone()
    assert row is not None
    return row


def insert_initial_task(
    cursor: psycopg.Cursor[DictRow],
    *,
    workflow_instance_id: uuid.UUID,
    registry_name: str,
    decision_id: str,
    task_type: str = "review_decision",
    assigned_role: str = "human_reviewer",
    blocking: bool = True,
) -> dict[str, Any]:
    cursor.execute(
        """
        INSERT INTO cdp_core.workflow_task (
            workflow_instance_id, registry_name, decision_id,
            assigned_role, task_type, blocking
        )
        VALUES (
            %(workflow_instance_id)s, %(registry_name)s, %(decision_id)s,
            %(assigned_role)s, %(task_type)s, %(blocking)s
        )
        RETURNING *
        """,
        {
            "workflow_instance_id": workflow_instance_id,
            "registry_name": registry_name,
            "decision_id": decision_id,
            "assigned_role": assigned_role,
            "task_type": task_type,
            "blocking": blocking,
        },
    )
    row = cursor.fetchone()
    assert row is not None
    return row
