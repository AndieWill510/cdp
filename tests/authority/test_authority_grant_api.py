"""API round-trip tests for Authority Grants (RFC-CDP-032 Authority and
Delegation Model, scoped to SS19 Minimal Compliance) against the running
cdp-api.

Follows the pattern in tests/identify_attest_standing/test_identity_attestation_api.py:
assumes the local Docker stack (`make up-build`) is already running, and
talks to it over plain HTTP with no cdp import required.

Requires 001 and 011 already applied to the database cdp-api is using.

Cleanup note: cdp_core.authority_grant rows cannot be deleted (011
enforces this at the database level) -- see
tests/identify_attest_standing/test_actor_service.py's module docstring
for the same reasoning applied there.
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


def _register_actor() -> str:
    actor_id = _unique("iaa-api-authority-actor")
    status, body = _post_json(
        f"{API_URL}/actors",
        {"actor_id": actor_id, "actor_type": "human", "display_label": f"Authority test actor {actor_id}"},
    )
    assert status == 201, f"expected 201, got {status}: {body}"
    return actor_id


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
    actor_id = _register_actor()

    status, body = _post_json(f"{API_URL}/authority-grants", _grant_payload(actor_id))
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
    )
    assert revoke_status == 200, f"expected 200, got {revoke_status}: {revoke_body}"
    assert revoke_body["authority_grant"]["status"] == "revoked"

    get_after_status, get_after_body = _get_json(f"{API_URL}/authority-grants/{grant_id}")
    assert get_after_status == 200, "a revoked grant must still be retrievable, not erased"
    assert get_after_body["status"] == "revoked"


def test_wildcard_scope_grant_has_null_decision_class() -> None:
    actor_id = _register_actor()
    status, body = _post_json(
        f"{API_URL}/authority-grants", _grant_payload(actor_id, scope_decision_class_id=None)
    )
    assert status == 201, f"expected 201, got {status}: {body}"
    assert body["authority_grant"]["scope_decision_class_id"] is None


def test_grant_by_unauthorized_actor_returns_403() -> None:
    actor_id = _register_actor()
    unrelated_actor_id = _register_actor()

    status, body = _post_json(
        f"{API_URL}/authority-grants", _grant_payload(actor_id, issued_by_actor_id=unrelated_actor_id)
    )
    assert status == 403, f"expected 403, got {status}: {body}"


def test_grant_for_unknown_actor_returns_404() -> None:
    unknown_actor_id = _unique("iaa-api-authority-unknown")
    status, body = _post_json(f"{API_URL}/authority-grants", _grant_payload(unknown_actor_id))
    assert status == 404, f"expected 404, got {status}: {body}"


def test_revoke_by_unauthorized_actor_returns_403() -> None:
    actor_id = _register_actor()
    unrelated_actor_id = _register_actor()
    grant_id = _post_json(f"{API_URL}/authority-grants", _grant_payload(actor_id))[1][
        "authority_grant"
    ]["authority_grant_id"]

    status, body = _post_json(
        f"{API_URL}/authority-grants/{grant_id}/revoke",
        {"revoked_by_actor_id": unrelated_actor_id, "reason": "I say so."},
    )
    assert status == 403, f"expected 403, got {status}: {body}"


def test_revoke_already_revoked_grant_returns_409() -> None:
    actor_id = _register_actor()
    grant_id = _post_json(f"{API_URL}/authority-grants", _grant_payload(actor_id))[1][
        "authority_grant"
    ]["authority_grant_id"]
    _post_json(
        f"{API_URL}/authority-grants/{grant_id}/revoke",
        {"revoked_by_actor_id": GRANT_ISSUER_ACTOR_ID, "reason": "First revocation."},
    )

    status, body = _post_json(
        f"{API_URL}/authority-grants/{grant_id}/revoke",
        {"revoked_by_actor_id": GRANT_ISSUER_ACTOR_ID, "reason": "Second revocation."},
    )
    assert status == 409, f"expected 409, got {status}: {body}"


def test_revoke_unknown_grant_returns_404() -> None:
    status, body = _post_json(
        f"{API_URL}/authority-grants/{uuid.uuid4()}/revoke",
        {"revoked_by_actor_id": GRANT_ISSUER_ACTOR_ID, "reason": "N/A"},
    )
    assert status == 404, f"expected 404, got {status}: {body}"


def test_get_missing_authority_grant_returns_404() -> None:
    status, body = _get_json(f"{API_URL}/authority-grants/{uuid.uuid4()}")
    assert status == 404
    assert "detail" in body
