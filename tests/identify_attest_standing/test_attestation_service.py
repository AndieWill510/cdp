"""Integration tests for attest_and_create_decision (RFC-CDP-031 Attest
Protocol), the Identity and Attestation slice's proof path: attest a
decision-creation act to an actor holding a recognized, in-scope identity
claim, then create the decision -- all inside one transaction.

Require CDP_TEST_DATABASE_URL pointing at a database with
001, 003, 004, and 010 already applied, and 004's
nemawashi_default_v1 -> sample_attorney_demo.claim_approval workflow
configured.

Cleanup note: a decision created through the happy path here gets a
permanent cdp_core.attestation_record row FK'd to it, so (unlike
tests/decision/test_decision_service.py) its decision_registry /
workflow_instance / workflow_task rows cannot be cleaned up afterward
either -- deleting them would violate that foreign key. Failure-path tests
below never reach decision creation (verification fails first, inside the
same rolled-back transaction), so there is nothing to clean up for those.
See test_actor_service.py's module docstring for the same reasoning
applied to actor/identity_claim rows.

v0.2 review correction: attestation_input.actor_id (the attestor -- who
performed the governed act) is no longer required to equal
decision_input.subject_actor_id (who/what the decision is about). See
test_attestor_and_subject_may_independently_differ_and_both_are_preserved
below, which is the proof path the review asked for: Alice attests, the
decision concerns Bob, neither identity collapses into the other. Claim
recognition below uses the seeded recognition-authority actor_id (see
test_identity_claim_service.py's module docstring) rather than an
arbitrary registered actor.
"""

from __future__ import annotations

import os
import unittest
import uuid
from datetime import UTC, datetime
from unittest import mock

import psycopg
from psycopg.rows import dict_row

REGISTRY_NAME = "sample_attorney_demo"
DECISION_CLASS_ID = "claim_approval"

# Pre-seeded by 010-identity-and-attestation.sql; not registered by these
# tests. See test_identity_claim_service.py's module docstring.
RECOGNITION_AUTHORITY_ACTOR_ID = "cdp_identity_recognition_authority"


def _database_url() -> str:
    return os.environ.get("CDP_TEST_DATABASE_URL", "postgresql://cdp:cdp@localhost:5432/cdp")


def _attestation_table_exists() -> bool:
    with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
        cursor.execute("SELECT to_regclass('cdp_core.attestation_record')")
        return cursor.fetchone()[0] is not None


def _decision_workflow_configured() -> bool:
    with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT 1
            FROM cdp_core.workflow_definition
            WHERE workflow_code = 'nemawashi_default_v1'
              AND workflow_version = 'v1'
              AND applies_to_registry_name = %s
              AND applies_to_decision_class_id = %s
              AND status = 'active'
            """,
            (REGISTRY_NAME, DECISION_CLASS_ID),
        )
        return cursor.fetchone() is not None


def _unique(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def _register_actor(prefix: str, **overrides):
    from cdp.core.services import ActorInput, register_actor

    actor_id = _unique(prefix)
    kwargs = {"actor_id": actor_id, "actor_type": "human", "display_label": prefix, **overrides}
    register_actor(ActorInput(**kwargs))
    return actor_id


def _submit_and_recognize_claim(actor_id: str, *, purpose_scope: str = "decision_creation"):
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
            claimed_identity_descriptor="Continuity for attestation tests.",
            purpose_scope=purpose_scope,
        )
    )["identity_claim"]
    recognize_identity_claim(
        IdentityClaimDecisionInput(
            claim_id=claim["claim_id"],
            decided_by_actor_id=RECOGNITION_AUTHORITY_ACTOR_ID,
            rationale="Checked.",
        )
    )
    return claim["claim_id"]


def _make_decision_input(decision_id: str, subject_actor_id: str):
    from cdp.core.services import DecisionInput

    return DecisionInput(
        registry_name=REGISTRY_NAME,
        decision_id=decision_id,
        decision_class_id=DECISION_CLASS_ID,
        antecedent_text="Attestation-slice integration test decision.",
        subject_actor_type="human",
        subject_actor_id=subject_actor_id,
        predicate_verb="recommend_approval",
        object_type="claim",
        object_id="claim_9981",
        permission_source_type="policy_rule",
        permission_source_id="policy_claims_approval_v2",
        human_required=True,
    )


def _make_attestation_input(actor_id: str, claim_id):
    from cdp.core.services import AttestationInput

    return AttestationInput(
        actor_id=actor_id,
        identity_claim_id=claim_id,
        attestation_method="shared_secret_reference",
        credential_reference="test-harness-credential-ref-1",
        issued_at=datetime.now(UTC),
    )


def _decision_row_count(registry_name: str, decision_id: str) -> int:
    with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
        cursor.execute(
            "SELECT count(*) AS n FROM cdp_core.decision_registry "
            "WHERE registry_name = %s AND decision_id = %s",
            (registry_name, decision_id),
        )
        return cursor.fetchone()["n"]


@unittest.skipUnless(os.environ.get("CDP_TEST_DATABASE_URL"), "set CDP_TEST_DATABASE_URL to run")
class AttestAndCreateDecisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ.setdefault("DATABASE_URL", _database_url())
        if not _attestation_table_exists():
            raise unittest.SkipTest(
                "010-identity-and-attestation.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )
        if not _decision_workflow_configured():
            raise unittest.SkipTest(
                "004-decision-class-workflow-seed.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )

    def test_happy_path_attests_and_creates_decision_with_immutable_attribution(self) -> None:
        from cdp.core.services import AttestedDecisionInput, attest_and_create_decision

        actor_id = _register_actor("iaa-attest-happy")
        claim_id = _submit_and_recognize_claim(actor_id)
        decision_id = _unique("iaa-attested-decision")

        result = attest_and_create_decision(
            AttestedDecisionInput(
                decision_input=_make_decision_input(decision_id, actor_id),
                attestation_input=_make_attestation_input(actor_id, claim_id),
            )
        )

        self.assertEqual(result["decision"]["decision_id"], decision_id)
        self.assertEqual(result["decision"]["subject_actor_id"], actor_id)
        attestation = result["attestation"]
        self.assertEqual(attestation["actor_id"], actor_id)
        self.assertEqual(attestation["verification_result"], "verified")
        self.assertEqual(attestation["governed_act_decision_id"], decision_id)

        with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
            cursor.execute(
                "SELECT actor_id, identity_claim_id, verification_result "
                "FROM cdp_core.attestation_record "
                "WHERE governed_act_registry_name = %s AND governed_act_decision_id = %s",
                (REGISTRY_NAME, decision_id),
            )
            row = cursor.fetchone()
            self.assertEqual(row["actor_id"], actor_id)
            self.assertEqual(row["identity_claim_id"], claim_id)
            self.assertEqual(row["verification_result"], "verified")

            cursor.execute(
                "SELECT event_type FROM cdp_audit.event_log "
                "WHERE payload ->> 'registry_name' = %s AND payload ->> 'decision_id' = %s "
                "ORDER BY event_sequence",
                (REGISTRY_NAME, decision_id),
            )
            event_types = [row["event_type"] for row in cursor.fetchall()]
            self.assertEqual(
                event_types,
                ["decision.created", "workflow.started", "task.created", "attestation.recorded"],
            )

    def test_unknown_actor_fails_closed_and_nothing_is_persisted(self) -> None:
        from cdp.core.services import ActorNotFound, AttestedDecisionInput, attest_and_create_decision

        unknown_actor_id = _unique("iaa-attest-unknown")
        decision_id = _unique("iaa-attested-decision-unknown")

        with self.assertRaises(ActorNotFound):
            attest_and_create_decision(
                AttestedDecisionInput(
                    decision_input=_make_decision_input(decision_id, unknown_actor_id),
                    attestation_input=_make_attestation_input(
                        unknown_actor_id, uuid.uuid4()
                    ),
                )
            )
        self.assertEqual(_decision_row_count(REGISTRY_NAME, decision_id), 0)

    def test_inactive_actor_fails_closed(self) -> None:
        from cdp.core.services import ActorNotActive, AttestedDecisionInput, attest_and_create_decision

        actor_id = _register_actor("iaa-attest-inactive")
        claim_id = _submit_and_recognize_claim(actor_id)
        with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
            cursor.execute(
                "UPDATE cdp_core.actor SET actor_status = 'suspended' WHERE actor_id = %s",
                (actor_id,),
            )
            conn.commit()
        decision_id = _unique("iaa-attested-decision-inactive")

        with self.assertRaises(ActorNotActive):
            attest_and_create_decision(
                AttestedDecisionInput(
                    decision_input=_make_decision_input(decision_id, actor_id),
                    attestation_input=_make_attestation_input(actor_id, claim_id),
                )
            )
        self.assertEqual(_decision_row_count(REGISTRY_NAME, decision_id), 0)

    def test_attestor_and_subject_may_independently_differ_and_both_are_preserved(self) -> None:
        """The proof path the v0.2 review asked for: Alice (the attestor,
        who performed the governed act) attests a decision whose subject
        is Bob (an entirely different actor, e.g. a patient or claimant).
        Neither identity collapses into the other -- Alice remains
        immutably attributable as the attestor via
        cdp_core.attestation_record.actor_id, and Bob remains the
        decision's subject via cdp_core.decision_registry.subject_actor_id,
        unaffected by (and not required to hold) any identity claim of his
        own."""
        from cdp.core.services import AttestedDecisionInput, attest_and_create_decision

        alice_actor_id = _register_actor("iaa-attest-alice")
        bob_actor_id = _register_actor("iaa-attest-bob")
        alice_claim_id = _submit_and_recognize_claim(alice_actor_id)
        decision_id = _unique("iaa-attested-decision-distinct-roles")

        result = attest_and_create_decision(
            AttestedDecisionInput(
                decision_input=_make_decision_input(decision_id, bob_actor_id),
                attestation_input=_make_attestation_input(alice_actor_id, alice_claim_id),
            )
        )

        self.assertEqual(result["decision"]["subject_actor_id"], bob_actor_id)
        self.assertEqual(result["attestation"]["actor_id"], alice_actor_id)

        with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
            cursor.execute(
                "SELECT subject_actor_id FROM cdp_core.decision_registry "
                "WHERE registry_name = %s AND decision_id = %s",
                (REGISTRY_NAME, decision_id),
            )
            self.assertEqual(cursor.fetchone()["subject_actor_id"], bob_actor_id)

            cursor.execute(
                "SELECT actor_id FROM cdp_core.attestation_record "
                "WHERE governed_act_registry_name = %s AND governed_act_decision_id = %s",
                (REGISTRY_NAME, decision_id),
            )
            self.assertEqual(cursor.fetchone()["actor_id"], alice_actor_id)

    def test_unrecognized_claim_fails_closed(self) -> None:
        from cdp.core.services import (
            AttestedDecisionInput,
            IdentityClaimInput,
            IdentityClaimNotRecognized,
            attest_and_create_decision,
            submit_identity_claim,
        )

        actor_id = _register_actor("iaa-attest-unrecognized")
        claim_id = submit_identity_claim(
            IdentityClaimInput(
                actor_id=actor_id,
                claimant_actor_id=actor_id,
                claimed_identity_descriptor="Never recognized.",
                purpose_scope="decision_creation",
            )
        )["identity_claim"]["claim_id"]
        decision_id = _unique("iaa-attested-decision-unrecognized")

        with self.assertRaises(IdentityClaimNotRecognized):
            attest_and_create_decision(
                AttestedDecisionInput(
                    decision_input=_make_decision_input(decision_id, actor_id),
                    attestation_input=_make_attestation_input(actor_id, claim_id),
                )
            )
        self.assertEqual(_decision_row_count(REGISTRY_NAME, decision_id), 0)

    def test_wrong_scope_claim_fails_closed(self) -> None:
        from cdp.core.services import (
            AttestedDecisionInput,
            IdentityClaimScopeInsufficient,
            attest_and_create_decision,
        )

        actor_id = _register_actor("iaa-attest-wrongscope")
        claim_id = _submit_and_recognize_claim(actor_id, purpose_scope="some_other_purpose")
        decision_id = _unique("iaa-attested-decision-wrongscope")

        with self.assertRaises(IdentityClaimScopeInsufficient):
            attest_and_create_decision(
                AttestedDecisionInput(
                    decision_input=_make_decision_input(decision_id, actor_id),
                    attestation_input=_make_attestation_input(actor_id, claim_id),
                )
            )
        self.assertEqual(_decision_row_count(REGISTRY_NAME, decision_id), 0)

    def test_claim_belonging_to_a_different_actor_fails_closed(self) -> None:
        from cdp.core.services import (
            AttestedDecisionInput,
            IdentityClaimActorMismatch,
            attest_and_create_decision,
        )

        actor_id = _register_actor("iaa-attest-claimowner")
        other_actor_id = _register_actor("iaa-attest-claimborrower")
        claim_id = _submit_and_recognize_claim(actor_id)
        decision_id = _unique("iaa-attested-decision-claimmismatch")

        with self.assertRaises(IdentityClaimActorMismatch):
            attest_and_create_decision(
                AttestedDecisionInput(
                    decision_input=_make_decision_input(decision_id, other_actor_id),
                    attestation_input=_make_attestation_input(other_actor_id, claim_id),
                )
            )
        self.assertEqual(_decision_row_count(REGISTRY_NAME, decision_id), 0)

    def test_downstream_failure_rolls_back_the_whole_transaction(self) -> None:
        from cdp.core.services import AttestedDecisionInput, attest_and_create_decision

        actor_id = _register_actor("iaa-attest-rollback")
        claim_id = _submit_and_recognize_claim(actor_id)
        decision_id = _unique("iaa-attested-decision-rollback")

        with mock.patch(
            "cdp.core.services.attestations_repo.insert_attestation",
            side_effect=RuntimeError("forced failure after decision creation"),
        ):
            with self.assertRaises(RuntimeError):
                attest_and_create_decision(
                    AttestedDecisionInput(
                        decision_input=_make_decision_input(decision_id, actor_id),
                        attestation_input=_make_attestation_input(actor_id, claim_id),
                    )
                )

        self.assertEqual(
            _decision_row_count(REGISTRY_NAME, decision_id),
            0,
            "decision should not survive rollback even though it was inserted mid-transaction",
        )
        with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
            cursor.execute(
                "SELECT count(*) AS n FROM cdp_audit.event_log "
                "WHERE payload ->> 'registry_name' = %s AND payload ->> 'decision_id' = %s",
                (REGISTRY_NAME, decision_id),
            )
            self.assertEqual(cursor.fetchone()["n"], 0, "no audit event should survive rollback")


if __name__ == "__main__":
    unittest.main()
