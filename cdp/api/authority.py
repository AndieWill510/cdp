"""Authority routes (RFC-CDP-032), scoped to that RFC's §19 Minimal
Compliance -- see db/ddl/011-authority-and-delegation.sql's header for the
full boundary statement.

POST /authority-grants and POST /authority-grants/{grant_id}/revoke both
require the calling actor_id to be the single seeded authority-grant
issuer (`cdp_identity_recognition_authority`'s counterpart for this
slice, `cdp_authority_grant_issuer`) -- an arbitrary registered actor
cannot issue or revoke a grant, mirroring the recognition-authority
discipline the Identity and Attestation slice's v0.2 review correction
established, applied here from the start.

Caller authentication (session 032, db/ddl/014-caller-authentication.sql):
both routes also require an `Authorization: Bearer <token>` header
matching cdp_authority_grant_issuer's own token (seeded by that
migration for local/dev/test use -- see its header) -- previously an
arbitrary request body could simply assert issued_by_actor_id/
revoked_by_actor_id equal to that actor_id with nothing checking the
caller actually controlled it.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

import psycopg
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

from cdp.core import db
from cdp.core.repositories import authority as authority_repo
from cdp.core.services import (
    ActorNotFound,
    AuthorityGrantIssuerRequired,
    AuthorityGrantNotActive,
    AuthorityGrantNotFound,
    BearerTokenActorMismatch,
    BearerTokenInvalid,
    BearerTokenMissing,
    GrantAuthorityInput,
    RevokeAuthorityInput,
    grant_authority,
    revoke_authority,
    verify_bearer_token,
)

router = APIRouter(tags=["authority"])


def _require_caller(authorization: str | None, expected_actor_id: str) -> None:
    try:
        verify_bearer_token(authorization_header=authorization, expected_actor_id=expected_actor_id)
    except (BearerTokenMissing, BearerTokenInvalid) as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except BearerTokenActorMismatch as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


class AuthorityGrantCreateRequest(BaseModel):
    actor_id: str
    authority: str
    scope_registry_name: str
    scope_decision_class_id: str | None = None
    expires_at: datetime
    issued_by_actor_id: str
    basis: str
    issued_at: datetime | None = None
    effective_at: datetime | None = None


@router.post("/authority-grants", status_code=201)
def create_authority_grant(
    request: AuthorityGrantCreateRequest, authorization: str | None = Header(default=None)
) -> dict[str, Any]:
    _require_caller(authorization, request.issued_by_actor_id)
    try:
        return grant_authority(GrantAuthorityInput(**request.model_dump()))
    except AuthorityGrantIssuerRequired as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ActorNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except (
        psycopg.errors.ForeignKeyViolation,
        psycopg.errors.RaiseException,
        psycopg.errors.CheckViolation,
    ) as exc:
        raise HTTPException(
            status_code=422,
            detail="The authority grant references unregistered or invalid identifiers",
        ) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail="Internal server error") from exc


@router.get("/authority-grants/{grant_id}")
def get_authority_grant(grant_id: uuid.UUID) -> dict[str, Any]:
    try:
        with db.transaction() as cursor:
            grant = authority_repo.fetch_grant(cursor, grant_id=grant_id)
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail="Internal server error") from exc

    if grant is None:
        raise HTTPException(status_code=404, detail="Authority grant not found")
    return grant


class AuthorityGrantRevokeRequest(BaseModel):
    revoked_by_actor_id: str
    reason: str = Field(min_length=1)


@router.post("/authority-grants/{grant_id}/revoke")
def revoke_authority_grant(
    grant_id: uuid.UUID,
    request: AuthorityGrantRevokeRequest,
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    _require_caller(authorization, request.revoked_by_actor_id)
    try:
        return revoke_authority(
            RevokeAuthorityInput(
                grant_id=grant_id,
                revoked_by_actor_id=request.revoked_by_actor_id,
                reason=request.reason,
            )
        )
    except AuthorityGrantIssuerRequired as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except AuthorityGrantNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AuthorityGrantNotActive as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail="Internal server error") from exc
