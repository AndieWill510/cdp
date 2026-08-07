"""Standing routes (RFC-CDP-033), scoped to the narrowest slice that
reaches E4: Constitutional Affected-Party Standing for the Challenge stage
only -- see db/ddl/015-standing-and-recusal.sql's header for the full
boundary statement.

POST /standing-claims/{claim_id}/{recognize,deny} require
determined_by_actor_id to be the single seeded Standing recognition
authority and reject an actor determining its own claim, both with 403 --
see _determine_standing_claim's docstring in cdp/core/services.py.

Caller authentication (session 032 discipline, applied here from the
start): POST /standing-claims requires an Authorization: Bearer <token>
header matching the claimant actor_id's own token. Both determination
routes each require a header matching determined_by_actor_id.

No /narrow route exists here, deliberately (review finding on PR #53):
this table has no outcome_scope column to record what a narrowing
narrows to, so writing a 'narrowed' determination would be enforcement-
indistinguishable from 'recognized' while still asserting something the
system cannot describe. See cdp/core/services.py's comment next to
recognize_standing_claim.

No Recusal route exists here at all -- this slice does not implement
Recusal.
"""

from __future__ import annotations

import uuid
from typing import Any

import psycopg
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

from cdp.core import db
from cdp.core.repositories import standing as standing_repo
from cdp.core.services import (
    ActorNotFound,
    BearerTokenActorMismatch,
    BearerTokenInvalid,
    BearerTokenMissing,
    DecisionNotFound,
    SelfStandingRecognitionForbidden,
    StandingClaimAlreadyDetermined,
    StandingClaimInput,
    StandingClaimNotFound,
    StandingDeterminationInput,
    StandingRecognitionAuthorityRequired,
    StandingStageNotSupported,
    StandingTypeNotSupported,
    deny_standing_claim,
    recognize_standing_claim,
    submit_affected_party_standing_claim,
    verify_bearer_token,
)

router = APIRouter(tags=["standing"])


def _require_caller(authorization: str | None, expected_actor_id: str) -> None:
    try:
        verify_bearer_token(authorization_header=authorization, expected_actor_id=expected_actor_id)
    except (BearerTokenMissing, BearerTokenInvalid) as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except BearerTokenActorMismatch as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


class StandingClaimCreateRequest(BaseModel):
    decision_registry_name: str
    decision_id: str
    actor_id: str
    claimed_impact: str = Field(min_length=1)
    standing_basis_role: str | None = None
    standing_basis_accountability: str | None = None
    standing_basis_contextual_relationship: str | None = None
    stage: str = "challenge"
    standing_type: str = "constitutional_affected_party"


@router.post("/standing-claims", status_code=201)
def create_standing_claim(
    request: StandingClaimCreateRequest, authorization: str | None = Header(default=None)
) -> dict[str, Any]:
    _require_caller(authorization, request.actor_id)
    try:
        return submit_affected_party_standing_claim(StandingClaimInput(**request.model_dump()))
    except ActorNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except DecisionNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except (StandingStageNotSupported, StandingTypeNotSupported) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except (
        psycopg.errors.ForeignKeyViolation,
        psycopg.errors.RaiseException,
        psycopg.errors.CheckViolation,
    ) as exc:
        raise HTTPException(
            status_code=422,
            detail="The standing claim references unregistered or invalid identifiers, or "
            "does not meet minimal sufficiency (a claimed_impact plus at least one of "
            "standing_basis_role/accountability/contextual_relationship, all non-blank)",
        ) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail="Internal server error") from exc


@router.get("/standing-claims/{claim_id}")
def get_standing_claim(claim_id: uuid.UUID) -> dict[str, Any]:
    try:
        with db.transaction() as cursor:
            claim = standing_repo.fetch_claim(cursor, claim_id=claim_id)
            determination = (
                standing_repo.fetch_determination_for_claim(cursor, claim_id=claim_id)
                if claim is not None
                else None
            )
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail="Internal server error") from exc

    if claim is None:
        raise HTTPException(status_code=404, detail="Standing claim not found")

    return {"standing_claim": claim, "standing_recognition_determination": determination}


class StandingDeterminationRequest(BaseModel):
    determined_by_actor_id: str
    outcome_basis: str = Field(min_length=1)


def _handle_determination(
    claim_id: uuid.UUID, request: StandingDeterminationRequest, service_fn: Any
) -> dict[str, Any]:
    try:
        return service_fn(
            StandingDeterminationInput(
                claim_id=claim_id,
                determined_by_actor_id=request.determined_by_actor_id,
                outcome_basis=request.outcome_basis,
            )
        )
    except StandingClaimNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ActorNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except (StandingRecognitionAuthorityRequired, SelfStandingRecognitionForbidden) as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except StandingClaimAlreadyDetermined as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except (
        psycopg.errors.ForeignKeyViolation,
        psycopg.errors.RaiseException,
        psycopg.errors.CheckViolation,
    ) as exc:
        raise HTTPException(
            status_code=422,
            detail="The standing determination references unregistered or invalid identifiers",
        ) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail="Internal server error") from exc


@router.post("/standing-claims/{claim_id}/recognize")
def recognize_standing_claim_route(
    claim_id: uuid.UUID,
    request: StandingDeterminationRequest,
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    _require_caller(authorization, request.determined_by_actor_id)
    return _handle_determination(claim_id, request, recognize_standing_claim)


@router.post("/standing-claims/{claim_id}/deny")
def deny_standing_claim_route(
    claim_id: uuid.UUID,
    request: StandingDeterminationRequest,
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    _require_caller(authorization, request.determined_by_actor_id)
    return _handle_determination(claim_id, request, deny_standing_claim)
