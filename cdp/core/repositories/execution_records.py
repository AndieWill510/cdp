"""Repository for cdp_core.execution_record."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

import psycopg
from psycopg.rows import DictRow
from psycopg.types.json import Jsonb


def insert_execution_record(
    cursor: psycopg.Cursor[DictRow],
    *,
    registry_name: str,
    decision_id: str,
    authorization_id: uuid.UUID,
    workflow_instance_id: uuid.UUID,
    executed_by_actor_id: str,
    execution_status: str,
    result_summary: str,
    attempted_at: datetime,
    completed_at: datetime,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    cursor.execute(
        """
        INSERT INTO cdp_core.execution_record (
            registry_name, decision_id, authorization_id, workflow_instance_id,
            executed_by_actor_id, execution_status, result_summary,
            attempted_at, completed_at, metadata
        )
        VALUES (
            %(registry_name)s, %(decision_id)s, %(authorization_id)s, %(workflow_instance_id)s,
            %(executed_by_actor_id)s, %(execution_status)s, %(result_summary)s,
            %(attempted_at)s, %(completed_at)s, %(metadata)s
        )
        RETURNING *
        """,
        {
            "registry_name": registry_name,
            "decision_id": decision_id,
            "authorization_id": authorization_id,
            "workflow_instance_id": workflow_instance_id,
            "executed_by_actor_id": executed_by_actor_id,
            "execution_status": execution_status,
            "result_summary": result_summary,
            "attempted_at": attempted_at,
            "completed_at": completed_at,
            "metadata": Jsonb(metadata or {}),
        },
    )
    row = cursor.fetchone()
    assert row is not None
    return row


def fetch_execution_records_for_authorization(
    cursor: psycopg.Cursor[DictRow], *, authorization_id: uuid.UUID
) -> list[dict[str, Any]]:
    cursor.execute(
        """
        SELECT *
        FROM cdp_core.execution_record
        WHERE authorization_id = %(authorization_id)s
        ORDER BY created_at
        """,
        {"authorization_id": authorization_id},
    )
    return cursor.fetchall()


def fetch_succeeded_execution_for_authorization(
    cursor: psycopg.Cursor[DictRow], *, authorization_id: uuid.UUID
) -> dict[str, Any] | None:
    cursor.execute(
        """
        SELECT *
        FROM cdp_core.execution_record
        WHERE authorization_id = %(authorization_id)s
          AND execution_status = 'succeeded'
        """,
        {"authorization_id": authorization_id},
    )
    return cursor.fetchone()
