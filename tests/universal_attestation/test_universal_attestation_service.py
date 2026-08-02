"""Integration tests for the Universal Attestation proof paths (session
029, RFC-CDP-031 SS2): attest_and_raise_challenge,
attest_and_adjudicate_challenge, attest_and_authorize_execution,
attest_and_record_execution_attempt.

Require CDP_TEST_DATABASE_URL pointing at a database with 001, 003, 004,
010, 011, and 012 already applied, and 004's nemawashi_default_v1 ->
sample_attorney_demo.claim_approval workflow configured.

Each function follows the exact shape attest_and_create_decision
established (sessions 027/028): actor active, identity claim recognized
and scoped to that act's own purpose_scope, an active/unexpired grant for
that act's own authority type, then the underlying unattested service
function, then attestation + authority evaluation persisted together. See
cdp/core/services.py's "Universal Attestation" section header for the
full shape and its scope boundary.

Cleanup note: as in tests/identify_attest_standing/test_attestation_service.py,
a decision (and its challenge/adjudication/authorization/execution
sub-records) that gets a permanent attestation_record/
authority_evaluation_result row FK'd to it cannot be cleaned up
afterward -- see that file's module docstring for the same reasoning.
"""

from __future__ import annotations

import os
import unittest
import uuid
from datetime import UTC, datetime, timedelta
from unittest import mock

import psycopg
from psycopg.rows import dict_row

REGISTRY_NAME = "sample_attorney_demo"
DECISION_CLASS_ID = "claim_approval"

# Pre-seeded by 010/011-*.sql; not registered by these tests.
RECOGNITION_AUTHORITY_ACTOR_ID = "cdp_identity_recognition_authority"
GRANT_ISSUER_ACTOR_ID = "cdp_authority_grant_issuer"


def _database_url() -> str:
    return os.environ.get("CDP_TEST_DATABASE_URL", "postgresql://cdp:cdp@localhost:5432/cdp")


def _universal_attestation_columns_exist() -> bool:
    with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
        cursor.execute(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_schema = 'cdp_core' AND table_name = 'attestation_record' "
            "AND column_name = 'governed_act_ref_id'"
        )
        return cursor.fetchone() is not None


def _decision_workflow_configured() -> bool:
    with psycopg.connect(_database_url()) as conn, conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT 1 FROM cdp_core.workflow_definition
            WHERE workflow_code = 'nemawashi_default_v1' AND workflow_version = 'v1'
              AND applies_to_registry_name = %s AND applies_to_decision_class_id = %s
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


def _submit_and_recognize_claim(actor_id: str, *, purpose_scope: str):
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
            claimed_identity_descriptor="Continuity for universal-attestation tests.",
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


def _grant_authority(actor_id: str, authority: str) -> None:
    from cdp.core.services import GrantAuthorityInput, grant_authority

    grant_authority(
        GrantAuthorityInput(
            actor_id=actor_id,
            authority=authority,
            scope_registry_name=REGISTRY_NAME,
            scope_decision_class_id=DECISION_CLASS_ID,
            expires_at=datetime.now(UTC) + timedelta(days=1),
            issued_by_actor_id=GRANT_ISSUER_ACTOR_ID,
            basis="policy",
        )
    )


def _make_attestation_input(actor_id: str, claim_id):
    from cdp.core.services import AttestationInput

    return AttestationInput(
        actor_id=actor_id,
        identity_claim_id=claim_id,
        attestation_method="shared_secret_reference",
        credential_reference="universal-attestation-test-credential-1",
        issued_at=datetime.now(UTC),
    )


def _create_plain_decision(decision_id: str, subject_actor_id: str):
    from cdp.core.services import DecisionInput, create_decision_with_workflow

    return create_decision_with_workflow(
        DecisionInput(
            registry_name=REGISTRY_NAME,
            decision_id=decision_id,
            decision_class_id=DECISION_CLASS_ID,
            antecedent_text="Universal-attestation-slice integration test decision.",
            subject_actor_type="human",
            subject_actor_id=subject_actor_id,
            predicate_verb="recommend_approval",
            object_type="claim",
            object_id="claim_9981",
            permission_source_type="policy_rule",
            permission_source_id="policy_claims_approval_v2",
            human_required=True,
        )
    )


@unittest.skipUnless(os.environ.get("CDP_TEST_DATABASE_URL"), "set CDP_TEST_DATABASE_URL to run")
class AttestAndRaiseChallengeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ.setdefault("DATABASE_URL", _database_url())
        if not _universal_attestation_columns_exist():
            raise unittest.SkipTest(
                "012-universal-attestation.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )
        if not _decision_workflow_configured():
            raise unittest.SkipTest(
                "004-decision-class-workflow-seed.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )

    def test_happy_path_attests_and_raises_challenge(self) -> None:
        from cdp.core.services import AttestedChallengeInput, ChallengeInput, attest_and_raise_challenge

        subject_id = _register_actor("ua-challenge-subject")
        decision_id = _unique("ua-challenge-decision")
        _create_plain_decision(decision_id, subject_id)

        actor_id = _register_actor("ua-challenge-actor")
        claim_id = _submit_and_recognize_claim(actor_id, purpose_scope="challenge_raising")
        _grant_authority(actor_id, "CHALLENGE")

        result = attest_and_raise_challenge(
            AttestedChallengeInput(
                challenge_input=ChallengeInput(
                    registry_name=REGISTRY_NAME,
                    decision_id=decision_id,
                    raised_by_actor_id=actor_id,
                    challenge_text="Universal attestation challenge test.",
                    challenge_type="policy",
                ),
                attestation_input=_make_attestation_input(actor_id, claim_id),
            )
        )

        self.assertEqual(result["challenge"]["raised_by_actor_id"], actor_id)
        self.assertEqual(result["attestation"]["actor_id"], actor_id)
        self.assertEqual(result["attestation"]["governed_act_type"], "challenge_raised")
        self.assertEqual(result["attestation"]["governed_act_ref_id"], result["challenge"]["challenge_id"])
        self.assertEqual(result["authority_evaluation"]["result"], "pass")
        self.assertEqual(result["authority_evaluation"]["required_authority"], "CHALLENGE")

        with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
            cursor.execute(
                "SELECT governed_act_ref_id FROM cdp_core.authority_evaluation_result "
                "WHERE governed_act_type = 'challenge_raised' AND governed_act_decision_id = %s",
                (decision_id,),
            )
            self.assertEqual(cursor.fetchone()["governed_act_ref_id"], result["challenge"]["challenge_id"])

    def test_missing_authority_fails_closed(self) -> None:
        from cdp.core.services import (
            AttestedChallengeInput,
            AuthorityNotGranted,
            ChallengeInput,
            attest_and_raise_challenge,
        )

        subject_id = _register_actor("ua-challenge-noauth-subject")
        decision_id = _unique("ua-challenge-noauth-decision")
        _create_plain_decision(decision_id, subject_id)

        actor_id = _register_actor("ua-challenge-noauth-actor")
        claim_id = _submit_and_recognize_claim(actor_id, purpose_scope="challenge_raising")
        # Deliberately no _grant_authority call.

        with self.assertRaises(AuthorityNotGranted):
            attest_and_raise_challenge(
                AttestedChallengeInput(
                    challenge_input=ChallengeInput(
                        registry_name=REGISTRY_NAME,
                        decision_id=decision_id,
                        raised_by_actor_id=actor_id,
                        challenge_text="Should not be created.",
                    ),
                    attestation_input=_make_attestation_input(actor_id, claim_id),
                )
            )

        with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
            cursor.execute(
                "SELECT count(*) AS n FROM cdp_core.challenge_record WHERE decision_id = %s",
                (decision_id,),
            )
            self.assertEqual(cursor.fetchone()["n"], 0)

    def test_unrecognized_claim_fails_closed(self) -> None:
        from cdp.core.services import (
            AttestedChallengeInput,
            ChallengeInput,
            IdentityClaimInput,
            IdentityClaimNotRecognized,
            attest_and_raise_challenge,
            submit_identity_claim,
        )

        subject_id = _register_actor("ua-challenge-unrec-subject")
        decision_id = _unique("ua-challenge-unrec-decision")
        _create_plain_decision(decision_id, subject_id)

        actor_id = _register_actor("ua-challenge-unrec-actor")
        claim_id = submit_identity_claim(
            IdentityClaimInput(
                actor_id=actor_id,
                claimant_actor_id=actor_id,
                claimed_identity_descriptor="Never recognized.",
                purpose_scope="challenge_raising",
            )
        )["identity_claim"]["claim_id"]
        _grant_authority(actor_id, "CHALLENGE")

        with self.assertRaises(IdentityClaimNotRecognized):
            attest_and_raise_challenge(
                AttestedChallengeInput(
                    challenge_input=ChallengeInput(
                        registry_name=REGISTRY_NAME,
                        decision_id=decision_id,
                        raised_by_actor_id=actor_id,
                        challenge_text="Should not be created.",
                    ),
                    attestation_input=_make_attestation_input(actor_id, claim_id),
                )
            )

    def test_wrong_purpose_scope_claim_fails_closed(self) -> None:
        from cdp.core.services import (
            AttestedChallengeInput,
            ChallengeInput,
            IdentityClaimScopeInsufficient,
            attest_and_raise_challenge,
        )

        subject_id = _register_actor("ua-challenge-wrongscope-subject")
        decision_id = _unique("ua-challenge-wrongscope-decision")
        _create_plain_decision(decision_id, subject_id)

        actor_id = _register_actor("ua-challenge-wrongscope-actor")
        # Recognized, but scoped for a different act.
        claim_id = _submit_and_recognize_claim(actor_id, purpose_scope="decision_creation")
        _grant_authority(actor_id, "CHALLENGE")

        with self.assertRaises(IdentityClaimScopeInsufficient):
            attest_and_raise_challenge(
                AttestedChallengeInput(
                    challenge_input=ChallengeInput(
                        registry_name=REGISTRY_NAME,
                        decision_id=decision_id,
                        raised_by_actor_id=actor_id,
                        challenge_text="Should not be created.",
                    ),
                    attestation_input=_make_attestation_input(actor_id, claim_id),
                )
            )

    def test_unknown_actor_fails_closed(self) -> None:
        from cdp.core.services import (
            ActorNotFound,
            AttestedChallengeInput,
            ChallengeInput,
            attest_and_raise_challenge,
        )

        subject_id = _register_actor("ua-challenge-unknown-subject")
        decision_id = _unique("ua-challenge-unknown-decision")
        _create_plain_decision(decision_id, subject_id)
        unknown_actor_id = _unique("ua-challenge-unknown-actor")

        with self.assertRaises(ActorNotFound):
            attest_and_raise_challenge(
                AttestedChallengeInput(
                    challenge_input=ChallengeInput(
                        registry_name=REGISTRY_NAME,
                        decision_id=decision_id,
                        raised_by_actor_id=unknown_actor_id,
                        challenge_text="Should not be created.",
                    ),
                    attestation_input=_make_attestation_input(unknown_actor_id, uuid.uuid4()),
                )
            )

    def test_downstream_failure_rolls_back_the_whole_transaction(self) -> None:
        from cdp.core.services import AttestedChallengeInput, ChallengeInput, attest_and_raise_challenge

        subject_id = _register_actor("ua-challenge-rollback-subject")
        decision_id = _unique("ua-challenge-rollback-decision")
        _create_plain_decision(decision_id, subject_id)

        actor_id = _register_actor("ua-challenge-rollback-actor")
        claim_id = _submit_and_recognize_claim(actor_id, purpose_scope="challenge_raising")
        _grant_authority(actor_id, "CHALLENGE")

        with mock.patch(
            "cdp.core.services.attestations_repo.insert_attestation",
            side_effect=RuntimeError("forced failure after challenge raised"),
        ):
            with self.assertRaises(RuntimeError):
                attest_and_raise_challenge(
                    AttestedChallengeInput(
                        challenge_input=ChallengeInput(
                            registry_name=REGISTRY_NAME,
                            decision_id=decision_id,
                            raised_by_actor_id=actor_id,
                            challenge_text="Should not survive rollback.",
                        ),
                        attestation_input=_make_attestation_input(actor_id, claim_id),
                    )
                )

        with psycopg.connect(_database_url(), row_factory=dict_row) as conn, conn.cursor() as cursor:
            cursor.execute(
                "SELECT count(*) AS n FROM cdp_core.challenge_record WHERE decision_id = %s",
                (decision_id,),
            )
            self.assertEqual(cursor.fetchone()["n"], 0, "challenge should not survive rollback")

            cursor.execute(
                "SELECT blocked FROM cdp_core.workflow_instance "
                "WHERE registry_name = %s AND decision_id = %s",
                (REGISTRY_NAME, decision_id),
            )
            self.assertFalse(cursor.fetchone()["blocked"], "workflow should not remain blocked")


@unittest.skipUnless(os.environ.get("CDP_TEST_DATABASE_URL"), "set CDP_TEST_DATABASE_URL to run")
class AttestAndAdjudicateChallengeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ.setdefault("DATABASE_URL", _database_url())
        if not _universal_attestation_columns_exist():
            raise unittest.SkipTest(
                "012-universal-attestation.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )
        if not _decision_workflow_configured():
            raise unittest.SkipTest(
                "004-decision-class-workflow-seed.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )

    def _raise_plain_challenge(self, decision_id: str):
        from cdp.core.services import ChallengeInput, raise_challenge_for_decision

        return raise_challenge_for_decision(
            ChallengeInput(
                registry_name=REGISTRY_NAME,
                decision_id=decision_id,
                raised_by_actor_id="claims_review_agent",
                challenge_text="Plain, unattested challenge for adjudication setup.",
            )
        )["challenge"]

    def test_happy_path_attests_and_adjudicates(self) -> None:
        from cdp.core.services import AdjudicationInput, AttestedAdjudicationInput, attest_and_adjudicate_challenge

        subject_id = _register_actor("ua-adjudicate-subject")
        decision_id = _unique("ua-adjudicate-decision")
        _create_plain_decision(decision_id, subject_id)
        challenge = self._raise_plain_challenge(decision_id)

        actor_id = _register_actor("ua-adjudicate-actor")
        claim_id = _submit_and_recognize_claim(actor_id, purpose_scope="challenge_adjudication")
        _grant_authority(actor_id, "ADJUDICATE")

        result = attest_and_adjudicate_challenge(
            AttestedAdjudicationInput(
                adjudication_input=AdjudicationInput(
                    registry_name=REGISTRY_NAME,
                    decision_id=decision_id,
                    challenge_id=challenge["challenge_id"],
                    adjudicated_by_actor_id=actor_id,
                    outcome="not_sustained",
                    rationale="Universal attestation adjudication test.",
                ),
                attestation_input=_make_attestation_input(actor_id, claim_id),
            )
        )

        self.assertEqual(result["adjudication"]["outcome"], "not_sustained")
        self.assertEqual(result["attestation"]["governed_act_type"], "challenge_adjudicated")
        self.assertEqual(
            result["attestation"]["governed_act_ref_id"], result["adjudication"]["adjudication_id"]
        )
        self.assertEqual(result["authority_evaluation"]["required_authority"], "ADJUDICATE")

    def test_missing_authority_fails_closed(self) -> None:
        from cdp.core.services import (
            AdjudicationInput,
            AttestedAdjudicationInput,
            AuthorityNotGranted,
            attest_and_adjudicate_challenge,
        )

        subject_id = _register_actor("ua-adjudicate-noauth-subject")
        decision_id = _unique("ua-adjudicate-noauth-decision")
        _create_plain_decision(decision_id, subject_id)
        challenge = self._raise_plain_challenge(decision_id)

        actor_id = _register_actor("ua-adjudicate-noauth-actor")
        claim_id = _submit_and_recognize_claim(actor_id, purpose_scope="challenge_adjudication")

        with self.assertRaises(AuthorityNotGranted):
            attest_and_adjudicate_challenge(
                AttestedAdjudicationInput(
                    adjudication_input=AdjudicationInput(
                        registry_name=REGISTRY_NAME,
                        decision_id=decision_id,
                        challenge_id=challenge["challenge_id"],
                        adjudicated_by_actor_id=actor_id,
                        outcome="not_sustained",
                        rationale="Should not be created.",
                    ),
                    attestation_input=_make_attestation_input(actor_id, claim_id),
                )
            )

    def test_challenge_not_found_fails_closed(self) -> None:
        from cdp.core.services import (
            AdjudicationInput,
            AttestedAdjudicationInput,
            ChallengeNotFound,
            attest_and_adjudicate_challenge,
        )

        subject_id = _register_actor("ua-adjudicate-nochallenge-subject")
        decision_id = _unique("ua-adjudicate-nochallenge-decision")
        _create_plain_decision(decision_id, subject_id)

        actor_id = _register_actor("ua-adjudicate-nochallenge-actor")
        claim_id = _submit_and_recognize_claim(actor_id, purpose_scope="challenge_adjudication")
        _grant_authority(actor_id, "ADJUDICATE")

        with self.assertRaises(ChallengeNotFound):
            attest_and_adjudicate_challenge(
                AttestedAdjudicationInput(
                    adjudication_input=AdjudicationInput(
                        registry_name=REGISTRY_NAME,
                        decision_id=decision_id,
                        challenge_id=uuid.uuid4(),
                        adjudicated_by_actor_id=actor_id,
                        outcome="not_sustained",
                        rationale="No such challenge.",
                    ),
                    attestation_input=_make_attestation_input(actor_id, claim_id),
                )
            )


@unittest.skipUnless(os.environ.get("CDP_TEST_DATABASE_URL"), "set CDP_TEST_DATABASE_URL to run")
class AttestAndAuthorizeExecutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ.setdefault("DATABASE_URL", _database_url())
        if not _universal_attestation_columns_exist():
            raise unittest.SkipTest(
                "012-universal-attestation.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )
        if not _decision_workflow_configured():
            raise unittest.SkipTest(
                "004-decision-class-workflow-seed.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )

    def test_happy_path_attests_and_authorizes(self) -> None:
        from cdp.core.services import (
            AttestedExecutionAuthorizationInput,
            ExecutionAuthorizationInput,
            attest_and_authorize_execution,
        )

        subject_id = _register_actor("ua-execauth-subject")
        decision_id = _unique("ua-execauth-decision")
        _create_plain_decision(decision_id, subject_id)

        actor_id = _register_actor("ua-execauth-actor")
        claim_id = _submit_and_recognize_claim(actor_id, purpose_scope="execution_authorization")
        _grant_authority(actor_id, "AUTHORIZE_EXECUTION")

        result = attest_and_authorize_execution(
            AttestedExecutionAuthorizationInput(
                authorization_input=ExecutionAuthorizationInput(
                    registry_name=REGISTRY_NAME,
                    decision_id=decision_id,
                    authorized_by_actor_id=actor_id,
                    rationale="Universal attestation execution-authorization test.",
                ),
                attestation_input=_make_attestation_input(actor_id, claim_id),
            )
        )

        self.assertEqual(result["attestation"]["governed_act_type"], "execution_authorized")
        self.assertEqual(
            result["attestation"]["governed_act_ref_id"], result["authorization"]["authorization_id"]
        )
        self.assertEqual(result["authority_evaluation"]["required_authority"], "AUTHORIZE_EXECUTION")

    def test_missing_authority_fails_closed(self) -> None:
        from cdp.core.services import (
            AttestedExecutionAuthorizationInput,
            AuthorityNotGranted,
            ExecutionAuthorizationInput,
            attest_and_authorize_execution,
        )

        subject_id = _register_actor("ua-execauth-noauth-subject")
        decision_id = _unique("ua-execauth-noauth-decision")
        _create_plain_decision(decision_id, subject_id)

        actor_id = _register_actor("ua-execauth-noauth-actor")
        claim_id = _submit_and_recognize_claim(actor_id, purpose_scope="execution_authorization")

        with self.assertRaises(AuthorityNotGranted):
            attest_and_authorize_execution(
                AttestedExecutionAuthorizationInput(
                    authorization_input=ExecutionAuthorizationInput(
                        registry_name=REGISTRY_NAME,
                        decision_id=decision_id,
                        authorized_by_actor_id=actor_id,
                        rationale="Should not be created.",
                    ),
                    attestation_input=_make_attestation_input(actor_id, claim_id),
                )
            )


@unittest.skipUnless(os.environ.get("CDP_TEST_DATABASE_URL"), "set CDP_TEST_DATABASE_URL to run")
class AttestAndRecordExecutionAttemptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ.setdefault("DATABASE_URL", _database_url())
        if not _universal_attestation_columns_exist():
            raise unittest.SkipTest(
                "012-universal-attestation.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )
        if not _decision_workflow_configured():
            raise unittest.SkipTest(
                "004-decision-class-workflow-seed.sql is not applied to CDP_TEST_DATABASE_URL yet"
            )

    def _authorize_plain_execution(self, decision_id: str):
        from cdp.core.services import ExecutionAuthorizationInput, authorize_execution

        return authorize_execution(
            ExecutionAuthorizationInput(
                registry_name=REGISTRY_NAME,
                decision_id=decision_id,
                authorized_by_actor_id="user_442",
                rationale="Plain, unattested authorization for execution-record setup.",
            )
        )["authorization"]

    def test_happy_path_attests_and_records(self) -> None:
        from cdp.core.services import (
            AttestedExecutionRecordInput,
            ExecutionRecordInput,
            attest_and_record_execution_attempt,
        )

        subject_id = _register_actor("ua-execrecord-subject")
        decision_id = _unique("ua-execrecord-decision")
        _create_plain_decision(decision_id, subject_id)
        self._authorize_plain_execution(decision_id)

        actor_id = _register_actor("ua-execrecord-actor")
        claim_id = _submit_and_recognize_claim(actor_id, purpose_scope="execution_recording")
        _grant_authority(actor_id, "RECORD")

        now = datetime.now(UTC)
        result = attest_and_record_execution_attempt(
            AttestedExecutionRecordInput(
                execution_input=ExecutionRecordInput(
                    registry_name=REGISTRY_NAME,
                    decision_id=decision_id,
                    executed_by_actor_id=actor_id,
                    execution_status="succeeded",
                    result_summary="Universal attestation execution-record test.",
                    attempted_at=now,
                    completed_at=now,
                ),
                attestation_input=_make_attestation_input(actor_id, claim_id),
            )
        )

        self.assertEqual(result["attestation"]["governed_act_type"], "execution_recorded")
        self.assertEqual(
            result["attestation"]["governed_act_ref_id"], result["execution_record"]["execution_id"]
        )
        self.assertEqual(result["authority_evaluation"]["required_authority"], "RECORD")

    def test_missing_authority_fails_closed(self) -> None:
        from cdp.core.services import (
            AttestedExecutionRecordInput,
            AuthorityNotGranted,
            ExecutionRecordInput,
            attest_and_record_execution_attempt,
        )

        subject_id = _register_actor("ua-execrecord-noauth-subject")
        decision_id = _unique("ua-execrecord-noauth-decision")
        _create_plain_decision(decision_id, subject_id)
        self._authorize_plain_execution(decision_id)

        actor_id = _register_actor("ua-execrecord-noauth-actor")
        claim_id = _submit_and_recognize_claim(actor_id, purpose_scope="execution_recording")

        now = datetime.now(UTC)
        with self.assertRaises(AuthorityNotGranted):
            attest_and_record_execution_attempt(
                AttestedExecutionRecordInput(
                    execution_input=ExecutionRecordInput(
                        registry_name=REGISTRY_NAME,
                        decision_id=decision_id,
                        executed_by_actor_id=actor_id,
                        execution_status="succeeded",
                        result_summary="Should not be created.",
                        attempted_at=now,
                        completed_at=now,
                    ),
                    attestation_input=_make_attestation_input(actor_id, claim_id),
                )
            )

    def test_no_authorization_fails_closed(self) -> None:
        from cdp.core.services import (
            AttestedExecutionRecordInput,
            DecisionNotAuthorizedForExecution,
            ExecutionRecordInput,
            attest_and_record_execution_attempt,
        )

        subject_id = _register_actor("ua-execrecord-noAuthorization-subject")
        decision_id = _unique("ua-execrecord-noAuthorization-decision")
        _create_plain_decision(decision_id, subject_id)
        # Deliberately no _authorize_plain_execution call.

        actor_id = _register_actor("ua-execrecord-noAuthorization-actor")
        claim_id = _submit_and_recognize_claim(actor_id, purpose_scope="execution_recording")
        _grant_authority(actor_id, "RECORD")

        now = datetime.now(UTC)
        with self.assertRaises(DecisionNotAuthorizedForExecution):
            attest_and_record_execution_attempt(
                AttestedExecutionRecordInput(
                    execution_input=ExecutionRecordInput(
                        registry_name=REGISTRY_NAME,
                        decision_id=decision_id,
                        executed_by_actor_id=actor_id,
                        execution_status="succeeded",
                        result_summary="Should not be created.",
                        attempted_at=now,
                        completed_at=now,
                    ),
                    attestation_input=_make_attestation_input(actor_id, claim_id),
                )
            )


if __name__ == "__main__":
    unittest.main()
