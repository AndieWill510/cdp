# RFC-CCP-003: Proposal Protocol

Status: Draft  
Author: CCP Project  
Intended Status: Informational  
Created: 2026

---

## Abstract
This document defines the Proposal Protocol for the Constitutional Cognitive Control Plane (CCP).
A Proposal is the canonical decision primitive used throughout the CCP governance lifecycle.

---

## Motivation
All governance actions begin with a proposal submitted by an actor.
This protocol standardizes the structure, metadata, and lifecycle entry point for proposals.

---

## Proposal Structure

Required fields:

- proposal_id
- proposer_identity
- timestamp
- attestation
- decision_payload
- policy_scope
- execution_target

Optional fields:

- supporting_evidence
- simulation_requirements
- revision_history

---

## Proposal Lifecycle Entry

1. Actor submits proposal
2. Governance API validates structure
3. Attestation verification
4. Proposal enters Governance State Machine

---

## Security Considerations

- Prevent forged proposals
- Validate identity and authority
- Prevent replay attacks