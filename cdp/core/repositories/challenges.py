"""Repository for cdp_core.challenge_record."""

from __future__ import annotations

import uuid
from typing import Any

import psycopg
from psycopg.rows import DictRow
from psycopg.types.json import Jsonb


def insert_challenge(
    cursor: psycopg.Cursor[DictRow],
    *,
    registry_name: str,
    decision_id: str,
    workflow_instance_id: uuid.UUID,
    raised_by_actor_id: str,
    challenge_text: str,
    challenge_type: str = "other",
    created_task_id: uuid.UUID | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    cursor.execute(
        """
        INSERT INTO cdp_core.challenge_record (
            registry_name, decision_id, workflow_instance_id,
            raised_by_actor_id, challenge_type, challenge_text,
            created_task_id, metadata
        )
        VALUES (
            %(registry_name)s, %(decision_id)s, %(workflow_instance_id)s,
            %(raised_by_actor_id)s, %(challenge_type)s, %(challenge_text)s,
            %(created_task_id)s, %(metadata)s
        )
        RETURNING *
        """,
        {
            "registry_name": registry_name,
            "decision_id": decision_id,
            "workflow_instance_id": workflow_instance_id,
            "raised_by_actor_id": raised_by_actor_id,
            "challenge_type": challenge_type,
            "challenge_text": challenge_text,
            "created_task_id": created_task_id,
            "metadata": Jsonb(metadata or {}),
        },
    )
    row = cursor.fetchone()
    assert row is not None
    return row


def fetch_challenges_for_decision(
    cursor: psycopg.Cursor[DictRow], *, registry_name: str, decision_id: str
) -> list[dict[str, Any]]:
    cursor.execute(
        """
        SELECT *
        FROM cdp_core.challenge_record
        WHERE registry_name = %(registry_name)s
          AND decision_id = %(decision_id)s
        ORDER BY created_at
        """,
        {"registry_name": registry_name, "decision_id": decision_id},
    )
    return cursor.fetchall()


def fetch_challenge(
    cursor: psycopg.Cursor[DictRow], *, challenge_id: uuid.UUID
) -> dict[str, Any] | None:
    cursor.execute(
        "SELECT * FROM cdp_core.challenge_record WHERE challenge_id = %(challenge_id)s",
        {"challenge_id": challenge_id},
    )
    return cursor.fetchone()


def update_challenge_status(
    cursor: psycopg.Cursor[DictRow],
    *,
    challenge_id: uuid.UUID,
    challenge_status: str,
    set_resolved_at: bool = False,
) -> dict[str, Any]:
    cursor.execute(
        """
        UPDATE cdp_core.challenge_record
        SET challenge_status = %(challenge_status)s,
            resolved_at = CASE WHEN %(set_resolved_at)s THEN now() ELSE resolved_at END,
            updated_at = now()
        WHERE challenge_id = %(challenge_id)s
        RETURNING *
        """,
        {
            "challenge_id": challenge_id,
            "challenge_status": challenge_status,
            "set_resolved_at": set_resolved_at,
        },
    )
    row = cursor.fetchone()
    assert row is not None
    return row


def count_open_challenges_for_decision(
    cursor: psycopg.Cursor[DictRow],
    *,
    registry_name: str,
    decision_id: str,
    exclude_challenge_id: uuid.UUID | None = None,
) -> int:
    cursor.execute(
        """
        SELECT count(*) AS n
        FROM cdp_core.challenge_record
        WHERE registry_name = %(registry_name)s
          AND decision_id = %(decision_id)s
          AND challenge_status IN ('raised', 'under_review')
          AND (
            %(exclude_challenge_id)s::uuid IS NULL
            OR challenge_id != %(exclude_challenge_id)s::uuid
          )
        """,
        {
            "registry_name": registry_name,
            "decision_id": decision_id,
            "exclude_challenge_id": exclude_challenge_id,
        },
    )
    row = cursor.fetchone()
    assert row is not None
    return row["n"]
