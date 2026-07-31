"""Integration tests for the authorize_execution vertical slice.

These tests exercise the real repository/service stack against Postgres.
They require:

- CDP_TEST_DATABASE_URL pointing at a disposable/local database
- db/ddl/001, 003, 004, 005, 006, 007, and 008 already applied to that database

Each test uses a uniquely-namespaced decision_id and cleans up everything it
inserts in a `finally` block, so these tests do not contaminate persistent
local data. They are skipped entirely when CDP_TEST_DATABASE_URL is not set,
or when 008's execution_authorization_record table is not yet applied.

Import note: this module uses cdp.core (dataclasses, modern union type
hints) which targets the project's Python 3.12 runtime. Run it with the
interpreter used by the Docker stack (e.g. `docker compose exec cdp-api
pytest tests/test_execution_authorization_service.py`), not an older local
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


def _execution_authorization_table_exists() -> bool:
    with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
        cursor.execute("SELECT to_regclass('cdp_core.execution_authorization_record')")
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
            antecedent_text="Execution-authorization-slice integration test decision.",
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


def _adjudicate(decision_id, challenge_id, outcome: str):
    from cdp.core.services import AdjudicationInput, adjudicate_challenge

    return adjudicate_challenge(
        AdjudicationInput(
            registry_name=REGISTRY_NAME,
            decision_id=decision_id,
            challenge_id=challenge_id,
            adjudicated_by_actor_id="review_board",
            outcome=outcome,
            rationale=f"Adjudication-slice test rationale for outcome={outcome}.",
        )
    )


def _make_authorization_input(decision_id: str):
    from cdp.core.services import ExecutionAuthorizationInput

    return ExecutionAuthorizationInput(
        registry_name=REGISTRY_NAME,
        decision_id=decision_id,
        authorized_by_actor_id="review_board",
        rationale=(
            "No blocking challenge work remains; authorized to proceed to "
            "execution under the current workflow conditions."
        ),
    )


def _cleanup_decision(decision_id: str) -> None:
    with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
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
class AuthorizeExecutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ.setdefault("DATABASE_URL", _database_url())
        if not _decision_workflow_configured():
            raise unittest.SkipTest(
                "004-decision-class-workflow-seed.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )
        if not _execution_authorization_table_exists():
            raise unittest.SkipTest(
                "008-execution-authorization.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )

    def test_happy_path_completes_review_task_advances_workflow_and_orders_audit_events(
        self,
    ) -> None:
        from cdp.core.services import authorize_execution

        decision_id = f"vslice4-happy-{uuid.uuid4().hex[:12]}"
        try:
            decision_result = _create_decision(decision_id)
            review_task_id = decision_result["task"]["task_id"]

            result = authorize_execution(_make_authorization_input(decision_id))

            self.assertEqual(result["authorization"]["authorization_status"], "authorized")
            self.assertEqual(result["authorization"]["completed_task_id"], review_task_id)
            self.assertEqual(result["completed_task"]["task_id"], review_task_id)
            self.assertEqual(result["completed_task"]["task_status"], "completed")
            self.assertIsNotNone(result["completed_task"]["completed_at"])
            self.assertEqual(result["workflow_instance"]["workflow_status"], "advanced")

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                # 1: happy path completes the existing review_decision task
                cursor.execute(
                    "SELECT task_status, completed_at FROM cdp_core.workflow_task WHERE task_id = %s",
                    (review_task_id,),
                )
                row = cursor.fetchone()
                self.assertEqual(row["task_status"], "completed")
                self.assertIsNotNone(row["completed_at"])

                # 2: workflow status becomes advanced
                cursor.execute(
                    "SELECT workflow_status FROM cdp_core.workflow_instance "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["workflow_status"], "advanced")

                # 3: audit order is execution.authorized -> workflow.transitioned -> task.completed
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
                    ],
                )

                cursor.execute(
                    "SELECT payload FROM cdp_audit.event_log WHERE event_type = 'execution.authorized' "
                    "AND payload ->> 'decision_id' = %s",
                    (decision_id,),
                )
                payload = cursor.fetchone()["payload"]
                for key in (
                    "registry_name",
                    "decision_id",
                    "authorization_id",
                    "workflow_instance_id",
                    "completed_task_id",
                ):
                    self.assertIn(key, payload)
        finally:
            _cleanup_decision(decision_id)

    def test_open_raised_challenge_blocks_with_409(self) -> None:
        from cdp.core.services import ExecutionAuthorizationNotPermitted, authorize_execution

        decision_id = f"vslice4-raised-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)
            _raise_challenge(decision_id)

            with self.assertRaises(ExecutionAuthorizationNotPermitted):
                authorize_execution(_make_authorization_input(decision_id))

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.execution_authorization_record "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0)
        finally:
            _cleanup_decision(decision_id)

    def test_open_under_review_challenge_blocks_with_409(self) -> None:
        from cdp.core.services import ExecutionAuthorizationNotPermitted, authorize_execution

        decision_id = f"vslice4-underreview-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)
            challenge = _raise_challenge(decision_id)["challenge"]
            _adjudicate(decision_id, challenge["challenge_id"], "deferred")

            with self.assertRaises(ExecutionAuthorizationNotPermitted):
                authorize_execution(_make_authorization_input(decision_id))

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.execution_authorization_record "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0)
        finally:
            _cleanup_decision(decision_id)

    def test_open_adjudicate_challenge_task_blocks_with_409(self) -> None:
        """Defense-in-depth: force challenge_status out of sync with its task
        (direct DB manipulation, bypassing the service layer) to prove the
        open-task check independently blocks even if challenge_status alone
        would not have."""
        from cdp.core.services import ExecutionAuthorizationNotPermitted, authorize_execution

        decision_id = f"vslice4-opentask-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)
            challenge = _raise_challenge(decision_id)["challenge"]

            with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE cdp_core.challenge_record SET challenge_status = 'resolved', "
                    "resolved_at = now() WHERE challenge_id = %s",
                    (challenge["challenge_id"],),
                )
                conn.commit()

            with self.assertRaises(ExecutionAuthorizationNotPermitted):
                authorize_execution(_make_authorization_input(decision_id))

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.execution_authorization_record "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0)
        finally:
            _cleanup_decision(decision_id)

    def test_resolved_dismissed_withdrawn_challenges_do_not_block(self) -> None:
        from cdp.core.services import authorize_execution

        decision_id = f"vslice4-nonblocking-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)

            sustained_challenge = _raise_challenge(decision_id, challenge_text="First concern.")[
                "challenge"
            ]
            _adjudicate(decision_id, sustained_challenge["challenge_id"], "sustained")

            not_sustained_challenge = _raise_challenge(
                decision_id, challenge_text="Second concern."
            )["challenge"]
            _adjudicate(decision_id, not_sustained_challenge["challenge_id"], "not_sustained")

            with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT challenge_status FROM cdp_core.challenge_record "
                    "WHERE registry_name = %s AND decision_id = %s ORDER BY created_at",
                    (REGISTRY_NAME, decision_id),
                )
                statuses = {row[0] for row in cursor.fetchall()}
                self.assertEqual(statuses, {"resolved", "dismissed"})

            result = authorize_execution(_make_authorization_input(decision_id))
            self.assertEqual(result["authorization"]["authorization_status"], "authorized")
        finally:
            _cleanup_decision(decision_id)

    def test_missing_open_review_task_returns_409(self) -> None:
        """No authorization exists yet for this decision, so the
        already-authorized check passes through cleanly and this must
        surface as the general ExecutionAuthorizationNotPermitted conflict,
        not ExecutionAlreadyAuthorized."""
        from cdp.core.services import ExecutionAuthorizationNotPermitted, authorize_execution

        decision_id = f"vslice4-noreviewtask-{uuid.uuid4().hex[:12]}"
        try:
            decision_result = _create_decision(decision_id)
            review_task_id = decision_result["task"]["task_id"]

            with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE cdp_core.workflow_task SET task_status = 'completed', "
                    "completed_at = now() WHERE task_id = %s",
                    (review_task_id,),
                )
                conn.commit()

            with self.assertRaises(ExecutionAuthorizationNotPermitted):
                authorize_execution(_make_authorization_input(decision_id))

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.execution_authorization_record "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0)
        finally:
            _cleanup_decision(decision_id)

    def test_second_authorization_attempt_returns_409(self) -> None:
        """The already-authorized check runs immediately after confirming
        the decision exists -- before the workflow/challenge/task
        eligibility checks -- so a second attempt must fail because the
        decision is already authorized, not because a downstream side
        effect of the first call (the review task now being completed)
        happens to make it look ineligible. uq_execution_authorization_decision
        remains the DB-level backstop against a concurrent race (two
        requests passing this application-level check before either
        commits), which this single-threaded test cannot exercise."""
        from cdp.core.services import ExecutionAlreadyAuthorized, authorize_execution

        decision_id = f"vslice4-duplicate-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)
            authorize_execution(_make_authorization_input(decision_id))

            with self.assertRaises(ExecutionAlreadyAuthorized):
                authorize_execution(_make_authorization_input(decision_id))

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.execution_authorization_record "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 1, "only the first authorization should persist")
        finally:
            _cleanup_decision(decision_id)

    def test_failure_after_authorization_insert_rolls_back_everything(self) -> None:
        from cdp.core.services import authorize_execution

        decision_id = f"vslice4-atomic-{uuid.uuid4().hex[:12]}"
        try:
            _create_decision(decision_id)

            with mock.patch(
                "cdp.core.services.audit_repo.append_event",
                side_effect=RuntimeError("forced audit failure after authorization insert"),
            ):
                with self.assertRaises(RuntimeError):
                    authorize_execution(_make_authorization_input(decision_id))

            with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_core.execution_authorization_record "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0, "authorization should not survive rollback")

                cursor.execute(
                    "SELECT task_status, completed_at FROM cdp_core.workflow_task "
                    "WHERE registry_name = %s AND decision_id = %s AND task_type = 'review_decision'",
                    (REGISTRY_NAME, decision_id),
                )
                row = cursor.fetchone()
                self.assertEqual(row["task_status"], "open", "task completion should roll back")
                self.assertIsNone(row["completed_at"])

                cursor.execute(
                    "SELECT workflow_status FROM cdp_core.workflow_instance "
                    "WHERE registry_name = %s AND decision_id = %s",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(
                    cursor.fetchone()["workflow_status"], "active", "workflow advance should roll back"
                )

                cursor.execute(
                    "SELECT count(*) AS n FROM cdp_audit.event_log "
                    "WHERE payload ->> 'registry_name' = %s AND payload ->> 'decision_id' = %s "
                    "AND event_type = 'execution.authorized'",
                    (REGISTRY_NAME, decision_id),
                )
                self.assertEqual(cursor.fetchone()["n"], 0, "no authorization audit event should survive")
        finally:
            _cleanup_decision(decision_id)


if __name__ == "__main__":
    unittest.main()
