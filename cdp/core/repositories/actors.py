"""Repository for cdp_core.actor and its underlying identifier_registry row."""

from __future__ import annotations

from typing import Any

import psycopg
from psycopg.rows import DictRow

# cdp_core.decision_registry's validate_decision_registry_identifiers
# trigger (001-decision-registry-kernel.sql) hard-checks that
# subject_actor_id is typed under the legacy 'actor_type' registry
# (agent/human/system/institution/unknown) -- it predates this slice and is
# out of bounds to change here (that would retrofit an existing table
# beyond this slice's scope). So the identifier_registry row underlying a
# governed actor is tagged with a compatible legacy actor_type, while
# cdp_core.actor.actor_type (FK'd to the richer 'cdp_actor_type' registry:
# human|institution|synthetic|collective) remains the actor's real,
# RFC-CDP-030 type. This mapping is a compatibility bridge, not a claim
# that the two vocabularies are equivalent.
_LEGACY_ACTOR_TYPE_MAP = {
    "human": "human",
    "institution": "institution",
    "synthetic": "agent",
    "collective": "institution",
}


def insert_actor(
    cursor: psycopg.Cursor[DictRow],
    *,
    actor_id: str,
    actor_type: str,
    display_label: str,
    display_mode: str = "public",
    description: str | None = None,
) -> dict[str, Any]:
    """Register a new governed actor.

    Inserts both the underlying cdp_core.identifier_registry row
    (registry_name='actor') and the cdp_core.actor elaboration row in the
    caller's transaction. Raises psycopg.errors.UniqueViolation if
    actor_id is already registered.
    """
    cursor.execute(
        """
        INSERT INTO cdp_core.identifier_registry (
            registry_name, identifier_id, identifier_type_registry_name, identifier_type_id,
            display_label, description, status
        )
        VALUES ('actor', %(actor_id)s, 'actor_type', %(legacy_actor_type)s,
                %(display_label)s, %(description)s, 'active')
        """,
        {
            "actor_id": actor_id,
            # An actor_type outside the map (i.e. not a valid cdp_actor_type
            # value) falls back to the legacy 'unknown' enum value here; the
            # cdp_core.actor insert below is what actually rejects an
            # invalid actor_type, via its own FK to the cdp_actor_type
            # registry -- this lookup must not raise KeyError first and mask
            # that with a bare Python exception instead of a clean FK
            # violation the API layer already knows how to map to 422.
            "legacy_actor_type": _LEGACY_ACTOR_TYPE_MAP.get(actor_type, "unknown"),
            "display_label": display_label,
            "description": description,
        },
    )
    cursor.execute(
        """
        INSERT INTO cdp_core.actor (
            actor_id, actor_type, display_mode
        )
        VALUES (%(actor_id)s, %(actor_type)s, %(display_mode)s)
        RETURNING *
        """,
        {
            "actor_id": actor_id,
            "actor_type": actor_type,
            "display_mode": display_mode,
        },
    )
    row = cursor.fetchone()
    assert row is not None
    return {**row, "display_label": display_label, "description": description}


def fetch_actor(cursor: psycopg.Cursor[DictRow], *, actor_id: str) -> dict[str, Any] | None:
    cursor.execute(
        """
        SELECT a.*, i.display_label, i.description
        FROM cdp_core.actor a
        JOIN cdp_core.identifier_registry i
          ON i.registry_name = a.actor_registry_name
         AND i.identifier_id = a.actor_id
        WHERE a.actor_id = %(actor_id)s
        """,
        {"actor_id": actor_id},
    )
    return cursor.fetchone()
