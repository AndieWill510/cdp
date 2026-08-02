"""Smoke tests for the 013 identity-claim-scope migration.

Two layers, following the pattern established in
test_migration_012_universal_attestation.py:

1. static smoke tests that inspect the DDL text with no database dependency;
2. an optional Postgres integration smoke test, enabled only when
   CDP_TEST_DATABASE_URL is set, that proves 001 -> ... -> 012 -> 013 apply
   cleanly and that re-running 013 is a no-op (idempotent, rerun-safe).
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
    "013-identity-claim-scope.sql",
]
DDL_013 = REPO_ROOT / "db" / "ddl" / "013-identity-claim-scope.sql"


def read_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_sql_comments(sql: str) -> str:
    """Drop `-- ...` line comments so text assertions ignore prose in comments."""
    return re.sub(r"--[^\n]*", "", sql)


class Migration013StaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sql = read_sql(DDL_013)
        cls.executable_sql = strip_sql_comments(cls.sql)

    def test_migration_file_exists(self) -> None:
        self.assertTrue(DDL_013.exists(), "013 identity-claim-scope DDL should exist")

    def test_migration_is_additive_only(self) -> None:
        compact_sql = re.sub(r"\s+", " ", self.executable_sql.lower())
        for forbidden in ("drop table", "drop schema", "truncate", "delete from", "drop column"):
            self.assertNotIn(forbidden, compact_sql, f"013 should not contain: {forbidden}")

    def test_migration_only_alters_identity_claim_additively(self) -> None:
        self.assertIn(
            "ALTER TABLE cdp_core.identity_claim\n    ADD COLUMN IF NOT EXISTS scope_registry_name",
            self.executable_sql,
        )
        self.assertIn(
            "ALTER TABLE cdp_core.identity_claim\n    ADD COLUMN IF NOT EXISTS scope_decision_class_id",
            self.executable_sql,
        )

    def test_migration_adds_constraint_idempotently(self) -> None:
        self.assertIn("chk_identity_claim_scope_decision_class_requires_registry", self.sql)
        self.assertIn("IF NOT EXISTS", self.sql)
        self.assertIn("pg_constraint", self.sql)

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

    def test_no_secret_bearing_columns_anywhere_in_migration(self) -> None:
        column_def_pattern = re.compile(
            r"\b(password|passwd|private_key|secret_key)\s+(TEXT|VARCHAR|BYTEA|CHAR)\b",
            re.IGNORECASE,
        )
        self.assertIsNone(
            column_def_pattern.search(self.executable_sql),
            "013 should not define a secret-bearing column",
        )


class Migration013PostgresSmokeTests(unittest.TestCase):
    """Optional Postgres execution smoke test.

    Set CDP_TEST_DATABASE_URL to enable. Applies 001 through 012, then 013
    twice inside one transaction (rolled back at the end) to prove
    rerun-safety without touching persistent local data.
    """

    def test_apply_001_through_012_then_013_twice_is_idempotent(self) -> None:
        database_url = os.environ.get("CDP_TEST_DATABASE_URL")
        if not database_url:
            self.skipTest("set CDP_TEST_DATABASE_URL to run Postgres DDL smoke test")

        conn = self._connect(database_url)
        try:
            cursor = conn.cursor()
            for filename in DDL_FILES:
                cursor.execute(read_sql(REPO_ROOT / "db" / "ddl" / filename))
            # Rerun 013 alone to prove idempotency/rerun-safety.
            cursor.execute(read_sql(DDL_013))

            cursor.execute(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_schema = 'cdp_core' AND table_name = 'identity_claim' "
                "AND column_name = 'scope_registry_name'"
            )
            self.assertIsNotNone(cursor.fetchone(), "missing identity_claim.scope_registry_name")

            cursor.execute(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_schema = 'cdp_core' AND table_name = 'identity_claim' "
                "AND column_name = 'scope_decision_class_id'"
            )
            self.assertIsNotNone(
                cursor.fetchone(), "missing identity_claim.scope_decision_class_id"
            )

            cursor.execute(
                "SELECT count(*) FROM pg_constraint "
                "WHERE conname = 'chk_identity_claim_scope_decision_class_requires_registry'"
            )
            self.assertEqual(
                cursor.fetchone()[0],
                1,
                "expected exactly one copy of the CHECK constraint after rerun",
            )

            # The CHECK constraint fires immediately on INSERT, before any
            # deferred FK check -- a decision-class scope without a
            # registry scope must be rejected regardless of whether the
            # referenced actor rows exist.
            with self.assertRaises(Exception):
                nested = conn.cursor()
                nested.execute(
                    """
                    INSERT INTO cdp_core.identity_claim (
                        actor_id, claimant_actor_id, claimed_identity_descriptor,
                        purpose_scope, scope_decision_class_id
                    )
                    VALUES (
                        'mig013-smoke-actor', 'mig013-smoke-actor', 'smoke descriptor',
                        'smoke_purpose', 'some_class_without_registry'
                    )
                    """
                )
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
