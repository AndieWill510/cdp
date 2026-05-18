# RFC-CDP-021 — Wire Message Envelope Schema

Author: Kevin “Andie” Williams  
Status: Draft v0.4  
Series: Constitutional Decision Plane (CDP)  
Date: May 17, 2026  
Updates: RFC-CDP-021 v0.3  
Related: RFC-CDP-022, RFC-CDP-023, RFC-CDP-030, RFC-CDP-031, RFC-CDP-032, RFC-CDP-033

## Abstract

This RFC defines the **Wire Message Envelope**: the structure carried on every CDP protocol message.

The Wire Message Envelope ensures that every protocol act carries identity, versioning, correlation, actor, authority, attestation, payload, integrity, and lineage.

This RFC does **not** define the Decision Lifecycle Envelope. The Decision Lifecycle Envelope is the governed path index for a complete decision across lifecycle stages and is defined separately in:

```text
RFC-CDP-023-Decision-Lifecycle-Envelope.md
```

These are different objects and MUST NOT be conflated.

---

## 1. Purpose

The Wire Message Envelope answers:

- what fields are present in every CDP protocol message;
- how versioning, correlation, actor, authority, attestation, payload, and metadata are encoded;
- how a single protocol act is linked to a decision and to other messages in the causal chain.

The Wire Message Envelope prevents unattributed, unversioned, unauthenticated, and untraced acts from entering the CDP system.

A wire message is not the full decision record.

A wire message is one governed act within a decision lifecycle.

---

## 2. Relationship to the Decision Lifecycle Envelope

The Wire Message Envelope is per-message.

The Decision Lifecycle Envelope is per-decision.

The Wire Message Envelope carries protocol-specific payloads for individual acts such as Propose, Challenge, Test, Adjudicate, Legitimize, Execute, Record, or Learn.

The Decision Lifecycle Envelope indexes the governed path across those acts and references the governed artifacts produced by the lifecycle.

Implementations SHOULD link wire messages to the Decision Lifecycle Envelope using `decision_id`, `correlation_id`, lineage fields, and governed record references.

---

## 3. Canonical Fields

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

---

## 4. Recommended Protocol Enums

```text
PROPOSE, CHALLENGE, TEST, ADJUDICATE, LEGITIMIZE, EXECUTE, RECORD, LEARN, ATTEST, IDENTIFY, NEMAWASHI, CONSENSUS
```

---

## 5. Recommended Act Enums

```text
SUBMIT, AMEND, OBJECT, REBUT, SIMULATE, VERIFY, APPROVE, REJECT, AUTHORIZE, ENACT, COMMIT, UPDATE, ALIGN, CLOSE
```

---

## 6. Recommended Lineage Object

```json
{
  "parent_decision_id": "dec-001",
  "parent_message_id": "msg-001",
  "ancestor_ids": ["dec-root"],
  "causal_chain": ["msg-001", "msg-004", "msg-009"],
  "precedent_refs": ["rec-112", "rec-204"]
}
```

---

## 7. Integrity Requirements

A Wire Message Envelope MUST include an `integrity_hash`.

The hash SHOULD cover either:

- the payload alone; or
- the canonicalized envelope excluding the hash field itself.

The selected hash scope SHOULD be declared in implementation profiles or protocol-specific payload schemas.

---

## 8. Principle

No protocol act exists outside a Wire Message Envelope.

No complete decision lifecycle is fully represented by a single Wire Message Envelope.

For full lifecycle reconstruction, use the Decision Lifecycle Envelope defined in `RFC-CDP-023-Decision-Lifecycle-Envelope.md`.
