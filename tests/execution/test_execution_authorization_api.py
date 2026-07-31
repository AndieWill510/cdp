"""API round-trip test for
POST /decisions/{registry_name}/{decision_id}/execution-authorizations
against the running cdp-api.

Follows the pattern in test_challenge_adjudication_api.py: assumes the
local Docker stack (`make up-build`) is already running, and talks to it
over plain HTTP with no cdp import required, so it runs fine under any
local interpreter.

Requires 004, 005, 006, 007, and 008 to already be applied to the database
cdp-api is using.
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


def _cleanup_decision(decision_id: str) -> None:
    with psycopg.connect(DATABASE_URL) as conn, conn.cursor() as cursor:
        cursor.execute(
            "DELETE FROM cdp_core.execution_authorization_record "
            "WHERE registry_name = %s AND decision_id = %s",
            (REGISTRY_NAME, decision_id),
        )
        cursor.execute(
            "DELETE FROM cdp_core.challenge_adjudication_record "
            "WHERE registry_name = %s AND decision_id = %s",
            (REGISTRY_NAME, decision_id),
        )
        cursor.execute(
            "DELETE FROM cdp_core.challenge_record WHERE registry_name = %s AND decision_id = %s",
            (REGISTRY_NAME, decision_id),
        )
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


def _decision_payload(decision_id: str) -> dict:
    return {
        "registry_name": REGISTRY_NAME,
        "decision_id": decision_id,
        "decision_class_id": "claim_approval",
        "antecedent_text": "Execution authorization API round-trip test decision.",
        "subject_actor_type": "agent",
        "subject_actor_id": "claims_review_agent",
        "predicate_verb": "recommend_approval",
        "object_type": "claim",
        "object_id": "claim_9981",
        "permission_source_type": "policy_rule",
        "permission_source_id": "policy_claims_approval_v2",
        "human_required": True,
    }


def test_post_decision_then_authorize_execution_round_trip() -> None:
    decision_id = f"vslice4-api-{uuid.uuid4().hex[:12]}"

    try:
        decision_status, _ = _post_json(f"{API_URL}/decisions", _decision_payload(decision_id))
        assert decision_status == 201

        authorization_payload = {
            "authorized_by_actor_id": "review_board",
            "rationale": (
                "No blocking challenge work remains; authorized to proceed to "
                "execution under the current workflow conditions."
            ),
        }
        status, body = _post_json(
            f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/execution-authorizations",
            authorization_payload,
        )
        assert status == 201, f"expected 201, got {status}: {body}"
        assert body["authorization"]["authorization_status"] == "authorized"
        assert body["completed_task"]["task_status"] == "completed"
        assert body["workflow_instance"]["workflow_status"] == "advanced"

        with psycopg.connect(DATABASE_URL) as conn, conn.cursor() as cursor:
            cursor.execute(
                "SELECT count(*) FROM cdp_core.execution_authorization_record "
                "WHERE registry_name = %s AND decision_id = %s",
                (REGISTRY_NAME, decision_id),
            )
            assert cursor.fetchone()[0] == 1

        # A second attempt must be rejected as already-authorized, not
        # silently duplicated and not reported as some other conflict.
        second_status, second_body = _post_json(
            f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/execution-authorizations",
            authorization_payload,
        )
        assert second_status == 409, f"expected 409, got {second_status}: {second_body}"
        assert "already" in second_body["detail"].lower(), second_body
    finally:
        _cleanup_decision(decision_id)


def test_authorization_against_missing_decision_returns_404() -> None:
    missing_decision_id = f"vslice4-missing-{uuid.uuid4().hex[:12]}"
    status, body = _post_json(
        f"{API_URL}/decisions/{REGISTRY_NAME}/{missing_decision_id}/execution-authorizations",
        {
            "authorized_by_actor_id": "review_board",
            "rationale": "irrelevant, decision does not exist",
        },
    )
    assert status == 404
    assert "detail" in body


def test_authorization_blocked_by_open_challenge_returns_409() -> None:
    decision_id = f"vslice4-blocked-{uuid.uuid4().hex[:12]}"

    try:
        decision_status, _ = _post_json(f"{API_URL}/decisions", _decision_payload(decision_id))
        assert decision_status == 201

        challenge_status, _ = _post_json(
            f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/challenges",
            {
                "raised_by_actor_id": "user_442",
                "challenge_text": "Blocking concern for the 409 test.",
                "challenge_type": "policy",
            },
        )
        assert challenge_status == 201

        status, body = _post_json(
            f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/execution-authorizations",
            {
                "authorized_by_actor_id": "review_board",
                "rationale": "irrelevant, should be blocked",
            },
        )
        assert status == 409, f"expected 409, got {status}: {body}"
    finally:
        _cleanup_decision(decision_id)
