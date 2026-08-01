"""Integration tests for grant_authority/revoke_authority (RFC-CDP-032
Authority and Delegation Model, scoped to SS19 Minimal Compliance).

Require CDP_TEST_DATABASE_URL pointing at a database with
001-decision-registry-kernel.sql and 011-authority-and-delegation.sql
already applied.

Recognition-authority-style discipline: only the single seeded
`cdp_authority_grant_issuer` actor may issue or revoke a grant. Tests
below use that literal, pre-seeded actor_id rather than registering an
arbitrary actor for the role -- an arbitrary registered actor is exactly
what must be rejected, covered by
test_grant_by_unauthorized_actor_is_rejected and
test_revoke_by_unauthorized_actor_is_rejected below.

Cleanup note: cdp_core.authority_grant rows cannot be deleted (011
enforces this at the database level) -- see
tests/identify_attest_standing/test_actor_service.py's module docstring
for the same reasoning applied there. Tests use uuid-suffixed identifiers.
"""

from __future__ import annotations

import os
import unittest
import uuid
from datetime import datetime, timedelta, timezone

import psycopg
from psycopg.rows import dict_row

REGISTRY_NAME = "sample_attorney_demo"
DECISION_CLASS_ID = "claim_approval"

# Pre-seeded by 011-authority-and-delegation.sql; not registered by these
# tests.
GRANT_ISSUER_ACTOR_ID = "cdp_authority_grant_issuer"


def _database_url() -> str:
    return os.environ.get("CDP_TEST_DATABASE_URL", "postgresql://cdp:cdp@localhost:5432/cdp")


def _authority_grant_table_exists() -> bool:
    with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
        cursor.execute("SELECT to_regclass('cdp_core.authority_grant')")
        return cursor.fetchone()[0] is not None


def _unique(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def _register_actor(prefix: str, **overrides):
    from cdp.core.services import ActorInput, register_actor

    actor_id = _unique(prefix)
    kwargs = {"actor_id": actor_id, "actor_type": "human", "display_label": prefix, **overrides}
    register_actor(ActorInput(**kwargs))
    return actor_id


def _make_grant_input(actor_id: str, **overrides):
    from cdp.core.services import GrantAuthorityInput

    kwargs = {
        "actor_id": actor_id,
        "authority": "PROPOSE",
        "scope_registry_name": REGISTRY_NAME,
        "scope_decision_class_id": DECISION_CLASS_ID,
        "expires_at": datetime.now(timezone.utc) + timedelta(days=1),
        "issued_by_actor_id": GRANT_ISSUER_ACTOR_ID,
        "basis": "policy",
        **overrides,
    }
    return GrantAuthorityInput(**kwargs)


@unittest.skipUnless(os.environ.get("CDP_TEST_DATABASE_URL"), "set CDP_TEST_DATABASE_URL to run")
class AuthorityGrantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ.setdefault("DATABASE_URL", _database_url())
        if not _authority_grant_table_exists():
            raise unittest.SkipTest(
                "011-authority-and-delegation.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )

    def test_happy_path_issues_grant(self) -> None:
        from cdp.core.services import grant_authority

        actor_id = _register_actor("iaa-grant-happy")
        result = grant_authority(_make_grant_input(actor_id))

        grant = result["authority_grant"]
        self.assertEqual(grant["actor_id"], actor_id)
        self.assertEqual(grant["authority"], "PROPOSE")
        self.assertEqual(grant["scope_registry_name"], REGISTRY_NAME)
        self.assertEqual(grant["scope_decision_class_id"], DECISION_CLASS_ID)
        self.assertEqual(grant["status"], "active")

        with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
            cursor.execute(
                "SELECT event_type FROM cdp_audit.event_log "
                "WHERE aggregate_type = 'authority_grant' AND aggregate_id = %s "
                "ORDER BY event_sequence",
                (str(grant["authority_grant_id"]),),
            )
            event_types = [row["event_type"] for row in cursor.fetchall()]
            self.assertEqual(event_types, ["authority_grant.issued"])

    def test_wildcard_scope_grant_omits_decision_class(self) -> None:
        from cdp.core.services import grant_authority

        actor_id = _register_actor("iaa-grant-wildcard")
        result = grant_authority(_make_grant_input(actor_id, scope_decision_class_id=None))
        self.assertIsNone(result["authority_grant"]["scope_decision_class_id"])

    def test_grant_by_unauthorized_actor_is_rejected(self) -> None:
        from cdp.core.services import AuthorityGrantIssuerRequired, grant_authority

        actor_id = _register_actor("iaa-grant-unauth-subject")
        unrelated_actor_id = _register_actor("iaa-grant-unauth-issuer")

        with self.assertRaises(AuthorityGrantIssuerRequired):
            grant_authority(_make_grant_input(actor_id, issued_by_actor_id=unrelated_actor_id))

    def test_grant_for_unknown_actor_fails(self) -> None:
        from cdp.core.services import ActorNotFound, grant_authority

        unknown_actor_id = _unique("iaa-grant-unknown")
        with self.assertRaises(ActorNotFound):
            grant_authority(_make_grant_input(unknown_actor_id))

    def test_revoke_happy_path_preserves_the_row(self) -> None:
        from cdp.core.services import RevokeAuthorityInput, grant_authority, revoke_authority

        actor_id = _register_actor("iaa-grant-revoke")
        grant = grant_authority(_make_grant_input(actor_id))["authority_grant"]

        result = revoke_authority(
            RevokeAuthorityInput(
                grant_id=grant["authority_grant_id"],
                revoked_by_actor_id=GRANT_ISSUER_ACTOR_ID,
                reason="No longer needed.",
            )
        )
        revoked = result["authority_grant"]
        self.assertEqual(revoked["status"], "revoked")
        self.assertIsNotNone(revoked["revoked_at"])
        self.assertEqual(revoked["revoked_by_actor_id"], GRANT_ISSUER_ACTOR_ID)
        self.assertEqual(revoked["revocation_reason"], "No longer needed.")

        with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
            cursor.execute(
                "SELECT status FROM cdp_core.authority_grant WHERE authority_grant_id = %s",
                (grant["authority_grant_id"],),
            )
            self.assertEqual(cursor.fetchone()["status"], "revoked")

    def test_revoke_by_unauthorized_actor_is_rejected(self) -> None:
        from cdp.core.services import (
            AuthorityGrantIssuerRequired,
            RevokeAuthorityInput,
            grant_authority,
            revoke_authority,
        )

        actor_id = _register_actor("iaa-grant-revoke-unauth")
        unrelated_actor_id = _register_actor("iaa-grant-revoke-unauth-revoker")
        grant = grant_authority(_make_grant_input(actor_id))["authority_grant"]

        with self.assertRaises(AuthorityGrantIssuerRequired):
            revoke_authority(
                RevokeAuthorityInput(
                    grant_id=grant["authority_grant_id"],
                    revoked_by_actor_id=unrelated_actor_id,
                    reason="I say so.",
                )
            )

    def test_revoke_unknown_grant_fails(self) -> None:
        from cdp.core.services import AuthorityGrantNotFound, RevokeAuthorityInput, revoke_authority

        with self.assertRaises(AuthorityGrantNotFound):
            revoke_authority(
                RevokeAuthorityInput(
                    grant_id=uuid.uuid4(),
                    revoked_by_actor_id=GRANT_ISSUER_ACTOR_ID,
                    reason="N/A",
                )
            )

    def test_revoke_already_revoked_grant_fails(self) -> None:
        from cdp.core.services import (
            AuthorityGrantNotActive,
            RevokeAuthorityInput,
            grant_authority,
            revoke_authority,
        )

        actor_id = _register_actor("iaa-grant-double-revoke")
        grant = grant_authority(_make_grant_input(actor_id))["authority_grant"]
        revoke_authority(
            RevokeAuthorityInput(
                grant_id=grant["authority_grant_id"],
                revoked_by_actor_id=GRANT_ISSUER_ACTOR_ID,
                reason="First revocation.",
            )
        )

        with self.assertRaises(AuthorityGrantNotActive):
            revoke_authority(
                RevokeAuthorityInput(
                    grant_id=grant["authority_grant_id"],
                    revoked_by_actor_id=GRANT_ISSUER_ACTOR_ID,
                    reason="Second revocation.",
                )
            )

    def test_grant_cannot_be_deleted_at_the_database_level(self) -> None:
        from cdp.core.services import grant_authority

        actor_id = _register_actor("iaa-grant-nodelete")
        grant = grant_authority(_make_grant_input(actor_id))["authority_grant"]

        with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
            with self.assertRaises(psycopg.errors.Error):
                cursor.execute(
                    "DELETE FROM cdp_core.authority_grant WHERE authority_grant_id = %s",
                    (grant["authority_grant_id"],),
                )
            conn.rollback()


if __name__ == "__main__":
    unittest.main()
