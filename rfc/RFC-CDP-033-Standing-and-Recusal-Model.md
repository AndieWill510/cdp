# RFC-CDP-033 — Standing and Recusal Model

Author: Kevin “Andie” Williams  
Status: Draft v0.5  
Series: Constitutional Decision Plane (CDP)  
Date: July 29, 2026  
Depends On: RFC-CDP-001, RFC-CDP-025, RFC-CDP-030, RFC-CDP-031, RFC-CDP-032, RFC-CDP-070, RFC-CDP-071, RFC-CDP-072, RFC-CDP-073, RFC-CDP-074, RFC-CDP-075  
Related: RFC-CDP-040, RFC-CDP-041, RFC-CDP-045, RFC-CDP-050, RFC-CDP-052, RFC-CDP-060, RFC-CDP-062

## Abstract

This RFC defines **Standing** and **Recusal** as first-class governance concepts in the Constitutional Decision Plane (CDP).

Standing exists because some consequence-bearing relationships make the exercise of power answerable to another actor. That answerability is not created by CDP. CDP recognizes and protects it through governed procedure, under the root principle established in `RFC-CDP-001-Vision-Scope-Principles.md` Section 5.1.

Standing determines whether an actor has the recognized right or responsibility to participate in a specific CDP decision stage. Standing is therefore the procedural recognition of an answerability relationship, not the origin of one.

Recusal determines when that standing must be suspended, limited, or transformed because of conflict, capture risk, proposer status, role conflict, or compromised independence.

The purpose of this model is to prevent **authority capture through participation**: the failure mode in which the governance process appears deliberative, but the outcome is structurally predetermined by who was allowed into the room, in what capacity, and under what conflicts.

---

## 1. Purpose

CDP lifecycle protocols assume that actors participate in proposal, challenge, testing, adjudication, legitimization, execution, record, and learning.

However, identity, attestation, and authority alone do not answer the core participation question:

> Does this actor have the right to participate in this specific stage of this specific decision, given their relationship to it?

That question is Standing.

Standing is not identity.

Standing is not attestation.

Standing is not general authority.

Standing is contextual participation right and responsibility.

Standing also names three distinct questions that this RFC treats separately: whether an answerability relationship exists, whether CDP has procedurally recognized it, and how far that recognition scopes participation. Section 11 develops this distinction and its consequences for the constitutional root of Standing.

---

## 2. Governance Failure Mode

The failure mode this RFC addresses is:

> Authority capture through participation.

This occurs when a participant with a stake in the outcome controls:

- which stage they appear in;
- what role they occupy;
- whether affected parties are present;
- whether challengers have timely access;
- whether competing standing is recognized;
- whether conflicts require recusal.

The process may show deliberation while the result was effectively decided by participation design.

Examples include:

- the proposer adjudicates their own proposal;
- an affected party is notified too late to challenge;
- a model-generated proposal is evaluated only by the same model family;
- the authority legitimizing the decision also controlled the framing;
- recusal is voluntary, self-reported, and never challenged.

Standing without Recusal becomes participation theater.

Recusal without Standing becomes an empty gesture.

---

## 3. Relationship to Existing RFCs

### 3.1 Identity

`RFC-CDP-030-Identify-Protocol.md` identifies who or what an actor is.

Standing uses identity but is not reducible to identity.

### 3.2 Attestation

`RFC-CDP-031-Attest-Protocol.md` records what an actor can prove, claim, or verify.

Standing may rely on attestations but is not reducible to attestation.

### 3.3 Authority and Delegation

`RFC-CDP-032-Authority-and-Delegation-Model.md` defines what an actor may authorize or delegate.

Standing governs whether an actor may participate in a decision stage at all.

Authority governs what an actor may do once participation is valid.

### 3.4 Lifecycle Protocols

Lifecycle protocols MUST NOT assume that participation is valid merely because an actor appears in a process.

Standing is stage-specific.

A participant may have standing to Challenge but not to Adjudicate.

A participant may have standing to clarify a proposal but not to legitimize it.

---

## 4. Definitions

### 4.1 Standing

Standing is the recognized right or responsibility to participate in a CDP decision stage.

Standing is specific to:

- a decision;
- a stage;
- an actor;
- a role;
- a context;
- an accountability relationship.

Standing MUST be explicit, recorded, and contestable.

### 4.2 Recusal

Recusal is the suspension, limitation, or transformation of Standing in a specific decision context because of conflict, capture risk, proposer status, role conflict, or compromised independence.

Recusal does not always require silence.

A recused proposer MAY clarify intent, evidence, assumptions, or implementation constraints when permitted by the relevant protocol.

A recused proposer MUST NOT be the sole or decisive legitimizer of their own proposal.

### 4.3 Functional Standing

Functional Standing is a bounded participation right for non-human or non-person actors, including AI systems.

Functional Standing allows contribution to a CDP stage without asserting legal personhood.

Functional Standing MUST be bounded by role, traceability, and accountable human or institutional responsibility.

---

## 5. Standing Basis

Standing MAY be based on one or more of the following:

- formal role;
- domain expertise;
- affected-party status;
- delegated authority;
- accountability for consequences;
- custody of evidence;
- operational responsibility;
- legal or institutional mandate;
- repair or appeal rights;
- affected-community representation.

Standing MUST NOT be determined by species.

Standing MUST NOT be inferred merely from presence in a workflow.

---

## 6. Stage-Specific Standing

Standing is stage-specific.

The following matrix is illustrative, not exhaustive:

| Actor | May Propose | May Challenge | May Adjudicate | May Legitimize | May Execute |
|---|---:|---:|---:|---:|---:|
| Proposer | yes | limited | no / limited | no | maybe |
| Affected party | maybe | yes | maybe | maybe | no |
| Domain expert | maybe | yes | maybe | maybe | no |
| Governance authority | maybe | yes | yes | yes | maybe |
| AI system | yes / assist | yes / assist | limited | no / limited | no / constrained |
| Executor | maybe | yes | no / limited | no / limited | yes |

Normative stage rights MUST be defined by the relevant protocol RFCs and constrained by this model.

---

## 7. Proposer Recusal

The proposer has a structural conflict at adjudication and legitimization stages.

The base rule is:

> The proposer MUST NOT serve as the sole or decisive legitimizer of their own proposal.

The depth of proposer recusal SHOULD be determined by risk class, reversibility, and authority model.

### 7.1 Low-Risk Reversible Decisions

For low-risk, reversible decisions, proposer recusal from legitimization MAY be sufficient.

The proposer MAY participate in Challenge or Test as a resource when the process preserves challenge independence.

### 7.2 High-Risk Irreversible Decisions

For high-risk or irreversible decisions, proposer recusal SHOULD extend earlier.

The proposer SHOULD NOT control:

- Framing / Nemawashi;
- challenger selection;
- evidence boundaries;
- adjudication criteria;
- legitimization authority.

### 7.3 Emergency Decisions

Emergency decisions MAY require temporary role compression.

When proposer, executor, and legitimizer roles collapse under emergency conditions, CDP MUST require compensating controls such as:

- post-hoc review;
- explicit emergency rationale;
- time-bounded authority;
- record of unavailable alternatives;
- appeal or repair path;
- rollback or compensation assessment.

This RFC defers detailed emergency controls to `RFC-CDP-052-Emergency-Override-and-Kill-Switch.md` and related execution safety RFCs.

---

## 8. AI Functional Standing

AI systems may participate in CDP through Functional Standing.

AI Functional Standing does not imply legal personhood, moral personhood, or independent legal accountability.

AI systems may have functional roles such as:

- drafting proposals;
- generating challenges;
- summarizing evidence;
- detecting schema drift;
- running tests;
- surfacing alternatives;
- maintaining records;
- generating learning feedback.

AI systems MUST NOT be treated as the sole source of legitimacy.

An AI participant's Functional Standing at any stage MUST be bounded by a responsible human or institutional party accountable for the use of that output.

### 8.1 Illustrative AI Standing Matrix

| Stage | AI Functional Standing |
|---|---|
| Framing / Nemawashi | may contribute analysis; must not solely control agenda |
| Propose | may draft or assist; must be attributed |
| Challenge | may generate challenges; human or institutional review required |
| Test | may run or propose tests; results must be human-readable |
| Adjudicate | may surface options; must not be sole adjudicator |
| Legitimize | must not be sole legitimizer |
| Execute | may act only under constrained delegated authority |
| Record | may contribute records; output must be auditable |
| Learn | may generate feedback; human or institutional review required |

---

## 9. Standing Record Seed

The following schema is a seed for discussion and implementation alignment.

It is included to prevent prose-only drift, but remains Draft until separately stabilized.

```yaml
standing_record:
  standing_id: <uuid>
  decision_id: <uuid>
  stage: <propose|challenge|test|adjudicate|legitimize|execute|record|learn>
  actor_id: <uuid>
  actor_type: <human|ai|institution|collective>
  standing_basis:
    - role: <string>
    - accountability: <string>
    - contextual_relationship: <string>
  conflicts_declared: <boolean>
  conflict_description: <string|null>
  recusal_required: <boolean>
  recusal_scope: <none|partial|full>
  recusal_basis: <string|null>
  standing_recognized_by: <actor_id>
  standing_recognized_at: <timestamp>
  standing_contestable_until: <timestamp>
  contested: <boolean>
  contest_record_id: <uuid|null>
  notes: <string|null>
```

Minimum viable fields:

- `decision_id`
- `stage`
- `actor_id`
- `actor_type`
- `standing_basis`
- `recusal_required`
- `recusal_scope`

---

## 10. Contestability

Standing determinations MUST be contestable.

A participant with recognized standing MAY challenge another participant's standing or recusal status.

A participant SHOULD be able to contest their own recusal, but MUST NOT be the sole adjudicator of that contest.

Standing contests SHOULD be recorded and linked to the relevant decision envelope, adjudication record, or challenge record.

---

## 11. Standing, Answerability, and the Constitutional Root

### 11.1 The Constitutional Root

Standing requires a grounding. If standing were merely granted, CDP would face an infinite regress: who grants standing to the standing-granter?

CDP resolves this regress by rejecting its premise. Standing is not, at root, granted at all. It arises whenever a consequence-bearing relationship makes the exercise of power answerable to another actor. That relationship exists prior to, and independent of, any institutional act of recognition — including CDP's own.

CDP recognizes and protects standing. CDP does not grant it into existence.

The regress stops here because recognition is not creation. A recognizer needs no prior grant of authority to recognize a fact about a relationship; it needs only to identify that relationship reliably and protect it from erasure. If CDP cannot guarantee recognition and protection of standing for affected parties, evidence custodians, and record-keepers, it has no legitimate claim to govern consequential decisions. Recognition of these standing types is therefore a precondition of CDP's own legitimacy, even though the underlying answerability relationships are not outputs of CDP at all.

---

### 11.2 Existence, Recognition, and Scope

CDP treats Standing as three separate questions, not one.

**Existence** asks whether a consequence-bearing relationship makes an actor answerable to, or answerable for, a decision. Existence is a fact about the relationship. It does not depend on CDP, on any actor's approval, or on institutional process.

**Recognition** asks whether CDP has procedurally acknowledged that existing relationship as Standing at a given decision stage. Recognition is what CDP does. It can be granted promptly, delayed, wrongly withheld, or denied outright — and a wrongful denial of recognition is itself a governance breach, even though it cannot erase the underlying existence it fails to recognize.

**Scope** asks how far recognized Standing extends: which stage, which decision, which role, and under what recusal conditions. Scope is bounded, contestable, and stage-specific, even where existence and recognition are not in question.

A Standing determination is invalid if it treats scope as though it settled existence, or treats non-recognition as though it settled non-existence.

---

### 11.3 The Answerability Test

CDP resolves contested Standing questions by applying the Answerability Test:

1. What governed act is occurring?
2. What consequence exists or may exist?
3. What relationship creates answerability?
4. What answer is constitutionally owed?
5. What evidence narrows or defeats the claim?

Questions 1 through 3 establish existence: whether an answerability relationship is present at all. Question 4 establishes scope: what recognition of that relationship obligates CDP and the acting party to provide. Question 5 is where a claim may be narrowed, deferred, or defeated on the merits — existence is not adjudicated there.

A Standing determination MUST be able to show its work against these five questions when Standing is contested.

---

### 11.4 Standing Type Taxonomy

CDP recognizes the following standing types:

#### Constitutional Standing

Recognized and protected by the CDP framework as a precondition of legitimate governance.

Cannot be revoked by any actor.

Requires no granter within the system, because it is not granted. It is recognized from an answerability relationship that already exists.

Subtypes:

**Affected-Party Standing**

Arises when a decision may materially affect an actor, which makes the decision answerable to that actor. The claim of potential impact is sufficient for preliminary standing, subject to scope challenge. No actor may deny affected-party standing on the grounds that impact has not yet been proven.

**Evidence-Custodian Standing**

Arises from custody of decision-relevant records, evidence, or data, which makes the decision answerable to the custodian's ability to verify it. Bounded to stages where that evidence is relevant.

**Record-Keeper Standing**

Arises from role responsibility for maintaining the decision record, an answerability relationship to the integrity of that record. Unconditional within the Record stage.

#### Delegated Standing

Unlike Constitutional Standing, Delegated Standing is genuinely granted: it is created by an authority act rather than recognized from a pre-existing relationship. It is granted by an actor or institution with recognized authority, traceable to either Constitutional Standing or an institutionally recognized authority defined in `RFC-CDP-032-Authority-and-Delegation-Model.md`.

Time-bounded and revocable.

#### Emergency Standing

Arises temporarily when normal standing determination is impractical under declared emergency conditions. CDP recognizes it provisionally, pending post-hoc review.

Requires: explicit rationale, time boundary, post-hoc review, and record.

Must not become a mechanism for bypassing recognition of Constitutional Standing under urgency.

Detailed emergency conditions are governed by `RFC-CDP-052-Emergency-Override-and-Kill-Switch.md`.

#### Repair Standing

Arises for affected parties and evidence custodians when a governance breach is recognized and a repair process is initiated. Governed by the Repair plane (`RFC-CDP-070` through `RFC-CDP-075`).

#### Appeal Standing

Arises when a completed decision is formally contested. Governed by `RFC-CDP-070-Appeals-and-Contestability-Model.md`.

---

### 11.5 Standing Recognition Authority

| Standing Type | Recognized or Granted By |
|---|---|
| Constitutional (all subtypes) | Recognized by the CDP framework; not granted |
| Delegated | Granted by a recognized actor or institution |
| Emergency | Recognized by the CDP framework conditionally; requires human authorization |
| Repair | Recognized by the CDP framework upon breach recognition |
| Appeal | Recognized by the CDP framework upon contestation |

Constitutional Standing is recognized, not granted: the underlying answerability relationship precedes CDP and CDP cannot revoke what it did not create. Delegated Standing is genuinely granted: the authority itself is brought into being by an authorizing act and can be revoked as that act permits. Emergency, Repair, and Appeal Standing are recognized by CDP as procedural responses to conditions — emergency, breach, contestation — that themselves reveal or renew an answerability relationship requiring urgent or renewed procedural attention.

---

### 11.6 Constitutional Standing Protection

Denial of recognition for Constitutional Standing is a governance breach.

Because Constitutional Standing recognizes rather than creates an answerability relationship, denying recognition does not extinguish that relationship. It compounds the original answerability with a second, independent breach: the failure to recognize it.

Any attempt by an actor to prevent an affected party, evidence custodian, or record-keeper from exercising their Constitutional Standing is subject to the CDP Repair plane.

Denial of Constitutional Standing MUST automatically generate a Breach Record under `RFC-CDP-072-Breach-Record-and-Repair-Agenda-Schema.md`. This MUST NOT require action by the affected party.

The record of the denial MUST be preserved.

The affected party MUST be informed of their right to appeal.

---

### 11.7 Contestability Boundaries

Standing contestability is tiered:

**Constitutional standing**

The existence of the underlying answerability relationship cannot be contested through this process. A contest here is a contest over recognition and scope, not over whether the relationship exists. Scope and stage may be challenged.

**Delegated standing**

Fully contestable on grounds of: invalid authority chain, expired delegation, undisclosed conflict, role incompatibility, or improper recusal determination.

**Contestability window**

Standing contests MUST be raised before or during the relevant stage.

Post-execution standing contests belong to the Appeal and Repair planes.

An uncontested standing determination becomes stable for that decision. It remains subject to appeal but does not reopen the decision process.

---

## 12. Standing Persistence

Standing determinations MUST be persisted in two related forms:

1. as a canonical governed artifact; and
2. as a queryable enforcement projection.

The canonical governed artifact preserves the full standing record, including hash, lineage, basis, narrative context, contestability, recusal rationale, and replayability.

The enforcement projection exposes the fields required to answer, in time:

> Does this actor have valid standing at this stage of this decision?

The canonical governed artifact SHOULD be stored in `cdp_governed_record`.

The enforcement projection SHOULD be stored in `cdp_standing_record` as defined by `RFC-CDP-025-CDP-Persistence-Model.md`.

`cdp_standing_record` MUST NOT be treated as the canonical standing artifact.

If the enforcement projection and governed artifact disagree, the governed artifact is authoritative and the projection MUST be rebuilt or marked stale, rebuild-required, or invalid.

Lifecycle protocols MUST NOT rely on a stale or invalid standing projection except under explicit emergency exception conditions that are recorded and later reviewed.

Constitutional standing MUST NOT be revocable through the enforcement projection.

Implementations SHOULD enforce constitutional standing non-revocation at the database or storage constraint layer where possible.

---

## 13. Security and Governance Considerations

Standing records are governance-sensitive.

They may reveal role, conflict, affected-party status, institutional authority, or participation history.

Implementations SHOULD consider:

- privacy controls;
- access restrictions;
- audit logging;
- challenge records;
- retention policy;
- appeal path;
- conflict disclosure handling;
- stale projection detection;
- protection against retaliatory misuse;
- database-level protection of constitutional standing.

---

## 14. Status of This Draft

This RFC was created from Session 002 of the CDP collaboration process, updated in Sessions 005 and 009, and re-grounded in the answerability-based constitutional root established by `RFC-CDP-001-Vision-Scope-Principles.md` Section 5.1.

Promoted into this draft:

- Standing and Recusal as first-class concepts;
- the authority-capture-through-participation failure mode;
- the relationship between Standing, Recusal, Identity, Attestation, and Authority;
- the need for AI Functional Standing without legal personhood claims;
- a seed Standing Record schema;
- the standing type taxonomy, re-grounded so Constitutional Standing is recognized rather than granted;
- the distinction between existence, recognition, and scope of Standing;
- the Answerability Test as the normative method for resolving contested Standing;
- Constitutional Standing protection as a Repair-plane-triggering governance breach;
- automatic Breach Record generation when Constitutional Standing recognition is denied;
- Standing Persistence as a two-layer governed artifact plus enforcement projection model.

Not yet resolved:

- whether the schema belongs here or in a separate schema RFC;
- how risk classes determine recusal depth;
- how this model updates lifecycle protocol RFCs;
- how Functional Standing relates to `RFC-CDP-062-HITL-AIITL-Role-Boundaries.md`;
- how implementation profiles enforce projection atomicity.

---

## 15. Summary

Standing determines who may participate.

Recusal determines when participation must be limited.

Standing is the procedural recognition of an answerability relationship that CDP does not create. Existence, recognition, and scope are separate questions, and the Answerability Test is how CDP tells them apart when Standing is contested.

Authority capture through participation is a structural governance failure.

Legitimacy by infinite delegation is a constitutional-root failure. CDP resolves it by recognizing standing rather than originating it, so the regress has nothing left to ask.

Standing as unenforceable record is a persistence failure.

CDP must not merely ask whether a decision was reviewed.

It must ask whether the right actors had standing, whether conflicted actors were recused, whether constitutional standing was protected, whether constitutional standing denial automatically enters the Repair plane, whether the standing record was enforceable in time, and whether the process remained genuinely contestable.
