# RFC-CDP-033 — Standing and Recusal Model

Author: Kevin “Andie” Williams  
Status: Draft v0.4  
Series: Constitutional Decision Plane (CDP)  
Date: May 23, 2026  
Depends On: RFC-CDP-025, RFC-CDP-030, RFC-CDP-031, RFC-CDP-032, RFC-CDP-070, RFC-CDP-071, RFC-CDP-072, RFC-CDP-073, RFC-CDP-074, RFC-CDP-075  
Related: RFC-CDP-040, RFC-CDP-041, RFC-CDP-045, RFC-CDP-050, RFC-CDP-052, RFC-CDP-060, RFC-CDP-062

## Abstract

This RFC defines **Standing** and **Recusal** as first-class governance concepts in the Constitutional Decision Plane (CDP).

Standing determines whether an actor has the recognized right or responsibility to participate in a specific CDP decision stage.

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
  standing_granted_by: <actor_id>
  standing_granted_at: <timestamp>
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

## 11. Standing Types and Constitutional Root

### 11.1 The Constitutional Root Problem

Standing requires a granter. But who grants standing to the standing-granter?

CDP resolves this by establishing that some standing types are **constitutional** — granted by the CDP framework itself as a precondition of legitimate governance, not by any actor within the system.

Constitutional standing requires no granter.

It is axiomatic within CDP.

If CDP cannot guarantee standing to affected parties, evidence custodians, and record-keepers, it has no legitimate claim to govern consequential decisions. The constitutional standing types are therefore preconditions of CDP's own legitimacy, not outputs of it.

The regress stops here.

---

### 11.2 Standing Type Taxonomy

CDP recognizes the following standing types:

#### Constitutional Standing

Granted by the CDP framework itself.

Cannot be revoked by any actor.

Requires no granter within the system.

Subtypes:

**Affected-Party Standing**

Arises when a decision may materially affect an actor. The claim of potential impact is sufficient for preliminary standing, subject to scope challenge. No actor may deny affected-party standing on the grounds that impact has not yet been proven.

**Evidence-Custodian Standing**

Arises from custody of decision-relevant records, evidence, or data. Bounded to stages where that evidence is relevant.

**Record-Keeper Standing**

Arises from role responsibility for maintaining the decision record. Unconditional within the Record stage.

#### Delegated Standing

Granted by an actor or institution with recognized authority, traceable to either constitutional standing or an institutionally recognized authority defined in `RFC-CDP-032-Authority-and-Delegation-Model.md`.

Time-bounded and revocable.

#### Emergency Standing

Arises temporarily when normal standing determination is impractical under declared emergency conditions.

Requires: explicit rationale, time boundary, post-hoc review, and record.

Must not become a mechanism for bypassing constitutional standing under urgency.

Detailed emergency conditions are governed by `RFC-CDP-052-Emergency-Override-and-Kill-Switch.md`.

#### Repair Standing

Arises for affected parties and evidence custodians when a governance breach is recognized and a repair process is initiated. Governed by the Repair plane (`RFC-CDP-070` through `RFC-CDP-075`).

#### Appeal Standing

Arises when a completed decision is formally contested. Governed by `RFC-CDP-070-Appeals-and-Contestability-Model.md`.

---

### 11.3 Standing Grant Authority

| Standing Type | Granted By |
|---|---|
| Constitutional (all subtypes) | CDP framework |
| Delegated | Recognized actor or institution |
| Emergency | CDP framework conditionally; requires human authorization |
| Repair | CDP framework upon breach recognition |
| Appeal | CDP framework upon contestation |

---

### 11.4 Constitutional Standing Protection

Denial of constitutional standing is a governance breach.

Any attempt by an actor to prevent an affected party, evidence custodian, or record-keeper from exercising their constitutional standing is subject to the CDP Repair plane.

Denial of constitutional standing MUST automatically generate a Breach Record under `RFC-CDP-072-Breach-Record-and-Repair-Agenda-Schema.md`. This MUST NOT require action by the affected party.

The record of the denial MUST be preserved.

The affected party MUST be informed of their right to appeal.

---

### 11.5 Contestability Boundaries

Standing contestability is tiered:

**Constitutional standing**

Cannot be contested as to existence. Scope and stage may be challenged.

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

This RFC was created from Session 002 of the CDP collaboration process and updated in Sessions 005 and 009.

Promoted into this draft:

- Standing and Recusal as first-class concepts;
- the authority-capture-through-participation failure mode;
- the relationship between Standing, Recusal, Identity, Attestation, and Authority;
- the need for AI Functional Standing without legal personhood claims;
- a seed Standing Record schema;
- the standing type taxonomy and constitutional root model;
- constitutional standing protection as a Repair-plane-triggering governance breach;
- automatic Breach Record generation when constitutional standing is denied;
- Standing Persistence as a two-layer governed artifact plus enforcement projection model.

Not yet resolved:

- whether the schema belongs here or in a separate schema RFC;
- how risk classes determine recusal depth;
- how this model updates lifecycle protocol RFCs;
- how Functional Standing relates to `RFC-CDP-062-HITL-AIITL-Role-Boundaries.md`;
- whether `RFC-CDP-001-Vision-Scope-Principles.md` sufficiently supports constitutional standing as axiomatic;
- how implementation profiles enforce projection atomicity.

---

## 15. Summary

Standing determines who may participate.

Recusal determines when participation must be limited.

Authority capture through participation is a structural governance failure.

Legitimacy by infinite delegation is a constitutional-root failure.

Standing as unenforceable record is a persistence failure.

CDP must not merely ask whether a decision was reviewed.

It must ask whether the right actors had standing, whether conflicted actors were recused, whether constitutional standing was protected, whether constitutional standing denial automatically enters the Repair plane, whether the standing record was enforceable in time, and whether the process remained genuinely contestable.
