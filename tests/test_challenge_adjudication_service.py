"""Integration tests for the adjudicate_challenge vertical slice.

These tests exercise the real repository/service stack against Postgres.
They require:

- CDP_TEST_DATABASE_URL pointing at a disposable/local database
- db/ddl/001, 003, 004, 005, 006, and 007 already applied to that database

Each test uses a uniquely-namespaced decision_id and cleans up everything it
inserts in a `finally` block, so these tests do not contaminate persistent
local data. They are skipped entirely when CDP_TEST_DATABASE_URL is not set,
or when 006's event_sequence column or 007's challenge_adjudication_record
table are not yet applied.

Import note: this module uses cdp.core (dataclasses, modern union type
hints) which targets the project's Python 3.12 runtime. Run it with the
interpreter used by the Docker stack (e.g. `docker compose exec cdp-api
pytest tests/test_challenge_adjudication_service.py`), not an older local
virtualenv.
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


def _adjudication_table_exists() -> bool:
    with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
        cursor.execute("SELECT to_regclass('cdp_core.challenge_adjudication_record')")
        return cursor.fetchone()[0] is not None


def _event_sequence_column_exists() -> bool:
    with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT 1 FROM information_schema.columns
            WHERE table_schema = 'cdp_audit' AND table_name = 'event_log'
              AND column_name = 'event_sequence'
            """
        )
        return cursor.fetchone() is not None


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
            antecedent_text="Adjudication-slice integration test decision.",
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


def _raise_challenge(decision_id: str):
    from cdp.core.services import ChallengeInput, raise_challenge_for_decision

    return raise_challenge_for_decision(
        ChallengeInput(
            registry_name=REGISTRY_NAME,
            decision_id=decision_id,
            raised_by_actor_id="user_442",
            challenge_text="This recommendation overlooks a documented policy exception.",
            challenge_type="policy",
        )
    )


def _make_adjudication_input(decision_id: str, challenge_id, outcome: str):
    from cdp.core.services import AdjudicationInput

    return AdjudicationInput(
        registry_name=REGISTRY_NAME,
        decision_id=decision_id,
        challenge_id=challenge_id,
        adjudicated_by_actor_id="review_board",
        outcome=outcome,
        rationale=f"Adjudication-slice test rationale for outcome={outcome}.",
    )


def _cleanup_decision(decision_id: str) -> None:
    with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
        cursor.execute(
            "DELETE FROM cdp_core.challenge_adjudication_record "
            "WHERE registry_name = %s AND decision_id = %s",
            (REGISTRY_NAME, decision_id),
        )
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
class AdjudicateChallengeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ.setdefault("DATABASE_URL", _database_url())
        if not _decision_workflow_configured():
            raise unittest.SkipTest(
                "004-decision-class-workflow-seed.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )
        if not _event_sequence_column_exists():
            raise unittest.SkipTest(
                "006-audit-event-ordering.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )
        if not _adjudication_table_exists():
            raise unittest.SkipTest(
                "007-challenge-adjudication.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )

    def test_sustained_outcome_resolves_challenge_completes_task_and_unblocks_workflow(
        self,
    ) -> None:
        from cdp.core.services import adjudicate_challenge

        decision_id = f"vslice3-sustained-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)
            challenge_result = _raise_challenge(decision_id)
            challenge_id = challenge_result["challenge"]["challenge_id"]
            task_id = challenge_result["task"]["task_id"]

            result = adjudicate_challenge(
                _make_adjudication_input(decision_id, challenge_id, "sustained")
            )

            self.assertEqual(result["adjudication"]["outcome"], "sustained")
            self.assertEqual(result["adjudication"]["resulting_challenge_status"], "resolved")
            self.assertEqual(result["adjudication"]["adjudicated_task_id"], task_id)
            self.assertEqual(result["challenge"]["challenge_status"], "resolved")
            self.assertIsNotNone(result["challenge"]["resolved_at"])
            self.assertIsNotNone(result["task"])
            self.assertEqual(result["task"]["task_status"], "completed")
            self.assertIsNotNone(result["task"]["completed_at"])
            self.assertIsNotNone(result["workflow_instance"])
            self.assertFalse(result["workflow_instance"]["blocked"])
            self.assertEqual(result["workflow_instance"]["workflow_status"], "active")

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.challenge_adjudication_record "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 1)

                cursor.execute(
                    "SELECT event_type FROM cdp_audit.event_log "
                    "WHERE payload ->> 'registry_name' = %s AND payload ->> 'decision_id' = %s "
                    "ORDER BY event_sequence",
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
                        "challenge.adjudicated",
                        "workflow.transitioned",
                        "task.completed",
                    ],
                )
        finally:
            _cleanup_decision(decision_id)

    def test_not_sustained_outcome_dismisses_challenge(self) -> None:
        from cdp.core.services import adjudicate_challenge

        decision_id = f"vslice3-not-sustained-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)
            challenge_result = _raise_challenge(decision_id)
            challenge_id = challenge_result["challenge"]["challenge_id"]

            result = adjudicate_challenge(
                _make_adjudication_input(decision_id, challenge_id, "not_sustained")
            )

            self.assertEqual(result["challenge"]["challenge_status"], "dismissed")
            self.assertEqual(result["task"]["task_status"], "completed")
            self.assertFalse(result["workflow_instance"]["blocked"])
        finally:
            _cleanup_decision(decision_id)

    def test_deferred_outcome_leaves_task_and_workflow_untouched_and_allows_reajudication(
        self,
    ) -> None:
        from cdp.core.services import adjudicate_challenge

        decision_id = f"vslice3-deferred-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)
            challenge_result = _raise_challenge(decision_id)
            challenge_id = challenge_result["challenge"]["challenge_id"]

            deferred_result = adjudicate_challenge(
                _make_adjudication_input(decision_id, challenge_id, "deferred")
            )

            self.assertEqual(deferred_result["challenge"]["challenge_status"], "under_review")
            self.assertIsNone(deferred_result["challenge"]["resolved_at"])
            self.assertIsNone(deferred_result["task"])
            self.assertIsNone(deferred_result["workflow_instance"])

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT task_status, completed_at FROM cdp_core.workflow_task "
                    "WHERE registry_name = %s AND decision_id = %s AND task_type = 'adjudicate_challenge'",
                    (REGISTRY_NAME, decision_id),
                )
                row = cursor.fetchone()
                self.assertEqual(row["task_status"], "open")
                self.assertIsNone(row["completed_at"])

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
                    "ORDER BY event_sequence",
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
                        "challenge.adjudicated",
                    ],
                    "a deferred adjudication should only add challenge.adjudicated -- "
                    "the single workflow.transitioned above is from raising the "
                    "challenge, not from this deferred adjudication",
                )
                self.assertNotIn("task.completed", event_types)

            # Deferred is non-terminal, so a second, final adjudication is allowed.
            final_result = adjudicate_challenge(
                _make_adjudication_input(decision_id, challenge_id, "sustained")
            )
            self.assertEqual(final_result["challenge"]["challenge_status"], "resolved")
            self.assertEqual(final_result["task"]["task_status"], "completed")
            self.assertFalse(final_result["workflow_instance"]["blocked"])

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.challenge_adjudication_record "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 2)
        finally:
            _cleanup_decision(decision_id)

    def test_unblocks_only_after_last_open_challenge_is_adjudicated(self) -> None:
        from cdp.core.services import adjudicate_challenge

        decision_id = f"vslice3-multi-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)
            first_challenge = _raise_challenge(decision_id)["challenge"]

            # Raise a second challenge directly against the same (already
            # blocked) workflow instance/decision.
            from cdp.core.services import ChallengeInput, raise_challenge_for_decision

            second_challenge = raise_challenge_for_decision(
                ChallengeInput(
                    registry_name=REGISTRY_NAME,
                    decision_id=decision_id,
                    raised_by_actor_id="user_442",
                    challenge_text="A second, independent concern about this decision.",
                    challenge_type="evidentiary",
                )
            )["challenge"]

            first_result = adjudicate_challenge(
                _make_adjudication_input(decision_id, first_challenge["challenge_id"], "sustained")
            )
            self.assertIsNone(
                first_result["workflow_instance"],
                "workflow should stay blocked while the second challenge is still open",
            )

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT blocked FROM cdp_core.workflow_instance "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertTrue(cursor.fetchone()["blocked"])

            second_result = adjudicate_challenge(
                _make_adjudication_input(
                    decision_id, second_challenge["challenge_id"], "not_sustained"
                )
            )
            self.assertIsNotNone(
                second_result["workflow_instance"],
                "workflow should unblock once the last open challenge is adjudicated",
            )
            self.assertFalse(second_result["workflow_instance"]["blocked"])
        finally:
            _cleanup_decision(decision_id)

    def test_missing_decision_returns_clean_error_with_no_partial_state(self) -> None:
        from cdp.core.services import DecisionNotFound, adjudicate_challenge

        decision_id = f"vslice3-missing-decision-{uuid.uuid4().hex[:12]}"
        try:
            with self.assertRaises(DecisionNotFound):
                adjudicate_challenge(
                    _make_adjudication_input(decision_id, uuid.uuid4(), "sustained")
                )

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.challenge_adjudication_record "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0)
        finally:
            _cleanup_decision(decision_id)

    def test_missing_challenge_returns_clean_error_with_no_partial_state(self) -> None:
        from cdp.core.services import ChallengeNotFound, adjudicate_challenge

        decision_id = f"vslice3-missing-challenge-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)

            with self.assertRaises(ChallengeNotFound):
                adjudicate_challenge(
                    _make_adjudication_input(decision_id, uuid.uuid4(), "sustained")
                )

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.challenge_adjudication_record "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0)
        finally:
            _cleanup_decision(decision_id)

    def test_already_terminal_challenge_rejects_further_adjudication(self) -> None:
        from cdp.core.services import ChallengeNotAdjudicable, adjudicate_challenge

        decision_id = f"vslice3-terminal-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)
            challenge_id = _raise_challenge(decision_id)["challenge"]["challenge_id"]
            adjudicate_challenge(
                _make_adjudication_input(decision_id, challenge_id, "sustained")
            )

            with self.assertRaises(ChallengeNotAdjudicable):
                adjudicate_challenge(
                    _make_adjudication_input(decision_id, challenge_id, "not_sustained")
                )

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.challenge_adjudication_record "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 1, "second adjudication must not persist")
        finally:
            _cleanup_decision(decision_id)

    def test_failure_after_adjudication_insert_rolls_back_everything(self) -> None:
        from cdp.core.services import adjudicate_challenge

        decision_id = f"vslice3-atomic-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)
            challenge_id = _raise_challenge(decision_id)["challenge"]["challenge_id"]

            with mock.patch(
                "cdp.core.services.audit_repo.append_event",
                side_effect=RuntimeError("forced audit failure after adjudication insert"),
            ):
                with self.assertRaises(RuntimeError):
                    adjudicate_challenge(
                        _make_adjudication_input(decision_id, challenge_id, "sustained")
                    )

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.challenge_adjudication_record "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0, "adjudication should not survive rollback")

                cursor.execute(
                    "SELECT challenge_status, resolved_at FROM cdp_core.challenge_record "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                row = cursor.fetchone()
                self.assertEqual(row["challenge_status"], "raised", "challenge status should roll back")
                self.assertIsNone(row["resolved_at"])

                cursor.execute(
                    "SELECT task_status, completed_at FROM cdp_core.workflow_task "
                    "WHERE registry_name = %s AND decision_id = %s AND task_type = 'adjudicate_challenge'",
                    (REGISTRY_NAME, decision_id),
                )
                row = cursor.fetchone()
                self.assertEqual(row["task_status"], "open", "task completion should roll back")
                self.assertIsNone(row["completed_at"])

                cursor.execute(
                    "SELECT blocked FROM cdp_core.workflow_instance "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertTrue(cursor.fetchone()["blocked"], "workflow unblock should roll back")

                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_audit.event_log "
                    "WHERE payload ->> 'registry_name' = %s AND payload ->> 'decision_id' = %s "
                    "AND event_type = 'challenge.adjudicated'",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0, "no adjudication audit event should survive")
        finally:
            _cleanup_decision(decision_id)


if __name__ == "__main__":
    unittest.main()
