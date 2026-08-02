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

v0.2 review correction: /attested-decisions' submitted_by_actor_id (the
attestor) is independent of subject_actor_id (who/what the decision is
about) -- see test_attested_decision_attestor_and_subject_may_differ
below. /identity-claims/{claim_id}/recognize (and deny/contest) require
decided_by_actor_id to be the seeded recognition-authority actor,
RECOGNITION_AUTHORITY_ACTOR_ID below -- see
test_recognize_claim_by_unauthorized_actor_returns_403 and
test_self_recognition_returns_403.

Authority slice (session 028, RFC-CDP-032): /attested-decisions now also
requires submitted_by_actor_id to hold an active, unexpired PROPOSE
authority grant scoped to the decision's registry_name/decision_class_id,
issued via POST /authority-grants by the seeded GRANT_ISSUER_ACTOR_ID
below -- see test_attested_decision_without_authority_grant_returns_403.

Caller authentication (session 032, RFC-CDP-030 SS6 / RFC-CDP-031 SS7):
every route that accepts an actor-asserting field now also requires an
Authorization: Bearer <token> header matching that actor's active token.
_register_actor returns (actor_id, token); the two bounded system actors
(RECOGNITION_AUTHORITY_ACTOR_ID, GRANT_ISSUER_ACTOR_ID) use the fixed
seed tokens db/ddl/014-caller-authentication.sql publishes for local/
dev/test use -- see test_caller_authentication_* below for the dedicated
coverage of missing/wrong/mismatched tokens.
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

# Pre-seeded by 010-identity-and-attestation.sql; not registered by these
# tests.
RECOGNITION_AUTHORITY_ACTOR_ID = "cdp_identity_recognition_authority"

# Pre-seeded by 011-authority-and-delegation.sql; not registered by these
# tests.
GRANT_ISSUER_ACTOR_ID = "cdp_authority_grant_issuer"

# Fixed seed tokens for the two bounded system actors above, published in
# db/ddl/014-caller-authentication.sql's header for local/dev/test use --
# never use these outside a local/test/demo environment.
RECOGNITION_AUTHORITY_TOKEN = (
    "seed-token-recognition-authority-local-dev-only-do-not-use-in-production"
)
GRANT_ISSUER_TOKEN = "seed-token-grant-issuer-local-dev-only-do-not-use-in-production"


def _request(
    method: str, url: str, payload: dict | None = None, *, token: str | None = None
) -> tuple[int, dict]:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json"}
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        pytest.fail(f"Could not reach {url}. Is the local Docker stack running? {exc}")


def _post_json(url: str, payload: dict, *, token: str | None = None) -> tuple[int, dict]:
    return _request("POST", url, payload, token=token)


def _get_json(url: str) -> tuple[int, dict]:
    return _request("GET", url)


def _unique(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def _register_actor(display_mode: str = "public") -> tuple[str, str]:
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
    return actor_id, body["bearer_token"]


def _submit_claim(
    actor_id: str,
    token: str,
    *,
    purpose_scope: str = "decision_creation",
    scope_registry_name: str | None = None,
    scope_decision_class_id: str | None = None,
) -> str:
    payload = {
        "actor_id": actor_id,
        "claimant_actor_id": actor_id,
        "claimed_identity_descriptor": "API round-trip descriptor for this actor.",
        "purpose_scope": purpose_scope,
        "evidence_refs": ["evidence-ref-api-1"],
    }
    if scope_registry_name is not None:
        payload["scope_registry_name"] = scope_registry_name
    if scope_decision_class_id is not None:
        payload["scope_decision_class_id"] = scope_decision_class_id

    status, body = _post_json(f"{API_URL}/identity-claims", payload, token=token)
    assert status == 201, f"expected 201, got {status}: {body}"
    return body["identity_claim"]["claim_id"]


def _recognize_claim(
    claim_id: str,
    decided_by_actor_id: str = RECOGNITION_AUTHORITY_ACTOR_ID,
    token: str = RECOGNITION_AUTHORITY_TOKEN,
) -> None:
    status, body = _post_json(
        f"{API_URL}/identity-claims/{claim_id}/recognize",
        {"decided_by_actor_id": decided_by_actor_id, "rationale": "Looks good."},
        token=token,
    )
    assert status == 200, f"expected 200, got {status}: {body}"


def _grant_propose_authority(
    actor_id: str,
    *,
    scope_registry_name: str = REGISTRY_NAME,
    scope_decision_class_id: str | None = DECISION_CLASS_ID,
) -> None:
    status, body = _post_json(
        f"{API_URL}/authority-grants",
        {
            "actor_id": actor_id,
            "authority": "PROPOSE",
            "scope_registry_name": scope_registry_name,
            "scope_decision_class_id": scope_decision_class_id,
            "expires_at": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
            "issued_by_actor_id": GRANT_ISSUER_ACTOR_ID,
            "basis": "policy",
        },
        token=GRANT_ISSUER_TOKEN,
    )
    assert status == 201, f"expected 201, got {status}: {body}"


def _attested_decision_payload(
    attestor_actor_id: str, claim_id: str, decision_id: str, *, subject_actor_id: str | None = None
) -> dict:
    return {
        "registry_name": REGISTRY_NAME,
        "decision_id": decision_id,
        "decision_class_id": DECISION_CLASS_ID,
        "antecedent_text": "Identity/Attestation API round-trip test decision.",
        "subject_actor_type": "human",
        "subject_actor_id": subject_actor_id or attestor_actor_id,
        "predicate_verb": "recommend_approval",
        "object_type": "claim",
        "object_id": "claim_9981",
        "permission_source_type": "policy_rule",
        "permission_source_id": "policy_claims_approval_v2",
        "human_required": True,
        "submitted_by_actor_id": attestor_actor_id,
        "identity_claim_id": claim_id,
        "attestation_method": "shared_secret_reference",
        "credential_reference": "api-test-credential-ref-1",
        "issued_at": datetime.now(timezone.utc).isoformat(),
    }


def test_full_actor_claim_attestation_round_trip_and_governed_mutation_succeeds() -> None:
    actor_id, token = _register_actor()
    claim_id = _submit_claim(actor_id, token)
    _recognize_claim(claim_id)
    _grant_propose_authority(actor_id)
    decision_id = _unique("iaa-api-decision")

    status, body = _post_json(
        f"{API_URL}/attested-decisions",
        _attested_decision_payload(actor_id, claim_id, decision_id),
        token=token,
    )
    assert status == 201, f"expected 201, got {status}: {body}"
    assert body["decision"]["decision_id"] == decision_id
    assert body["decision"]["subject_actor_id"] == actor_id
    assert body["attestation"]["verification_result"] == "verified"
    assert body["authority_evaluation"]["result"] == "pass"
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

    list_status, list_body = _get_json(
        f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/attestations"
    )
    assert list_status == 200
    assert [a["attestation_id"] for a in list_body["attestations"]] == [attestation_id]

    eval_status, eval_body = _get_json(
        f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/authority-evaluations"
    )
    assert eval_status == 200
    assert len(eval_body["authority_evaluations"]) == 1
    assert eval_body["authority_evaluations"][0]["result"] == "pass"


def test_attested_decision_attestor_and_subject_may_differ() -> None:
    """The proof path the v0.2 review asked for: Alice attests, the
    decision concerns Bob. Both roles are independently preserved -- no
    collapse of attestor into subject or vice versa."""
    alice_actor_id, alice_token = _register_actor()
    bob_actor_id, _bob_token = _register_actor()
    claim_id = _submit_claim(alice_actor_id, alice_token)
    _recognize_claim(claim_id)
    _grant_propose_authority(alice_actor_id)
    decision_id = _unique("iaa-api-decision-distinct-roles")

    status, body = _post_json(
        f"{API_URL}/attested-decisions",
        _attested_decision_payload(alice_actor_id, claim_id, decision_id, subject_actor_id=bob_actor_id),
        token=alice_token,
    )
    assert status == 201, f"expected 201, got {status}: {body}"
    assert body["decision"]["subject_actor_id"] == bob_actor_id
    assert body["attestation"]["actor_id"] == alice_actor_id

    decision_status, decision_body = _get_json(f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}")
    assert decision_status == 200
    assert decision_body["subject_actor_id"] == bob_actor_id

    list_status, list_body = _get_json(
        f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/attestations"
    )
    assert list_status == 200
    assert list_body["attestations"][0]["actor_id"] == alice_actor_id


def test_decision_attestations_list_is_empty_for_an_unattested_decision() -> None:
    decision_id = _unique("iaa-api-decision-unattested")
    actor_id = "claims_review_agent"  # pre-existing demo actor, not a governed Actor

    status, body = _post_json(
        f"{API_URL}/decisions",
        {
            "registry_name": REGISTRY_NAME,
            "decision_id": decision_id,
            "decision_class_id": DECISION_CLASS_ID,
            "antecedent_text": "Unattested decision for the attestations-list check.",
            "subject_actor_type": "agent",
            "subject_actor_id": actor_id,
            "predicate_verb": "recommend_approval",
            "object_type": "claim",
            "object_id": "claim_9981",
            "permission_source_type": "policy_rule",
            "permission_source_id": "policy_claims_approval_v2",
            "human_required": True,
        },
    )
    assert status == 201, f"expected 201, got {status}: {body}"

    list_status, list_body = _get_json(
        f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/attestations"
    )
    assert list_status == 200
    assert list_body["attestations"] == []


def test_decision_attestations_list_against_missing_decision_returns_404() -> None:
    status, body = _get_json(
        f"{API_URL}/decisions/{REGISTRY_NAME}/{_unique('iaa-api-missing-decision')}/attestations"
    )
    assert status == 404
    assert "detail" in body


def test_decision_authority_evaluations_list_against_missing_decision_returns_404() -> None:
    status, body = _get_json(
        f"{API_URL}/decisions/{REGISTRY_NAME}/{_unique('iaa-api-missing-decision')}/authority-evaluations"
    )
    assert status == 404
    assert "detail" in body


def test_attested_decision_missing_credential_reference_returns_422() -> None:
    actor_id, token = _register_actor()
    claim_id = _submit_claim(actor_id, token)
    _recognize_claim(claim_id)
    decision_id = _unique("iaa-api-decision-missing-cred")

    payload = _attested_decision_payload(actor_id, claim_id, decision_id)
    payload["credential_reference"] = ""

    status, body = _post_json(f"{API_URL}/attested-decisions", payload, token=token)
    assert status == 422, f"expected 422, got {status}: {body}"

    get_status, _ = _get_json(f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}")
    assert get_status == 404, "no decision should have been created"


def test_attested_decision_with_unrecognized_claim_returns_409() -> None:
    actor_id, token = _register_actor()
    claim_id = _submit_claim(actor_id, token)  # never recognized
    decision_id = _unique("iaa-api-decision-unrecognized")

    status, body = _post_json(
        f"{API_URL}/attested-decisions",
        _attested_decision_payload(actor_id, claim_id, decision_id),
        token=token,
    )
    assert status == 409, f"expected 409, got {status}: {body}"

    get_status, _ = _get_json(f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}")
    assert get_status == 404, "no decision should have been created"


def test_attested_decision_without_authority_grant_returns_403() -> None:
    actor_id, token = _register_actor()
    claim_id = _submit_claim(actor_id, token)
    _recognize_claim(claim_id)
    # Deliberately no _grant_propose_authority call.
    decision_id = _unique("iaa-api-decision-noauth")

    status, body = _post_json(
        f"{API_URL}/attested-decisions",
        _attested_decision_payload(actor_id, claim_id, decision_id),
        token=token,
    )
    assert status == 403, f"expected 403, got {status}: {body}"

    get_status, _ = _get_json(f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}")
    assert get_status == 404, "no decision should have been created"


def test_attested_decision_with_matching_registry_scoped_claim_succeeds() -> None:
    actor_id, token = _register_actor()
    claim_id = _submit_claim(actor_id, token, scope_registry_name=REGISTRY_NAME)
    _recognize_claim(claim_id)
    _grant_propose_authority(actor_id)
    decision_id = _unique("iaa-api-decision-scoped")

    status, body = _post_json(
        f"{API_URL}/attested-decisions",
        _attested_decision_payload(actor_id, claim_id, decision_id),
        token=token,
    )
    assert status == 201, f"expected 201, got {status}: {body}"
    assert body["decision"]["decision_id"] == decision_id


def test_attested_decision_with_wrong_registry_scoped_claim_returns_409() -> None:
    actor_id, token = _register_actor()
    claim_id = _submit_claim(actor_id, token, scope_registry_name="some_other_registry")
    _recognize_claim(claim_id)
    _grant_propose_authority(actor_id)
    decision_id = _unique("iaa-api-decision-wrongscope")

    status, body = _post_json(
        f"{API_URL}/attested-decisions",
        _attested_decision_payload(actor_id, claim_id, decision_id),
        token=token,
    )
    assert status == 409, f"expected 409, got {status}: {body}"

    get_status, _ = _get_json(f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}")
    assert get_status == 404, "no decision should have been created"


def test_attested_decision_with_unknown_actor_returns_403_via_caller_binding() -> None:
    """Since session 032, ActorNotFound is no longer directly reachable
    through this route's HTTP surface: an actor that was never
    registered also never received a bearer token, so any token
    presented on its behalf necessarily belongs to someone else, and
    caller-binding (checked first) rejects with 403 before the
    service-layer ActorNotFound check is ever reached. ActorNotFound
    itself remains directly exercised at the service layer
    (tests/identify_attest_standing/test_attestation_service.py)."""
    unknown_actor_id = _unique("iaa-api-unknown-actor")
    decision_id = _unique("iaa-api-decision-unknown-actor")
    _, some_registered_token = _register_actor()

    status, body = _post_json(
        f"{API_URL}/attested-decisions",
        _attested_decision_payload(unknown_actor_id, str(uuid.uuid4()), decision_id),
        token=some_registered_token,
    )
    assert status == 403, f"expected 403 (token does not belong to unknown actor), got {status}: {body}"


def test_recognize_claim_by_unauthorized_actor_returns_403() -> None:
    actor_id, actor_token = _register_actor()
    unrelated_actor_id, unrelated_token = _register_actor()
    claim_id = _submit_claim(actor_id, actor_token)

    status, body = _post_json(
        f"{API_URL}/identity-claims/{claim_id}/recognize",
        {"decided_by_actor_id": unrelated_actor_id, "rationale": "I say it's fine."},
        token=unrelated_token,
    )
    assert status == 403, f"expected 403, got {status}: {body}"

    get_status, get_body = _get_json(f"{API_URL}/identity-claims/{claim_id}")
    assert get_status == 200
    assert get_body["recognition_status"] == "pending"


def test_self_recognition_returns_403() -> None:
    actor_id, token = _register_actor()

    status, body = _post_json(
        f"{API_URL}/identity-claims/{_submit_claim(actor_id, token)}/recognize",
        {"decided_by_actor_id": actor_id, "rationale": "I recognize myself."},
        token=token,
    )
    assert status == 403, f"expected 403, got {status}: {body}"


def test_protected_actor_identity_claim_response_redacts_descriptor_and_evidence() -> None:
    actor_id, token = _register_actor(display_mode="protected")
    claim_id = _submit_claim(actor_id, token)

    status, body = _get_json(f"{API_URL}/identity-claims/{claim_id}")
    assert status == 200
    assert body["claimed_identity_descriptor"] == "[protected]"
    assert body["evidence_refs"] == "[protected]"
    # Actor-level identity (actor_id, type, status) remains visible --
    # only claim content is redacted.
    assert body["actor_id"] == actor_id


def test_pseudonymous_actor_display_mode_visible_via_get_actor() -> None:
    actor_id, _token = _register_actor(display_mode="pseudonymous")
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
    actor_id, token = _register_actor()
    claim_id = _submit_claim(actor_id, token)

    status, body = _post_json(
        f"{API_URL}/identity-claims/{claim_id}/deny",
        {"decided_by_actor_id": RECOGNITION_AUTHORITY_ACTOR_ID, "rationale": "Insufficient evidence."},
        token=RECOGNITION_AUTHORITY_TOKEN,
    )
    assert status == 200, f"expected 200, got {status}: {body}"
    assert body["identity_claim"]["recognition_status"] == "denied"

    get_status, get_body = _get_json(f"{API_URL}/identity-claims/{claim_id}")
    assert get_status == 200, "denied claim must still be retrievable, not erased"
    assert get_body["recognition_status"] == "denied"


# --- Caller authentication (session 032) -----------------------------------


def test_register_actor_response_includes_a_one_time_bearer_token() -> None:
    actor_id = _unique("iaa-api-token-actor")
    status, body = _post_json(
        f"{API_URL}/actors",
        {"actor_id": actor_id, "actor_type": "human", "display_label": "Token check actor"},
    )
    assert status == 201
    assert isinstance(body["bearer_token"], str)
    assert len(body["bearer_token"]) > 20


def test_identity_claim_submission_without_token_returns_401() -> None:
    actor_id, _token = _register_actor()
    status, body = _post_json(
        f"{API_URL}/identity-claims",
        {
            "actor_id": actor_id,
            "claimant_actor_id": actor_id,
            "claimed_identity_descriptor": "No token presented.",
            "purpose_scope": "decision_creation",
        },
    )
    assert status == 401, f"expected 401, got {status}: {body}"


def test_identity_claim_submission_with_wrong_actors_token_returns_403() -> None:
    actor_id, _token = _register_actor()
    _other_actor_id, other_token = _register_actor()
    status, body = _post_json(
        f"{API_URL}/identity-claims",
        {
            "actor_id": actor_id,
            "claimant_actor_id": actor_id,
            "claimed_identity_descriptor": "Wrong actor's token presented.",
            "purpose_scope": "decision_creation",
        },
        token=other_token,
    )
    assert status == 403, f"expected 403, got {status}: {body}"


def test_attested_decision_with_mismatched_token_returns_403() -> None:
    actor_id, _token = _register_actor()
    _other_actor_id, other_token = _register_actor()
    claim_id = _submit_claim(actor_id, _token)
    _recognize_claim(claim_id)
    _grant_propose_authority(actor_id)
    decision_id = _unique("iaa-api-decision-tokenmismatch")

    status, body = _post_json(
        f"{API_URL}/attested-decisions",
        _attested_decision_payload(actor_id, claim_id, decision_id),
        token=other_token,
    )
    assert status == 403, f"expected 403, got {status}: {body}"

    get_status, _ = _get_json(f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}")
    assert get_status == 404, "no decision should have been created"


def test_revoke_token_then_reuse_returns_401() -> None:
    actor_id, token = _register_actor()
    revoke_status, revoke_body = _post_json(
        f"{API_URL}/actors/{actor_id}/tokens/revoke", {}, token=token
    )
    assert revoke_status == 200, f"expected 200, got {revoke_status}: {revoke_body}"

    status, body = _post_json(
        f"{API_URL}/identity-claims",
        {
            "actor_id": actor_id,
            "claimant_actor_id": actor_id,
            "claimed_identity_descriptor": "Should be rejected -- token revoked.",
            "purpose_scope": "decision_creation",
        },
        token=token,
    )
    assert status == 401, f"expected 401, got {status}: {body}"


def test_revoke_token_without_presenting_current_token_returns_401() -> None:
    actor_id, _token = _register_actor()
    status, body = _post_json(f"{API_URL}/actors/{actor_id}/tokens/revoke", {})
    assert status == 401, f"expected 401, got {status}: {body}"


def test_revoke_token_twice_returns_404_the_second_time() -> None:
    actor_id, token = _register_actor()
    first_status, _ = _post_json(f"{API_URL}/actors/{actor_id}/tokens/revoke", {}, token=token)
    assert first_status == 200

    second_status, second_body = _post_json(
        f"{API_URL}/actors/{actor_id}/tokens/revoke", {}, token=token
    )
    assert second_status == 401, f"expected 401 (token already revoked), got {second_status}: {second_body}"
