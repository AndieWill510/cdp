"""Repository for cdp_core.authority_grant and cdp_core.authority_evaluation_result.

No function in this module ever issues a DELETE against either table --
both also enforce this at the database level via forbid-delete triggers
(011-authority-and-delegation.sql). Revocation is always a status
transition on the existing grant row, never erasure.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

import psycopg
from psycopg.rows import DictRow


def insert_grant(
    cursor: psycopg.Cursor[DictRow],
    *,
    actor_id: str,
    authority: str,
    scope_registry_name: str,
    scope_decision_class_id: str | None,
    issued_at: datetime,
    effective_at: datetime,
    expires_at: datetime,
    issuer_actor_id: str,
    basis: str,
) -> dict[str, Any]:
    cursor.execute(
        """
        INSERT INTO cdp_core.authority_grant (
            actor_id, authority, scope_registry_name, scope_decision_class_id,
            issued_at, effective_at, expires_at, issuer_actor_id, basis
        )
        VALUES (
            %(actor_id)s, %(authority)s, %(scope_registry_name)s, %(scope_decision_class_id)s,
            %(issued_at)s, %(effective_at)s, %(expires_at)s, %(issuer_actor_id)s, %(basis)s
        )
        RETURNING *
        """,
        {
            "actor_id": actor_id,
            "authority": authority,
            "scope_registry_name": scope_registry_name,
            "scope_decision_class_id": scope_decision_class_id,
            "issued_at": issued_at,
            "effective_at": effective_at,
            "expires_at": expires_at,
            "issuer_actor_id": issuer_actor_id,
            "basis": basis,
        },
    )
    row = cursor.fetchone()
    assert row is not None
    return row


def fetch_grant(
    cursor: psycopg.Cursor[DictRow], *, grant_id: uuid.UUID
) -> dict[str, Any] | None:
    cursor.execute(
        "SELECT * FROM cdp_core.authority_grant WHERE authority_grant_id = %(grant_id)s",
        {"grant_id": grant_id},
    )
    return cursor.fetchone()


def fetch_active_grants_for_actor(
    cursor: psycopg.Cursor[DictRow],
    *,
    actor_id: str,
    authority: str,
    scope_registry_name: str,
    scope_decision_class_id: str,
    at_time: datetime,
) -> list[dict[str, Any]]:
    """Return active, currently-effective, unexpired grants matching the
    given actor/authority/scope. A grant with scope_decision_class_id NULL
    matches any scope_decision_class_id -- the wildcard rule described in
    011-authority-and-delegation.sql's header. Exact-class matches are
    returned before wildcard matches so a caller taking the first row
    prefers the more specific grant."""
    cursor.execute(
        """
        SELECT *
        FROM cdp_core.authority_grant
        WHERE actor_id = %(actor_id)s
          AND authority = %(authority)s
          AND status = 'active'
          AND scope_registry_name = %(scope_registry_name)s
          AND (
            scope_decision_class_id IS NULL
            OR scope_decision_class_id = %(scope_decision_class_id)s
          )
          AND effective_at <= %(at_time)s
          AND expires_at > %(at_time)s
        ORDER BY scope_decision_class_id NULLS LAST, issued_at DESC
        """,
        {
            "actor_id": actor_id,
            "authority": authority,
            "scope_registry_name": scope_registry_name,
            "scope_decision_class_id": scope_decision_class_id,
            "at_time": at_time,
        },
    )
    return cursor.fetchall()


def revoke_grant(
    cursor: psycopg.Cursor[DictRow],
    *,
    grant_id: uuid.UUID,
    revoked_by_actor_id: str,
    reason: str,
) -> dict[str, Any] | None:
    """Revoke a grant. Returns None (rather than raising) if the grant does
    not exist or is not currently 'active', so the caller can distinguish
    "not found" from "already revoked"."""
    cursor.execute(
        """
        UPDATE cdp_core.authority_grant
        SET status = 'revoked',
            revoked_at = now(),
            revoked_by_actor_id = %(revoked_by_actor_id)s,
            revocation_reason = %(reason)s,
            updated_at = now()
        WHERE authority_grant_id = %(grant_id)s
          AND status = 'active'
        RETURNING *
        """,
        {
            "grant_id": grant_id,
            "revoked_by_actor_id": revoked_by_actor_id,
            "reason": reason,
        },
    )
    return cursor.fetchone()


def insert_evaluation_result(
    cursor: psycopg.Cursor[DictRow],
    *,
    actor_id: str,
    required_authority: str,
    governed_act_type: str,
    governed_act_registry_name: str,
    governed_act_decision_id: str,
    matched_authority_grant_id: uuid.UUID | None,
    result: str,
    failure_reason: str | None,
    governed_act_ref_id: uuid.UUID | None = None,
) -> dict[str, Any]:
    """governed_act_ref_id disambiguates which sub-record (challenge,
    adjudication, authorization, execution) this evaluation covers when a
    decision can have more than one -- see 012-universal-attestation.sql.
    NULL for decision_created."""
    cursor.execute(
        """
        INSERT INTO cdp_core.authority_evaluation_result (
            actor_id, required_authority, governed_act_type,
            governed_act_registry_name, governed_act_decision_id, governed_act_ref_id,
            matched_authority_grant_id, result, failure_reason
        )
        VALUES (
            %(actor_id)s, %(required_authority)s, %(governed_act_type)s,
            %(governed_act_registry_name)s, %(governed_act_decision_id)s, %(governed_act_ref_id)s,
            %(matched_authority_grant_id)s, %(result)s, %(failure_reason)s
        )
        RETURNING *
        """,
        {
            "actor_id": actor_id,
            "required_authority": required_authority,
            "governed_act_type": governed_act_type,
            "governed_act_registry_name": governed_act_registry_name,
            "governed_act_decision_id": governed_act_decision_id,
            "governed_act_ref_id": governed_act_ref_id,
            "matched_authority_grant_id": matched_authority_grant_id,
            "result": result,
            "failure_reason": failure_reason,
        },
    )
    row = cursor.fetchone()
    assert row is not None
    return row


def fetch_evaluation_results_for_decision(
    cursor: psycopg.Cursor[DictRow], *, registry_name: str, decision_id: str
) -> list[dict[str, Any]]:
    cursor.execute(
        """
        SELECT *
        FROM cdp_core.authority_evaluation_result
        WHERE governed_act_registry_name = %(registry_name)s
          AND governed_act_decision_id = %(decision_id)s
        ORDER BY evaluated_at
        """,
        {"registry_name": registry_name, "decision_id": decision_id},
    )
    return cursor.fetchall()
