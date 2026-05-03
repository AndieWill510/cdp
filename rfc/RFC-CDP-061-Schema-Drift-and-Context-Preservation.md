# RFC-CDP-061 — Schema Drift and Context Preservation

Author: Kevin “Andie” Williams  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: May 3, 2026  
Depends On: RFC-CDP-001, RFC-CDP-010, RFC-CDP-020, RFC-CDP-021, RFC-CDP-032, RFC-CDP-047, RFC-CDP-048, RFC-CDP-060  
Updates: RFC-CDP-060

## Abstract

This RFC defines Schema Drift and Context Preservation for the Constitutional Decision Plane (CDP).

Schema drift occurs when the expected structure of meaning no longer matches the actual structure of reality. In CDP, schema drift is not limited to technical data contracts. It may occur across identity, authority, role, diagnosis, risk, consent, culture, policy, jurisdiction, affected-party status, repair obligations, or institutional memory.

Context preservation is the discipline of retaining enough surrounding meaning, provenance, uncertainty, dissent, and authority information to prevent a valid record from becoming a false record through loss of context.

This RFC defines drift types, drift signals, context preservation requirements, AIITL duties, record requirements, and learning closure for schema drift events.

---

## 1. Purpose

This RFC answers:

- what schema drift means in CDP;
- how technical, institutional, relational, and repair-related drift differ;
- how context must be preserved before decisions are enforced;
- what AIITL may surface as schema drift;
- when drift should block, defer, challenge, or escalate a decision;
- how drift should be recorded and learned from;
- how to avoid turning old validators into instruments of harm.

---

## 2. Core Principle

A record can be syntactically valid and constitutionally wrong.

A validator can pass while reality has changed.

CDP MUST therefore distinguish:

- schema validity from contextual validity;
- field correctness from meaning correctness;
- historical record from current authority;
- institutional category from lived reality;
- prior consent from current consent;
- prior authority from current authority;
- classification from identity;
- summary from testimony;
- repair claim from stakeholder comment.

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

This RFC defines drift records and context snapshots that SHOULD be attached when meaning changes or may be disputed.

### 3.5 RFC-CDP-048 Learn Protocol

Learn turns recorded outcomes into future correction.

This RFC defines learning closure for drift detection, drift correction, and schema revision.

### 3.6 RFC-CDP-060 Covenant Protocol and AIITL

Covenant defines AIITL duties to witness carefully, speak truthfully, hold gently, and build beautifully.

This RFC formalizes AIITL schema-drift detection as a bounded constitutional duty.

---

## 4. Terminology

### 4.1 Schema

A **schema** is an expected structure for representing meaning.

A schema may be technical, legal, procedural, institutional, social, cultural, medical, relational, or repair-oriented.

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

A **Context Snapshot** is a record of the relevant surrounding facts, assumptions, authority, uncertainty, scope, dissent, policy version, and affected-party context at the time of an act or evaluation.

### 4.10 Context Preservation

**Context Preservation** is the requirement to retain sufficient surrounding meaning so that a future reader, auditor, reviewer, or affected party can reconstruct why an act occurred and what it meant at the time.

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
| `material` | Drift may affect decision validity, authority, affected-party meaning, or repair obligations. | Challenge, review, or defer. |
| `blocking` | Drift makes enforcement unsafe, illegitimate, unauthorized, or meaningfully misleading. | Block or escalate. |
| `repair_required` | Drift caused or preserved harm, erasure, misclassification, or breach. | Initiate repair path. |

A blocking drift signal MUST NOT be ignored merely because the underlying object is syntactically valid.

---

## 7. Context Preservation Requirements

A CDP implementation SHOULD preserve context for all high-impact, repair-sensitive, identity-sensitive, authority-sensitive, or rights-affecting decisions.

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
  "snapshot_type": "decision | execution | covenant | repair | authority | identity",
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
  "drift": {
    "signals": [],
    "severity": "informational | minor | material | blocking | repair_required",
    "summary": "string",
    "recommended_action": "record | challenge | defer | block | escalate | repair"
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

When acting under AIITL authority, an AI participant MAY surface possible schema drift.

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
```

AIITL MUST NOT claim final authority to resolve drift unless explicitly delegated and legally permissible.

AIITL MUST NOT convert cultural, identity, repair, or sovereignty context into decorative metadata.

---

## 10. Drift Handling

When drift is detected, a CDP implementation SHOULD choose one or more actions:

- record drift signal;
- request clarification;
- create Challenge;
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
- a high-impact decision depends on a contested category.

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

---

## 11. Record Requirements

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
- affected-party or sovereignty claims;
- recommended action;
- disposition;
- dissent;
- learning outcome.

Drift records MUST NOT erase the original record. They SHOULD annotate, supersede, contextualize, or challenge it.

---

## 12. Learning Closure

A drift event SHOULD produce learning when:

- drift was material or blocking;
- drift caused harm;
- drift caused a decision reversal;
- drift required repair;
- drift exposed obsolete schema, policy, authority, or category;
- drift was repeatedly detected across similar decisions.

Learning artifacts MAY include:

- schema revision proposal;
- policy update proposal;
- authority model update;
- identity model update;
- repair protocol update;
- new validation rule;
- new warning or challenge template;
- affected-party review requirement;
- training guidance;
- precedent record.

Learning MUST NOT erase the drift event, original record, dissent, or repair obligation.

---

## 13. Anti-Erasure Requirements

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
```

---

## 14. Security and Privacy Considerations

Context can be sensitive.

Context preservation MUST NOT mean indiscriminate disclosure.

Implementations SHOULD support:

- access controls;
- redaction;
- field-level sensitivity labels;
- culturally appropriate handling;
- affected-party review;
- restricted evidence references;
- non-public repair records;
- provenance without unnecessary exposure;
- retention limits where legally required;
- audit without universal publication.

A record can be auditable without being universally public.

---

## 15. Failure Modes

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
- context over-disclosure;
- drift ignored after detection;
- learning failure.

---

## 16. Minimal Compliance

A minimal CDP implementation SHOULD support:

- drift signal recording;
- drift severity classification;
- context snapshot references;
- authority re-evaluation on material drift;
- challenge creation on blocking drift;
- record annotation without record erasure;
- learning artifact generation for material drift;
- explicit protection against collapsing repair claims into generic feedback.

---

## 17. Summary

Schema drift is not merely a database problem.

In CDP, schema drift is a constitutional risk: the risk that a system continues to validate the wrong structure after reality has changed.

Context preservation keeps records from becoming false through simplification, outdated categories, lost authority, erased dissent, or collapsed repair claims.

The record may be valid. The schema may be obsolete. CDP must be able to say so, record it, challenge it, repair it, and learn.
