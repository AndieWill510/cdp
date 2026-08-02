"""Integration tests for submit/recognize/deny/contest_identity_claim
(RFC-CDP-030 Identify Protocol, RFC-CDP-033 SS11.2 existence/recognition/
scope distinction).

Require CDP_TEST_DATABASE_URL pointing at a database with
001-decision-registry-kernel.sql and 010-identity-and-attestation.sql
already applied.

Recognition authority note (v0.2 review correction): recognizing, denying,
or contesting a claim requires decided_by_actor_id to be the single
seeded recognition-authority actor, 'cdp_identity_recognition_authority'
(db/ddl/010-identity-and-attestation.sql, cdp/core/services.py's
_decide_identity_claim). Tests below use that literal, pre-seeded actor_id
rather than registering an arbitrary actor for the role -- an arbitrary
registered actor is exactly what must now be rejected, covered by
test_recognition_by_unauthorized_actor_is_rejected and
test_recognition_authority_cannot_decide_its_own_claim below.

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

# Pre-seeded by 010-identity-and-attestation.sql; not registered by these
# tests. See the module docstring above.
RECOGNITION_AUTHORITY_ACTOR_ID = "cdp_identity_recognition_authority"


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
                decided_by_actor_id=RECOGNITION_AUTHORITY_ACTOR_ID,
                rationale="Evidence checked out.",
            )
        )

        recognized = result["identity_claim"]
        self.assertEqual(recognized["recognition_status"], "recognized")
        self.assertEqual(recognized["recognized_by_actor_id"], RECOGNITION_AUTHORITY_ACTOR_ID)
        self.assertEqual(recognized["recognition_rationale"], "Evidence checked out.")
        self.assertIsNotNone(recognized["decided_at"])

    def test_recognition_by_unauthorized_actor_is_rejected(self) -> None:
        """An arbitrary registered actor -- not the seeded recognition
        authority -- must not be able to produce a binding recognition
        decision. This is the ambient-recognition gap the v0.2 review
        correction closes."""
        from cdp.core.services import (
            IdentityClaimDecisionInput,
            IdentityClaimInput,
            RecognitionAuthorityRequired,
            recognize_identity_claim,
            submit_identity_claim,
        )

        actor_id = _register_actor("iaa-claim-unauth-subject")
        unrelated_actor_id = _register_actor("iaa-claim-unauth-decider")
        claim = submit_identity_claim(
            IdentityClaimInput(
                actor_id=actor_id,
                claimant_actor_id=actor_id,
                claimed_identity_descriptor="Should not be recognizable by just anyone.",
                purpose_scope="decision_creation",
            )
        )["identity_claim"]

        with self.assertRaises(RecognitionAuthorityRequired):
            recognize_identity_claim(
                IdentityClaimDecisionInput(
                    claim_id=claim["claim_id"],
                    decided_by_actor_id=unrelated_actor_id,
                    rationale="I say it's fine.",
                )
            )

        with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
            cursor.execute(
                "SELECT recognition_status FROM cdp_core.identity_claim WHERE claim_id = %s",
                (claim["claim_id"],),
            )
            self.assertEqual(cursor.fetchone()["recognition_status"], "pending")

    def test_claimant_cannot_recognize_their_own_claim(self) -> None:
        """The claimant registering as decided_by_actor_id for their own
        claim is rejected by the authority check alone (the claimant is
        never the seeded authority) -- covered here as the concrete
        "self-recognition" scenario the review explicitly asked to see
        proven, distinct from an unrelated third party."""
        from cdp.core.services import (
            IdentityClaimDecisionInput,
            IdentityClaimInput,
            RecognitionAuthorityRequired,
            recognize_identity_claim,
            submit_identity_claim,
        )

        actor_id = _register_actor("iaa-claim-self-recognize")
        claim = submit_identity_claim(
            IdentityClaimInput(
                actor_id=actor_id,
                claimant_actor_id=actor_id,
                claimed_identity_descriptor="Self-submitted, should not self-recognize.",
                purpose_scope="decision_creation",
            )
        )["identity_claim"]

        with self.assertRaises(RecognitionAuthorityRequired):
            recognize_identity_claim(
                IdentityClaimDecisionInput(
                    claim_id=claim["claim_id"],
                    decided_by_actor_id=actor_id,
                    rationale="I recognize myself.",
                )
            )

    def test_recognition_authority_cannot_decide_its_own_claim(self) -> None:
        """Even the seeded recognition authority is forbidden from deciding
        a claim where it is itself the claim's actor or claimant --
        SelfRecognitionForbidden is independently reachable and
        load-bearing, not merely implied by the authority check."""
        from cdp.core.services import (
            IdentityClaimDecisionInput,
            IdentityClaimInput,
            SelfRecognitionForbidden,
            recognize_identity_claim,
            submit_identity_claim,
        )

        claim = submit_identity_claim(
            IdentityClaimInput(
                actor_id=RECOGNITION_AUTHORITY_ACTOR_ID,
                claimant_actor_id=RECOGNITION_AUTHORITY_ACTOR_ID,
                claimed_identity_descriptor="The authority's own claim about itself.",
                purpose_scope="decision_creation",
            )
        )["identity_claim"]

        with self.assertRaises(SelfRecognitionForbidden):
            recognize_identity_claim(
                IdentityClaimDecisionInput(
                    claim_id=claim["claim_id"],
                    decided_by_actor_id=RECOGNITION_AUTHORITY_ACTOR_ID,
                    rationale="I recognize myself.",
                )
            )

    def test_deny_claim_preserves_the_row_it_does_not_erase_it(self) -> None:
        from cdp.core.services import (
            IdentityClaimDecisionInput,
            IdentityClaimInput,
            deny_identity_claim,
            submit_identity_claim,
        )

        actor_id = _register_actor("iaa-claim-deny")
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
                decided_by_actor_id=RECOGNITION_AUTHORITY_ACTOR_ID,
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
                claim_id=claim["claim_id"],
                decided_by_actor_id=RECOGNITION_AUTHORITY_ACTOR_ID,
                rationale="No.",
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
                claim_id=claim["claim_id"],
                decided_by_actor_id=RECOGNITION_AUTHORITY_ACTOR_ID,
                rationale="Looked fine.",
            )
        )

        result = contest_identity_claim(
            IdentityClaimDecisionInput(
                claim_id=claim["claim_id"],
                decided_by_actor_id=RECOGNITION_AUTHORITY_ACTOR_ID,
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
                claim_id=claim["claim_id"],
                decided_by_actor_id=RECOGNITION_AUTHORITY_ACTOR_ID,
                rationale="No.",
            )
        )

        with self.assertRaises(IdentityClaimNotDecidable):
            deny_identity_claim(
                IdentityClaimDecisionInput(
                    claim_id=claim["claim_id"],
                    decided_by_actor_id=RECOGNITION_AUTHORITY_ACTOR_ID,
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
                decided_by_actor_id=RECOGNITION_AUTHORITY_ACTOR_ID,
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

    def test_submit_claim_with_registry_and_class_scope_persists_both(self) -> None:
        from cdp.core.services import IdentityClaimInput, submit_identity_claim

        actor_id = _register_actor("iaa-claim-scoped")
        claim = submit_identity_claim(
            IdentityClaimInput(
                actor_id=actor_id,
                claimant_actor_id=actor_id,
                claimed_identity_descriptor="Scoped claim.",
                purpose_scope="decision_creation",
                scope_registry_name="sample_attorney_demo",
                scope_decision_class_id="claim_approval",
            )
        )["identity_claim"]

        self.assertEqual(claim["scope_registry_name"], "sample_attorney_demo")
        self.assertEqual(claim["scope_decision_class_id"], "claim_approval")

    def test_submit_claim_with_registry_scope_and_no_class_scope_is_a_wildcard(self) -> None:
        from cdp.core.services import IdentityClaimInput, submit_identity_claim

        actor_id = _register_actor("iaa-claim-wildcard")
        claim = submit_identity_claim(
            IdentityClaimInput(
                actor_id=actor_id,
                claimant_actor_id=actor_id,
                claimed_identity_descriptor="Registry-wide claim.",
                purpose_scope="decision_creation",
                scope_registry_name="sample_attorney_demo",
            )
        )["identity_claim"]

        self.assertEqual(claim["scope_registry_name"], "sample_attorney_demo")
        self.assertIsNone(claim["scope_decision_class_id"])

    def test_submit_claim_without_scope_fields_leaves_both_null(self) -> None:
        from cdp.core.services import IdentityClaimInput, submit_identity_claim

        actor_id = _register_actor("iaa-claim-unscoped")
        claim = submit_identity_claim(
            IdentityClaimInput(
                actor_id=actor_id,
                claimant_actor_id=actor_id,
                claimed_identity_descriptor="Unscoped claim, purpose_scope only.",
                purpose_scope="decision_creation",
            )
        )["identity_claim"]

        self.assertIsNone(claim["scope_registry_name"])
        self.assertIsNone(claim["scope_decision_class_id"])

    def test_submit_claim_with_class_scope_but_no_registry_scope_is_rejected(self) -> None:
        from cdp.core.services import IdentityClaimInput, submit_identity_claim

        actor_id = _register_actor("iaa-claim-badscope")
        with self.assertRaises(psycopg.errors.CheckViolation):
            submit_identity_claim(
                IdentityClaimInput(
                    actor_id=actor_id,
                    claimant_actor_id=actor_id,
                    claimed_identity_descriptor="Should be rejected by the DB CHECK.",
                    purpose_scope="decision_creation",
                    scope_decision_class_id="claim_approval",
                )
            )


if __name__ == "__main__":
    unittest.main()
