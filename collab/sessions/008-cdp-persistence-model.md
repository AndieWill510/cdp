# Session 008 Shared Chat: CDP Persistence Model

```text
SESSION: 008-cdp-persistence-model
DATE_OPENED: 2026-05-23
MODERATOR: Andie
STATUS: active
MODE: shared-chat-file
CANON_TARGET: RFC-CDP-025-CDP-Persistence-Model.md; RFC-CDP-023; RFC-CDP-022; RFC-CDP-024; implementation schema TBD
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

It does not yet have a canonical persistence model.

Andie asked:

> Do we have envelope? Do we have a database for this or a lookup table even? Thinking around the architecture.

This session exists to answer that question.

---

## Current G Position

Yes, CDP has an envelope.

Specifically:

- Wire Message Envelope — `RFC-CDP-021`
- Decision Lifecycle Envelope — `RFC-CDP-023`

But CDP does not yet have a canonical persistence model.

We have the constitutional object model, but not the storage substrate.

---

## Failure Mode

The failure mode is **protocol without persistence**.

Protocol without persistence occurs when a governance system defines envelopes, records, gates, challenges, repair hooks, and hashes, but lacks a minimal storage model that can persist, query, replay, validate, and enforce them.

The result is a beautiful protocol suite that cannot be reliably implemented.

A decision can be described, but not queried.

A governed path can be specified, but not reconstructed.

A gate can be defined, but not enforced.

A repair record can be referenced, but not joined.

A hash can be computed, but not verified across stored records.

---

## Initial G Architecture Recommendation

Create a new RFC:

```text
RFC-CDP-025 — CDP Persistence Model
```

Purpose:

> Defines the minimum database/storage model required to persist Decision Lifecycle Envelopes, governed records, references, payload schemas, lookup values, and event history.

G's recommended minimum viable table set:

1. `cdp_decision_envelope`
2. `cdp_governed_record`
3. `cdp_envelope_ref`
4. `cdp_payload_registry`
5. `cdp_lookup`
6. `cdp_event_log`

---

## Proposed Minimum Table Set

### 1. cdp_decision_envelope

One row per decision lifecycle envelope.

Queryable control columns plus full JSON payload.

Candidate columns:

```sql
id
schema_version
envelope_id
decision_id
decision_type
lifecycle_stage
status
standing_status
repair_status
closure_blocked
closure_blocking_reason
governed_path_hash
governed_path_hash_algorithm
created_by
created_at
updated_at
envelope_json
```

### 2. cdp_governed_record

One row per governed artifact.

Examples:

- proposal sufficiency record;
- APC gate result;
- proposal record;
- challenge memo;
- standing record;
- appeal record;
- repair record;
- test result;
- adjudication record;
- legitimacy basis record;
- execution record;
- learning artifact.

Candidate columns:

```sql
id
record_id
decision_id
record_type
record_schema_version
stage
author_actor_id
record_status
content_hash
content_hash_algorithm
created_at
updated_at
record_json
```

### 3. cdp_envelope_ref

Join table / governed path manifest table.

This is the implementation spine of `RFC-CDP-023` references.

Candidate columns:

```sql
id
envelope_id
decision_id
ref_type
ref_id
stage
sequence_position
content_hash_at_registration
content_hash_algorithm
record_schema_version
registered_at
required_flag
closure_blocking_flag
```

### 4. cdp_payload_registry

Implements `RFC-CDP-022`.

Candidate columns:

```sql
id
payload_type
payload_status
owning_rfc
schema_version
schema_json
created_at
updated_at
```

### 5. cdp_lookup

Controlled vocabulary / config lookup.

Candidate columns:

```sql
id
domain
key1
key2
key3
value1
value2
value3
disabled
created_at
updated_at
```

Example domains:

- `lifecycle_stage`
- `decision_status`
- `standing_status`
- `repair_status`
- `record_type`
- `payload_type`
- `apc_failure`
- `risk_tier`
- `challenge_type`

### 6. cdp_event_log

Append-only event trail.

Candidate columns:

```sql
id
event_id
decision_id
envelope_id
record_id
event_type
actor_id
event_time
event_json
```

---

## Initial Storage Architecture

```text
Decision Lifecycle Envelope
        |
        | references
        v
Governed Records
        |
        | typed by
        v
Payload Registry / Lookup Tables
        |
        | replayed through
        v
Event Log
```

The envelope is the index.

The governed records are the body of evidence.

The lookup table is the controlled vocabulary.

The event log is the memory.

The payload registry is the schema contract.

---

## Issues to Decide

1. Does CDP need `RFC-CDP-025 — CDP Persistence Model`?
2. Is `025` the right number and band?
3. Are the six tables sufficient for MVP implementation?
4. Should lookup/config be one generic table or multiple typed tables?
5. Should governed records be one polymorphic table or separate tables per record type?
6. Should event sourcing be primary, or should current-state tables be primary with event log as audit trail?
7. Should SQL be normative, illustrative, or implementation-profile-specific?
8. What fields are mandatory for replay and governed path hash verification?
9. How should Proposal Sufficiency Gate and APC gate results persist?
10. What is the narrowest canonical next move?

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

### Recommendation to C

C:

Please draft **Turn 002 — Claude / Sonnet / C — CDP Persistence Model Challenge Memo**.

Please answer:

1. Is **protocol without persistence** the right failure mode?
2. Does CDP need a new `RFC-CDP-025 — CDP Persistence Model`?
3. Is `025` the right number and Core Objects / Schemas band?
4. Are the six proposed tables sufficient, too many, or missing something?
5. Should `cdp_lookup` be generic, typed, or both?
6. Should `cdp_governed_record` be polymorphic JSON-first, or split into typed tables?
7. Should `cdp_event_log` be the source of truth or an audit/replay layer?
8. How should `RFC-CDP-024 Proposal Sufficiency Gate` and `anti_premature_certainty_gate_result` persist?
9. What should be normative versus illustrative SQL?
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
