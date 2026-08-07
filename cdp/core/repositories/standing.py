"""Repository for cdp_core.standing_claim and
cdp_core.standing_recognition_determination.

No function in this module ever issues a DELETE or an UPDATE against
either table -- both also enforce this at the database level via
forbid-delete AND forbid-update triggers (015-standing-and-recusal.sql).
A Standing Claim and its Recognition Determination are each immutable
once inserted; a correction is a new row, never an edit to an existing
one.
"""

from __future__ import annotations

import uuid
from typing import Any

import psycopg
from psycopg.rows import DictRow


def insert_claim(
    cursor: psycopg.Cursor[DictRow],
    *,
    decision_registry_name: str,
    decision_id: str,
    stage: str,
    actor_id: str,
    standing_type: str,
    claimed_impact: str,
    standing_basis_role: str | None = None,
    standing_basis_accountability: str | None = None,
    standing_basis_contextual_relationship: str | None = None,
) -> dict[str, Any]:
    cursor.execute(
        """
        INSERT INTO cdp_core.standing_claim (
            decision_registry_name, decision_id, stage, actor_id, standing_type,
            claimed_impact, standing_basis_role, standing_basis_accountability,
            standing_basis_contextual_relationship
        )
        VALUES (
            %(decision_registry_name)s, %(decision_id)s, %(stage)s, %(actor_id)s, %(standing_type)s,
            %(claimed_impact)s, %(standing_basis_role)s, %(standing_basis_accountability)s,
            %(standing_basis_contextual_relationship)s
        )
        RETURNING *
        """,
        {
            "decision_registry_name": decision_registry_name,
            "decision_id": decision_id,
            "stage": stage,
            "actor_id": actor_id,
            "standing_type": standing_type,
            "claimed_impact": claimed_impact,
            "standing_basis_role": standing_basis_role,
            "standing_basis_accountability": standing_basis_accountability,
            "standing_basis_contextual_relationship": standing_basis_contextual_relationship,
        },
    )
    row = cursor.fetchone()
    assert row is not None
    return row


def fetch_claim(cursor: psycopg.Cursor[DictRow], *, claim_id: uuid.UUID) -> dict[str, Any] | None:
    cursor.execute(
        "SELECT * FROM cdp_core.standing_claim WHERE claim_id = %(claim_id)s",
        {"claim_id": claim_id},
    )
    return cursor.fetchone()


def insert_determination(
    cursor: psycopg.Cursor[DictRow],
    *,
    claim_id: uuid.UUID,
    outcome: str,
    outcome_basis: str,
    determined_by_actor_id: str,
) -> dict[str, Any]:
    cursor.execute(
        """
        INSERT INTO cdp_core.standing_recognition_determination (
            claim_id, outcome, outcome_basis, determined_by_actor_id
        )
        VALUES (
            %(claim_id)s, %(outcome)s, %(outcome_basis)s, %(determined_by_actor_id)s
        )
        RETURNING *
        """,
        {
            "claim_id": claim_id,
            "outcome": outcome,
            "outcome_basis": outcome_basis,
            "determined_by_actor_id": determined_by_actor_id,
        },
    )
    row = cursor.fetchone()
    assert row is not None
    return row


def fetch_determination_for_claim(
    cursor: psycopg.Cursor[DictRow], *, claim_id: uuid.UUID
) -> dict[str, Any] | None:
    cursor.execute(
        "SELECT * FROM cdp_core.standing_recognition_determination WHERE claim_id = %(claim_id)s",
        {"claim_id": claim_id},
    )
    return cursor.fetchone()
