"""Smoke tests for the 010 identity-and-attestation migration.

Two layers, following the pattern established in
test_migration_009_execution_record.py:

1. static smoke tests that inspect the DDL text with no database dependency;
2. an optional Postgres integration smoke test, enabled only when
   CDP_TEST_DATABASE_URL is set, that proves 001 -> ... -> 009 -> 010 apply
   cleanly and that re-running 010 is a no-op (idempotent, rerun-safe).
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


def read_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_sql_comments(sql: str) -> str:
    """Drop `-- ...` line comments so text assertions ignore prose in comments."""
    return re.sub(r"--[^\n]*", "", sql)


class Migration010StaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sql = read_sql(DDL_010)
        cls.executable_sql = strip_sql_comments(cls.sql)

    def test_migration_file_exists(self) -> None:
        self.assertTrue(DDL_010.exists(), "010 identity-and-attestation DDL should exist")

    def test_migration_is_additive_only(self) -> None:
        compact_sql = re.sub(r"\s+", " ", self.executable_sql.lower())
        for forbidden in ("drop table", "drop schema", "truncate", "delete from"):
            self.assertNotIn(forbidden, compact_sql, f"010 should not contain: {forbidden}")

    def test_migration_uses_create_if_not_exists_for_new_tables(self) -> None:
        for table in ("cdp_core.actor", "cdp_core.identity_claim", "cdp_core.attestation_record"):
            self.assertIn(f"CREATE TABLE IF NOT EXISTS {table}", self.executable_sql)

    def test_migration_does_not_touch_schema_version(self) -> None:
        self.assertNotIn("cdp_core.schema_version", self.executable_sql)

    def test_migration_does_not_write_out_of_scope_governance_tables(self) -> None:
        """This slice must not implement Authority, Standing, Legitimize, or
        Repair, and must not write to decision_registry, workflow_instance,
        workflow_definition, challenge_record, or execution tables -- only
        read them via FK reference."""
        forbidden_statements = [
            "UPDATE cdp_core.decision_registry",
            "UPDATE cdp_core.workflow_instance",
            "UPDATE cdp_core.workflow_definition",
            "UPDATE cdp_core.workflow_task",
            "UPDATE cdp_core.challenge_record",
            "UPDATE cdp_core.challenge_adjudication_record",
            "UPDATE cdp_core.execution_authorization_record",
            "UPDATE cdp_core.execution_record",
            "CREATE TABLE IF NOT EXISTS cdp_core.authority",
            "CREATE TABLE IF NOT EXISTS cdp_core.standing",
            "CREATE TABLE IF NOT EXISTS cdp_core.legitimacy",
            "CREATE TABLE IF NOT EXISTS cdp_core.repair",
        ]
        for statement in forbidden_statements:
            self.assertNotIn(statement, self.executable_sql)

    def test_migration_registers_all_controlled_vocabularies(self) -> None:
        required_snippets = [
            "'cdp_actor_type'",
            "('cdp_actor_type', 'human'",
            "('cdp_actor_type', 'institution'",
            "('cdp_actor_type', 'synthetic'",
            "('cdp_actor_type', 'collective'",
            "'actor_display_mode'",
            "('actor_display_mode', 'public'",
            "('actor_display_mode', 'protected'",
            "('actor_display_mode', 'pseudonymous'",
            "'actor_status'",
            "('actor_status', 'active'",
            "('actor_status', 'suspended'",
            "('actor_status', 'revoked'",
            "('actor_status', 'superseded'",
            "'identity_claim_recognition_status'",
            "('identity_claim_recognition_status', 'pending'",
            "('identity_claim_recognition_status', 'recognized'",
            "('identity_claim_recognition_status', 'denied'",
            "('identity_claim_recognition_status', 'contested'",
            "('identity_claim_recognition_status', 'superseded'",
            "('identity_claim_recognition_status', 'withdrawn'",
            "'attestation_method'",
            "('attestation_method', 'shared_secret_reference'",
            "'governed_act_type'",
            "('governed_act_type', 'decision_created'",
            "'attestation_verification_result'",
            "('attestation_verification_result', 'verified'",
            "('attestation_verification_result', 'failed'",
        ]
        for snippet in required_snippets:
            self.assertIn(snippet, self.sql)

    def test_actor_table_has_immutable_continuity_key(self) -> None:
        self.assertIn("identity_continuity_key UUID NOT NULL DEFAULT gen_random_uuid()", self.sql)
        self.assertIn("trg_actor_identity_continuity_immutable", self.sql)

    def test_no_secret_bearing_columns_anywhere_in_migration(self) -> None:
        """No column definition (name followed by a column type) may be
        named after a secret. This intentionally does not forbid the word
        'password' from appearing anywhere in the file -- it appears in
        prose comments and inside the credential_reference CHECK
        constraint's forbidden-substring pattern, neither of which defines
        a column."""
        column_def_pattern = re.compile(
            r"\b(password|passwd|private_key|secret_key)\s+(TEXT|VARCHAR|BYTEA|CHAR)\b",
            re.IGNORECASE,
        )
        self.assertIsNone(
            column_def_pattern.search(self.executable_sql),
            "010 should not define a secret-bearing column",
        )

    def test_identity_claim_forbids_delete_at_database_level(self) -> None:
        self.assertIn("trg_identity_claim_forbid_delete", self.sql)
        self.assertIn("BEFORE DELETE ON cdp_core.identity_claim", self.executable_sql)
        self.assertIn("RAISE EXCEPTION", self.sql)

    def test_identity_claim_supports_supersession_without_erasure(self) -> None:
        self.assertIn("supersedes_claim_id UUID", self.sql)
        self.assertIn("superseded_by_claim_id UUID", self.sql)

    def test_actor_references_identifier_registry(self) -> None:
        self.assertIn(
            "REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)",
            self.sql,
        )

    def test_attestation_record_references_actor_claim_and_decision(self) -> None:
        required_snippets = [
            "REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)",
            "REFERENCES cdp_core.identity_claim (claim_id)",
            "REFERENCES cdp_core.decision_registry (registry_name, decision_id)",
        ]
        for snippet in required_snippets:
            self.assertIn(snippet, self.sql)

    def test_attestation_verification_result_requires_failure_reason_pairing(self) -> None:
        self.assertIn("chk_attestation_failure_reason_pairing", self.sql)

    def test_recognition_authority_actor_is_seeded_in_both_tables(self) -> None:
        """The bounded recognition authority must be seeded as both an
        identifier_registry row and a full cdp_core.actor row -- the
        latter is required because _decide_identity_claim's decider lookup
        (actors_repo.fetch_actor) inner-joins both tables."""
        self.assertIn("'actor', 'cdp_identity_recognition_authority'", self.sql)
        self.assertIn(
            "INSERT INTO cdp_core.actor (actor_id, actor_type, display_mode, actor_status)",
            self.executable_sql,
        )
        self.assertIn("'cdp_identity_recognition_authority', 'institution'", self.sql)


class Migration010PostgresSmokeTests(unittest.TestCase):
    """Optional Postgres execution smoke test.

    Set CDP_TEST_DATABASE_URL to enable. Applies 001 through 009, then 010
    twice inside one transaction (rolled back at the end) to prove
    rerun-safety without touching persistent local data.
    """

    def test_apply_001_through_009_then_010_twice_is_idempotent(self) -> None:
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
            # Rerun 010 alone to prove idempotency/rerun-safety.
            cursor.execute(read_sql(DDL_010))

            for table in (
                "cdp_core.actor",
                "cdp_core.identity_claim",
                "cdp_core.attestation_record",
            ):
                cursor.execute(f"SELECT to_regclass('{table}')")
                self.assertIsNotNone(cursor.fetchone()[0], f"missing {table}")

            cursor.execute(
                "SELECT count(*) FROM cdp_core.identifier_registry WHERE registry_name = 'cdp_actor_type'"
            )
            self.assertEqual(cursor.fetchone()[0], 4)

            cursor.execute(
                "SELECT count(*) FROM cdp_core.identifier_registry "
                "WHERE registry_name = 'identity_claim_recognition_status'"
            )
            self.assertEqual(cursor.fetchone()[0], 6)

            cursor.execute(
                "SELECT 1 FROM cdp_core.identifier_registry "
                "WHERE registry_name = 'actor' AND identifier_id = 'cdp_attestation_service'"
            )
            self.assertIsNotNone(cursor.fetchone(), "missing seeded cdp_attestation_service actor")

            cursor.execute(
                "SELECT 1 FROM cdp_core.identifier_registry "
                "WHERE registry_name = 'actor' AND identifier_id = 'cdp_identity_recognition_authority'"
            )
            self.assertIsNotNone(
                cursor.fetchone(),
                "missing seeded cdp_identity_recognition_authority identifier_registry row",
            )

            cursor.execute(
                "SELECT actor_type, actor_status FROM cdp_core.actor "
                "WHERE actor_id = 'cdp_identity_recognition_authority'"
            )
            row = cursor.fetchone()
            self.assertIsNotNone(
                row, "missing seeded cdp_identity_recognition_authority cdp_core.actor row"
            )
            self.assertEqual(row[0], "institution")
            self.assertEqual(row[1], "active")

            # Prove the anti-delete trigger actually fires, not just that
            # the SQL text mentions it.
            cursor.execute(
                """
                INSERT INTO cdp_core.identifier_registry
                    (registry_name, identifier_id, identifier_type_registry_name, identifier_type_id,
                     display_label, status)
                VALUES ('actor', 'test_delete_actor', 'cdp_actor_type', 'human', 'Test Delete Actor', 'active')
                """
            )
            cursor.execute(
                "INSERT INTO cdp_core.actor (actor_id, actor_type) VALUES ('test_delete_actor', 'human')"
            )
            cursor.execute(
                """
                INSERT INTO cdp_core.identity_claim
                    (actor_id, claimant_actor_id, claimed_identity_descriptor, purpose_scope)
                VALUES ('test_delete_actor', 'test_delete_actor', 'test descriptor', 'decision_creation')
                RETURNING claim_id
                """
            )
            claim_id = cursor.fetchone()[0]
            with self.assertRaises(Exception):
                cursor.execute(
                    "DELETE FROM cdp_core.identity_claim WHERE claim_id = %s", (claim_id,)
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
