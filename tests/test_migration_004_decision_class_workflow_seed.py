"""Smoke tests for the 004 decision-class/workflow-applicability seed migration.

Two layers, following the pattern established in
test_nemawashi_workflow_rules_ddl.py:

1. static smoke tests that inspect the DDL text with no database dependency;
2. an optional Postgres integration smoke test, enabled only when
   CDP_TEST_DATABASE_URL is set, that proves 001 -> 003 -> 004 apply cleanly
   and that re-running 004 is a no-op (idempotent, rerun-safe).
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


def read_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_sql_comments(sql: str) -> str:
    """Drop `-- ...` line comments so text assertions ignore prose in comments."""
    return re.sub(r"--[^\n]*", "", sql)


class Migration004StaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sql = read_sql(DDL_004)
        cls.executable_sql = strip_sql_comments(cls.sql)

    def test_migration_file_exists(self) -> None:
        self.assertTrue(DDL_004.exists(), "004 decision-class/workflow seed DDL should exist")

    def test_migration_is_additive_only(self) -> None:
        compact_sql = re.sub(r"\s+", " ", self.sql.lower())
        for forbidden in ("drop table", "drop schema", "truncate", "delete from"):
            self.assertNotIn(forbidden, compact_sql, f"004 should not contain: {forbidden}")

    def test_migration_does_not_touch_schema_version(self) -> None:
        self.assertNotIn(
            "cdp_core.schema_version",
            self.executable_sql,
            "schema_version is owned exclusively by docker/postgres/init/01-init-cdp.sql; "
            "001 and 003 do not touch it, so 004 should not either",
        )

    def test_migration_registers_decision_class_with_conflict_handling(self) -> None:
        required_snippets = [
            "INSERT INTO cdp_core.decision_class_registry",
            "ON CONFLICT (registry_name, class_id)",
            "DO UPDATE SET",
            "'sample_attorney_demo'",
            "'claim'",
            "'claim_approval'",
        ]
        for snippet in required_snippets:
            self.assertIn(snippet, self.sql)

    def test_migration_configures_nemawashi_default_workflow_applicability(self) -> None:
        required_snippets = [
            "UPDATE cdp_core.workflow_definition",
            "applies_to_registry_name = 'sample_attorney_demo'",
            "applies_to_decision_class_id = 'claim_approval'",
            "WHERE workflow_code = 'nemawashi_default_v1'",
            "AND workflow_version = 'v1'",
        ]
        for snippet in required_snippets:
            self.assertIn(snippet, self.sql)

    def test_migration_does_not_touch_restricted_data_access_workflow(self) -> None:
        self.assertNotIn("restricted_data_access_v1", self.executable_sql)


class Migration004PostgresSmokeTests(unittest.TestCase):
    """Optional Postgres execution smoke test.

    Set CDP_TEST_DATABASE_URL to enable. Applies 001, then 003, then 004
    twice inside one transaction (rolled back at the end) to prove
    rerun-safety without touching persistent local data.
    """

    def test_apply_001_then_003_then_004_twice_is_idempotent(self) -> None:
        database_url = os.environ.get("CDP_TEST_DATABASE_URL")
        if not database_url:
            self.skipTest("set CDP_TEST_DATABASE_URL to run Postgres DDL smoke test")

        conn = self._connect(database_url)
        try:
            cursor = conn.cursor()
            cursor.execute(read_sql(DDL_001))
            cursor.execute(read_sql(DDL_003))
            cursor.execute(read_sql(DDL_004))
            # Rerun 004 alone to prove idempotency/rerun-safety.
            cursor.execute(read_sql(DDL_004))

            cursor.execute(
                """
                SELECT class_id, parent_class_id, class_label, class_level
                FROM cdp_core.decision_class_registry
                WHERE registry_name = 'sample_attorney_demo'
                ORDER BY class_level
                """
            )
            rows = {row[0]: row for row in cursor.fetchall()}
            self.assertIn("claim", rows)
            self.assertIn("claim_approval", rows)
            self.assertIsNone(rows["claim"][1])
            self.assertEqual(rows["claim_approval"][1], "claim")

            cursor.execute(
                """
                SELECT applies_to_registry_name, applies_to_decision_class_id, status
                FROM cdp_core.workflow_definition
                WHERE workflow_code = 'nemawashi_default_v1'
                  AND workflow_version = 'v1'
                """
            )
            applies_to_registry_name, applies_to_decision_class_id, status = cursor.fetchone()
            self.assertEqual(applies_to_registry_name, "sample_attorney_demo")
            self.assertEqual(applies_to_decision_class_id, "claim_approval")
            self.assertEqual(status, "active")

            # Unrelated configured workflow_definition row must be untouched.
            cursor.execute(
                """
                SELECT applies_to_registry_name, applies_to_decision_class_id
                FROM cdp_core.workflow_definition
                WHERE workflow_code = 'restricted_data_access_v1'
                  AND workflow_version = 'v1'
                """
            )
            restricted_row = cursor.fetchone()
            self.assertIsNone(restricted_row[0])
            self.assertIsNone(restricted_row[1])
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
