"""Decision creation and lookup routes.

GET reads directly from cdp_core.decision_registry (the authoritative
table) rather than cdp_projection.decision_registry_flat. That projection is
a wide, denormalized display surface built for attorney-facing/demo output:
it joins in derived display labels and a generated plain-English sentence
that are convenient for reporting but are not a stable API contract, and it
returns NULL label columns whenever a referenced identifier lacks a label
join. For a decision round-trip GET, the smaller and stable authoritative
table is the better fit.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Literal

import psycopg
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from cdp.core import db
from cdp.core.repositories import decisions as decisions_repo
from cdp.core.services import (
    AdjudicationInput,
    ChallengeInput,
    ChallengeNotAdjudicable,
    ChallengeNotFound,
    ChallengeNotPermitted,
    DecisionClassNotConfigured,
    DecisionInput,
    DecisionNotAuthorizedForExecution,
    DecisionNotFound,
    ExecutionAlreadyAuthorized,
    ExecutionAlreadySucceeded,
    ExecutionAuthorizationInput,
    ExecutionAuthorizationNotPermitted,
    ExecutionNotPermitted,
    ExecutionRecordInput,
    WorkflowStageNotConfigured,
    adjudicate_challenge,
    authorize_execution,
    create_decision_with_workflow,
    raise_challenge_for_decision,
    record_execution_attempt,
)

router = APIRouter(tags=["decisions"])


class DecisionCreateRequest(BaseModel):
    registry_name: str
    decision_id: str
    decision_class_id: str
    antecedent_text: str
    subject_actor_type: str
    subject_actor_id: str
    predicate_verb: str
    object_type: str
    object_id: str
    permission_source_type: str
    permission_source_id: str
    human_required: bool
    human_approver_id: str = "none"
    parent_decision_id: str | None = None
    parent_relation_type: str = "none"
    source_system: str = "api"
    source_ref: str | None = None


@router.post("/decisions", status_code=201)
def create_decision(request: DecisionCreateRequest) -> dict[str, Any]:
    decision_input = DecisionInput(**request.model_dump())
    try:
        return create_decision_with_workflow(decision_input)
    except (DecisionClassNotConfigured, WorkflowStageNotConfigured) as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except psycopg.errors.UniqueViolation as exc:
        raise HTTPException(
            status_code=409,
            detail="A decision already exists for this registry_name and decision_id",
        ) from exc
    except (
        psycopg.errors.ForeignKeyViolation,
        psycopg.errors.RaiseException,
        psycopg.errors.CheckViolation,
    ) as exc:
        raise HTTPException(
            status_code=422,
            detail="The decision references unregistered or invalid identifiers",
        ) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail="Internal server error") from exc


@router.get("/decisions/{registry_name}/{decision_id}")
def get_decision(registry_name: str, decision_id: str) -> dict[str, Any]:
    try:
        with db.transaction() as cursor:
            decision = decisions_repo.fetch_decision(
                cursor, registry_name=registry_name, decision_id=decision_id
            )
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail="Internal server error") from exc

    if decision is None:
        raise HTTPException(status_code=404, detail="Decision not found")
    return decision


class ChallengeCreateRequest(BaseModel):
    raised_by_actor_id: str
    challenge_text: str
    challenge_type: str = "other"
    metadata: dict[str, Any] | None = None


@router.post("/decisions/{registry_name}/{decision_id}/challenges", status_code=201)
def create_challenge(
    registry_name: str, decision_id: str, request: ChallengeCreateRequest
) -> dict[str, Any]:
    challenge_input = ChallengeInput(
        registry_name=registry_name,
        decision_id=decision_id,
        **request.model_dump(),
    )
    try:
        return raise_challenge_for_decision(challenge_input)
    except DecisionNotFound as exc:
        raise HTTPException(status_code=404, detail="Decision not found") from exc
    except ChallengeNotPermitted as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except (
        psycopg.errors.ForeignKeyViolation,
        psycopg.errors.RaiseException,
        psycopg.errors.CheckViolation,
    ) as exc:
        raise HTTPException(
            status_code=422,
            detail="The challenge references unregistered or invalid identifiers",
        ) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail="Internal server error") from exc


class ExecutionAuthorizationCreateRequest(BaseModel):
    authorized_by_actor_id: str
    rationale: str


@router.post(
    "/decisions/{registry_name}/{decision_id}/execution-authorizations",
    status_code=201,
)
def create_execution_authorization(
    registry_name: str, decision_id: str, request: ExecutionAuthorizationCreateRequest
) -> dict[str, Any]:
    authorization_input = ExecutionAuthorizationInput(
        registry_name=registry_name,
        decision_id=decision_id,
        **request.model_dump(),
    )
    try:
        return authorize_execution(authorization_input)
    except DecisionNotFound as exc:
        raise HTTPException(status_code=404, detail="Decision not found") from exc
    except ExecutionAlreadyAuthorized as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ExecutionAuthorizationNotPermitted as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except psycopg.errors.UniqueViolation as exc:
        raise HTTPException(
            status_code=409,
            detail="This decision has already received execution authorization",
        ) from exc
    except (
        psycopg.errors.ForeignKeyViolation,
        psycopg.errors.RaiseException,
        psycopg.errors.CheckViolation,
    ) as exc:
        raise HTTPException(
            status_code=422,
            detail="The authorization references unregistered or invalid identifiers",
        ) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail="Internal server error") from exc


class ExecutionRecordCreateRequest(BaseModel):
    executed_by_actor_id: str
    execution_status: Literal["succeeded", "failed", "partial"]
    result_summary: str
    attempted_at: datetime
    completed_at: datetime


@router.post(
    "/decisions/{registry_name}/{decision_id}/execution-records",
    status_code=201,
)
def create_execution_record(
    registry_name: str, decision_id: str, request: ExecutionRecordCreateRequest
) -> dict[str, Any]:
    execution_input = ExecutionRecordInput(
        registry_name=registry_name,
        decision_id=decision_id,
        **request.model_dump(),
    )
    try:
        return record_execution_attempt(execution_input)
    except DecisionNotFound as exc:
        raise HTTPException(status_code=404, detail="Decision not found") from exc
    except DecisionNotAuthorizedForExecution as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ExecutionNotPermitted as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ExecutionAlreadySucceeded as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except psycopg.errors.UniqueViolation as exc:
        raise HTTPException(
            status_code=409,
            detail="This authorization already has a succeeded execution record",
        ) from exc
    except (
        ValueError,
        psycopg.errors.ForeignKeyViolation,
        psycopg.errors.RaiseException,
        psycopg.errors.CheckViolation,
    ) as exc:
        raise HTTPException(
            status_code=422,
            detail="The execution record references unregistered or invalid identifiers",
        ) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail="Internal server error") from exc


class AdjudicationCreateRequest(BaseModel):
    adjudicated_by_actor_id: str
    outcome: Literal["sustained", "not_sustained", "deferred", "referred_to_repair"]
    rationale: str


@router.post(
    "/decisions/{registry_name}/{decision_id}/challenges/{challenge_id}/adjudications",
    status_code=201,
)
def create_adjudication(
    registry_name: str,
    decision_id: str,
    challenge_id: uuid.UUID,
    request: AdjudicationCreateRequest,
) -> dict[str, Any]:
    adjudication_input = AdjudicationInput(
        registry_name=registry_name,
        decision_id=decision_id,
        challenge_id=challenge_id,
        **request.model_dump(),
    )
    try:
        return adjudicate_challenge(adjudication_input)
    except DecisionNotFound as exc:
        raise HTTPException(status_code=404, detail="Decision not found") from exc
    except ChallengeNotFound as exc:
        raise HTTPException(status_code=404, detail="Challenge not found") from exc
    except ChallengeNotAdjudicable as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except (
        ValueError,
        psycopg.errors.ForeignKeyViolation,
        psycopg.errors.RaiseException,
        psycopg.errors.CheckViolation,
    ) as exc:
        raise HTTPException(
            status_code=422,
            detail="The adjudication references unregistered or invalid identifiers",
        ) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail="Internal server error") from exc
