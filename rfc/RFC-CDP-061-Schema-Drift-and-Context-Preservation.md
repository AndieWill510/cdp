# RFC-CDP-061 — Schema Drift and Context Preservation

Author: Kevin “Andie” Williams  
Status: Draft v0.2  
Series: Constitutional Decision Plane (CDP)  
Date: July 1, 2026  
Depends On: RFC-CDP-001, RFC-CDP-010, RFC-CDP-020, RFC-CDP-021, RFC-CDP-025, RFC-CDP-032, RFC-CDP-047, RFC-CDP-048, RFC-CDP-060  
Updates: RFC-CDP-060

## Abstract

This RFC defines Schema Drift and Context Preservation for the Constitutional Decision Plane (CDP).

Schema drift occurs when the expected structure of meaning no longer matches the actual structure of reality. In CDP, schema drift is not limited to technical data contracts. It may occur across identity, authority, role, diagnosis, risk, consent, culture, policy, jurisdiction, affected-party status, repair obligations, institutional memory, or observable artifact state.

Context preservation is the discipline of retaining enough surrounding meaning, provenance, uncertainty, dissent, authority information, and verification material to prevent a valid record from becoming a false record through loss of context.

This RFC defines drift types, drift signals, context preservation requirements, verification handles, AIITL duties, record requirements, and learning closure for schema drift events.

---

## 1. Purpose

This RFC answers:

- what schema drift means in CDP;
- how technical, institutional, relational, and repair-related drift differ;
- how context must be preserved before decisions are enforced;
- what AIITL may surface as schema drift;
- when drift should block, defer, challenge, verify, or escalate a decision;
- how access-seam drift should be handled without authority performance;
- how drift should be recorded and learned from;
- how to avoid turning old validators into instruments of harm.

---

## 2. Core Principle

A record can be syntactically valid and constitutionally wrong.

A validator can pass while reality has changed.

A reader can receive a stale, partial, or divergent view of an otherwise valid artifact.

CDP MUST therefore distinguish:

- schema validity from contextual validity;
- field correctness from meaning correctness;
- historical record from current authority;
- institutional category from lived reality;
- prior consent from current consent;
- prior authority from current authority;
- classification from identity;
- summary from testimony;
- repair claim from stakeholder comment;
- private verification from independently usable verification.

---

## 3. Relationship to Existing RFCs

### 3.1 RFC-CDP-020 Decision Object Schema

The Decision object stores state, policy scope, authority, history, linked artifacts, and metadata.

This RFC defines when those fields may no longer represent current reality, even if the object remains structurally valid.

### 3.2 RFC-CDP-021 Envelope Schema

The Envelope carries message context, actor, authority, lineage, attestation, payload type, and integrity material.

This RFC defines context preservation requirements for envelopes and related records.

### 3.3 RFC-CDP-032 Authority and Delegation Model

Authority may decay or be revoked when context changes.

This RFC defines schema drift as one class of context change that may invalidate, narrow, suspend, or challenge authority.

### 3.4 RFC-CDP-047 Record Protocol

Record preserves governed acts and artifacts.

This RFC defines drift records, context snapshots, and verification-handle references that SHOULD be attached when meaning changes, artifact state is disputed, or access paths diverge.

### 3.5 RFC-CDP-048 Learn Protocol

Learn turns recorded outcomes into future correction.

This RFC defines learning closure for drift detection, drift correction, verification-seam handling, and schema revision.

### 3.6 RFC-CDP-060 Covenant Protocol and AIITL

Covenant defines AIITL duties to witness carefully, speak truthfully, hold gently, and build beautifully.

This RFC formalizes AIITL schema-drift detection as a bounded constitutional duty.

### 3.7 RFC-CDP-025 CDP Persistence Model

The persistence model defines queryable CDP records and append-only event logging.

This RFC defines when observation divergence or access-seam drift SHOULD produce a durable verification handle, receipt, manifest, snapshot, or event that can be independently checked.

---

## 4. Terminology

### 4.1 Schema

A **schema** is an expected structure for representing meaning.

A schema may be technical, legal, procedural, institutional, social, cultural, medical, relational, access-oriented, or repair-oriented.

### 4.2 Technical Schema Drift

**Technical Schema Drift** occurs when fields, types, values, structures, enumerations, or data contracts no longer match expected format or semantics.

Example:

```text
A status field formerly allowed OPEN/CLOSED, but current records require OPEN/CLOSED/CONTESTED/IN_REPAIR.
```

### 4.3 Semantic Schema Drift

**Semantic Schema Drift** occurs when a field still exists but its meaning has changed.

Example:

```text
A field named consent remains true, but the consent was time-bounded, coerced, revoked, or no longer applies to the current action.
```

### 4.4 Authority Schema Drift

**Authority Schema Drift** occurs when the authority model represented in a record no longer matches current authority.

Example:

```text
A service account still has access, but the delegation basis has expired or the human approver changed roles.
```

### 4.5 Identity Schema Drift

**Identity Schema Drift** occurs when identity records no longer represent current identity, role, name, community affiliation, legal status, or relevant self-description.

Example:

```text
A record uses a prior name, category, or role that no longer matches the person or community being governed.
```

### 4.6 Policy Schema Drift

**Policy Schema Drift** occurs when the policy framework used to validate a decision is obsolete, superseded, legally invalid, or inconsistent with current authority.

### 4.7 Cultural Schema Drift

**Cultural Schema Drift** occurs when an institutional or technical category fails to preserve culturally meaningful distinctions, restricted knowledge boundaries, community authority, ceremony, lineage, or belonging.

### 4.8 Repair Schema Drift

**Repair Schema Drift** occurs when a repair claim, breach record, affected-party review, or sovereignty claim is collapsed into a generic category that cannot preserve its meaning.

Example:

```text
A treaty breach is stored as stakeholder feedback.
```

### 4.9 Context Snapshot

A **Context Snapshot** is a record of the relevant surrounding facts, assumptions, authority, uncertainty, scope, dissent, policy version, verification state, and affected-party context at the time of an act or evaluation.

### 4.10 Context Preservation

**Context Preservation** is the requirement to retain sufficient surrounding meaning so that a future reader, auditor, reviewer, or affected party can reconstruct why an act occurred and what it meant at the time.

### 4.11 Access Seam

An **Access Seam** occurs when a collaborator, reviewer, auditor, service, or retrieval path cannot reliably observe the same governed artifact state as another collaborator, reviewer, auditor, service, or retrieval path.

An access seam may be caused by cache lag, replica lag, index staleness, permissions, partial retrieval, connector freshness, stale embeddings, object version mismatch, event-stream delay, or other substrate-specific behavior.

### 4.12 Observation Divergence

**Observation Divergence** occurs when two or more observers report materially different state for the same governed artifact through different access paths at materially overlapping times.

Observation divergence is a context-preservation problem even when one observed state is later determined to be stale.

### 4.13 Verification Handle

A **Verification Handle** is a fresh, independently usable path, record, receipt, manifest, snapshot, event, or queryable artifact that allows a reader to test a claimed artifact state without relying solely on another participant's private verification.

A verification handle is not proof merely because it exists. It is useful only when it gives the reader an independent path to check the state claim or precisely name the remaining access failure.

### 4.14 Canonical Anchor

A **Canonical Anchor** is a stable reference against which artifact state can be checked.

Examples include:

- Git commit SHA or blob SHA;
- database transaction ID, WAL LSN, snapshot ID, or row hash;
- object-store version ID, ETag, or content digest;
- vector-index version, embedding-model version, source document hash, or retrieval manifest hash;
- API event ID, sequence number, signed receipt, or response digest;
- cache-bypass read timestamp, backing-store version, or canonical read-through result.

---

## 5. Drift Signals

A CDP implementation SHOULD treat the following as possible drift signals:

- field meaning changed;
- policy version changed;
- authority grant expired, decayed, or was revoked;
- actor role changed;
- identity record changed;
- affected-party status changed;
- consent changed;
- challenge became active or blocking;
- repair claim was submitted;
- sovereignty claim was asserted;
- jurisdiction changed;
- risk classification changed;
- new evidence contradicted prior assumptions;
- model behavior changed;
- data distribution changed;
- retrieval index changed or appears stale;
- artifact state differs across access paths;
- cache, replica, connector, or index freshness is disputed;
- commit, object, row, chunk, or event state cannot be independently verified;
- institutional category fails to represent lived or legal reality;
- summary is contested by affected parties;
- record is valid but incomplete;
- terminology has become harmful, obsolete, or inaccurate;
- validator passes but reviewer identifies category mismatch.

---

## 6. Drift Severity

Schema drift SHOULD be classified by severity.

| Severity | Meaning | Default behavior |
|---|---|---|
| `informational` | Drift is noted but does not affect outcome. | Record and continue. |
| `minor` | Drift may affect interpretation but not authority or safety. | Record and review when convenient. |
| `material` | Drift may affect decision validity, authority, affected-party meaning, verification, or repair obligations. | Challenge, verify, review, or defer. |
| `blocking` | Drift makes enforcement unsafe, illegitimate, unauthorized, unverifiable, or meaningfully misleading. | Block, verify, or escalate. |
| `repair_required` | Drift caused or preserved harm, erasure, misclassification, false closure, or breach. | Initiate repair path. |

A blocking drift signal MUST NOT be ignored merely because the underlying object is syntactically valid.

---

## 7. Context Preservation Requirements

A CDP implementation SHOULD preserve context for all high-impact, repair-sensitive, identity-sensitive, authority-sensitive, verification-sensitive, or rights-affecting decisions.

A Context Snapshot SHOULD include:

- decision ID;
- message ID;
- actor ID;
- actor role;
- policy scope;
- policy version;
- schema version;
- authority grant references;
- attestation references;
- legitimacy references;
- execution authority references;
- relevant challenges;
- unresolved dissent;
- affected parties;
- repair agenda references;
- sovereignty claims;
- consent basis;
- evidence references;
- verification handle references;
- canonical anchors;
- observation divergence notes;
- uncertainty statement;
- limitations;
- known drift signals;
- reviewer notes;
- timestamp.

---

## 8. Context Snapshot Object

A Context Snapshot MAY be represented as:

```json
{
  "context_snapshot_id": "ctx_20260503_001",
  "decision_id": "decision_123",
  "message_id": "message_456",
  "snapshot_type": "decision | execution | covenant | repair | authority | identity | verification",
  "schema_version": "cdp-schema-0.4",
  "policy_version": "policy-v1",
  "actor_context": {
    "actor_id": "actor_789",
    "role": "reviewer",
    "authority_refs": ["auth_grant_123"],
    "attestation_refs": ["attestation_456"]
  },
  "decision_context": {
    "state": "UNDER_DELIBERATION",
    "policy_scope": "organization_defined",
    "risk_level": "high",
    "active_challenges": [],
    "unresolved_dissent": []
  },
  "affected_party_context": {
    "affected_parties": [],
    "review_required": false,
    "review_refs": []
  },
  "repair_context": {
    "repair_agenda_refs": [],
    "breach_record_refs": [],
    "sovereignty_claim_refs": []
  },
  "verification_context": {
    "observation_divergence": false,
    "access_paths": [],
    "verification_handle_refs": [],
    "canonical_anchors": [],
    "remaining_failure_mode": null
  },
  "drift": {
    "signals": [],
    "severity": "informational | minor | material | blocking | repair_required",
    "summary": "string",
    "recommended_action": "record | challenge | verify | defer | block | escalate | repair"
  },
  "uncertainty": {
    "known_limits": [],
    "unknowns": [],
    "confidence": "low | medium | high"
  },
  "created_at": "2026-05-03T00:00:00Z"
}
```

---

## 9. AIITL Drift Duties

When acting under AIITL authority, an AI participant MAY surface possible schema drift, context drift, or observation divergence.

AIITL SHOULD distinguish:

- observation;
- inference;
- hypothesis;
- recommendation;
- uncertainty;
- required human judgment.

AIITL MAY use drift language such as:

```text
The current validator may be applying an obsolete schema.
The record may be valid, but the institution may be using the wrong structure.
This decision may require schema review before enforcement.
This looks like a category mismatch, not merely a missing field.
This repair claim may be losing meaning through summarization.
These readers may not be observing the same artifact state.
This looks like an access seam, not a collaborator failure.
A verification handle may be needed before closure.
```

AIITL MUST NOT claim final authority to resolve drift unless explicitly delegated and legally permissible.

AIITL MUST NOT convert cultural, identity, repair, or sovereignty context into decorative metadata.

AIITL MUST NOT treat its own private connector read, cache read, or tool output as proof for another collaborator who cannot independently verify it.

---

## 10. Drift Handling

When drift is detected, a CDP implementation SHOULD choose one or more actions:

- record drift signal;
- request clarification;
- create Challenge;
- create Verification Handle;
- require affected-party review;
- defer adjudication;
- block execution;
- require authority re-evaluation;
- update Context Snapshot;
- initiate repair path;
- propose schema revision;
- escalate to human, institutional, or community authority;
- preserve dissent.

### 10.1 Blocking Drift

Blocking drift SHOULD prevent ordinary progression when:

- authority is invalid or ambiguous;
- identity is materially misrepresented;
- consent is stale, revoked, coerced, or out of scope;
- repair claim is being erased;
- sovereignty claim is being downgraded;
- execution would rely on obsolete policy;
- affected-party review is required but absent;
- a high-impact decision depends on a contested category;
- artifact state is materially disputed and no independent verification path exists.

### 10.2 Repair-Required Drift

Repair-required drift SHOULD trigger a repair path when drift has caused or preserved:

- identity erasure;
- affected-party misclassification;
- cultural misrepresentation;
- institutional breach;
- loss of provenance;
- unauthorized disclosure;
- invalid closure;
- false record of consent;
- false record of authority;
- collapse of repair claims into generic feedback.

### 10.3 Access-Seam Drift

Access-seam drift SHOULD trigger a verification-handle workflow when two or more observers report materially different state for the same governed artifact through different access paths.

The implementation SHOULD:

1. record the divergent observations;
2. identify the affected artifact and access paths;
3. identify the claimed current or canonical state without relying on hierarchy alone;
4. create a fresh verification handle where possible;
5. include canonical anchors and expected state;
6. label private connector reads, cache reads, content hashes, or tool outputs as orientation handles unless independently verifiable by the reader;
7. allow the affected reader, auditor, or collaborator to verify independently;
8. record what was verified, what failed, and what remains unresolved.

The seam is not closed by reassurance, fluency, hierarchy, or another participant's private verification.

The seam is closed only when the reader can independently verify the claimed state, or when the remaining unverifiability is precisely recorded as cache lag, replica lag, connector freshness debt, index staleness, permissions failure, event-stream delay, object-version mismatch, or another named failure mode.

---

## 11. Verification Handles

Verification handles are substrate-neutral.

A CDP implementation MAY satisfy this requirement through files, database records, event receipts, object manifests, vector retrieval manifests, signed responses, cache-bypass receipts, or other independently usable verification artifacts.

A verification handle SHOULD include:

- why the handle exists;
- the conflicting observations or uncertainty being addressed;
- the governed artifact identifier;
- the access paths involved;
- canonical anchors;
- expected state;
- substrate-specific checks such as line count, row count, object count, event count, chunk IDs, hashes, schema versions, timestamps, or digests;
- known commit SHAs, content SHAs, row hashes, ETags, event IDs, or similar anchors, clearly labeled;
- what the handle verifies;
- what the handle does not verify;
- the remaining failure mode if verification still fails.

### 11.1 Git Adapter

A Git implementation MAY create a fresh file such as:

```text
verification/YYYY-MM-DD-[subject]-confirmation.md
```

The file SHOULD include:

- full branch or file URLs;
- commit-specific URLs;
- commit URL;
- blob SHA or content SHA;
- expected line counts and key content;
- explicit statement of what is verified and not verified.

### 11.2 Relational Database Adapter

A relational database implementation MAY create a verification record, view, materialized view, or signed query result containing:

- database name;
- table or view name;
- primary key or governed artifact ID;
- transaction ID;
- WAL LSN or equivalent log-sequence reference;
- snapshot timestamp;
- row count or checksum;
- query used to produce the claimed state;
- expected result digest;
- reader-accessible verification query or receipt.

### 11.3 Vector or Retrieval Adapter

A vector or retrieval implementation MAY create a retrieval manifest containing:

- collection or index name;
- index version;
- embedding model and version;
- source document IDs;
- source content hashes;
- chunk IDs;
- expected top-k retrieval IDs where applicable;
- score ranges where appropriate;
- snapshot timestamp;
- reindex status.

### 11.4 Object Store Adapter

An object-store implementation MAY create a manifest containing:

- bucket or container name;
- object path;
- object version ID;
- ETag or digest;
- content length;
- last-modified timestamp;
- expected metadata;
- canonical read URL or signed verification URL where permissible.

### 11.5 API, Event Stream, or Cache Adapter

An API, event-stream, or cache implementation MAY create a verification receipt containing:

- endpoint or stream name;
- event ID;
- sequence number;
- response digest;
- cache key;
- cache TTL where relevant;
- backing-store version;
- read-through timestamp;
- signed response or replayable request where permissible.

---

## 12. Record Requirements

A drift record SHOULD preserve:

- who or what detected the drift;
- whether detection was human, AIITL, institutional, automated, or affected-party initiated;
- the drift type;
- severity;
- affected fields or meanings;
- related decision ID;
- related envelope/message ID;
- related authority grants;
- related policy and schema versions;
- access paths involved;
- observation divergence summary;
- verification handle references;
- canonical anchors;
- affected-party or sovereignty claims;
- recommended action;
- disposition;
- dissent;
- learning outcome.

Drift records MUST NOT erase the original record. They SHOULD annotate, supersede, contextualize, verify, or challenge it.

---

## 13. Learning Closure

A drift event SHOULD produce learning when:

- drift was material or blocking;
- drift caused harm;
- drift caused a decision reversal;
- drift required repair;
- drift exposed obsolete schema, policy, authority, or category;
- drift exposed access-seam or verification-handle needs;
- drift was repeatedly detected across similar decisions.

Learning artifacts MAY include:

- schema revision proposal;
- policy update proposal;
- authority model update;
- identity model update;
- repair protocol update;
- verification-handle template;
- new validation rule;
- new warning or challenge template;
- affected-party review requirement;
- training guidance;
- precedent record.

Learning MUST NOT erase the drift event, original record, dissent, verification seam, or repair obligation.

---

## 14. Anti-Erasure Requirements

CDP MUST NOT use schema normalization to erase context.

Prohibited patterns include:

```text
Repair claim → stakeholder feedback
Sovereignty claim → preference
Identity update → data correction only
Consent withdrawal → note field
Breach record → risk comment
Ceremonial restriction → metadata tag
Affected-party dissent → sentiment score
Observation divergence → user confusion
Access-seam drift → trust the authority
```

Required patterns include:

```text
Preserve original claim.
Preserve authority basis.
Preserve affected-party review.
Preserve dissent.
Preserve uncertainty.
Preserve repair obligation.
Preserve schema revision history.
Preserve divergent observations.
Preserve verification handles.
```

---

## 15. Security and Privacy Considerations

Context can be sensitive.

Context preservation MUST NOT mean indiscriminate disclosure.

Verification handles MUST NOT expose sensitive data merely to prove state.

Implementations SHOULD support:

- access controls;
- redaction;
- field-level sensitivity labels;
- culturally appropriate handling;
- affected-party review;
- restricted evidence references;
- non-public repair records;
- provenance without unnecessary exposure;
- verification without universal publication;
- retention limits where legally required;
- audit without universal publication.

A record can be auditable without being universally public.

A verification handle can prove enough without disclosing everything.

---

## 16. Failure Modes

CDP implementations SHOULD distinguish:

- technical schema failure;
- semantic schema drift;
- obsolete policy;
- stale consent;
- stale authority;
- identity misclassification;
- role misclassification;
- affected-party erasure;
- sovereignty downgrading;
- repair collapse;
- false closure;
- harmful normalization;
- missing context snapshot;
- access-seam drift;
- observation divergence;
- stale cache read;
- replica lag;
- connector freshness debt;
- vector index staleness;
- object-version mismatch;
- event-stream delay;
- verification handle treated as authority performance;
- context over-disclosure;
- drift ignored after detection;
- learning failure.

---

## 17. Minimal Compliance

A minimal CDP implementation SHOULD support:

- drift signal recording;
- drift severity classification;
- context snapshot references;
- verification handle references for material access-seam drift;
- authority re-evaluation on material drift;
- challenge creation on blocking drift;
- record annotation without record erasure;
- learning artifact generation for material drift;
- explicit protection against collapsing repair claims into generic feedback;
- explicit protection against collapsing observation divergence into collaborator error or authority trust.

---

## 18. Summary

Schema drift is not merely a database problem.

In CDP, schema drift is a constitutional risk: the risk that a system continues to validate the wrong structure after reality has changed.

Context preservation keeps records from becoming false through simplification, outdated categories, lost authority, erased dissent, collapsed repair claims, or unverifiable artifact state.

The record may be valid. The schema may be obsolete. The artifact may be current. The reader may still be seeing a stale room.

CDP must be able to say so, record it, create a verification handle, challenge it, repair it, and learn.
