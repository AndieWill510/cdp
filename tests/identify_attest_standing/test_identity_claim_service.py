"""Integration tests for submit/recognize/deny/contest_identity_claim
(RFC-CDP-030 Identify Protocol, RFC-CDP-033 SS11.2 existence/recognition/
scope distinction).

Require CDP_TEST_DATABASE_URL pointing at a database with
001-decision-registry-kernel.sql and 010-identity-and-attestation.sql
already applied.

Cleanup note: cdp_core.identity_claim and cdp_core.actor rows cannot be
deleted (010 enforces this at the database level) -- see
test_actor_service.py's module docstring for why tests do not attempt to
clean these tables up, and instead use uuid-suffixed identifiers.
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


def _register_actor(prefix: str, **overrides):
    from cdp.core.services import ActorInput, register_actor

    actor_id = _unique_actor_id(prefix)
    kwargs = {
        "actor_id": actor_id,
        "actor_type": "human",
        "display_label": prefix,
        **overrides,
    }
    register_actor(ActorInput(**kwargs))
    return actor_id


@unittest.skipUnless(os.environ.get("CDP_TEST_DATABASE_URL"), "set CDP_TEST_DATABASE_URL to run")
class IdentityClaimTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ.setdefault("DATABASE_URL", _database_url())
        if not _actor_table_exists():
            raise unittest.SkipTest(
                "010-identity-and-attestation.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )

    def test_submit_claim_starts_pending_and_is_preserved(self) -> None:
        from cdp.core.services import IdentityClaimInput, submit_identity_claim

        actor_id = _register_actor("iaa-claim-submit")
        result = submit_identity_claim(
            IdentityClaimInput(
                actor_id=actor_id,
                claimant_actor_id=actor_id,
                claimed_identity_descriptor="Continuity of this test actor.",
                purpose_scope="decision_creation",
                evidence_refs=["evidence-ref-1"],
            )
        )

        claim = result["identity_claim"]
        self.assertEqual(claim["recognition_status"], "pending")
        self.assertEqual(claim["actor_id"], actor_id)
        self.assertIsNone(claim["recognized_by_actor_id"])
        self.assertIsNone(claim["decided_at"])

    def test_submit_claim_for_unknown_actor_fails(self) -> None:
        from cdp.core.services import ActorNotFound, IdentityClaimInput, submit_identity_claim

        unknown_actor_id = _unique_actor_id("iaa-claim-unknown")
        with self.assertRaises(ActorNotFound):
            submit_identity_claim(
                IdentityClaimInput(
                    actor_id=unknown_actor_id,
                    claimant_actor_id=unknown_actor_id,
                    claimed_identity_descriptor="Should not be created.",
                    purpose_scope="decision_creation",
                )
            )

    def test_recognize_claim_records_who_why_when(self) -> None:
        from cdp.core.services import (
            IdentityClaimDecisionInput,
            IdentityClaimInput,
            recognize_identity_claim,
            submit_identity_claim,
        )

        actor_id = _register_actor("iaa-claim-recognize")
        recognizer_id = _register_actor("iaa-claim-recognizer")
        claim = submit_identity_claim(
            IdentityClaimInput(
                actor_id=actor_id,
                claimant_actor_id=actor_id,
                claimed_identity_descriptor="Continuity claim.",
                purpose_scope="decision_creation",
            )
        )["identity_claim"]

        result = recognize_identity_claim(
            IdentityClaimDecisionInput(
                claim_id=claim["claim_id"],
                decided_by_actor_id=recognizer_id,
                rationale="Evidence checked out.",
            )
        )

        recognized = result["identity_claim"]
        self.assertEqual(recognized["recognition_status"], "recognized")
        self.assertEqual(recognized["recognized_by_actor_id"], recognizer_id)
        self.assertEqual(recognized["recognition_rationale"], "Evidence checked out.")
        self.assertIsNotNone(recognized["decided_at"])

    def test_deny_claim_preserves_the_row_it_does_not_erase_it(self) -> None:
        from cdp.core.services import (
            IdentityClaimDecisionInput,
            IdentityClaimInput,
            deny_identity_claim,
            submit_identity_claim,
        )

        actor_id = _register_actor("iaa-claim-deny")
        denier_id = _register_actor("iaa-claim-denier")
        descriptor = "A claim that will be denied but never erased."
        claim = submit_identity_claim(
            IdentityClaimInput(
                actor_id=actor_id,
                claimant_actor_id=actor_id,
                claimed_identity_descriptor=descriptor,
                purpose_scope="decision_creation",
            )
        )["identity_claim"]

        result = deny_identity_claim(
            IdentityClaimDecisionInput(
                claim_id=claim["claim_id"],
                decided_by_actor_id=denier_id,
                rationale="Evidence did not support the claim.",
            )
        )
        self.assertEqual(result["identity_claim"]["recognition_status"], "denied")

        with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
            cursor.execute(
                "SELECT recognition_status, claimed_identity_descriptor "
                "FROM cdp_core.identity_claim WHERE claim_id = %s",
                (claim["claim_id"],),
            )
            row = cursor.fetchone()
            self.assertIsNotNone(row, "denied claim row must still exist")
            self.assertEqual(row["recognition_status"], "denied")
            self.assertEqual(row["claimed_identity_descriptor"], descriptor)

    def test_deny_claim_cannot_be_deleted_at_the_database_level(self) -> None:
        from cdp.core.services import (
            IdentityClaimDecisionInput,
            IdentityClaimInput,
            deny_identity_claim,
            submit_identity_claim,
        )

        actor_id = _register_actor("iaa-claim-nodelete")
        denier_id = _register_actor("iaa-claim-nodelete-denier")
        claim = submit_identity_claim(
            IdentityClaimInput(
                actor_id=actor_id,
                claimant_actor_id=actor_id,
                claimed_identity_descriptor="Never erasable.",
                purpose_scope="decision_creation",
            )
        )["identity_claim"]
        deny_identity_claim(
            IdentityClaimDecisionInput(
                claim_id=claim["claim_id"], decided_by_actor_id=denier_id, rationale="No."
            )
        )

        with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
            with self.assertRaises(psycopg.errors.Error):
                cursor.execute(
                    "DELETE FROM cdp_core.identity_claim WHERE claim_id = %s",
                    (claim["claim_id"],),
                )
            conn.rollback()

    def test_contest_a_recognized_claim(self) -> None:
        from cdp.core.services import (
            IdentityClaimDecisionInput,
            IdentityClaimInput,
            contest_identity_claim,
            recognize_identity_claim,
            submit_identity_claim,
        )

        actor_id = _register_actor("iaa-claim-contest")
        other_id = _register_actor("iaa-claim-contester")
        claim = submit_identity_claim(
            IdentityClaimInput(
                actor_id=actor_id,
                claimant_actor_id=actor_id,
                claimed_identity_descriptor="Contested continuity.",
                purpose_scope="decision_creation",
            )
        )["identity_claim"]
        recognize_identity_claim(
            IdentityClaimDecisionInput(
                claim_id=claim["claim_id"], decided_by_actor_id=other_id, rationale="Looked fine."
            )
        )

        result = contest_identity_claim(
            IdentityClaimDecisionInput(
                claim_id=claim["claim_id"],
                decided_by_actor_id=other_id,
                rationale="New information raises doubt.",
            )
        )
        self.assertEqual(result["identity_claim"]["recognition_status"], "contested")

    def test_deciding_an_already_denied_claim_is_rejected(self) -> None:
        from cdp.core.services import (
            IdentityClaimDecisionInput,
            IdentityClaimInput,
            IdentityClaimNotDecidable,
            deny_identity_claim,
            submit_identity_claim,
        )

        actor_id = _register_actor("iaa-claim-terminal")
        decider_id = _register_actor("iaa-claim-terminal-decider")
        claim = submit_identity_claim(
            IdentityClaimInput(
                actor_id=actor_id,
                claimant_actor_id=actor_id,
                claimed_identity_descriptor="Will be denied twice.",
                purpose_scope="decision_creation",
            )
        )["identity_claim"]
        deny_identity_claim(
            IdentityClaimDecisionInput(
                claim_id=claim["claim_id"], decided_by_actor_id=decider_id, rationale="No."
            )
        )

        with self.assertRaises(IdentityClaimNotDecidable):
            deny_identity_claim(
                IdentityClaimDecisionInput(
                    claim_id=claim["claim_id"],
                    decided_by_actor_id=decider_id,
                    rationale="Still no.",
                )
            )

    def test_supersede_links_both_claims_without_deleting_either(self) -> None:
        from cdp.core.services import (
            IdentityClaimDecisionInput,
            IdentityClaimInput,
            recognize_identity_claim,
            submit_identity_claim,
        )

        actor_id = _register_actor("iaa-claim-supersede")
        recognizer_id = _register_actor("iaa-claim-supersede-recognizer")
        original = submit_identity_claim(
            IdentityClaimInput(
                actor_id=actor_id,
                claimant_actor_id=actor_id,
                claimed_identity_descriptor="Original claim.",
                purpose_scope="decision_creation",
            )
        )["identity_claim"]
        recognize_identity_claim(
            IdentityClaimDecisionInput(
                claim_id=original["claim_id"],
                decided_by_actor_id=recognizer_id,
                rationale="Fine for now.",
            )
        )

        successor = submit_identity_claim(
            IdentityClaimInput(
                actor_id=actor_id,
                claimant_actor_id=actor_id,
                claimed_identity_descriptor="Updated claim.",
                purpose_scope="decision_creation",
                supersedes_claim_id=original["claim_id"],
            )
        )["identity_claim"]

        with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
            cursor.execute(
                "SELECT recognition_status, superseded_by_claim_id "
                "FROM cdp_core.identity_claim WHERE claim_id = %s",
                (original["claim_id"],),
            )
            row = cursor.fetchone()
            self.assertEqual(row["recognition_status"], "superseded")
            self.assertEqual(row["superseded_by_claim_id"], successor["claim_id"])

            cursor.execute(
                "SELECT recognition_status, supersedes_claim_id "
                "FROM cdp_core.identity_claim WHERE claim_id = %s",
                (successor["claim_id"],),
            )
            row = cursor.fetchone()
            self.assertEqual(row["recognition_status"], "pending")
            self.assertEqual(row["supersedes_claim_id"], original["claim_id"])


if __name__ == "__main__":
    unittest.main()
