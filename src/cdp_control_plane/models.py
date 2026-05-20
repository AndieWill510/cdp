from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class EnvelopeStatus(StrEnum):
    proposed = "proposed"
    challenged = "challenged"
    adjudicated = "adjudicated"
    closed = "closed"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class DecisionEnvelope(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    status: EnvelopeStatus = EnvelopeStatus.proposed
    actor_id: str
    proposal: str
    challenge: Optional[str] = None
    adjudication: Optional[str] = None
    lineage_ref: Optional[UUID] = None
    record_hash: str = ""


class ProposalRequest(BaseModel):
    actor_id: str
    proposal: str
    lineage_ref: Optional[UUID] = None


class ChallengeRequest(BaseModel):
    record_id: UUID
    actor_id: str
    challenge: str


class AdjudicationRequest(BaseModel):
    record_id: UUID
    actor_id: str
    adjudication: str
