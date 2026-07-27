"""Repository for cdp_core.execution_authorization_record."""

from __future__ import annotations

import uuid
from typing import Any

import psycopg
from psycopg.rows import DictRow
from psycopg.types.json import Jsonb


def insert_authorization(
    cursor: psycopg.Cursor[DictRow],
    *,
    registry_name: str,
    decision_id: str,
    workflow_instance_id: uuid.UUID,
    authorized_by_actor_id: str,
    rationale: str,
    completed_task_id: uuid.UUID | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    cursor.execute(
        """
        INSERT INTO cdp_core.execution_authorization_record (
            registry_name, decision_id, workflow_instance_id,
            authorized_by_actor_id, rationale, completed_task_id, metadata
        )
        VALUES (
            %(registry_name)s, %(decision_id)s, %(workflow_instance_id)s,
            %(authorized_by_actor_id)s, %(rationale)s, %(completed_task_id)s, %(metadata)s
        )
        RETURNING *
        """,
        {
            "registry_name": registry_name,
            "decision_id": decision_id,
            "workflow_instance_id": workflow_instance_id,
            "authorized_by_actor_id": authorized_by_actor_id,
            "rationale": rationale,
            "completed_task_id": completed_task_id,
            "metadata": Jsonb(metadata or {}),
        },
    )
    row = cursor.fetchone()
    assert row is not None
    return row


def fetch_authorization_for_decision(
    cursor: psycopg.Cursor[DictRow], *, registry_name: str, decision_id: str
) -> dict[str, Any] | None:
    cursor.execute(
        """
        SELECT *
        FROM cdp_core.execution_authorization_record
        WHERE registry_name = %(registry_name)s
          AND decision_id = %(decision_id)s
        """,
        {"registry_name": registry_name, "decision_id": decision_id},
    )
    return cursor.fetchone()
