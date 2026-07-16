# ConstantC ↔ CDP Bridge
## Standing, Epistemic Safety, Participation Integrity, Contestability, and Sovereignty

**Status:** Active reconciliation document  
**Date:** 2026-07-16  
**Steward:** Andie  
**Purpose:** Map independently developed ConstantC concepts onto canonical CDP architecture without duplicate schemas or ontology drift.

---

## Abstract

ConstantC developed a constitutional account of standing, epistemic safety, contestability, and sovereignty through first-principles inquiry.

A later review of the CDP RFC corpus showed that CDP had already developed mature models for Standing, Recusal, Authority, Appeals, Affected-Party Review, Anti-Erasure, and Sovereignty months earlier.

The convergence is real, but it does not justify duplicate architecture.

This bridge records the reconciliation and identifies the canonical CDP implementation:

> **RFC-CDP-034 — Participation Integrity Attestation**

Participation Integrity is now the CDP protocol term for whether validly allocated Standing remains intact through entry, representation, evaluation, revision, review, and repair.

Operational Reachability is one required dimension of Participation Integrity.

---

## Sources reconciled

### CDP

- `rfc/RFC-CDP-020-Decision-Object-Schema.md`
- `rfc/RFC-CDP-032-Authority-and-Delegation-Model.md`
- `rfc/RFC-CDP-033-Standing-and-Recusal-Model.md`
- `rfc/RFC-CDP-034-Participation-Integrity-Attestation.md`
- `rfc/RFC-CDP-043-Test-Protocol.md`
- `rfc/RFC-CDP-044-Adjudicate-Protocol.md`
- `rfc/RFC-CDP-045-Legitimize-Protocol.md`
- `rfc/RFC-CDP-047-Record-Protocol.md`
- `rfc/RFC-CDP-048-Learn-Protocol.md`
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

The CDP RFCs predate the current ConstantC work. The similarities are treated as independent convergence rather than inheritance.

---

## Canonical reconciliation map

| ConstantC concept | Canonical CDP home | Reconciliation |
|---|---|---|
| Standing as governed recognition of participation | RFC-CDP-033 | Compatible. CDP's stage-specific Standing remains authoritative. |
| Standing distinct from Authority | RFC-CDP-032 and RFC-CDP-033 §3.3 | Already established. Standing governs participation; Authority governs what may be done once participation is valid. |
| Contestability downstream of Standing | RFC-CDP-070 | Already established through explicit dependency on RFC-CDP-033. |
| AI participation without personhood claims | RFC-CDP-033 Functional Standing | Already established without ontology inflation. |
| Affected-party anti-erasure | RFC-CDP-073 | Already established. Presence, meaning, authority context, and dissent must not be flattened or replaced by institutional self-approval. |
| Sovereignty not reducible to stakeholder standing | RFC-CDP-032 and RFC-CDP-074 | Already established. Sovereignty claims must not be downgraded into preference, sentiment, consultation, or ordinary stakeholder input. |
| Epistemic safety | ConstantC culture language | Not imported as a separate CDP lifecycle stage or primitive. |
| Participation Integrity | RFC-CDP-034 | Canonical CDP artifact and cross-cutting governance property. |
| Operational Reachability | RFC-CDP-034 dimension | Measures whether materially similar participants can actually use the governed path. |

---

## Standing

RFC-CDP-033 remains authoritative inside CDP.

Standing answers:

> May this actor participate in this stage of this decision, in this role and context?

No rename is required.

No new Standing stage is required.

No competing Standing object is permitted.

The earlier proposal to rename Standing as `Proposer Authority` is rejected because it would collapse concepts CDP has correctly kept separate.

---

## Participation Integrity

Participation Integrity answers:

> **Did the decision process preserve the integrity of this participant's valid Standing from entry through representation, evaluation, revision, review, and repair?**

It includes:

- allocation integrity;
- entry integrity;
- representation integrity;
- evaluation integrity;
- revision integrity;
- review integrity;
- repair integrity;
- operational reachability;
- sovereignty and authority integrity.

A path may be reachable while participation integrity still fails—for example, when testimony is successfully submitted but inaccurately summarized, categorically discounted, or prevented from revising the controlling account.

Participation Integrity therefore cannot be reduced to accessibility alone.

---

## Relationship to ConstantC epistemic safety

ConstantC's working concept of epistemic safety is not installed in CDP as a separate architecture node.

Within CDP, the relevant concerns are operationalized through:

- Standing;
- Participation Integrity;
- Contestability;
- Anti-Erasure;
- Record;
- Learn;
- Repair.

The bridge preserves the possibility that epistemic safety is a completeness condition for rigorous contestability rather than a separate primitive.

CDP does not need to settle that culture-level question to enforce Participation Integrity.

---

## Sovereignty

The ConstantC Indigenous land and Land Back case produced a necessary narrowing:

> Within an inquiry, Standing may be first. Sovereignty concerns authority the inquiry did not create.

CDP already operationalizes this distinction in RFC-CDP-032 and RFC-CDP-074.

RFC-CDP-034 does not create a competing sovereignty screen.

It records whether a Sovereignty Claim or Authority Conflict is present and whether the process properly deferred to the authoritative RFCs.

A sovereign authority must not be converted into:

- an ordinary stakeholder;
- an evidence source with a weight;
- consultation feedback;
- sentiment;
- preference;
- a participant whose authority exists only because the inquiry granted it Standing.

Participation Integrity cannot cure missing jurisdiction or illegitimate authority.

---

## Protocol effects

RFC-CDP-034 is canonical in `rfc/` and integrates Participation Integrity into the existing lifecycle without creating a new stage.

The current implementation path is:

1. RFC-CDP-033 allocates and governs Standing.
2. RFC-CDP-034 defines the Participation Integrity Attestation.
3. RFC-CDP-043 tests Participation Integrity and Operational Reachability.
4. RFC-CDP-044 adjudicates Standing, Authority, evidence, credibility, correctness, Participation Integrity, and Sovereignty as distinct questions.
5. RFC-CDP-045 consumes required Participation Integrity evidence at Legitimize.
6. RFC-CDP-047 preserves the attestation, underlying records, exceptions, uncertainty, and repair references.
7. RFC-CDP-048 learns from patterned participation-integrity failures without creating generalized trustworthiness scores.
8. RFC-CDP-070 permits Participation Integrity claims to enter Appeal and Contestability without conditioning the constitutional right of entry.
9. RFC-CDP-073 governs related affected-party review and anti-erasure failures.
10. RFC-CDP-074 remains authoritative for Sovereignty Claims and Authority Conflicts.

---

## Explicit boundaries

This reconciliation does not:

- rename Standing;
- collapse Standing into Authority;
- create a new lifecycle stage;
- duplicate sovereignty logic;
- create `relational epistemic safety` as a CDP node;
- create a generalized credibility or trustworthiness score;
- assert AI sentience, consciousness, interiority, legal personhood, or moral personhood;
- treat the existence of an attestation as proof of integrity;
- treat Participation Integrity as proof of decision correctness.

---

## Load-bearing formulation

> **Standing allocates participation. Participation Integrity tests whether participation remained real. Contestability challenges failure. Anti-Erasure preserves contribution, authority context, and dissent. Repair restores what the process damaged. Sovereignty remains authority the inquiry did not create.**

The independent convergence between ConstantC and CDP strengthens confidence in this architecture.

It does not make the architecture immune from challenge.
