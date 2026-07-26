"""Repository for cdp_core.challenge_adjudication_record."""

from __future__ import annotations

import uuid
from typing import Any

import psycopg
from psycopg.rows import DictRow


def insert_adjudication(
    cursor: psycopg.Cursor[DictRow],
    *,
    registry_name: str,
    decision_id: str,
    challenge_id: uuid.UUID,
    adjudicated_by_actor_id: str,
    outcome: str,
    rationale: str,
    resulting_challenge_status: str,
    adjudicated_task_id: uuid.UUID | None = None,
) -> dict[str, Any]:
    cursor.execute(
        """
        INSERT INTO cdp_core.challenge_adjudication_record (
            registry_name, decision_id, challenge_id,
            adjudicated_by_actor_id, outcome, rationale,
            resulting_challenge_status, adjudicated_task_id
        )
        VALUES (
            %(registry_name)s, %(decision_id)s, %(challenge_id)s,
            %(adjudicated_by_actor_id)s, %(outcome)s, %(rationale)s,
            %(resulting_challenge_status)s, %(adjudicated_task_id)s
        )
        RETURNING *
        """,
        {
            "registry_name": registry_name,
            "decision_id": decision_id,
            "challenge_id": challenge_id,
            "adjudicated_by_actor_id": adjudicated_by_actor_id,
            "outcome": outcome,
            "rationale": rationale,
            "resulting_challenge_status": resulting_challenge_status,
            "adjudicated_task_id": adjudicated_task_id,
        },
    )
    row = cursor.fetchone()
    assert row is not None
    return row


def fetch_adjudications_for_challenge(
    cursor: psycopg.Cursor[DictRow], *, challenge_id: uuid.UUID
) -> list[dict[str, Any]]:
    cursor.execute(
        """
        SELECT *
        FROM cdp_core.challenge_adjudication_record
        WHERE challenge_id = %(challenge_id)s
        ORDER BY created_at
        """,
        {"challenge_id": challenge_id},
    )
    return cursor.fetchall()
