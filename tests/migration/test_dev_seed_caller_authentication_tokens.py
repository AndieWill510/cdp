"""Smoke tests for db/seed/dev-caller-authentication-tokens.sql.

This file is deliberately NOT part of the canonical db/ddl/ migration
path -- see its own header and db/ddl/014-caller-authentication.sql's
"No privileged tokens are seeded here" note (both added correcting an
earlier version of PR #48 that seeded these same tokens directly inside
014, which meant any deployment applying the normal migrations was born
with known, active, privileged credentials).

Two layers, following the pattern established for db/ddl/ migrations
elsewhere in this repo:

1. a static smoke test that inspects the file's text with no database
   dependency;
2. an optional Postgres integration smoke test, enabled only when
   CDP_TEST_DATABASE_URL is set, that proves applying 001-014 then this
   seed file actually activates the two bounded system actors' tokens,
   and that reapplying it is a no-op (idempotent, rerun-safe).
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
DEV_SEED_FILE = REPO_ROOT / "db" / "seed" / "dev-caller-authentication-tokens.sql"

RECOGNITION_AUTHORITY_SEED_TOKEN = (
    "seed-token-recognition-authority-local-dev-only-do-not-use-in-production"
)
GRANT_ISSUER_SEED_TOKEN = "seed-token-grant-issuer-local-dev-only-do-not-use-in-production"


def read_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_sql_comments(sql: str) -> str:
    return re.sub(r"--[^\n]*", "", sql)


class DevSeedCallerAuthenticationTokensStaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sql = read_sql(DEV_SEED_FILE)
        cls.executable_sql = strip_sql_comments(cls.sql)

    def test_file_exists_outside_the_canonical_migration_path(self) -> None:
        self.assertTrue(DEV_SEED_FILE.exists())
        self.assertNotEqual(
            DEV_SEED_FILE.parent.name,
            "ddl",
            "dev-only seed data must not live under db/ddl/, the canonical migration path",
        )

    def test_file_warns_unmistakably_against_deployment_use(self) -> None:
        upper_sql = self.sql.upper()
        self.assertIn("DO NOT APPLY THIS FILE TO ANY DEPLOYMENT THAT MATTERS", upper_sql)

    def test_seeded_tokens_match_the_published_plaintext(self) -> None:
        """Proves the hash actually stored in this file matches
        sha256(the exact plaintext this file's own header publishes) --
        catching any transcription drift between the header comment and
        the real INSERT value."""
        recognition_hash = hashlib.sha256(
            RECOGNITION_AUTHORITY_SEED_TOKEN.encode("utf-8")
        ).hexdigest()
        grant_issuer_hash = hashlib.sha256(GRANT_ISSUER_SEED_TOKEN.encode("utf-8")).hexdigest()
        self.assertIn(recognition_hash, self.sql)
        self.assertIn(grant_issuer_hash, self.sql)

    def test_only_inserts_into_actor_bearer_token(self) -> None:
        compact_sql = re.sub(r"\s+", " ", self.executable_sql.lower())
        for forbidden in ("drop table", "drop schema", "truncate", "delete from", "update "):
            self.assertNotIn(forbidden, compact_sql, f"dev seed file should not contain: {forbidden}")
        self.assertIn("INSERT INTO cdp_core.actor_bearer_token", self.executable_sql)


class DevSeedCallerAuthenticationTokensPostgresSmokeTests(unittest.TestCase):
    """Optional Postgres execution smoke test.

    Set CDP_TEST_DATABASE_URL to enable. Applies 001 through 014, then
    this dev-seed file twice inside one transaction (rolled back at the
    end) to prove it actually activates the two bounded system actors'
    tokens and that reapplying it is idempotent.
    """

    def test_apply_after_014_then_reapply_is_idempotent(self) -> None:
        database_url = os.environ.get("CDP_TEST_DATABASE_URL")
        if not database_url:
            self.skipTest("set CDP_TEST_DATABASE_URL to run Postgres DDL smoke test")

        conn = self._connect(database_url)
        try:
            cursor = conn.cursor()
            for filename in DDL_FILES:
                cursor.execute(read_sql(REPO_ROOT / "db" / "ddl" / filename))
            cursor.execute(read_sql(DEV_SEED_FILE))
            # Reapply to prove idempotency/rerun-safety.
            cursor.execute(read_sql(DEV_SEED_FILE))

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
