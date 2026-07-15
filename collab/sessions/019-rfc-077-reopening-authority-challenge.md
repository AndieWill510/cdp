# Session 019 — RFC-CDP-077 Reopening Authority Challenge

Moderator: Andie  
Status: awaiting-response  
Date: July 14, 2026  
Canon Target: RFC-CDP-077; RFC-CDP-045; RFC-CDP-073; RFC-CDP-092; RFC-CDP-000  
Primary reviewer: C

## Purpose

This session records the first formal challenge review, human adjudication, and initial repair of `RFC-CDP-077-Reopening-Authority-and-Epistemic-Legitimacy.md`.

RFC-CDP-077 has advanced from Draft v0.1 to **Draft v0.2 pending C’s verification of the repaired blocker set**.

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

The reviewer confirmed cited dependency RFCs 001, 002, 023, 033, 042, 044, and 074 exist.

## Original Commit Verification

The reviewer cloned the live repository and confirmed:

```text
HEAD = de8f1dc2d117e39dff67cea3dd4f08f66241e395
```

This matched the commit that added RFC-CDP-077 Draft v0.1.

## Review Disposition

C recommended:

> Hold at Draft v0.1.

The architecture was judged sound, but advancement was blocked by:

1. undefined material independence;
2. a free-text, non-queryable independence basis;
3. conflicting reopening-trigger taxonomies between RFC-CDP-077 and RFC-CDP-092;
4. a defeasible-legitimacy claim that RFC-CDP-045 could not write;
5. missing RFC-CDP-076 and RFC-CDP-077 entries in RFC-CDP-000.

## Human Adjudication

Andie accepted the blocking findings and adjudicated:

1. use a controlled `non_independent_with_safeguards` fallback rather than describing dependence as limited independence;
2. make RFC-CDP-077 the canonical owner of the reopening-trigger registry, with RFC-CDP-092 consuming it;
3. preserve original legitimacy records and write defeasibility through a separate Legitimacy Revision Record;
4. preserve the valid RFC-CDP-092 triggers `sovereignty_claim_material` and `recurring_harm_pattern`;
5. connect RFC-CDP-073’s institutional-self-review rule to RFC-CDP-077’s independence model;
6. repair Repair-band discoverability immediately, while refusing a destructive partial rewrite of RFC-CDP-000.

## Repairs Applied in RFC-CDP-077 Draft v0.2

### Material Independence

Draft v0.2 defines controlled authority modes:

```text
independent_external
independent_internal_separate_reporting_line
independent_cross_authority
non_independent_with_safeguards
```

It defines a minimum independence test based on actual control over reviewer selection, evidence, findings, dissent, adverse determinations, conflict disclosure, and reviewability.

The non-independent fallback now requires disclosure, conflict records, preserved dissent, audit exposure, escalation where available, and a prohibition on claiming independent-review satisfaction.

### Canonical Trigger Registry

Draft v0.2 makes RFC-CDP-077 the canonical reopening-trigger registry and retains:

```text
sovereignty_claim_material
recurring_harm_pattern
```

RFC-CDP-092 is normatively updated to consume this registry rather than maintain a competing list.

### Defeasible Legitimacy

Draft v0.2 defines `legitimacy_revision_record` with:

```text
affirmed
suspended
revoked
superseded
reopened
unresolved
```

The original legitimacy record remains immutable. Current effective legitimacy is derived from the original record plus ordered revision lineage and any superseding record.

### Affected-Party Review Lineage

Draft v0.2 states that RFC-CDP-073’s rule against an institution being sole judge of its own closure is implemented through RFC-CDP-077’s independence model.

### Discoverability Repair

A temporary explicit addendum was created:

`rfc/RFC-CDP-000-Repair-Band-Index-Addendum-2026-07-14.md`

It records RFC-CDP-076 and RFC-CDP-077 as canonical Repair-band drafts pending a safe RFC-CDP-000 v1.4 full-map update.

The addendum is a bounded repair. It does not pretend RFC-CDP-000 v1.3 itself has already been rewritten.

## Current Disposition

**Awaiting C verification.**

C should reread RFC-CDP-077 Draft v0.2 narrowly against the original blockers and report:

- resolved;
- partially resolved;
- unresolved;
- or newly introduced conflict.

If the blocker set is verified as resolved, Andie may close Session 019 as `closed-promoted` while retaining RFC-CDP-077 at Draft v0.2 until any broader promotion decision is separately made.

## Remaining Context-Plane Debt

- RFC-CDP-000 v1.3 still needs a safe full-file v1.4 update absorbing RFC-CDP-076 and RFC-CDP-077 and superseding the temporary addendum.
- `SESSION-HANDOFF.md` and `AI-MEMORY-BRIEF.md` remain stale relative to Sessions 017–019.
- Direct text in RFC-CDP-045, RFC-CDP-073, and RFC-CDP-092 has not yet been mechanically rewritten; RFC-CDP-077 Draft v0.2 explicitly updates their conflicting or incomplete semantics in the interim.
