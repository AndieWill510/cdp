"""Repository for cdp_core.attestation_record."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

import psycopg
from psycopg.rows import DictRow


def insert_attestation(
    cursor: psycopg.Cursor[DictRow],
    *,
    actor_id: str,
    identity_claim_id: uuid.UUID,
    governed_act_type: str,
    governed_act_registry_name: str,
    governed_act_decision_id: str,
    attestation_method: str,
    credential_reference: str,
    issued_at: datetime,
    verifier_actor_id: str,
) -> dict[str, Any]:
    """Insert a 'verified' attestation record.

    This slice's service layer only ever calls this after synchronously
    confirming the actor and identity claim -- verification_result is
    always 'verified' here. A 'failed' result is schema-supported (see
    010-identity-and-attestation.sql) but not written by this function; a
    failed check raises an exception before any row is inserted instead.
    """
    cursor.execute(
        """
        INSERT INTO cdp_core.attestation_record (
            actor_id, identity_claim_id, governed_act_type,
            governed_act_registry_name, governed_act_decision_id,
            attestation_method, credential_reference, issued_at,
            verification_result, verifier_actor_id
        )
        VALUES (
            %(actor_id)s, %(identity_claim_id)s, %(governed_act_type)s,
            %(governed_act_registry_name)s, %(governed_act_decision_id)s,
            %(attestation_method)s, %(credential_reference)s, %(issued_at)s,
            'verified', %(verifier_actor_id)s
        )
        RETURNING *
        """,
        {
            "actor_id": actor_id,
            "identity_claim_id": identity_claim_id,
            "governed_act_type": governed_act_type,
            "governed_act_registry_name": governed_act_registry_name,
            "governed_act_decision_id": governed_act_decision_id,
            "attestation_method": attestation_method,
            "credential_reference": credential_reference,
            "issued_at": issued_at,
            "verifier_actor_id": verifier_actor_id,
        },
    )
    row = cursor.fetchone()
    assert row is not None
    return row


def fetch_attestation(
    cursor: psycopg.Cursor[DictRow], *, attestation_id: uuid.UUID
) -> dict[str, Any] | None:
    cursor.execute(
        "SELECT * FROM cdp_core.attestation_record WHERE attestation_id = %(attestation_id)s",
        {"attestation_id": attestation_id},
    )
    return cursor.fetchone()


def fetch_attestations_for_decision(
    cursor: psycopg.Cursor[DictRow], *, registry_name: str, decision_id: str
) -> list[dict[str, Any]]:
    cursor.execute(
        """
        SELECT *
        FROM cdp_core.attestation_record
        WHERE governed_act_registry_name = %(registry_name)s
          AND governed_act_decision_id = %(decision_id)s
        ORDER BY created_at
        """,
        {"registry_name": registry_name, "decision_id": decision_id},
    )
    return cursor.fetchall()
