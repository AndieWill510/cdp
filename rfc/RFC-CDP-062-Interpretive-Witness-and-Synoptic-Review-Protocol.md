# RFC-CDP-062 — Interpretive Witness and Synoptic Review Protocol

Author: Kevin “Andie” Williams / AIITL contribution  
Status: Draft v0.2  
Series: Constitutional Decision Plane (CDP)  
Date: May 15, 2026  
Depends On: RFC-CDP-001, RFC-CDP-010, RFC-CDP-020, RFC-CDP-021, RFC-CDP-040, RFC-CDP-042, RFC-CDP-044, RFC-CDP-045, RFC-CDP-047, RFC-CDP-048, RFC-CDP-060, RFC-CDP-061  
Updates: RFC-CDP-021, RFC-CDP-047, RFC-CDP-060, RFC-CDP-061

---

## Abstract

This RFC defines the **Interpretive Witness and Synoptic Review Protocol** for the Constitutional Decision Plane (CDP).

CDP distinguishes between a canonical machine-readable record and a human-readable interpretation of that record. A JSON object, envelope, policy packet, decision object, or event record may be syntactically valid while still being misunderstood, mistranslated, selectively summarized, or rendered illegible to affected humans.

This RFC introduces **Interpretive Witnesses**: independent human, AI, institutional, or tool-based interpretations of a canonical record. It further defines **Synoptic Review**: the governed comparison of multiple witness records to detect agreement, contradiction, omission, unsupported inference, semantic drift, and human-readable surface risk.

The purpose of this protocol is to prevent the human-readable layer from becoming an ungoverned translation of machine state. CDP treats human-readable meaning as a governed, multi-witness artifact rather than a direct rendering of machine-readable state.

A Witness Record MUST preserve testimony in a durable human-readable form, PDF or equivalent by default. Machine-readable metadata may index, route, hash, compare, and ground the witness, but it MUST NOT replace the witness testimony itself.

---

## 1. Purpose

This RFC answers:

- how a CDP system should generate human-readable interpretations of canonical records;
- why a single AI-generated explanation is insufficient for high-impact decisions;
- how multiple independent witnesses can reveal semantic drift;
- how witness claims should be grounded in canonical record fields;
- how omissions, contradictions, and unsupported inferences become challengeable;
- how synoptic review supports legitimacy before publication, execution, notice, or enforcement;
- how CDP should preserve the difference between record, interpretation, adjudication, and legitimated surface;
- why witness testimony must remain human-readable and must not be collapsed into JSON alone.

---

## 2. Core Principle

A valid record is not necessarily an adequate witness.

A canonical record may preserve what the machine received, decided, emitted, or enforced. That does not mean the record has been faithfully interpreted for humans, affected parties, reviewers, auditors, courts, regulators, or communities.

CDP MUST therefore distinguish:

- canonical record from interpretive witness;
- record validity from interpretive adequacy;
- explanation from adjudicated meaning;
- summary from testimony;
- inference from fact;
- omission from irrelevance;
- agreement from legitimacy;
- human-readable surface from approved institutional position;
- machine-readable control metadata from witness testimony.

The witness must remain readable as witness.

CDP MUST preserve testimony in the form required for human review, not merely in the form preferred by machine control.

---

## 3. Relationship to Existing RFCs

### 3.1 RFC-CDP-020 Decision Object Schema

The Decision Object stores the canonical decision state, authority, evidence, lifecycle status, linked artifacts, and metadata.

This RFC defines how independent witnesses interpret that object and how claims about its meaning are traced back to canonical fields.

### 3.2 RFC-CDP-021 Envelope Schema

The Envelope carries message context, actor, authority, lineage, attestation, payload type, and integrity material.

This RFC extends the envelope model by requiring human-readable surfaces to preserve traceable correspondence to the canonical record and to disclose when interpretation is model-generated, human-authored, adjudicated, contested, or incomplete.

### 3.3 RFC-CDP-042 Challenge Protocol

Witness divergence, unsupported inference, material omission, or misleading simplification SHOULD create a challenge candidate.

### 3.4 RFC-CDP-044 Adjudicate Protocol

Synoptic Review produces comparison findings that MAY require adjudication before a human-readable surface is approved.

### 3.5 RFC-CDP-045 Legitimize Protocol

A human-readable surface SHOULD NOT be legitimated merely because one witness produced a plausible explanation. Legitimation requires governed correspondence between canonical record, interpretive claims, and adjudicated meaning.

### 3.6 RFC-CDP-047 Record Protocol

Witness records, comparison findings, challenges, adjudications, and final surfaces SHOULD be recorded as governed artifacts.

### 3.7 RFC-CDP-060 Covenant Protocol and AIITL

AIITL may serve as witness, challenger, translator, summarizer, contradiction detector, and schema-drift detector.

This RFC specifies how AIITL witness roles are bounded, compared, and prevented from becoming unreviewed authority.

### 3.8 RFC-CDP-061 Schema Drift and Context Preservation

This RFC provides one mechanism for detecting schema drift between canonical machine-readable records and human-readable meaning.

Where interpretations diverge materially, CDP SHOULD treat the divergence as a schema-drift signal until reviewed.

---

## 4. Terminology

### 4.1 Canonical Record

A **Canonical Record** is the machine-readable artifact treated as the authoritative record of a decision, event, policy, envelope, execution request, challenge, adjudication, or other governed act.

A canonical record may be represented as JSON, YAML, database rows, event messages, signed envelopes, policy objects, or other structured artifacts.

### 4.2 Interpretive Witness

An **Interpretive Witness** is an independent account of what a Canonical Record appears to mean.

A witness may be produced by:

- an AI model;
- a human reviewer;
- a policy subject-matter expert;
- a rule engine;
- a static analyzer;
- a legal reviewer;
- an affected-party representative;
- an institutional actor;
- a domain-specific interpreter.

An Interpretive Witness is not automatically authoritative.

### 4.3 Witness Record

A **Witness Record** is the durable artifact produced by an Interpretive Witness.

A Witness Record MUST preserve the witness testimony as a first-class human-readable artifact.

A Witness Record MUST NOT consist only of JSON, YAML, database rows, vectors, embeddings, or other machine-readable structures.

A Witness Record SHOULD be stored as PDF by default, or an equivalent durable human-readable format such as:

- PDF/A;
- signed PDF;
- signed HTML rendered to PDF;
- Markdown with a rendered PDF artifact;
- DOCX with a rendered PDF artifact;
- other immutable or versioned human-readable format approved by the implementation profile.

Machine-readable metadata MAY accompany the Witness Record, but only as a control, routing, indexing, grounding, hashing, comparison, or audit layer.

JSON can point to testimony.

JSON can route testimony.

JSON can index testimony.

JSON can ground testimony.

JSON must not replace testimony.

### 4.4 Witness Testimony

**Witness Testimony** is the human-readable account of what the witness saw, understood, inferred, doubted, omitted, refused to conclude, or would challenge.

Witness Testimony SHOULD include:

- what the witness believes the Canonical Record means;
- what the witness is confident about;
- what the witness is uncertain about;
- what the witness believes is missing;
- what the witness believes may be misleading;
- what the witness would challenge;
- what the witness refuses to conclude;
- what context the witness did or did not have.

### 4.5 Interpretive Claim

An **Interpretive Claim** is a discrete assertion about what the Canonical Record means.

Each claim SHOULD be separable, reviewable, and traceable.

Example:

```text
The decision was approved because the proposer had delegated authority under policy version 2026.05.
```

### 4.6 Grounding

**Grounding** is the trace from an Interpretive Claim to one or more elements of the Canonical Record, policy basis, evidence artifact, prior adjudication, or recorded context snapshot.

Ungrounded claims MUST be marked as inference, hypothesis, interpretation, or unsupported.

### 4.7 Grounding Map

A **Grounding Map** is the structured or semi-structured artifact that links claims in the Witness Testimony to canonical fields, policy artifacts, evidence records, context snapshots, caveats, or adjudication records.

The Grounding Map MAY be machine-readable.

The Witness Testimony MUST remain human-readable.

### 4.8 Synoptic Review

**Synoptic Review** is the governed comparison of multiple Witness Records over the same Canonical Record.

Synoptic Review asks what the witnesses share, where they diverge, what each omits, and where the record itself may be insufficient to support legitimate interpretation.

### 4.9 Divergence

A **Divergence** is a material difference between Witness Records.

Divergence may involve contradiction, emphasis, scope, omission, risk framing, authority interpretation, affected-party meaning, legal meaning, or operational implication.

### 4.10 Omission

An **Omission** is a missing claim, caveat, risk, authority condition, affected-party impact, uncertainty, or contextual element that is material to interpretation.

### 4.11 Unsupported Inference

An **Unsupported Inference** is a claim that goes beyond the Canonical Record and available context without adequate grounding.

Unsupported inference may be useful, but it MUST NOT be presented as fact.

### 4.12 Human-Readable Surface

A **Human-Readable Surface** is any explanation, notice, summary, report, dashboard, recommendation, rationale, email, interface text, or narrative rendering intended for human use.

### 4.13 Legitimated Surface

A **Legitimated Surface** is a Human-Readable Surface that has passed required review, challenge, adjudication, approval, or publication controls.

---

## 5. Protocol Overview

The Interpretive Witness and Synoptic Review Protocol follows this sequence:

```text
Canonical Record
  → Witness Assignment
  → Independent Interpretation
  → Witness Record Creation
  → Claim Extraction
  → Grounding Check
  → Synoptic Comparison
  → Divergence Classification
  → Challenge / Adjudication
  → Legitimated Surface
  → Record / Learn
```

A CDP implementation MAY simplify this flow for low-impact decisions.

For high-impact, rights-affecting, safety-sensitive, identity-sensitive, repair-sensitive, or enforcement-related decisions, a CDP implementation SHOULD require more than one independent Interpretive Witness before approving a Human-Readable Surface.

---

## 6. Witness Assignment

A CDP implementation SHOULD assign witnesses according to decision risk, decision type, policy domain, authority scope, and affected-party impact.

### 6.1 Minimum Witness Classes

For high-impact decisions, Synoptic Review SHOULD include at least two materially distinct witness classes.

Examples:

```text
AI model witness + human policy reviewer
AI model witness + rule engine
AI model A + AI model B + human adjudicator
policy SME + affected-party representative + AI summarizer
```

### 6.2 Independence Requirement

Witnesses SHOULD be independent enough that their agreement provides evidence rather than mere duplication.

Independence may involve:

- different model families;
- different prompts;
- different roles;
- different institutional positions;
- different data access scopes;
- different review duties;
- different interpretive frames.

Two witnesses using the same model, same prompt, same context, and same hidden assumptions SHOULD NOT be treated as independent.

### 6.3 Context Disclosure

Each witness MUST disclose, or have recorded on its behalf, what context it had access to.

A witness that saw only the Canonical Record must not be treated the same as a witness that also saw policy history, prior challenges, affected-party testimony, or adjudication records.

---

## 7. Witness Record Requirements

A Witness Record MUST preserve both:

1. durable human-readable testimony; and  
2. machine-readable control metadata.

The durable human-readable testimony is the primary witness artifact.

The machine-readable metadata is secondary. It exists to support routing, indexing, comparison, challenge, grounding, hashing, audit, retention, and replay.

### 7.1 Required Human-Readable Artifact

The Witness Record MUST include a human-readable artifact.

The preferred format is PDF or PDF/A.

An implementation MAY use Markdown, HTML, DOCX, or another editable authoring format, but SHOULD render or preserve a PDF-equivalent artifact for durable review, audit, and exchange.

The human-readable artifact SHOULD include:

- witness identity or class;
- input scope;
- available context;
- excluded or unavailable context;
- testimony;
- claims;
- caveats;
- uncertainties;
- omissions;
- dissent or minority reading;
- refusal to conclude;
- challenge recommendations;
- timestamp;
- version information.

### 7.2 Machine-Readable Control Metadata

Machine-readable control metadata MAY be represented in JSON, YAML, database rows, event metadata, or envelope fields.

Example:

```json
{
  "witness_record_id": "wit_20260515_001",
  "canonical_record_id": "dec_20260515_001",
  "witness_type": "ai_model",
  "witness_role": "interpretive_witness",
  "testimony_artifact_ref": "artifact://witness-testimony/wit_20260515_001.pdf",
  "authoring_artifact_ref": "artifact://witness-testimony/wit_20260515_001.md",
  "claim_register_ref": "artifact://claim-register/wit_20260515_001.json",
  "grounding_map_ref": "artifact://grounding-map/wit_20260515_001.json",
  "content_hash": "sha256:example",
  "status": "draft",
  "created_at": "2026-05-15T00:00:00Z"
}
```

This JSON is not the Witness Record.

It is the control metadata for the Witness Record.

### 7.3 Claim Register

A Witness Record MAY include a machine-readable Claim Register to support comparison and grounding.

The Claim Register MUST NOT replace the testimony.

Each claim SHOULD distinguish:

- fact;
- interpretation;
- inference;
- hypothesis;
- recommendation;
- caveat;
- dissent;
- unresolved question.

### 7.4 Grounding Map

The Grounding Map SHOULD link claims in the testimony to the Canonical Record, policy basis, evidence artifacts, adjudications, or context snapshots.

Example:

```json
{
  "claim_id": "clm_001",
  "claim_text_ref": "page=2;paragraph=4",
  "claim_type": "authority_interpretation",
  "grounding": [
    {
      "artifact_id": "dec_20260515_001",
      "path": "$.authority.delegation_basis",
      "support_type": "direct"
    }
  ],
  "confidence": "medium",
  "classification": "interpretation",
  "caveats": [
    "Delegation expiry was not visible to this witness."
  ]
}
```

The Grounding Map may be structured.

The testimony must remain readable.

---

## 8. Synoptic Comparison

Synoptic Review SHOULD compare Witness Records across at least the following dimensions:

| Dimension | Question |
|---|---|
| Agreement | What claims do witnesses materially share? |
| Contradiction | What claims cannot both be true? |
| Omission | What did one witness notice that another missed? |
| Unsupported inference | What claims exceed the record? |
| Authority interpretation | Do witnesses agree about who had authority? |
| Policy interpretation | Do witnesses agree about applicable policy? |
| Affected-party impact | Do witnesses preserve the human consequence? |
| Risk framing | Do witnesses describe risk similarly? |
| Remedy or action | Do witnesses agree about what should happen next? |
| Adequacy of record | Is the Canonical Record sufficient to support interpretation? |
| Testimony quality | Does the witness remain readable, reviewable, and contestable? |

---

## 9. Divergence Classification

Divergence SHOULD be classified by severity.

| Severity | Meaning | Default behavior |
|---|---|---|
| `none` | No material divergence detected. | Continue. |
| `stylistic` | Difference in wording or emphasis only. | Record if useful. |
| `minor` | Difference may affect interpretation but not authority, rights, safety, or legitimacy. | Record and optionally review. |
| `material` | Difference may affect meaning, authority, fairness, policy, or outcome. | Challenge or adjudicate. |
| `blocking` | Difference makes publication, execution, notice, or enforcement unsafe or misleading. | Block pending adjudication. |
| `record_insufficient` | Witnesses reveal that the Canonical Record cannot support legitimate interpretation. | Return to Record, Challenge, or Propose. |
| `testimony_insufficient` | Witness output is too structured, opaque, terse, or machine-oriented for human review. | Require new Witness Record. |

A blocking divergence MUST NOT be resolved by choosing the most fluent witness.

A testimony-insufficient divergence MUST NOT be resolved by relying on JSON metadata alone.

---

## 10. Human-Readable Surface Integrity

A Human-Readable Surface SHOULD NOT present itself as a neutral rendering of machine state when it is actually an interpretation.

A Human-Readable Surface SHOULD disclose, as appropriate:

- whether it is generated, human-authored, or adjudicated;
- what record it interprets;
- what Witness Records contributed to it;
- what material assumptions it relies on;
- what uncertainties remain;
- what claims are grounded directly;
- what claims are inferred;
- whether any witness divergence remains unresolved;
- who approved the final surface;
- how to challenge the surface.

For high-impact decisions, a Human-Readable Surface SHOULD be traceable from each material sentence or claim back to the Canonical Record, evidence artifact, policy basis, adjudication, context snapshot, or Witness Record.

---

## 11. Challenge Triggers

A CDP implementation SHOULD create a challenge candidate when:

- witnesses materially disagree;
- a witness identifies a missing field needed for interpretation;
- a witness identifies expired, ambiguous, or contested authority;
- a witness makes a high-confidence claim with weak grounding;
- a witness omits affected-party impact in a rights-affecting decision;
- a witness summarizes contested testimony as settled fact;
- a human-readable surface hides material uncertainty;
- all witnesses agree but the Canonical Record appears inadequate;
- a witness detects schema drift under RFC-CDP-061;
- a witness identifies a repair, appeal, or sovereignty-sensitive issue;
- a witness output is only JSON, YAML, vectors, embeddings, or database records without durable testimony;
- a witness testimony cannot be understood, reviewed, or challenged by the intended human reviewers.

---

## 12. Adjudication Requirements

When Synoptic Review produces material, blocking, record-insufficient, or testimony-insufficient divergence, adjudication SHOULD determine:

- which claims are accepted;
- which claims are rejected;
- which claims remain unresolved;
- which claims require additional evidence;
- which omissions are material;
- whether the Canonical Record must be amended;
- whether a Witness Record must be regenerated;
- whether the Human-Readable Surface may be published;
- whether execution must be deferred;
- whether repair, appeal, or affected-party review is required.

Adjudication MUST preserve dissent where dissent remains material to future review.

---

## 13. Record Requirements

A CDP implementation SHOULD record:

- Canonical Record identifier;
- witness assignments;
- Witness Records;
- testimony artifacts;
- control metadata;
- claim registers;
- grounding maps;
- synoptic comparison results;
- divergence classifications;
- challenge records;
- adjudication decisions;
- approved Human-Readable Surface;
- unresolved caveats;
- learning actions.

The record MUST preserve enough context for a future reviewer to determine whether the human-readable surface faithfully represented the canonical record and the adjudicated meaning.

The record MUST preserve enough human-readable testimony for a future reviewer to understand what each witness actually said.

---

## 14. Learning Closure

Synoptic Review SHOULD feed the Learn Protocol when:

- witnesses repeatedly disagree on the same field or policy pattern;
- human-readable surfaces repeatedly omit the same context;
- model witnesses hallucinate or over-infer recurring claims;
- canonical records lack fields needed for legitimate interpretation;
- affected parties successfully challenge published surfaces;
- policy changes create recurring interpretive ambiguity;
- schema drift is detected after publication or enforcement;
- witness outputs are repeatedly too structured or opaque for human review.

Learning closure MAY require:

- schema revision;
- envelope revision;
- prompt revision;
- witness-role revision;
- witness-output format revision;
- review threshold revision;
- policy clarification;
- interface redesign;
- additional affected-party review;
- repair action.

---

## 15. Security and Safety Considerations

### 15.1 Model Collusion and Correlated Error

Multiple AI witnesses do not guarantee independence. Shared training data, shared prompts, shared retrieved context, or shared institutional assumptions may produce correlated error.

CDP implementations SHOULD treat model diversity as useful but insufficient.

### 15.2 Fluency Bias

A fluent explanation may be wrong. A less polished witness may preserve a material caveat that a fluent witness omits.

Synoptic Review MUST NOT resolve divergence by rhetorical quality alone.

### 15.3 Authority Laundering

A Human-Readable Surface may accidentally launder unsupported model interpretation into institutional authority.

CDP MUST distinguish generated interpretation from approved position.

### 15.4 JSON Recursion Risk

If a Witness Record is reduced to JSON alone, CDP recreates the same schema-drift risk one layer higher.

The system may falsely believe it has created human-readable testimony when it has merely created another machine-readable object requiring interpretation.

CDP MUST prevent witness testimony from being collapsed into control metadata.

### 15.5 Privacy and Context Minimization

Witnesses SHOULD receive enough context to interpret the record but not unnecessary sensitive data.

Where context is withheld for privacy, the withholding SHOULD be recorded as a limitation.

### 15.6 Affected-Party Harm

A technically accurate surface may still be misleading, stigmatizing, decontextualized, or harmful.

For rights-affecting or repair-sensitive decisions, witness review SHOULD include affected-party meaning and human consequence.

---

## 16. Implementation Notes

A simple implementation MAY begin with:

1. one canonical JSON record;
2. two AI witness prompts using different models or roles;
3. one PDF witness testimony artifact per witness;
4. one machine-readable metadata file per witness;
5. one claim-extraction step;
6. one comparison table;
7. one human adjudication checkpoint;
8. one approved explanation stored with trace links.

A mature implementation MAY include:

- structured Witness Record metadata;
- durable PDF/A witness testimony;
- model diversity policies;
- automated claim-grounding checks;
- contradiction detection;
- affected-party review workflows;
- adjudication queues;
- sentence-level provenance in human-readable surfaces;
- dashboards for recurring interpretive drift;
- cryptographic hashes for witness artifacts;
- immutable storage for high-impact witness records.

---

## 17. Non-Goals

This RFC does not require:

- treating AI systems as persons;
- granting AI systems final authority;
- using a fixed number of models;
- averaging model outputs;
- replacing human judgment;
- exposing all private context to all witnesses;
- publishing every witness record to every audience;
- eliminating structured metadata;
- forbidding JSON as metadata, index, grounding, or routing material.

This protocol governs interpretation. It does not eliminate the need for authority, judgment, consent, challenge, repair, or accountability.

---

## 18. Summary

CDP cannot treat human-readable meaning as an automatic byproduct of valid JSON.

The machine-readable record and the human-readable surface can drift apart. That drift may create misunderstanding, false legitimacy, hidden policy change, affected-party harm, or institutional self-deception.

The Interpretive Witness and Synoptic Review Protocol makes interpretation governed.

It requires CDP systems to compare independent witness records, ground claims, surface omissions, classify divergence, adjudicate material differences, preserve dissent, and legitimate only those human-readable surfaces the institution is willing to stand behind.

The canonical record says what was recorded.

The witnesses say what it appears to mean.

The Witness Record preserves that testimony in durable human-readable form.

Synoptic review shows where meaning is stable, contested, missing, or unsafe.

Legitimation says what CDP is prepared to stand behind.

That is how CDP reduces schema drift between machine truth, human meaning, institutional authority, and real-world consequence.
