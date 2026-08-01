"""Identity and Attestation routes (RFC-CDP-030, RFC-CDP-031).

Additive to the existing decision API: POST /decisions
(cdp/api/decisions.py) is untouched. POST /attested-decisions is the one
new, explicit integration path that requires attestation before creating a
decision -- see attest_and_create_decision's docstring in
cdp/core/services.py for why this is a separate route rather than a
retrofit of the existing one. The request's submitted_by_actor_id (the
attestor) is independent of subject_actor_id (who/what the decision is
about) -- see AttestedDecisionCreateRequest below.

POST /identity-claims/{claim_id}/{recognize,deny,contest} require
decided_by_actor_id to be the single seeded recognition-authority actor
and reject an actor deciding its own claim, both with 403 -- see
_decide_identity_claim's docstring in cdp/core/services.py.

GET /actors/{actor_id} and GET /identity-claims/{claim_id} redact
identity-claim content whenever the actor's display_mode is not 'public',
so a protected or pseudonymous actor's claimed identity descriptor and
evidence references never leak through a public/API response -- only
actor_id, actor_type, display_mode, actor_status, and the actor's chosen
display_label are ever exposed for such actors.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

import psycopg
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from cdp.core import db
from cdp.core.repositories import actors as actors_repo
from cdp.core.repositories import attestations as attestations_repo
from cdp.core.repositories import identity_claims as identity_claims_repo
from cdp.core.services import (
    ActorAlreadyRegistered,
    ActorInput,
    ActorNotActive,
    ActorNotFound,
    AttestationInput,
    AttestedDecisionInput,
    DecisionClassNotConfigured,
    DecisionInput,
    IdentityClaimActorMismatch,
    IdentityClaimDecisionInput,
    IdentityClaimInput,
    IdentityClaimNotDecidable,
    IdentityClaimNotFound,
    IdentityClaimNotRecognized,
    IdentityClaimScopeInsufficient,
    RecognitionAuthorityRequired,
    SelfRecognitionForbidden,
    WorkflowStageNotConfigured,
    attest_and_create_decision,
    contest_identity_claim,
    deny_identity_claim,
    recognize_identity_claim,
    register_actor,
    submit_identity_claim,
)

router = APIRouter(tags=["identity"])


def _redact_claim_if_protected(
    claim: dict[str, Any], actor: dict[str, Any] | None
) -> dict[str, Any]:
    if actor is not None and actor["display_mode"] != "public":
        return {
            **claim,
            "claimed_identity_descriptor": "[protected]",
            "evidence_refs": "[protected]",
        }
    return claim


class ActorCreateRequest(BaseModel):
    actor_id: str
    actor_type: str
    display_label: str
    display_mode: str = "public"
    description: str | None = None


@router.post("/actors", status_code=201)
def create_actor(request: ActorCreateRequest) -> dict[str, Any]:
    try:
        return register_actor(ActorInput(**request.model_dump()))
    except ActorAlreadyRegistered as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except (
        psycopg.errors.ForeignKeyViolation,
        psycopg.errors.RaiseException,
        psycopg.errors.CheckViolation,
    ) as exc:
        raise HTTPException(
            status_code=422,
            detail="The actor references an invalid actor_type or display_mode",
        ) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail="Internal server error") from exc


@router.get("/actors/{actor_id}")
def get_actor(actor_id: str) -> dict[str, Any]:
    try:
        with db.transaction() as cursor:
            actor = actors_repo.fetch_actor(cursor, actor_id=actor_id)
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail="Internal server error") from exc

    if actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")

    return {
        "actor_id": actor["actor_id"],
        "actor_type": actor["actor_type"],
        "display_mode": actor["display_mode"],
        "actor_status": actor["actor_status"],
        "display_label": actor["display_label"],
        "created_at": actor["created_at"],
    }


class IdentityClaimCreateRequest(BaseModel):
    actor_id: str
    claimant_actor_id: str
    claimed_identity_descriptor: str
    purpose_scope: str
    evidence_refs: list[Any] | None = None
    supersedes_claim_id: uuid.UUID | None = None


@router.post("/identity-claims", status_code=201)
def create_identity_claim(request: IdentityClaimCreateRequest) -> dict[str, Any]:
    try:
        return submit_identity_claim(IdentityClaimInput(**request.model_dump()))
    except ActorNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except IdentityClaimActorMismatch as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except (
        psycopg.errors.ForeignKeyViolation,
        psycopg.errors.RaiseException,
        psycopg.errors.CheckViolation,
    ) as exc:
        raise HTTPException(
            status_code=422,
            detail="The identity claim references unregistered or invalid identifiers",
        ) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail="Internal server error") from exc


@router.get("/identity-claims/{claim_id}")
def get_identity_claim(claim_id: uuid.UUID) -> dict[str, Any]:
    try:
        with db.transaction() as cursor:
            claim = identity_claims_repo.fetch_claim(cursor, claim_id=claim_id)
            actor = (
                actors_repo.fetch_actor(cursor, actor_id=claim["actor_id"])
                if claim is not None
                else None
            )
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail="Internal server error") from exc

    if claim is None:
        raise HTTPException(status_code=404, detail="Identity claim not found")

    return _redact_claim_if_protected(claim, actor)


class IdentityClaimDecisionRequest(BaseModel):
    decided_by_actor_id: str
    rationale: str = Field(min_length=1)


def _handle_claim_decision(
    claim_id: uuid.UUID, request: IdentityClaimDecisionRequest, service_fn: Any
) -> dict[str, Any]:
    try:
        return service_fn(
            IdentityClaimDecisionInput(
                claim_id=claim_id,
                decided_by_actor_id=request.decided_by_actor_id,
                rationale=request.rationale,
            )
        )
    except IdentityClaimNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ActorNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except (RecognitionAuthorityRequired, SelfRecognitionForbidden) as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except IdentityClaimNotDecidable as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except (
        psycopg.errors.ForeignKeyViolation,
        psycopg.errors.RaiseException,
        psycopg.errors.CheckViolation,
    ) as exc:
        raise HTTPException(
            status_code=422,
            detail="The identity claim decision references unregistered or invalid identifiers",
        ) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail="Internal server error") from exc


@router.post("/identity-claims/{claim_id}/recognize")
def recognize_claim_route(
    claim_id: uuid.UUID, request: IdentityClaimDecisionRequest
) -> dict[str, Any]:
    return _handle_claim_decision(claim_id, request, recognize_identity_claim)


@router.post("/identity-claims/{claim_id}/deny")
def deny_claim_route(
    claim_id: uuid.UUID, request: IdentityClaimDecisionRequest
) -> dict[str, Any]:
    return _handle_claim_decision(claim_id, request, deny_identity_claim)


@router.post("/identity-claims/{claim_id}/contest")
def contest_claim_route(
    claim_id: uuid.UUID, request: IdentityClaimDecisionRequest
) -> dict[str, Any]:
    return _handle_claim_decision(claim_id, request, contest_identity_claim)


class AttestedDecisionCreateRequest(BaseModel):
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

    # The actor who performed/submitted this governed act -- the attestor.
    # Deliberately not required to equal subject_actor_id above, which is
    # the actor or entity the decision is about. See
    # attest_and_create_decision's docstring in cdp/core/services.py.
    submitted_by_actor_id: str
    identity_claim_id: uuid.UUID
    attestation_method: str
    credential_reference: str = Field(min_length=1)
    issued_at: datetime


_DECISION_FIELDS = (
    "registry_name",
    "decision_id",
    "decision_class_id",
    "antecedent_text",
    "subject_actor_type",
    "subject_actor_id",
    "predicate_verb",
    "object_type",
    "object_id",
    "permission_source_type",
    "permission_source_id",
    "human_required",
    "human_approver_id",
    "parent_decision_id",
    "parent_relation_type",
    "source_system",
    "source_ref",
)


@router.post("/attested-decisions", status_code=201)
def create_attested_decision(request: AttestedDecisionCreateRequest) -> dict[str, Any]:
    payload = request.model_dump()
    decision_input = DecisionInput(**{key: payload[key] for key in _DECISION_FIELDS})
    attestation_input = AttestationInput(
        actor_id=payload["submitted_by_actor_id"],
        identity_claim_id=payload["identity_claim_id"],
        attestation_method=payload["attestation_method"],
        credential_reference=payload["credential_reference"],
        issued_at=payload["issued_at"],
    )
    try:
        return attest_and_create_decision(
            AttestedDecisionInput(
                decision_input=decision_input, attestation_input=attestation_input
            )
        )
    except ActorNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ActorNotActive as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except IdentityClaimActorMismatch as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except IdentityClaimNotRecognized as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except IdentityClaimScopeInsufficient as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
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
            detail="The attested decision references unregistered or invalid identifiers",
        ) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail="Internal server error") from exc


@router.get("/attestations/{attestation_id}")
def get_attestation(attestation_id: uuid.UUID) -> dict[str, Any]:
    try:
        with db.transaction() as cursor:
            attestation = attestations_repo.fetch_attestation(cursor, attestation_id=attestation_id)
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail="Internal server error") from exc

    if attestation is None:
        raise HTTPException(status_code=404, detail="Attestation not found")
    return attestation
