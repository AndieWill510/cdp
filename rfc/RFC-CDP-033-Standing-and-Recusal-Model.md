# RFC-CDP-033 — Standing and Recusal Model

Author: Kevin “Andie” Williams  
Status: Draft v0.7  
Series: Constitutional Decision Plane (CDP)  
Date: July 29, 2026; revised August 6, 2026  
Depends On: RFC-CDP-001, RFC-CDP-025, RFC-CDP-030, RFC-CDP-031, RFC-CDP-032, RFC-CDP-070, RFC-CDP-071, RFC-CDP-072, RFC-CDP-073, RFC-CDP-074  
Related: RFC-CDP-040, RFC-CDP-041, RFC-CDP-045, RFC-CDP-050, RFC-CDP-052, RFC-CDP-060, RFC-CDP-062, RFC-CDP-078  
Reserved, not a dependency: RFC-CDP-075 (Rematriation and Land/Resource Return Protocol) does not yet exist as a drafted RFC. This RFC does not depend on its content and will cite it if and when it is drafted.

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

### 3.5 Relationship Type

`RFC-CDP-078-Relationship-Taxonomy-and-Recognition-Model.md` classifies what kind of relationship exists between actors.

Relationship Type is explanatory, not gating. It MUST NOT be treated as a prerequisite for Standing, and unresolved or contested Relationship Type classification MUST NOT suspend, delay, diminish, or defeat a Standing determination, per `RFC-CDP-078` §8.2's non-suspension rule. A Standing claim MAY be evaluated and recognized before, without, or independently of any Relationship Type classification of the same underlying relationship.

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

The following four schemas are a seed for discussion and implementation alignment. They are included to prevent prose-only drift, but remain Draft until separately stabilized.

Standing Claim, Standing Recognition, Recusal, and Contest are four distinct acts, made by different parties at different times, each with its own epistemic status. A single mutable record that overwrites earlier fields when a later act occurs would erase the disagreement, timing, and provenance those acts are supposed to preserve. This RFC therefore requires four separate, append-only records rather than one record updated in place. Implementations MAY store them in separate tables or as separate immutable rows in a shared table; they MUST NOT collapse them into a single row that a later act overwrites.

### 9.1 Standing Claim

Created when an actor asserts a basis for Standing. Immutable once created; a correction or withdrawal is a new record, not an edit.

```yaml
standing_claim:
  claim_id: <uuid>
  decision_id: <uuid>
  stage: <propose|challenge|test|adjudicate|legitimize|execute|record|learn>
  actor_id: <uuid>
  actor_type: <human|ai|institution|collective>
  standing_type: <constitutional_affected_party|constitutional_evidence_custodian|constitutional_record_keeper|delegated|emergency|repair|appeal>
  standing_basis:
    - role: <string>
    - accountability: <string>
    - contextual_relationship: <string>
  submitted_at: <timestamp>
  withdrawn_at: <timestamp|null>
  notes: <string|null>
```

Minimum viable fields: `decision_id`, `stage`, `actor_id`, `actor_type`, `standing_type`, `standing_basis`, `submitted_at`.

### 9.2 Standing Recognition Determination

Created when a binding recognition act (Section 11.5) confirms, narrows, defers, rejects, or denies a Standing Claim. References the claim it determines; never edits it. A later determination on the same claim (correction, contest outcome) is a new record referencing the prior determination, not an overwrite of it.

```yaml
standing_recognition_determination:
  determination_id: <uuid>
  claim_id: <uuid>
  outcome: <recognized|narrowed|deferred|rejected|denied>
  outcome_scope: <string|null>
  outcome_basis: <string>
  determined_by: <actor_id>
  determined_at: <timestamp>
  supersedes_determination_id: <uuid|null>
  contestable_until: <timestamp>
  notes: <string|null>
```

Minimum viable fields: `claim_id`, `outcome`, `outcome_basis`, `determined_by`, `determined_at`.

Section 11.8 defines `recognized`, `narrowed`, `deferred`, `rejected`, and `denied` precisely, including which outcomes may trigger the automatic Breach Record rule in Section 11.6.

### 9.3 Recusal Declaration or Determination

Created independently of a Standing Claim or Recognition Determination — an actor may hold otherwise-valid Standing and still be subject to a Recusal record limiting or suspending it for a specific decision and stage.

```yaml
recusal_record:
  recusal_id: <uuid>
  decision_id: <uuid>
  stage: <propose|challenge|test|adjudicate|legitimize|execute|record|learn>
  actor_id: <uuid>
  conflict_description: <string>
  recusal_scope: <none|partial|full>
  self_declared: <boolean>
  determined_by: <actor_id|null>
  determined_at: <timestamp|null>
  notes: <string|null>
```

Minimum viable fields: `decision_id`, `stage`, `actor_id`, `conflict_description`, `recusal_scope`, `self_declared`. A self-declared recusal (`self_declared: true`, `determined_by: null`) is evidence, not final disposition, per Section 10; it takes effect as a precaution pending confirmation, but a later contest or review MAY narrow, extend, or overturn it via its own new record.

### 9.4 Standing Contest Record

Created when a participant contests a Standing determination or Recusal determination under Section 10. References what it contests; never edits it.

```yaml
standing_contest_record:
  contest_id: <uuid>
  contests_determination_id: <uuid|null>
  contests_recusal_id: <uuid|null>
  raised_by_actor_id: <uuid>
  grounds: <string>
  raised_at: <timestamp>
  resolution: <pending|upheld|overturned|narrowed>
  resolved_by: <actor_id|null>
  resolved_at: <timestamp|null>
  notes: <string|null>
```

Minimum viable fields: exactly one of `contests_determination_id` or `contests_recusal_id`, `raised_by_actor_id`, `grounds`, `raised_at`, `resolution`.

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

The regress stops here because recognition is not creation, but that does not make recognition ambient or ungoverned. Recognition does not manufacture the underlying relationship; it identifies one that already holds. A *binding* CDP recognition — the determination that fixes Standing as enforceable at a given decision stage — is not self-executing merely because someone perceives or asserts a relationship. It requires valid procedural authority, competence, independence, and record, exercised by an actor or process authorized under this RFC to make that determination.

The regress about who authorizes the granter does not reappear here, because the thing being authorized is the act of recognizing an already-existing fact, not the act of creating a right. That distinction matters operationally: a recognition can still be performed by the wrong actor, without required independence, or without record, and when it is, the recognition itself is invalid and contestable under Section 11.7 — even though the underlying relationship is untouched by that failure. Anyone may perceive or assert that a consequence-bearing relationship exists. Only an actor or process with recognized procedural authority under this RFC may bind CDP to that determination.

If CDP cannot guarantee properly authorized recognition and protection of standing for affected parties, evidence custodians, and record-keepers, it has no legitimate claim to govern consequential decisions. Recognition of these standing types is therefore a precondition of CDP's own legitimacy, even though the underlying answerability relationships are not outputs of CDP at all.

---

### 11.2 Existence, Recognition, and Scope

CDP treats Standing as three separate questions, not one.

**Existence** asks whether a consequence-bearing relationship makes an actor answerable to, or answerable for, a decision. Existence is a fact about the relationship, not a fact settled by institutional process. It does not depend on CDP, on any actor's approval, or on institutional process. But a *claim* that existence obtains is not thereby true merely for being asserted: claims about existence remain contestable through evidence and adjudication under the Answerability Test in Section 11.3. Non-recognition MUST NOT be treated as proof that no relationship exists, and, symmetrically, a sustained claim MUST NOT be treated as proof that recognition is what brought the relationship into being. Reality does not depend on procedure. Claims about reality still require testing, and CDP's role is to test them, not to place them beyond examination in either direction.

CDP distinguishes two relationships that "existence" can otherwise blur together:

- **Answerable to** identifies a party to whom an owed answer runs — typically an affected party, an evidence custodian whose material is at stake, or a record-keeper whose record is implicated. Being answerable to an actor is what grounds that actor's own Standing to participate and demand an answer.
- **Answerable for** identifies an actor who holds custodial, official, or agent responsibility for producing, executing, or accounting for a governed act — typically a custodian, officeholder, or delegated agent. Being answerable for a decision grounds duties and record obligations; it does not by itself confer the participation rights that Standing recognizes in the actor to whom the answer is owed.

An actor may be answerable for a decision without being answerable to it in the sense that grounds Affected-Party Standing, and vice versa. The Standing Type Taxonomy in Section 11.4 keeps these separate: Affected-Party Standing arises substantially from being answerable to; Evidence-Custodian and Record-Keeper Standing arise substantially from being answerable for.

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

Questions 1 through 3 identify the *claimed basis* for existence: what is happening, what consequence attaches, and what relationship is asserted to create answerability. Question 4 is compound: it asks what answer is owed, who owes it, to whom, under what authority source — policy, delegation, treaty, law, community authority, or RFC — and within what response window. An implementation MUST be able to answer all parts of question 4 before treating it as settled, and SHOULD align that determination with the authority basis required by `RFC-CDP-032-Authority-and-Delegation-Model.md` and the sovereignty and institutional-response requirements of `RFC-CDP-074-Sovereignty-Claims-and-Authority-Pluralism.md`.

Question 5 tests the claim itself. It may confirm, narrow, defer, or reject the asserted existence or scope: evidence may show that the alleged consequence is too remote, that the actor is not in fact within the relationship claimed, that a claimed custodial relationship does not exist, or that the dispute concerns scope rather than Standing itself. Evidence cannot extinguish a real relationship, and no answer to question 5 is a declaration that institutional recognition creates or extinguishes the underlying reality Section 11.2 describes. But evidence can defeat the *claim* that a relationship exists in a given case. Rejection of a claim under question 5 is a finding about whether this claim correctly describes an existing relationship; it is not a finding that no such relationship could exist, and it does not immunize the determination from later correction if the evidence was wrong.

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

A minimally sufficient claim — one that identifies a possible consequence and the relationship that makes the actor answerable to it — creates **provisional Standing** immediately upon submission. Provisional Standing is sufficient to participate in the stage claimed, including raising the first protected act (for example, a Challenge), without waiting for a binding recognition determination. Binding recognition (Section 11.5) MAY later confirm, narrow, defer, reject, or deny that claim (Section 11.8), but a pending determination MUST NOT itself block the act the provisional claim was sufficient for. This is the operational consequence of treating existence as prior to recognition (Section 11.2): if the first protected act had to wait on recognition, recognition would function as creation in practice, which Section 11.1 already forbids in principle.

A claim that fails minimal sufficiency — one that identifies no possible consequence and no relationship that could make the decision answerable to the claimant — does not acquire provisional Standing. Failing to recognize such a claim does not trigger Section 11.6's Breach Record rule: a claim that never cleared minimal sufficiency was never a sufficient claim to deny. This is distinct from denial of a claim that did clear minimal sufficiency, which Section 11.8 governs precisely.

**Evidence-Custodian Standing**

Arises from custody of decision-relevant records, evidence, or data, which makes the decision answerable to the custodian's ability to verify it. Bounded to stages where that evidence is relevant.

**Record-Keeper Standing**

Arises from role responsibility for maintaining the decision record, an answerability relationship to the integrity of that record. Unconditional within the Record stage.

#### Delegated Standing

Unlike Constitutional Standing, Delegated Standing is genuinely granted: the governed *capacity to exercise participation rights* is created by an authority act, traceable to either Constitutional Standing or an institutionally recognized authority defined in `RFC-CDP-032-Authority-and-Delegation-Model.md`.

Delegation creates a capacity to represent or participate on another basis. It does not manufacture the consequence-bearing relationship from which the underlying answerability arises. An affected party appointing an advocate creates representative authority derived from the affected party's own Standing; it does not create new Standing independent of that relationship. Delegated Standing is therefore doubly grounded: the delegation act is genuinely granted, while the answerability it represents may itself be Constitutional, Repair, or Appeal Standing that CDP only recognizes. A delegate's Standing MUST be traceable to the relationship it represents; a delegation record that cannot be traced back to a recognized or genuinely granted basis is invalid.

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

"Recognized by the CDP framework" in the table above names a role, not a mechanism left open. A binding Standing recognition determination MUST be made by an actor or process that is:

- **bounded** — explicitly identified in advance, not inferred from participation in the matter being decided;
- **non-self-interested** — never the actor whose own Standing, claim, or proposal is under determination, and never an actor whose own conduct is the subject of the answerability relationship being recognized;
- **procedurally authorized** — holding that role through a recorded act (for example, a seeded constitutional role, an Authority Grant under `RFC-CDP-032`, or an equivalent governed appointment), not through unrecorded custom or informal practice;
- **auditable** — every determination it makes MUST be recorded, attributed to it by identity, and reachable by the contestability mechanism in Section 10 and Section 11.7.

This closes the regress named in Section 11.1 without collapsing into either extreme it warns against: the recognizing role does not originate Standing (it is bound by the same existence/recognition/scope distinction as every other recognition act), and it is not ambient (an arbitrary actor asserting a relationship cannot bind CDP merely by asserting it). This RFC does not itself name the specific actor(s) that hold this role for a given deployment — that is an implementation decision, analogous to how `RFC-CDP-030` and `RFC-CDP-032` each bind their own recognition and grant-issuance roles to a specific, bounded, seeded actor rather than leaving either ambient. An implementation MUST document which actor(s) hold the Standing recognition role and MUST be able to show that determination satisfies the four properties above.

---

### 11.6 Constitutional Standing Protection

Denial of recognition for Constitutional Standing is a governance breach.

"Denial" here has the precise meaning Section 11.8 defines, distinguishing it from a `rejected`, `narrowed`, or `deferred` outcome and from a claim that never cleared minimal sufficiency under Section 11.4. Only a `denied` outcome triggers this section.

Because Constitutional Standing recognizes rather than creates an answerability relationship, denying recognition does not extinguish that relationship. It compounds the original answerability with a second, independent breach: the failure to recognize it.

Any attempt by an actor to prevent an affected party, evidence custodian, or record-keeper from exercising their Constitutional Standing is subject to the CDP Repair plane.

Denial of Constitutional Standing MUST automatically generate a Breach Record under `RFC-CDP-072-Breach-Record-and-Repair-Agenda-Schema.md`. This MUST NOT require action by the affected party. The Breach Record MUST be generated by the same actor or process that records the `denied` outcome (Section 9.2, Section 11.8), as part of recording that determination itself — this is what makes generation automatic rather than dependent on a further act by the affected party, who by definition may lack a recognized basis at that moment to initiate a Repair process on their own.

The record of the denial MUST be preserved.

The affected party MUST be informed of their right to appeal.

---

### 11.7 Contestability Boundaries

Standing contestability is tiered:

**Constitutional standing**

The underlying answerability relationship's existence does not depend on institutional recognition and is not created or extinguished by CDP's determination. That independence is not immunity from examination. A *claim* that such a relationship exists remains contestable through evidence and adjudication under the Answerability Test in Section 11.3, on the same terms as any other application of that test. Non-recognition MUST NOT be treated as proof that no relationship exists. Scope and stage may also be challenged.

**Delegated standing**

Fully contestable on grounds of: invalid authority chain, expired delegation, undisclosed conflict, role incompatibility, or improper recusal determination.

**Contestability window**

Standing contests MUST be raised before or during the relevant stage.

Post-execution standing contests belong to the Appeal and Repair planes.

An uncontested standing determination becomes stable for that decision. It remains subject to appeal but does not reopen the decision process.

---

### 11.8 Recognition Outcomes

A binding Standing recognition determination (Section 9.2) MUST record exactly one of the following outcomes:

- **recognized** — the claim is confirmed as presented; Standing is established at the scope claimed.
- **narrowed** — the claim is confirmed but at a smaller scope than claimed (a different stage, a different decision, a different role): Standing exists, bounded differently than asserted.
- **deferred** — the determination is postponed, typically pending evidence or a concurrent process (for example, an unresolved Sovereignty Claim under `RFC-CDP-074`). Provisional Standing established under Section 11.4 continues to apply while deferred, unless the deferral itself states a reasoned basis for suspending it.
- **rejected** — the claim, having cleared minimal sufficiency, is found on the merits not to describe an existing answerability relationship, applying Answerability Test Question 5 (Section 11.3). Rejection is a finding about this claim, not a declaration that no such relationship could exist, and does not immunize the determination from later correction under Section 10.
- **denied** — for Constitutional Standing only: the claim, having cleared minimal sufficiency and correctly describing an existing answerability relationship, is refused recognition anyway; or the recognition process fails to act on a sufficient claim within a reasonable period; or a recognized claim's protection is defeated by an actor's conduct. Denial is what Section 11.6's automatic Breach Record rule attaches to.

**Denial, precisely.** "Denial of Constitutional Standing" in Section 11.6 means a **denied** outcome as defined here — not a **rejected** outcome (the claim did not hold up on the merits after clearing minimal sufficiency), not a claim that never cleared minimal sufficiency in the first place (Section 11.4), and not a **narrowed** or **deferred** outcome, both of which preserve some or all of the claimed Standing rather than refusing it. A good-faith determination that a claim is **rejected** under Question 5, recorded with its basis and open to contest under Section 10, is not itself a breach. A refusal to recognize a claim the Answerability Test would sustain, or a failure to determine a sufficient claim at all, is. Distinguishing a mistaken-but-good-faith rejection from a denial-in-substance is itself a contestable determination (Section 10, Section 11.7) — this RFC does not resolve every case in advance, and an implementation MUST record the basis for classifying an outcome as `denied` rather than `rejected` so that classification is itself reviewable.

Delegated, Emergency, Repair, and Appeal Standing use the same five-value outcome vocabulary where a binding determination is made, except that `denied` in Section 11.6's automatic-breach sense applies only to Constitutional Standing. A denied Delegated, Emergency, Repair, or Appeal claim is contestable under the ordinary mechanisms named for each (Section 11.7, and — for Repair and Appeal — the governing RFCs in the `RFC-CDP-070` band) without itself generating a further, independent Breach Record.

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

Promoted into Draft v0.6, following review that found the v0.5 recognition model over-corrected in places:

- binding CDP recognition requires valid procedural authority, competence, independence, and record; recognition is not creation, but it is not ambient or self-executing either;
- claims that an answerability relationship exists remain contestable through the Answerability Test; non-recognition is not proof of non-existence, and a sustained claim is not proof that recognition created the relationship;
- the distinction between being answerable *to* an actor (grounding participation rights) and answerable *for* a decision (grounding custodial or official duties);
- Question 4 of the Answerability Test expanded to require an identified obligor, recipient, authority source, and response window;
- Question 5 clarified to test the claim of existence, not to place existence beyond examination;
- Delegated Standing clarified as a genuinely granted capacity to represent or participate, distinct from the underlying answerability relationship it represents, which delegation does not manufacture.

Promoted into Draft v0.7, following a reconnaissance pass (Session 033) that found the v0.6 recognition model conceptually sound but not yet precise enough to implement without inventing policy in code:

- the Standing recognition role's required properties made explicit — bounded, non-self-interested, procedurally authorized, auditable — closing the regress named in Section 11.1 without naming a specific implementation actor (Section 11.5);
- provisional affected-party Standing formalized: a minimally sufficient claim creates provisional Standing sufficient for the first protected act, without waiting on binding recognition (Section 11.4);
- a five-value recognition outcome vocabulary (`recognized | narrowed | deferred | rejected | denied`), with `denied` precisely defined for Section 11.6's automatic Breach Record rule and distinguished from `rejected`, from `narrowed`/`deferred`, and from a claim that never cleared minimal sufficiency (Section 11.8);
- the Standing Record Seed split into four separate, append-only records — Standing Claim, Standing Recognition Determination, Recusal Record, Standing Contest Record — replacing the single mutable seed row (Section 9);
- `RFC-CDP-078` cited directly (Section 3.5) so Relationship Type cannot become a Standing prerequisite;
- `RFC-CDP-075`, which does not yet exist as a drafted RFC, removed from `Depends On` and noted separately as reserved.

Not yet resolved:

- how risk classes determine recusal depth;
- how this model updates lifecycle protocol RFCs;
- how Functional Standing relates to `RFC-CDP-062-HITL-AIITL-Role-Boundaries.md`;
- how implementation profiles enforce projection atomicity;
- which specific actor(s) satisfy the Standing recognition role's four required properties (Section 11.5) for a given implementation — this RFC states the properties, not a name;
- the abuse or anti-flooding threshold referenced in Section 11.4 for provisional affected-party claims is not yet specified.

---

## 15. Summary

Standing determines who may participate.

Recusal determines when participation must be limited.

Standing is the procedural recognition of an answerability relationship that CDP does not create. Existence, recognition, and scope are separate questions, and the Answerability Test is how CDP tells them apart when Standing is contested. Recognition is not creation, but recognition is not ambient either: only an actor or process with authority under this RFC can bind CDP to a determination, and that determination remains open to correction, not immune from it.

Authority capture through participation is a structural governance failure.

Legitimacy by infinite delegation is a constitutional-root failure. CDP resolves it by recognizing standing rather than originating it, so the regress has nothing left to ask.

Standing as unenforceable record is a persistence failure.

CDP must not merely ask whether a decision was reviewed.

It must ask whether the right actors had standing, whether conflicted actors were recused, whether constitutional standing was protected, whether constitutional standing denial automatically enters the Repair plane, whether the standing record was enforceable in time, and whether the process remained genuinely contestable.
