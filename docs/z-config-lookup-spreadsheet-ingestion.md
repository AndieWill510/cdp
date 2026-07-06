# Spreadsheet Ingestion Contract for `z_config_lookup`

Status: Demo ingestion contract  
Scope: Sample Decision Register spreadsheet ingestion into current control-plane lookup schema  
Audience: first-pass implementers, test authors, attorney-facing demo builders  

---

## 1. Purpose

This document defines the spreadsheet format and ingestion process for the first sample Decision Register ingestion into the CDP control plane using the current `z_config_lookup`-style Postgres shape.

The current target table shape is intentionally small:

```text
z_config_lookup
- domain
- key1
- value1
- key2
- value2
- key3
- value3
- created
```

This means the first ingestion must stay simple.

Do not design the spreadsheet as if the database already has a rich Decision Register table.

Do not add columns to the spreadsheet unless the ingestion code explicitly ignores them or the database schema has changed.

For this demo, the spreadsheet represents one decision per row using four logical fields plus a created date:

1. `domain`
2. `key1/value1`
3. `key2/value2`
4. `key3/value3`
5. `created`

`key1/value1`, `key2/value2`, and `key3/value3` are paired fields. They are treated as three named facts about the decision.

---

## 2. Design posture

This is a deliberately constrained ingestion contract.

The purpose is to prove that a simple spreadsheet can be turned into structured control-plane records.

The purpose is not to ingest the whole attorney-facing Decision Register yet.

The attorney-facing record may eventually care about fields such as:

- permission source type;
- permission source ID;
- human approval requirement;
- human approver ID;
- evidence references;
- policy references;
- tool used;
- audit record reference.

Those are important for the future governed record.

They are not part of this first spreadsheet ingestion unless they are encoded into one of the three key/value pairs by a later profile.

For now: keep the ingestion stupid simple.

---

## 3. Required spreadsheet columns

The spreadsheet must contain exactly these required columns for v0.1 ingestion:

```text
domain
key1
value1
key2
value2
key3
value3
created
```

Column names must be lowercase snake_case exactly as shown.

The first row must be the header row.

Each subsequent row is one decision clause record.

The ingestion code may accept `.xlsx` or `.csv`, but tests should begin with `.csv` because CSV is easier to diff, fixture, and validate.

---

## 4. Field meanings

### 4.1 `domain`

`domain` identifies the registry, demo, or bounded decision set.

Recommended format:

```text
decision_register:<registry_name>:<decision_number>
```

Example:

```text
decision_register:sample_attorney_demo:dec_001
```

Why include the decision number in `domain`?

Because the current `z_config_lookup` shape has no dedicated `decision_id` column.

For the demo, the decision identifier must live somewhere predictable.

Using the final segment of `domain` gives the ingestion code a stable way to derive `decision_id` without adding a column the current schema does not have.

Parsing rule:

```text
decision_id = final colon-delimited segment of domain
```

Example:

```text
domain = decision_register:sample_attorney_demo:dec_001
decision_id = dec_001
```

If the domain does not contain at least three colon-delimited segments, the row should fail validation.

### 4.2 `key1/value1`: antecedent

`key1/value1` captures the antecedent: the condition, prior event, trigger, dependency, or context that made the decision relevant.

For v0.1, `key1` should usually be:

```text
antecedent
```

`value1` should contain a short plain-language antecedent.

Examples:

```text
key1 = antecedent
value1 = identity verification passed
```

```text
key1 = antecedent
value1 = prior decision dec_001 recommended review
```

```text
key1 = antecedent
value1 = claim amount exceeded auto-approval threshold
```

If there is no known antecedent, use:

```text
key1 = antecedent
value1 = none_supplied
```

Do not leave `value1` blank.

Blank means the spreadsheet is incomplete.

`none_supplied` means the record affirmatively says no antecedent was supplied.

That distinction matters.

### 4.3 `key2/value2`: subject

`key2/value2` captures the subject: the actor that made, recommended, blocked, escalated, or recorded the decision.

For v0.1, `key2` should usually be:

```text
subject
```

`value2` should identify the actor in a stable, boring format.

Recommended format:

```text
<actor_type>:<actor_id>
```

Allowed `actor_type` values for v0.1:

```text
agent
human
system
institution
unknown
```

Examples:

```text
agent:claims_review_agent
human:user_442
system:workflow_engine
institution:review_board
unknown:unknown
```

If the subject is unknown, use:

```text
key2 = subject
value2 = unknown:unknown
```

Do not leave it blank.

### 4.4 `key3/value3`: predicate

`key3/value3` captures the predicate: the decision, recommendation, or action.

For v0.1, `key3` should usually be:

```text
predicate
```

`value3` should use a simple action phrase.

Recommended format:

```text
<verb>:<object_type>:<object_id>
```

Examples:

```text
recommend_approval:claim:claim_9981
deny_access:access_request:access_7731
escalate_review:claim:claim_9982
create_task:review_task:task_1001
```

The predicate must name what happened.

Do not hide the whole decision in vague text such as:

```text
decision made
processed
handled
completed
```

Those are not useful decision predicates.

### 4.5 `created`

`created` is the date or timestamp the decision record was created or captured for ingestion.

Preferred format:

```text
YYYY-MM-DDTHH:MM:SSZ
```

Example:

```text
2026-07-06T18:42:11Z
```

Acceptable date-only fallback:

```text
YYYY-MM-DD
```

Example:

```text
2026-07-06
```

If date-only is provided, the ingestion code should either:

1. store it as the date with midnight UTC, or
2. store it as a date if the database column is date-only.

The chosen behavior must be explicit in unit tests.

---

## 5. Minimal sample spreadsheet

CSV fixture:

```csv
domain,key1,value1,key2,value2,key3,value3,created
decision_register:sample_attorney_demo:dec_001,antecedent,claim submitted,subject,agent:claims_review_agent,predicate,recommend_approval:claim:claim_9981,2026-07-06T18:42:11Z
decision_register:sample_attorney_demo:dec_002,antecedent,identity verification failed,subject,agent:access_agent,predicate,deny_access:access_request:access_7731,2026-07-06T18:44:09Z
decision_register:sample_attorney_demo:dec_003,antecedent,claim amount exceeded auto-approval threshold,subject,agent:claims_review_agent,predicate,escalate_review:claim:claim_9982,2026-07-06T18:45:33Z
decision_register:sample_attorney_demo:dec_004,antecedent,prior decision dec_003 escalated claim,subject,human:user_442,predicate,approve_review:claim:claim_9982,2026-07-06T18:52:10Z
```

This fixture should be enough to test:

- header validation;
- required fields;
- parsing of decision IDs from `domain`;
- actor parsing from `value2`;
- predicate parsing from `value3`;
- created-date parsing;
- insert into `z_config_lookup`;
- retrieval by domain prefix;
- reconstruction of plain-language rows.

---

## 6. Spreadsheet-to-database mapping

Each spreadsheet row maps directly into one `z_config_lookup` row.

| Spreadsheet column | Database column | Required | Notes |
|---|---|---:|---|
| `domain` | `domain` | yes | Contains registry and derived decision ID |
| `key1` | `key1` | yes | Usually `antecedent` |
| `value1` | `value1` | yes | Antecedent value or `none_supplied` |
| `key2` | `key2` | yes | Usually `subject` |
| `value2` | `value2` | yes | Actor value, e.g. `agent:claims_review_agent` |
| `key3` | `key3` | yes | Usually `predicate` |
| `value3` | `value3` | yes | Action/object value, e.g. `recommend_approval:claim:claim_9981` |
| `created` | `created` | yes | ISO timestamp or date |

No other spreadsheet columns should be ingested in v0.1.

If the spreadsheet contains extra columns, the ingestion code should either:

1. reject the spreadsheet with a clear error, or
2. ignore extra columns with a logged warning.

For unit tests, choose one behavior and make it explicit.

Recommendation: reject extra columns for v0.1 to reduce schema drift.

---

## 7. Ingestion process

The ingestion process should be boring and deterministic.

### Step 1: Load the spreadsheet

Input may be CSV first, XLSX later.

For CSV:

- read with UTF-8 encoding;
- preserve strings as strings;
- do not auto-convert IDs into numbers;
- trim leading/trailing whitespace;
- preserve internal spaces.

For XLSX:

- read the first worksheet unless a worksheet name is explicitly provided;
- require the same header row;
- treat all cells as strings except `created`, which may be parsed as date/time.

### Step 2: Validate headers

Expected header list:

```text
domain,key1,value1,key2,value2,key3,value3,created
```

Validation should fail when:

- a required column is missing;
- a required column is misspelled;
- duplicate columns exist;
- column names differ by case, such as `Domain` instead of `domain`.

### Step 3: Normalize row values

For each row:

- trim leading and trailing whitespace;
- convert empty strings to validation errors;
- preserve case inside values unless a field has a controlled vocabulary;
- normalize controlled vocabulary values to lowercase snake_case.

Controlled fields for v0.1:

```text
key1
key2
key3
actor_type segment of value2
```

Expected default keys:

```text
key1 = antecedent
key2 = subject
key3 = predicate
```

### Step 4: Validate row structure

A row is valid when:

1. `domain` is present.
2. `domain` starts with `decision_register:`.
3. `domain` has at least three colon-delimited segments.
4. The final domain segment is a non-empty decision ID.
5. `key1` equals `antecedent`.
6. `value1` is non-empty.
7. `key2` equals `subject`.
8. `value2` follows `<actor_type>:<actor_id>`.
9. `actor_type` is one of `agent`, `human`, `system`, `institution`, `unknown`.
10. `actor_id` is non-empty.
11. `key3` equals `predicate`.
12. `value3` follows `<verb>:<object_type>:<object_id>`.
13. `verb`, `object_type`, and `object_id` are non-empty.
14. `created` parses as an allowed date or timestamp.

### Step 5: Derive helper values for tests and logs

The database may not store these as separate columns yet, but the ingestion code may derive them for validation, unit tests, logging, or later projection:

```text
decision_id
registry_name
actor_type
actor_id
predicate_verb
object_type
object_id
```

Derivation rules:

```text
registry_name = second colon-delimited segment of domain
decision_id = final colon-delimited segment of domain
actor_type = segment before first colon in value2
actor_id = segment after first colon in value2
predicate_verb = first colon-delimited segment of value3
object_type = second colon-delimited segment of value3
object_id = third colon-delimited segment of value3
```

### Step 6: Insert into `z_config_lookup`

Insert the original normalized row into `z_config_lookup`.

Pseudo-SQL:

```sql
INSERT INTO z_config_lookup (
    domain,
    key1,
    value1,
    key2,
    value2,
    key3,
    value3,
    created
) VALUES (
    :domain,
    :key1,
    :value1,
    :key2,
    :value2,
    :key3,
    :value3,
    :created
);
```

Do not split one spreadsheet row into multiple database rows for v0.1.

Do not create JSON payloads for v0.1 unless the ingesting code keeps them outside `z_config_lookup`.

### Step 7: Produce an ingestion summary

After ingestion, produce a summary such as:

```text
rows_read: 4
rows_valid: 4
rows_inserted: 4
rows_failed: 0
registry_name: sample_attorney_demo
first_created: 2026-07-06T18:42:11Z
last_created: 2026-07-06T18:52:10Z
```

If rows fail validation, produce row-number-specific errors.

Example:

```text
Row 3 failed: value2 must follow <actor_type>:<actor_id>; got claims_review_agent.
```

---

## 8. Reconstructing an attorney-readable register row

Even though the database only stores the lookup shape, the application can reconstruct a simple attorney-readable row.

From this database row:

```text
domain = decision_register:sample_attorney_demo:dec_001
key1 = antecedent
value1 = claim submitted
key2 = subject
value2 = agent:claims_review_agent
key3 = predicate
value3 = recommend_approval:claim:claim_9981
created = 2026-07-06T18:42:11Z
```

The application can derive:

```text
decision_id = dec_001
created = 2026-07-06T18:42:11Z
antecedent = claim submitted
subject = agent:claims_review_agent
predicate = recommend_approval:claim:claim_9981
plain_english_decision = Because claim submitted, agent claims_review_agent performed recommend_approval on claim claim_9981.
```

This is not the final attorney-facing Decision Register.

It is the first reconstructable output from the constrained lookup schema.

---

## 9. Handling the four future attorney fields

The earlier attorney-facing register identifies four governance fields that matter but are not part of the v0.1 lookup ingestion:

```text
permission_source_type
permission_source_id
human_required
human_approver_id
```

For v0.1, do not add these as spreadsheet columns.

They can be handled later in one of three ways:

### Option A: Add real columns later

Preferred long-term approach when a real Decision Register table exists.

### Option B: Add a second lookup row profile later

Example:

```text
domain = decision_register_authority:sample_attorney_demo:dec_001
key1 = permission_source_type
value1 = policy_rule
key2 = permission_source_id
value2 = policy_claims_approval_v2
key3 = human_required
value3 = yes
created = 2026-07-06T18:42:11Z
```

This still has no clean place for `human_approver_id`, so it is not ideal.

### Option C: Encode authority in predicate or antecedent

Not recommended.

It hides governance-critical information inside prose and makes later enforcement harder.

Conclusion: the four future attorney fields are important, but they should not be forced into this first ingestion shape unless the schema changes or a second row profile is deliberately added.

---

## 10. Unit test plan

The ingestion code should include tests for the following.

### 10.1 Happy path

Input: valid CSV with four rows.

Expected:

- four rows inserted;
- no validation errors;
- each inserted row matches normalized source values;
- decision IDs are derived as `dec_001`, `dec_002`, `dec_003`, `dec_004`.

### 10.2 Header validation

Failures:

- missing `domain`;
- misspelled `value1`;
- uppercase `Domain`;
- duplicate `key1`;
- extra column if strict mode is enabled.

### 10.3 Required value validation

Failures:

- blank `domain`;
- blank `value1`;
- blank `value2`;
- blank `value3`;
- blank `created`.

### 10.4 Domain validation

Failures:

- `domain = sample_attorney_demo`;
- `domain = decision_register`;
- `domain = decision_register:sample_attorney_demo`;
- `domain = decision_register:sample_attorney_demo:`.

Expected error:

```text
domain must follow decision_register:<registry_name>:<decision_id>
```

### 10.5 Subject validation

Failures:

- `value2 = claims_review_agent`;
- `value2 = robot:claims_review_agent`;
- `value2 = agent:`;
- `value2 = :claims_review_agent`.

Expected allowed actor types:

```text
agent,human,system,institution,unknown
```

### 10.6 Predicate validation

Failures:

- `value3 = recommend_approval`;
- `value3 = recommend_approval:claim`;
- `value3 = recommend_approval::claim_9981`;
- `value3 = :claim:claim_9981`.

Expected format:

```text
<verb>:<object_type>:<object_id>
```

### 10.7 Created validation

Valid:

```text
2026-07-06T18:42:11Z
2026-07-06
```

Invalid:

```text
07/06/2026
yesterday
2026-13-99
```

### 10.8 Re-query test

After insert, query by registry prefix:

```sql
SELECT *
FROM z_config_lookup
WHERE domain LIKE 'decision_register:sample_attorney_demo:%'
ORDER BY created, domain;
```

Expected:

- rows return in stable order;
- all four decisions are present;
- reconstructed decision IDs match expected values.

---

## 11. Implementation notes

### 11.1 Do not rely on spreadsheet row number as identity

Spreadsheet row number is not durable.

Use the final segment of `domain` as the decision ID.

### 11.2 Do not auto-generate decision IDs during ingestion

For deterministic tests, the sample spreadsheet should contain stable decision IDs inside `domain`.

Generated IDs can come later.

### 11.3 Keep the grammar visible

The spreadsheet should make the grammar obvious:

```text
antecedent -> subject -> predicate
```

That is the whole point of the demo.

### 11.4 Keep extra attorney fields out for now

The attorney-facing Decision Register is the future review surface.

This spreadsheet is the first ingestion fixture.

Do not confuse the two.

---

## 12. Non-goals

This v0.1 ingestion contract does not define:

- a full attorney-facing Decision Register table;
- a full CDP Decision Lifecycle Envelope;
- a full Wire Message Envelope;
- a governed record table;
- authority/permission enforcement;
- human approval workflows;
- evidence reference ingestion;
- policy reference ingestion;
- tool-call audit ingestion;
- JSONB record storage;
- multi-row records for one decision.

Those are later steps.

For this demo, one spreadsheet row becomes one `z_config_lookup` row.

That is enough.

---

## 13. Final v0.1 contract

The v0.1 ingestion contract is:

```text
Spreadsheet columns:
  domain,key1,value1,key2,value2,key3,value3,created

One row means:
  one decision clause record

Mapping:
  domain -> registry and decision identity
  key1/value1 -> antecedent
  key2/value2 -> subject
  key3/value3 -> predicate
  created -> date/time captured

Database target:
  z_config_lookup

Insert behavior:
  one spreadsheet row inserts one database row

No hidden magic.
No extra columns.
No authority fields yet.
No JSON blob pretending to be governance.
```

This gives enough structure to create:

- the sample spreadsheet;
- ingestion code;
- validation code;
- unit tests;
- a first reconstructed Decision Register view.
