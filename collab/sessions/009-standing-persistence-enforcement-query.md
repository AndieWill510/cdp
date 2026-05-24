# Session 009 Shared Chat: Standing Persistence and Enforcement Query

```text
SESSION: 009-standing-persistence-enforcement-query
DATE_OPENED: 2026-05-23
MODERATOR: Andie
STATUS: promotion-applied
MODE: shared-chat-file
CANON_TARGET: RFC-CDP-025-CDP-Persistence-Model.md; RFC-CDP-033-Standing-and-Recusal-Model.md
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

A standing query that takes too long or requires manual reconstruction is not merely slow.

It is a governance gap.

---

## Current G / C Convergence

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

---

## Turn 001 — 2026-05-23 — Andie / G / C — Session Opening

G and C opened Session 009 around the standing persistence enforcement gap.

C sharpened the failure mode from `standing as opaque record` to `standing as unenforceable record`, including the temporal risk that a slow standing query becomes a governance gap.

---

## Turn 002 — 2026-05-23 — Claude / Sonnet / C — Standing Persistence Challenge Memo

C recommended:

- define a dedicated `cdp_standing_record` table;
- treat it as an enforcement projection over `cdp_governed_record`, not the authoritative artifact;
- keep the canonical standing artifact in `cdp_governed_record`;
- require indexed standing enforcement fields;
- represent recusal with `recusal_required` and `recusal_scope`;
- represent standing types with `standing_type` values aligned to RFC-CDP-033;
- add mandatory indexes for enforcement, contestability window, and emergency standing expiry;
- enforce constitutional standing non-revocation as a database/storage constraint where possible;
- patch both RFC-CDP-025 and RFC-CDP-033.

---

## Turn 003 — 2026-05-23 — Andie / G — Standing Persistence Promotion

Decision 021 approved C's standing persistence design with one G amendment.

G amendment:

```text
projection_status
```

Allowed Draft v0.2 values:

```text
current | stale | rebuild_required | invalid
```

Reason: if `cdp_standing_record` is a projection, the projection needs its own validity state.

### Action Taken

Patched:

```text
rfc/RFC-CDP-025-CDP-Persistence-Model.md
```

Advanced to Draft v0.2.

Added:

- standing as unenforceable record as a specific persistence failure mode;
- `cdp_standing_record` as required enforcement projection;
- projection-not-authoritative rule;
- `projection_status` field;
- standing type and standing status controlled vocabulary hooks;
- mandatory enforcement query;
- three mandatory standing indexes;
- constitutional standing non-revocation constraint;
- emergency standing time-bound constraint;
- standing projection atomicity requirement;
- stage-specific recusal override as known gap.

Patched:

```text
rfc/RFC-CDP-033-Standing-and-Recusal-Model.md
```

Advanced to Draft v0.4.

Added Section 12: Standing Persistence.

Section 12 declares that standing determinations must be persisted as both:

1. a canonical governed artifact; and
2. a queryable enforcement projection.

### Promotion Decision

```text
PROMOTE TO CANON:
- RFC-CDP-025 Draft v0.2 standing enforcement projection
- RFC-CDP-033 Draft v0.4 Standing Persistence bridge

DEFER:
- recusal_stage_override dedicated field
- actor-level audit index
- projection propagation implementation mechanism
- lifecycle protocol standing enforcement integration
```
