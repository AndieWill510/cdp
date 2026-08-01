"""Integration tests for register_actor (RFC-CDP-030 Identify Protocol).

These tests exercise the real repository/service stack against Postgres.
They require CDP_TEST_DATABASE_URL pointing at a database with
001-decision-registry-kernel.sql and 010-identity-and-attestation.sql
already applied.

Cleanup note: cdp_core.actor rows (and their underlying
cdp_core.identifier_registry rows) cannot be deleted -- 010 enforces this
at the database level (trg_actor_forbid_delete), which is the point of
this slice, not an oversight. Tests therefore use uuid-suffixed actor_ids
so repeated local runs never collide, and rely on CI's fresh-Postgres-per-
run (see .github/workflows/cdp-ci.yml) for a clean slate there, rather
than attempting any cleanup of these tables.

Import note: this module uses cdp.core (dataclasses, modern union type
hints) which targets the project's Python 3.12 runtime. Run it with the
interpreter used by the Docker stack (e.g. `docker compose exec cdp-api
pytest tests/identify_attest_standing/test_actor_service.py`), not an
older local virtualenv.
"""

from __future__ import annotations

import os
import unittest
import uuid

import psycopg
from psycopg.rows import dict_row


def _database_url() -> str:
    return os.environ.get("CDP_TEST_DATABASE_URL", "postgresql://cdp:cdp@localhost:5432/cdp")


def _actor_table_exists() -> bool:
    with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
        cursor.execute("SELECT to_regclass('cdp_core.actor')")
        return cursor.fetchone()[0] is not None


def _unique_actor_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


@unittest.skipUnless(os.environ.get("CDP_TEST_DATABASE_URL"), "set CDP_TEST_DATABASE_URL to run")
class RegisterActorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ.setdefault("DATABASE_URL", _database_url())
        if not _actor_table_exists():
            raise unittest.SkipTest(
                "010-identity-and-attestation.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )

    def test_happy_path_registers_actor_and_underlying_identifier(self) -> None:
        from cdp.core.services import ActorInput, register_actor

        actor_id = _unique_actor_id("iaa-actor-happy")
        result = register_actor(
            ActorInput(
                actor_id=actor_id,
                actor_type="human",
                display_label="Test Human Actor",
                display_mode="public",
            )
        )

        actor = result["actor"]
        self.assertEqual(actor["actor_id"], actor_id)
        self.assertEqual(actor["actor_type"], "human")
        self.assertEqual(actor["display_mode"], "public")
        self.assertEqual(actor["actor_status"], "active")
        self.assertIsNotNone(actor["identity_continuity_key"])

        with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
            cursor.execute(
                "SELECT registry_name, identifier_id FROM cdp_core.identifier_registry "
                "WHERE registry_name = 'actor' AND identifier_id = %s",
                (actor_id,),
            )
            self.assertIsNotNone(cursor.fetchone(), "underlying identifier_registry row missing")

            cursor.execute(
                "SELECT event_type FROM cdp_audit.event_log "
                "WHERE aggregate_type = 'actor' AND aggregate_id = %s "
                "ORDER BY event_sequence",
                (actor_id,),
            )
            event_types = [row["event_type"] for row in cursor.fetchall()]
            self.assertEqual(event_types, ["actor.registered"])

    def test_duplicate_actor_id_rejected_and_original_untouched(self) -> None:
        from cdp.core.services import ActorAlreadyRegistered, ActorInput, register_actor

        actor_id = _unique_actor_id("iaa-actor-dup")
        register_actor(
            ActorInput(actor_id=actor_id, actor_type="human", display_label="Original")
        )

        with self.assertRaises(ActorAlreadyRegistered):
            register_actor(
                ActorInput(actor_id=actor_id, actor_type="institution", display_label="Impostor")
            )

        with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
            cursor.execute(
                "SELECT actor_type FROM cdp_core.actor WHERE actor_id = %s", (actor_id,)
            )
            self.assertEqual(cursor.fetchone()["actor_type"], "human")

    def test_unknown_actor_type_rejected(self) -> None:
        from cdp.core.services import ActorInput, register_actor

        actor_id = _unique_actor_id("iaa-actor-badtype")
        with self.assertRaises(psycopg.errors.Error):
            register_actor(
                ActorInput(actor_id=actor_id, actor_type="not_a_real_type", display_label="X")
            )

    def test_actor_supports_all_minimum_required_actor_types(self) -> None:
        """RFC-CDP-030's minimum (human, institution, synthetic) plus this
        slice's required extension (collective) must all be representable."""
        from cdp.core.services import ActorInput, register_actor

        for actor_type in ("human", "institution", "synthetic", "collective"):
            actor_id = _unique_actor_id(f"iaa-actor-{actor_type}")
            result = register_actor(
                ActorInput(actor_id=actor_id, actor_type=actor_type, display_label=actor_type)
            )
            self.assertEqual(result["actor"]["actor_type"], actor_type)

    def test_protected_and_pseudonymous_display_modes_are_representable(self) -> None:
        """Display mode is a capability orthogonal to actor_type -- a human
        actor may be protected or pseudonymous without changing its type,
        supporting accountable continuity without forced public exposure."""
        from cdp.core.services import ActorInput, register_actor

        for display_mode in ("public", "protected", "pseudonymous"):
            actor_id = _unique_actor_id(f"iaa-actor-{display_mode}")
            result = register_actor(
                ActorInput(
                    actor_id=actor_id,
                    actor_type="human",
                    display_label=f"Actor ({display_mode})",
                    display_mode=display_mode,
                )
            )
            self.assertEqual(result["actor"]["display_mode"], display_mode)


if __name__ == "__main__":
    unittest.main()
