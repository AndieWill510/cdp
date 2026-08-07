"""Smoke tests for the 015 Standing and Recusal migration.

Two layers, following the pattern established in
test_migration_014_caller_authentication.py:

1. static smoke tests that inspect the DDL text with no database dependency;
2. an optional Postgres integration smoke test, enabled only when
   CDP_TEST_DATABASE_URL is set, that proves 001 -> ... -> 014 -> 015 apply
   cleanly and that re-running 015 is a no-op (idempotent, rerun-safe).

Like 014, this migration seeds no privileged token for its bounded actor
(cdp_standing_recognition_authority) -- see this file's
test_migration_does_not_seed_any_tokens and
db/seed/dev-caller-authentication-tokens.sql for local/dev/test
bootstrapping instead.
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
    "015-standing-and-recusal.sql",
]
DDL_015 = REPO_ROOT / "db" / "ddl" / "015-standing-and-recusal.sql"


def read_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_sql_comments(sql: str) -> str:
    return re.sub(r"--[^\n]*", "", sql)


class Migration015StaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sql = read_sql(DDL_015)
        cls.executable_sql = strip_sql_comments(cls.sql)

    def test_migration_file_exists(self) -> None:
        self.assertTrue(DDL_015.exists(), "015 standing-and-recusal DDL should exist")

    def test_migration_creates_standing_claim_table(self) -> None:
        self.assertIn("CREATE TABLE IF NOT EXISTS cdp_core.standing_claim", self.executable_sql)

    def test_migration_creates_standing_recognition_determination_table(self) -> None:
        self.assertIn(
            "CREATE TABLE IF NOT EXISTS cdp_core.standing_recognition_determination",
            self.executable_sql,
        )

    def test_migration_does_not_drop_or_truncate_anything(self) -> None:
        compact_sql = re.sub(r"\s+", " ", self.executable_sql.lower())
        for forbidden in ("drop table", "drop schema", "truncate", "delete from", "drop column"):
            self.assertNotIn(forbidden, compact_sql, f"015 should not contain: {forbidden}")

    def test_migration_forbids_claim_deletion_and_update_at_the_database_level(self) -> None:
        self.assertIn("forbid_standing_claim_delete", self.sql)
        self.assertIn("forbid_standing_claim_update", self.sql)
        self.assertIn("BEFORE DELETE ON cdp_core.standing_claim", self.executable_sql)
        self.assertIn("BEFORE UPDATE ON cdp_core.standing_claim", self.executable_sql)

    def test_migration_forbids_determination_deletion_and_update_at_the_database_level(
        self,
    ) -> None:
        self.assertIn("forbid_standing_determination_delete", self.sql)
        self.assertIn("forbid_standing_determination_update", self.sql)
        self.assertIn(
            "BEFORE DELETE ON cdp_core.standing_recognition_determination", self.executable_sql
        )
        self.assertIn(
            "BEFORE UPDATE ON cdp_core.standing_recognition_determination", self.executable_sql
        )

    def test_migration_enforces_minimal_sufficiency_at_the_database_level(self) -> None:
        self.assertIn("chk_standing_claim_impact_not_blank", self.sql)
        self.assertIn("chk_standing_claim_basis_minimally_sufficient", self.sql)

    def test_migration_enforces_one_determination_per_claim(self) -> None:
        self.assertIn("uq_standing_determination_claim", self.sql)
        self.assertIn("UNIQUE (claim_id)", self.executable_sql)

    def test_migration_restricts_outcome_to_the_two_outcomes_this_slice_writes(self) -> None:
        self.assertIn(
            "CHECK (outcome IN ('recognized', 'denied'))",
            self.executable_sql,
        )

    def test_migration_seeds_but_does_not_permit_narrowed(self) -> None:
        """'narrowed' remains in the standing_recognition_outcome
        vocabulary (for a future session that adds outcome_scope) but
        must not appear in the determination table's own CHECK constraint
        -- see the DDL header's review-finding note (PR #53)."""
        self.assertIn(
            "'standing_recognition_outcome', 'narrowed'", self.executable_sql
        )
        self.assertNotIn("'recognized', 'narrowed'", self.executable_sql)

    def test_migration_does_not_seed_any_tokens(self) -> None:
        """The canonical migration path must never insert a row into
        actor_bearer_token -- same discipline as 014, see that file's
        header (PR #48 review correction)."""
        self.assertNotIn("INSERT INTO cdp_core.actor_bearer_token", self.executable_sql)

    def test_migration_seeds_exactly_one_new_bounded_actor(self) -> None:
        self.assertIn("cdp_standing_recognition_authority", self.sql)
        self.assertNotIn("cdp_identity_recognition_authority", self.executable_sql)
        self.assertNotIn("cdp_authority_grant_issuer", self.executable_sql)

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

    def test_no_secret_bearing_columns_in_migration(self) -> None:
        column_def_pattern = re.compile(
            r"\b(password|passwd|private_key|secret_key)\s+(TEXT|VARCHAR|BYTEA|CHAR)\b",
            re.IGNORECASE,
        )
        self.assertIsNone(
            column_def_pattern.search(self.executable_sql),
            "015 should not define a secret-bearing column",
        )


class Migration015PostgresSmokeTests(unittest.TestCase):
    """Optional Postgres execution smoke test.

    Set CDP_TEST_DATABASE_URL to enable. Applies 001 through 014, then 015
    twice inside one transaction (rolled back at the end) to prove
    rerun-safety without touching persistent local data.
    """

    def test_apply_001_through_014_then_015_twice_is_idempotent(self) -> None:
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
                "WHERE table_schema = 'cdp_core' AND table_name = 'standing_claim' "
                "AND column_name = 'claimed_impact'"
            )
            self.assertIsNotNone(cursor.fetchone(), "missing standing_claim.claimed_impact")

            cursor.execute(
                "SELECT actor_id, actor_status FROM cdp_core.actor "
                "WHERE actor_id = 'cdp_standing_recognition_authority'"
            )
            row = cursor.fetchone()
            self.assertIsNotNone(row, "cdp_standing_recognition_authority actor row missing")
            self.assertEqual(row[1], "active")

            cursor.execute(read_sql(DDL_015))
            cursor.execute(
                "SELECT count(*) FROM cdp_core.actor "
                "WHERE actor_id = 'cdp_standing_recognition_authority'"
            )
            self.assertEqual(
                cursor.fetchone()[0], 1, "rerunning 015 must not duplicate the bounded actor"
            )

            # Minimal sufficiency is enforced -- a claim with no basis field
            # set at all must be rejected.
            with self.assertRaises(Exception):
                nested = conn.cursor()
                nested.execute(
                    "INSERT INTO cdp_core.standing_claim "
                    "(decision_registry_name, decision_id, actor_id, claimed_impact) "
                    "VALUES ('mig015-smoke-registry', 'mig015-smoke-decision', "
                    "'cdp_standing_recognition_authority', 'some impact')"
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
