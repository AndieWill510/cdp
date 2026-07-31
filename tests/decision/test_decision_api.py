"""API round-trip test for POST/GET /decisions against the running cdp-api.

Follows the pattern in test_build_verification.py: assumes the local Docker
stack (`make up-build`) is already running, and talks to it over plain HTTP
with no cdp import required, so it runs fine under any local interpreter.

Requires 004-decision-class-workflow-seed.sql to already be applied to the
database cdp-api is using (POST would otherwise fail with 409, since no
workflow would be configured for the seeded claim_approval class).
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
import uuid

import psycopg
import pytest

API_URL = os.getenv("CDP_TEST_API_URL", "http://localhost:8000")
DATABASE_URL = os.getenv("CDP_TEST_DATABASE_URL", "postgresql://cdp:cdp@localhost:5432/cdp")

REGISTRY_NAME = "sample_attorney_demo"


def _post_json(url: str, payload: dict) -> tuple[int, dict]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        pytest.fail(f"Could not reach {url}. Is the local Docker stack running? {exc}")


def _get_json(url: str) -> tuple[int, dict]:
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        pytest.fail(f"Could not reach {url}. Is the local Docker stack running? {exc}")


def _cleanup_decision(decision_id: str) -> None:
    with psycopg.connect(DATABASE_URL) as conn, conn.cursor() as cursor:
        cursor.execute(
            "DELETE FROM cdp_core.workflow_task WHERE registry_name = %s AND decision_id = %s",
            (REGISTRY_NAME, decision_id),
        )
        cursor.execute(
            "DELETE FROM cdp_core.workflow_instance WHERE registry_name = %s AND decision_id = %s",
            (REGISTRY_NAME, decision_id),
        )
        cursor.execute(
            "DELETE FROM cdp_core.decision_registry WHERE registry_name = %s AND decision_id = %s",
            (REGISTRY_NAME, decision_id),
        )
        cursor.execute(
            "DELETE FROM cdp_audit.event_log "
            "WHERE payload ->> 'registry_name' = %s AND payload ->> 'decision_id' = %s",
            (REGISTRY_NAME, decision_id),
        )
        conn.commit()


def test_post_then_get_decision_round_trip() -> None:
    decision_id = f"vslice-api-{uuid.uuid4().hex[:12]}"
    payload = {
        "registry_name": REGISTRY_NAME,
        "decision_id": decision_id,
        "decision_class_id": "claim_approval",
        "antecedent_text": "API round-trip test decision.",
        "subject_actor_type": "agent",
        "subject_actor_id": "claims_review_agent",
        "predicate_verb": "recommend_approval",
        "object_type": "claim",
        "object_id": "claim_9981",
        "permission_source_type": "policy_rule",
        "permission_source_id": "policy_claims_approval_v2",
        "human_required": True,
    }

    try:
        post_status, post_body = _post_json(f"{API_URL}/decisions", payload)
        assert post_status == 201, f"expected 201, got {post_status}: {post_body}"
        assert post_body["decision"]["decision_id"] == decision_id
        assert post_body["workflow_instance"]["workflow_status"] == "active"
        assert post_body["task"]["task_status"] == "open"

        get_status, get_body = _get_json(f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}")
        assert get_status == 200, f"expected 200, got {get_status}: {get_body}"
        assert get_body["decision_id"] == decision_id
        assert get_body["registry_name"] == REGISTRY_NAME
        assert get_body["decision_class_id"] == "claim_approval"
        assert get_body["antecedent_text"] == payload["antecedent_text"]
    finally:
        _cleanup_decision(decision_id)


def test_get_missing_decision_returns_404() -> None:
    missing_decision_id = f"vslice-missing-{uuid.uuid4().hex[:12]}"
    status, body = _get_json(f"{API_URL}/decisions/{REGISTRY_NAME}/{missing_decision_id}")
    assert status == 404
    assert "detail" in body
