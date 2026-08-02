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
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from cdp.core import db
from cdp.core.repositories import attestations as attestations_repo
from cdp.core.repositories import authority as authority_repo
from cdp.core.repositories import decisions as decisions_repo
from cdp.core.services import (
    ActorNotActive,
    ActorNotFound,
    AdjudicationInput,
    AttestationInput,
    AttestedAdjudicationInput,
    AttestedChallengeInput,
    AttestedExecutionAuthorizationInput,
    AttestedExecutionRecordInput,
    AuthorityNotGranted,
    BearerTokenActorMismatch,
    BearerTokenInvalid,
    BearerTokenMissing,
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
    IdentityClaimActorMismatch,
    IdentityClaimNotRecognized,
    IdentityClaimScopeInsufficient,
    WorkflowStageNotConfigured,
    adjudicate_challenge,
    attest_and_adjudicate_challenge,
    attest_and_authorize_execution,
    attest_and_raise_challenge,
    attest_and_record_execution_attempt,
    authorize_execution,
    create_decision_with_workflow,
    raise_challenge_for_decision,
    record_execution_attempt,
    verify_bearer_token,
)

router = APIRouter(tags=["decisions"])


def _require_caller(authorization: str | None, expected_actor_id: str) -> None:
    """Caller authentication (session 032) -- see cdp/api/identity.py's
    module docstring for the full boundary statement."""
    try:
        verify_bearer_token(authorization_header=authorization, expected_actor_id=expected_actor_id)
    except (BearerTokenMissing, BearerTokenInvalid) as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except BearerTokenActorMismatch as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


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


@router.get("/decisions/{registry_name}/{decision_id}/attestations")
def list_decision_attestations(registry_name: str, decision_id: str) -> dict[str, Any]:
    """Durably discover who attested this governed act.

    Returns every cdp_core.attestation_record bound to this decision (see
    attest_and_create_decision / POST /attested-decisions in
    cdp/api/identity.py). Does not require the caller to already know an
    attestation_id -- this is what makes "who performed this act"
    discoverable from the decision itself, not just from a separate
    lookup. 404s only if the decision itself does not exist; an
    unattested decision returns an empty list, not a 404.
    """
    try:
        with db.transaction() as cursor:
            decision = decisions_repo.fetch_decision(
                cursor, registry_name=registry_name, decision_id=decision_id
            )
            if decision is None:
                raise HTTPException(status_code=404, detail="Decision not found")
            attestations = attestations_repo.fetch_attestations_for_decision(
                cursor, registry_name=registry_name, decision_id=decision_id
            )
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail="Internal server error") from exc

    return {"attestations": attestations}


@router.get("/decisions/{registry_name}/{decision_id}/authority-evaluations")
def list_decision_authority_evaluations(registry_name: str, decision_id: str) -> dict[str, Any]:
    """Durably discover whether -- and how -- authority was evaluated for
    this governed act. Mirrors list_decision_attestations above: 404s only
    if the decision itself does not exist; a decision created without an
    authority gate (e.g. via POST /decisions directly) returns an empty
    list, not a 404.
    """
    try:
        with db.transaction() as cursor:
            decision = decisions_repo.fetch_decision(
                cursor, registry_name=registry_name, decision_id=decision_id
            )
            if decision is None:
                raise HTTPException(status_code=404, detail="Decision not found")
            evaluations = authority_repo.fetch_evaluation_results_for_decision(
                cursor, registry_name=registry_name, decision_id=decision_id
            )
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail="Internal server error") from exc

    return {"authority_evaluations": evaluations}


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


class AttestedChallengeCreateRequest(BaseModel):
    challenge_text: str
    challenge_type: str = "other"
    metadata: dict[str, Any] | None = None

    submitted_by_actor_id: str
    identity_claim_id: uuid.UUID
    attestation_method: str
    credential_reference: str
    issued_at: datetime


@router.post("/decisions/{registry_name}/{decision_id}/attested-challenges", status_code=201)
def create_attested_challenge(
    registry_name: str,
    decision_id: str,
    request: AttestedChallengeCreateRequest,
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    """Universal Attestation proof path for RFC-CDP-042 Challenge (session
    029) -- see attest_and_raise_challenge's docstring in
    cdp/core/services.py. Additive to POST .../challenges above, which is
    unchanged."""
    _require_caller(authorization, request.submitted_by_actor_id)
    payload = request.model_dump()
    challenge_input = ChallengeInput(
        registry_name=registry_name,
        decision_id=decision_id,
        raised_by_actor_id=payload["submitted_by_actor_id"],
        challenge_text=payload["challenge_text"],
        challenge_type=payload["challenge_type"],
        metadata=payload["metadata"],
    )
    attestation_input = AttestationInput(
        actor_id=payload["submitted_by_actor_id"],
        identity_claim_id=payload["identity_claim_id"],
        attestation_method=payload["attestation_method"],
        credential_reference=payload["credential_reference"],
        issued_at=payload["issued_at"],
    )
    try:
        return attest_and_raise_challenge(
            AttestedChallengeInput(
                challenge_input=challenge_input, attestation_input=attestation_input
            )
        )
    except DecisionNotFound as exc:
        raise HTTPException(status_code=404, detail="Decision not found") from exc
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
    except AuthorityNotGranted as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
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


class AttestedExecutionAuthorizationCreateRequest(BaseModel):
    rationale: str

    submitted_by_actor_id: str
    identity_claim_id: uuid.UUID
    attestation_method: str
    credential_reference: str
    issued_at: datetime


@router.post(
    "/decisions/{registry_name}/{decision_id}/attested-execution-authorizations",
    status_code=201,
)
def create_attested_execution_authorization(
    registry_name: str,
    decision_id: str,
    request: AttestedExecutionAuthorizationCreateRequest,
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    """Universal Attestation proof path for execution authorization
    (session 029) -- see attest_and_authorize_execution's docstring in
    cdp/core/services.py. Additive to POST .../execution-authorizations
    above, which is unchanged."""
    _require_caller(authorization, request.submitted_by_actor_id)
    payload = request.model_dump()
    authorization_input = ExecutionAuthorizationInput(
        registry_name=registry_name,
        decision_id=decision_id,
        authorized_by_actor_id=payload["submitted_by_actor_id"],
        rationale=payload["rationale"],
    )
    attestation_input = AttestationInput(
        actor_id=payload["submitted_by_actor_id"],
        identity_claim_id=payload["identity_claim_id"],
        attestation_method=payload["attestation_method"],
        credential_reference=payload["credential_reference"],
        issued_at=payload["issued_at"],
    )
    try:
        return attest_and_authorize_execution(
            AttestedExecutionAuthorizationInput(
                authorization_input=authorization_input, attestation_input=attestation_input
            )
        )
    except DecisionNotFound as exc:
        raise HTTPException(status_code=404, detail="Decision not found") from exc
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
    except AuthorityNotGranted as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
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


class AttestedExecutionRecordCreateRequest(BaseModel):
    execution_status: Literal["succeeded", "failed", "partial"]
    result_summary: str
    attempted_at: datetime
    completed_at: datetime

    submitted_by_actor_id: str
    identity_claim_id: uuid.UUID
    attestation_method: str
    credential_reference: str
    issued_at: datetime


@router.post(
    "/decisions/{registry_name}/{decision_id}/attested-execution-records",
    status_code=201,
)
def create_attested_execution_record(
    registry_name: str,
    decision_id: str,
    request: AttestedExecutionRecordCreateRequest,
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    """Universal Attestation proof path for execution recording (session
    029) -- see attest_and_record_execution_attempt's docstring in
    cdp/core/services.py. Additive to POST .../execution-records above,
    which is unchanged."""
    _require_caller(authorization, request.submitted_by_actor_id)
    payload = request.model_dump()
    execution_input = ExecutionRecordInput(
        registry_name=registry_name,
        decision_id=decision_id,
        executed_by_actor_id=payload["submitted_by_actor_id"],
        execution_status=payload["execution_status"],
        result_summary=payload["result_summary"],
        attempted_at=payload["attempted_at"],
        completed_at=payload["completed_at"],
    )
    attestation_input = AttestationInput(
        actor_id=payload["submitted_by_actor_id"],
        identity_claim_id=payload["identity_claim_id"],
        attestation_method=payload["attestation_method"],
        credential_reference=payload["credential_reference"],
        issued_at=payload["issued_at"],
    )
    try:
        return attest_and_record_execution_attempt(
            AttestedExecutionRecordInput(
                execution_input=execution_input, attestation_input=attestation_input
            )
        )
    except DecisionNotFound as exc:
        raise HTTPException(status_code=404, detail="Decision not found") from exc
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
    except AuthorityNotGranted as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
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


class AttestedAdjudicationCreateRequest(BaseModel):
    outcome: Literal["sustained", "not_sustained", "deferred", "referred_to_repair"]
    rationale: str

    submitted_by_actor_id: str
    identity_claim_id: uuid.UUID
    attestation_method: str
    credential_reference: str
    issued_at: datetime


@router.post(
    "/decisions/{registry_name}/{decision_id}/challenges/{challenge_id}/attested-adjudications",
    status_code=201,
)
def create_attested_adjudication(
    registry_name: str,
    decision_id: str,
    challenge_id: uuid.UUID,
    request: AttestedAdjudicationCreateRequest,
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    """Universal Attestation proof path for challenge adjudication (session
    029) -- see attest_and_adjudicate_challenge's docstring in
    cdp/core/services.py. Additive to POST .../adjudications above, which
    is unchanged."""
    _require_caller(authorization, request.submitted_by_actor_id)
    payload = request.model_dump()
    adjudication_input = AdjudicationInput(
        registry_name=registry_name,
        decision_id=decision_id,
        challenge_id=challenge_id,
        adjudicated_by_actor_id=payload["submitted_by_actor_id"],
        outcome=payload["outcome"],
        rationale=payload["rationale"],
    )
    attestation_input = AttestationInput(
        actor_id=payload["submitted_by_actor_id"],
        identity_claim_id=payload["identity_claim_id"],
        attestation_method=payload["attestation_method"],
        credential_reference=payload["credential_reference"],
        issued_at=payload["issued_at"],
    )
    try:
        return attest_and_adjudicate_challenge(
            AttestedAdjudicationInput(
                adjudication_input=adjudication_input, attestation_input=attestation_input
            )
        )
    except DecisionNotFound as exc:
        raise HTTPException(status_code=404, detail="Decision not found") from exc
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
    except AuthorityNotGranted as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
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
