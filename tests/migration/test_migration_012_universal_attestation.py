"""Smoke tests for the 012 universal-attestation migration.

Two layers, following the pattern established in
test_migration_011_authority_and_delegation.py:

1. static smoke tests that inspect the DDL text with no database dependency;
2. an optional Postgres integration smoke test, enabled only when
   CDP_TEST_DATABASE_URL is set, that proves 001 -> ... -> 011 -> 012 apply
   cleanly and that re-running 012 is a no-op (idempotent, rerun-safe).
"""

from __future__ import annotations

import os
import re
import unittest
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DDL_FILES = [
    "001-decision-registry-kernel.sql",
    "003-nemawashi-workflow-rules.sql",
    "004-decision-class-workflow-seed.sql",
    "005-challenge-transition.sql",
    "006-audit-event-ordering.sql",
    "007-challenge-adjudication.sql",
    "008-execution-authorization.sql",
    "009-execution-record.sql",
    "010-identity-and-attestation.sql",
    "011-authority-and-delegation.sql",
    "012-universal-attestation.sql",
]
DDL_012 = REPO_ROOT / "db" / "ddl" / "012-universal-attestation.sql"


def read_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_sql_comments(sql: str) -> str:
    """Drop `-- ...` line comments so text assertions ignore prose in comments."""
    return re.sub(r"--[^\n]*", "", sql)


class Migration012StaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sql = read_sql(DDL_012)
        cls.executable_sql = strip_sql_comments(cls.sql)

    def test_migration_file_exists(self) -> None:
        self.assertTrue(DDL_012.exists(), "012 universal-attestation DDL should exist")

    def test_migration_is_additive_only(self) -> None:
        compact_sql = re.sub(r"\s+", " ", self.executable_sql.lower())
        for forbidden in ("drop table", "drop schema", "truncate", "delete from", "drop column"):
            self.assertNotIn(forbidden, compact_sql, f"012 should not contain: {forbidden}")

    def test_migration_only_alters_existing_tables_additively(self) -> None:
        self.assertIn(
            "ALTER TABLE cdp_core.attestation_record\n    ADD COLUMN IF NOT EXISTS governed_act_ref_id",
            self.executable_sql,
        )
        self.assertIn(
            "ALTER TABLE cdp_core.authority_evaluation_result\n    ADD COLUMN IF NOT EXISTS governed_act_ref_id",
            self.executable_sql,
        )

    def test_migration_does_not_touch_schema_version(self) -> None:
        self.assertNotIn("cdp_core.schema_version", self.executable_sql)

    def test_migration_does_not_write_out_of_scope_governance_tables(self) -> None:
        forbidden_statements = [
            "UPDATE cdp_core.decision_registry",
            "UPDATE cdp_core.workflow_instance",
            "UPDATE cdp_core.identity_claim",
            "UPDATE cdp_core.actor",
            "UPDATE cdp_core.authority_grant",
            "CREATE TABLE",
        ]
        for statement in forbidden_statements:
            self.assertNotIn(statement, self.executable_sql)

    def test_migration_registers_four_new_governed_act_types(self) -> None:
        required_snippets = [
            "('governed_act_type', 'challenge_raised'",
            "('governed_act_type', 'challenge_adjudicated'",
            "('governed_act_type', 'execution_authorized'",
            "('governed_act_type', 'execution_recorded'",
        ]
        for snippet in required_snippets:
            self.assertIn(snippet, self.sql)

    def test_no_secret_bearing_columns_anywhere_in_migration(self) -> None:
        column_def_pattern = re.compile(
            r"\b(password|passwd|private_key|secret_key)\s+(TEXT|VARCHAR|BYTEA|CHAR)\b",
            re.IGNORECASE,
        )
        self.assertIsNone(
            column_def_pattern.search(self.executable_sql),
            "012 should not define a secret-bearing column",
        )


class Migration012PostgresSmokeTests(unittest.TestCase):
    """Optional Postgres execution smoke test.

    Set CDP_TEST_DATABASE_URL to enable. Applies 001 through 011, then 012
    twice inside one transaction (rolled back at the end) to prove
    rerun-safety without touching persistent local data.
    """

    def test_apply_001_through_011_then_012_twice_is_idempotent(self) -> None:
        database_url = os.environ.get("CDP_TEST_DATABASE_URL")
        if not database_url:
            self.skipTest("set CDP_TEST_DATABASE_URL to run Postgres DDL smoke test")

        conn = self._connect(database_url)
        try:
            cursor = conn.cursor()
            for filename in DDL_FILES:
                cursor.execute(read_sql(REPO_ROOT / "db" / "ddl" / filename))
            # Rerun 012 alone to prove idempotency/rerun-safety.
            cursor.execute(read_sql(DDL_012))

            cursor.execute(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_schema = 'cdp_core' AND table_name = 'attestation_record' "
                "AND column_name = 'governed_act_ref_id'"
            )
            self.assertIsNotNone(
                cursor.fetchone(), "missing attestation_record.governed_act_ref_id"
            )

            cursor.execute(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_schema = 'cdp_core' AND table_name = 'authority_evaluation_result' "
                "AND column_name = 'governed_act_ref_id'"
            )
            self.assertIsNotNone(
                cursor.fetchone(), "missing authority_evaluation_result.governed_act_ref_id"
            )

            cursor.execute(
                "SELECT count(*) FROM cdp_core.identifier_registry "
                "WHERE registry_name = 'governed_act_type'"
            )
            self.assertEqual(cursor.fetchone()[0], 5)  # decision_created + 4 new values

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
            raise unittest.SkipTest(
                "install psycopg or psycopg2 to run Postgres DDL smoke test"
            ) from exc


if __name__ == "__main__":
    unittest.main()
