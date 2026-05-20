from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path
from uuid import UUID

from .models import DecisionEnvelope

RECORDS_FILE = Path("data/records.jsonl")


def compute_record_hash(envelope: DecisionEnvelope) -> str:
    payload = envelope.model_dump(mode="json")
    payload.pop("record_hash", None)
    payload["created_at"] = envelope.created_at.isoformat()
    payload["updated_at"] = envelope.updated_at.isoformat()
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256(text.encode("utf-8")).hexdigest()


def read_records() -> list[DecisionEnvelope]:
    if not RECORDS_FILE.exists():
        return []
    return [DecisionEnvelope.model_validate_json(line) for line in RECORDS_FILE.read_text().splitlines() if line]


def write_records(records: list[DecisionEnvelope]) -> None:
    RECORDS_FILE.parent.mkdir(parents=True, exist_ok=True)
    RECORDS_FILE.write_text("\n".join(r.model_dump_json() for r in records) + "\n")


def save_record(envelope: DecisionEnvelope) -> DecisionEnvelope:
    records = [r for r in read_records() if r.id != envelope.id]
    envelope.record_hash = compute_record_hash(envelope)
    records.append(envelope)
    write_records(records)
    return envelope


def get_record(record_id: UUID) -> DecisionEnvelope | None:
    for record in read_records():
        if record.id == record_id:
            return record
    return None
