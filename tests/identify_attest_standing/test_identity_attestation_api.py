"""API round-trip tests for the Identity and Attestation slice
(RFC-CDP-030, RFC-CDP-031) against the running cdp-api.

Follows the pattern in tests/challenge/test_challenge_api.py: assumes the
local Docker stack (`make up-build`) is already running, and talks to it
over plain HTTP with no cdp import required, so it runs fine under any
local interpreter.

Requires 001 and 010 already applied to the database cdp-api is using, and
004's nemawashi_default_v1 -> sample_attorney_demo.claim_approval workflow
configured (for the attested-decision round trip).

Cleanup note: as in the service-layer tests, cdp_core.actor and
cdp_core.identity_claim rows cannot be deleted (010 enforces this at the
database level), and a decision created through /attested-decisions gets a
permanent cdp_core.attestation_record row FK'd to it, so none of those
rows are cleaned up here -- see
tests/identify_attest_standing/test_actor_service.py's module docstring.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone

import pytest

API_URL = os.getenv("CDP_TEST_API_URL", "http://localhost:8000")
REGISTRY_NAME = "sample_attorney_demo"
DECISION_CLASS_ID = "claim_approval"


def _request(method: str, url: str, payload: dict | None = None) -> tuple[int, dict]:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method=method,
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


def _register_actor(display_mode: str = "public") -> str:
    actor_id = _unique("iaa-api-actor")
    status, body = _post_json(
        f"{API_URL}/actors",
        {
            "actor_id": actor_id,
            "actor_type": "human",
            "display_label": f"API test actor {actor_id}",
            "display_mode": display_mode,
        },
    )
    assert status == 201, f"expected 201, got {status}: {body}"
    return actor_id


def _submit_claim(actor_id: str, *, purpose_scope: str = "decision_creation") -> str:
    status, body = _post_json(
        f"{API_URL}/identity-claims",
        {
            "actor_id": actor_id,
            "claimant_actor_id": actor_id,
            "claimed_identity_descriptor": "API round-trip descriptor for this actor.",
            "purpose_scope": purpose_scope,
            "evidence_refs": ["evidence-ref-api-1"],
        },
    )
    assert status == 201, f"expected 201, got {status}: {body}"
    return body["identity_claim"]["claim_id"]


def _recognize_claim(claim_id: str, recognizer_actor_id: str) -> None:
    status, body = _post_json(
        f"{API_URL}/identity-claims/{claim_id}/recognize",
        {"decided_by_actor_id": recognizer_actor_id, "rationale": "Looks good."},
    )
    assert status == 200, f"expected 200, got {status}: {body}"


def _attested_decision_payload(actor_id: str, claim_id: str, decision_id: str) -> dict:
    return {
        "registry_name": REGISTRY_NAME,
        "decision_id": decision_id,
        "decision_class_id": DECISION_CLASS_ID,
        "antecedent_text": "Identity/Attestation API round-trip test decision.",
        "subject_actor_type": "human",
        "subject_actor_id": actor_id,
        "predicate_verb": "recommend_approval",
        "object_type": "claim",
        "object_id": "claim_9981",
        "permission_source_type": "policy_rule",
        "permission_source_id": "policy_claims_approval_v2",
        "human_required": True,
        "actor_id": actor_id,
        "identity_claim_id": claim_id,
        "attestation_method": "shared_secret_reference",
        "credential_reference": "api-test-credential-ref-1",
        "issued_at": datetime.now(timezone.utc).isoformat(),
    }


def test_full_actor_claim_attestation_round_trip_and_governed_mutation_succeeds() -> None:
    actor_id = _register_actor()
    recognizer_id = _register_actor()
    claim_id = _submit_claim(actor_id)
    _recognize_claim(claim_id, recognizer_id)
    decision_id = _unique("iaa-api-decision")

    status, body = _post_json(
        f"{API_URL}/attested-decisions", _attested_decision_payload(actor_id, claim_id, decision_id)
    )
    assert status == 201, f"expected 201, got {status}: {body}"
    assert body["decision"]["decision_id"] == decision_id
    assert body["decision"]["subject_actor_id"] == actor_id
    assert body["attestation"]["verification_result"] == "verified"
    attestation_id = body["attestation"]["attestation_id"]

    actor_status, actor_body = _get_json(f"{API_URL}/actors/{actor_id}")
    assert actor_status == 200
    assert actor_body["actor_id"] == actor_id
    assert actor_body["display_mode"] == "public"

    claim_status, claim_body = _get_json(f"{API_URL}/identity-claims/{claim_id}")
    assert claim_status == 200
    assert claim_body["recognition_status"] == "recognized"
    assert claim_body["claimed_identity_descriptor"] != "[protected]"

    attestation_status, attestation_body = _get_json(f"{API_URL}/attestations/{attestation_id}")
    assert attestation_status == 200
    assert attestation_body["actor_id"] == actor_id
    assert attestation_body["governed_act_decision_id"] == decision_id

    decision_status, decision_body = _get_json(f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}")
    assert decision_status == 200
    assert decision_body["subject_actor_id"] == actor_id


def test_attested_decision_missing_credential_reference_returns_422() -> None:
    actor_id = _register_actor()
    recognizer_id = _register_actor()
    claim_id = _submit_claim(actor_id)
    _recognize_claim(claim_id, recognizer_id)
    decision_id = _unique("iaa-api-decision-missing-cred")

    payload = _attested_decision_payload(actor_id, claim_id, decision_id)
    payload["credential_reference"] = ""

    status, body = _post_json(f"{API_URL}/attested-decisions", payload)
    assert status == 422, f"expected 422, got {status}: {body}"

    get_status, _ = _get_json(f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}")
    assert get_status == 404, "no decision should have been created"


def test_attested_decision_with_unrecognized_claim_returns_409() -> None:
    actor_id = _register_actor()
    claim_id = _submit_claim(actor_id)  # never recognized
    decision_id = _unique("iaa-api-decision-unrecognized")

    status, body = _post_json(
        f"{API_URL}/attested-decisions", _attested_decision_payload(actor_id, claim_id, decision_id)
    )
    assert status == 409, f"expected 409, got {status}: {body}"

    get_status, _ = _get_json(f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}")
    assert get_status == 404, "no decision should have been created"


def test_attested_decision_with_mismatched_subject_actor_returns_409() -> None:
    attesting_actor_id = _register_actor()
    subject_actor_id = _register_actor()
    recognizer_id = _register_actor()
    claim_id = _submit_claim(attesting_actor_id)
    _recognize_claim(claim_id, recognizer_id)
    decision_id = _unique("iaa-api-decision-mismatch")

    payload = _attested_decision_payload(attesting_actor_id, claim_id, decision_id)
    payload["subject_actor_id"] = subject_actor_id  # decision subject differs from attestor

    status, body = _post_json(f"{API_URL}/attested-decisions", payload)
    assert status == 409, f"expected 409, got {status}: {body}"

    get_status, _ = _get_json(f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}")
    assert get_status == 404, "no decision should have been created"


def test_attested_decision_with_unknown_actor_returns_404() -> None:
    unknown_actor_id = _unique("iaa-api-unknown-actor")
    decision_id = _unique("iaa-api-decision-unknown-actor")

    status, body = _post_json(
        f"{API_URL}/attested-decisions",
        _attested_decision_payload(unknown_actor_id, str(uuid.uuid4()), decision_id),
    )
    assert status == 404, f"expected 404, got {status}: {body}"


def test_protected_actor_identity_claim_response_redacts_descriptor_and_evidence() -> None:
    actor_id = _register_actor(display_mode="protected")
    claim_id = _submit_claim(actor_id)

    status, body = _get_json(f"{API_URL}/identity-claims/{claim_id}")
    assert status == 200
    assert body["claimed_identity_descriptor"] == "[protected]"
    assert body["evidence_refs"] == "[protected]"
    # Actor-level identity (actor_id, type, status) remains visible --
    # only claim content is redacted.
    assert body["actor_id"] == actor_id


def test_pseudonymous_actor_display_mode_visible_via_get_actor() -> None:
    actor_id = _register_actor(display_mode="pseudonymous")
    status, body = _get_json(f"{API_URL}/actors/{actor_id}")
    assert status == 200
    assert body["display_mode"] == "pseudonymous"
    assert "identity_continuity_key" not in body


def test_get_missing_actor_returns_404() -> None:
    status, body = _get_json(f"{API_URL}/actors/{_unique('iaa-api-missing-actor')}")
    assert status == 404
    assert "detail" in body


def test_get_missing_identity_claim_returns_404() -> None:
    status, body = _get_json(f"{API_URL}/identity-claims/{uuid.uuid4()}")
    assert status == 404
    assert "detail" in body


def test_get_missing_attestation_returns_404() -> None:
    status, body = _get_json(f"{API_URL}/attestations/{uuid.uuid4()}")
    assert status == 404
    assert "detail" in body


def test_deny_identity_claim_preserves_it_and_is_visible_via_get() -> None:
    actor_id = _register_actor()
    denier_id = _register_actor()
    claim_id = _submit_claim(actor_id)

    status, body = _post_json(
        f"{API_URL}/identity-claims/{claim_id}/deny",
        {"decided_by_actor_id": denier_id, "rationale": "Insufficient evidence."},
    )
    assert status == 200, f"expected 200, got {status}: {body}"
    assert body["identity_claim"]["recognition_status"] == "denied"

    get_status, get_body = _get_json(f"{API_URL}/identity-claims/{claim_id}")
    assert get_status == 200, "denied claim must still be retrievable, not erased"
    assert get_body["recognition_status"] == "denied"
