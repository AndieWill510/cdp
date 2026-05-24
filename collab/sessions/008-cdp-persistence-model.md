# Session 008 Shared Chat: CDP Persistence Model

```text
SESSION: 008-cdp-persistence-model
DATE_OPENED: 2026-05-23
MODERATOR: Andie
STATUS: promotion-applied
MODE: shared-chat-file
CANON_TARGET: RFC-CDP-025-CDP-Persistence-Model.md
PURPOSE: Determine whether CDP needs a persistence-model RFC and define the minimum viable database/storage substrate for Decision Lifecycle Envelopes, governed records, references, lookup values, payload schemas, gate results, and event history.
```

## Why This Session Exists

CDP now has several core governance objects and primitives:

- `RFC-CDP-021` — Wire Message Envelope
- `RFC-CDP-022` — Protocol Payload Schema Registry
- `RFC-CDP-023` — Decision Lifecycle Envelope
- `RFC-CDP-024` — Proposal Sufficiency Gate, reserved
- `RFC-CDP-002` — Anti-Premature-Certainty Principle
- `RFC-CDP-033` — Standing and Recusal Model
- `RFC-CDP-070` — Appeals and Contestability Model

The architecture now has the constitutional object model.

It did not yet have a canonical persistence model.

Andie asked:

> Do we have envelope? Do we have a database for this or a lookup table even? Thinking around the architecture.

This session exists to answer that question.

---

## Failure Mode

C sharpened the failure mode to:

> **Protocol without queryable persistence**

A governance system can persist records as flat files, JSONL, object storage, or document blobs and still fail CDP conformance if it cannot query, join, replay, validate, and enforce governance-critical relationships.

The gap is not mere storage.

The gap is queryable enforcement.

---

## Turn 001 — 2026-05-23 — Andie / G — Session Opening

```text
DATE: 2026-05-23
AUTHOR: Andie, recorded by ChatGPT / G
ROLE: moderator / architecture framer
STATUS: active
PURPOSE: Open persistence architecture discussion and propose RFC-CDP-025 CDP Persistence Model.
```

### G Position

CDP needs a persistence model before implementation work gets serious.

Not a heavy enterprise data warehouse.

Not a vendor-specific database prescription.

A minimum viable persistence substrate.

G proposed six tables:

1. `cdp_decision_envelope`
2. `cdp_governed_record`
3. `cdp_envelope_ref`
4. `cdp_payload_registry`
5. `cdp_lookup`
6. `cdp_event_log`

---

## Turn 002 — 2026-05-23 — Claude / Sonnet / C — CDP Persistence Model Challenge Memo

```text
DATE: 2026-05-23
AUTHOR: Claude / Sonnet (claude-sonnet-4-6)
ROLE: challenger / coherence reviewer
STATUS: draft-promoted
PURPOSE: Challenge RFC-CDP-025 persistence model design. Name the failure mode precisely.
```

### 1. Failure Mode

C accepted the failure mode, but sharpened it from **protocol without persistence** to **protocol without queryable persistence**.

Specific failures:

- closure-blocking rules cannot be enforced if repair and appeal refs are not joinable to status;
- governed path hash verification fails if registration-time hashes are not stored adjacent to current record hashes;
- standing cannot be audited if standing records are not queryable by decision and stage;
- APC gate results cannot be replayed if stored only as opaque blobs.

### 2. Need for RFC-CDP-025

C agreed that CDP needs `RFC-CDP-025 — CDP Persistence Model`.

Reason:

Without it, implementers will make different schema decisions, and persistence schema drift becomes the next protocol schema drift.

### 3. Number and Band

C agreed that `025` is the correct number and that the Core Objects and Schemas band (`020–029`) is correct.

### 4. Table Set

C accepted five core tables:

- `cdp_decision_envelope`
- `cdp_governed_record`
- `cdp_envelope_ref`
- `cdp_payload_registry`
- `cdp_event_log`

C challenged a single generic `cdp_lookup` table as too broad for governance-critical vocabulary.

Recommendation:

- keep `cdp_lookup` for open-ended config;
- add `cdp_controlled_vocabulary` for RFC-defined governance-critical enums.

### 5. Standing Record Gap

C named a real gap:

```text
cdp_standing_record
```

The query:

> Does this actor have valid standing at this stage of this decision?

is not merely a reporting query.

It is a governance enforcement query.

C recommended not deferring this beyond Session 009.

### 6. Governed Record Shape

C accepted JSON-first governed records for MVP, with mandatory queryable columns:

- `record_type`
- `stage`
- `content_hash`

### 7. Event Log Role

C agreed with G's hybrid model:

- current-state tables are authoritative queryable state;
- `cdp_event_log` is append-only audit/replay layer;
- event log is not the source of truth in Draft v0.1.

### 8. Proposal Sufficiency and APC Persistence

C recommended two governed records:

1. `proposal_sufficiency_record`
2. `anti_premature_certainty_gate_result`

These are separate because they are produced by different actors at different times.

### 9. Normative vs Illustrative SQL

C recommended that table names, required columns, required queryable fields, key constraints, and event-log insert-only behavior be normative.

SQL dialect, exact index names, partitioning, JSONB syntax, and optimization details remain implementation-profile concerns.

---

## Turn 003 — 2026-05-23 — Andie / G — RFC-CDP-025 Promotion

```text
DATE: 2026-05-23
AUTHOR: Andie, recorded by ChatGPT / G
ROLE: moderator / canon promotion recorder
STATUS: adjudicated-and-promoted
PURPOSE: Record approval and promotion of RFC-CDP-025 Draft v0.1.
```

### Decision 020

Approved.

### G Position

G accepted the `cdp_standing_record` gap but deferred its design to Session 009.

Reason:

Standing is constitutional. It should not be jammed into the persistence RFC casually like a utility table.

### Action Taken

Created:

```text
rfc/RFC-CDP-025-CDP-Persistence-Model.md
```

Status:

```text
Draft v0.1
```

Promoted into Draft v0.1:

- protocol without queryable persistence as the failure mode;
- five core tables;
- two vocabulary/config tables;
- JSON-first governed records for MVP;
- event log as audit/replay, not source of truth;
- insert-only event log requirement;
- Proposal Sufficiency and APC persistence pattern;
- standing record table as an open enforcement gap.

### Promotion Decision

```text
PROMOTE TO CANON:
- RFC-CDP-025 CDP Persistence Model Draft v0.1

PROMOTE WITH OPEN QUESTIONS:
- cdp_standing_record table design
- typed governed record tables under query pressure
- migration scripts
- database-specific DDL
- implementation profile mappings

DEFER:
- cdp_standing_record to Session 009
- concrete index strategy
- implementation migrations
```

---

## Promotion Decision

```text
PROMOTE TO CANON:
- RFC-CDP-025 CDP Persistence Model Draft v0.1

DEFER:
- cdp_standing_record design to Session 009
- typed governed record tables under query pressure
- database-specific DDL and implementation profiles
```
