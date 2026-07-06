# Spreadsheet Ingestion Contract for the Normalized Decision Registry

Status: Demo ingestion contract v0.4  
Scope: Sample Decision Register spreadsheet ingestion into the normalized CDP control-plane Decision Registry  
Audience: implementers, test authors, attorney-facing demo builders  
Related DDL: `db/ddl/001-decision-registry-kernel.sql`  

---

## 1. Purpose

This document defines the spreadsheet format and ingestion process for the first sample Decision Register ingestion into the normalized CDP control-plane registry.

The canonical control-plane target is:

```text
cdp_core.decision_registry
```

The v0.4 registry is normalized. It does not use:

```text
domain
key1/value1
key2/value2
key3/value3
actor_type:actor_id
verb:object_type:object_id
```

Those were useful scaffolding ideas, but they pack multiple facts into single columns or encode field names as row data. The control-plane table now stores each fact in its own atomic column.

Compatibility strings such as:

```text
decision_register:<registry_name>:<decision_id>
decision_class:<registry_name>:<class_id>
```

may still be generated in views for display, export, or compatibility. They are not authoritative stored fields.

---

## 2. Required decision spreadsheet columns

The decision spreadsheet must contain exactly these required columns for v0.4 ingestion:

```text
registry_name,decision_id,decision_class_id,parent_decision_id,parent_relation_type,antecedent_text,subject_actor_type,subject_actor_id,predicate_verb,object_type,object_id,permission_source_type,permission_source_id,human_required,human_approver_id,created
```

Column names must be lowercase snake_case exactly as shown.

The first row must be the header row.

Each subsequent row is one material decision clause record.

CSV should be the first fixture format because it is easy to diff, test, and version.

XLSX may be supported later, using the same header names.

---

## 3. Required decision class spreadsheet columns

Class rows may be loaded separately into:

```text
cdp_core.decision_class_registry
```

The class spreadsheet should contain exactly:

```text
registry_name,class_id,parent_class_id,class_label,class_level,created
```

Class rows are useful for labels, parent-child class hierarchy, and rollup display.

---

## 4. Decision field meanings

### 4.1 `registry_name`

`registry_name` identifies the bounded decision set.

Examples:

```text
sample_attorney_demo
claims_demo
access_review_demo
```

Allowed format:

```text
^[A-Za-z0-9_-]+$
```

Do not include colons or packed domain strings.

### 4.2 `decision_id`

`decision_id` is the stable decision identifier within `registry_name`.

Examples:

```text
dec_001
dec_002
dec_003
```

The pair `(registry_name, decision_id)` is unique.

### 4.3 `decision_class_id`

`decision_class_id` identifies the decision class for analytics.

Examples:

```text
claim_intake
claim_approval
access_denial
human_review_escalation
```

This should match a `class_id` in `cdp_core.decision_class_registry` for the same registry.

### 4.4 `parent_decision_id`

`parent_decision_id` optionally identifies a parent decision within the same registry.

Use a blank cell when there is no parent decision.

The ingestion code should normalize blank `parent_decision_id` to SQL `NULL`.

Do not use `none` in this field.

### 4.5 `parent_relation_type`

`parent_relation_type` states the relationship from the current decision to `parent_decision_id`.

Allowed values:

```text
none
child_of
depends_on
derived_from
escalates_from
approves
denies
appeal_of
repair_of
supersedes
```

Rules:

- If `parent_relation_type = none`, `parent_decision_id` must be blank.
- If `parent_relation_type != none`, `parent_decision_id` must be populated.

### 4.6 `antecedent_text`

`antecedent_text` captures the condition, trigger, prior event, dependency, or context that made the decision relevant.

Examples:

```text
claim submitted
identity verification failed
claim amount exceeded auto-approval threshold
prior decision dec_003 escalated claim
none_supplied
```

Do not leave it blank.

### 4.7 `subject_actor_type`

Allowed values:

```text
agent
human
system
institution
unknown
```

### 4.8 `subject_actor_id`

Stable identifier for the actor.

Examples:

```text
claims_review_agent
access_agent
user_442
workflow_engine
review_board
unknown
```

Do not pack actor type and actor ID into one cell.

### 4.9 `predicate_verb`

The decision/action verb.

Examples:

```text
recommend_approval
deny_access
escalate_review
approve_review
create_task
```

Avoid vague verbs such as `processed`, `handled`, or `completed`.

### 4.10 `object_type`

The type of object affected by the decision.

Examples:

```text
claim
access_request
review_task
```

### 4.11 `object_id`

The specific object affected by the decision.

Examples:

```text
claim_9981
access_7731
task_1001
```

Do not pack predicate verb, object type, and object ID into one cell.

### 4.12 `permission_source_type`

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

`unknown` is allowed, but it should be treated as a governance finding.

### 4.13 `permission_source_id`

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

### 4.14 `human_required`

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

### 4.15 `human_approver_id`

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

### 4.16 `created`

Preferred format:

```text
YYYY-MM-DDTHH:MM:SSZ
```

Acceptable date-only fallback:

```text
YYYY-MM-DD
```

---

## 5. Minimal decision spreadsheet fixture

```csv
registry_name,decision_id,decision_class_id,parent_decision_id,parent_relation_type,antecedent_text,subject_actor_type,subject_actor_id,predicate_verb,object_type,object_id,permission_source_type,permission_source_id,human_required,human_approver_id,created
sample_attorney_demo,dec_001,claim_intake,,none,claim submitted,agent,claims_review_agent,recommend_approval,claim,claim_9981,policy_rule,policy_claims_approval_v2,yes,user_442,2026-07-06T18:42:11Z
sample_attorney_demo,dec_002,access_denial,,none,identity verification failed,agent,access_agent,deny_access,access_request,access_7731,workflow_configuration,workflow_access_v1,no,none,2026-07-06T18:44:09Z
sample_attorney_demo,dec_003,human_review_escalation,dec_001,escalates_from,claim amount exceeded auto-approval threshold,agent,claims_review_agent,escalate_review,claim,claim_9982,policy_rule,policy_claims_approval_v2,yes,unknown,2026-07-06T18:45:33Z
sample_attorney_demo,dec_004,claim_approval,dec_003,approves,prior decision dec_003 escalated claim,human,user_442,approve_review,claim,claim_9982,human_approval,user_442,yes,user_442,2026-07-06T18:52:10Z
```

---

## 6. Minimal class spreadsheet fixture

```csv
registry_name,class_id,parent_class_id,class_label,class_level,created
sample_attorney_demo,claim,,Claim Decisions,0,2026-07-06T18:00:00Z
sample_attorney_demo,claim_intake,claim,Claim Intake,1,2026-07-06T18:00:00Z
sample_attorney_demo,claim_approval,claim,Claim Approval,1,2026-07-06T18:00:00Z
sample_attorney_demo,human_review_escalation,claim,Human Review Escalation,1,2026-07-06T18:00:00Z
sample_attorney_demo,access,,Access Decisions,0,2026-07-06T18:00:00Z
sample_attorney_demo,access_denial,access,Access Denial,1,2026-07-06T18:00:00Z
```

---

## 7. Spreadsheet-to-database mapping

Each decision spreadsheet row maps directly into one `cdp_core.decision_registry` row.

| Spreadsheet column | Database column | Required | Notes |
|---|---|---:|---|
| `registry_name` | `registry_name` | yes | Atomic registry name |
| `decision_id` | `decision_id` | yes | Atomic decision ID |
| `decision_class_id` | `decision_class_id` | yes | Class ID within registry |
| `parent_decision_id` | `parent_decision_id` | conditional | Blank/null when no parent decision |
| `parent_relation_type` | `parent_relation_type` | yes | `none` when no parent decision |
| `antecedent_text` | `antecedent_text` | yes | Antecedent or `none_supplied` |
| `subject_actor_type` | `subject_actor_type` | yes | Controlled vocabulary |
| `subject_actor_id` | `subject_actor_id` | yes | Atomic actor ID |
| `predicate_verb` | `predicate_verb` | yes | Atomic action verb |
| `object_type` | `object_type` | yes | Atomic object type |
| `object_id` | `object_id` | yes | Atomic object ID |
| `permission_source_type` | `permission_source_type` | yes | Controlled vocabulary |
| `permission_source_id` | `permission_source_id` | yes | Source ID or `unknown` |
| `human_required` | `human_required` | yes | Normalize yes/no to Boolean |
| `human_approver_id` | `human_approver_id` | yes | Use `none` or `unknown` when applicable |
| `created` | `created` | yes | ISO timestamp or date |

For v0.4, extra spreadsheet columns should be rejected to reduce schema drift.

---

## 8. Ingestion process

### Step 1: Load

For CSV:

- read with UTF-8 encoding;
- preserve strings as strings;
- do not auto-convert IDs into numbers;
- trim leading/trailing whitespace;
- preserve internal spaces;
- normalize blank `parent_decision_id` and `parent_class_id` to SQL `NULL`.

### Step 2: Validate headers

Decision header:

```text
registry_name,decision_id,decision_class_id,parent_decision_id,parent_relation_type,antecedent_text,subject_actor_type,subject_actor_id,predicate_verb,object_type,object_id,permission_source_type,permission_source_id,human_required,human_approver_id,created
```

Class header:

```text
registry_name,class_id,parent_class_id,class_label,class_level,created
```

### Step 3: Validate decision rows

A row is valid when:

1. `registry_name`, `decision_id`, and `decision_class_id` are simple IDs.
2. `parent_relation_type` is an allowed value.
3. If `parent_relation_type = none`, `parent_decision_id` is blank/null.
4. If `parent_relation_type != none`, `parent_decision_id` is populated.
5. `antecedent_text` is non-empty.
6. `subject_actor_type` is one of `agent`, `human`, `system`, `institution`, `unknown`.
7. `subject_actor_id` is non-empty.
8. `predicate_verb`, `object_type`, and `object_id` are non-empty atomic values.
9. `permission_source_type` is an allowed value.
10. `permission_source_id` is non-empty.
11. `human_required` is `yes`, `no`, `true`, or `false` before normalization.
12. `human_approver_id` is non-empty.
13. If `human_required` is false, `human_approver_id` should be `none`.
14. `created` parses as an allowed date or timestamp.

### Step 4: Insert class rows first

Class rows should be inserted before decision rows so the decision foreign key to `(registry_name, decision_class_id)` can resolve.

Pseudo-SQL:

```sql
INSERT INTO cdp_core.decision_class_registry (
    registry_name,
    class_id,
    parent_class_id,
    class_label,
    class_level,
    created
) VALUES (
    :registry_name,
    :class_id,
    :parent_class_id,
    :class_label,
    :class_level,
    :created
);
```

### Step 5: Insert decision rows

Pseudo-SQL:

```sql
INSERT INTO cdp_core.decision_registry (
    registry_name,
    decision_id,
    decision_class_id,
    parent_decision_id,
    parent_relation_type,
    antecedent_text,
    subject_actor_type,
    subject_actor_id,
    predicate_verb,
    object_type,
    object_id,
    permission_source_type,
    permission_source_id,
    human_required,
    human_approver_id,
    created
) VALUES (
    :registry_name,
    :decision_id,
    :decision_class_id,
    :parent_decision_id,
    :parent_relation_type,
    :antecedent_text,
    :subject_actor_type,
    :subject_actor_id,
    :predicate_verb,
    :object_type,
    :object_id,
    :permission_source_type,
    :permission_source_id,
    :human_required,
    :human_approver_id,
    :created
);
```

Do not split one decision spreadsheet row into multiple database rows.

---

## 9. Analytics targets

The v0.4 DDL exposes these read surfaces.

```text
cdp_projection.decision_class_registry_flat
cdp_projection.decision_registry_flat
cdp_projection.decision_class_rollup
cdp_projection.decision_parent_child_edges
```

Use `decision_registry_flat` for attorney-facing review rows.

Use `decision_class_rollup` for class counts, human-review burden, and unknown-permission findings.

Use `decision_parent_child_edges` for lineage and graph/tree analysis.

---

## 10. Compatibility with `z_config_lookup`

The old `z_config_lookup` shape is not normal-form compliant for this purpose because it encodes field names and multi-part facts in columns such as:

```text
key1/value1
key2/value2
key3/value3
```

and previously encouraged packed values such as:

```text
agent:claims_review_agent
recommend_approval:claim:claim_9981
```

That should remain a legacy/staging idea only.

The canonical v0.4 target is:

```text
cdp_core.decision_registry
```

Recommended flow:

```text
spreadsheet -> parser/validator -> cdp_core.decision_class_registry
spreadsheet -> parser/validator -> cdp_core.decision_registry
registry -> projections
```

---

## 11. Unit test plan

### 11.1 Happy path

Input: valid class CSV and valid decision CSV.

Expected:

- class rows inserted;
- decision rows inserted;
- no validation errors;
- two parent-child decision edges exist;
- class rollups group decisions correctly;
- derived compatibility domains appear only in projections;
- no core table stores packed field strings.

### 11.2 Header validation

Failures:

- missing `subject_actor_type`;
- missing `object_id`;
- misspelled `decision_class_id`;
- uppercase `Registry_Name`;
- duplicate `decision_id`;
- extra column in strict mode.

### 11.3 Normal form validation

Failures:

```text
subject_actor_id = agent:claims_review_agent
predicate_verb = recommend_approval:claim:claim_9981
registry_name = decision_register:sample_attorney_demo:dec_001
decision_class_id = decision_class:sample_attorney_demo:claim_approval
```

Expected: packed fields are rejected before insert.

### 11.4 Re-query tests

Class rollup:

```sql
SELECT *
FROM cdp_projection.decision_class_rollup
WHERE registry_name = 'sample_attorney_demo'
ORDER BY decision_class_id;
```

Parent-child edges:

```sql
SELECT *
FROM cdp_projection.decision_parent_child_edges
WHERE parent_decision_id = 'dec_001';
```

Expected:

- rollup counts group decisions by atomic class ID;
- edge query returns descendants by atomic parent decision ID;
- no query has to parse colon-delimited values from core tables.

---

## 12. Final v0.4 contract

```text
Spreadsheet columns:
  registry_name,decision_id,decision_class_id,parent_decision_id,parent_relation_type,antecedent_text,subject_actor_type,subject_actor_id,predicate_verb,object_type,object_id,permission_source_type,permission_source_id,human_required,human_approver_id,created

One row means:
  one material decision clause record

Database target:
  cdp_core.decision_registry

Projection targets:
  cdp_projection.decision_class_registry_flat
  cdp_projection.decision_registry_flat
  cdp_projection.decision_class_rollup
  cdp_projection.decision_parent_child_edges

Insert behavior:
  one spreadsheet decision row inserts one normalized database decision row

No hidden magic.
No key/value pseudo-columns.
No packed colon-delimited facts in core tables.
No parent-child inference from prose.
No JSON blob pretending to be hierarchy.
```
