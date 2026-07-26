"""Repository for cdp_core.decision_registry."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import psycopg
from psycopg.rows import DictRow


def insert_decision(
    cursor: psycopg.Cursor[DictRow],
    *,
    registry_name: str,
    decision_id: str,
    decision_class_id: str,
    antecedent_text: str,
    subject_actor_type: str,
    subject_actor_id: str,
    predicate_verb: str,
    object_type: str,
    object_id: str,
    permission_source_type: str,
    permission_source_id: str,
    human_required: bool,
    created: datetime,
    human_approver_id: str = "none",
    parent_decision_id: str | None = None,
    parent_relation_type: str = "none",
    source_system: str = "api",
    source_ref: str | None = None,
) -> dict[str, Any]:
    """Insert one decision_registry row. row_hash is trigger-computed."""
    cursor.execute(
        """
        INSERT INTO cdp_core.decision_registry (
            registry_name, decision_id, decision_class_id,
            parent_decision_id, parent_relation_type,
            antecedent_text,
            subject_actor_type, subject_actor_id,
            predicate_verb, object_type, object_id,
            permission_source_type, permission_source_id,
            human_required, human_approver_id,
            created, source_system, source_ref
        )
        VALUES (
            %(registry_name)s, %(decision_id)s, %(decision_class_id)s,
            %(parent_decision_id)s, %(parent_relation_type)s,
            %(antecedent_text)s,
            %(subject_actor_type)s, %(subject_actor_id)s,
            %(predicate_verb)s, %(object_type)s, %(object_id)s,
            %(permission_source_type)s, %(permission_source_id)s,
            %(human_required)s, %(human_approver_id)s,
            %(created)s, %(source_system)s, %(source_ref)s
        )
        RETURNING *
        """,
        {
            "registry_name": registry_name,
            "decision_id": decision_id,
            "decision_class_id": decision_class_id,
            "parent_decision_id": parent_decision_id,
            "parent_relation_type": parent_relation_type,
            "antecedent_text": antecedent_text,
            "subject_actor_type": subject_actor_type,
            "subject_actor_id": subject_actor_id,
            "predicate_verb": predicate_verb,
            "object_type": object_type,
            "object_id": object_id,
            "permission_source_type": permission_source_type,
            "permission_source_id": permission_source_id,
            "human_required": human_required,
            "human_approver_id": human_approver_id,
            "created": created,
            "source_system": source_system,
            "source_ref": source_ref,
        },
    )
    row = cursor.fetchone()
    assert row is not None
    return row


def fetch_decision(
    cursor: psycopg.Cursor[DictRow], *, registry_name: str, decision_id: str
) -> dict[str, Any] | None:
    cursor.execute(
        """
        SELECT *
        FROM cdp_core.decision_registry
        WHERE registry_name = %(registry_name)s
          AND decision_id = %(decision_id)s
        """,
        {"registry_name": registry_name, "decision_id": decision_id},
    )
    return cursor.fetchone()
