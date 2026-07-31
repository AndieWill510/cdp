"""Smoke tests for the 009 execution-record migration.

Two layers, following the pattern established in
test_migration_008_execution_authorization.py:

1. static smoke tests that inspect the DDL text with no database dependency;
2. an optional Postgres integration smoke test, enabled only when
   CDP_TEST_DATABASE_URL is set, that proves 001 -> ... -> 008 -> 009 apply
   cleanly and that re-running 009 is a no-op (idempotent, rerun-safe).
"""

from __future__ import annotations

import os
import re
import unittest
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DDL_001 = REPO_ROOT / "db" / "ddl" / "001-decision-registry-kernel.sql"
DDL_003 = REPO_ROOT / "db" / "ddl" / "003-nemawashi-workflow-rules.sql"
DDL_004 = REPO_ROOT / "db" / "ddl" / "004-decision-class-workflow-seed.sql"
DDL_005 = REPO_ROOT / "db" / "ddl" / "005-challenge-transition.sql"
DDL_006 = REPO_ROOT / "db" / "ddl" / "006-audit-event-ordering.sql"
DDL_007 = REPO_ROOT / "db" / "ddl" / "007-challenge-adjudication.sql"
DDL_008 = REPO_ROOT / "db" / "ddl" / "008-execution-authorization.sql"
DDL_009 = REPO_ROOT / "db" / "ddl" / "009-execution-record.sql"


def read_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_sql_comments(sql: str) -> str:
    """Drop `-- ...` line comments so text assertions ignore prose in comments."""
    return re.sub(r"--[^\n]*", "", sql)


class Migration009StaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sql = read_sql(DDL_009)
        cls.executable_sql = strip_sql_comments(cls.sql)

    def test_migration_file_exists(self) -> None:
        self.assertTrue(DDL_009.exists(), "009 execution-record DDL should exist")

    def test_migration_is_additive_only(self) -> None:
        compact_sql = re.sub(r"\s+", " ", self.executable_sql.lower())
        for forbidden in ("drop table", "drop schema", "truncate", "delete from"):
            self.assertNotIn(forbidden, compact_sql, f"009 should not contain: {forbidden}")

    def test_migration_uses_create_if_not_exists_for_new_table(self) -> None:
        self.assertIn(
            "CREATE TABLE IF NOT EXISTS cdp_core.execution_record", self.executable_sql
        )

    def test_migration_does_not_touch_schema_version(self) -> None:
        self.assertNotIn("cdp_core.schema_version", self.executable_sql)

    def test_migration_never_touches_workflow_instance(self) -> None:
        """The constitutional invariant this slice preserves: execution
        never closes or transitions the workflow instance, on any outcome.
        This migration must not contain any statement that writes to it."""
        self.assertNotIn("UPDATE cdp_core.workflow_instance", self.executable_sql)
        self.assertNotIn("UPDATE cdp_core.workflow_definition", self.executable_sql)
        self.assertNotIn("UPDATE cdp_core.workflow_task", self.executable_sql)

    def test_migration_registers_execution_status_vocabulary(self) -> None:
        required_snippets = [
            "'execution_status'",
            "('execution_status', 'succeeded'",
            "('execution_status', 'failed'",
            "('execution_status', 'partial'",
        ]
        for snippet in required_snippets:
            self.assertIn(snippet, self.sql)

    def test_execution_record_references_decision_authorization_workflow_actor(self) -> None:
        required_snippets = [
            "REFERENCES cdp_core.decision_registry (registry_name, decision_id)",
            "REFERENCES cdp_core.execution_authorization_record (authorization_id)",
            "REFERENCES cdp_core.workflow_instance (workflow_instance_id)",
            "REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)",
        ]
        for snippet in required_snippets:
            self.assertIn(snippet, self.sql)

    def test_execution_record_requires_authorization_link_and_result_summary(self) -> None:
        self.assertIn("authorization_id UUID NOT NULL", self.sql)
        self.assertIn("result_summary TEXT NOT NULL", self.sql)

    def test_execution_record_requires_attempted_and_completed_timestamps(self) -> None:
        self.assertIn("attempted_at TIMESTAMPTZ NOT NULL", self.sql)
        self.assertIn("completed_at TIMESTAMPTZ NOT NULL", self.sql)
        self.assertIn("chk_execution_record_completed_not_before_attempted", self.sql)

    def test_at_most_one_succeeded_execution_per_authorization(self) -> None:
        """Retries are allowed, but success is not repeatable: this must be
        a partial unique index scoped to execution_status = 'succeeded',
        not a plain unique constraint on authorization_id (which would
        forbid retries entirely)."""
        self.assertIn(
            "CREATE UNIQUE INDEX IF NOT EXISTS uq_execution_record_one_success_per_authorization",
            self.sql,
        )
        self.assertIn("WHERE execution_status = 'succeeded'", self.sql)


class Migration009PostgresSmokeTests(unittest.TestCase):
    """Optional Postgres execution smoke test.

    Set CDP_TEST_DATABASE_URL to enable. Applies 001 through 008, then 009
    twice inside one transaction (rolled back at the end) to prove
    rerun-safety without touching persistent local data.
    """

    def test_apply_001_through_008_then_009_twice_is_idempotent(self) -> None:
        database_url = os.environ.get("CDP_TEST_DATABASE_URL")
        if not database_url:
            self.skipTest("set CDP_TEST_DATABASE_URL to run Postgres DDL smoke test")

        conn = self._connect(database_url)
        try:
            cursor = conn.cursor()
            cursor.execute(read_sql(DDL_001))
            cursor.execute(read_sql(DDL_003))
            cursor.execute(read_sql(DDL_004))
            cursor.execute(read_sql(DDL_005))
            cursor.execute(read_sql(DDL_006))
            cursor.execute(read_sql(DDL_007))
            cursor.execute(read_sql(DDL_008))
            cursor.execute(read_sql(DDL_009))
            # Rerun 009 alone to prove idempotency/rerun-safety.
            cursor.execute(read_sql(DDL_009))

            cursor.execute("SELECT to_regclass('cdp_core.execution_record')")
            self.assertIsNotNone(cursor.fetchone()[0], "missing cdp_core.execution_record")

            cursor.execute(
                """
                SELECT count(*) FROM cdp_core.identifier_registry
                WHERE registry_name = 'execution_status'
                """
            )
            self.assertEqual(cursor.fetchone()[0], 3)

            cursor.execute(
                "SELECT 1 FROM pg_indexes WHERE indexname = "
                "'uq_execution_record_one_success_per_authorization'"
            )
            self.assertIsNotNone(
                cursor.fetchone(),
                "missing uq_execution_record_one_success_per_authorization",
            )

            # Unrelated configured workflow_definition rows must be untouched.
            cursor.execute(
                """
                SELECT applies_to_registry_name, applies_to_decision_class_id
                FROM cdp_core.workflow_definition
                WHERE workflow_code = 'nemawashi_default_v1' AND workflow_version = 'v1'
                """
            )
            applies_to_registry_name, applies_to_decision_class_id = cursor.fetchone()
            self.assertEqual(applies_to_registry_name, "sample_attorney_demo")
            self.assertEqual(applies_to_decision_class_id, "claim_approval")
        finally:
            conn.rollback()
            conn.close()

    @staticmethod
    def _connect(database_url: str) -> Any:
        try:
            import psycopg  # type: ignore

            return psycopg.connect(database_url)
        except ImportError:
            pass

        try:
            import psycopg2  # type: ignore

            return psycopg2.connect(database_url)
        except ImportError as exc:
            raise unittest.SkipTest("install psycopg or psycopg2 to run Postgres DDL smoke test") from exc


if __name__ == "__main__":
    unittest.main()
