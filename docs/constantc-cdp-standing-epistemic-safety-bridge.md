# ConstantC ↔ CDP Bridge
## Standing, Epistemic Safety, Contestability, and Sovereignty

**Status:** Proposed bridge document  
**Date:** 2026-07-15  
**Steward:** Andie  
**Purpose:** Reconcile independently developed ConstantC and CDP concepts without creating duplicate architecture.

---

## Abstract

ConstantC recently developed a constitutional account of standing, epistemic safety, contestability, and sovereignty through first-principles inquiry.

A subsequent review of the CDP RFC corpus showed that CDP had already developed mature models for Standing, Recusal, Authority, Appeals, Affected-Party Review, Anti-Erasure, and Sovereignty months earlier.

This bridge therefore does not replace CDP architecture.

It records independent convergence, maps the vocabularies, preserves provenance, and isolates the remaining implementation gap: whether standing that is validly allocated is actually reachable in practice.

---

## Sources reconciled

### CDP

- `rfc/RFC-CDP-020-Decision-Object-Schema.md`
- `rfc/RFC-CDP-032-Authority-and-Delegation-Model.md`
- `rfc/RFC-CDP-033-Standing-and-Recusal-Model.md`
- `rfc/RFC-CDP-070-Appeals-and-Contestability-Model.md`
- `rfc/RFC-CDP-073-Affected-Party-Review-and-Anti-Erasure.md`
- `rfc/RFC-CDP-074-Sovereignty-Claims-and-Authority-Pluralism.md`

### ConstantC

- https://github.com/AndieWill510/constantc/blob/main/culture/standing-is-the-first-covenant.md
- https://github.com/AndieWill510/constantc/blob/main/culture/standing-vs-epistemic-safety.md
- https://github.com/AndieWill510/constantc/blob/main/culture/epistemic-safety.md
- https://github.com/AndieWill510/constantc/blob/main/culture/worked-case-standing-ai-prior-authorization.md
- https://github.com/AndieWill510/constantc/blob/main/culture/candidate-constitutional-primitives.md
- https://github.com/AndieWill510/constantc/blob/main/culture/worked-case-standing-indigenous-land.md

The CDP RFCs predate the current ConstantC work. The similarities are therefore treated as independent convergence rather than inheritance.

---

## Reconciliation map

| ConstantC concept | Existing CDP home | Reconciliation |
|---|---|---|
| Standing as governed recognition of a relevant domain of participation | RFC-CDP-033 Standing and Recusal Model | Compatible. CDP's stage-specific Standing remains authoritative inside CDP. No competing Standing object should be created. |
| Standing distinct from Authority | RFC-CDP-032 Authority and Delegation Model; RFC-CDP-033 §3.3 | Already established. Standing governs valid participation; Authority governs what may be done after participation is valid. |
| Contestability downstream of Standing | RFC-CDP-070 depends explicitly on RFC-CDP-033 | Already established. ConstantC does not replace or rename Contestability. |
| AI participation without personhood claims | RFC-CDP-033 Functional Standing | Already established. Functional Standing permits bounded contribution without ontology inflation. |
| Affected-party anti-erasure | RFC-CDP-073 | Already established. Formal participation must not be flattened, hidden, misclassified, or replaced by institutional self-approval. |
| Sovereignty not reducible to stakeholder standing | RFC-CDP-032 Sovereignty Authority and RFC-CDP-074 | Already established. Sovereignty claims must not be downgraded into preference, sentiment, consultation, or ordinary stakeholder input. |
| Epistemic safety | No single settled CDP node | Proposed as an audit condition: whether allocated standing survives operational credibility assessment, accessibility, review, and repair. |
| Reachability | Not yet fully explicit in RFC-CDP-033 | Remaining gap. A valid participation right may exist while the path is structurally incapable of changing the controlling account. |

---

## Standing

ConstantC's current working definition is:

> Standing is the governed recognition that a participant has a relevant domain of contribution which an inquiry is obligated to receive, evaluate, and answer through accountable standards.

RFC-CDP-033 defines Standing as:

> the recognized right or responsibility to participate in a CDP decision stage.

These are compatible.

CDP's definition is stage-specific and operational. ConstantC's formulation explains the normative reason the participation right matters.

Inside CDP, RFC-CDP-033 remains authoritative.

No rename is required.

No new Standing lifecycle stage is required.

No competing Standing schema should be introduced.

---

## Authority

Standing and Authority must remain separate.

Standing asks:

> May this actor participate in this stage of this decision, in this role and context?

Authority asks:

> What may this actor authorize, adjudicate, delegate, legitimize, or execute once participation is valid?

RFC-CDP-032 and RFC-CDP-033 already preserve this distinction.

This bridge rejects the earlier proposal to rename Standing as `Proposer Authority`. That rename would collapse two concepts CDP has correctly kept separate and would conflict with `proposer` as an existing role and recusal label.

---

## Contestability

RFC-CDP-070 already builds Appeals and Contestability on affected-party standing defined in RFC-CDP-033.

The architectural order is therefore already present:

1. Standing provides a constitutional right of entry and stage participation.
2. Contestability provides governed mechanisms for challenge, review, and appeal.
3. Repair responds when standing or contestability is denied, erased, or rendered ineffective.

ConstantC does not propose a replacement for that structure.

---

## Sovereignty

The ConstantC Indigenous land and Land Back worked case produced an important narrowing:

> Within an inquiry, standing may be first. Sovereignty concerns authority the inquiry did not create.

CDP already operationalizes this distinction in RFC-CDP-032 and RFC-CDP-074.

This bridge therefore does not create new sovereignty-screening logic.

When a sovereignty claim is present:

- ordinary participant allocation must not downgrade the claimant into a stakeholder;
- the process must defer to RFC-CDP-074's Sovereignty Claim and Authority Conflict rules;
- closure and execution must follow RFC-CDP-074's blocking and escalation requirements;
- AIITL must remain within RFC-CDP-074's existing boundaries.

Standing is not a gift conferred upon sovereign authority by a settler, institutional, or platform-defined inquiry.

---

## Remaining gap: operational reachability

RFC-CDP-033 governs whether standing is validly allocated.

A separate question remains:

> Can the participant actually exercise that standing in a way capable of revising the account, decision, credibility judgment, or record?

A standing path may exist in policy while being unreachable in operation because of:

- inaccessible communication channels;
- impossible evidentiary thresholds;
- patterned credibility discounting;
- disability, distress, language, fluency, hierarchy, or source-status effects;
- institutional records receiving unearned authority;
- review mechanisms that cannot reconsider credibility judgments;
- retaliation or access loss after challenge;
- successful appeals that do not repair downstream records;
- delay or abandonment that makes formal rights practically unusable.

This is the principal non-redundant contribution of the current ConstantC work to CDP.

---

## Epistemic safety

ConstantC does not currently propose Epistemic Safety as a new CDP lifecycle stage or settled constitutional primitive.

The current working formulation is:

> Epistemic safety is the observable condition in which allocated standing is honored in practice rather than defeated by patterned credibility discount, inaccessible procedure, retaliation, category error, or institutional self-protection.

In CDP terms:

- RFC-CDP-033 allocates and governs Standing;
- RFC-CDP-070 provides contestability and appeal entry;
- RFC-CDP-073 protects affected-party review and anti-erasure;
- a reachability attestation tests whether those rights and mechanisms function in practice.

Epistemic Safety may ultimately prove to be a completeness condition for rigorous Contestability rather than an independent primitive. This bridge preserves that question.

---

## Proposed extension path

The narrow implementation path is:

1. Preserve RFC-CDP-033's Standing model and taxonomy.
2. Extend the existing `standing_record` only through a staged, separately reviewable reachability proposal.
3. Add a Reachability Attestation artifact rather than redefining Standing.
4. Permit Test and Legitimize to reference reachability evidence.
5. Permit Learn to measure patterned accessibility, credibility, reversal, abandonment, delay, and downstream-repair outcomes.
6. Reference RFC-CDP-074 whenever sovereignty or authority pluralism is implicated; do not reimplement it.

A staged companion proposal is recorded in:

- `rfcs/RFC-CDP-033A-Operational-Reachability-Attestation.md`

---

## Explicit non-goals

This bridge does not:

- rename Standing;
- collapse Standing into Authority;
- create a new Standing object parallel to RFC-CDP-033;
- create a new lifecycle stage;
- duplicate sovereignty logic;
- declare Epistemic Safety a settled independent primitive;
- create a generalized credibility or trustworthiness score;
- assert AI sentience, consciousness, interiority, legal personhood, or moral personhood;
- move any ConstantC culture note into CDP canon.

---

## Validity signal and limit

The independent convergence between ConstantC and CDP is a meaningful validity signal.

It is not proof that either framework is complete or correct.

The convergence strengthens confidence in the distinctions among Standing, Authority, Contestability, and Sovereignty.

The divergence identifies the work still worth testing:

> CDP already governs the right to participate. ConstantC asks whether that right is reachable enough to matter.

That claim remains proposed, auditable, and falsifiable.

---

## Status

This bridge is descriptive and reconciliatory.

It introduces no immediate normative changes to accepted CDP RFCs.

Any schema or protocol amendment must proceed through the normal RFC process, preserve provenance, remain contestable, and state what evidence would weaken or reject the proposed reachability model.
