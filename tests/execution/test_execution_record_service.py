"""Integration tests for the record_execution_attempt vertical slice.

These tests exercise the real repository/service stack against Postgres.
They require:

- CDP_TEST_DATABASE_URL pointing at a disposable/local database
- db/ddl/001 through 009 already applied to that database

Each test uses a uniquely-namespaced decision_id and cleans up everything it
inserts in a `finally` block, so these tests do not contaminate persistent
local data. They are skipped entirely when CDP_TEST_DATABASE_URL is not set,
or when 009's execution_record table is not yet applied.

Import note: this module uses cdp.core (dataclasses, modern union type
hints) which targets the project's Python 3.12 runtime. Run it with the
interpreter used by the Docker stack (e.g. `docker compose exec cdp-api
pytest tests/test_execution_record_service.py`), not an older local
virtualenv.
"""

from __future__ import annotations

import os
import unittest
import uuid
from datetime import datetime, timedelta, timezone
from unittest import mock

import psycopg
from psycopg.rows import dict_row

REGISTRY_NAME = "sample_attorney_demo"
DECISION_CLASS_ID = "claim_approval"


def _database_url() -> str:
    return os.environ.get("CDP_TEST_DATABASE_URL", "postgresql://cdp:cdp@localhost:5432/cdp")


def _execution_record_table_exists() -> bool:
    with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
        cursor.execute("SELECT to_regclass('cdp_core.execution_record')")
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
            antecedent_text="Execution-record-slice integration test decision.",
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


def _authorize(decision_id: str):
    from cdp.core.services import ExecutionAuthorizationInput, authorize_execution

    return authorize_execution(
        ExecutionAuthorizationInput(
            registry_name=REGISTRY_NAME,
            decision_id=decision_id,
            authorized_by_actor_id="review_board",
            rationale=(
                "No blocking challenge work remains; authorized to proceed to "
                "execution under the current workflow conditions."
            ),
        )
    )


def _raise_challenge(decision_id: str, *, challenge_text: str = "A concern about this decision."):
    from cdp.core.services import ChallengeInput, raise_challenge_for_decision

    return raise_challenge_for_decision(
        ChallengeInput(
            registry_name=REGISTRY_NAME,
            decision_id=decision_id,
            raised_by_actor_id="user_442",
            challenge_text=challenge_text,
            challenge_type="policy",
        )
    )


def _make_execution_input(decision_id: str, execution_status: str = "succeeded", **overrides):
    from cdp.core.services import ExecutionRecordInput

    attempted_at = overrides.pop("attempted_at", datetime.now(timezone.utc) - timedelta(minutes=5))
    completed_at = overrides.pop("completed_at", datetime.now(timezone.utc))

    return ExecutionRecordInput(
        registry_name=REGISTRY_NAME,
        decision_id=decision_id,
        executed_by_actor_id=overrides.pop("executed_by_actor_id", "workflow_engine"),
        execution_status=execution_status,
        result_summary=overrides.pop(
            "result_summary", f"Execution-slice test result for status={execution_status}."
        ),
        attempted_at=attempted_at,
        completed_at=completed_at,
    )


def _cleanup_decision(decision_id: str) -> None:
    with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
        cursor.execute(
            "DELETE FROM cdp_core.execution_record WHERE registry_name = %s AND decision_id = %s",
            (REGISTRY_NAME, decision_id),
        )
        cursor.execute(
            "DELETE FROM cdp_core.execution_authorization_record "
            "WHERE registry_name = %s AND decision_id = %s",
            (REGISTRY_NAME, decision_id),
        )
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
class RecordExecutionAttemptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ.setdefault("DATABASE_URL", _database_url())
        if not _decision_workflow_configured():
            raise unittest.SkipTest(
                "004-decision-class-workflow-seed.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )
        if not _execution_record_table_exists():
            raise unittest.SkipTest(
                "009-execution-record.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )

    def test_succeeded_outcome_records_attempt_and_leaves_workflow_untouched(self) -> None:
        """The constitutional invariant this slice preserves: success does
        not close the workflow or exempt the decision from repair. Only one
        audit event is emitted -- there is no workflow.transitioned, because
        nothing about the workflow changes on any outcome."""
        from cdp.core.services import record_execution_attempt

        decision_id = f"vslice5-succeeded-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)
            authorization_result = _authorize(decision_id)
            authorization_id = authorization_result["authorization"]["authorization_id"]

            result = record_execution_attempt(_make_execution_input(decision_id, "succeeded"))

            self.assertEqual(result["execution_record"]["execution_status"], "succeeded")
            self.assertEqual(result["execution_record"]["authorization_id"], authorization_id)
            self.assertEqual(result["workflow_instance"]["workflow_status"], "advanced")
            self.assertFalse(result["workflow_instance"]["blocked"])
            self.assertIsNone(result["workflow_instance"]["closed_at"])

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT workflow_status, blocked, closed_at FROM cdp_core.workflow_instance "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                row = cursor.fetchone()
                self.assertEqual(row["workflow_status"], "advanced", "success must not close the workflow")
                self.assertFalse(row["blocked"])
                self.assertIsNone(row["closed_at"])

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
                        "execution.authorized",
                        "workflow.transitioned",
                        "task.completed",
                        "execution.recorded",
                    ],
                    "execution must add exactly one event (execution.recorded) and no "
                    "workflow.transitioned of its own",
                )
        finally:
            _cleanup_decision(decision_id)

    def test_failed_outcome_leaves_workflow_untouched_and_allows_retry(self) -> None:
        from cdp.core.services import record_execution_attempt

        decision_id = f"vslice5-failed-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)
            _authorize(decision_id)

            failed_result = record_execution_attempt(_make_execution_input(decision_id, "failed"))
            self.assertEqual(failed_result["execution_record"]["execution_status"], "failed")
            self.assertEqual(failed_result["workflow_instance"]["workflow_status"], "advanced")

            # A retry after failure must succeed and coexist with the failed row.
            retry_result = record_execution_attempt(
                _make_execution_input(decision_id, "succeeded")
            )
            self.assertEqual(retry_result["execution_record"]["execution_status"], "succeeded")

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT execution_status FROM cdp_core.execution_record "
                    "WHERE registry_name = %s AND decision_id = %s ORDER BY created_at",
                    (REGISTRY_NAME, decision_id),
                )
                statuses = [row["execution_status"] for row in cursor.fetchall()]
                self.assertEqual(statuses, ["failed", "succeeded"])
        finally:
            _cleanup_decision(decision_id)

    def test_partial_outcome_leaves_workflow_untouched(self) -> None:
        from cdp.core.services import record_execution_attempt

        decision_id = f"vslice5-partial-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)
            _authorize(decision_id)

            result = record_execution_attempt(_make_execution_input(decision_id, "partial"))
            self.assertEqual(result["execution_record"]["execution_status"], "partial")
            self.assertEqual(result["workflow_instance"]["workflow_status"], "advanced")
        finally:
            _cleanup_decision(decision_id)

    def test_second_succeeded_attempt_is_rejected(self) -> None:
        from cdp.core.services import ExecutionAlreadySucceeded, record_execution_attempt

        decision_id = f"vslice5-doublesuccess-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)
            _authorize(decision_id)
            record_execution_attempt(_make_execution_input(decision_id, "succeeded"))

            with self.assertRaises(ExecutionAlreadySucceeded):
                record_execution_attempt(_make_execution_input(decision_id, "succeeded"))

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.execution_record "
                    "WHERE registry_name = %s AND decision_id = %s AND execution_status = 'succeeded'",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 1)
        finally:
            _cleanup_decision(decision_id)

    def test_missing_authorization_returns_clean_error_with_no_partial_state(self) -> None:
        from cdp.core.services import DecisionNotAuthorizedForExecution, record_execution_attempt

        decision_id = f"vslice5-noauth-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)

            with self.assertRaises(DecisionNotAuthorizedForExecution):
                record_execution_attempt(_make_execution_input(decision_id))

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.execution_record "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0)
        finally:
            _cleanup_decision(decision_id)

    def test_missing_decision_returns_clean_error(self) -> None:
        from cdp.core.services import DecisionNotFound, record_execution_attempt

        decision_id = f"vslice5-nodecision-{uuid.uuid4().hex[:12]}"
        with self.assertRaises(DecisionNotFound):
            record_execution_attempt(_make_execution_input(decision_id))

    def test_workflow_blocked_by_new_challenge_after_authorization_blocks_execution(self) -> None:
        """A decision may be authorized, then re-challenged before execution
        is ever recorded. This proves that gap is closed: execution must
        re-check workflow state at record time, not trust the authorization
        row's now-stale eligibility."""
        from cdp.core.services import ExecutionNotPermitted, record_execution_attempt

        decision_id = f"vslice5-reblocked-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)
            _authorize(decision_id)
            _raise_challenge(decision_id, challenge_text="A new concern raised after authorization.")

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT workflow_status, blocked FROM cdp_core.workflow_instance "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                row = cursor.fetchone()
                self.assertTrue(row["blocked"])
                self.assertEqual(row["workflow_status"], "blocked")

            with self.assertRaises(ExecutionNotPermitted):
                record_execution_attempt(_make_execution_input(decision_id))

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.execution_record "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0)
        finally:
            _cleanup_decision(decision_id)

    def test_completed_before_attempted_is_rejected(self) -> None:
        from cdp.core.services import record_execution_attempt

        decision_id = f"vslice5-badtimestamps-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)
            _authorize(decision_id)

            now = datetime.now(timezone.utc)
            with self.assertRaises(ValueError):
                record_execution_attempt(
                    _make_execution_input(
                        decision_id,
                        attempted_at=now,
                        completed_at=now - timedelta(minutes=1),
                    )
                )

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.execution_record "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0)
        finally:
            _cleanup_decision(decision_id)

    def test_failure_after_execution_insert_rolls_back_everything(self) -> None:
        from cdp.core.services import record_execution_attempt

        decision_id = f"vslice5-atomic-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)
            _authorize(decision_id)

            with mock.patch(
                "cdp.core.services.audit_repo.append_event",
                side_effect=RuntimeError("forced audit failure after execution insert"),
            ):
                with self.assertRaises(RuntimeError):
                    record_execution_attempt(_make_execution_input(decision_id, "succeeded"))

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.execution_record "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0, "execution record should not survive rollback")

                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_audit.event_log "
                    "WHERE payload ->> 'registry_name' = %s AND payload ->> 'decision_id' = %s "
                    "AND event_type = 'execution.recorded'",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0, "no execution audit event should survive")
        finally:
            _cleanup_decision(decision_id)


if __name__ == "__main__":
    unittest.main()
