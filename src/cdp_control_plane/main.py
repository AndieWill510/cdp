from __future__ import annotations

from uuid import UUID

from fastapi import FastAPI, HTTPException

from .models import (
    AdjudicationRequest,
    ChallengeRequest,
    DecisionEnvelope,
    EnvelopeStatus,
    ProposalRequest,
    utc_now,
)
from .store import get_record, save_record

app = FastAPI(title="CDP Control Plane", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/proposals", response_model=DecisionEnvelope)
def create_proposal(request: ProposalRequest) -> DecisionEnvelope:
    envelope = DecisionEnvelope(
        actor_id=request.actor_id,
        proposal=request.proposal,
        lineage_ref=request.lineage_ref,
    )
    return save_record(envelope)


@app.post("/challenges", response_model=DecisionEnvelope)
def add_challenge(request: ChallengeRequest) -> DecisionEnvelope:
    envelope = get_record(request.record_id)
    if envelope is None:
        raise HTTPException(status_code=404, detail="record not found")
    if envelope.status == EnvelopeStatus.adjudicated:
        raise HTTPException(status_code=409, detail="cannot challenge adjudicated record")
    envelope.challenge = request.challenge
    envelope.status = EnvelopeStatus.challenged
    envelope.updated_at = utc_now()
    return save_record(envelope)


@app.post("/adjudications", response_model=DecisionEnvelope)
def add_adjudication(request: AdjudicationRequest) -> DecisionEnvelope:
    envelope = get_record(request.record_id)
    if envelope is None:
        raise HTTPException(status_code=404, detail="record not found")
    envelope.adjudication = request.adjudication
    envelope.status = EnvelopeStatus.adjudicated
    envelope.updated_at = utc_now()
    return save_record(envelope)


@app.get("/records/{record_id}", response_model=DecisionEnvelope)
def read_record(record_id: UUID) -> DecisionEnvelope:
    envelope = get_record(record_id)
    if envelope is None:
        raise HTTPException(status_code=404, detail="record not found")
    return envelope
