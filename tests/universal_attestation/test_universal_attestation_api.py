"""API round-trip tests for the Universal Attestation proof paths (session
029, RFC-CDP-031 SS2) against the running cdp-api.

Follows the pattern in tests/identify_attest_standing/test_identity_attestation_api.py:
assumes the local Docker stack (`make up-build`) is already running, and
talks to it over plain HTTP with no cdp import required.

Requires 001, 004, 010, 011, and 012 already applied to the database
cdp-api is using.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timedelta, timezone

import pytest

API_URL = os.getenv("CDP_TEST_API_URL", "http://localhost:8000")
REGISTRY_NAME = "sample_attorney_demo"
DECISION_CLASS_ID = "claim_approval"

RECOGNITION_AUTHORITY_ACTOR_ID = "cdp_identity_recognition_authority"
GRANT_ISSUER_ACTOR_ID = "cdp_authority_grant_issuer"


def _request(method: str, url: str, payload: dict | None = None) -> tuple[int, dict]:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}, method=method
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        pytest.fail(f"Could not reach {url}. Is the local Docker stack running? {exc}")


def _post_json(url: str, payload: dict) -> tuple[int, dict]:
    return _request("POST", url, payload)


def _get_json(url: str) -> tuple[int, dict]:
    return _request("GET", url)


def _unique(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def _register_actor() -> str:
    actor_id = _unique("ua-api-actor")
    status, body = _post_json(
        f"{API_URL}/actors",
        {"actor_id": actor_id, "actor_type": "human", "display_label": f"UA test actor {actor_id}"},
    )
    assert status == 201, f"expected 201, got {status}: {body}"
    return actor_id


def _submit_and_recognize_claim(actor_id: str, purpose_scope: str) -> str:
    status, body = _post_json(
        f"{API_URL}/identity-claims",
        {
            "actor_id": actor_id,
            "claimant_actor_id": actor_id,
            "claimed_identity_descriptor": "UA API round-trip descriptor.",
            "purpose_scope": purpose_scope,
        },
    )
    assert status == 201, f"expected 201, got {status}: {body}"
    claim_id = body["identity_claim"]["claim_id"]

    status, body = _post_json(
        f"{API_URL}/identity-claims/{claim_id}/recognize",
        {"decided_by_actor_id": RECOGNITION_AUTHORITY_ACTOR_ID, "rationale": "Looks good."},
    )
    assert status == 200, f"expected 200, got {status}: {body}"
    return claim_id


def _grant_authority(actor_id: str, authority: str) -> None:
    status, body = _post_json(
        f"{API_URL}/authority-grants",
        {
            "actor_id": actor_id,
            "authority": authority,
            "scope_registry_name": REGISTRY_NAME,
            "scope_decision_class_id": DECISION_CLASS_ID,
            "expires_at": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
            "issued_by_actor_id": GRANT_ISSUER_ACTOR_ID,
            "basis": "policy",
        },
    )
    assert status == 201, f"expected 201, got {status}: {body}"


def _create_plain_decision(decision_id: str, subject_actor_id: str) -> None:
    status, body = _post_json(
        f"{API_URL}/decisions",
        {
            "registry_name": REGISTRY_NAME,
            "decision_id": decision_id,
            "decision_class_id": DECISION_CLASS_ID,
            "antecedent_text": "UA API round-trip test decision.",
            "subject_actor_type": "human",
            "subject_actor_id": subject_actor_id,
            "predicate_verb": "recommend_approval",
            "object_type": "claim",
            "object_id": "claim_9981",
            "permission_source_type": "policy_rule",
            "permission_source_id": "policy_claims_approval_v2",
            "human_required": True,
        },
    )
    assert status == 201, f"expected 201, got {status}: {body}"


def _attestation_fields(actor_id: str, claim_id: str) -> dict:
    return {
        "submitted_by_actor_id": actor_id,
        "identity_claim_id": claim_id,
        "attestation_method": "shared_secret_reference",
        "credential_reference": "ua-api-test-credential-1",
        "issued_at": datetime.now(timezone.utc).isoformat(),
    }


def test_attested_challenge_round_trip_succeeds() -> None:
    subject_id = _register_actor()
    decision_id = _unique("ua-api-challenge-decision")
    _create_plain_decision(decision_id, subject_id)

    actor_id = _register_actor()
    claim_id = _submit_and_recognize_claim(actor_id, "challenge_raising")
    _grant_authority(actor_id, "CHALLENGE")

    status, body = _post_json(
        f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/attested-challenges",
        {
            "challenge_text": "UA API attested challenge.",
            "challenge_type": "policy",
            **_attestation_fields(actor_id, claim_id),
        },
    )
    assert status == 201, f"expected 201, got {status}: {body}"
    assert body["challenge"]["raised_by_actor_id"] == actor_id
    assert body["attestation"]["governed_act_type"] == "challenge_raised"
    assert body["authority_evaluation"]["result"] == "pass"

    list_status, list_body = _get_json(
        f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/attestations"
    )
    assert list_status == 200
    assert len(list_body["attestations"]) == 1


def test_attested_challenge_without_authority_grant_returns_403() -> None:
    subject_id = _register_actor()
    decision_id = _unique("ua-api-challenge-noauth-decision")
    _create_plain_decision(decision_id, subject_id)

    actor_id = _register_actor()
    claim_id = _submit_and_recognize_claim(actor_id, "challenge_raising")

    status, body = _post_json(
        f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/attested-challenges",
        {
            "challenge_text": "Should not be created.",
            **_attestation_fields(actor_id, claim_id),
        },
    )
    assert status == 403, f"expected 403, got {status}: {body}"


def test_attested_adjudication_round_trip_succeeds() -> None:
    subject_id = _register_actor()
    decision_id = _unique("ua-api-adjudication-decision")
    _create_plain_decision(decision_id, subject_id)

    plain_status, plain_body = _post_json(
        f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/challenges",
        {"raised_by_actor_id": "user_442", "challenge_text": "Plain challenge for adjudication setup."},
    )
    assert plain_status == 201, f"expected 201, got {plain_status}: {plain_body}"
    challenge_id = plain_body["challenge"]["challenge_id"]

    actor_id = _register_actor()
    claim_id = _submit_and_recognize_claim(actor_id, "challenge_adjudication")
    _grant_authority(actor_id, "ADJUDICATE")

    status, body = _post_json(
        f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/challenges/{challenge_id}/attested-adjudications",
        {
            "outcome": "not_sustained",
            "rationale": "UA API attested adjudication.",
            **_attestation_fields(actor_id, claim_id),
        },
    )
    assert status == 201, f"expected 201, got {status}: {body}"
    assert body["adjudication"]["outcome"] == "not_sustained"
    assert body["attestation"]["governed_act_type"] == "challenge_adjudicated"


def test_attested_execution_authorization_round_trip_succeeds() -> None:
    subject_id = _register_actor()
    decision_id = _unique("ua-api-execauth-decision")
    _create_plain_decision(decision_id, subject_id)

    actor_id = _register_actor()
    claim_id = _submit_and_recognize_claim(actor_id, "execution_authorization")
    _grant_authority(actor_id, "AUTHORIZE_EXECUTION")

    status, body = _post_json(
        f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/attested-execution-authorizations",
        {
            "rationale": "UA API attested execution authorization.",
            **_attestation_fields(actor_id, claim_id),
        },
    )
    assert status == 201, f"expected 201, got {status}: {body}"
    assert body["attestation"]["governed_act_type"] == "execution_authorized"


def test_attested_execution_record_round_trip_succeeds() -> None:
    subject_id = _register_actor()
    decision_id = _unique("ua-api-execrecord-decision")
    _create_plain_decision(decision_id, subject_id)

    plain_status, plain_body = _post_json(
        f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/execution-authorizations",
        {"authorized_by_actor_id": "user_442", "rationale": "Plain authorization for execution-record setup."},
    )
    assert plain_status == 201, f"expected 201, got {plain_status}: {plain_body}"

    actor_id = _register_actor()
    claim_id = _submit_and_recognize_claim(actor_id, "execution_recording")
    _grant_authority(actor_id, "RECORD")

    now = datetime.now(timezone.utc).isoformat()
    status, body = _post_json(
        f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/attested-execution-records",
        {
            "execution_status": "succeeded",
            "result_summary": "UA API attested execution record.",
            "attempted_at": now,
            "completed_at": now,
            **_attestation_fields(actor_id, claim_id),
        },
    )
    assert status == 201, f"expected 201, got {status}: {body}"
    assert body["attestation"]["governed_act_type"] == "execution_recorded"

    eval_status, eval_body = _get_json(
        f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/authority-evaluations"
    )
    assert eval_status == 200
    assert len(eval_body["authority_evaluations"]) == 1
    assert eval_body["authority_evaluations"][0]["required_authority"] == "RECORD"
