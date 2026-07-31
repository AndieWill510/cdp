"""API round-trip test for POST /decisions/{registry_name}/{decision_id}/challenges
against the running cdp-api.

Follows the pattern in test_decision_api.py: assumes the local Docker stack
(`make up-build`) is already running, and talks to it over plain HTTP with no
cdp import required, so it runs fine under any local interpreter.

Requires 004 and 005 to already be applied to the database cdp-api is using.
There is no GET /challenges endpoint in this slice, so persistence is proven
by reading back the decision plus a direct DB check of the challenge/
workflow/task rows the POST response claims to have created.
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


def test_post_decision_then_post_challenge_round_trip() -> None:
    decision_id = f"vslice2-api-{uuid.uuid4().hex[:12]}"
    decision_payload = {
        "registry_name": REGISTRY_NAME,
        "decision_id": decision_id,
        "decision_class_id": "claim_approval",
        "antecedent_text": "Challenge API round-trip test decision.",
        "subject_actor_type": "agent",
        "subject_actor_id": "claims_review_agent",
        "predicate_verb": "recommend_approval",
        "object_type": "claim",
        "object_id": "claim_9981",
        "permission_source_type": "policy_rule",
        "permission_source_id": "policy_claims_approval_v2",
        "human_required": True,
    }
    challenge_payload = {
        "raised_by_actor_id": "user_442",
        "challenge_text": "This recommendation overlooks a documented policy exception.",
        "challenge_type": "policy",
    }

    try:
        decision_status, decision_body = _post_json(f"{API_URL}/decisions", decision_payload)
        assert decision_status == 201, f"expected 201, got {decision_status}: {decision_body}"

        challenge_status, challenge_body = _post_json(
            f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}/challenges", challenge_payload
        )
        assert challenge_status == 201, f"expected 201, got {challenge_status}: {challenge_body}"
        assert challenge_body["challenge"]["challenge_status"] == "raised"
        assert challenge_body["challenge"]["challenge_type"] == "policy"
        assert challenge_body["workflow_instance"]["blocked"] is True
        assert challenge_body["workflow_instance"]["workflow_status"] == "blocked"
        assert challenge_body["task"]["task_type"] == "adjudicate_challenge"

        # The decision itself is unaffected; only its workflow instance changed.
        get_status, get_body = _get_json(f"{API_URL}/decisions/{REGISTRY_NAME}/{decision_id}")
        assert get_status == 200
        assert get_body["decision_id"] == decision_id

        with psycopg.connect(DATABASE_URL) as conn, conn.cursor() as cursor:
            cursor.execute(
                "SELECT count(*) FROM cdp_core.challenge_record "
                "WHERE registry_name = %s AND decision_id = %s",
                (REGISTRY_NAME, decision_id),
            )
            assert cursor.fetchone()[0] == 1

            cursor.execute(
                "SELECT blocked, workflow_status FROM cdp_core.workflow_instance "
                "WHERE registry_name = %s AND decision_id = %s",
                (REGISTRY_NAME, decision_id),
            )
            blocked, workflow_status = cursor.fetchone()
            assert blocked is True
            assert workflow_status == "blocked"
    finally:
        _cleanup_decision(decision_id)


def test_challenge_against_missing_decision_returns_404() -> None:
    missing_decision_id = f"vslice2-missing-{uuid.uuid4().hex[:12]}"
    status, body = _post_json(
        f"{API_URL}/decisions/{REGISTRY_NAME}/{missing_decision_id}/challenges",
        {
            "raised_by_actor_id": "user_442",
            "challenge_text": "irrelevant, decision does not exist",
        },
    )
    assert status == 404
    assert "detail" in body
