"""Integration tests for the Standing slice (RFC-CDP-033), scoped to
Constitutional Affected-Party Standing for the Challenge stage only.

Require CDP_TEST_DATABASE_URL pointing at a database with
001-decision-registry-kernel.sql through 015-standing-and-recusal.sql
already applied.

Recognition-authority-style discipline: only the single seeded
`cdp_standing_recognition_authority` actor may recognize or deny a
standing claim -- mirrors identity_claim's / authority_grant's own
discipline, tested the same way as
tests/identify_attest_standing/test_identity_claim_service.py and
tests/authority/test_authority_grant_service.py.

No 'narrowed' outcome is reachable in this slice, deliberately (review
finding on PR #53) -- see cdp/core/services.py's comment next to
recognize_standing_claim for why.

Cleanup note: cdp_core.standing_claim and
cdp_core.standing_recognition_determination rows cannot be deleted or
updated (015 enforces both at the database level) -- see
tests/identify_attest_standing/test_actor_service.py's module docstring
for the same reasoning applied there. Tests use uuid-suffixed
identifiers.
"""

from __future__ import annotations

import os
import unittest
import uuid
from datetime import UTC, datetime, timedelta

import psycopg

REGISTRY_NAME = "sample_attorney_demo"
DECISION_CLASS_ID = "claim_approval"

# Pre-seeded by 015-standing-and-recusal.sql; not registered by these tests.
STANDING_AUTHORITY_ACTOR_ID = "cdp_standing_recognition_authority"

# Pre-seeded by 010/011; used to grant the identity/authority preconditions
# a Standing-gated challenge needs.
IDENTITY_RECOGNITION_AUTHORITY_ACTOR_ID = "cdp_identity_recognition_authority"
AUTHORITY_GRANT_ISSUER_ACTOR_ID = "cdp_authority_grant_issuer"


def _database_url() -> str:
    return os.environ.get("CDP_TEST_DATABASE_URL", "postgresql://cdp:cdp@localhost:5432/cdp")


def _standing_claim_table_exists() -> bool:
    with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
        cursor.execute("SELECT to_regclass('cdp_core.standing_claim')")
        return cursor.fetchone()[0] is not None


def _unique(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def _register_actor(prefix: str, **overrides):
    from cdp.core.services import ActorInput, register_actor

    actor_id = _unique(prefix)
    kwargs = {"actor_id": actor_id, "actor_type": "human", "display_label": prefix, **overrides}
    register_actor(ActorInput(**kwargs))
    return actor_id


def _make_decision(prefix: str) -> str:
    from cdp.core.services import DecisionInput, create_decision_with_workflow

    decision_id = _unique(prefix)
    create_decision_with_workflow(
        DecisionInput(
            registry_name=REGISTRY_NAME,
            decision_id=decision_id,
            decision_class_id=DECISION_CLASS_ID,
            antecedent_text="Standing slice integration test decision.",
            subject_actor_type="agent",
            subject_actor_id="claims_review_agent",
            predicate_verb="recommend_approval",
            object_type="claim",
            object_id="claim_9981",
            permission_source_type="policy_rule",
            permission_source_id="policy_claims_approval_v2",
            human_required=True,
        )
    )
    return decision_id


def _make_recognized_identity_claim(actor_id: str) -> uuid.UUID:
    from cdp.core.services import (
        IdentityClaimDecisionInput,
        IdentityClaimInput,
        recognize_identity_claim,
        submit_identity_claim,
    )

    claim = submit_identity_claim(
        IdentityClaimInput(
            actor_id=actor_id,
            claimant_actor_id=actor_id,
            claimed_identity_descriptor="self",
            purpose_scope="challenge_raising",
        )
    )["identity_claim"]
    recognize_identity_claim(
        IdentityClaimDecisionInput(
            claim_id=claim["claim_id"],
            decided_by_actor_id=IDENTITY_RECOGNITION_AUTHORITY_ACTOR_ID,
            rationale="Test fixture recognition.",
        )
    )
    return claim["claim_id"]


def _grant_challenge_authority(actor_id: str) -> None:
    from cdp.core.services import GrantAuthorityInput, grant_authority

    grant_authority(
        GrantAuthorityInput(
            actor_id=actor_id,
            authority="CHALLENGE",
            scope_registry_name=REGISTRY_NAME,
            scope_decision_class_id=DECISION_CLASS_ID,
            expires_at=datetime.now(UTC) + timedelta(days=1),
            issued_by_actor_id=AUTHORITY_GRANT_ISSUER_ACTOR_ID,
            basis="policy",
        )
    )


def _make_claim_input(decision_id: str, actor_id: str, **overrides):
    from cdp.core.services import StandingClaimInput

    kwargs = {
        "decision_registry_name": REGISTRY_NAME,
        "decision_id": decision_id,
        "actor_id": actor_id,
        "claimed_impact": "This decision may materially affect me.",
        "standing_basis_contextual_relationship": "Adjacent property owner.",
        **overrides,
    }
    return StandingClaimInput(**kwargs)


@unittest.skipUnless(os.environ.get("CDP_TEST_DATABASE_URL"), "set CDP_TEST_DATABASE_URL to run")
class StandingClaimTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ.setdefault("DATABASE_URL", _database_url())
        if not _standing_claim_table_exists():
            raise unittest.SkipTest(
                "015-standing-and-recusal.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )

    def test_happy_path_submits_provisional_claim(self) -> None:
        from cdp.core.services import submit_affected_party_standing_claim

        actor_id = _register_actor("standing-claim-happy")
        decision_id = _make_decision("standing-decision-happy")

        result = submit_affected_party_standing_claim(_make_claim_input(decision_id, actor_id))
        claim = result["standing_claim"]
        self.assertEqual(claim["actor_id"], actor_id)
        self.assertEqual(claim["decision_id"], decision_id)
        self.assertEqual(claim["stage"], "challenge")
        self.assertEqual(claim["standing_type"], "constitutional_affected_party")

        with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
            cursor.execute(
                "SELECT event_type FROM cdp_audit.event_log "
                "WHERE aggregate_type = 'standing_claim' AND aggregate_id = %s "
                "ORDER BY event_sequence",
                (str(claim["claim_id"]),),
            )
            event_types = [row[0] for row in cursor.fetchall()]
            self.assertEqual(event_types, ["standing_claim.submitted"])

    def test_claim_missing_basis_and_impact_fails_closed(self) -> None:
        from cdp.core.services import StandingClaimInput, submit_affected_party_standing_claim

        actor_id = _register_actor("standing-claim-insufficient")
        decision_id = _make_decision("standing-decision-insufficient")

        with self.assertRaises(psycopg.errors.CheckViolation):
            submit_affected_party_standing_claim(
                StandingClaimInput(
                    decision_registry_name=REGISTRY_NAME,
                    decision_id=decision_id,
                    actor_id=actor_id,
                    claimed_impact="I might be affected somehow.",
                )
            )

    def test_claim_for_unknown_actor_fails(self) -> None:
        from cdp.core.services import ActorNotFound, submit_affected_party_standing_claim

        decision_id = _make_decision("standing-decision-unknown-actor")
        unknown_actor_id = _unique("standing-claim-unknown-actor")

        with self.assertRaises(ActorNotFound):
            submit_affected_party_standing_claim(
                _make_claim_input(decision_id, unknown_actor_id)
            )

    def test_claim_for_unknown_decision_fails(self) -> None:
        from cdp.core.services import DecisionNotFound, submit_affected_party_standing_claim

        actor_id = _register_actor("standing-claim-unknown-decision")

        with self.assertRaises(DecisionNotFound):
            submit_affected_party_standing_claim(
                _make_claim_input(_unique("nonexistent-decision"), actor_id)
            )

    def test_unsupported_stage_rejected(self) -> None:
        from cdp.core.services import (
            StandingStageNotSupported,
            submit_affected_party_standing_claim,
        )

        actor_id = _register_actor("standing-claim-bad-stage")
        decision_id = _make_decision("standing-decision-bad-stage")

        with self.assertRaises(StandingStageNotSupported):
            submit_affected_party_standing_claim(
                _make_claim_input(decision_id, actor_id, stage="adjudicate")
            )

    def test_unsupported_standing_type_rejected(self) -> None:
        from cdp.core.services import StandingTypeNotSupported, submit_affected_party_standing_claim

        actor_id = _register_actor("standing-claim-bad-type")
        decision_id = _make_decision("standing-decision-bad-type")

        with self.assertRaises(StandingTypeNotSupported):
            submit_affected_party_standing_claim(
                _make_claim_input(
                    decision_id, actor_id, standing_type="constitutional_evidence_custodian"
                )
            )

    def test_recognize_happy_path(self) -> None:
        from cdp.core.services import (
            StandingDeterminationInput,
            recognize_standing_claim,
            submit_affected_party_standing_claim,
        )

        actor_id = _register_actor("standing-claim-recognize")
        decision_id = _make_decision("standing-decision-recognize")
        claim = submit_affected_party_standing_claim(
            _make_claim_input(decision_id, actor_id)
        )["standing_claim"]

        result = recognize_standing_claim(
            StandingDeterminationInput(
                claim_id=claim["claim_id"],
                determined_by_actor_id=STANDING_AUTHORITY_ACTOR_ID,
                outcome_basis="Confirmed adjacency.",
            )
        )
        determination = result["standing_recognition_determination"]
        self.assertEqual(determination["outcome"], "recognized")
        self.assertEqual(determination["claim_id"], claim["claim_id"])

    def test_narrow_standing_claim_does_not_exist(self) -> None:
        """narrow_standing_claim was removed after PR #53 review: this
        table has no outcome_scope column to record what a narrowing
        narrows to, so writing 'narrowed' would be enforcement-
        indistinguishable from 'recognized' while still asserting
        something the system cannot describe. Pinned here so
        reintroducing it is a deliberate decision, not an accident -- see
        the comment next to recognize_standing_claim in
        cdp/core/services.py."""
        import cdp.core.services as services

        self.assertFalse(hasattr(services, "narrow_standing_claim"))

    def test_narrowed_outcome_rejected_by_the_database(self) -> None:
        """'narrowed' remains seeded in the standing_recognition_outcome
        vocabulary (for a future session that adds outcome_scope) but
        cdp_core.standing_recognition_determination's own CHECK constraint
        rejects it directly -- not merely omitted at the service layer."""
        from cdp.core.services import submit_affected_party_standing_claim

        actor_id = _register_actor("standing-claim-narrow-db-reject")
        decision_id = _make_decision("standing-decision-narrow-db-reject")
        claim = submit_affected_party_standing_claim(
            _make_claim_input(decision_id, actor_id)
        )["standing_claim"]

        with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
            with self.assertRaises(psycopg.errors.CheckViolation):
                cursor.execute(
                    "INSERT INTO cdp_core.standing_recognition_determination "
                    "(claim_id, outcome, outcome_basis, determined_by_actor_id) "
                    "VALUES (%s, 'narrowed', 'test', %s)",
                    (claim["claim_id"], STANDING_AUTHORITY_ACTOR_ID),
                )
            conn.rollback()

    def test_deny_happy_path(self) -> None:
        from cdp.core.services import (
            StandingDeterminationInput,
            deny_standing_claim,
            submit_affected_party_standing_claim,
        )

        actor_id = _register_actor("standing-claim-deny")
        decision_id = _make_decision("standing-decision-deny")
        claim = submit_affected_party_standing_claim(
            _make_claim_input(decision_id, actor_id)
        )["standing_claim"]

        result = deny_standing_claim(
            StandingDeterminationInput(
                claim_id=claim["claim_id"],
                determined_by_actor_id=STANDING_AUTHORITY_ACTOR_ID,
                outcome_basis="No consequence shown on review.",
            )
        )
        self.assertEqual(result["standing_recognition_determination"]["outcome"], "denied")

    def test_self_determination_forbidden(self) -> None:
        """Even the seeded Standing recognition authority is forbidden
        from determining a claim where it is itself the claimant --
        SelfStandingRecognitionForbidden is independently reachable and
        load-bearing, not merely implied by the authority check (which an
        arbitrary, non-authority actor determining its own claim would hit
        first -- see test_determination_by_unauthorized_actor_forbidden)."""
        from cdp.core.services import (
            SelfStandingRecognitionForbidden,
            StandingDeterminationInput,
            recognize_standing_claim,
            submit_affected_party_standing_claim,
        )

        decision_id = _make_decision("standing-decision-self-determine")
        claim = submit_affected_party_standing_claim(
            _make_claim_input(decision_id, STANDING_AUTHORITY_ACTOR_ID)
        )["standing_claim"]

        with self.assertRaises(SelfStandingRecognitionForbidden):
            recognize_standing_claim(
                StandingDeterminationInput(
                    claim_id=claim["claim_id"],
                    determined_by_actor_id=STANDING_AUTHORITY_ACTOR_ID,
                    outcome_basis="I recognize my own claim.",
                )
            )

    def test_determination_by_unauthorized_actor_forbidden(self) -> None:
        from cdp.core.services import (
            StandingDeterminationInput,
            StandingRecognitionAuthorityRequired,
            recognize_standing_claim,
            submit_affected_party_standing_claim,
        )

        actor_id = _register_actor("standing-claim-unauth-subject")
        unrelated_actor_id = _register_actor("standing-claim-unauth-determiner")
        decision_id = _make_decision("standing-decision-unauth")
        claim = submit_affected_party_standing_claim(
            _make_claim_input(decision_id, actor_id)
        )["standing_claim"]

        with self.assertRaises(StandingRecognitionAuthorityRequired):
            recognize_standing_claim(
                StandingDeterminationInput(
                    claim_id=claim["claim_id"],
                    determined_by_actor_id=unrelated_actor_id,
                    outcome_basis="I say so.",
                )
            )

    def test_second_determination_on_same_claim_fails(self) -> None:
        from cdp.core.services import (
            StandingClaimAlreadyDetermined,
            StandingDeterminationInput,
            deny_standing_claim,
            recognize_standing_claim,
            submit_affected_party_standing_claim,
        )

        actor_id = _register_actor("standing-claim-double-determine")
        decision_id = _make_decision("standing-decision-double-determine")
        claim = submit_affected_party_standing_claim(
            _make_claim_input(decision_id, actor_id)
        )["standing_claim"]

        recognize_standing_claim(
            StandingDeterminationInput(
                claim_id=claim["claim_id"],
                determined_by_actor_id=STANDING_AUTHORITY_ACTOR_ID,
                outcome_basis="First determination.",
            )
        )
        with self.assertRaises(StandingClaimAlreadyDetermined):
            deny_standing_claim(
                StandingDeterminationInput(
                    claim_id=claim["claim_id"],
                    determined_by_actor_id=STANDING_AUTHORITY_ACTOR_ID,
                    outcome_basis="Second determination.",
                )
            )

    def test_claim_cannot_be_deleted_or_updated_at_the_database_level(self) -> None:
        from cdp.core.services import submit_affected_party_standing_claim

        actor_id = _register_actor("standing-claim-nodelete")
        decision_id = _make_decision("standing-decision-nodelete")
        claim = submit_affected_party_standing_claim(
            _make_claim_input(decision_id, actor_id)
        )["standing_claim"]

        with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
            with self.assertRaises(psycopg.errors.Error):
                cursor.execute(
                    "DELETE FROM cdp_core.standing_claim WHERE claim_id = %s",
                    (claim["claim_id"],),
                )
            conn.rollback()
            with self.assertRaises(psycopg.errors.Error):
                cursor.execute(
                    "UPDATE cdp_core.standing_claim SET claimed_impact = 'edited' "
                    "WHERE claim_id = %s",
                    (claim["claim_id"],),
                )
            conn.rollback()

    def test_determination_cannot_be_deleted_or_updated_at_the_database_level(self) -> None:
        from cdp.core.services import (
            StandingDeterminationInput,
            recognize_standing_claim,
            submit_affected_party_standing_claim,
        )

        actor_id = _register_actor("standing-determination-nodelete")
        decision_id = _make_decision("standing-decision-determination-nodelete")
        claim = submit_affected_party_standing_claim(
            _make_claim_input(decision_id, actor_id)
        )["standing_claim"]
        determination = recognize_standing_claim(
            StandingDeterminationInput(
                claim_id=claim["claim_id"],
                determined_by_actor_id=STANDING_AUTHORITY_ACTOR_ID,
                outcome_basis="Confirmed.",
            )
        )["standing_recognition_determination"]

        with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
            with self.assertRaises(psycopg.errors.Error):
                cursor.execute(
                    "DELETE FROM cdp_core.standing_recognition_determination "
                    "WHERE determination_id = %s",
                    (determination["determination_id"],),
                )
            conn.rollback()
            with self.assertRaises(psycopg.errors.Error):
                cursor.execute(
                    "UPDATE cdp_core.standing_recognition_determination "
                    "SET outcome_basis = 'edited' WHERE determination_id = %s",
                    (determination["determination_id"],),
                )
            conn.rollback()


@unittest.skipUnless(os.environ.get("CDP_TEST_DATABASE_URL"), "set CDP_TEST_DATABASE_URL to run")
class ProvisionalStandingChallengeGateTests(unittest.TestCase):
    """Proves the load-bearing claim from RFC-CDP-033 SS11.4 (Draft v0.7)
    that this slice implements: a minimally sufficient, still-pending
    affected-party standing claim is sufficient to raise the first
    Challenge, without waiting on binding recognition."""

    @classmethod
    def setUpClass(cls) -> None:
        os.environ.setdefault("DATABASE_URL", _database_url())
        if not _standing_claim_table_exists():
            raise unittest.SkipTest(
                "015-standing-and-recusal.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )

    def _prepare_challenger(self, prefix: str) -> tuple[str, uuid.UUID, str]:
        actor_id = _register_actor(prefix)
        decision_id = _make_decision(f"{prefix}-decision")
        identity_claim_id = _make_recognized_identity_claim(actor_id)
        _grant_challenge_authority(actor_id)
        return actor_id, identity_claim_id, decision_id

    def _attest_and_raise(
        self, *, actor_id: str, identity_claim_id: uuid.UUID, decision_id: str, standing_claim_id
    ):
        from cdp.core.services import (
            AttestationInput,
            AttestedChallengeInput,
            ChallengeInput,
            attest_and_raise_challenge,
        )

        return attest_and_raise_challenge(
            AttestedChallengeInput(
                challenge_input=ChallengeInput(
                    registry_name=REGISTRY_NAME,
                    decision_id=decision_id,
                    raised_by_actor_id=actor_id,
                    challenge_text="I object as an affected party.",
                ),
                attestation_input=AttestationInput(
                    actor_id=actor_id,
                    identity_claim_id=identity_claim_id,
                    attestation_method="shared_secret_reference",
                    credential_reference=_unique("cred"),
                    issued_at=datetime.now(UTC),
                ),
                standing_claim_id=standing_claim_id,
            )
        )

    def test_pending_minimally_sufficient_claim_permits_challenge(self) -> None:
        from cdp.core.services import submit_affected_party_standing_claim

        actor_id, identity_claim_id, decision_id = self._prepare_challenger(
            "standing-gate-provisional"
        )
        standing_claim = submit_affected_party_standing_claim(
            _make_claim_input(decision_id, actor_id)
        )["standing_claim"]

        result = self._attest_and_raise(
            actor_id=actor_id,
            identity_claim_id=identity_claim_id,
            decision_id=decision_id,
            standing_claim_id=standing_claim["claim_id"],
        )
        self.assertEqual(result["standing_claim"]["claim_id"], standing_claim["claim_id"])
        self.assertIsNotNone(result["challenge"]["challenge_id"])

        with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
            cursor.execute(
                "SELECT event_type FROM cdp_audit.event_log "
                "WHERE aggregate_type = 'standing_claim' AND aggregate_id = %s "
                "ORDER BY event_sequence",
                (str(standing_claim["claim_id"]),),
            )
            event_types = [row[0] for row in cursor.fetchall()]
            self.assertEqual(event_types, ["standing_claim.submitted", "standing_claim.exercised"])

    def test_recognized_claim_permits_challenge(self) -> None:
        from cdp.core.services import (
            StandingDeterminationInput,
            recognize_standing_claim,
            submit_affected_party_standing_claim,
        )

        actor_id, identity_claim_id, decision_id = self._prepare_challenger(
            "standing-gate-recognized"
        )
        standing_claim = submit_affected_party_standing_claim(
            _make_claim_input(decision_id, actor_id)
        )["standing_claim"]
        recognize_standing_claim(
            StandingDeterminationInput(
                claim_id=standing_claim["claim_id"],
                determined_by_actor_id=STANDING_AUTHORITY_ACTOR_ID,
                outcome_basis="Confirmed.",
            )
        )

        result = self._attest_and_raise(
            actor_id=actor_id,
            identity_claim_id=identity_claim_id,
            decision_id=decision_id,
            standing_claim_id=standing_claim["claim_id"],
        )
        self.assertIsNotNone(result["challenge"]["challenge_id"])

    def test_denied_claim_blocks_challenge(self) -> None:
        from cdp.core.services import (
            StandingClaimNotSufficient,
            StandingDeterminationInput,
            deny_standing_claim,
            submit_affected_party_standing_claim,
        )

        actor_id, identity_claim_id, decision_id = self._prepare_challenger("standing-gate-denied")
        standing_claim = submit_affected_party_standing_claim(
            _make_claim_input(decision_id, actor_id)
        )["standing_claim"]
        deny_standing_claim(
            StandingDeterminationInput(
                claim_id=standing_claim["claim_id"],
                determined_by_actor_id=STANDING_AUTHORITY_ACTOR_ID,
                outcome_basis="No consequence shown.",
            )
        )

        with self.assertRaises(StandingClaimNotSufficient):
            self._attest_and_raise(
                actor_id=actor_id,
                identity_claim_id=identity_claim_id,
                decision_id=decision_id,
                standing_claim_id=standing_claim["claim_id"],
            )

    def test_claim_belonging_to_a_different_actor_is_rejected(self) -> None:
        from cdp.core.services import (
            StandingClaimActorMismatch,
            submit_affected_party_standing_claim,
        )

        actor_id, identity_claim_id, decision_id = self._prepare_challenger(
            "standing-gate-actor-mismatch"
        )
        other_actor_id = _register_actor("standing-gate-other-claimant")
        other_standing_claim = submit_affected_party_standing_claim(
            _make_claim_input(decision_id, other_actor_id)
        )["standing_claim"]

        with self.assertRaises(StandingClaimActorMismatch):
            self._attest_and_raise(
                actor_id=actor_id,
                identity_claim_id=identity_claim_id,
                decision_id=decision_id,
                standing_claim_id=other_standing_claim["claim_id"],
            )

    def test_claim_for_a_different_decision_is_rejected(self) -> None:
        from cdp.core.services import (
            StandingClaimDecisionMismatch,
            submit_affected_party_standing_claim,
        )

        actor_id, identity_claim_id, decision_id = self._prepare_challenger(
            "standing-gate-decision-mismatch"
        )
        other_decision_id = _make_decision("standing-gate-other-decision")
        wrong_decision_claim = submit_affected_party_standing_claim(
            _make_claim_input(other_decision_id, actor_id)
        )["standing_claim"]

        with self.assertRaises(StandingClaimDecisionMismatch):
            self._attest_and_raise(
                actor_id=actor_id,
                identity_claim_id=identity_claim_id,
                decision_id=decision_id,
                standing_claim_id=wrong_decision_claim["claim_id"],
            )

    def test_challenge_without_standing_claim_id_is_unaffected(self) -> None:
        """The Standing gate is opt-in, not mandatory -- see
        attest_and_raise_challenge's docstring. Omitting standing_claim_id
        must behave exactly as it did before this slice existed."""
        actor_id, identity_claim_id, decision_id = self._prepare_challenger(
            "standing-gate-omitted"
        )

        result = self._attest_and_raise(
            actor_id=actor_id,
            identity_claim_id=identity_claim_id,
            decision_id=decision_id,
            standing_claim_id=None,
        )
        self.assertIsNone(result["standing_claim"])
        self.assertIsNotNone(result["challenge"]["challenge_id"])


if __name__ == "__main__":
    unittest.main()
