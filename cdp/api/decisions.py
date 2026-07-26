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

from typing import Any

import psycopg
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from cdp.core import db
from cdp.core.repositories import decisions as decisions_repo
from cdp.core.services import (
    ChallengeInput,
    ChallengeNotPermitted,
    DecisionClassNotConfigured,
    DecisionInput,
    DecisionNotFound,
    WorkflowStageNotConfigured,
    create_decision_with_workflow,
    raise_challenge_for_decision,
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
