"""Smoke tests for the 014 caller-authentication migration.

Two layers, following the pattern established in
test_migration_013_identity_claim_scope.py:

1. static smoke tests that inspect the DDL text with no database dependency;
2. an optional Postgres integration smoke test, enabled only when
   CDP_TEST_DATABASE_URL is set, that proves 001 -> ... -> 013 -> 014
   apply cleanly and that re-running 014 is a no-op (idempotent,
   rerun-safe).

Review correction (before merging PR #48): this migration no longer
seeds any tokens itself -- see 014's file header ("No privileged tokens
are seeded here") and db/seed/dev-caller-authentication-tokens.sql,
which is not part of this migration and is covered by
test_dev_seed_caller_authentication_tokens.py instead. The definitive
proof that 014 seeds nothing is the static
test_migration_does_not_seed_any_tokens (SQL text inspection, database-
state-independent); the Postgres smoke test below only proves rerunning
014 changes nothing, since the shared test database it runs against may
already have db/seed/ applied by an earlier CI/local-init step intended
for other tests in the same run.
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
    "014-caller-authentication.sql",
]
DDL_014 = REPO_ROOT / "db" / "ddl" / "014-caller-authentication.sql"


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

    def test_migration_does_not_seed_any_tokens(self) -> None:
        """The canonical migration path must never insert a row into
        actor_bearer_token -- a deployment applying only db/ddl/*.sql
        must not be born with any bearer token, privileged or otherwise.
        See this file's header for the review correction that established
        this rule (PR #48)."""
        self.assertNotIn("INSERT INTO cdp_core.actor_bearer_token", self.executable_sql)

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

            cursor.execute(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_schema = 'cdp_core' AND table_name = 'actor_bearer_token' "
                "AND column_name = 'token_hash'"
            )
            self.assertIsNotNone(cursor.fetchone(), "missing actor_bearer_token.token_hash")

            # 014 itself must never change the token count for the two
            # bounded system actors -- whether this shared test database
            # already has db/seed/ applied (as CI's own "Seed dev/
            # test-only data" step and this repo's local Docker init both
            # do, for the benefit of *other* tests in the same run) or
            # not, rerunning 014 alone must be a pure no-op on this
            # table. This is the property the PR #48 review required --
            # proven here as "014 changes nothing," not "the count is
            # zero," since this test does not control whether it runs
            # against an otherwise-fresh database or one db/seed/ has
            # already touched. The static test
            # test_migration_does_not_seed_any_tokens proves the stronger
            # claim (014's own SQL text contains no INSERT into this
            # table at all) independent of database state.
            cursor.execute(
                "SELECT count(*) FROM cdp_core.actor_bearer_token "
                "WHERE actor_id IN ('cdp_identity_recognition_authority', 'cdp_authority_grant_issuer')"
            )
            count_before_rerun = cursor.fetchone()[0]

            cursor.execute(read_sql(DDL_014))

            cursor.execute(
                "SELECT count(*) FROM cdp_core.actor_bearer_token "
                "WHERE actor_id IN ('cdp_identity_recognition_authority', 'cdp_authority_grant_issuer')"
            )
            self.assertEqual(
                cursor.fetchone()[0],
                count_before_rerun,
                "rerunning 014 must not change the bounded actors' token count",
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
            # per actor. actor_bearer_token.actor_id's FK to
            # identifier_registry is DEFERRABLE INITIALLY DEFERRED and
            # this whole test rolls back without ever committing, so a
            # synthetic actor_id with no matching identifier_registry row
            # is fine here.
            cursor.execute(
                "INSERT INTO cdp_core.actor_bearer_token (actor_id, token_hash) "
                "VALUES ('mig014-smoke-actor', 'mig014-smoke-first-hash')"
            )
            with self.assertRaises(Exception):
                nested = conn.cursor()
                nested.execute(
                    "INSERT INTO cdp_core.actor_bearer_token (actor_id, token_hash) "
                    "VALUES ('mig014-smoke-actor', 'mig014-smoke-second-hash')"
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
