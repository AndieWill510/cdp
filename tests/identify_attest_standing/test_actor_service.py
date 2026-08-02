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


@unittest.skipUnless(os.environ.get("CDP_TEST_DATABASE_URL"), "set CDP_TEST_DATABASE_URL to run")
class CallerAuthenticationTests(unittest.TestCase):
    """Session 032 (RFC-CDP-030 SS6 / RFC-CDP-031 SS7): register_actor now
    also issues a bearer token, and verify_bearer_token /
    revoke_actor_bearer_token are the standalone boundary-check functions
    the API layer calls before every actor-asserting mutating route --
    see db/ddl/014-caller-authentication.sql and
    cdp/core/services.py's Caller Authentication section header."""

    @classmethod
    def setUpClass(cls) -> None:
        os.environ.setdefault("DATABASE_URL", _database_url())
        if not _actor_table_exists():
            raise unittest.SkipTest(
                "010-identity-and-attestation.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )
        with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
            cursor.execute("SELECT to_regclass('cdp_core.actor_bearer_token')")
            if cursor.fetchone()[0] is None:
                raise unittest.SkipTest(
                    "014-caller-authentication.sql is not applied to CDP_TEST_DATABASE_URL yet"
                )

    def test_register_actor_issues_a_token_stored_only_as_a_hash(self) -> None:
        import hashlib

        from cdp.core.services import ActorInput, register_actor

        actor_id = _unique_actor_id("iaa-actor-token")
        result = register_actor(
            ActorInput(actor_id=actor_id, actor_type="human", display_label="Token actor")
        )

        token = result["bearer_token"]
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 20)

        expected_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
            cursor.execute(
                "SELECT token_hash, status FROM cdp_core.actor_bearer_token WHERE actor_id = %s",
                (actor_id,),
            )
            row = cursor.fetchone()
            self.assertIsNotNone(row, "no actor_bearer_token row was created")
            self.assertEqual(row["token_hash"], expected_hash)
            self.assertEqual(row["status"], "active")
            self.assertNotEqual(row["token_hash"], token, "plaintext must never be stored")

    def test_verify_bearer_token_succeeds_for_the_correct_actor(self) -> None:
        from cdp.core.services import ActorInput, register_actor, verify_bearer_token

        actor_id = _unique_actor_id("iaa-actor-verify-ok")
        result = register_actor(
            ActorInput(actor_id=actor_id, actor_type="human", display_label="Verify actor")
        )

        verify_bearer_token(
            authorization_header=f"Bearer {result['bearer_token']}", expected_actor_id=actor_id
        )  # must not raise

    def test_verify_bearer_token_missing_header_raises(self) -> None:
        from cdp.core.services import BearerTokenMissing, verify_bearer_token

        with self.assertRaises(BearerTokenMissing):
            verify_bearer_token(authorization_header=None, expected_actor_id="anyone")

        with self.assertRaises(BearerTokenMissing):
            verify_bearer_token(authorization_header="", expected_actor_id="anyone")

        with self.assertRaises(BearerTokenMissing):
            verify_bearer_token(
                authorization_header="NotBearer sometoken", expected_actor_id="anyone"
            )

    def test_verify_bearer_token_unknown_token_raises_invalid(self) -> None:
        from cdp.core.services import BearerTokenInvalid, verify_bearer_token

        with self.assertRaises(BearerTokenInvalid):
            verify_bearer_token(
                authorization_header="Bearer this-token-was-never-issued",
                expected_actor_id="anyone",
            )

    def test_verify_bearer_token_wrong_actor_raises_mismatch(self) -> None:
        from cdp.core.services import (
            ActorInput,
            BearerTokenActorMismatch,
            register_actor,
            verify_bearer_token,
        )

        actor_id = _unique_actor_id("iaa-actor-verify-mismatch")
        other_actor_id = _unique_actor_id("iaa-actor-verify-other")
        result = register_actor(
            ActorInput(actor_id=actor_id, actor_type="human", display_label="Mismatch actor")
        )

        with self.assertRaises(BearerTokenActorMismatch):
            verify_bearer_token(
                authorization_header=f"Bearer {result['bearer_token']}",
                expected_actor_id=other_actor_id,
            )

    def test_revoke_then_verify_raises_invalid(self) -> None:
        from cdp.core.services import (
            ActorInput,
            BearerTokenInvalid,
            register_actor,
            revoke_actor_bearer_token,
            verify_bearer_token,
        )

        actor_id = _unique_actor_id("iaa-actor-revoke")
        result = register_actor(
            ActorInput(actor_id=actor_id, actor_type="human", display_label="Revoke actor")
        )
        token = result["bearer_token"]

        revoke_result = revoke_actor_bearer_token(actor_id)
        self.assertEqual(revoke_result["actor_bearer_token"]["status"], "revoked")
        self.assertIsNotNone(revoke_result["actor_bearer_token"]["revoked_at"])

        with self.assertRaises(BearerTokenInvalid):
            verify_bearer_token(authorization_header=f"Bearer {token}", expected_actor_id=actor_id)

    def test_revoke_with_no_active_token_raises(self) -> None:
        from cdp.core.services import (
            ActorInput,
            NoActiveBearerToken,
            register_actor,
            revoke_actor_bearer_token,
        )

        actor_id = _unique_actor_id("iaa-actor-revoke-twice")
        register_actor(ActorInput(actor_id=actor_id, actor_type="human", display_label="X"))
        revoke_actor_bearer_token(actor_id)

        with self.assertRaises(NoActiveBearerToken):
            revoke_actor_bearer_token(actor_id)

    def test_token_row_cannot_be_deleted_at_the_database_level(self) -> None:
        from cdp.core.services import ActorInput, register_actor

        actor_id = _unique_actor_id("iaa-actor-token-forbid-delete")
        register_actor(ActorInput(actor_id=actor_id, actor_type="human", display_label="X"))

        with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
            with self.assertRaises(psycopg.errors.RaiseException):
                cursor.execute(
                    "DELETE FROM cdp_core.actor_bearer_token WHERE actor_id = %s", (actor_id,)
                )
            conn.rollback()


if __name__ == "__main__":
    unittest.main()
