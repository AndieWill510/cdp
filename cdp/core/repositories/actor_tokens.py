"""Repository for cdp_core.actor_bearer_token.

No function in this module ever issues a DELETE -- cdp_core.actor_bearer_token
also enforces this at the database level via
trg_actor_bearer_token_forbid_delete (014-caller-authentication.sql).
Revocation is always recorded as a status transition on the existing row,
never erasure.
"""

from __future__ import annotations

from typing import Any

import psycopg
from psycopg.rows import DictRow


def insert_token(
    cursor: psycopg.Cursor[DictRow], *, actor_id: str, token_hash: str
) -> dict[str, Any]:
    cursor.execute(
        """
        INSERT INTO cdp_core.actor_bearer_token (actor_id, token_hash)
        VALUES (%(actor_id)s, %(token_hash)s)
        RETURNING *
        """,
        {"actor_id": actor_id, "token_hash": token_hash},
    )
    row = cursor.fetchone()
    assert row is not None
    return row


def fetch_token_by_hash(
    cursor: psycopg.Cursor[DictRow], *, token_hash: str
) -> dict[str, Any] | None:
    cursor.execute(
        "SELECT * FROM cdp_core.actor_bearer_token WHERE token_hash = %(token_hash)s",
        {"token_hash": token_hash},
    )
    return cursor.fetchone()


def revoke_active_token_for_actor(
    cursor: psycopg.Cursor[DictRow], *, actor_id: str
) -> dict[str, Any] | None:
    """Revoke actor_id's currently active token, if any. Returns the
    revoked row, or None if the actor has no active token to revoke."""
    cursor.execute(
        """
        UPDATE cdp_core.actor_bearer_token
        SET status = 'revoked',
            revoked_at = now(),
            updated_at = now()
        WHERE actor_id = %(actor_id)s
          AND status = 'active'
        RETURNING *
        """,
        {"actor_id": actor_id},
    )
    return cursor.fetchone()
