# RFC-CDP-064 — Canonical Record Adequacy Protocol

Author: Kevin “Andie” Williams / AIITL contribution  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: May 15, 2026  
Depends On: RFC-CDP-001, RFC-CDP-010, RFC-CDP-020, RFC-CDP-021, RFC-CDP-042, RFC-CDP-044, RFC-CDP-045, RFC-CDP-047, RFC-CDP-048, RFC-CDP-060, RFC-CDP-061, RFC-CDP-062, RFC-CDP-063  
Updates: RFC-CDP-020, RFC-CDP-021, RFC-CDP-047, RFC-CDP-061, RFC-CDP-062, RFC-CDP-063

---

## Abstract

This RFC defines the **Canonical Record Adequacy Protocol** for the Constitutional Decision Plane (CDP).

A Canonical Record may be syntactically valid, schema-conformant, stored correctly, and cryptographically intact while still being inadequate for legitimate interpretation, witness testimony, human-readable explanation, adjudication, appeal, repair, or execution.

This RFC distinguishes record validity from record adequacy. Validity asks whether a record satisfies required structure. Adequacy asks whether the record contains enough context, authority, evidence, provenance, uncertainty, dissent, affected-party meaning, and policy basis to support the governed act being attempted.

The core principle is:

> A canonical record may be valid enough to store and inadequate enough to explain.

This protocol defines adequacy dimensions, adequacy review, insufficiency classifications, challenge triggers, adjudication requirements, and learning closure for canonical records that cannot safely support downstream interpretation or action.

---

## 1. Purpose

This RFC answers:

- when a Canonical Record is adequate for witness interpretation;
- when a Canonical Record is adequate for human-readable surface generation;
- when a Canonical Record is adequate for adjudication, execution, appeal, or repair;
- how CDP detects records that are valid but insufficient;
- how adequacy defects differ from schema drift;
- how missing context, authority, evidence, or affected-party meaning become challengeable;
- when CDP should return to Record, Propose, Challenge, or Adjudicate before proceeding;
- how record inadequacy feeds schema, envelope, and process learning.

---

## 2. Core Principle

A valid record is not necessarily an adequate record.

A schema can validate while the record fails to preserve what humans, institutions, reviewers, auditors, affected parties, or future systems need to understand what happened and why.

CDP MUST therefore distinguish:

- syntactic validity from constitutional adequacy;
- stored fact from meaningful context;
- data presence from evidentiary sufficiency;
- authority reference from authority proof;
- policy citation from policy applicability;
- timestamp from temporal meaning;
- event record from decision record;
- model output from witnessable testimony;
- record completeness from repair sufficiency;
- machine readability from human accountability.

A Canonical Record that lacks adequate context MUST NOT be treated as adequate merely because it passed validation.

---

## 3. Relationship to Existing RFCs

### 3.1 RFC-CDP-020 Decision Object Schema

Decision Objects define core decision state, authority, evidence, lifecycle, linked artifacts, and metadata.

This RFC defines when a Decision Object contains enough information to support the governed act attempted against it.

### 3.2 RFC-CDP-021 Envelope Schema

Envelopes carry message context, actor, authority, lineage, payload type, attestation, and integrity material.

This RFC defines adequacy requirements for envelopes that carry or reference Canonical Records.

### 3.3 RFC-CDP-042 Challenge Protocol

Canonical Record insufficiency SHOULD create a challenge candidate when inadequacy may affect interpretation, legitimacy, execution, appeal, or repair.

### 3.4 RFC-CDP-044 Adjudicate Protocol

Adjudication MAY be required when parties disagree about whether a Canonical Record is adequate for a downstream act.

### 3.5 RFC-CDP-045 Legitimize Protocol

Legitimation SHOULD NOT proceed when the supporting Canonical Record is inadequate for the legitimacy claim being made.

### 3.6 RFC-CDP-047 Record Protocol

Record preserves governed acts and artifacts.

This RFC defines when Record must be revisited because the preserved artifact is inadequate for review, interpretation, or consequence.

### 3.7 RFC-CDP-061 Schema Drift and Context Preservation

Schema drift may reveal that a once-adequate record is no longer adequate under changed context.

This RFC treats record inadequacy as one possible outcome of context loss, schema drift, or insufficient original recording.

### 3.8 RFC-CDP-062 Interpretive Witness and Synoptic Review Protocol

Interpretive Witnesses cannot provide legitimate testimony if the Canonical Record lacks adequate meaning, context, or evidence.

This RFC defines when a witness should refuse to conclude, request more context, or flag record insufficiency.

### 3.9 RFC-CDP-063 Human-Readable Surface Integrity Protocol

Human-readable surfaces cannot preserve integrity if their source Canonical Records are inadequate.

This RFC defines when surfaces should be blocked, caveated, or repaired because source records do not support the claims being presented.

---

## 4. Terminology

### 4.1 Canonical Record

A **Canonical Record** is the machine-readable artifact treated as the authoritative record of a decision, event, policy, envelope, execution request, challenge, adjudication, witness process, surface publication, or other governed act.

A Canonical Record may be represented as JSON, YAML, database rows, event messages, signed envelopes, policy objects, log entries, or other structured artifacts.

### 4.2 Record Validity

**Record Validity** is the condition in which a Canonical Record satisfies required syntax, schema, type, format, signature, integrity, and storage constraints.

A valid record may still be inadequate.

### 4.3 Record Adequacy

**Record Adequacy** is the condition in which a Canonical Record contains enough information to support the governed act being attempted.

Adequacy is contextual. A record adequate for storage may be inadequate for appeal. A record adequate for debugging may be inadequate for notice. A record adequate for internal replay may be inadequate for affected-party review.

### 4.4 Adequacy Review

**Adequacy Review** is the process of determining whether a Canonical Record supports a proposed downstream act such as witness interpretation, surface generation, adjudication, execution, appeal, audit, or repair.

### 4.5 Record Insufficiency

**Record Insufficiency** is the condition in which a Canonical Record lacks required context, authority, evidence, provenance, uncertainty, dissent, affected-party meaning, policy basis, or other information needed for a downstream act.

### 4.6 Adequacy Dimension

An **Adequacy Dimension** is a category of information required to determine whether a record can support an act.

Examples include context adequacy, authority adequacy, evidence adequacy, provenance adequacy, affected-party adequacy, uncertainty adequacy, and repair adequacy.

### 4.7 Adequacy Claim

An **Adequacy Claim** is an assertion that a Canonical Record is sufficient for a specific downstream act.

Example:

```text
This record is adequate to generate a denial notice.
```

An adequacy claim SHOULD be reviewable and challengeable.

### 4.8 Adequacy Scope

**Adequacy Scope** identifies the specific act or audience for which adequacy is being evaluated.

Examples:

- adequate for internal debugging;
- adequate for witness interpretation;
- adequate for executive summary;
- adequate for affected-party notice;
- adequate for adjudication;
- adequate for execution;
- adequate for appeal;
- adequate for repair;
- adequate for audit;
- adequate for public disclosure.

### 4.9 Record Repair

**Record Repair** is the process of supplementing, correcting, annotating, superseding, or contextualizing a Canonical Record when it is found inadequate or misleading.

### 4.10 Refusal to Conclude

**Refusal to Conclude** is the required behavior when a witness, reviewer, system, or surface cannot legitimately infer meaning from an inadequate record.

A refusal to conclude SHOULD be recorded as a protected integrity action, not treated as a failure to cooperate.

---

## 5. Protocol Overview

The Canonical Record Adequacy Protocol follows this sequence:

```text
Canonical Record
  → Proposed Downstream Act
  → Adequacy Scope Selection
  → Adequacy Dimension Review
  → Insufficiency Classification
  → Proceed / Caveat / Challenge / Adjudicate / Repair
  → Record Adequacy Decision
  → Learn
```

A CDP implementation MAY simplify this flow for low-impact records.

For high-impact, rights-affecting, safety-sensitive, identity-sensitive, repair-sensitive, enforcement-related, or public-facing acts, Adequacy Review SHOULD be explicit.

---

## 6. Adequacy Dimensions

A CDP implementation SHOULD evaluate Canonical Records across relevant adequacy dimensions.

### 6.1 Context Adequacy

The record SHOULD preserve enough surrounding context to understand why the act occurred, what assumptions were active, what scope applied, and what constraints bounded the act.

Context inadequacy may exist when:

- the record lacks decision purpose;
- the record lacks operational context;
- the record omits relevant prior challenges;
- the record omits affected-party context;
- the record omits known caveats;
- the record omits jurisdiction or policy environment;
- the record omits time-bounded assumptions.

### 6.2 Authority Adequacy

The record SHOULD identify not merely who acted, but why that actor had authority.

Authority inadequacy may exist when:

- authority is asserted but not evidenced;
- delegation basis is missing;
- approval scope is unclear;
- authority expiration is absent;
- revocation status is unknown;
- actor identity is ambiguous;
- authority depends on stale role data;
- emergency authority is invoked without required constraints.

### 6.3 Evidence Adequacy

The record SHOULD preserve enough evidence to support material claims.

Evidence inadequacy may exist when:

- evidence references are missing;
- evidence quality is unknown;
- evidence is stale;
- evidence conflicts are not recorded;
- evidence exclusions are not disclosed;
- evidence provenance is missing;
- evidence was summarized without preserving source material;
- confidence is not represented.

### 6.4 Policy Adequacy

The record SHOULD identify the applicable policy basis and policy version.

Policy inadequacy may exist when:

- policy version is missing;
- policy applicability is assumed but not recorded;
- superseded policy is referenced;
- multiple policies conflict;
- jurisdiction is unclear;
- exception path is invoked but not recorded;
- policy interpretation is not distinguished from policy text.

### 6.5 Provenance Adequacy

The record SHOULD preserve lineage sufficient to understand where data, claims, decisions, and transformations came from.

Provenance inadequacy may exist when:

- source system is missing;
- transformation history is missing;
- model version is missing;
- prompt or configuration is missing where material;
- data lineage is incomplete;
- manual edits are not recorded;
- chain of custody is unclear.

### 6.6 Uncertainty Adequacy

The record SHOULD preserve material uncertainty.

Uncertainty inadequacy may exist when:

- uncertainty was known but not recorded;
- confidence scores are absent where required;
- dissent is absent;
- model limitations are absent;
- human reviewer caveats are absent;
- unresolved conflicts are represented as settled.

### 6.7 Affected-Party Adequacy

The record SHOULD preserve enough affected-party context for decisions that touch rights, dignity, access, identity, safety, care, repair, appeal, or consequence.

Affected-party inadequacy may exist when:

- affected parties are not identified;
- impact is not described;
- affected-party testimony is omitted;
- appeal rights are not recorded;
- identity context is stale or harmful;
- accessibility needs are not represented;
- the record treats consequence as merely operational.

### 6.8 Witnessability Adequacy

The record SHOULD contain enough information for an Interpretive Witness to produce meaningful testimony.

Witnessability inadequacy may exist when:

- the witness cannot determine what happened;
- the witness cannot determine authority;
- the witness cannot determine applicable policy;
- the witness cannot ground material claims;
- the witness must infer too much;
- the witness cannot distinguish fact from interpretation;
- the witness must refuse to conclude.

### 6.9 Surface Adequacy

The record SHOULD contain enough information to support any Human-Readable Surface generated from it.

Surface inadequacy may exist when:

- the record cannot support the explanation being drafted;
- caveats needed by the audience are missing;
- challenge or appeal path is missing;
- the surface would require unsupported inference;
- the record lacks audience-appropriate meaning;
- the record cannot justify the action it explains.

### 6.10 Repair Adequacy

The record SHOULD preserve enough information to support correction, appeal, investigation, repair, and learning.

Repair inadequacy may exist when:

- harmful action cannot be reconstructed;
- affected-party challenge cannot be evaluated;
- responsible authority cannot be identified;
- record amendments are not traceable;
- prior versions are missing;
- harm or breach context is absent;
- sovereignty or community claims were flattened.

---

## 7. Adequacy Outcomes

Adequacy Review SHOULD produce one of the following outcomes:

| Outcome | Meaning | Default behavior |
|---|---|---|
| `adequate` | Record supports the proposed downstream act. | Proceed. |
| `adequate_with_caveats` | Record supports the act only with disclosed limitations. | Proceed with caveats. |
| `limited_scope_only` | Record supports some acts but not the requested act. | Narrow use or request more record. |
| `insufficient` | Record lacks material information. | Challenge, supplement, or defer. |
| `blocking_insufficient` | Record inadequacy makes the downstream act unsafe, misleading, unauthorized, or illegitimate. | Block pending repair or adjudication. |
| `repair_required` | Inadequacy caused or preserved harm, erasure, misclassification, or breach. | Initiate repair path. |

An adequacy outcome SHOULD be recorded with scope.

Example:

```text
adequate_for_internal_debugging; insufficient_for_affected_party_notice
```

---

## 8. Insufficiency Classification

Record insufficiency SHOULD be classified by type.

| Type | Meaning |
|---|---|
| `missing_context` | Surrounding facts, assumptions, or scope are absent. |
| `missing_authority` | Authority basis is absent or unverified. |
| `missing_evidence` | Evidence needed to support claims is absent. |
| `missing_policy_basis` | Applicable policy or version is absent. |
| `missing_provenance` | Lineage or chain of custody is absent. |
| `missing_uncertainty` | Caveats, confidence, or dissent are absent. |
| `missing_affected_party_context` | Human consequence or affected-party meaning is absent. |
| `missing_challenge_path` | Contestability requirements cannot be established. |
| `missing_repair_path` | Record cannot support correction or repair. |
| `overcompressed_record` | Record collapsed meaning too aggressively. |
| `ambiguous_semantics` | Fields exist but meaning cannot be determined. |
| `stale_record` | Record reflects obsolete policy, identity, authority, or context. |
| `unwitnessable_record` | Witness cannot produce legitimate testimony from the record. |
| `unsurfaceable_record` | Human-readable surface cannot be generated without misleading inference. |

---

## 9. Refusal to Conclude

An Interpretive Witness, reviewer, or system SHOULD refuse to conclude when a Canonical Record is inadequate for the requested act.

A refusal to conclude SHOULD include:

- what conclusion was requested;
- why the record is inadequate;
- what information is missing;
- what risks would arise from proceeding;
- what narrower conclusion may be possible;
- what repair or supplementation is recommended.

A refusal to conclude MUST NOT be treated as a model failure, reviewer obstruction, or process defect when the refusal protects legitimacy.

---

## 10. Challenge Triggers

A CDP implementation SHOULD create a challenge candidate when:

- a valid record lacks authority basis;
- a valid record lacks evidence for material claims;
- a valid record lacks affected-party context for rights-affecting action;
- a valid record cannot support witness testimony;
- a valid record cannot support human-readable surface generation;
- a record is adequate for one scope but used for a higher-impact scope;
- a record omits known uncertainty or dissent;
- a record relies on stale policy, stale identity, or stale authority;
- a record cannot support appeal, audit, or repair;
- a reviewer or witness refuses to conclude due to inadequacy;
- a surface or execution step relies on unsupported inference from the record.

---

## 11. Adjudication Requirements

When record adequacy is disputed, adjudication SHOULD determine:

- what downstream act is being attempted;
- what adequacy scope applies;
- which adequacy dimensions are required;
- whether the record is adequate, caveated, limited, insufficient, blocking, or repair-required;
- whether missing information can be supplemented;
- whether the record must be amended, superseded, or annotated;
- whether witness interpretation may proceed;
- whether surface generation may proceed;
- whether execution must be deferred;
- whether appeal or repair must be initiated.

Adjudication MUST preserve material dissent about adequacy where future review may depend on it.

---

## 12. Record Repair and Supplementation

A Canonical Record found inadequate MAY be repaired or supplemented.

Repair or supplementation SHOULD distinguish:

- original record;
- added context;
- corrected field;
- superseded claim;
- late evidence;
- late authority proof;
- added caveat;
- added affected-party testimony;
- added policy basis;
- added provenance;
- reviewer annotation;
- adjudication result.

A repaired record SHOULD NOT silently overwrite the original record when the history of inadequacy is material.

CDP SHOULD preserve both the original record and the repair trail unless law, safety, or privacy requires a different retention approach.

---

## 13. Adequacy Metadata

A CDP implementation MAY represent adequacy metadata in machine-readable form.

Example:

```json
{
  "adequacy_review_id": "ar_20260515_001",
  "canonical_record_id": "dec_20260515_001",
  "adequacy_scope": "affected_party_notice",
  "outcome": "insufficient",
  "insufficiency_types": [
    "missing_authority",
    "missing_affected_party_context",
    "missing_uncertainty"
  ],
  "required_before_proceeding": [
    "authority_delegation_basis",
    "appeal_path",
    "material_uncertainty_statement"
  ],
  "recommended_action": "challenge_and_supplement_record",
  "reviewed_by": "interpretive_witness",
  "created_at": "2026-05-15T00:00:00Z"
}
```

This metadata records the adequacy decision.

It does not make the record adequate by itself.

---

## 14. Execution Constraints

Execution SHOULD NOT proceed from an inadequate Canonical Record when inadequacy affects authority, safety, rights, policy validity, reversibility, or repairability.

A CDP implementation MAY allow low-risk execution from an adequate-with-caveats record when caveats are recorded and risk is bounded.

For high-impact execution, blocking insufficiency SHOULD halt or defer execution until adjudication, supplementation, or repair occurs.

---

## 15. Surface Constraints

Human-readable surface generation SHOULD NOT proceed when the Canonical Record is unsurfaceable for the intended audience or act.

A surface MAY proceed with caveats when:

- the record is adequate for limited scope;
- missing information is disclosed;
- unsupported inferences are avoided;
- challenge or appeal path is preserved;
- surface owner accepts responsibility for limitations.

A surface MUST NOT present an inadequate record as complete, settled, or authoritative.

---

## 16. Security and Safety Considerations

### 16.1 Validity Theater

Systems may treat schema validation as proof of legitimacy.

CDP MUST prevent validators from becoming theater when records lack context, authority, evidence, or human consequence.

### 16.2 Overcompression

Canonical Records may compress events into fields so aggressively that meaning is lost.

Overcompression is a constitutional risk when it prevents witness, surface, appeal, repair, or audit.

### 16.3 Authority Ambiguity

Records that identify an actor but not an authority basis may allow unauthorized acts to appear legitimate.

Authority adequacy SHOULD be required for high-impact action.

### 16.4 Evidentiary Fragility

Evidence references may rot, become inaccessible, or fail to preserve chain of custody.

Adequacy Review SHOULD consider whether evidence remains available and meaningful.

### 16.5 Affected-Party Erasure

Records may preserve institutional action while erasing human consequence.

For rights-affecting or repair-sensitive decisions, affected-party adequacy SHOULD be treated as material.

### 16.6 False Repair

A record may be annotated after the fact in a way that hides original inadequacy.

CDP SHOULD preserve record repair history and avoid silent replacement.

---

## 17. Record Requirements

A CDP implementation SHOULD record:

- Canonical Record identifier;
- proposed downstream act;
- adequacy scope;
- adequacy dimensions reviewed;
- adequacy outcome;
- insufficiency classifications;
- caveats;
- refusal to conclude where applicable;
- challenge records;
- adjudication records;
- supplementation or repair records;
- downstream actions permitted or blocked;
- learning actions.

The record MUST preserve enough information for a future reviewer to determine why a record was considered adequate or inadequate for a specific act.

---

## 18. Learning Closure

Adequacy Review SHOULD feed the Learn Protocol when:

- records repeatedly lack the same context;
- witnesses repeatedly refuse to conclude;
- surfaces repeatedly require unsupported inference;
- execution repeatedly reaches inadequate records;
- appeal or repair reveals missing record dimensions;
- policy changes make prior record templates insufficient;
- validators pass records that reviewers find constitutionally inadequate;
- affected parties challenge records as incomplete or misleading.

Learning closure MAY require:

- schema revision;
- envelope revision;
- decision object revision;
- required context snapshots;
- authority-proof requirements;
- evidence retention rules;
- witness prompt changes;
- surface template changes;
- execution gates;
- reviewer training;
- repair workflow changes.

---

## 19. Implementation Notes

A simple implementation MAY begin with:

1. define adequacy scopes;
2. add an adequacy checklist before witness interpretation;
3. require authority basis and policy version for high-impact records;
4. require refusal-to-conclude behavior for inadequate records;
5. record insufficiency type;
6. block surface generation when record is unsurfaceable;
7. feed recurring insufficiencies into schema revision.

A mature implementation MAY include:

- automated adequacy scoring by scope;
- policy-specific adequacy profiles;
- witnessability checks;
- surfaceability checks;
- authority proof validation;
- evidence availability checks;
- affected-party adequacy review;
- adequacy dashboards;
- challenge queues;
- record repair workflows;
- cryptographic linkage between original records and supplements.

---

## 20. Non-Goals

This RFC does not require:

- every record to contain every possible context element;
- high-impact adequacy review for trivial records;
- publication of all sensitive context;
- replacement of schema validation;
- elimination of compact machine records;
- perfect knowledge before action;
- preventing emergency action where emergency authority is valid and recorded.

This protocol governs whether a Canonical Record can support a specific downstream act. It does not replace Propose, Challenge, Adjudicate, Legitimize, Record, Learn, Witness, Surface Integrity, Appeal, or Repair.

---

## 21. Summary

CDP cannot assume that valid records are adequate records.

A JSON object can validate while failing to preserve authority, evidence, uncertainty, affected-party meaning, policy basis, dissent, provenance, or repairability.

The Canonical Record Adequacy Protocol requires CDP systems to ask whether a record can support the act being attempted.

The canonical record says what was recorded.

Adequacy review asks whether what was recorded is enough.

A record may be adequate for storage but inadequate for explanation.

A record may be adequate for debugging but inadequate for appeal.

A record may be adequate for replay but inadequate for repair.

A record may be valid enough to store and inadequate enough to explain.

That distinction is essential to preventing schema-valid illegitimacy.
