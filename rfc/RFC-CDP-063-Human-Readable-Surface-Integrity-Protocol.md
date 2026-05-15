# RFC-CDP-063 — Human-Readable Surface Integrity Protocol

Author: Kevin “Andie” Williams / AIITL contribution  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: May 15, 2026  
Depends On: RFC-CDP-001, RFC-CDP-010, RFC-CDP-020, RFC-CDP-021, RFC-CDP-042, RFC-CDP-044, RFC-CDP-045, RFC-CDP-047, RFC-CDP-048, RFC-CDP-060, RFC-CDP-061, RFC-CDP-062  
Updates: RFC-CDP-021, RFC-CDP-045, RFC-CDP-047, RFC-CDP-061, RFC-CDP-062

---

## Abstract

This RFC defines the **Human-Readable Surface Integrity Protocol** for the Constitutional Decision Plane (CDP).

A Human-Readable Surface is any explanation, notice, report, dashboard, recommendation, email, user-interface message, rationale, transcript, summary, or narrative representation that presents CDP meaning to a human reader.

Human-readable surfaces are not neutral renderings of machine-readable state. They are interpretive artifacts. They may omit context, overstate certainty, hide dissent, flatten testimony, misrepresent authority, or convert unresolved interpretation into apparent institutional truth.

This RFC defines how CDP systems preserve integrity between canonical machine-readable records, witness testimony, adjudicated meaning, and the human-facing surfaces that people actually read and rely upon.

---

## 1. Purpose

This RFC answers:

- what counts as a Human-Readable Surface in CDP;
- why human-facing explanations require governance rather than mere generation;
- how surfaces remain bound to canonical records and Witness Records;
- how surfaces disclose uncertainty, inference, dissent, and unresolved divergence;
- how surfaces avoid laundering model output into institutional authority;
- how affected humans can challenge surfaces that misrepresent meaning;
- how CDP records, versions, reviews, and repairs surface drift.

---

## 2. Core Principle

A human-readable surface is not the decision.

A human-readable surface is not the canonical record.

A human-readable surface is not automatically truth.

It is a governed interpretive presentation of meaning.

CDP MUST therefore distinguish:

- canonical record from displayed explanation;
- witness testimony from final surface;
- adjudicated meaning from generated wording;
- policy basis from rhetorical justification;
- confidence from authority;
- omission from simplification;
- publication from legitimacy;
- comprehension from consent;
- human-readable from human-accountable.

A surface that humans rely on must be worthy of reliance.

---

## 3. Relationship to Existing RFCs

### 3.1 RFC-CDP-020 Decision Object Schema

Decision Objects preserve canonical decision state, policy basis, evidence, authority, lifecycle status, and linked artifacts.

This RFC defines how human-readable surfaces reference, summarize, and present those decision objects without replacing them.

### 3.2 RFC-CDP-021 Envelope Schema

The Envelope carries actor, authority, lineage, payload type, integrity material, and context.

This RFC defines surface-binding requirements for envelopes that carry or reference human-readable outputs.

### 3.3 RFC-CDP-042 Challenge Protocol

Human-readable surface defects SHOULD become challenge candidates when they materially affect understanding, rights, action, authority, or appeal.

### 3.4 RFC-CDP-044 Adjudicate Protocol

Surface disputes MAY require adjudication when generated wording, witness testimony, policy interpretation, or canonical records diverge.

### 3.5 RFC-CDP-045 Legitimize Protocol

A surface SHOULD NOT be treated as legitimated merely because it is fluent, approved by a model, or derived from valid JSON.

Legitimation requires a governed relationship between record, testimony, surface, authority, and review.

### 3.6 RFC-CDP-047 Record Protocol

Human-readable surfaces, versions, approvals, challenges, retractions, and repairs SHOULD be recorded as governed artifacts.

### 3.7 RFC-CDP-061 Schema Drift and Context Preservation

Human-readable surfaces are a primary location where schema drift becomes visible to humans.

Surface drift occurs when the meaning presented to humans diverges from the canonical record, current context, authority, witness testimony, or adjudicated meaning.

### 3.8 RFC-CDP-062 Interpretive Witness and Synoptic Review Protocol

RFC-CDP-062 defines Witness Records and Synoptic Review.

This RFC governs the downstream human-readable surfaces produced from canonical records, Witness Records, and adjudicated findings.

---

## 4. Terminology

### 4.1 Human-Readable Surface

A **Human-Readable Surface** is any artifact intended for human interpretation or reliance.

Examples include:

- eligibility notices;
- denial explanations;
- approval explanations;
- dashboards;
- reports;
- summaries;
- email notifications;
- chat responses;
- user-interface messages;
- executive briefings;
- audit narratives;
- public statements;
- appeal instructions;
- policy rationales;
- generated recommendations.

### 4.2 Surface Integrity

**Surface Integrity** is the condition in which a Human-Readable Surface faithfully, proportionately, and contestably represents the canonical record, relevant Witness Records, adjudications, caveats, and unresolved uncertainties.

Surface integrity does not require exhaustive disclosure of every internal detail. It requires that what is presented does not materially mislead the human audience.

### 4.3 Surface Binding

**Surface Binding** is the traceable relationship between a Human-Readable Surface and the artifacts that support it.

A surface may bind to:

- canonical records;
- decision objects;
- envelopes;
- policy artifacts;
- evidence records;
- Witness Records;
- grounding maps;
- adjudications;
- challenge records;
- context snapshots;
- repair records.

### 4.4 Surface Claim

A **Surface Claim** is a discrete statement in a Human-Readable Surface that asserts, implies, explains, summarizes, recommends, or instructs.

Examples:

```text
Your application was denied because the required documentation was not received.
```

```text
This action is authorized under the delegated authority recorded for the reviewer.
```

```text
The system found no material policy conflict.
```

### 4.5 Material Surface Claim

A **Material Surface Claim** is a Surface Claim that may affect rights, duties, trust, action, appeal, safety, identity, affected-party meaning, institutional accountability, or legal/policy interpretation.

### 4.6 Surface Drift

**Surface Drift** occurs when a Human-Readable Surface diverges materially from the canonical record, relevant testimony, current context, authority, adjudicated meaning, or known uncertainty.

### 4.7 Surface Defect

A **Surface Defect** is a flaw in a Human-Readable Surface that may mislead, obscure, overstate, erase, or improperly authorize.

Surface defects include omission, false certainty, unsupported inference, stale authority, hidden model interpretation, misleading simplification, missing appeal path, harmful categorization, or suppressed dissent.

### 4.8 Surface Owner

A **Surface Owner** is the human, team, system, institution, or role responsible for approving, publishing, maintaining, retracting, or repairing a Human-Readable Surface.

### 4.9 Surface Audience

A **Surface Audience** is the intended human reader or affected group.

A surface audience may include affected parties, operators, auditors, policymakers, executives, regulators, courts, communities, or the general public.

### 4.10 Surface Status

**Surface Status** indicates the lifecycle state of a Human-Readable Surface.

Recommended statuses include:

- `draft`;
- `generated`;
- `under_review`;
- `adjudication_required`;
- `approved`;
- `published`;
- `challenged`;
- `superseded`;
- `retracted`;
- `repaired`;
- `archived`.

---

## 5. Protocol Overview

The Human-Readable Surface Integrity Protocol follows this sequence:

```text
Canonical Record / Witness Records / Adjudication
  → Surface Generation or Drafting
  → Surface Claim Extraction
  → Surface Binding
  → Integrity Review
  → Disclosure and Challenge Check
  → Approval / Publication
  → Record
  → Monitor / Challenge / Repair / Learn
```

A CDP implementation MAY simplify this flow for low-impact internal surfaces.

For high-impact, rights-affecting, safety-sensitive, identity-sensitive, repair-sensitive, or enforcement-related surfaces, the full protocol SHOULD apply.

---

## 6. Surface Generation Requirements

A Human-Readable Surface MAY be generated by an AI system, drafted by a human, assembled from templates, produced by a rule engine, or composed by multiple systems.

Regardless of origin, a surface SHOULD identify:

- source canonical records;
- relevant Witness Records;
- relevant adjudications;
- applicable policy basis;
- surface audience;
- surface owner;
- generation or authorship method;
- review status;
- publication status;
- challenge path.

A generated surface MUST NOT be treated as approved merely because it was generated from approved data.

A templated surface MUST NOT be treated as accurate merely because the template was approved.

A human-authored surface MUST NOT be treated as legitimate merely because a human wrote it.

---

## 7. Surface Claim Extraction

A CDP implementation SHOULD extract material Surface Claims before approval or publication.

Claim extraction MAY be manual, automated, AI-assisted, or hybrid.

Each material Surface Claim SHOULD be classified as one or more of:

- fact;
- interpretation;
- inference;
- policy basis;
- authority claim;
- evidence claim;
- risk claim;
- recommendation;
- instruction;
- caveat;
- appeal instruction;
- affected-party impact;
- unresolved uncertainty.

Each material Surface Claim SHOULD be traceable to at least one supporting artifact or explicitly marked as ungrounded, inferred, unresolved, or rhetorical.

---

## 8. Surface Binding Requirements

A Human-Readable Surface SHOULD include or be associated with a Surface Binding record.

The Surface Binding record MAY be machine-readable.

Example:

```json
{
  "surface_id": "surf_20260515_001",
  "surface_type": "decision_explanation",
  "surface_artifact_ref": "artifact://surfaces/surf_20260515_001.pdf",
  "canonical_record_refs": ["dec_20260515_001"],
  "witness_record_refs": [
    "artifact://witness-testimony/wit_20260515_001.pdf",
    "artifact://witness-testimony/wit_20260515_002.pdf"
  ],
  "adjudication_refs": ["adj_20260515_001"],
  "claim_binding_ref": "artifact://surface-bindings/surf_20260515_001.json",
  "status": "under_review",
  "surface_owner": "policy_review_team",
  "created_at": "2026-05-15T00:00:00Z"
}
```

This metadata is not the surface.

It is the control record that binds the surface to its sources.

The Human-Readable Surface itself SHOULD be preserved in a durable human-readable format such as PDF, PDF/A, signed HTML rendered to PDF, Markdown with rendered artifact, DOCX with rendered artifact, or another approved human-readable form.

---

## 9. Integrity Review

Before approval, a Human-Readable Surface SHOULD be reviewed for integrity.

Integrity Review SHOULD ask:

- Does the surface accurately represent the canonical record?
- Does the surface preserve material witness testimony?
- Does the surface hide unresolved divergence?
- Does the surface overstate certainty?
- Does the surface imply authority that has not been granted?
- Does the surface omit material caveats?
- Does the surface preserve affected-party meaning?
- Does the surface distinguish fact from interpretation?
- Does the surface distinguish decision from recommendation?
- Does the surface provide a challenge or appeal path when required?
- Does the surface remain understandable to its intended audience?
- Does the surface create new schema drift by simplifying too aggressively?

A surface that fails Integrity Review SHOULD NOT be published without adjudication or exception handling.

---

## 10. Required Disclosures

A Human-Readable Surface SHOULD disclose, as appropriate to risk and audience:

- whether it was generated, human-authored, templated, or adjudicated;
- what decision, record, or event it describes;
- whether it is final, draft, provisional, or under review;
- whether material uncertainty remains;
- whether dissent or unresolved witness divergence exists;
- whether the surface includes inference rather than direct fact;
- who or what approved publication;
- how the surface may be challenged;
- what deadline applies to challenge or appeal;
- where a fuller record may be accessed when appropriate.

For high-impact decisions, missing challenge or appeal instructions SHOULD be treated as a material defect.

---

## 11. Surface Defect Types

A CDP implementation SHOULD classify surface defects.

| Defect | Meaning | Typical response |
|---|---|---|
| `ungrounded_claim` | Claim lacks sufficient support. | Revise, ground, caveat, or remove. |
| `false_certainty` | Surface presents uncertainty as settled fact. | Add caveat or adjudicate. |
| `authority_laundering` | Generated or inferred wording appears institutionally approved without approval. | Block, review, or relabel. |
| `material_omission` | Important context is missing. | Revise or challenge. |
| `misleading_simplification` | Surface is simpler than truth permits. | Revise for fidelity. |
| `hidden_divergence` | Witness disagreement or dissent is suppressed. | Disclose or adjudicate. |
| `stale_context` | Surface relies on outdated policy, authority, evidence, or identity. | Regenerate or repair. |
| `harmful_category` | Surface uses inaccurate, stigmatizing, obsolete, or harmful classification. | Repair and update schema. |
| `missing_challenge_path` | Audience lacks contestability instructions. | Add challenge path before publication. |
| `audience_mismatch` | Surface cannot be understood by intended readers. | Rewrite and retest. |
| `record_surface_mismatch` | Surface conflicts with canonical record. | Block and adjudicate. |

---

## 12. Challenge Triggers

A CDP implementation SHOULD create a challenge candidate when:

- a surface claim conflicts with a canonical record;
- a surface omits material witness testimony;
- a surface hides unresolved synoptic divergence;
- a surface implies a decision is final when it is not;
- a surface describes a recommendation as a command;
- a surface presents inference as fact;
- a surface uses stale authority, stale policy, or stale identity data;
- a surface lacks required appeal or challenge instructions;
- an affected party contests the meaning of the surface;
- a reviewer identifies surface drift under RFC-CDP-061;
- a witness record under RFC-CDP-062 does not support the surface;
- the surface owner cannot identify what record the surface is based on.

A challenged surface SHOULD receive a status such as `challenged`, `adjudication_required`, `superseded`, or `retracted` depending on severity.

---

## 13. Adjudication Requirements

When a surface dispute requires adjudication, adjudication SHOULD determine:

- which surface claims are accepted;
- which surface claims are rejected;
- which claims require caveats;
- which claims require additional evidence;
- which witness records support or contradict the surface;
- whether the surface may remain published;
- whether the surface must be corrected;
- whether the surface must be retracted;
- whether affected parties must be notified;
- whether repair is required;
- whether schemas, prompts, templates, policies, or controls must change.

Adjudication MUST preserve material dissent and unresolved uncertainty where relevant to future review.

---

## 14. Publication and Versioning

A published Human-Readable Surface SHOULD be versioned.

A surface version SHOULD include:

- surface identifier;
- version number;
- publication timestamp;
- source record identifiers;
- source Witness Record identifiers;
- adjudication identifiers;
- surface owner;
- approval status;
- content hash;
- supersession relationship;
- retraction relationship where applicable.

If a surface is materially corrected after publication, CDP SHOULD preserve both the prior version and the corrected version, unless law, safety, or privacy requires a different retention approach.

Silent correction SHOULD be avoided for high-impact surfaces.

---

## 15. Retraction and Repair

A Human-Readable Surface SHOULD be retracted or repaired when it materially misleads, harms, misclassifies, erases, or falsely authorizes.

Retraction or repair SHOULD record:

- original surface identifier;
- defect type;
- reason for correction;
- affected audience;
- corrected surface;
- notification requirements;
- repair obligations;
- learning actions.

Repair MAY include:

- corrected notice;
- apology or acknowledgement;
- restored appeal window;
- re-opened review;
- policy correction;
- schema correction;
- prompt correction;
- template correction;
- affected-party review;
- audit escalation.

---

## 16. Record Requirements

A CDP implementation SHOULD record:

- surface artifact;
- surface metadata;
- source canonical records;
- source Witness Records;
- claim bindings;
- integrity review results;
- approval records;
- publication records;
- challenge records;
- adjudication records;
- correction records;
- retraction records;
- repair records;
- learning closure.

The record MUST preserve enough information for a future reviewer to determine what humans were shown, what the surface meant, what it was based on, who approved it, whether it was challenged, and whether it was repaired.

---

## 17. Learning Closure

Surface Integrity Review SHOULD feed the Learn Protocol when:

- similar surfaces repeatedly create confusion;
- model-generated surfaces repeatedly overstate certainty;
- templates omit required challenge rights;
- explanations repeatedly fail affected-party review;
- surface drift occurs after policy change;
- witness testimony is repeatedly flattened or erased;
- dashboards produce misleading operational conclusions;
- generated summaries fail to preserve caveats;
- users rely on surfaces in ways the surface did not support.

Learning closure MAY require:

- surface template revision;
- prompt revision;
- witness protocol revision;
- schema revision;
- UI redesign;
- publication gating;
- reviewer training;
- affected-party testing;
- policy clarification;
- automated surface-drift detection.

---

## 18. Security and Safety Considerations

### 18.1 Explanation Laundering

Generated explanations may make unsupported decisions appear legitimate.

CDP MUST distinguish fluent explanation from governed legitimacy.

### 18.2 Surface Capture

A surface may become the practical truth of a system because humans see it more often than the canonical record.

CDP SHOULD treat high-reliance surfaces as governance-critical artifacts.

### 18.3 Harmful Simplification

Plain language is necessary, but simplification can erase material caveats, rights, dissent, history, or affected-party context.

CDP SHOULD prefer understandable fidelity over comforting oversimplification.

### 18.4 Hidden Dissent

A surface that hides material disagreement may falsely imply consensus.

Where unresolved dissent matters, the surface SHOULD disclose it or defer publication.

### 18.5 Privacy and Disclosure Balance

Surface integrity does not require exposing all sensitive information.

A surface may preserve integrity by stating that certain evidence exists but cannot be disclosed, provided the limitation itself is recorded and challengeable.

### 18.6 Accessibility

A human-readable surface is not human-readable if the intended audience cannot access or understand it.

CDP SHOULD consider language, disability access, reading level, cultural context, legal context, and user interface constraints.

---

## 19. Implementation Notes

A simple implementation MAY begin with:

1. one generated or drafted explanation;
2. one PDF or durable surface artifact;
3. one surface metadata record;
4. one source-record binding;
5. one claim-to-record mapping;
6. one review checkbox for uncertainty, authority, appeal, and caveats;
7. one challenge path;
8. one version record.

A mature implementation MAY include:

- automated surface claim extraction;
- sentence-level source binding;
- witness-to-surface comparison;
- surface drift detection;
- affected-party comprehension testing;
- accessibility checks;
- mandatory challenge-path validation;
- publication gating;
- cryptographic hashes for published surfaces;
- immutable retention for high-impact surfaces;
- surface repair workflows.

---

## 20. Non-Goals

This RFC does not require:

- publishing all internal evidence to all audiences;
- making every surface exhaustive;
- eliminating summarization;
- forbidding AI-generated explanations;
- treating surface text as the canonical record;
- replacing legal, policy, or human judgment;
- exposing private witness testimony where disclosure would be unlawful or unsafe.

This protocol governs the integrity of human-facing meaning. It does not replace the canonical record, Witness Records, adjudication, appeal, repair, or institutional responsibility.

---

## 21. Summary

CDP decisions do not reach humans as JSON.

They reach humans as explanations, notices, dashboards, reports, messages, recommendations, and narratives.

Those surfaces shape what humans believe, contest, accept, appeal, fear, trust, or obey.

Therefore human-readable surfaces are governance-critical artifacts.

The Human-Readable Surface Integrity Protocol requires CDP systems to bind surfaces to records, preserve witness testimony, extract material claims, disclose uncertainty, prevent authority laundering, support challenge, record publication, repair defects, and learn from surface drift.

The canonical record says what was recorded.

The Witness Records say what it appears to mean.

The Human-Readable Surface says what a human is being shown.

Surface Integrity ensures those three do not drift apart in silence.
