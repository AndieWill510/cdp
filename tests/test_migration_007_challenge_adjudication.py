"""Smoke tests for the 007 challenge-adjudication migration.

Two layers, following the pattern established in
test_migration_005_challenge_transition.py:

1. static smoke tests that inspect the DDL text with no database dependency;
2. an optional Postgres integration smoke test, enabled only when
   CDP_TEST_DATABASE_URL is set, that proves 001 -> 003 -> 004 -> 005 -> 006
   -> 007 apply cleanly and that re-running 007 is a no-op (idempotent,
   rerun-safe).

Note on numbering: this migration was originally drafted as 006, but
006-audit-event-ordering.sql (a foundational fix to cdp_audit.event_log
discovered while manually verifying this slice) needed to land first, so
this migration was renumbered to 007.
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


def read_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_sql_comments(sql: str) -> str:
    """Drop `-- ...` line comments so text assertions ignore prose in comments."""
    return re.sub(r"--[^\n]*", "", sql)


class Migration007StaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sql = read_sql(DDL_007)
        cls.executable_sql = strip_sql_comments(cls.sql)

    def test_migration_file_exists(self) -> None:
        self.assertTrue(DDL_007.exists(), "007 challenge-adjudication DDL should exist")

    def test_migration_is_additive_only(self) -> None:
        compact_sql = re.sub(r"\s+", " ", self.executable_sql.lower())
        for forbidden in ("drop table", "drop schema", "truncate", "delete from"):
            self.assertNotIn(forbidden, compact_sql, f"007 should not contain: {forbidden}")

    def test_migration_uses_create_if_not_exists_for_new_table(self) -> None:
        self.assertIn(
            "CREATE TABLE IF NOT EXISTS cdp_core.challenge_adjudication_record",
            self.executable_sql,
        )

    def test_migration_does_not_touch_schema_version(self) -> None:
        self.assertNotIn("cdp_core.schema_version", self.executable_sql)

    def test_migration_does_not_modify_any_workflow_definition_or_challenge_record_rows(
        self,
    ) -> None:
        """007 should not UPDATE workflow_definition or challenge_record -- it
        only adds a new table and new controlled vocabulary. The service
        layer, not this migration, updates challenge_record."""
        self.assertNotIn("UPDATE cdp_core.workflow_definition", self.executable_sql)
        self.assertNotIn("UPDATE cdp_core.challenge_record", self.executable_sql)

    def test_migration_registers_adjudication_outcome_vocabulary(self) -> None:
        required_snippets = [
            "'challenge_adjudication_outcome'",
            "('challenge_adjudication_outcome', 'sustained'",
            "('challenge_adjudication_outcome', 'not_sustained'",
            "('challenge_adjudication_outcome', 'deferred'",
            "('challenge_adjudication_outcome', 'referred_to_repair'",
        ]
        for snippet in required_snippets:
            self.assertIn(snippet, self.sql)

    def test_challenge_adjudication_record_references_challenge_decision_actor_task(
        self,
    ) -> None:
        required_snippets = [
            "REFERENCES cdp_core.challenge_record (challenge_id)",
            "REFERENCES cdp_core.decision_registry (registry_name, decision_id)",
            "REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)",
            "REFERENCES cdp_core.workflow_task (task_id)",
        ]
        for snippet in required_snippets:
            self.assertIn(snippet, self.sql)

    def test_challenge_adjudication_record_is_not_a_status_flip(self) -> None:
        """Confirm the adjudication artifact preserves who/what/why/when,
        not just a challenge_status flag flip."""
        required_snippets = [
            "adjudication_id UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "adjudicated_by_actor_id TEXT NOT NULL",
            "outcome TEXT NOT NULL",
            "rationale TEXT NOT NULL",
            "resulting_challenge_status TEXT NOT NULL",
            "created_at TIMESTAMPTZ NOT NULL DEFAULT now()",
        ]
        for snippet in required_snippets:
            self.assertIn(snippet, self.sql)

    def test_outcome_to_status_mapping_is_enforced_by_check_constraint(self) -> None:
        self.assertIn("chk_challenge_adjudication_outcome_status_mapping", self.sql)


class Migration007PostgresSmokeTests(unittest.TestCase):
    """Optional Postgres execution smoke test.

    Set CDP_TEST_DATABASE_URL to enable. Applies 001, 003, 004, 005, 006,
    then 007 twice inside one transaction (rolled back at the end) to prove
    rerun-safety without touching persistent local data.
    """

    def test_apply_001_003_004_005_006_then_007_twice_is_idempotent(self) -> None:
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
            # Rerun 007 alone to prove idempotency/rerun-safety.
            cursor.execute(read_sql(DDL_007))

            cursor.execute("SELECT to_regclass('cdp_core.challenge_adjudication_record')")
            self.assertIsNotNone(
                cursor.fetchone()[0], "missing cdp_core.challenge_adjudication_record"
            )

            cursor.execute(
                """
                SELECT count(*) FROM cdp_core.identifier_registry
                WHERE registry_name = 'challenge_adjudication_outcome'
                """
            )
            self.assertEqual(cursor.fetchone()[0], 4)

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
