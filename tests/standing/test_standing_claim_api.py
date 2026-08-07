"""API round-trip tests for Standing Claims (RFC-CDP-033), scoped to
Constitutional Affected-Party Standing for the Challenge stage only,
against the running cdp-api.

Follows the pattern in
tests/universal_attestation/test_universal_attestation_api.py: assumes
the local Docker stack (`make up-build`) is already running, and talks to
it over plain HTTP with no cdp import required.

Requires 001, 004, 010, 011, 012, 014, and 015 already applied to the
database cdp-api is using.

Caller authentication (session 032 discipline, applied here from the
start): POST /standing-claims requires the claimant's own token. Both
determination routes (recognize, deny) each require a header matching
determined_by_actor_id -- see test_standing_claim_without_token_returns_401
and test_recognize_without_token_returns_401 below.

No /narrow route exists, deliberately (review finding on PR #53) -- see
test_narrow_route_does_not_exist below and cdp/api/standing.py's module
docstring for why.

Cleanup note: cdp_core.standing_claim and
cdp_core.standing_recognition_determination rows cannot be deleted or
updated (015 enforces both at the database level) -- see
tests/authority/test_authority_grant_api.py's module docstring for the
same reasoning applied there.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
import uuid
from datetime import UTC, datetime, timedelta

import pytest

API_URL = os.getenv("CDP_TEST_API_URL", "http://localhost:8000")
REGISTRY_NAME = "sample_attorney_demo"
DECISION_CLASS_ID = "claim_approval"

RECOGNITION_AUTHORITY_ACTOR_ID = "cdp_identity_recognition_authority"
GRANT_ISSUER_ACTOR_ID = "cdp_authority_grant_issuer"
STANDING_AUTHORITY_ACTOR_ID = "cdp_standing_recognition_authority"

# Fixed seed tokens for the three bounded system actors above, published
# in db/seed/dev-caller-authentication-tokens.sql for local/dev/test use
# -- never use these outside a local/test/demo environment.
RECOGNITION_AUTHORITY_TOKEN = (
    "seed-token-recognition-authority-local-dev-only-do-not-use-in-production"
)
GRANT_ISSUER_TOKEN = "seed-token-grant-issuer-local-dev-only-do-not-use-in-production"
STANDING_AUTHORITY_TOKEN = (
    "seed-token-standing-recognition-authority-local-dev-only-do-not-use-in-production"
)


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


def _register_actor(prefix: str = "standing-api-actor") -> tuple[str, str]:
    actor_id = _unique(prefix)
    status, body = _post_json(
        f"{API_URL}/actors",
        {
            "actor_id": actor_id,
            "actor_type": "human",
            "display_label": f"Standing test actor {actor_id}",
        },
    )
    assert status == 201, f"expected 201, got {status}: {body}"
    return actor_id, body["bearer_token"]


def _create_plain_decision(decision_id: str, subject_actor_id: str) -> None:
    status, body = _post_json(
        f"{API_URL}/decisions",
        {
            "registry_name": REGISTRY_NAME,
            "decision_id": decision_id,
            "decision_class_id": DECISION_CLASS_ID,
            "antecedent_text": "Standing API round-trip test decision.",
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


def _submit_and_recognize_identity_claim(actor_id: str, token: str) -> str:
    status, body = _post_json(
        f"{API_URL}/identity-claims",
        {
            "actor_id": actor_id,
            "claimant_actor_id": actor_id,
            "claimed_identity_descriptor": "Standing API round-trip descriptor.",
            "purpose_scope": "challenge_raising",
        },
        token=token,
    )
    assert status == 201, f"expected 201, got {status}: {body}"
    claim_id = body["identity_claim"]["claim_id"]

    status, body = _post_json(
        f"{API_URL}/identity-claims/{claim_id}/recognize",
        {"decided_by_actor_id": RECOGNITION_AUTHORITY_ACTOR_ID, "rationale": "Looks good."},
        token=RECOGNITION_AUTHORITY_TOKEN,
    )
    assert status == 200, f"expected 200, got {status}: {body}"
    return claim_id


def _grant_challenge_authority(actor_id: str) -> None:
    status, body = _post_json(
        f"{API_URL}/authority-grants",
        {
            "actor_id": actor_id,
            "authority": "CHALLENGE",
            "scope_registry_name": REGISTRY_NAME,
            "scope_decision_class_id": DECISION_CLASS_ID,
            "expires_at": (datetime.now(UTC) + timedelta(days=1)).isoformat(),
            "issued_by_actor_id": GRANT_ISSUER_ACTOR_ID,
            "basis": "policy",
        },
        token=GRANT_ISSUER_TOKEN,
    )
    assert status == 201, f"expected 201, got {status}: {body}"


def _standing_claim_payload(decision_id: str, actor_id: str, **overrides) -> dict:
    payload = {
        "decision_registry_name": REGISTRY_NAME,
        "decision_id": decision_id,
        "actor_id": actor_id,
        "claimed_impact": "This decision may materially affect me.",
        "standing_basis_contextual_relationship": "Adjacent property owner.",
    }
    payload.update(overrides)
    return payload


def _attestation_fields(actor_id: str, identity_claim_id: str) -> dict:
    return {
        "submitted_by_actor_id": actor_id,
        "identity_claim_id": identity_claim_id,
        "attestation_method": "shared_secret_reference",
        "credential_reference": _unique("standing-api-cred"),
        "issued_at": datetime.now(UTC).isoformat(),
    }


# --- Claim submission and GET ------------------------------------------------


def test_standing_claim_submit_and_get_round_trip() -> None:
    actor_id, token = _register_actor()
    decision_id = _unique("standing-api-decision")
    _create_plain_decision(decision_id, actor_id)

    status, body = _post_json(
        f"{API_URL}/standing-claims",
        _standing_claim_payload(decision_id, actor_id),
        token=token,
    )
    assert status == 201, f"expected 201, got {status}: {body}"
    claim = body["standing_claim"]
    assert claim["actor_id"] == actor_id
    assert claim["stage"] == "challenge"
    assert claim["standing_type"] == "constitutional_affected_party"
    claim_id = claim["claim_id"]

    get_status, get_body = _get_json(f"{API_URL}/standing-claims/{claim_id}")
    assert get_status == 200
    assert get_body["standing_claim"]["claim_id"] == claim_id
    assert get_body["standing_recognition_determination"] is None


def test_standing_claim_missing_basis_returns_422() -> None:
    actor_id, token = _register_actor()
    decision_id = _unique("standing-api-insufficient-decision")
    _create_plain_decision(decision_id, actor_id)

    status, body = _post_json(
        f"{API_URL}/standing-claims",
        _standing_claim_payload(
            decision_id,
            actor_id,
            claimed_impact="I might be affected somehow.",
            standing_basis_contextual_relationship=None,
        ),
        token=token,
    )
    assert status == 422, f"expected 422, got {status}: {body}"


def test_standing_claim_for_unknown_actor_returns_403_via_caller_binding() -> None:
    """Caller-binding is checked first, exactly as it is on every other
    caller-bound route since session 032 -- see
    evidence/003-known-gaps.md's Caller Authentication section, "actor
    not registered" note. Since no token could ever exist for an actor
    that was never registered, presenting an unrelated, valid token for a
    body that asserts an unknown actor_id always intercepts with 403
    (mismatch) before the service-layer ActorNotFound check would be
    reached -- ActorNotFound itself remains directly exercised at the
    service layer (tests/standing/test_standing_claim_service.py's
    test_claim_for_unknown_actor_fails)."""
    actor_id, token = _register_actor()
    decision_id = _unique("standing-api-unknown-actor-decision")
    _create_plain_decision(decision_id, actor_id)
    unknown_actor_id = _unique("standing-api-unknown-actor")

    status, body = _post_json(
        f"{API_URL}/standing-claims",
        _standing_claim_payload(decision_id, unknown_actor_id),
        token=token,
    )
    assert status == 403, f"expected 403, got {status}: {body}"


def test_get_missing_standing_claim_returns_404() -> None:
    status, body = _get_json(f"{API_URL}/standing-claims/{uuid.uuid4()}")
    assert status == 404
    assert "detail" in body


def test_standing_claim_without_token_returns_401() -> None:
    actor_id, _token = _register_actor()
    decision_id = _unique("standing-api-notoken-decision")
    _create_plain_decision(decision_id, actor_id)

    status, body = _post_json(
        f"{API_URL}/standing-claims", _standing_claim_payload(decision_id, actor_id)
    )
    assert status == 401, f"expected 401, got {status}: {body}"


# --- Determination routes ----------------------------------------------------


def test_recognize_and_deny_each_require_a_fresh_claim() -> None:
    actor_id, token = _register_actor()

    for outcome, route in (("recognized", "recognize"), ("denied", "deny")):
        decision_id = _unique(f"standing-api-{route}-decision")
        _create_plain_decision(decision_id, actor_id)
        claim_status, claim_body = _post_json(
            f"{API_URL}/standing-claims",
            _standing_claim_payload(decision_id, actor_id),
            token=token,
        )
        assert claim_status == 201
        claim_id = claim_body["standing_claim"]["claim_id"]

        status, body = _post_json(
            f"{API_URL}/standing-claims/{claim_id}/{route}",
            {
                "determined_by_actor_id": STANDING_AUTHORITY_ACTOR_ID,
                "outcome_basis": f"Test {route}.",
            },
            token=STANDING_AUTHORITY_TOKEN,
        )
        assert status == 200, f"expected 200, got {status}: {body}"
        assert body["standing_recognition_determination"]["outcome"] == outcome

        get_status, get_body = _get_json(f"{API_URL}/standing-claims/{claim_id}")
        assert get_status == 200
        assert get_body["standing_recognition_determination"]["outcome"] == outcome


def test_narrow_route_does_not_exist() -> None:
    """No /narrow route exists, deliberately (review finding on PR #53):
    this table has no outcome_scope column to record what a narrowing
    narrows to. FastAPI's own 404 for an unregistered path proves the
    route is genuinely gone, not merely undocumented."""
    actor_id, token = _register_actor()
    decision_id = _unique("standing-api-no-narrow-route-decision")
    _create_plain_decision(decision_id, actor_id)
    claim_id = _post_json(
        f"{API_URL}/standing-claims", _standing_claim_payload(decision_id, actor_id), token=token
    )[1]["standing_claim"]["claim_id"]

    status, _body = _post_json(
        f"{API_URL}/standing-claims/{claim_id}/narrow",
        {
            "determined_by_actor_id": STANDING_AUTHORITY_ACTOR_ID,
            "outcome_basis": "Should not exist.",
        },
        token=STANDING_AUTHORITY_TOKEN,
    )
    assert status == 404, f"expected 404 (no such route), got {status}"


def test_self_recognition_returns_403() -> None:
    actor_id, token = _register_actor()
    decision_id = _unique("standing-api-self-recognize-decision")
    _create_plain_decision(decision_id, actor_id)
    claim_id = _post_json(
        f"{API_URL}/standing-claims", _standing_claim_payload(decision_id, actor_id), token=token
    )[1]["standing_claim"]["claim_id"]

    status, body = _post_json(
        f"{API_URL}/standing-claims/{claim_id}/recognize",
        {"determined_by_actor_id": actor_id, "outcome_basis": "I recognize myself."},
        token=token,
    )
    assert status == 403, f"expected 403, got {status}: {body}"


def test_recognize_by_unauthorized_actor_returns_403() -> None:
    actor_id, token = _register_actor()
    unrelated_actor_id, unrelated_token = _register_actor("standing-api-unrelated")
    decision_id = _unique("standing-api-unauth-decision")
    _create_plain_decision(decision_id, actor_id)
    claim_id = _post_json(
        f"{API_URL}/standing-claims", _standing_claim_payload(decision_id, actor_id), token=token
    )[1]["standing_claim"]["claim_id"]

    status, body = _post_json(
        f"{API_URL}/standing-claims/{claim_id}/recognize",
        {"determined_by_actor_id": unrelated_actor_id, "outcome_basis": "I say so."},
        token=unrelated_token,
    )
    assert status == 403, f"expected 403, got {status}: {body}"


def test_second_determination_returns_409() -> None:
    actor_id, token = _register_actor()
    decision_id = _unique("standing-api-double-determine-decision")
    _create_plain_decision(decision_id, actor_id)
    claim_id = _post_json(
        f"{API_URL}/standing-claims", _standing_claim_payload(decision_id, actor_id), token=token
    )[1]["standing_claim"]["claim_id"]
    _post_json(
        f"{API_URL}/standing-claims/{claim_id}/recognize",
        {"determined_by_actor_id": STANDING_AUTHORITY_ACTOR_ID, "outcome_basis": "First."},
        token=STANDING_AUTHORITY_TOKEN,
    )

    status, body = _post_json(
        f"{API_URL}/standing-claims/{claim_id}/deny",
        {"determined_by_actor_id": STANDING_AUTHORITY_ACTOR_ID, "outcome_basis": "Second."},
        token=STANDING_AUTHORITY_TOKEN,
    )
    assert status == 409, f"expected 409, got {status}: {body}"


def test_recognize_without_token_returns_401() -> None:
    actor_id, token = _register_actor()
    decision_id = _unique("standing-api-recognize-notoken-decision")
    _create_plain_decision(decision_id, actor_id)
    claim_id = _post_json(
        f"{API_URL}/standing-claims", _standing_claim_payload(decision_id, actor_id), token=token
    )[1]["standing_claim"]["claim_id"]

    status, body = _post_json(
        f"{API_URL}/standing-claims/{claim_id}/recognize",
        {"determined_by_actor_id": STANDING_AUTHORITY_ACTOR_ID, "outcome_basis": "No token."},
    )
    assert status == 401, f"expected 401, got {status}: {body}"


def test_recognize_missing_claim_returns_404() -> None:
    status, body = _post_json(
        f"{API_URL}/standing-claims/{uuid.uuid4()}/recognize",
        {"determined_by_actor_id": STANDING_AUTHORITY_ACTOR_ID, "outcome_basis": "N/A"},
        token=STANDING_AUTHORITY_TOKEN,
    )
    assert status == 404, f"expected 404, got {status}: {body}"


# --- Standing gate on attested Challenge --------------------------------------


def test_pending_standing_claim_permits_attested_challenge() -> None:
    actor_id, token = _register_actor("standing-api-gate-provisional")
    decision_id = _unique("standing-api-gate-provisional-decision")
    _create_plain_decision(decision_id, actor_id)
    identity_claim_id = _submit_and_recognize_identity_claim(actor_id, token)
    _grant_challenge_authority(actor_id)

    standing_claim_id = _post_json(
        f"{API_URL}/standing-claims", _standing_claim_payload(decision_id, actor_id), token=token
    )[1]["standing_claim"]["claim_id"]

    status, body = _post_json(
        f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/attested-challenges",
        {
            "challenge_text": "I object as an affected party.",
            "standing_claim_id": standing_claim_id,
            **_attestation_fields(actor_id, identity_claim_id),
        },
        token=token,
    )
    assert status == 201, f"expected 201, got {status}: {body}"
    assert body["standing_claim"]["claim_id"] == standing_claim_id
    assert body["challenge"]["raised_by_actor_id"] == actor_id


def test_denied_standing_claim_blocks_attested_challenge() -> None:
    actor_id, token = _register_actor("standing-api-gate-denied")
    decision_id = _unique("standing-api-gate-denied-decision")
    _create_plain_decision(decision_id, actor_id)
    identity_claim_id = _submit_and_recognize_identity_claim(actor_id, token)
    _grant_challenge_authority(actor_id)

    standing_claim_id = _post_json(
        f"{API_URL}/standing-claims", _standing_claim_payload(decision_id, actor_id), token=token
    )[1]["standing_claim"]["claim_id"]
    _post_json(
        f"{API_URL}/standing-claims/{standing_claim_id}/deny",
        {
            "determined_by_actor_id": STANDING_AUTHORITY_ACTOR_ID,
            "outcome_basis": "No consequence shown.",
        },
        token=STANDING_AUTHORITY_TOKEN,
    )

    status, body = _post_json(
        f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/attested-challenges",
        {
            "challenge_text": "Should not be permitted.",
            "standing_claim_id": standing_claim_id,
            **_attestation_fields(actor_id, identity_claim_id),
        },
        token=token,
    )
    assert status == 403, f"expected 403, got {status}: {body}"


def test_attested_challenge_without_standing_claim_id_is_unaffected() -> None:
    """The Standing gate is opt-in -- omitting standing_claim_id must
    behave exactly as it did before this slice existed."""
    actor_id, token = _register_actor("standing-api-gate-omitted")
    decision_id = _unique("standing-api-gate-omitted-decision")
    _create_plain_decision(decision_id, actor_id)
    identity_claim_id = _submit_and_recognize_identity_claim(actor_id, token)
    _grant_challenge_authority(actor_id)

    status, body = _post_json(
        f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/attested-challenges",
        {
            "challenge_text": "No standing claim referenced.",
            **_attestation_fields(actor_id, identity_claim_id),
        },
        token=token,
    )
    assert status == 201, f"expected 201, got {status}: {body}"
    assert body["standing_claim"] is None
