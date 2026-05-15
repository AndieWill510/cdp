# RFC-CDP-065 — Semantic Layer and Meta-Review Protocol

Author: Kevin “Andie” Williams / AIITL contribution  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: May 15, 2026  
Depends On: RFC-CDP-001, RFC-CDP-010, RFC-CDP-020, RFC-CDP-021, RFC-CDP-042, RFC-CDP-044, RFC-CDP-045, RFC-CDP-047, RFC-CDP-048, RFC-CDP-060, RFC-CDP-061, RFC-CDP-062, RFC-CDP-063, RFC-CDP-064  
Updates: RFC-CDP-045, RFC-CDP-047, RFC-CDP-061, RFC-CDP-062, RFC-CDP-063, RFC-CDP-064

---

## Abstract

This RFC defines the **Semantic Layer and Meta-Review Protocol** for the Constitutional Decision Plane (CDP).

RFC-CDP-062 defines Interpretive Witnesses and Synoptic Review over Canonical Records. RFC-CDP-063 governs Human-Readable Surfaces. RFC-CDP-064 determines whether Canonical Records are adequate for downstream interpretation.

This RFC defines a higher-order layer: governed semantic synthesis across multiple Canonical Records, Witness Records, Synoptic Reviews, Human-Readable Surfaces, Adequacy Reviews, challenges, adjudications, outcomes, and repairs.

The Semantic Layer does not act as another primary witness. It interprets the witness corpus.

The core principle is:

> A semantic layer interprets the witness corpus; it does not overwrite the witness record.

Semantic synthesis may reveal patterns, meaning, risk, doctrine, learning, policy implications, and institutional drift that no single record or witness can show alone. But semantic synthesis can also launder later interpretation into original fact, erase dissent, flatten witness testimony, or convert institutional preference into apparent truth.

This protocol defines Meta-Witnesses, Synthesis Claims, Corpus Adequacy, Semantic Drift, semantic provenance, challenge triggers, adjudication requirements, and learning closure for higher-order meaning-making.

---

## 1. Purpose

This RFC answers:

- how CDP governs meaning-making across multiple records and witnesses;
- how semantic synthesis differs from primary witness testimony;
- how meta-review differs from synoptic review;
- how synthesis claims are grounded in a witness corpus;
- how later interpretation preserves rather than colonizes earlier testimony;
- how semantic drift is detected and challenged;
- how corpus adequacy is evaluated before synthesis;
- how semantic conclusions become legitimate, caveated, contested, or rejected;
- how CDP learns from patterns across decisions, surfaces, challenges, outcomes, and repairs.

---

## 2. Core Principle

Meaning may emerge after witness, but it must not colonize witness.

CDP MUST distinguish:

- Canonical Record from Witness Record;
- Witness Record from Synoptic Review;
- Synoptic Review from Human-Readable Surface;
- Human-Readable Surface from Semantic Synthesis;
- semantic synthesis from adjudicated fact;
- later interpretation from primary testimony;
- pattern recognition from proof;
- doctrine from evidence;
- corpus-level meaning from individual consequence;
- institutional learning from institutional self-justification.

A synthesis may interpret a witness corpus.

A synthesis MUST NOT silently rewrite what the witnesses said.

---

## 3. Relationship to Existing RFCs

### 3.1 RFC-CDP-020 Decision Object Schema

Decision Objects preserve canonical decision state, authority, evidence, lifecycle status, and linked artifacts.

This RFC defines how patterns across multiple Decision Objects may be synthesized without replacing any single decision record.

### 3.2 RFC-CDP-021 Envelope Schema

Envelopes carry message context, actor, authority, lineage, attestation, payload type, and integrity material.

This RFC defines semantic provenance requirements for synthesis artifacts that reference multiple envelopes or record lineages.

### 3.3 RFC-CDP-042 Challenge Protocol

Semantic synthesis SHOULD be challengeable when it misreads the corpus, overstates meaning, erases dissent, or relies on inadequate records.

### 3.4 RFC-CDP-044 Adjudicate Protocol

Adjudication MAY be required when synthesis claims materially affect legitimacy, policy, execution, repair, or institutional learning.

### 3.5 RFC-CDP-045 Legitimize Protocol

Semantic synthesis SHOULD NOT be legitimated merely because it is persuasive, elegant, statistically suggestive, or institutionally useful.

Legitimation requires governed grounding in the corpus and preservation of dissent, caveats, uncertainty, and scope.

### 3.6 RFC-CDP-047 Record Protocol

Semantic synthesis, meta-review artifacts, corpus definitions, synthesis claims, challenges, adjudications, and learning actions SHOULD be recorded as governed artifacts.

### 3.7 RFC-CDP-061 Schema Drift and Context Preservation

Semantic Drift is a higher-order form of schema drift: later synthesis changes the practical meaning of earlier records without preserving provenance, caveat, dissent, or scope.

### 3.8 RFC-CDP-062 Interpretive Witness and Synoptic Review Protocol

RFC-CDP-062 governs primary witness testimony and comparison across witnesses.

This RFC governs interpretation across a witness corpus.

### 3.9 RFC-CDP-063 Human-Readable Surface Integrity Protocol

Semantic synthesis often becomes visible through surfaces such as reports, policy memos, dashboards, audits, briefings, public statements, and doctrine.

This RFC defines how those synthesis surfaces remain bound to their corpus.

### 3.10 RFC-CDP-064 Canonical Record Adequacy Protocol

Synthesis depends on corpus adequacy.

A synthesis SHOULD NOT proceed as authoritative when the underlying record and witness corpus is inadequate for the claims being made.

---

## 4. Terminology

### 4.1 Semantic Layer

A **Semantic Layer** is a governed interpretive layer that synthesizes meaning across a corpus of CDP artifacts.

The Semantic Layer may consider:

- Canonical Records;
- Decision Objects;
- Envelopes;
- Witness Records;
- Synoptic Reviews;
- Human-Readable Surfaces;
- Adequacy Reviews;
- Challenge Records;
- Adjudications;
- Execution outcomes;
- Appeal records;
- Repair records;
- Learning records;
- policy changes;
- context snapshots.

### 4.2 Meta-Review

**Meta-Review** is the governed act of reviewing and synthesizing meaning across a corpus rather than interpreting a single Canonical Record.

Meta-Review asks:

- What patterns emerge?
- What meaning is stable?
- What meaning is contested?
- What is repeatedly omitted?
- What changes over time?
- What later evidence changes interpretation?
- What doctrine or policy may need revision?
- What harms or risks recur?
- What cannot be concluded from the corpus?

### 4.3 Meta-Witness

A **Meta-Witness** is a human, AI system, review team, analytic tool, subject-matter expert, affected-party representative, auditor, or institutional process that produces a synthesis over a witness or record corpus.

A Meta-Witness is not a primary witness.

A Meta-Witness interprets what the witness corpus appears to mean.

### 4.4 Witness Corpus

A **Witness Corpus** is the defined set of Witness Records, Canonical Records, surfaces, reviews, outcomes, and related artifacts considered by a Meta-Review.

The corpus MUST be defined or discoverable.

A synthesis without a defined corpus is not reviewable.

### 4.5 Corpus Adequacy

**Corpus Adequacy** is the condition in which the witness or record corpus is sufficient to support the synthesis claims being made.

A corpus may be adequate for exploratory interpretation but inadequate for policy change, public reporting, execution rules, legal conclusion, or repair closure.

### 4.6 Synthesis Claim

A **Synthesis Claim** is a claim about meaning, pattern, trend, doctrine, risk, legitimacy, harm, evidence, omission, or institutional learning across a corpus.

Examples:

```text
Witnesses consistently identify authority ambiguity in this decision class.
```

```text
Human-readable denial notices repeatedly omit appeal timing.
```

```text
The record corpus is inadequate to support a conclusion that the policy is being applied consistently.
```

### 4.7 Semantic Provenance

**Semantic Provenance** is the trace from a Synthesis Claim to the corpus artifacts, witness testimony, surface records, challenges, adjudications, outcomes, and caveats that support or limit the claim.

### 4.8 Semantic Drift

**Semantic Drift** occurs when later synthesis changes, narrows, expands, sanitizes, theologizes, operationalizes, or institutionalizes the meaning of earlier records without preserving provenance, scope, uncertainty, dissent, or affected-party meaning.

### 4.9 Synthesis Surface

A **Synthesis Surface** is a human-readable output produced by Meta-Review.

Examples include:

- policy memo;
- audit report;
- executive briefing;
- model card;
- governance dashboard;
- trend report;
- doctrine note;
- public report;
- learning report;
- repair report;
- risk assessment;
- meta-analysis.

### 4.10 Semantic Status

**Semantic Status** indicates the review state of a synthesis artifact.

Recommended statuses include:

- `exploratory`;
- `draft`;
- `under_review`;
- `corpus_inadequate`;
- `contested`;
- `adjudication_required`;
- `approved`;
- `published`;
- `superseded`;
- `retracted`;
- `repaired`;
- `archived`.

---

## 5. Protocol Overview

The Semantic Layer and Meta-Review Protocol follows this sequence:

```text
Corpus Definition
  → Corpus Adequacy Review
  → Meta-Witness Assignment
  → Semantic Synthesis
  → Synthesis Claim Extraction
  → Semantic Provenance Mapping
  → Drift / Dissent / Caveat Review
  → Challenge / Adjudication
  → Synthesis Surface Publication
  → Record / Learn / Repair
```

A CDP implementation MAY use lightweight Meta-Review for low-impact internal learning.

For high-impact, policy-shaping, rights-affecting, public-facing, repair-sensitive, or execution-modifying synthesis, the full protocol SHOULD apply.

---

## 6. Corpus Definition Requirements

A Meta-Review MUST define the corpus it interprets.

Corpus definition SHOULD include:

- corpus identifier;
- purpose of review;
- inclusion criteria;
- exclusion criteria;
- time range;
- decision classes;
- policy scope;
- affected-party scope;
- record types included;
- witness types included;
- surface types included;
- challenge and adjudication records included;
- known gaps;
- known biases;
- corpus owner;
- review status.

A corpus definition MAY be machine-readable, but SHOULD be understandable to human reviewers.

A synthesis MUST NOT imply universality when the corpus is limited.

---

## 7. Corpus Adequacy Review

Before producing authoritative synthesis, CDP SHOULD review whether the corpus is adequate for the intended synthesis scope.

Corpus Adequacy Review SHOULD ask:

- Are enough relevant records included?
- Are key witness traditions missing?
- Are affected-party records included where required?
- Are challenge and adjudication records included?
- Are dissenting records included?
- Are outcome and repair records included?
- Are relevant time periods included?
- Are policy versions distinguishable?
- Are records adequate under RFC-CDP-064?
- Are surfaces adequate under RFC-CDP-063?
- Are Witness Records adequate under RFC-CDP-062?
- Are known omissions disclosed?
- Is the corpus sufficient for the strength of the claim?

A corpus may be sufficient for hypothesis generation but insufficient for policy conclusion.

A corpus may be sufficient for internal learning but insufficient for public reporting.

A corpus may be sufficient for pattern detection but insufficient for causal attribution.

---

## 8. Meta-Witness Assignment

A CDP implementation SHOULD assign Meta-Witnesses according to synthesis risk, domain, corpus type, policy impact, affected-party impact, and intended use.

Meta-Witnesses may include:

- AI models;
- human analysts;
- policy subject-matter experts;
- affected-party representatives;
- auditors;
- legal reviewers;
- statisticians;
- domain experts;
- cultural or community reviewers;
- governance boards;
- analytic tools.

High-impact synthesis SHOULD include more than one materially distinct Meta-Witness class.

A Meta-Witness MUST disclose, or have recorded on its behalf, what corpus it reviewed and what context it had access to.

---

## 9. Semantic Synthesis Requirements

Semantic Synthesis SHOULD distinguish:

- primary record facts;
- witness testimony;
- synoptic findings;
- adjudicated findings;
- surface claims;
- observed outcomes;
- repair claims;
- statistical patterns;
- interpretive patterns;
- hypotheses;
- recommendations;
- doctrine;
- uncertainty;
- dissent.

A synthesis MUST NOT present a later interpretive conclusion as if it were a primary record.

A synthesis MUST NOT erase witness divergence merely because an aggregate pattern is useful.

A synthesis SHOULD preserve minority readings when they materially affect legitimacy, policy, repair, or affected-party meaning.

---

## 10. Synthesis Claim Requirements

Each material Synthesis Claim SHOULD include:

- claim identifier;
- claim text;
- claim type;
- corpus scope;
- supporting artifacts;
- contradicting artifacts;
- caveats;
- uncertainty;
- affected-party implications where relevant;
- confidence or evidentiary strength;
- recommended status;
- review history.

Claim types MAY include:

- pattern claim;
- trend claim;
- omission claim;
- authority claim;
- policy claim;
- risk claim;
- legitimacy claim;
- repair claim;
- causal hypothesis;
- doctrinal synthesis;
- implementation recommendation;
- refusal to conclude.

---

## 11. Semantic Provenance Mapping

A Meta-Review SHOULD maintain semantic provenance for material Synthesis Claims.

Semantic provenance SHOULD trace claims to:

- Canonical Records;
- Witness Records;
- Synoptic Reviews;
- Surface Integrity records;
- Adequacy Reviews;
- Challenge Records;
- Adjudications;
- outcome records;
- appeal records;
- repair records;
- policy artifacts;
- context snapshots.

A Synthesis Claim without semantic provenance SHOULD be marked as exploratory, rhetorical, speculative, or unsupported.

---

## 12. Semantic Drift Detection

A CDP implementation SHOULD detect Semantic Drift when:

- synthesis rewrites witness testimony;
- synthesis hides dissent;
- synthesis presents later interpretation as original fact;
- synthesis overgeneralizes from a limited corpus;
- synthesis converts correlation into causation;
- synthesis treats institutional convenience as legitimacy;
- synthesis erases affected-party meaning;
- synthesis collapses repair claims into ordinary feedback;
- synthesis turns policy preference into evidence;
- synthesis uses stale context;
- synthesis ignores corpus inadequacy;
- synthesis becomes doctrine without adjudication.

Semantic Drift SHOULD become a challenge candidate when material.

---

## 13. Challenge Triggers

A CDP implementation SHOULD create a challenge candidate when:

- the corpus is undefined;
- the corpus is inadequate for the synthesis claim;
- material dissent is omitted;
- witness testimony is misrepresented;
- a synthesis claim lacks provenance;
- the synthesis overstates certainty;
- the synthesis overgeneralizes beyond scope;
- the synthesis conflicts with adjudicated findings;
- affected-party meaning is erased or flattened;
- repair-sensitive claims are treated as ordinary process feedback;
- later synthesis is presented as primary fact;
- a synthesis surface becomes policy without review;
- a Meta-Witness refuses to conclude due to corpus inadequacy.

---

## 14. Adjudication Requirements

When Semantic Synthesis is contested, adjudication SHOULD determine:

- what corpus was reviewed;
- whether the corpus is adequate;
- what synthesis claims are accepted;
- what synthesis claims are rejected;
- what claims remain exploratory;
- what claims require caveats;
- what dissent must be preserved;
- what witness testimony was misread or flattened;
- whether a synthesis surface may be published;
- whether a policy, schema, template, execution gate, or repair path may change based on the synthesis;
- whether affected parties must be notified;
- whether the synthesis must be corrected, retracted, or repaired.

Adjudication MUST preserve material dissent and uncertainty where future review may depend on it.

---

## 15. Synthesis Surface Requirements

A Synthesis Surface SHOULD disclose:

- corpus scope;
- corpus limitations;
- Meta-Witnesses involved;
- synthesis status;
- material caveats;
- unresolved dissent;
- confidence or evidentiary strength;
- whether claims are exploratory, adjudicated, or approved;
- how to challenge the synthesis;
- what downstream use is permitted.

A Synthesis Surface MUST NOT imply that semantic synthesis is primary testimony.

A Synthesis Surface MUST NOT present corpus-level meaning as determinative for every individual case unless adjudicated and scoped for that use.

---

## 16. Downstream Use Constraints

Semantic Synthesis MAY inform:

- policy revision;
- schema revision;
- prompt revision;
- template revision;
- execution gates;
- training;
- audit focus;
- repair priorities;
- governance dashboards;
- risk controls;
- public reporting;
- institutional learning.

Semantic Synthesis SHOULD NOT directly authorize high-impact execution unless the synthesis has been scoped, adjudicated, and legitimated for that purpose.

A synthesis created for learning SHOULD NOT silently become enforcement policy.

A synthesis created for internal review SHOULD NOT silently become public truth.

A synthesis created from incomplete records SHOULD NOT silently become doctrine.

---

## 17. Record Requirements

A CDP implementation SHOULD record:

- corpus definition;
- corpus adequacy review;
- Meta-Witness assignments;
- synthesis artifacts;
- Synthesis Claims;
- semantic provenance maps;
- caveats;
- dissent;
- challenge records;
- adjudication records;
- synthesis surfaces;
- publication records;
- correction or retraction records;
- downstream actions taken;
- learning closure.

The record MUST preserve enough information for a future reviewer to determine what corpus was interpreted, what meaning was synthesized, what was caveated, what was contested, and how the synthesis affected later action.

---

## 18. Learning Closure

Meta-Review SHOULD feed the Learn Protocol when:

- repeated record inadequacy appears across a corpus;
- repeated surface drift appears across decisions;
- witnesses repeatedly disagree in predictable patterns;
- affected-party testimony reveals recurring omission;
- challenges reveal policy ambiguity;
- repair records reveal structural harm;
- execution outcomes contradict expected meaning;
- synthesis claims are successfully challenged;
- semantic drift becomes visible after publication;
- doctrine or templates require revision.

Learning closure MAY require:

- schema revision;
- envelope revision;
- witness protocol revision;
- surface protocol revision;
- adequacy criteria revision;
- policy clarification;
- execution control changes;
- affected-party review processes;
- repair protocol activation;
- dashboard redesign;
- training changes;
- public correction.

---

## 19. Security and Safety Considerations

### 19.1 Theology Laundering

A later synthesis may become more authoritative in practice than primary witness testimony.

CDP MUST prevent later interpretation from pretending to be original record.

### 19.2 Corpus Capture

A synthesis can appear objective while the corpus is biased, incomplete, overfiltered, or institutionally captured.

Corpus definition and adequacy review are required safeguards.

### 19.3 Dissent Erasure

Aggregate meaning may erase minority witness readings that are material to legitimacy, safety, rights, culture, or repair.

CDP SHOULD preserve dissent where dissent matters.

### 19.4 Pattern Overreach

Pattern detection may overgeneralize beyond the corpus.

CDP SHOULD distinguish exploratory patterns from adjudicated conclusions.

### 19.5 Semantic Authority Laundering

An institution may use synthesis to convert preference, convenience, or risk aversion into apparent evidence.

Synthesis Claims SHOULD preserve provenance, caveat, and contestability.

### 19.6 Affected-Party Erasure

Meta-analysis can flatten lived experience into aggregate trend.

For repair-sensitive or rights-affecting synthesis, affected-party testimony SHOULD remain visible and challengeable.

---

## 20. Implementation Notes

A simple implementation MAY begin with:

1. define a witness corpus;
2. review corpus adequacy;
3. assign one AI Meta-Witness and one human reviewer;
4. generate a synthesis memo;
5. extract material Synthesis Claims;
6. map claims to supporting and contradicting artifacts;
7. disclose caveats and dissent;
8. publish a draft Synthesis Surface only after review.

A mature implementation MAY include:

- semantic provenance graphs;
- corpus adequacy scoring;
- multi-model Meta-Witness comparison;
- affected-party meta-review;
- synthesis claim registries;
- contradiction and dissent preservation;
- dashboard-level semantic drift detection;
- policy impact gating;
- doctrine approval workflows;
- public correction and retraction workflows;
- repair-linked meta-analysis.

---

## 21. Non-Goals

This RFC does not require:

- treating synthesis as superior to witness testimony;
- replacing primary records;
- eliminating human interpretation;
- forbidding AI-assisted meta-review;
- requiring statistical meta-analysis for every synthesis;
- publishing all sensitive corpus material;
- resolving every disagreement;
- producing doctrine from every pattern.

This protocol governs higher-order meaning-making. It does not replace Canonical Records, Witness Records, Synoptic Review, Surface Integrity, Adequacy Review, Challenge, Adjudication, Legitimation, Appeal, Repair, or Learn.

---

## 22. Summary

CDP decisions do not only produce records.

They produce traditions of interpretation.

Witnesses testify.

Surfaces explain.

Records prove or fail to prove.

Outcomes reveal consequences.

Repairs reveal what was missed.

Over time, meaning emerges across the corpus.

The Semantic Layer and Meta-Review Protocol governs that emergence.

It allows CDP to synthesize meaning across witnesses, records, challenges, surfaces, outcomes, and repairs without pretending that synthesis is primary testimony.

The canonical record says what was recorded.

The witnesses say what it appears to mean.

The surface says what humans were shown.

Adequacy review asks whether the record was enough.

Semantic synthesis asks what the corpus means.

And CDP requires that later meaning preserve provenance, caveat, dissent, affected-party context, and contestability.

Meaning may emerge after witness.

But it must not colonize witness.
