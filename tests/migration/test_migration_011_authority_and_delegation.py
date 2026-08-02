"""Smoke tests for the 011 authority-and-delegation migration.

Two layers, following the pattern established in
test_migration_010_identity_and_attestation.py:

1. static smoke tests that inspect the DDL text with no database dependency;
2. an optional Postgres integration smoke test, enabled only when
   CDP_TEST_DATABASE_URL is set, that proves 001 -> ... -> 010 -> 011 apply
   cleanly and that re-running 011 is a no-op (idempotent, rerun-safe).
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
DDL_009 = REPO_ROOT / "db" / "ddl" / "009-execution-record.sql"
DDL_010 = REPO_ROOT / "db" / "ddl" / "010-identity-and-attestation.sql"
DDL_011 = REPO_ROOT / "db" / "ddl" / "011-authority-and-delegation.sql"


def read_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_sql_comments(sql: str) -> str:
    """Drop `-- ...` line comments so text assertions ignore prose in comments."""
    return re.sub(r"--[^\n]*", "", sql)


class Migration011StaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sql = read_sql(DDL_011)
        cls.executable_sql = strip_sql_comments(cls.sql)

    def test_migration_file_exists(self) -> None:
        self.assertTrue(DDL_011.exists(), "011 authority-and-delegation DDL should exist")

    def test_migration_is_additive_only(self) -> None:
        compact_sql = re.sub(r"\s+", " ", self.executable_sql.lower())
        for forbidden in ("drop table", "drop schema", "truncate", "delete from"):
            self.assertNotIn(forbidden, compact_sql, f"011 should not contain: {forbidden}")

    def test_migration_uses_create_if_not_exists_for_new_tables(self) -> None:
        for table in ("cdp_core.authority_grant", "cdp_core.authority_evaluation_result"):
            self.assertIn(f"CREATE TABLE IF NOT EXISTS {table}", self.executable_sql)

    def test_migration_does_not_touch_schema_version(self) -> None:
        self.assertNotIn("cdp_core.schema_version", self.executable_sql)

    def test_migration_does_not_write_out_of_scope_governance_tables(self) -> None:
        """This slice must not implement Standing, Legitimize, or Repair,
        and must not write to decision_registry, workflow_instance,
        identity_claim, or attestation_record -- only read/reference them
        via FK."""
        forbidden_statements = [
            "UPDATE cdp_core.decision_registry",
            "UPDATE cdp_core.workflow_instance",
            "UPDATE cdp_core.identity_claim",
            "UPDATE cdp_core.attestation_record",
            "UPDATE cdp_core.actor",
            "CREATE TABLE IF NOT EXISTS cdp_core.standing",
            "CREATE TABLE IF NOT EXISTS cdp_core.legitimacy",
            "CREATE TABLE IF NOT EXISTS cdp_core.repair",
            "CREATE TABLE IF NOT EXISTS cdp_core.delegation",
        ]
        for statement in forbidden_statements:
            self.assertNotIn(statement, self.executable_sql)

    def test_migration_registers_all_controlled_vocabularies(self) -> None:
        required_snippets = [
            "'authority_type'",
            "('authority_type', 'PROPOSE'",
            "('authority_type', 'IDENTIFY'",
            "('authority_type', 'DELEGATE'",
            "'authority_grant_status'",
            "('authority_grant_status', 'active'",
            "('authority_grant_status', 'revoked'",
            "'authority_grant_basis'",
            "('authority_grant_basis', 'policy'",
            "'authority_evaluation_result'",
            "('authority_evaluation_result', 'pass'",
            "('authority_evaluation_result', 'fail'",
        ]
        for snippet in required_snippets:
            self.assertIn(snippet, self.sql)

    def test_authority_type_registers_the_full_rfc_032_vocabulary(self) -> None:
        """All 23 RFC-CDP-032 SS5 authority types must be seeded, even
        though only PROPOSE is evaluated by this slice -- see the DDL
        header."""
        required_types = [
            "IDENTIFY", "ATTEST", "ALIGN", "PROPOSE", "CHALLENGE", "TEST",
            "ADJUDICATE", "LEGITIMIZE", "REQUEST_EXECUTION", "AUTHORIZE_EXECUTION",
            "EXECUTE", "PAUSE_EXECUTION", "ROLLBACK", "OVERRIDE", "RECORD", "LEARN",
            "COVENANT_PARTICIPATE", "AIITL_CHALLENGE", "REPAIR_CLAIM", "REPAIR_REVIEW",
            "REPAIR_COMMIT", "REVOKE", "DELEGATE",
        ]
        for authority_type in required_types:
            self.assertIn(f"'authority_type', '{authority_type}'", self.sql)

    def test_authority_grant_seeded_issuer_is_seeded_in_both_tables(self) -> None:
        """The bounded grant issuer must be seeded as both an
        identifier_registry row and available via cdp_core.actor's join
        target -- unlike the identity-recognition authority, this actor
        does not need a cdp_core.actor row itself (it is only ever an
        issuer/revoker reference, never a subject looked up via
        actors_repo.fetch_actor), so only the identifier_registry seed is
        required here."""
        self.assertIn("'actor', 'cdp_authority_grant_issuer'", self.sql)

    def test_authority_grant_requires_mandatory_expiry(self) -> None:
        self.assertIn("expires_at TIMESTAMPTZ NOT NULL", self.sql)
        self.assertIn("chk_authority_grant_expires_after_effective", self.sql)

    def test_authority_grant_forbids_delete_at_database_level(self) -> None:
        self.assertIn("trg_authority_grant_forbid_delete", self.sql)
        self.assertIn("BEFORE DELETE ON cdp_core.authority_grant", self.executable_sql)

    def test_authority_evaluation_result_forbids_delete_at_database_level(self) -> None:
        self.assertIn("trg_authority_evaluation_result_forbid_delete", self.sql)
        self.assertIn(
            "BEFORE DELETE ON cdp_core.authority_evaluation_result", self.executable_sql
        )

    def test_authority_grant_status_is_restricted_to_active_or_revoked(self) -> None:
        """Even though the controlled vocabulary seeds all 5 RFC values,
        this slice's own CHECK constraint only permits the two values its
        service layer actually writes."""
        self.assertIn("chk_authority_grant_status_value", self.sql)
        self.assertIn("CHECK (status IN ('active', 'revoked'))", self.executable_sql)

    def test_authority_grant_revocation_fields_are_paired(self) -> None:
        self.assertIn("chk_authority_grant_revocation_pairing", self.sql)

    def test_authority_grant_references_actor_and_issuer(self) -> None:
        required_snippets = [
            "REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)",
        ]
        for snippet in required_snippets:
            self.assertIn(snippet, self.sql)

    def test_authority_evaluation_result_references_grant_and_decision(self) -> None:
        required_snippets = [
            "REFERENCES cdp_core.authority_grant (authority_grant_id)",
            "REFERENCES cdp_core.decision_registry (registry_name, decision_id)",
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
            "011 should not define a secret-bearing column",
        )


class Migration011PostgresSmokeTests(unittest.TestCase):
    """Optional Postgres execution smoke test.

    Set CDP_TEST_DATABASE_URL to enable. Applies 001 through 010, then 011
    twice inside one transaction (rolled back at the end) to prove
    rerun-safety without touching persistent local data.
    """

    def test_apply_001_through_010_then_011_twice_is_idempotent(self) -> None:
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
            cursor.execute(read_sql(DDL_010))
            cursor.execute(read_sql(DDL_011))
            # Rerun 011 alone to prove idempotency/rerun-safety.
            cursor.execute(read_sql(DDL_011))

            for table in ("cdp_core.authority_grant", "cdp_core.authority_evaluation_result"):
                cursor.execute(f"SELECT to_regclass('{table}')")
                self.assertIsNotNone(cursor.fetchone()[0], f"missing {table}")

            cursor.execute(
                "SELECT count(*) FROM cdp_core.identifier_registry WHERE registry_name = 'authority_type'"
            )
            self.assertEqual(cursor.fetchone()[0], 23)

            cursor.execute(
                "SELECT 1 FROM cdp_core.identifier_registry "
                "WHERE registry_name = 'actor' AND identifier_id = 'cdp_authority_grant_issuer'"
            )
            self.assertIsNotNone(cursor.fetchone(), "missing seeded cdp_authority_grant_issuer actor")

            # Prove the anti-delete trigger on authority_grant actually
            # fires, not just that the SQL text mentions it. Needs a real
            # actor row (FK target), created directly rather than through
            # the application's register_actor path.
            cursor.execute(
                """
                INSERT INTO cdp_core.identifier_registry
                    (registry_name, identifier_id, identifier_type_registry_name, identifier_type_id,
                     display_label, status)
                VALUES ('actor', 'test_authority_actor', 'cdp_actor_type', 'human', 'Test Authority Actor', 'active')
                """
            )
            cursor.execute(
                "INSERT INTO cdp_core.actor (actor_id, actor_type) VALUES ('test_authority_actor', 'human')"
            )
            cursor.execute(
                """
                INSERT INTO cdp_core.authority_grant
                    (actor_id, authority, scope_registry_name, issued_at, effective_at,
                     expires_at, issuer_actor_id, basis)
                VALUES
                    ('test_authority_actor', 'PROPOSE', 'sample_attorney_demo', now(), now(),
                     now() + interval '1 day', 'cdp_authority_grant_issuer', 'policy')
                RETURNING authority_grant_id
                """
            )
            grant_id = cursor.fetchone()[0]
            with self.assertRaises(Exception):
                cursor.execute(
                    "DELETE FROM cdp_core.authority_grant WHERE authority_grant_id = %s",
                    (grant_id,),
                )
            conn.rollback()

            # Unrelated configured workflow_definition rows must be untouched.
            cursor = conn.cursor()
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
