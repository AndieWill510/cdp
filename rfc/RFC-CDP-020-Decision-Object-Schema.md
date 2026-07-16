# RFC-CDP-020 — Decision Object Schema

Author: Kevin “Andie” Williams  
Status: Draft v0.4  
Series: Constitutional Decision Plane (CDP)  
Date: July 16, 2026  
Updates: RFC-CDP-020 v0.3  
Related: RFC-CDP-033, RFC-CDP-034

## Abstract
Defines the canonical Decision object.

## 1. Purpose
The Decision Schema answers:
- what the canonical Decision contains;
- what fields are mandatory;
- how state, authority, history, policy scope, Standing, and Participation Integrity are encoded or referenced.

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
| standing_refs | array[ref] | no | Standing artifacts governed by RFC-CDP-033 |
| participation_integrity_attestation_refs | array[ref] | no | Participation Integrity Attestations governed by RFC-CDP-034 |
| participation_integrity_status | enum | no | not_required, pending, intact, partially_intact, compromised, failed, or insufficient_evidence |
| sovereignty_claim_refs | array[ref] | no | Sovereignty Claim artifacts governed by RFC-CDP-074 |
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

Participation Integrity artifacts MUST be linked by reference rather than embedded as mutable duplicate objects.

A `participation_integrity_status` value of `intact` MUST NOT be asserted merely because an attestation record exists. It must reflect the attestation result defined by RFC-CDP-034.

A Sovereignty Claim MUST NOT be represented only as ordinary Standing or participation metadata.

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

The record must preserve not only that participation occurred, but whether the integrity of constitutionally protected participation was tested and what remained unresolved.
