"""API round-trip test for
POST /decisions/{registry_name}/{decision_id}/execution-records
against the running cdp-api.

Follows the pattern in test_execution_authorization_api.py: assumes the
local Docker stack (`make up-build`) is already running, and talks to it
over plain HTTP with no cdp import required, so it runs fine under any
local interpreter.

Requires 004 through 009 to already be applied to the database cdp-api is
using.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timedelta, timezone

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
            "DELETE FROM cdp_core.execution_record WHERE registry_name = %s AND decision_id = %s",
            (REGISTRY_NAME, decision_id),
        )
        cursor.execute(
            "DELETE FROM cdp_core.execution_authorization_record "
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
        "antecedent_text": "Execution record API round-trip test decision.",
        "subject_actor_type": "agent",
        "subject_actor_id": "claims_review_agent",
        "predicate_verb": "recommend_approval",
        "object_type": "claim",
        "object_id": "claim_9981",
        "permission_source_type": "policy_rule",
        "permission_source_id": "policy_claims_approval_v2",
        "human_required": True,
    }


def _iso(dt: datetime) -> str:
    return dt.isoformat()


def test_post_decision_authorize_then_record_execution_round_trip() -> None:
    decision_id = f"vslice5-api-{uuid.uuid4().hex[:12]}"

    try:
        decision_status, _ = _post_json(f"{API_URL}/decisions", _decision_payload(decision_id))
        assert decision_status == 201

        auth_status, _ = _post_json(
            f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/execution-authorizations",
            {
                "authorized_by_actor_id": "review_board",
                "rationale": (
                    "No blocking challenge work remains; authorized to proceed to "
                    "execution under the current workflow conditions."
                ),
            },
        )
        assert auth_status == 201

        now = datetime.now(timezone.utc)
        execution_payload = {
            "executed_by_actor_id": "workflow_engine",
            "execution_status": "succeeded",
            "result_summary": "API round-trip test execution completed successfully.",
            "attempted_at": _iso(now - timedelta(minutes=5)),
            "completed_at": _iso(now),
        }
        status, body = _post_json(
            f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/execution-records",
            execution_payload,
        )
        assert status == 201, f"expected 201, got {status}: {body}"
        assert body["execution_record"]["execution_status"] == "succeeded"
        # Constitutional invariant: success does not close the workflow.
        assert body["workflow_instance"]["workflow_status"] == "advanced"
        assert body["workflow_instance"]["closed_at"] is None

        with psycopg.connect(DATABASE_URL) as conn, conn.cursor() as cursor:
            cursor.execute(
                "SELECT count(*) FROM cdp_core.execution_record "
                "WHERE registry_name = %s AND decision_id = %s",
                (REGISTRY_NAME, decision_id),
            )
            assert cursor.fetchone()[0] == 1

            cursor.execute(
                "SELECT workflow_status, closed_at FROM cdp_core.workflow_instance "
                "WHERE registry_name = %s AND decision_id = %s",
                (REGISTRY_NAME, decision_id),
            )
            workflow_status, closed_at = cursor.fetchone()
            assert workflow_status == "advanced"
            assert closed_at is None

        # A second succeeded attempt must be rejected, not silently duplicated.
        second_status, second_body = _post_json(
            f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/execution-records",
            execution_payload,
        )
        assert second_status == 409, f"expected 409, got {second_status}: {second_body}"
    finally:
        _cleanup_decision(decision_id)


def test_execution_record_against_missing_decision_returns_404() -> None:
    missing_decision_id = f"vslice5-missing-{uuid.uuid4().hex[:12]}"
    now = datetime.now(timezone.utc)
    status, body = _post_json(
        f"{API_URL}/decisions/{REGISTRY_NAME}/{missing_decision_id}/execution-records",
        {
            "executed_by_actor_id": "workflow_engine",
            "execution_status": "succeeded",
            "result_summary": "irrelevant, decision does not exist",
            "attempted_at": _iso(now - timedelta(minutes=1)),
            "completed_at": _iso(now),
        },
    )
    assert status == 404
    assert "detail" in body


def test_execution_record_without_authorization_returns_409() -> None:
    decision_id = f"vslice5-noauth-{uuid.uuid4().hex[:12]}"

    try:
        decision_status, _ = _post_json(f"{API_URL}/decisions", _decision_payload(decision_id))
        assert decision_status == 201

        now = datetime.now(timezone.utc)
        status, body = _post_json(
            f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/execution-records",
            {
                "executed_by_actor_id": "workflow_engine",
                "execution_status": "succeeded",
                "result_summary": "should be blocked, no authorization exists",
                "attempted_at": _iso(now - timedelta(minutes=1)),
                "completed_at": _iso(now),
            },
        )
        assert status == 409, f"expected 409, got {status}: {body}"
    finally:
        _cleanup_decision(decision_id)
