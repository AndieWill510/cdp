"""Repository for cdp_audit.event_log."""

from __future__ import annotations

from typing import Any

import psycopg
from psycopg.rows import DictRow
from psycopg.types.json import Jsonb


def append_event(
    cursor: psycopg.Cursor[DictRow],
    *,
    event_type: str,
    aggregate_type: str,
    aggregate_id: str,
    payload: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    cursor.execute(
        """
        INSERT INTO cdp_audit.event_log (
            event_type, aggregate_type, aggregate_id, payload, metadata
        )
        VALUES (
            %(event_type)s, %(aggregate_type)s, %(aggregate_id)s,
            %(payload)s, %(metadata)s
        )
        RETURNING *
        """,
        {
            "event_type": event_type,
            "aggregate_type": aggregate_type,
            "aggregate_id": aggregate_id,
            "payload": Jsonb(payload or {}),
            "metadata": Jsonb(metadata or {}),
        },
    )
    row = cursor.fetchone()
    assert row is not None
    return row
