# Spreadsheet Ingestion Contract for the Decision Registry

Status: Demo ingestion contract v0.2  
Scope: Sample Decision Register spreadsheet ingestion into the CDP control-plane Decision Registry  
Audience: implementers, test authors, attorney-facing demo builders  
Related DDL: `db/ddl/001-decision-registry-kernel.sql`  

---

## 1. Purpose

This document defines the spreadsheet format and ingestion process for the first sample Decision Register ingestion into the CDP control plane.

The control-plane target is:

```text
cdp_core.decision_registry
```

The older `z_config_lookup` shape remains useful as a compatibility/staging concept, but it is not sufficient once the spreadsheet includes attorney-facing permission fields.

The v0.2 spreadsheet represents one decision per row using:

1. decision identity and domain;
2. three grammatical key/value pairs;
3. four attorney-facing governance fields;
4. a created timestamp.

The required columns are:

```text
domain
key1
value1
key2
value2
key3
value3
permission_source_type
permission_source_id
human_required
human_approver_id
created
```

---

## 2. Why the four permission fields are included now

The first spreadsheet must support the question an attorney will actually ask:

> What decisions did the agentic AI make, and what allowed those decisions to happen?

The four fields needed for that first answer are:

```text
permission_source_type
permission_source_id
human_required
human_approver_id
```

These fields do not answer every authority, standing, delegation, or legality question.

They do give the first registry enough structure to distinguish:

- a policy-authorized decision;
- a human-approved decision;
- a role-authorized decision;
- a workflow-authorized decision;
- a tool-permission-authorized action;
- a prior-decision-authorized action;
- an emergency exception;
- an unknown permission source.

That is enough for the demo and enough for first-pass attorney review.

---

## 3. Required spreadsheet columns

The spreadsheet must contain exactly these required columns for v0.2 ingestion:

```text
domain,key1,value1,key2,value2,key3,value3,permission_source_type,permission_source_id,human_required,human_approver_id,created
```

Column names must be lowercase snake_case exactly as shown.

The first row must be the header row.

Each subsequent row is one material decision clause record.

CSV should be the first fixture format because it is easy to diff, test, and version.

XLSX may be supported later, using the same header names.

---

## 4. Field meanings

### 4.1 `domain`

`domain` identifies both the bounded registry and the decision ID.

Required format:

```text
decision_register:<registry_name>:<decision_id>
```

Example:

```text
decision_register:sample_attorney_demo:dec_001
```

Parsing rule:

```text
registry_name = second colon-delimited segment of domain
decision_id = final colon-delimited segment of domain
```

The current v0.2 DDL stores `domain` as the durable identity path and derives `decision_id` in the projection view.

### 4.2 `key1/value1`: antecedent

`key1/value1` captures the antecedent: the condition, trigger, prior event, dependency, or context that made the decision relevant.

Required default:

```text
key1 = antecedent
```

Examples:

```text
value1 = claim submitted
value1 = identity verification failed
value1 = claim amount exceeded auto-approval threshold
value1 = prior decision dec_003 escalated claim
```

If no antecedent is supplied, use:

```text
value1 = none_supplied
```

Do not leave `value1` blank.

### 4.3 `key2/value2`: subject

`key2/value2` captures the subject: the actor that made, recommended, blocked, escalated, approved, or recorded the decision.

Required default:

```text
key2 = subject
```

Required `value2` format:

```text
<actor_type>:<actor_id>
```

Allowed `actor_type` values:

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
agent:access_agent
human:user_442
system:workflow_engine
institution:review_board
unknown:unknown
```

### 4.4 `key3/value3`: predicate

`key3/value3` captures the predicate: the decision, recommendation, or action.

Required default:

```text
key3 = predicate
```

Required `value3` format:

```text
<verb>:<object_type>:<object_id>
```

Examples:

```text
recommend_approval:claim:claim_9981
deny_access:access_request:access_7731
escalate_review:claim:claim_9982
approve_review:claim:claim_9982
create_task:review_task:task_1001
```

The predicate must name what happened. Avoid vague verbs such as `processed`, `handled`, or `completed`.

### 4.5 `permission_source_type`

`permission_source_type` states what kind of permission source allowed, supported, or routed the decision.

Allowed values:

```text
policy_rule
human_approval
system_role
workflow_configuration
tool_permission
prior_decision
emergency_exception
unknown
```

Definitions:

| Value | Meaning |
|---|---|
| `policy_rule` | A named policy or rule allowed the decision or recommendation |
| `human_approval` | A human approved the decision before it took effect |
| `system_role` | The agent or system had a configured role allowing the operation |
| `workflow_configuration` | A workflow step allowed the decision under configured conditions |
| `tool_permission` | A tool/API permission allowed the action |
| `prior_decision` | A previous recorded decision authorized this one |
| `emergency_exception` | An exception path was used |
| `unknown` | The system cannot show the permission source |

`unknown` is allowed, but it should be treated as a governance finding.

### 4.6 `permission_source_id`

`permission_source_id` identifies the specific permission source.

Examples:

```text
policy_claims_approval_v2
workflow_access_v1
role_claims_review_agent
claims_api_recommend_permission
dec_003
emergency_exception_2026_001
unknown
```

Do not leave it blank.

Use `unknown` when the source is not known.

### 4.7 `human_required`

`human_required` states whether a human approval was required before the decision or action could take effect.

Allowed spreadsheet values:

```text
yes
no
true
false
```

The ingestion code should normalize to Boolean:

```text
yes,true  -> true
no,false  -> false
```

For deterministic fixtures, prefer:

```text
yes
no
```

### 4.8 `human_approver_id`

`human_approver_id` identifies the human approver when applicable.

Examples:

```text
user_442
review_manager_01
none
unknown
```

Use `none` when human approval was not required.

Use `unknown` when human approval was required but the approver is not recorded.

Do not leave it blank.

### 4.9 `created`

`created` is the date or timestamp the decision record was created or captured for ingestion.

Preferred format:

```text
YYYY-MM-DDTHH:MM:SSZ
```

Acceptable date-only fallback:

```text
YYYY-MM-DD
```

The ingestion code must make date-only behavior explicit in tests.

---

## 5. Minimal sample spreadsheet

CSV fixture:

```csv
domain,key1,value1,key2,value2,key3,value3,permission_source_type,permission_source_id,human_required,human_approver_id,created
decision_register:sample_attorney_demo:dec_001,antecedent,claim submitted,subject,agent:claims_review_agent,predicate,recommend_approval:claim:claim_9981,policy_rule,policy_claims_approval_v2,yes,user_442,2026-07-06T18:42:11Z
decision_register:sample_attorney_demo:dec_002,antecedent,identity verification failed,subject,agent:access_agent,predicate,deny_access:access_request:access_7731,workflow_configuration,workflow_access_v1,no,none,2026-07-06T18:44:09Z
decision_register:sample_attorney_demo:dec_003,antecedent,claim amount exceeded auto-approval threshold,subject,agent:claims_review_agent,predicate,escalate_review:claim:claim_9982,policy_rule,policy_claims_approval_v2,yes,unknown,2026-07-06T18:45:33Z
decision_register:sample_attorney_demo:dec_004,antecedent,prior decision dec_003 escalated claim,subject,human:user_442,predicate,approve_review:claim:claim_9982,human_approval,user_442,yes,user_442,2026-07-06T18:52:10Z
```

This fixture should test:

- header validation;
- required fields;
- decision ID derivation from `domain`;
- actor parsing from `value2`;
- predicate parsing from `value3`;
- permission source validation;
- Boolean normalization for `human_required`;
- approver handling for `human_approver_id`;
- created-date parsing;
- insert into `cdp_core.decision_registry`;
- retrieval from `cdp_projection.decision_registry_flat`.

---

## 6. Spreadsheet-to-database mapping

Each spreadsheet row maps directly into one `cdp_core.decision_registry` row.

| Spreadsheet column | Database column | Required | Notes |
|---|---|---:|---|
| `domain` | `domain` | yes | Contains registry and derived decision ID |
| `key1` | `key1` | yes | Must be `antecedent` |
| `value1` | `value1` | yes | Antecedent value or `none_supplied` |
| `key2` | `key2` | yes | Must be `subject` |
| `value2` | `value2` | yes | Actor value, e.g. `agent:claims_review_agent` |
| `key3` | `key3` | yes | Must be `predicate` |
| `value3` | `value3` | yes | Action/object value, e.g. `recommend_approval:claim:claim_9981` |
| `permission_source_type` | `permission_source_type` | yes | Controlled vocabulary |
| `permission_source_id` | `permission_source_id` | yes | Source ID or `unknown` |
| `human_required` | `human_required` | yes | Normalize yes/no to Boolean |
| `human_approver_id` | `human_approver_id` | yes | Use `none` or `unknown` when applicable |
| `created` | `created` | yes | ISO timestamp or date |

For v0.2, extra spreadsheet columns should be rejected to reduce schema drift.

---

## 7. Ingestion process

### Step 1: Load the spreadsheet

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
domain,key1,value1,key2,value2,key3,value3,permission_source_type,permission_source_id,human_required,human_approver_id,created
```

Validation fails when a required column is missing, misspelled, duplicated, mis-cased, or when extra columns appear in strict mode.

### Step 3: Normalize row values

For each row:

- trim leading and trailing whitespace;
- convert empty strings to validation errors;
- normalize controlled vocabulary values to lowercase snake_case;
- normalize `human_required` to Boolean;
- keep IDs stable and boring.

Controlled fields:

```text
key1
key2
key3
actor_type segment of value2
permission_source_type
human_required
```

Expected default keys:

```text
key1 = antecedent
key2 = subject
key3 = predicate
```

### Step 4: Validate row structure

A row is valid when:

1. `domain` follows `decision_register:<registry_name>:<decision_id>`.
2. `key1` equals `antecedent`.
3. `value1` is non-empty.
4. `key2` equals `subject`.
5. `value2` follows `<actor_type>:<actor_id>`.
6. `actor_type` is one of `agent`, `human`, `system`, `institution`, `unknown`.
7. `key3` equals `predicate`.
8. `value3` follows `<verb>:<object_type>:<object_id>`.
9. `permission_source_type` is one of the allowed values.
10. `permission_source_id` is non-empty.
11. `human_required` is `yes`, `no`, `true`, or `false` before normalization.
12. `human_approver_id` is non-empty.
13. If `human_required` is false, `human_approver_id` should be `none`.
14. `created` parses as an allowed date or timestamp.

### Step 5: Derive helper values

The ingestion code may derive these for validation, logging, tests, and projections:

```text
registry_name
decision_id
actor_type
actor_id
predicate_verb
object_type
object_id
human_required_boolean
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

### Step 6: Insert into `cdp_core.decision_registry`

Pseudo-SQL:

```sql
INSERT INTO cdp_core.decision_registry (
    domain,
    key1,
    value1,
    key2,
    value2,
    key3,
    value3,
    permission_source_type,
    permission_source_id,
    human_required,
    human_approver_id,
    created
) VALUES (
    :domain,
    :key1,
    :value1,
    :key2,
    :value2,
    :key3,
    :value3,
    :permission_source_type,
    :permission_source_id,
    :human_required,
    :human_approver_id,
    :created
);
```

Do not split one spreadsheet row into multiple database rows for v0.2.

### Step 7: Produce an ingestion summary

Example:

```text
rows_read: 4
rows_valid: 4
rows_inserted: 4
rows_failed: 0
registry_name: sample_attorney_demo
first_created: 2026-07-06T18:42:11Z
last_created: 2026-07-06T18:52:10Z
permission_source_types: policy_rule, workflow_configuration, human_approval
human_required_count: 3
```

If rows fail validation, produce row-number-specific errors.

Example:

```text
Row 3 failed: human_required must be one of yes,no,true,false; got maybe.
```

---

## 8. Reconstructing an attorney-readable register row

From this database row:

```text
domain = decision_register:sample_attorney_demo:dec_001
key1 = antecedent
value1 = claim submitted
key2 = subject
value2 = agent:claims_review_agent
key3 = predicate
value3 = recommend_approval:claim:claim_9981
permission_source_type = policy_rule
permission_source_id = policy_claims_approval_v2
human_required = true
human_approver_id = user_442
created = 2026-07-06T18:42:11Z
```

The projection can derive:

```text
decision_id = dec_001
created = 2026-07-06T18:42:11Z
antecedent = claim submitted
subject = agent:claims_review_agent
predicate = recommend_approval:claim:claim_9981
permission = policy_rule:policy_claims_approval_v2
human_required = true
human_approver_id = user_442
plain_english_decision = Because claim submitted, agent claims_review_agent performed recommend_approval on claim claim_9981. Permission source: policy_rule:policy_claims_approval_v2. Human required: true. Human approver: user_442.
```

This is still not the full CDP governed record.

It is the first attorney-readable projection from the control-plane Decision Registry.

---

## 9. Compatibility with `z_config_lookup`

The current `z_config_lookup` shape can hold:

```text
domain,key1,value1,key2,value2,key3,value3,created
```

It cannot hold the four permission fields unless that table is extended or those fields are stored somewhere else.

Therefore, once the spreadsheet includes the four permission fields, the canonical target should be:

```text
cdp_core.decision_registry
```

If an implementation must temporarily use `z_config_lookup`, it must either:

1. extend `z_config_lookup` with the four permission columns; or
2. use `z_config_lookup` only for the grammar fields and store permission fields in a separate companion table; or
3. ingest directly into `cdp_core.decision_registry`.

Recommendation for the demo:

```text
spreadsheet -> parser/validator -> cdp_core.decision_registry -> cdp_projection.decision_registry_flat
```

---

## 10. Unit test plan

### 10.1 Happy path

Input: valid CSV with four rows.

Expected:

- four rows inserted;
- no validation errors;
- each inserted row matches normalized source values;
- decision IDs are derived as `dec_001`, `dec_002`, `dec_003`, `dec_004`;
- `human_required` is stored as Boolean;
- projection rows include permission fields.

### 10.2 Header validation

Failures:

- missing `permission_source_type`;
- missing `human_required`;
- misspelled `human_approver_id`;
- uppercase `Domain`;
- duplicate `key1`;
- extra column in strict mode.

### 10.3 Required value validation

Failures:

- blank `domain`;
- blank `value1`;
- blank `value2`;
- blank `value3`;
- blank `permission_source_type`;
- blank `permission_source_id`;
- blank `human_required`;
- blank `human_approver_id`;
- blank `created`.

### 10.4 Permission validation

Failures:

```text
permission_source_type = policy
permission_source_type = approval
permission_source_type = robot_authority
permission_source_id = <blank>
```

Allowed values:

```text
policy_rule,human_approval,system_role,workflow_configuration,tool_permission,prior_decision,emergency_exception,unknown
```

### 10.5 Human approval validation

Valid:

```text
human_required = yes, human_approver_id = user_442
human_required = no, human_approver_id = none
human_required = yes, human_approver_id = unknown
```

Invalid:

```text
human_required = maybe
human_required = no, human_approver_id = user_442
human_required = yes, human_approver_id = <blank>
```

### 10.6 Re-query test

After insert, query by registry prefix:

```sql
SELECT *
FROM cdp_projection.decision_registry_flat
WHERE domain LIKE 'decision_register:sample_attorney_demo:%'
ORDER BY created, domain;
```

Expected:

- rows return in stable order;
- all four decisions are present;
- derived decision IDs match expected values;
- permission fields are populated;
- `plain_english_decision` includes permission and human approval surface.

---

## 11. Final v0.2 contract

```text
Spreadsheet columns:
  domain,key1,value1,key2,value2,key3,value3,permission_source_type,permission_source_id,human_required,human_approver_id,created

One row means:
  one material decision clause record

Mapping:
  domain -> registry and decision identity
  key1/value1 -> antecedent
  key2/value2 -> subject
  key3/value3 -> predicate
  permission_source_type -> permission category
  permission_source_id -> permission source identifier
  human_required -> whether human approval was required
  human_approver_id -> approver, none, or unknown
  created -> date/time captured

Database target:
  cdp_core.decision_registry

Projection target:
  cdp_projection.decision_registry_flat

Insert behavior:
  one spreadsheet row inserts one database row

No hidden magic.
No authority metaphysics.
No JSON blob pretending to be governance.
```
