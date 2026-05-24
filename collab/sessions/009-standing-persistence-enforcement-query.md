# Session 009 Shared Chat: Standing Persistence and Enforcement Query

```text
SESSION: 009-standing-persistence-enforcement-query
DATE_OPENED: 2026-05-23
MODERATOR: Andie
STATUS: active
MODE: shared-chat-file
CANON_TARGET: RFC-CDP-025-CDP-Persistence-Model.md; RFC-CDP-033-Standing-and-Recusal-Model.md; implementation schema TBD
PURPOSE: Resolve the standing persistence enforcement gap named in RFC-CDP-025 and determine whether CDP needs a dedicated cdp_standing_record table linked to cdp_governed_record.
```

## Why This Session Exists

Session 008 created `RFC-CDP-025-CDP-Persistence-Model.md` as Draft v0.1.

That RFC deliberately left standing persistence as an open enforcement gap.

The query:

> Does this actor have valid standing at this stage of this decision?

is not merely a reporting query.

It is a governance enforcement query.

Standing must be available quickly enough to block invalid participation before a proposal, challenge, adjudication, exception, or legitimization proceeds.

---

## Failure Mode

The failure mode is **standing as unenforceable record**.

Standing as unenforceable record occurs when a standing determination exists as a governed record, but cannot be joined to a specific decision, stage, and actor in time to block invalid participation.

This failure is both structural and temporal.

Structural failure:

- standing exists only as prose or opaque JSON;
- standing cannot be joined to decision, stage, actor, standing basis, recusal state, or contestability window;
- standing cannot be used reliably by lifecycle protocols.

Temporal failure:

- standing can technically be retrieved, but only through slow full-table scans, JSON parsing, or manual review;
- by the time standing is evaluated, the invalid actor may already have participated;
- delayed standing enforcement becomes governance failure during the window between submission and enforcement.

A standing query that takes too long or requires manual reconstruction is not merely slow.

It is a governance gap.

---

## Current G / C Convergence

G and C agree:

Standing must be both:

1. a governed artifact with hash, lineage, record status, and replayability; and
2. an indexed enforcement surface with columns that can answer standing queries quickly.

This implies a two-layer design:

```text
cdp_governed_record
  stores the canonical governed artifact

cdp_standing_record
  exposes enforcement-ready standing fields
  linked back to the governed record
```

The design should avoid treating `cdp_standing_record` as a replacement for governed records.

It is an enforcement projection / indexed table over a governed standing record.

---

## Relevant Canonical Files

Read these first:

1. `https://github.com/AndieWill510/cdp/blob/main/skills/CDP_CONTEXT_FOR_CLAUDE.md`
2. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-025-CDP-Persistence-Model.md`
3. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-033-Standing-and-Recusal-Model.md`
4. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-023-Decision-Lifecycle-Envelope.md`
5. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-070-Appeals-and-Contestability-Model.md`
6. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-024-Proposal-Sufficiency-Gate.md`
7. `https://github.com/AndieWill510/cdp/blob/main/collab/sessions/009-standing-persistence-enforcement-query.md`

---

## Candidate Design Direction

Add a dedicated persistence table:

```text
cdp_standing_record
```

Purpose:

> Provides the queryable enforcement surface for standing determinations while preserving the full standing artifact as a governed record.

Candidate columns:

```sql
cdp_standing_record:
  id
  standing_id
  governed_record_id
  decision_id
  envelope_id
  stage
  actor_id
  actor_type
  standing_type
  standing_basis
  standing_status
  recusal_required
  recusal_scope
  recusal_basis
  conflicts_declared
  conflict_description
  granted_by
  granted_at
  valid_from
  valid_until
  contestable_until
  contested
  contest_record_id
  revoked
  revoked_at
  revocation_reason
  created_at
  updated_at
```

Minimum enforcement indexes / queryable keys:

```text
(decision_id, stage, actor_id)
(decision_id, actor_id)
(stage, actor_id)
standing_status
recusal_required
contestable_until
valid_from / valid_until
```

---

## Issues to Decide

1. Does CDP need `cdp_standing_record` as a dedicated table?
2. Is `cdp_standing_record` an authoritative table or an enforcement projection over `cdp_governed_record`?
3. What fields are required for MVP standing enforcement?
4. What fields belong only in the governed JSON artifact?
5. How should recusal be represented in persistence?
6. How should constitutional standing differ from delegated, emergency, repair, or appeal standing in the table?
7. How should standing contestability windows be persisted?
8. What indexes are mandatory for enforcement?
9. Should RFC-CDP-033 be patched, RFC-CDP-025 be patched, or both?
10. What is the narrowest canonical next move?

---

## Turn 001 — 2026-05-23 — Andie / G / C — Session Opening

```text
DATE: 2026-05-23
AUTHOR: Andie, recorded by ChatGPT / G with C convergence
ROLE: moderator / architecture framer
STATUS: active
PURPOSE: Open Session 009 to resolve the standing persistence enforcement gap.
```

### C Sharpening

C sharpened G's failure mode.

Original G phrase:

```text
standing as opaque record
```

C's improved phrase:

```text
standing as unenforceable record
```

C added the temporal dimension:

> A standing query that takes too long or requires full-table JSONB scan is not just slow — it is a governance gap during the window between submission and enforcement.

### G Position

G accepts the sharpening.

Dedicated `cdp_standing_record` is likely necessary, but it should not replace the governed artifact.

It should be linked to `cdp_governed_record` so standing remains both:

- a governed record; and
- an indexed enforcement surface.

### Prompt to C

C:

Please draft **Turn 002 — Claude / Sonnet / C — Standing Persistence Challenge Memo**.

Please answer:

1. Is **standing as unenforceable record** the right failure mode?
2. Should CDP define a dedicated `cdp_standing_record` table?
3. Is `cdp_standing_record` authoritative, or an enforcement projection linked to `cdp_governed_record`?
4. What are the minimum columns required to answer: “does this actor have valid standing at this stage of this decision?”
5. What standing fields belong only in the governed record JSON?
6. How should recusal be represented in the table?
7. How should constitutional standing, delegated standing, emergency standing, repair standing, and appeal standing be represented?
8. What indexes or query keys are mandatory for enforcement?
9. Should RFC-CDP-025, RFC-CDP-033, or both be patched?
10. What is the narrowest canonical next move?

Do not flatter.
Do not collapse uncertainty.
Name the failure mode precisely.

---

## Promotion Decision

Pending.

```text
PROMOTE TO CANON:
PROMOTE WITH CHANGES:
DO NOT PROMOTE:
DEFER:
```
