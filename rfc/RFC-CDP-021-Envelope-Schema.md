# RFC-CDP-014 — Envelope Schema

Author: Kevin “Andie” Williams  
Status: Draft v0.3  
Series: Constitutional Decision Plane (CDP)  
Date: March 17, 2026

## Abstract
Defines what every CDP wire message shares.

## 1. Purpose
The Envelope Schema answers:
- what fields are present in every message;
- how versioning, correlation, actor, attestation, payload, and metadata are encoded.

## 2. Canonical Fields
| Field | Type | Required | Meaning |
|---|---|---:|---|
| cdp_version | string | yes | Protocol version |
| message_id | string | yes | Unique message identifier |
| correlation_id | string | yes | Shared lifecycle identifier |
| decision_id | string | yes | Governed Decision identifier |
| protocol | enum | yes | Protocol carrying the act |
| act | enum | yes | Verb being performed |
| actor_id | string | yes | Sender |
| actor_type | enum | yes | human, institution, synthetic |
| authority | enum | yes | Authority claimed |
| policy_scope | string | yes | Governance domain or jurisdiction |
| lineage | object | yes | Provenance and ancestry |
| attestation | object | yes | Signature and attestation material |
| timestamp | string | yes | ISO-8601 creation time |
| ttl | integer | no | Lifetime in seconds |
| reply_to | string | no | Prior message responded to |
| payload_type | string | yes | Schema identifier for payload |
| payload | object | yes | Protocol-specific content |
| integrity_hash | string | yes | Hash of payload or envelope |
| metadata | object | no | Extensible metadata |

## 3. Recommended Protocol Enums
`PROPOSE, CHALLENGE, TEST, ADJUDICATE, LEGITIMIZE, EXECUTE, RECORD, LEARN, ATTEST, IDENTIFY, NEMAWASHI, CONSENSUS`

## 4. Recommended Act Enums
`SUBMIT, AMEND, OBJECT, REBUT, SIMULATE, VERIFY, APPROVE, REJECT, AUTHORIZE, ENACT, COMMIT, UPDATE, ALIGN, CLOSE`

## 5. Recommended Lineage Object
```json
{
  "parent_decision_id": "dec-001",
  "parent_message_id": "msg-001",
  "ancestor_ids": ["dec-root"],
  "causal_chain": ["msg-001", "msg-004", "msg-009"],
  "precedent_refs": ["rec-112", "rec-204"]
}
```

## 6. Principle
No act exists outside an Envelope.
