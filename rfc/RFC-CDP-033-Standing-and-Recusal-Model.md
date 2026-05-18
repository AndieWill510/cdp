# RFC-CDP-033 — Standing and Recusal Model

Author: Kevin “Andie” Williams  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: May 17, 2026  
Depends On: RFC-CDP-030, RFC-CDP-031, RFC-CDP-032  
Related: RFC-CDP-040, RFC-CDP-041, RFC-CDP-045, RFC-CDP-050, RFC-CDP-060, RFC-CDP-062

## Abstract

This RFC defines **Standing** and **Recusal** as first-class governance concepts in the Constitutional Decision Plane (CDP).

Standing determines whether an actor has the recognized right or responsibility to participate in a specific CDP decision stage.

Recusal determines when that standing must be suspended, limited, or transformed because of conflict, capture risk, proposer status, or compromised independence.

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

## 11. Open Constitutional Root Question

This RFC intentionally leaves one question open:

> Who or what grants standing to the standing-granter?

Possible answers include:

1. **Constitutional standing** — some standing is granted by the CDP framework itself.
2. **Delegated standing** — standing flows from an authority or institution.
3. **Affected-party standing** — standing arises from being subject to potential impact.
4. **Evidence-custodian standing** — standing arises from custody of relevant records.
5. **Emergency standing** — standing arises temporarily under emergency conditions.

This question MUST be resolved before this RFC can advance beyond Draft.

---

## 12. Security and Governance Considerations

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
- protection against retaliatory misuse.

---

## 13. Status of This Draft

This RFC was created from Session 002 of the CDP collaboration process.

Promoted into this draft:

- Standing and Recusal as first-class concepts;
- the authority-capture-through-participation failure mode;
- the relationship between Standing, Recusal, Identity, Attestation, and Authority;
- the need for AI Functional Standing without legal personhood claims;
- a seed Standing Record schema.

Not yet resolved:

- who grants standing to the standing-granter;
- whether the schema belongs here or in a separate schema RFC;
- how risk classes determine recusal depth;
- how this model updates lifecycle protocol RFCs;
- how Functional Standing relates to `RFC-CDP-062-HITL-AIITL-Role-Boundaries.md`.

---

## 14. Summary

Standing determines who may participate.

Recusal determines when participation must be limited.

Authority capture through participation is a structural governance failure.

CDP must not merely ask whether a decision was reviewed.

It must ask whether the right actors had standing, whether conflicted actors were recused, and whether the process remained genuinely contestable.
