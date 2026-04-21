from typing import Any, Optional
from pydantic import BaseModel, Field

class ProposalCreate(BaseModel):
    title: str
    domain: str
    proposer: str
    policy_basis: str
    payload: dict[str, Any] = Field(default_factory=dict)

class ChallengeCreate(BaseModel):
    proposal_id: int
    challenger: str
    challenge_type: str
    reason: str
    evidence: dict[str, Any] = Field(default_factory=dict)

class AdjudicationCreate(BaseModel):
    proposal_id: int
    adjudicator: str
    decision: str
    rationale: str
    conditions: dict[str, Any] = Field(default_factory=dict)

class LegitimationCreate(BaseModel):
    proposal_id: int
    legitimizer: str
    status: str
    basis: str

class ExecutionCreate(BaseModel):
    proposal_id: int
    executor: str
    execution_target: str
    execution_payload: dict[str, Any] = Field(default_factory=dict)

class ProposalOut(BaseModel):
    id: int
    title: str
    domain: str
    proposer: str
    status: str
    policy_basis: str
    payload: dict[str, Any]

    class Config:
        from_attributes = True
