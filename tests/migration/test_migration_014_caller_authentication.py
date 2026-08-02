"""Smoke tests for the 014 caller-authentication migration.

Two layers, following the pattern established in
test_migration_013_identity_claim_scope.py:

1. static smoke tests that inspect the DDL text with no database dependency;
2. an optional Postgres integration smoke test, enabled only when
   CDP_TEST_DATABASE_URL is set, that proves 001 -> ... -> 013 -> 014
   apply cleanly and that re-running 014 is a no-op (idempotent,
   rerun-safe).
"""

from __future__ import annotations

import hashlib
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
    "014-caller-authentication.sql",
]
DDL_014 = REPO_ROOT / "db" / "ddl" / "014-caller-authentication.sql"

RECOGNITION_AUTHORITY_SEED_TOKEN = (
    "seed-token-recognition-authority-local-dev-only-do-not-use-in-production"
)
GRANT_ISSUER_SEED_TOKEN = "seed-token-grant-issuer-local-dev-only-do-not-use-in-production"


def read_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_sql_comments(sql: str) -> str:
    """Drop `-- ...` line comments so text assertions ignore prose in comments."""
    return re.sub(r"--[^\n]*", "", sql)


class Migration014StaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sql = read_sql(DDL_014)
        cls.executable_sql = strip_sql_comments(cls.sql)

    def test_migration_file_exists(self) -> None:
        self.assertTrue(DDL_014.exists(), "014 caller-authentication DDL should exist")

    def test_migration_creates_actor_bearer_token_table(self) -> None:
        self.assertIn(
            "CREATE TABLE IF NOT EXISTS cdp_core.actor_bearer_token", self.executable_sql
        )

    def test_migration_does_not_drop_or_truncate_anything(self) -> None:
        compact_sql = re.sub(r"\s+", " ", self.executable_sql.lower())
        for forbidden in ("drop table", "drop schema", "truncate", "delete from", "drop column"):
            self.assertNotIn(forbidden, compact_sql, f"014 should not contain: {forbidden}")

    def test_migration_forbids_token_deletion_at_the_database_level(self) -> None:
        self.assertIn("forbid_actor_bearer_token_delete", self.sql)
        self.assertIn("BEFORE DELETE ON cdp_core.actor_bearer_token", self.executable_sql)
        self.assertIn("RAISE EXCEPTION", self.sql)

    def test_migration_only_stores_a_hash_never_a_plaintext_column(self) -> None:
        self.assertIn("token_hash", self.sql)
        self.assertNotRegex(self.sql.lower(), r"\btoken_plaintext\b")
        self.assertNotRegex(self.sql.lower(), r"\bplaintext_token\b")

    def test_migration_does_not_touch_schema_version(self) -> None:
        self.assertNotIn("cdp_core.schema_version", self.executable_sql)

    def test_migration_does_not_write_out_of_scope_governance_tables(self) -> None:
        forbidden_statements = [
            "UPDATE cdp_core.decision_registry",
            "UPDATE cdp_core.workflow_instance",
            "UPDATE cdp_core.identity_claim",
            "UPDATE cdp_core.actor",
            "UPDATE cdp_core.authority_grant",
        ]
        for statement in forbidden_statements:
            self.assertNotIn(statement, self.executable_sql)

    def test_seeded_tokens_match_the_published_plaintext(self) -> None:
        """The migration's file header publishes two plaintext seed tokens
        (local/dev/test use only). This test proves the hash actually
        stored in the migration matches sha256(that exact plaintext) --
        catching any transcription drift between the header comment and
        the real INSERT value."""
        recognition_hash = hashlib.sha256(
            RECOGNITION_AUTHORITY_SEED_TOKEN.encode("utf-8")
        ).hexdigest()
        grant_issuer_hash = hashlib.sha256(GRANT_ISSUER_SEED_TOKEN.encode("utf-8")).hexdigest()
        self.assertIn(recognition_hash, self.sql)
        self.assertIn(grant_issuer_hash, self.sql)

    def test_no_other_secret_bearing_columns_in_migration(self) -> None:
        column_def_pattern = re.compile(
            r"\b(password|passwd|private_key|secret_key)\s+(TEXT|VARCHAR|BYTEA|CHAR)\b",
            re.IGNORECASE,
        )
        self.assertIsNone(
            column_def_pattern.search(self.executable_sql),
            "014 should not define a secret-bearing column",
        )


class Migration014PostgresSmokeTests(unittest.TestCase):
    """Optional Postgres execution smoke test.

    Set CDP_TEST_DATABASE_URL to enable. Applies 001 through 013, then 014
    twice inside one transaction (rolled back at the end) to prove
    rerun-safety without touching persistent local data.
    """

    def test_apply_001_through_013_then_014_twice_is_idempotent(self) -> None:
        database_url = os.environ.get("CDP_TEST_DATABASE_URL")
        if not database_url:
            self.skipTest("set CDP_TEST_DATABASE_URL to run Postgres DDL smoke test")

        conn = self._connect(database_url)
        try:
            cursor = conn.cursor()
            for filename in DDL_FILES:
                cursor.execute(read_sql(REPO_ROOT / "db" / "ddl" / filename))
            # Rerun 014 alone to prove idempotency/rerun-safety.
            cursor.execute(read_sql(DDL_014))

            cursor.execute(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_schema = 'cdp_core' AND table_name = 'actor_bearer_token' "
                "AND column_name = 'token_hash'"
            )
            self.assertIsNotNone(cursor.fetchone(), "missing actor_bearer_token.token_hash")

            # Exactly one seeded, active token each for the two bounded
            # system actors -- rerunning 014 must not duplicate them
            # (ON CONFLICT (token_hash) DO NOTHING).
            cursor.execute(
                "SELECT actor_id, status FROM cdp_core.actor_bearer_token "
                "WHERE actor_id IN ('cdp_identity_recognition_authority', 'cdp_authority_grant_issuer') "
                "ORDER BY actor_id"
            )
            rows = cursor.fetchall()
            self.assertEqual(
                rows,
                [
                    ("cdp_authority_grant_issuer", "active"),
                    ("cdp_identity_recognition_authority", "active"),
                ],
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

            # The partial unique index actually enforces one active token
            # per actor -- inserting a second active row for an actor that
            # already has one must fail. Run last: this aborts the
            # transaction, so nothing after it can execute on this
            # connection.
            with self.assertRaises(Exception):
                nested = conn.cursor()
                nested.execute(
                    "INSERT INTO cdp_core.actor_bearer_token (actor_id, token_hash) "
                    "VALUES ('cdp_authority_grant_issuer', 'mig014-smoke-duplicate-hash')"
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
