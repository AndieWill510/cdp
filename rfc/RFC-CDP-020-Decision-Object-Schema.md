# RFC-CDP-013 — Decision Schema

Author: Kevin “Andie” Williams  
Status: Draft v0.3  
Series: Constitutional Decision Plane (CDP)  
Date: March 17, 2026

## Abstract
Defines the canonical Decision object.

## 1. Purpose
The Decision Schema answers:
- what the canonical Decision contains;
- what fields are mandatory;
- how state, authority, history, and policy scope are encoded.

## 2. Canonical Fields
| Field | Type | Required | Meaning |
|---|---|---:|---|
| decision_id | string | yes | Global identifier |
| title | string | yes | Human-readable short name |
| description | string | yes | Statement of the decision |
| state | enum | yes | Current lifecycle state |
| status | enum | yes | Active status marker |
| originator_id | string | yes | Original proposer |
| current_owner_id | string | no | Current responsible actor |
| policy_scope | string | yes | Governance domain |
| authority_required | array[enum] | yes | Authorities needed later |
| authority_observed | array[object] | no | Authorities already exercised |
| created_at | string | yes | Creation time |
| updated_at | string | yes | Last mutation time |
| effective_at | string | no | When decision becomes actionable |
| expires_at | string | no | Expiration, if any |
| objective | string | yes | Intended outcome |
| constraints | array | no | Hard limits and conditions |
| inputs | array | no | Facts, evidence, dependencies |
| tests | array | no | Linked test artifacts |
| challenges | array | no | Linked challenge artifacts |
| adjudications | array | no | Linked adjudication artifacts |
| legitimations | array | no | Linked legitimacy artifacts |
| executions | array | no | Linked execution artifacts |
| records | array | no | Linked record artifacts |
| precedent_refs | array | no | Relevant prior records |
| history | array | yes | State and act history |
| tags | array[string] | no | Classification tags |
| metadata | object | no | Extension space |

## 3. Recommended States
`DRAFT, PROPOSED, UNDER_DELIBERATION, UNDER_TEST, ADJUDICATED, LEGITIMIZED, EXECUTING, EXECUTED, RECORDED, LEARNED, REJECTED, WITHDRAWN, ESCALATED`

## 4. Recommended Status
`open, closed, pending, blocked, expired, failed, superseded`

## 5. Example Observed Authority
```json
{
  "authority": "CHALLENGE",
  "actor_id": "actor-789",
  "timestamp": "2026-03-14T12:30:00Z",
  "message_id": "msg-2231"
}
```

## 6. Example History Entry
```json
{
  "from_state": "PROPOSED",
  "to_state": "UNDER_DELIBERATION",
  "act": "CHALLENGE",
  "actor_id": "actor-789",
  "timestamp": "2026-03-14T12:30:00Z",
  "message_id": "msg-2231"
}
```

## 7. Principle
A Decision is a governed object with memory.
