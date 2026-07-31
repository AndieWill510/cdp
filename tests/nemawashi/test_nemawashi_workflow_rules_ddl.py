"""Smoke tests for the Nemawashi workflow/rules DDL.

These tests intentionally have two layers:

1. static smoke tests that inspect the DDL text with no database dependency;
2. an optional Postgres integration smoke test, enabled only when
   CDP_TEST_DATABASE_URL is set.

The goal is to prove the first workflow/rules slice has the right bones while
keeping the default test run lightweight and dependency-friendly.
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


REQUIRED_TABLES = {
    "cdp_core.decision_stakeholder",
    "cdp_core.workflow_definition",
    "cdp_core.workflow_stage",
    "cdp_core.workflow_instance",
    "cdp_core.workflow_task",
    "cdp_core.rule_set",
    "cdp_core.rule_definition",
    "cdp_core.rule_evaluation_result",
    "cdp_core.communication_thread",
    "cdp_core.communication_participant",
    "cdp_core.communication_message",
}


REQUIRED_PROJECTIONS = {
    "cdp_projection.nemawashi_stakeholder_map_flat",
    "cdp_projection.workflow_task_queue",
    "cdp_projection.nemawashi_blockers",
    "cdp_projection.communication_thread_flat",
    "cdp_projection.rule_evaluation_findings",
}


REQUIRED_REGISTRIES = {
    "stakeholder_role",
    "participation_status",
    "standing_status",
    "workflow_definition_code",
    "workflow_stage_code",
    "workflow_status",
    "workflow_task_type",
    "workflow_task_status",
    "rule_set_code",
    "rule_scope",
    "rule_condition_language",
    "rule_action_type",
    "rule_evaluation_status",
    "communication_thread_type",
    "communication_thread_status",
    "communication_message_type",
    "communication_message_status",
    "notification_status",
    "lifecycle_stage",
}


RESTRICTED_ACCESS_RULES = {
    "restricted_dataset_requires_data_owner",
    "workflow_configuration_requires_system_owner",
    "human_required_creates_reviewer_task",
    "access_escalation_opens_consultation_thread",
    "missing_required_stakeholder_blocks_admission",
}


def read_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def compact(sql: str) -> str:
    """Normalize whitespace for simple DDL text assertions."""
    return re.sub(r"\s+", " ", sql.lower()).strip()


class NemawashiWorkflowRulesDDLStaticTests(unittest.TestCase):
    """Fast tests that prove the DDL has the expected workflow/rules bones."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.sql = read_sql(DDL_003)
        cls.compact_sql = compact(cls.sql)

    def test_ddl_file_exists_and_names_boundary(self) -> None:
        self.assertTrue(DDL_003.exists(), "003 Nemawashi DDL file should exist")
        self.assertIn("config_lookup may hold boring non-governance defaults", self.sql)
        self.assertIn("Governed workflow/rule/stakeholder authority belongs here", self.sql)

    def test_config_lookup_is_not_used_as_governance_storage(self) -> None:
        forbidden_patterns = [
            r"create\s+table\s+if\s+not\s+exists\s+cdp_core\.config_lookup",
            r"insert\s+into\s+cdp_core\.config_lookup",
            r"update\s+cdp_core\.config_lookup",
            r"alter\s+table\s+cdp_core\.config_lookup",
        ]
        for pattern in forbidden_patterns:
            self.assertIsNone(
                re.search(pattern, self.compact_sql),
                f"003 DDL should not use config_lookup for governed workflow/rules storage: {pattern}",
            )

    def test_required_tables_are_created(self) -> None:
        for table in sorted(REQUIRED_TABLES):
            self.assertIn(f"create table if not exists {table}".lower(), self.compact_sql)

    def test_required_projection_views_are_created(self) -> None:
        for projection in sorted(REQUIRED_PROJECTIONS):
            self.assertIn(f"create or replace view {projection}".lower(), self.compact_sql)

    def test_controlled_registries_are_seeded(self) -> None:
        for registry_name in sorted(REQUIRED_REGISTRIES):
            self.assertIn(
                f"('registry', '{registry_name}'",
                self.sql,
                f"missing registry seed for {registry_name}",
            )

    def test_restricted_data_access_rules_are_seeded(self) -> None:
        for rule_code in sorted(RESTRICTED_ACCESS_RULES):
            self.assertIn(rule_code, self.sql)

    def test_rules_engine_is_governed_and_versioned(self) -> None:
        required_snippets = [
            "rule_set_code_registry_name TEXT NOT NULL DEFAULT 'rule_set_code'",
            "rule_set_version TEXT NOT NULL",
            "rule_code TEXT NOT NULL",
            "rule_version TEXT NOT NULL",
            "condition_language_registry_name TEXT NOT NULL DEFAULT 'rule_condition_language'",
            "action_type_registry_name TEXT NOT NULL DEFAULT 'rule_action_type'",
            "action_payload JSONB NOT NULL DEFAULT '{}'::jsonb",
            "COMMENT ON TABLE cdp_core.rule_definition IS",
            "Rules do not silently mutate decisions",
        ]
        for snippet in required_snippets:
            self.assertIn(snippet, self.sql)

    def test_stakeholder_and_workflow_tables_reference_decisions_and_identifiers(self) -> None:
        required_snippets = [
            "REFERENCES cdp_core.decision_registry (registry_name, decision_id)",
            "REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)",
            "REFERENCES cdp_core.workflow_definition (workflow_definition_id)",
            "REFERENCES cdp_core.workflow_stage (workflow_stage_id)",
            "REFERENCES cdp_core.rule_definition (rule_id)",
        ]
        for snippet in required_snippets:
            self.assertIn(snippet, self.sql)

    def test_communication_is_decision_scoped_not_general_chat(self) -> None:
        required_snippets = [
            "CREATE TABLE IF NOT EXISTS cdp_core.communication_thread",
            "registry_name TEXT NOT NULL",
            "decision_id TEXT NOT NULL",
            "workflow_instance_id UUID",
            "Governed decision-specific communication thread. Not a general chat room.",
            "CREATE TABLE IF NOT EXISTS cdp_core.communication_message",
        ]
        for snippet in required_snippets:
            self.assertIn(snippet, self.sql)

    def test_nemawashi_blocker_projection_covers_multiple_blocker_sources(self) -> None:
        required_blocker_sources = {
            "workflow_instance_blocked",
            "blocking_task",
            "required_stakeholder_response",
            "rule_blocked_transition",
        }
        for blocker_source in sorted(required_blocker_sources):
            self.assertIn(blocker_source, self.sql)


class NemawashiWorkflowRulesDDLPostgresSmokeTests(unittest.TestCase):
    """Optional Postgres execution smoke test.

    Set CDP_TEST_DATABASE_URL to enable. The test applies 001 then 003 inside a
    transaction and rolls back at the end so it can be pointed at a disposable
    local database during development or CI.
    """

    def test_apply_001_then_003_when_database_url_is_available(self) -> None:
        database_url = os.environ.get("CDP_TEST_DATABASE_URL")
        if not database_url:
            self.skipTest("set CDP_TEST_DATABASE_URL to run Postgres DDL smoke test")

        conn = self._connect(database_url)
        try:
            cursor = conn.cursor()
            cursor.execute(read_sql(DDL_001))
            cursor.execute(read_sql(DDL_003))

            for relation in sorted(REQUIRED_TABLES | REQUIRED_PROJECTIONS):
                cursor.execute("SELECT to_regclass(%s)", (relation,))
                self.assertIsNotNone(cursor.fetchone()[0], f"missing relation {relation}")

            cursor.execute(
                """
                SELECT count(*)
                FROM cdp_core.identifier_registry
                WHERE registry_name = 'stakeholder_role'
                  AND identifier_id IN ('data_owner', 'privacy_reviewer', 'legal_reviewer')
                """
            )
            self.assertEqual(cursor.fetchone()[0], 3)

            cursor.execute(
                """
                SELECT count(*)
                FROM cdp_core.rule_definition
                WHERE rule_code IN (
                    'restricted_dataset_requires_data_owner',
                    'human_required_creates_reviewer_task',
                    'missing_required_stakeholder_blocks_admission'
                )
                """
            )
            self.assertEqual(cursor.fetchone()[0], 3)
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
