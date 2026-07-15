# Session 019 — RFC-CDP-077 Reopening Authority Challenge

Moderator: Andie  
Status: adjudication-needed  
Date: July 14, 2026  
Canon Target: RFC-CDP-077; RFC-CDP-045; RFC-CDP-092; RFC-CDP-000  
Primary reviewer: C

## Purpose

This session records the first formal challenge review of `RFC-CDP-077-Reopening-Authority-and-Epistemic-Legitimacy.md`.

The RFC remains at **Draft v0.1** pending adjudication and repair.

## Files Read by Reviewer

### CDP orientation

- `CDP_START_HERE.md`
- `C_CDP_PREFERENCES.md`
- `SESSION-HANDOFF.md`
- `AI-MEMORY-BRIEF.md` tail
- `rfc/RFC-CDP-000-Series-Index.md`
- `PROMOTION_PROTOCOL.md`
- `CULTURE.md`

### RFC content

- `rfc/RFC-CDP-077-Reopening-Authority-and-Epistemic-Legitimacy.md` — full
- `rfc/RFC-CDP-070-Appeals-and-Contestability-Model.md` — full
- `rfc/RFC-CDP-073-Affected-Party-Review-and-Anti-Erasure.md` — full
- `rfc/RFC-CDP-076-Repair-Efficacy-and-Verification.md` — full
- `rfc/RFC-CDP-092-Repair-State-Machine.md` — relevant reopening sections
- `rfc/RFC-CDP-045-Legitimize-Protocol.md` — relevant legitimacy-record sections

The reviewer confirmed that cited dependency RFCs 001, 002, 023, 033, 042, 044, and 074 exist.

## Commit Verification

The reviewer cloned the live repository and confirmed:

```text
HEAD = de8f1dc2d117e39dff67cea3dd4f08f66241e395
```

This matches the commit that added RFC-CDP-077.

## Context-Plane Debt Named by Reviewer

- `SESSION-HANDOFF.md` and `AI-MEMORY-BRIEF.md` still reflect Session 016 and do not mention RFC-CDP-070 through RFC-CDP-077.
- No Session 019 record existed before this file.
- `docs/context/README.md`, `LIVING_COVENANT.md`, `collab/COUNCIL_ROLES.md`, and `collab/INDEX.md` were existence-confirmed but not read by the reviewer during the challenge pass.

## Review Disposition

**Hold at Draft v0.1.**

The reviewer did not recommend rejection. The architecture was judged sound, with strong finality, non-goal, and failure-mode sections. Advancement was blocked by unresolved independence semantics, a schema gap created by those semantics, and a reopening-trigger taxonomy collision with RFC-CDP-092.

## Strongest Objection

RFC-CDP-077 requires a `materially independent authority` but does not define what makes an authority materially independent.

Section 8 defines what the authority must be able to do, but not whether independence requires:

- a distinct institution;
- a distinct reporting line;
- a different decision-maker within the same institution;
- a separate authority domain;
- an external reviewer;
- or another controlled independence basis.

The corresponding schema field, `authority_independence_basis`, is free text. An implementation could therefore populate every required field while preserving the same power relationship and still appear compliant.

## Blocking Repairs

### 1. Define Material Independence

RFC-CDP-077 must define operational independence criteria.

The preferred structure is a two-branch rule:

1. **Independent-authority branch** — organizationally, jurisdictionally, or reporting-line distinct authority with no material responsibility for the challenged decision or governing account.
2. **Constrained fallback branch** — where genuine separation is unavailable, disclose non-independence explicitly, prohibit self-certification, require external audit exposure or plural review, preserve dissent, and prevent the fallback from being represented as fully independent.

`authority_independence_basis` should become controlled and queryable rather than free text alone.

### 2. Reconcile Reopening Trigger Taxonomies

RFC-CDP-092 already defines reopening conditions that include:

- `sovereignty_claim_material`
- `recurring_harm_pattern`

These are absent from RFC-CDP-077's `reopening_triggers` enumeration.

RFC-CDP-077 introduces triggers absent from RFC-CDP-092, including:

- `epistemic_exclusion`
- `non_contestable_governing_account`
- `repair_efficacy_failure`
- `legitimacy_basis_failure`

The RFCs must share one controlled vocabulary or explicitly define scope and authority between the two lists.

### 3. Make Defeasible Legitimacy Writable

RFC-CDP-077 states that legitimacy is defeasible and revisable.

RFC-CDP-045 currently defines:

```text
status: granted | denied | escalated
```

No status exists for a previously granted legitimacy determination that is later revoked or superseded after reopening.

RFC-CDP-045 must be patched with writable defeasibility semantics, including the required lineage to the reopening determination.

### 4. Repair the Canonical Series Index

`RFC-CDP-076` and `RFC-CDP-077` exist as committed canonical RFC files but are missing from `rfc/RFC-CDP-000-Series-Index.md` Section 6.8.

The safe repair-band map update already appears in the collaboration promotion queue. It must be completed before either RFC advances.

## Non-Blocking Repairs

- Cross-reference RFC-CDP-077 Section 8 with RFC-CDP-073 Section 14 so the independent-review principle has one lineage rather than two unlinked formulations.
- Import or explicitly reference the epistemic-safety audit methodology and falsification direction rather than leaving epistemic legitimacy entirely as case-by-case narrative judgment.
- Define a time/reliance gradient or implementation hook for increasing reopening thresholds while preserving bounded closure.

## Findings by Review Question

### Epistemic legitimacy

The definition is more operational than the source culture note because it is tied to enumerated triggers, schemas, and a screening pipeline. It remains partly modal and counterfactual. A single case cannot falsify whether a process preserved the possibility that knowledge could matter.

### Repair-plane placement

Reopening mechanics belong in the Repair plane. Defeasible legitimacy is a constitutional amendment to Legitimize and must also be represented directly in RFC-CDP-045.

### Screening threshold

Submission sufficiency is bounded and checkable. Screening relies on `reasonable possibility` and `materially affected` without a named evidentiary standard.

### Finality

The bounded-closure section is strong. Finality may prevail, but only through a reasoned and contestable determination rather than silent default.

### Schemas

The schemas are generally coherent and consistent with existing CDP record patterns. The independence field is the principal queryability gap.

### Standing versus truth

The RFC successfully distinguishes preserving a person's standing as a knower from presuming that person's account is true.

### Procedural compliance risk

A system could populate every schema field, deny reopening, and claim independence through plausible free text while the same authority relationship remains intact.

### Dependency review

- RFC-CDP-070: clean entry-versus-return relationship.
- RFC-CDP-073: no direct conflict; independence principle needs cross-reference and shared lineage.
- RFC-CDP-076: strong integration through repair-efficacy triggers.
- RFC-CDP-045: defeasibility is asserted but not writable.
- RFC-CDP-092: overlapping but inconsistent reopening-trigger enumerations require reconciliation.

## Adjudication Questions for Andie

1. Should the constrained fallback branch count as `independence_limited`, or should it be classified as explicitly non-independent review with additional safeguards?
2. Should reopening triggers live in RFC-CDP-022 as a shared registry, in RFC-CDP-077 as the controlling model, or in RFC-CDP-092 as state-machine events derived from 077?
3. Should RFC-CDP-045 add both `revoked` and `superseded`, or should revocation be represented through a separate legitimacy-revision record while retaining the original status?
4. Should the Series Index repair advance RFC-CDP-000 to Draft v1.4 in the same promotion set?

## Current State

```text
RFC-CDP-077: Draft v0.1 — hold
Session 019: adjudication-needed
Promotion: blocked pending four repairs
```

This challenge record does not itself promote or modify RFC-CDP-077. It preserves the review, blocking findings, and next adjudication points so the repair work is legible and contestable.
