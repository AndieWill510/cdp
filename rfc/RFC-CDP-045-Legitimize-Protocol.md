# RFC-CDP-006 — Legitimize Protocol

Author: Kevin “Andie” Williams  
Status: Draft v0.3  
Series: Constitutional Decision Plane (CDP)  
Date: March 17, 2026

## Abstract
Defines how a judged Decision becomes institutionally enactable.

## 1. Purpose
The Legitimize Protocol answers:
- how a judged decision becomes institutionally enactable;
- who confers legitimacy;
- what checks must pass;
- when legitimacy fails.

## 2. Authority
Actors invoking this protocol MUST possess `LEGITIMIZE` authority. Separation-of-duty rules SHOULD prevent the same actor from silently combining adjudication and legitimacy when policy forbids it.

## 3. Preconditions
- Decision MUST be `ADJUDICATED`;
- required policies, jurisdictional checks, and authority checks MUST be satisfied;
- required signatures, quorum, or approval bodies MUST be present if policy requires them.

## 4. Semantics
Legitimacy is not the same thing as correctness.
A judged decision MAY still fail legitimacy.
A flawed adjudication MAY appear coherent but still lack institutional authority.

## 5. Legitimacy Checks
Implementations SHOULD evaluate:
- policy compliance;
- jurisdictional fit;
- authority sufficiency;
- time validity (`effective_at`, `expires_at`);
- quorum or institutional signature requirements;
- conflict-of-interest rules;
- whether `no challenge` attestations satisfy policy.

## 6. State Transitions
- `ADJUDICATED → LEGITIMIZED`
- `ADJUDICATED → REJECTED`
- `ADJUDICATED → ESCALATED`

## 7. Recommended Payload
```json
{
  "status": "granted | denied | escalated",
  "basis": "string",
  "scope": "string",
  "constraints": ["string"],
  "granted_by": ["actor_id"],
  "effective_at": "timestamp",
  "expires_at": "timestamp",
  "execution_conditions": ["string"],
  "metadata": {}
}
```

## 8. Failure Modes
Legitimacy MUST fail when:
- adjudication is incomplete;
- authority is insufficient;
- jurisdiction is invalid;
- required controls are absent;
- time bounds or safety constraints are violated.

## 9. Principle
Correct does not imply legitimate. Legitimacy is conferred, not assumed.
