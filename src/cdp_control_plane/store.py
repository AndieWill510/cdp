from __future__ import annotations

import json
import os
from hashlib import sha256
from uuid import UUID

import psycopg
from psycopg.rows import dict_row

from .models import DecisionEnvelope

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://cdp:cdp@localhost:5432/cdp")


def compute_record_hash(envelope: DecisionEnvelope) -> str:
    payload = envelope.model_dump(mode="json")
    payload.pop("record_hash", None)
    payload["created_at"] = envelope.created_at.isoformat()
    payload["updated_at"] = envelope.updated_at.isoformat()
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256(text.encode("utf-8")).hexdigest()


def get_connection() -> psycopg.Connection:
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def save_record(envelope: DecisionEnvelope) -> DecisionEnvelope:
    envelope.record_hash = compute_record_hash(envelope)
    envelope_json = envelope.model_dump_json()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO decision_envelopes (
                    id, status, actor_id, created_at, updated_at, record_hash, envelope
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb)
                ON CONFLICT (id) DO UPDATE SET
                    status = EXCLUDED.status,
                    actor_id = EXCLUDED.actor_id,
                    updated_at = EXCLUDED.updated_at,
                    record_hash = EXCLUDED.record_hash,
                    envelope = EXCLUDED.envelope
                """,
                (
                    envelope.id,
                    envelope.status.value,
                    envelope.actor_id,
                    envelope.created_at,
                    envelope.updated_at,
                    envelope.record_hash,
                    envelope_json,
                ),
            )
    return envelope


def get_record(record_id: UUID) -> DecisionEnvelope | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT envelope FROM decision_envelopes WHERE id = %s",
                (record_id,),
            )
            row = cur.fetchone()
    if row is None:
        return None
    return DecisionEnvelope.model_validate(row["envelope"])
