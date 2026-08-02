"""Repository for cdp_core.identity_claim.

No function in this module ever issues a DELETE -- cdp_core.identity_claim
also enforces this at the database level via
trg_identity_claim_forbid_delete (010-identity-and-attestation.sql).
Denial, contest, and supersession are always recorded as recognition_status
transitions on the existing row, or via a new row linked through
supersedes_claim_id / superseded_by_claim_id.
"""

from __future__ import annotations

import uuid
from typing import Any

import psycopg
from psycopg.rows import DictRow
from psycopg.types.json import Jsonb


def insert_claim(
    cursor: psycopg.Cursor[DictRow],
    *,
    actor_id: str,
    claimant_actor_id: str,
    claimed_identity_descriptor: str,
    purpose_scope: str,
    evidence_refs: list[Any] | None = None,
    supersedes_claim_id: uuid.UUID | None = None,
    scope_registry_name: str | None = None,
    scope_decision_class_id: str | None = None,
) -> dict[str, Any]:
    cursor.execute(
        """
        INSERT INTO cdp_core.identity_claim (
            actor_id, claimant_actor_id, claimed_identity_descriptor,
            purpose_scope, evidence_refs, supersedes_claim_id,
            scope_registry_name, scope_decision_class_id
        )
        VALUES (
            %(actor_id)s, %(claimant_actor_id)s, %(claimed_identity_descriptor)s,
            %(purpose_scope)s, %(evidence_refs)s, %(supersedes_claim_id)s,
            %(scope_registry_name)s, %(scope_decision_class_id)s
        )
        RETURNING *
        """,
        {
            "actor_id": actor_id,
            "claimant_actor_id": claimant_actor_id,
            "claimed_identity_descriptor": claimed_identity_descriptor,
            "purpose_scope": purpose_scope,
            "evidence_refs": Jsonb(evidence_refs or []),
            "supersedes_claim_id": supersedes_claim_id,
            "scope_registry_name": scope_registry_name,
            "scope_decision_class_id": scope_decision_class_id,
        },
    )
    row = cursor.fetchone()
    assert row is not None

    if supersedes_claim_id is not None:
        cursor.execute(
            """
            UPDATE cdp_core.identity_claim
            SET recognition_status = 'superseded',
                superseded_by_claim_id = %(new_claim_id)s,
                updated_at = now()
            WHERE claim_id = %(supersedes_claim_id)s
            """,
            {"new_claim_id": row["claim_id"], "supersedes_claim_id": supersedes_claim_id},
        )

    return row


def fetch_claim(cursor: psycopg.Cursor[DictRow], *, claim_id: uuid.UUID) -> dict[str, Any] | None:
    cursor.execute(
        "SELECT * FROM cdp_core.identity_claim WHERE claim_id = %(claim_id)s",
        {"claim_id": claim_id},
    )
    return cursor.fetchone()


def _decide_claim(
    cursor: psycopg.Cursor[DictRow],
    *,
    claim_id: uuid.UUID,
    recognition_status: str,
    decided_by_actor_id: str,
    rationale: str,
) -> dict[str, Any] | None:
    """Shared update for recognize/deny/contest -- only fires from 'pending'
    or 'recognized' (contest may run against an already-recognized claim);
    returns None if the claim is not in a decidable state, so the caller
    can distinguish "not found" from "already decided"."""
    cursor.execute(
        """
        UPDATE cdp_core.identity_claim
        SET recognition_status = %(recognition_status)s,
            recognized_by_actor_id = %(decided_by_actor_id)s,
            recognition_rationale = %(rationale)s,
            decided_at = now(),
            updated_at = now()
        WHERE claim_id = %(claim_id)s
          AND recognition_status IN ('pending', 'recognized')
        RETURNING *
        """,
        {
            "claim_id": claim_id,
            "recognition_status": recognition_status,
            "decided_by_actor_id": decided_by_actor_id,
            "rationale": rationale,
        },
    )
    return cursor.fetchone()


def recognize_claim(
    cursor: psycopg.Cursor[DictRow],
    *,
    claim_id: uuid.UUID,
    decided_by_actor_id: str,
    rationale: str,
) -> dict[str, Any] | None:
    return _decide_claim(
        cursor,
        claim_id=claim_id,
        recognition_status="recognized",
        decided_by_actor_id=decided_by_actor_id,
        rationale=rationale,
    )


def deny_claim(
    cursor: psycopg.Cursor[DictRow],
    *,
    claim_id: uuid.UUID,
    decided_by_actor_id: str,
    rationale: str,
) -> dict[str, Any] | None:
    return _decide_claim(
        cursor,
        claim_id=claim_id,
        recognition_status="denied",
        decided_by_actor_id=decided_by_actor_id,
        rationale=rationale,
    )


def contest_claim(
    cursor: psycopg.Cursor[DictRow],
    *,
    claim_id: uuid.UUID,
    decided_by_actor_id: str,
    rationale: str,
) -> dict[str, Any] | None:
    return _decide_claim(
        cursor,
        claim_id=claim_id,
        recognition_status="contested",
        decided_by_actor_id=decided_by_actor_id,
        rationale=rationale,
    )
