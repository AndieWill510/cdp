"""Smoke tests for the 008 execution-authorization migration.

Two layers, following the pattern established in
test_migration_007_challenge_adjudication.py:

1. static smoke tests that inspect the DDL text with no database dependency;
2. an optional Postgres integration smoke test, enabled only when
   CDP_TEST_DATABASE_URL is set, that proves 001 -> 003 -> 004 -> 005 -> 006
   -> 007 -> 008 apply cleanly and that re-running 008 is a no-op
   (idempotent, rerun-safe).
"""

from __future__ import annotations

import os
import re
import unittest
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DDL_001 = REPO_ROOT / "db" / "ddl" / "001-decision-registry-kernel.sql"
DDL_003 = REPO_ROOT / "db" / "ddl" / "003-nemawashi-workflow-rules.sql"
DDL_004 = REPO_ROOT / "db" / "ddl" / "004-decision-class-workflow-seed.sql"
DDL_005 = REPO_ROOT / "db" / "ddl" / "005-challenge-transition.sql"
DDL_006 = REPO_ROOT / "db" / "ddl" / "006-audit-event-ordering.sql"
DDL_007 = REPO_ROOT / "db" / "ddl" / "007-challenge-adjudication.sql"
DDL_008 = REPO_ROOT / "db" / "ddl" / "008-execution-authorization.sql"


def read_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_sql_comments(sql: str) -> str:
    """Drop `-- ...` line comments so text assertions ignore prose in comments."""
    return re.sub(r"--[^\n]*", "", sql)


class Migration008StaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sql = read_sql(DDL_008)
        cls.executable_sql = strip_sql_comments(cls.sql)

    def test_migration_file_exists(self) -> None:
        self.assertTrue(DDL_008.exists(), "008 execution-authorization DDL should exist")

    def test_migration_is_additive_only(self) -> None:
        compact_sql = re.sub(r"\s+", " ", self.executable_sql.lower())
        for forbidden in ("drop table", "drop schema", "truncate", "delete from"):
            self.assertNotIn(forbidden, compact_sql, f"008 should not contain: {forbidden}")

    def test_migration_uses_create_if_not_exists_for_new_table(self) -> None:
        self.assertIn(
            "CREATE TABLE IF NOT EXISTS cdp_core.execution_authorization_record",
            self.executable_sql,
        )

    def test_migration_does_not_touch_schema_version(self) -> None:
        self.assertNotIn("cdp_core.schema_version", self.executable_sql)

    def test_migration_does_not_modify_any_workflow_definition_or_task_rows(self) -> None:
        """008 should not UPDATE workflow_definition or workflow_task -- it
        only adds a new table and new controlled vocabulary. The service
        layer, not this migration, completes tasks or advances instances."""
        self.assertNotIn("UPDATE cdp_core.workflow_definition", self.executable_sql)
        self.assertNotIn("UPDATE cdp_core.workflow_task", self.executable_sql)
        self.assertNotIn("UPDATE cdp_core.workflow_instance", self.executable_sql)

    def test_migration_registers_execution_authorization_status_vocabulary(self) -> None:
        required_snippets = [
            "'execution_authorization_status'",
            "('execution_authorization_status', 'authorized'",
        ]
        for snippet in required_snippets:
            self.assertIn(snippet, self.sql)

    def test_execution_authorization_record_references_decision_workflow_task_actor(
        self,
    ) -> None:
        required_snippets = [
            "REFERENCES cdp_core.decision_registry (registry_name, decision_id)",
            "REFERENCES cdp_core.workflow_instance (workflow_instance_id)",
            "REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)",
            "REFERENCES cdp_core.workflow_task (task_id)",
        ]
        for snippet in required_snippets:
            self.assertIn(snippet, self.sql)

    def test_execution_authorization_record_requires_rationale(self) -> None:
        self.assertIn("rationale TEXT NOT NULL", self.sql)

    def test_execution_authorization_record_does_not_create_task_columns_implying_creation(
        self,
    ) -> None:
        """The task-linkage column should be named completed_task_id, not
        created_task_id -- this slice completes an existing task, it does
        not create one."""
        self.assertIn("completed_task_id UUID NOT NULL", self.sql)
        self.assertNotIn("created_task_id", self.sql)

    def test_completed_task_id_is_required(self) -> None:
        """A successful authorization always completes exactly one review
        task, so the DB should enforce that no authorization record can
        exist without identifying it."""
        self.assertIn("completed_task_id UUID NOT NULL", self.sql)

    def test_one_terminal_authorization_per_decision(self) -> None:
        self.assertIn("CONSTRAINT uq_execution_authorization_decision", self.sql)
        self.assertIn("UNIQUE (registry_name, decision_id)", self.sql)


class Migration008PostgresSmokeTests(unittest.TestCase):
    """Optional Postgres execution smoke test.

    Set CDP_TEST_DATABASE_URL to enable. Applies 001, 003, 004, 005, 006,
    007, then 008 twice inside one transaction (rolled back at the end) to
    prove rerun-safety without touching persistent local data.
    """

    def test_apply_001_through_007_then_008_twice_is_idempotent(self) -> None:
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
            # Rerun 008 alone to prove idempotency/rerun-safety.
            cursor.execute(read_sql(DDL_008))

            cursor.execute("SELECT to_regclass('cdp_core.execution_authorization_record')")
            self.assertIsNotNone(
                cursor.fetchone()[0], "missing cdp_core.execution_authorization_record"
            )

            cursor.execute(
                """
                SELECT count(*) FROM cdp_core.identifier_registry
                WHERE registry_name = 'execution_authorization_status'
                """
            )
            self.assertEqual(cursor.fetchone()[0], 1)

            # The unique constraint (one terminal authorization per decision)
            # and the NOT NULL enforcement on completed_task_id must actually
            # exist in the live schema, not just in the DDL text.
            cursor.execute(
                "SELECT 1 FROM pg_constraint WHERE conname = 'uq_execution_authorization_decision'"
            )
            self.assertIsNotNone(
                cursor.fetchone(), "missing uq_execution_authorization_decision constraint"
            )

            cursor.execute(
                """
                SELECT is_nullable FROM information_schema.columns
                WHERE table_schema = 'cdp_core'
                  AND table_name = 'execution_authorization_record'
                  AND column_name = 'completed_task_id'
                """
            )
            self.assertEqual(cursor.fetchone()[0], "NO", "completed_task_id should be NOT NULL")

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
