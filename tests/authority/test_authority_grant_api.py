"""API round-trip tests for Authority Grants (RFC-CDP-032 Authority and
Delegation Model, scoped to SS19 Minimal Compliance) against the running
cdp-api.

Follows the pattern in tests/identify_attest_standing/test_identity_attestation_api.py:
assumes the local Docker stack (`make up-build`) is already running, and
talks to it over plain HTTP with no cdp import required.

Requires 001, 011, and 014 already applied to the database cdp-api is
using.

Cleanup note: cdp_core.authority_grant rows cannot be deleted (011
enforces this at the database level) -- see
tests/identify_attest_standing/test_actor_service.py's module docstring
for the same reasoning applied there.

Caller authentication (session 032): POST /authority-grants and POST
/authority-grants/{grant_id}/revoke both also require an Authorization:
Bearer <token> header matching cdp_authority_grant_issuer's own fixed
seed token, published in db/ddl/014-caller-authentication.sql's header
for local/dev/test use. A request presenting a *different*, still-valid
actor's token now fails caller-binding (403) before ever reaching the
service-layer AuthorityGrantIssuerRequired check -- see
test_grant_by_unauthorized_actor_returns_403 and
test_revoke_by_unauthorized_actor_returns_403 below, which now use the
unrelated actor's own real token specifically so the test still exercises
AuthorityGrantIssuerRequired, not just caller-binding.
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

# Pre-seeded by 011-authority-and-delegation.sql; not registered by these
# tests.
GRANT_ISSUER_ACTOR_ID = "cdp_authority_grant_issuer"

# Fixed seed token for GRANT_ISSUER_ACTOR_ID, published in
# db/ddl/014-caller-authentication.sql's header for local/dev/test use --
# never use this outside a local/test/demo environment.
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


def _register_actor() -> tuple[str, str]:
    actor_id = _unique("iaa-api-authority-actor")
    status, body = _post_json(
        f"{API_URL}/actors",
        {"actor_id": actor_id, "actor_type": "human", "display_label": f"Authority test actor {actor_id}"},
    )
    assert status == 201, f"expected 201, got {status}: {body}"
    return actor_id, body["bearer_token"]


def _grant_payload(actor_id: str, **overrides) -> dict:
    payload = {
        "actor_id": actor_id,
        "authority": "PROPOSE",
        "scope_registry_name": "sample_attorney_demo",
        "scope_decision_class_id": "claim_approval",
        "expires_at": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
        "issued_by_actor_id": GRANT_ISSUER_ACTOR_ID,
        "basis": "policy",
    }
    payload.update(overrides)
    return payload


def test_grant_get_and_revoke_round_trip() -> None:
    actor_id, _token = _register_actor()

    status, body = _post_json(
        f"{API_URL}/authority-grants", _grant_payload(actor_id), token=GRANT_ISSUER_TOKEN
    )
    assert status == 201, f"expected 201, got {status}: {body}"
    grant = body["authority_grant"]
    assert grant["actor_id"] == actor_id
    assert grant["status"] == "active"
    grant_id = grant["authority_grant_id"]

    get_status, get_body = _get_json(f"{API_URL}/authority-grants/{grant_id}")
    assert get_status == 200
    assert get_body["authority_grant_id"] == grant_id
    assert get_body["status"] == "active"

    revoke_status, revoke_body = _post_json(
        f"{API_URL}/authority-grants/{grant_id}/revoke",
        {"revoked_by_actor_id": GRANT_ISSUER_ACTOR_ID, "reason": "API round-trip test cleanup."},
        token=GRANT_ISSUER_TOKEN,
    )
    assert revoke_status == 200, f"expected 200, got {revoke_status}: {revoke_body}"
    assert revoke_body["authority_grant"]["status"] == "revoked"

    get_after_status, get_after_body = _get_json(f"{API_URL}/authority-grants/{grant_id}")
    assert get_after_status == 200, "a revoked grant must still be retrievable, not erased"
    assert get_after_body["status"] == "revoked"


def test_wildcard_scope_grant_has_null_decision_class() -> None:
    actor_id, _token = _register_actor()
    status, body = _post_json(
        f"{API_URL}/authority-grants",
        _grant_payload(actor_id, scope_decision_class_id=None),
        token=GRANT_ISSUER_TOKEN,
    )
    assert status == 201, f"expected 201, got {status}: {body}"
    assert body["authority_grant"]["scope_decision_class_id"] is None


def test_grant_by_unauthorized_actor_returns_403() -> None:
    actor_id, _token = _register_actor()
    unrelated_actor_id, unrelated_token = _register_actor()

    status, body = _post_json(
        f"{API_URL}/authority-grants",
        _grant_payload(actor_id, issued_by_actor_id=unrelated_actor_id),
        token=unrelated_token,
    )
    assert status == 403, f"expected 403, got {status}: {body}"


def test_grant_for_unknown_actor_returns_404() -> None:
    unknown_actor_id = _unique("iaa-api-authority-unknown")
    status, body = _post_json(
        f"{API_URL}/authority-grants", _grant_payload(unknown_actor_id), token=GRANT_ISSUER_TOKEN
    )
    assert status == 404, f"expected 404, got {status}: {body}"


def test_revoke_by_unauthorized_actor_returns_403() -> None:
    actor_id, _token = _register_actor()
    unrelated_actor_id, unrelated_token = _register_actor()
    grant_id = _post_json(
        f"{API_URL}/authority-grants", _grant_payload(actor_id), token=GRANT_ISSUER_TOKEN
    )[1]["authority_grant"]["authority_grant_id"]

    status, body = _post_json(
        f"{API_URL}/authority-grants/{grant_id}/revoke",
        {"revoked_by_actor_id": unrelated_actor_id, "reason": "I say so."},
        token=unrelated_token,
    )
    assert status == 403, f"expected 403, got {status}: {body}"


def test_revoke_already_revoked_grant_returns_409() -> None:
    actor_id, _token = _register_actor()
    grant_id = _post_json(
        f"{API_URL}/authority-grants", _grant_payload(actor_id), token=GRANT_ISSUER_TOKEN
    )[1]["authority_grant"]["authority_grant_id"]
    _post_json(
        f"{API_URL}/authority-grants/{grant_id}/revoke",
        {"revoked_by_actor_id": GRANT_ISSUER_ACTOR_ID, "reason": "First revocation."},
        token=GRANT_ISSUER_TOKEN,
    )

    status, body = _post_json(
        f"{API_URL}/authority-grants/{grant_id}/revoke",
        {"revoked_by_actor_id": GRANT_ISSUER_ACTOR_ID, "reason": "Second revocation."},
        token=GRANT_ISSUER_TOKEN,
    )
    assert status == 409, f"expected 409, got {status}: {body}"


def test_revoke_unknown_grant_returns_404() -> None:
    status, body = _post_json(
        f"{API_URL}/authority-grants/{uuid.uuid4()}/revoke",
        {"revoked_by_actor_id": GRANT_ISSUER_ACTOR_ID, "reason": "N/A"},
        token=GRANT_ISSUER_TOKEN,
    )
    assert status == 404, f"expected 404, got {status}: {body}"


def test_get_missing_authority_grant_returns_404() -> None:
    status, body = _get_json(f"{API_URL}/authority-grants/{uuid.uuid4()}")
    assert status == 404
    assert "detail" in body


# --- Caller authentication (session 032) -----------------------------------


def test_grant_without_token_returns_401() -> None:
    actor_id, _token = _register_actor()
    status, body = _post_json(f"{API_URL}/authority-grants", _grant_payload(actor_id))
    assert status == 401, f"expected 401, got {status}: {body}"


def test_revoke_without_token_returns_401() -> None:
    actor_id, _token = _register_actor()
    grant_id = _post_json(
        f"{API_URL}/authority-grants", _grant_payload(actor_id), token=GRANT_ISSUER_TOKEN
    )[1]["authority_grant"]["authority_grant_id"]

    status, body = _post_json(
        f"{API_URL}/authority-grants/{grant_id}/revoke",
        {"revoked_by_actor_id": GRANT_ISSUER_ACTOR_ID, "reason": "No token presented."},
    )
    assert status == 401, f"expected 401, got {status}: {body}"
