from collections.abc import Generator
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from .db import get_db
from .schemas import (
    AdjudicationCreate,
    ChallengeCreate,
    ExecutionCreate,
    LegitimationCreate,
    ProposalCreate,
)

app = FastAPI(title="CDP Prototype", version="0.1.0")

def emit_event(db: Session, proposal_id: int, event_type: str, actor: str, body: dict):
    db.execute(
        text("""
            INSERT INTO cdp_event (proposal_id, event_type, actor, body)
            VALUES (:proposal_id, :event_type, :actor, CAST(:body AS jsonb))
        """),
        {"proposal_id": proposal_id, "event_type": event_type, "actor": actor, "body": __import__("json").dumps(body)},
    )

@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"ok": True}

@app.get("/proposals")
def list_proposals(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT id, title, domain, proposer, status, policy_basis, payload::text, created_at
        FROM cdp_proposal
        ORDER BY id DESC
    """)).mappings().all()
    return [dict(r) for r in rows]

@app.post("/proposals")
def create_proposal(payload: ProposalCreate, db: Session = Depends(get_db)):
    row = db.execute(
        text("""
            INSERT INTO cdp_proposal (title, domain, proposer, status, policy_basis, payload)
            VALUES (:title, :domain, :proposer, 'proposed', :policy_basis, CAST(:payload AS jsonb))
            RETURNING id, title, domain, proposer, status, policy_basis, payload::text, created_at
        """),
        {
            "title": payload.title,
            "domain": payload.domain,
            "proposer": payload.proposer,
            "policy_basis": payload.policy_basis,
            "payload": __import__("json").dumps(payload.payload),
        },
    ).mappings().one()
    emit_event(db, row["id"], "proposal_created", payload.proposer, payload.model_dump())
    db.commit()
    return dict(row)

@app.post("/challenges")
def create_challenge(payload: ChallengeCreate, db: Session = Depends(get_db)):
    exists = db.execute(text("SELECT 1 FROM cdp_proposal WHERE id=:id"), {"id": payload.proposal_id}).first()
    if not exists:
        raise HTTPException(status_code=404, detail="Proposal not found")
    row = db.execute(
        text("""
            INSERT INTO cdp_challenge (proposal_id, challenger, challenge_type, reason, evidence)
            VALUES (:proposal_id, :challenger, :challenge_type, :reason, CAST(:evidence AS jsonb))
            RETURNING id, proposal_id, challenger, challenge_type, reason, evidence::text, created_at
        """),
        {
            "proposal_id": payload.proposal_id,
            "challenger": payload.challenger,
            "challenge_type": payload.challenge_type,
            "reason": payload.reason,
            "evidence": __import__("json").dumps(payload.evidence),
        },
    ).mappings().one()
    db.execute(text("UPDATE cdp_proposal SET status='challenged' WHERE id=:id"), {"id": payload.proposal_id})
    emit_event(db, payload.proposal_id, "challenge_created", payload.challenger, payload.model_dump())
    db.commit()
    return dict(row)

@app.post("/adjudications")
def create_adjudication(payload: AdjudicationCreate, db: Session = Depends(get_db)):
    exists = db.execute(text("SELECT 1 FROM cdp_proposal WHERE id=:id"), {"id": payload.proposal_id}).first()
    if not exists:
        raise HTTPException(status_code=404, detail="Proposal not found")
    row = db.execute(
        text("""
            INSERT INTO cdp_adjudication (proposal_id, adjudicator, decision, rationale, conditions)
            VALUES (:proposal_id, :adjudicator, :decision, :rationale, CAST(:conditions AS jsonb))
            RETURNING id, proposal_id, adjudicator, decision, rationale, conditions::text, created_at
        """),
        {
            "proposal_id": payload.proposal_id,
            "adjudicator": payload.adjudicator,
            "decision": payload.decision,
            "rationale": payload.rationale,
            "conditions": __import__("json").dumps(payload.conditions),
        },
    ).mappings().one()
    db.execute(text("UPDATE cdp_proposal SET status='adjudicated' WHERE id=:id"), {"id": payload.proposal_id})
    emit_event(db, payload.proposal_id, "adjudication_created", payload.adjudicator, payload.model_dump())
    db.commit()
    return dict(row)

@app.post("/legitimations")
def create_legitimation(payload: LegitimationCreate, db: Session = Depends(get_db)):
    exists = db.execute(text("SELECT 1 FROM cdp_proposal WHERE id=:id"), {"id": payload.proposal_id}).first()
    if not exists:
        raise HTTPException(status_code=404, detail="Proposal not found")
    row = db.execute(
        text("""
            INSERT INTO cdp_legitimation (proposal_id, legitimizer, status, basis)
            VALUES (:proposal_id, :legitimizer, :status, :basis)
            RETURNING id, proposal_id, legitimizer, status, basis, created_at
        """),
        payload.model_dump(),
    ).mappings().one()
    new_status = "legitimized" if payload.status == "approved" else "blocked"
    db.execute(text("UPDATE cdp_proposal SET status=:status WHERE id=:id"), {"status": new_status, "id": payload.proposal_id})
    emit_event(db, payload.proposal_id, "legitimation_created", payload.legitimizer, payload.model_dump())
    db.commit()
    return dict(row)

@app.post("/executions")
def create_execution(payload: ExecutionCreate, db: Session = Depends(get_db)):
    status = db.execute(text("SELECT status FROM cdp_proposal WHERE id=:id"), {"id": payload.proposal_id}).scalar_one_or_none()
    if status is None:
        raise HTTPException(status_code=404, detail="Proposal not found")
    if status != "legitimized":
        raise HTTPException(status_code=409, detail=f"Proposal status is {status}; only legitimized proposals can execute")
    row = db.execute(
        text("""
            INSERT INTO cdp_execution (proposal_id, executor, execution_target, execution_payload, status)
            VALUES (:proposal_id, :executor, :execution_target, CAST(:execution_payload AS jsonb), 'submitted')
            RETURNING id, proposal_id, executor, execution_target, execution_payload::text, status, created_at
        """),
        {
            **payload.model_dump(exclude={"execution_payload"}),
            "execution_payload": __import__("json").dumps(payload.execution_payload),
        },
    ).mappings().one()
    db.execute(text("UPDATE cdp_proposal SET status='executed' WHERE id=:id"), {"id": payload.proposal_id})
    emit_event(db, payload.proposal_id, "execution_created", payload.executor, payload.model_dump())
    db.commit()
    return dict(row)

@app.get("/timeline/{proposal_id}")
def timeline(proposal_id: int, db: Session = Depends(get_db)):
    rows = db.execute(
        text("""
            SELECT id, proposal_id, event_type, actor, body::text, created_at
            FROM cdp_event
            WHERE proposal_id=:proposal_id
            ORDER BY id ASC
        """),
        {"proposal_id": proposal_id},
    ).mappings().all()
    return [dict(r) for r in rows]
