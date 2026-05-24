# RFC-CDP-025 — CDP Persistence Model

Author: Kevin “Andie” Williams  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: May 23, 2026  
Depends On: RFC-CDP-021, RFC-CDP-022, RFC-CDP-023, RFC-CDP-024  
Related: RFC-CDP-002, RFC-CDP-033, RFC-CDP-070, RFC-CDP-090, RFC-CDP-092

## Abstract

This RFC defines the minimum persistence model required to implement the Constitutional Decision Plane (CDP).

It specifies the core database/storage substrate needed to persist, query, replay, validate, and enforce Decision Lifecycle Envelopes, governed records, governed references, payload schemas, controlled vocabularies, lookup/config values, and event history.

The purpose is not to prescribe a single database vendor or full enterprise data model.

The purpose is to prevent CDP protocols from becoming unimplementable because their envelopes, records, gates, repairs, and hashes cannot be queried or joined.

---

## 1. Purpose

CDP now defines several core governance objects and primitives:

- Wire Message Envelope (`RFC-CDP-021`)
- Protocol Payload Schema Registry (`RFC-CDP-022`)
- Decision Lifecycle Envelope (`RFC-CDP-023`)
- Proposal Sufficiency Gate (`RFC-CDP-024`, reserved)
- Anti-Premature-Certainty Principle (`RFC-CDP-002`)
- Standing and Recusal Model (`RFC-CDP-033`)
- Appeals and Contestability Model (`RFC-CDP-070`)

These define the constitutional object model.

This RFC defines the minimum queryable persistence substrate required to implement that object model.

---

## 2. Failure Mode: Protocol Without Queryable Persistence

The failure mode this RFC addresses is **protocol without queryable persistence**.

Protocol without queryable persistence occurs when a governance system defines envelopes, records, gates, challenges, repair hooks, and hashes, but lacks a minimal storage model that can persist, query, join, replay, validate, and enforce them.

This is not merely a storage problem.

A system can persist records as flat files, JSONL, object storage, or document blobs and still fail CDP conformance if it cannot query governance-critical relationships.

Examples:

- a closure-blocking rule cannot be enforced because `repair_refs` and `appeal_refs` are not joinable to their resolution status;
- a governed path hash cannot be verified because `content_hash_at_registration` is not stored adjacent to the current record hash;
- a standing determination cannot be audited because standing records are not queryable by decision and stage;
- an Anti-Premature-Certainty gate result cannot be replayed because it was stored only as an opaque blob;
- a proposal sufficiency decision cannot be inspected because the sufficiency record and evaluator result cannot be joined.

The goal of this RFC is to prevent persistence schema drift from becoming the next form of protocol schema drift.

---

## 3. Design Principles

### 3.1 Queryable Current State

CDP implementations SHOULD maintain current-state tables that make governance enforcement queries efficient and legible.

Current-state tables are the authoritative queryable state for ordinary enforcement and review.

### 3.2 Append-Only Event Trail

CDP implementations MUST maintain an append-only event trail for audit, replay, and dispute resolution.

The event log is not the primary source of current state in Draft v0.1.

It is an audit and replay layer.

### 3.3 JSON-First Governed Records

CDP implementations MAY use JSON-first governed records for MVP implementation.

However, governance-critical fields used for enforcement MUST be promoted into queryable columns.

### 3.4 Controlled Vocabulary Separation

Governance-critical enumerations MUST NOT drift through ungoverned configuration tables.

Open-ended lookup/config values and RFC-defined controlled vocabulary values are separate concerns.

### 3.5 Vendor Neutrality

This RFC describes logical tables and required columns.

SQL examples are normative for table structure and required fields, but implementation details such as exact data types, index names, partitioning, and JSON syntax MAY vary by database or implementation profile.

---

## 4. Minimum Persistence Model

Draft v0.1 defines five core tables plus two vocabulary/config tables.

Core tables:

1. `cdp_decision_envelope`
2. `cdp_governed_record`
3. `cdp_envelope_ref`
4. `cdp_payload_registry`
5. `cdp_event_log`

Vocabulary/config tables:

6. `cdp_lookup`
7. `cdp_controlled_vocabulary`

---

## 5. Table: cdp_decision_envelope

### 5.1 Purpose

`cdp_decision_envelope` stores one row per Decision Lifecycle Envelope.

It preserves the full envelope while promoting governance-critical fields into queryable columns.

### 5.2 Required Columns

```sql
cdp_decision_envelope:
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

### 5.3 Required Queryable Fields

The following MUST be queryable without parsing the full JSON payload:

- `envelope_id`
- `decision_id`
- `decision_type`
- `lifecycle_stage`
- `status`
- `standing_status`
- `repair_status`
- `closure_blocked`
- `governed_path_hash`
- `created_at`
- `updated_at`

### 5.4 Notes

`envelope_json` preserves the canonical envelope object defined in `RFC-CDP-023`.

Queryable columns exist to enforce workflow and governance constraints efficiently.

They MUST NOT silently diverge from the canonical envelope JSON.

If both are stored, implementations MUST define synchronization behavior.

---

## 6. Table: cdp_governed_record

### 6.1 Purpose

`cdp_governed_record` stores governed artifacts referenced by a Decision Lifecycle Envelope.

Examples include:

- proposal sufficiency record;
- Anti-Premature-Certainty gate result;
- proposal record;
- challenge memo;
- standing record for MVP storage;
- appeal record;
- repair record;
- test result;
- adjudication record;
- legitimacy basis record;
- execution record;
- learning artifact.

### 6.2 Required Columns

```sql
cdp_governed_record:
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

### 6.3 Required Queryable Fields

The following MUST be queryable without parsing `record_json`:

- `record_id`
- `decision_id`
- `record_type`
- `record_schema_version`
- `stage`
- `record_status`
- `content_hash`
- `content_hash_algorithm`
- `created_at`
- `updated_at`

### 6.4 JSON-First MVP Rule

Draft v0.1 permits governed record bodies to be stored as JSON-first objects in `record_json`.

However, implementations SHOULD promote fields into typed tables or indexed columns when those fields become governance enforcement paths rather than reporting fields.

Standing determinations are explicitly identified as a likely candidate for promotion in a future RFC revision.

---

## 7. Table: cdp_envelope_ref

### 7.1 Purpose

`cdp_envelope_ref` stores governed references from Decision Lifecycle Envelopes to governed records.

It is the implementation spine of the Governed Path Manifest defined in `RFC-CDP-023`.

### 7.2 Required Columns

```sql
cdp_envelope_ref:
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

### 7.3 Required Queryable Fields

The following MUST be queryable:

- `envelope_id`
- `decision_id`
- `ref_type`
- `ref_id`
- `stage`
- `sequence_position`
- `content_hash_at_registration`
- `registered_at`
- `closure_blocking_flag`

### 7.4 Required Constraints

`cdp_envelope_ref.envelope_id` MUST reference a row in `cdp_decision_envelope`.

`ref_id` SHOULD reference a row in `cdp_governed_record` when the referenced artifact is stored in the local persistence layer.

External references MAY be supported, but their reference type and hash behavior MUST be explicit.

### 7.5 Hash Verification

`content_hash_at_registration` stores the hash of the referenced record at the moment it was registered into the governed path.

This column is required for silent reference mutation detection.

Implementations MUST NOT rely only on current record hash values when verifying governed path integrity.

---

## 8. Table: cdp_payload_registry

### 8.1 Purpose

`cdp_payload_registry` implements the schema registry defined by `RFC-CDP-022`.

It stores named payload families, ownership RFCs, status, and schema definitions.

### 8.2 Required Columns

```sql
cdp_payload_registry:
  id
  payload_type
  payload_status
  owning_rfc
  schema_version
  schema_json
  created_at
  updated_at
```

### 8.3 Required Queryable Fields

The following MUST be queryable:

- `payload_type`
- `payload_status`
- `owning_rfc`
- `schema_version`

### 8.4 APC Gate Result

The payload type `anti_premature_certainty_gate_result` is reserved by `RFC-CDP-022`.

When implemented, it SHOULD be persisted as a governed record in `cdp_governed_record` and typed by `cdp_payload_registry`.

---

## 9. Table: cdp_event_log

### 9.1 Purpose

`cdp_event_log` stores append-only events for audit, replay, and dispute resolution.

### 9.2 Required Columns

```sql
cdp_event_log:
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

### 9.3 Required Queryable Fields

The following MUST be queryable:

- `event_id`
- `decision_id`
- `envelope_id`
- `record_id`
- `event_type`
- `actor_id`
- `event_time`

### 9.4 Insert-Only Rule

`cdp_event_log` MUST be append-only.

After an event is recorded, it MUST NOT be updated or deleted by normal application workflows.

Corrections MUST be represented by additional events, not mutation of prior events.

Implementations SHOULD enforce this rule at the database, storage, or infrastructure layer, not merely in application code.

---

## 10. Table: cdp_lookup

### 10.1 Purpose

`cdp_lookup` stores generic implementation configuration and display values.

It is not the authoritative source for RFC-defined governance-critical enumerations.

### 10.2 Required Columns

```sql
cdp_lookup:
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

### 10.3 Intended Use

Examples:

- display labels;
- feature flags;
- implementation-specific mappings;
- local UI labels;
- non-normative configuration.

### 10.4 Non-Use

`cdp_lookup` MUST NOT be the sole authoritative source for governance-critical enum values such as:

- lifecycle stages;
- decision statuses;
- standing statuses;
- repair statuses;
- protocol act names;
- gate result statuses.

Those belong in `cdp_controlled_vocabulary`.

---

## 11. Table: cdp_controlled_vocabulary

### 11.1 Purpose

`cdp_controlled_vocabulary` stores governance-critical enumerations defined by RFCs.

These values must be queryable, source-attributed, and lockable.

### 11.2 Required Columns

```sql
cdp_controlled_vocabulary:
  id
  domain
  value
  display_name
  description
  source_rfc
  schema_version
  locked
  disabled
  created_at
  updated_at
```

### 11.3 Required Queryable Fields

The following MUST be queryable:

- `domain`
- `value`
- `source_rfc`
- `locked`
- `disabled`

### 11.4 Locking Rule

Governance-critical values SHOULD be locked when defined by an RFC.

Locked values MUST NOT be modified by ordinary runtime configuration workflows.

Changes to locked values SHOULD require RFC update, migration, or explicit implementation-profile override.

### 11.5 Example Domains

Examples include:

- `lifecycle_stage`
- `decision_status`
- `standing_status`
- `repair_status`
- `record_type`
- `payload_type`
- `apc_failure`
- `risk_tier`
- `challenge_type`

---

## 12. Proposal Sufficiency and APC Persistence

### 12.1 Proposal Sufficiency Record

A Proposal Sufficiency Gate evaluation SHOULD persist at least two governed records.

The first is the proposal sufficiency record.

It SHOULD be stored in `cdp_governed_record` with:

```text
record_type: proposal_sufficiency_record
```

It contains the self-check fields such as evidence, alternatives, uncertainty, stakeholder impact, reversibility, and threshold.

Minimum indexed/queryable fields:

- `decision_id`
- `stage`
- `record_type`
- `record_status`
- `content_hash`

### 12.2 Anti-Premature-Certainty Gate Result

The second is the Anti-Premature-Certainty gate result.

It SHOULD be stored in `cdp_governed_record` with:

```text
record_type: anti_premature_certainty_gate_result
```

It contains fields such as:

- `passed`
- `failures`
- `unwaived_failures`
- `waivers`
- `evaluator`
- `evaluated_at`
- `risk_tier`

Minimum indexed/queryable fields:

- `decision_id`
- `record_type`
- `record_status`
- `content_hash`
- `created_at`

If implementations need to query `passed` frequently, they SHOULD promote `passed` into a queryable column or typed table.

### 12.3 Envelope References

Both proposal sufficiency records and APC gate results SHOULD be referenced in `cdp_envelope_ref`.

`closure_blocking_flag` SHOULD be set to `true` when the gate has not passed and no valid exception exists.

---

## 13. Standing Record Gap

Standing determinations are first-class governance controls under `RFC-CDP-033`.

Draft v0.1 permits standing records to be stored as governed records in `cdp_governed_record`.

However, this is an acknowledged enforcement gap.

The query:

> Does this actor have valid standing at this stage of this decision?

is not merely a reporting query.

It is a governance enforcement query.

For production-grade implementation, CDP may require a dedicated `cdp_standing_record` table or standing-specific indexed columns.

This question is deferred to Session 009 and a future RFC-CDP-025 revision.

---

## 14. Normative vs Illustrative SQL

In this RFC, the following are normative:

- table names;
- required columns;
- required queryable fields;
- primary identity columns;
- foreign key from `cdp_envelope_ref` to `cdp_decision_envelope`;
- insert-only behavior for `cdp_event_log`;
- separation between `cdp_lookup` and `cdp_controlled_vocabulary`.

The following are illustrative or implementation-profile-specific:

- exact SQL dialect;
- exact physical data types;
- index names;
- partitioning strategy;
- JSON/JSONB syntax;
- retention policy;
- database vendor;
- storage engine;
- query optimization strategies.

Implementation profiles MAY provide concrete Postgres, SQLite, Redshift, DynamoDB, document-store, lakehouse, or object-storage mappings.

---

## 15. Security and Governance Considerations

CDP persistence stores governance-sensitive information, including:

- affected-party claims;
- standing and recusal records;
- dissent;
- evidence references;
- appeal and repair records;
- APC failures and exceptions;
- actor actions;
- event history;
- governed path hashes.

Implementations SHOULD address:

- access control;
- redaction;
- retention;
- event-log immutability;
- hash verification;
- data minimization;
- culturally appropriate handling;
- affected-party review;
- repair and appeal obligations.

---

## 16. Status of This Draft

Promoted into Draft v0.1:

- protocol without queryable persistence as the failure mode;
- five core tables;
- two vocabulary/config tables;
- JSON-first governed records for MVP;
- event log as audit/replay, not source of truth;
- insert-only event log requirement;
- Proposal Sufficiency and APC persistence pattern;
- standing record table as an open enforcement gap.

Deferred:

- `cdp_standing_record` table design;
- typed governed record tables under query pressure;
- migration scripts;
- database-specific DDL;
- concrete indexing strategy;
- implementation profile mappings.

---

## 17. Summary

CDP requires queryable persistence.

The envelope is the index.

Governed records are the body of evidence.

Envelope references are the governed path manifest in storage form.

The payload registry is the schema contract.

Controlled vocabulary prevents enum drift.

Lookup configuration supports local implementation flexibility.

The event log is the memory.

Without queryable persistence, CDP remains a beautiful protocol suite that cannot reliably enforce its own claims.
