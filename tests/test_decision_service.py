"""Integration tests for the create_decision_with_workflow vertical slice.

These tests exercise the real repository/service stack against Postgres.
They require:

- CDP_TEST_DATABASE_URL pointing at a disposable/local database
- db/ddl/001, 003, and 004 already applied to that database

Each test uses a uniquely-namespaced decision_id and cleans up everything it
inserts in a `finally` block, so these tests do not contaminate persistent
local data. They are skipped entirely when CDP_TEST_DATABASE_URL is not set,
or when 004's configuration is not yet applied.

Import note: this module uses cdp.core (dataclasses, modern union type
hints) which targets the project's Python 3.12 runtime. Run it with the
interpreter used by the Docker stack (e.g. `docker compose exec cdp-api
pytest tests/test_decision_service.py`), not an older local virtualenv.
"""

from __future__ import annotations

import os
import unittest
import uuid
from unittest import mock

import psycopg
from psycopg.rows import dict_row

REGISTRY_NAME = "sample_attorney_demo"
DECISION_CLASS_ID = "claim_approval"
UNCONFIGURED_CLASS_ID_PREFIX = "vslice_unconfigured"


def _database_url() -> str:
    return os.environ.get("CDP_TEST_DATABASE_URL", "postgresql://cdp:cdp@localhost:5432/cdp")


def _configured() -> bool:
    """True once 004 has wired nemawashi_default_v1 to claim_approval."""
    with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT 1
            FROM cdp_core.workflow_definition
            WHERE workflow_code = 'nemawashi_default_v1'
              AND workflow_version = 'v1'
              AND applies_to_registry_name = %s
              AND applies_to_decision_class_id = %s
              AND status = 'active'
            """,
            (REGISTRY_NAME, DECISION_CLASS_ID),
        )
        return cursor.fetchone() is not None


def _make_decision_input(decision_id: str, *, decision_class_id: str = DECISION_CLASS_ID):
    from cdp.core.services import DecisionInput

    return DecisionInput(
        registry_name=REGISTRY_NAME,
        decision_id=decision_id,
        decision_class_id=decision_class_id,
        antecedent_text="Vertical slice integration test decision.",
        subject_actor_type="agent",
        subject_actor_id="claims_review_agent",
        predicate_verb="recommend_approval",
        object_type="claim",
        object_id="claim_9981",
        permission_source_type="policy_rule",
        permission_source_id="policy_claims_approval_v2",
        human_required=True,
    )


def _cleanup_decision(decision_id: str) -> None:
    with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM cdp_core.workflow_task
            WHERE registry_name = %s AND decision_id = %s
            """,
            (REGISTRY_NAME, decision_id),
        )
        cursor.execute(
            """
            DELETE FROM cdp_core.workflow_instance
            WHERE registry_name = %s AND decision_id = %s
            """,
            (REGISTRY_NAME, decision_id),
        )
        cursor.execute(
            """
            DELETE FROM cdp_core.decision_registry
            WHERE registry_name = %s AND decision_id = %s
            """,
            (REGISTRY_NAME, decision_id),
        )
        cursor.execute(
            """
            DELETE FROM cdp_audit.event_log
            WHERE payload ->> 'registry_name' = %s
              AND payload ->> 'decision_id' = %s
            """,
            (REGISTRY_NAME, decision_id),
        )
        conn.commit()


@unittest.skipUnless(os.environ.get("CDP_TEST_DATABASE_URL"), "set CDP_TEST_DATABASE_URL to run")
class CreateDecisionWithWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ.setdefault("DATABASE_URL", _database_url())
        if not _configured():
            raise unittest.SkipTest(
                "004-decision-class-workflow-seed.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )

    def test_happy_path_creates_decision_workflow_task_and_three_audit_events(self) -> None:
        from cdp.core.services import create_decision_with_workflow

        decision_id = f"vslice-happy-{uuid.uuid4().hex[:12]}"
        try:
            result = create_decision_with_workflow(_make_decision_input(decision_id))

            self.assertEqual(result["decision"]["decision_id"], decision_id)
            self.assertEqual(result["workflow_instance"]["workflow_status"], "active")
            self.assertEqual(result["task"]["task_status"], "open")
            self.assertTrue(result["task"]["blocking"])

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.decision_registry "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 1)

                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.workflow_instance "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 1)

                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.workflow_task "
                    "WHERE registry_name = %s AND decision_id = %s AND task_status = 'open'",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 1)

                cursor.execute(
                    "SELECT event_type FROM cdp_audit.event_log "
                    "WHERE payload ->> 'registry_name' = %s AND payload ->> 'decision_id' = %s "
                    "ORDER BY created_at",
                    (REGISTRY_NAME, decision_id),
                )
                event_types = [row["event_type"] for row in cursor.fetchall()]
                self.assertEqual(
                    event_types, ["decision.created", "workflow.started", "task.created"]
                )
        finally:
            _cleanup_decision(decision_id)

    def test_failure_after_decision_insertion_rolls_back_everything(self) -> None:
        from cdp.core.services import create_decision_with_workflow

        decision_id = f"vslice-atomic-{uuid.uuid4().hex[:12]}"
        try:
            with mock.patch(
                "cdp.core.services.workflows_repo.insert_task",
                side_effect=RuntimeError("forced task-creation failure"),
            ):
                with self.assertRaises(RuntimeError):
                    create_decision_with_workflow(_make_decision_input(decision_id))

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.decision_registry "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0, "decision should not survive rollback")

                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.workflow_instance "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0, "workflow instance should not survive rollback")

                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.workflow_task "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0, "task should not survive rollback")

                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_audit.event_log "
                    "WHERE payload ->> 'registry_name' = %s AND payload ->> 'decision_id' = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0, "no audit event should survive rollback")
        finally:
            _cleanup_decision(decision_id)

    def test_missing_workflow_configuration_raises_clean_error_with_no_partial_state(self) -> None:
        from cdp.core.services import DecisionClassNotConfigured, create_decision_with_workflow

        unconfigured_class_id = f"{UNCONFIGURED_CLASS_ID_PREFIX}_{uuid.uuid4().hex[:8]}"
        decision_id = f"vslice-unconfigured-{uuid.uuid4().hex[:12]}"

        with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO cdp_core.decision_class_registry
                    (registry_name, class_id, parent_class_id, class_label, class_level)
                VALUES (%s, %s, 'claim', 'Unconfigured Test Class', 1)
                """,
                (REGISTRY_NAME, unconfigured_class_id),
            )
            conn.commit()

        try:
            with self.assertRaises(DecisionClassNotConfigured):
                create_decision_with_workflow(
                    _make_decision_input(decision_id, decision_class_id=unconfigured_class_id)
                )

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.decision_registry "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0)
        finally:
            _cleanup_decision(decision_id)
            with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM cdp_core.decision_class_registry WHERE registry_name = %s AND class_id = %s",
                    (REGISTRY_NAME, unconfigured_class_id),
                )
                conn.commit()


if __name__ == "__main__":
    unittest.main()
