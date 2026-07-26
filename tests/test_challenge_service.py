"""Integration tests for the raise_challenge_for_decision vertical slice.

These tests exercise the real repository/service stack against Postgres.
They require:

- CDP_TEST_DATABASE_URL pointing at a disposable/local database
- db/ddl/001, 003, 004, and 005 already applied to that database

Each test uses a uniquely-namespaced decision_id and cleans up everything it
inserts in a `finally` block, so these tests do not contaminate persistent
local data. They are skipped entirely when CDP_TEST_DATABASE_URL is not set,
or when 005's challenge_record table is not yet applied.

Import note: this module uses cdp.core (dataclasses, modern union type
hints) which targets the project's Python 3.12 runtime. Run it with the
interpreter used by the Docker stack (e.g. `docker compose exec cdp-api
pytest tests/test_challenge_service.py`), not an older local virtualenv.
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


def _database_url() -> str:
    return os.environ.get("CDP_TEST_DATABASE_URL", "postgresql://cdp:cdp@localhost:5432/cdp")


def _challenge_record_table_exists() -> bool:
    with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
        cursor.execute("SELECT to_regclass('cdp_core.challenge_record')")
        return cursor.fetchone()[0] is not None


def _decision_workflow_configured() -> bool:
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


def _create_decision(decision_id: str):
    from cdp.core.services import DecisionInput, create_decision_with_workflow

    return create_decision_with_workflow(
        DecisionInput(
            registry_name=REGISTRY_NAME,
            decision_id=decision_id,
            decision_class_id=DECISION_CLASS_ID,
            antecedent_text="Challenge-slice integration test decision.",
            subject_actor_type="agent",
            subject_actor_id="claims_review_agent",
            predicate_verb="recommend_approval",
            object_type="claim",
            object_id="claim_9981",
            permission_source_type="policy_rule",
            permission_source_id="policy_claims_approval_v2",
            human_required=True,
        )
    )


def _make_challenge_input(decision_id: str):
    from cdp.core.services import ChallengeInput

    return ChallengeInput(
        registry_name=REGISTRY_NAME,
        decision_id=decision_id,
        raised_by_actor_id="user_442",
        challenge_text="This recommendation overlooks a documented policy exception.",
        challenge_type="policy",
    )


def _cleanup_decision(decision_id: str) -> None:
    with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
        cursor.execute(
            "DELETE FROM cdp_core.challenge_record WHERE registry_name = %s AND decision_id = %s",
            (REGISTRY_NAME, decision_id),
        )
        cursor.execute(
            "DELETE FROM cdp_core.workflow_task WHERE registry_name = %s AND decision_id = %s",
            (REGISTRY_NAME, decision_id),
        )
        cursor.execute(
            "DELETE FROM cdp_core.workflow_instance WHERE registry_name = %s AND decision_id = %s",
            (REGISTRY_NAME, decision_id),
        )
        cursor.execute(
            "DELETE FROM cdp_core.decision_registry WHERE registry_name = %s AND decision_id = %s",
            (REGISTRY_NAME, decision_id),
        )
        cursor.execute(
            "DELETE FROM cdp_audit.event_log "
            "WHERE payload ->> 'registry_name' = %s AND payload ->> 'decision_id' = %s",
            (REGISTRY_NAME, decision_id),
        )
        conn.commit()


@unittest.skipUnless(os.environ.get("CDP_TEST_DATABASE_URL"), "set CDP_TEST_DATABASE_URL to run")
class RaiseChallengeForDecisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ.setdefault("DATABASE_URL", _database_url())
        if not _decision_workflow_configured():
            raise unittest.SkipTest(
                "004-decision-class-workflow-seed.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )
        if not _challenge_record_table_exists():
            raise unittest.SkipTest(
                "005-challenge-transition.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )

    def test_happy_path_raises_challenge_blocks_workflow_and_opens_task(self) -> None:
        from cdp.core.services import raise_challenge_for_decision

        decision_id = f"vslice2-happy-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)

            result = raise_challenge_for_decision(_make_challenge_input(decision_id))

            self.assertEqual(result["challenge"]["challenge_status"], "raised")
            self.assertEqual(result["challenge"]["challenge_type"], "policy")
            self.assertEqual(result["challenge"]["raised_by_actor_id"], "user_442")
            self.assertTrue(result["workflow_instance"]["blocked"])
            self.assertEqual(result["workflow_instance"]["workflow_status"], "blocked")
            self.assertEqual(result["task"]["task_type"], "adjudicate_challenge")
            self.assertEqual(result["task"]["assigned_role"], "adjudicator")
            self.assertEqual(result["challenge"]["created_task_id"], result["task"]["task_id"])

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.challenge_record "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 1)

                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.workflow_task "
                    "WHERE registry_name = %s AND decision_id = %s AND task_type = 'adjudicate_challenge'",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 1)

                cursor.execute(
                    "SELECT blocked, workflow_status FROM cdp_core.workflow_instance "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                row = cursor.fetchone()
                self.assertTrue(row["blocked"])
                self.assertEqual(row["workflow_status"], "blocked")

                cursor.execute(
                    "SELECT event_type FROM cdp_audit.event_log "
                    "WHERE payload ->> 'registry_name' = %s AND payload ->> 'decision_id' = %s "
                    "ORDER BY created_at",
                    (REGISTRY_NAME, decision_id),
                )
                event_types = [row["event_type"] for row in cursor.fetchall()]
                self.assertEqual(
                    event_types,
                    [
                        "decision.created",
                        "workflow.started",
                        "task.created",
                        "challenge.raised",
                        "workflow.transitioned",
                        "task.created",
                    ],
                )
        finally:
            _cleanup_decision(decision_id)

    def test_missing_decision_returns_clean_error_with_no_partial_state(self) -> None:
        from cdp.core.services import DecisionNotFound, raise_challenge_for_decision

        decision_id = f"vslice2-missing-{uuid.uuid4().hex[:12]}"
        try:
            with self.assertRaises(DecisionNotFound):
                raise_challenge_for_decision(_make_challenge_input(decision_id))

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.challenge_record "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0)
        finally:
            _cleanup_decision(decision_id)

    def test_terminal_workflow_status_rejects_challenge_with_no_partial_state(self) -> None:
        from cdp.core.services import ChallengeNotPermitted, raise_challenge_for_decision

        decision_id = f"vslice2-terminal-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)

            with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE cdp_core.workflow_instance SET workflow_status = 'closed' "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                conn.commit()

            with self.assertRaises(ChallengeNotPermitted):
                raise_challenge_for_decision(_make_challenge_input(decision_id))

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.challenge_record "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0)

                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.workflow_task "
                    "WHERE registry_name = %s AND decision_id = %s AND task_type = 'adjudicate_challenge'",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0)

                cursor.execute(
                    "SELECT workflow_status FROM cdp_core.workflow_instance "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["workflow_status"], "closed")
        finally:
            _cleanup_decision(decision_id)

    def test_failure_after_challenge_insert_rolls_back_everything(self) -> None:
        from cdp.core.services import raise_challenge_for_decision

        decision_id = f"vslice2-atomic-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)

            with mock.patch(
                "cdp.core.services.audit_repo.append_event",
                side_effect=RuntimeError("forced audit failure after challenge insert"),
            ):
                with self.assertRaises(RuntimeError):
                    raise_challenge_for_decision(_make_challenge_input(decision_id))

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.challenge_record "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0, "challenge should not survive rollback")

                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.workflow_task "
                    "WHERE registry_name = %s AND decision_id = %s AND task_type = 'adjudicate_challenge'",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0, "adjudication task should not survive rollback")

                cursor.execute(
                    "SELECT blocked, workflow_status FROM cdp_core.workflow_instance "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                row = cursor.fetchone()
                self.assertFalse(row["blocked"], "workflow instance block should not survive rollback")
                self.assertEqual(row["workflow_status"], "active")

                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_audit.event_log "
                    "WHERE payload ->> 'registry_name' = %s AND payload ->> 'decision_id' = %s "
                    "AND event_type IN ('workflow.transitioned', 'challenge.raised')",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0, "no challenge-related audit event should survive")
        finally:
            _cleanup_decision(decision_id)


if __name__ == "__main__":
    unittest.main()
