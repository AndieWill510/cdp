# Spreadsheet Ingestion Contract for the Decision Registry

Status: Demo ingestion contract v0.3  
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

The older `z_config_lookup` shape remains useful as a compatibility/staging concept, but it is not sufficient once the spreadsheet includes attorney-facing permission fields and hierarchy fields.

The v0.3 spreadsheet represents one decision per row using:

1. decision identity and domain;
2. decision class / hierarchy fields;
3. three grammatical key/value pairs;
4. four attorney-facing governance fields;
5. a created timestamp.

The required columns are:

```text
domain
decision_class_domain
parent_domain
parent_relation_type
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

## 2. Why hierarchy fields are included now

The registry should not only answer:

```text
What decisions happened?
```

It should also answer:

```text
What kinds of decisions happened?
Which decisions descend from other decisions?
Where are decisions clustering?
Which classes require the most human review?
Which classes have unknown permission sources?
```

The hierarchy fields are:

```text
decision_class_domain
parent_domain
parent_relation_type
```

They support two different forms of analysis:

1. **Class analytics**: grouping decisions by type, subtype, workflow, risk area, or legal/compliance category.
2. **Parent-child lineage**: showing how one decision depends on, escalates from, approves, denies, repairs, appeals, or supersedes another decision.

These should remain distinct.

A decision can belong to a class without having a parent decision.

A decision can have a parent decision while belonging to the same or a different class.

---

## 3. Required spreadsheet columns

The spreadsheet must contain exactly these required columns for v0.3 ingestion:

```text
domain,decision_class_domain,parent_domain,parent_relation_type,key1,value1,key2,value2,key3,value3,permission_source_type,permission_source_id,human_required,human_approver_id,created
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

### 4.2 `decision_class_domain`

`decision_class_domain` identifies the class of decision for analytics.

Required format:

```text
decision_class:<registry_name>:<class_id>
```

Examples:

```text
decision_class:sample_attorney_demo:claim_intake
decision_class:sample_attorney_demo:claim_approval
decision_class:sample_attorney_demo:access_denial
decision_class:sample_attorney_demo:human_review_escalation
```

The class domain should be stable and boring.

Do not use long prose as the class ID.

Use `decision_class:<registry_name>:unclassified` only when the class is genuinely unknown.

### 4.3 `parent_domain`

`parent_domain` optionally identifies a parent decision row.

Required format when present:

```text
decision_register:<registry_name>:<parent_decision_id>
```

Examples:

```text
decision_register:sample_attorney_demo:dec_003
```

Use a blank cell when there is no parent decision.

The ingestion code should normalize blank `parent_domain` to SQL `NULL`.

Do not use `none` in this field.

### 4.4 `parent_relation_type`

`parent_relation_type` states the relationship from the current decision to `parent_domain`.

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

- If `parent_relation_type = none`, `parent_domain` must be blank.
- If `parent_relation_type != none`, `parent_domain` must be populated.

Examples:

| Current decision | Parent decision | Relation |
|---|---|---|
| human approval | agent recommendation | `approves` |
| denial | identity verification failure decision | `depends_on` |
| appeal | original denial | `appeal_of` |
| repair decision | harmful decision | `repair_of` |
| later corrected decision | earlier decision | `supersedes` |

### 4.5 `key1/value1`: antecedent

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

### 4.6 `key2/value2`: subject

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

### 4.7 `key3/value3`: predicate

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

### 4.8 `permission_source_type`

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

`unknown` is allowed, but it should be treated as a governance finding.

### 4.9 `permission_source_id`

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

### 4.10 `human_required`

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

### 4.11 `human_approver_id`

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

### 4.12 `created`

`created` is the date or timestamp the decision record was created or captured for ingestion.

Preferred format:

```text
YYYY-MM-DDTHH:MM:SSZ
```

Acceptable date-only fallback:

```text
YYYY-MM-DD
```

---

## 5. Minimal sample spreadsheet

CSV fixture:

```csv
domain,decision_class_domain,parent_domain,parent_relation_type,key1,value1,key2,value2,key3,value3,permission_source_type,permission_source_id,human_required,human_approver_id,created
decision_register:sample_attorney_demo:dec_001,decision_class:sample_attorney_demo:claim_intake,,none,antecedent,claim submitted,subject,agent:claims_review_agent,predicate,recommend_approval:claim:claim_9981,policy_rule,policy_claims_approval_v2,yes,user_442,2026-07-06T18:42:11Z
decision_register:sample_attorney_demo:dec_002,decision_class:sample_attorney_demo:access_denial,,none,antecedent,identity verification failed,subject,agent:access_agent,predicate,deny_access:access_request:access_7731,workflow_configuration,workflow_access_v1,no,none,2026-07-06T18:44:09Z
decision_register:sample_attorney_demo:dec_003,decision_class:sample_attorney_demo:human_review_escalation,decision_register:sample_attorney_demo:dec_001,escalates_from,antecedent,claim amount exceeded auto-approval threshold,subject,agent:claims_review_agent,predicate,escalate_review:claim:claim_9982,policy_rule,policy_claims_approval_v2,yes,unknown,2026-07-06T18:45:33Z
decision_register:sample_attorney_demo:dec_004,decision_class:sample_attorney_demo:claim_approval,decision_register:sample_attorney_demo:dec_003,approves,antecedent,prior decision dec_003 escalated claim,subject,human:user_442,predicate,approve_review:claim:claim_9982,human_approval,user_442,yes,user_442,2026-07-06T18:52:10Z
```

This fixture should test:

- header validation;
- required fields;
- decision ID derivation from `domain`;
- class ID derivation from `decision_class_domain`;
- parent decision derivation from `parent_domain`;
- parent relation validation;
- actor parsing from `value2`;
- predicate parsing from `value3`;
- permission source validation;
- Boolean normalization for `human_required`;
- approver handling for `human_approver_id`;
- created-date parsing;
- insert into `cdp_core.decision_registry`;
- retrieval from `cdp_projection.decision_registry_flat`;
- class rollup from `cdp_projection.decision_class_rollup`;
- parent-child edge output from `cdp_projection.decision_parent_child_edges`.

---

## 6. Optional decision class registry fixture

Class rows may be loaded separately into `cdp_core.decision_class_registry`.

They are useful for labels, parent-child class hierarchy, and rollup display.

CSV fixture:

```csv
domain,parent_domain,class_id,class_label,class_level,created
decision_class:sample_attorney_demo:claim,,claim,Claim Decisions,0,2026-07-06T18:00:00Z
decision_class:sample_attorney_demo:claim_intake,decision_class:sample_attorney_demo:claim,claim_intake,Claim Intake,1,2026-07-06T18:00:00Z
decision_class:sample_attorney_demo:claim_approval,decision_class:sample_attorney_demo:claim,claim_approval,Claim Approval,1,2026-07-06T18:00:00Z
decision_class:sample_attorney_demo:human_review_escalation,decision_class:sample_attorney_demo:claim,human_review_escalation,Human Review Escalation,1,2026-07-06T18:00:00Z
decision_class:sample_attorney_demo:access, ,access,Access Decisions,0,2026-07-06T18:00:00Z
decision_class:sample_attorney_demo:access_denial,decision_class:sample_attorney_demo:access,access_denial,Access Denial,1,2026-07-06T18:00:00Z
```

For strict CSV fixtures, prefer a truly blank `parent_domain` cell rather than a space.

---

## 7. Spreadsheet-to-database mapping

Each decision spreadsheet row maps directly into one `cdp_core.decision_registry` row.

| Spreadsheet column | Database column | Required | Notes |
|---|---|---:|---|
| `domain` | `domain` | yes | Contains registry and derived decision ID |
| `decision_class_domain` | `decision_class_domain` | yes | Class path for analytics |
| `parent_domain` | `parent_domain` | conditional | Blank when no parent decision |
| `parent_relation_type` | `parent_relation_type` | yes | `none` when no parent decision |
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

For v0.3, extra spreadsheet columns should be rejected to reduce schema drift.

---

## 8. Ingestion process

### Step 1: Load the spreadsheet

For CSV:

- read with UTF-8 encoding;
- preserve strings as strings;
- do not auto-convert IDs into numbers;
- trim leading/trailing whitespace;
- preserve internal spaces;
- normalize blank `parent_domain` to `NULL`.

For XLSX:

- read the first worksheet unless a worksheet name is explicitly provided;
- require the same header row;
- treat all cells as strings except `created`, which may be parsed as date/time.

### Step 2: Validate headers

Expected header list:

```text
domain,decision_class_domain,parent_domain,parent_relation_type,key1,value1,key2,value2,key3,value3,permission_source_type,permission_source_id,human_required,human_approver_id,created
```

Validation fails when a required column is missing, misspelled, duplicated, mis-cased, or when extra columns appear in strict mode.

### Step 3: Normalize row values

For each row:

- trim leading and trailing whitespace;
- convert empty required strings to validation errors;
- convert empty `parent_domain` to null;
- normalize controlled vocabulary values to lowercase snake_case;
- normalize `human_required` to Boolean;
- keep IDs stable and boring.

Controlled fields:

```text
key1
key2
key3
actor_type segment of value2
parent_relation_type
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
2. `decision_class_domain` follows `decision_class:<registry_name>:<class_id>`.
3. `parent_relation_type` is an allowed value.
4. If `parent_relation_type = none`, `parent_domain` is blank/null.
5. If `parent_relation_type != none`, `parent_domain` follows `decision_register:<registry_name>:<decision_id>`.
6. `key1` equals `antecedent`.
7. `value1` is non-empty.
8. `key2` equals `subject`.
9. `value2` follows `<actor_type>:<actor_id>`.
10. `actor_type` is one of `agent`, `human`, `system`, `institution`, `unknown`.
11. `key3` equals `predicate`.
12. `value3` follows `<verb>:<object_type>:<object_id>`.
13. `permission_source_type` is one of the allowed values.
14. `permission_source_id` is non-empty.
15. `human_required` is `yes`, `no`, `true`, or `false` before normalization.
16. `human_approver_id` is non-empty.
17. If `human_required` is false, `human_approver_id` should be `none`.
18. `created` parses as an allowed date or timestamp.

### Step 5: Derive helper values

The ingestion code may derive these for validation, logging, tests, and projections:

```text
registry_name
decision_id
decision_class_id
parent_decision_id
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
decision_class_id = final colon-delimited segment of decision_class_domain
parent_decision_id = final colon-delimited segment of parent_domain when present
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
    decision_class_domain,
    parent_domain,
    parent_relation_type,
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
    :decision_class_domain,
    :parent_domain,
    :parent_relation_type,
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

Do not split one decision spreadsheet row into multiple database rows for v0.3.

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
decision_classes: claim_intake, access_denial, human_review_escalation, claim_approval
parent_edge_count: 2
permission_source_types: policy_rule, workflow_configuration, human_approval
human_required_count: 3
```

If rows fail validation, produce row-number-specific errors.

Example:

```text
Row 3 failed: parent_relation_type escalates_from requires a non-empty parent_domain.
```

---

## 9. Analytics targets

The v0.3 DDL exposes three useful read surfaces.

### 9.1 Flat register view

```text
cdp_projection.decision_registry_flat
```

Use this for attorney-facing review rows.

### 9.2 Class rollup view

```text
cdp_projection.decision_class_rollup
```

Use this for questions such as:

```text
How many decisions were claim approvals?
How many access decisions were denials?
Which classes required the most human review?
Which classes have unknown permission sources?
```

### 9.3 Parent-child edge view

```text
cdp_projection.decision_parent_child_edges
```

Use this for graph/tree questions such as:

```text
Which decisions descended from dec_001?
Which decisions approved, denied, appealed, repaired, or superseded another decision?
What is the lineage of this decision?
```

---

## 10. Compatibility with `z_config_lookup`

The older `z_config_lookup` shape can hold:

```text
domain,key1,value1,key2,value2,key3,value3,created
```

It cannot hold the v0.3 fields unless it is extended:

```text
decision_class_domain
parent_domain
parent_relation_type
permission_source_type
permission_source_id
human_required
human_approver_id
```

Therefore, the canonical v0.3 target should be:

```text
cdp_core.decision_registry
```

Recommended flow:

```text
spreadsheet -> parser/validator -> cdp_core.decision_registry -> projections
```

---

## 11. Unit test plan

### 11.1 Happy path

Input: valid CSV with four rows.

Expected:

- four rows inserted;
- no validation errors;
- decision IDs are derived as `dec_001`, `dec_002`, `dec_003`, `dec_004`;
- class IDs are derived;
- two parent-child edges exist;
- `human_required` is stored as Boolean;
- projection rows include class, parent, permission, and human approval fields.

### 11.2 Header validation

Failures:

- missing `decision_class_domain`;
- missing `parent_relation_type`;
- missing `permission_source_type`;
- missing `human_required`;
- misspelled `human_approver_id`;
- uppercase `Domain`;
- duplicate `key1`;
- extra column in strict mode.

### 11.3 Hierarchy validation

Failures:

```text
parent_relation_type = none, parent_domain = decision_register:sample_attorney_demo:dec_001
parent_relation_type = escalates_from, parent_domain = <blank>
parent_domain = dec_001
parent_domain = decision_class:sample_attorney_demo:claim
```

Expected parent domain format:

```text
decision_register:<registry_name>:<decision_id>
```

### 11.4 Class validation

Failures:

```text
decision_class_domain = claim_approval
decision_class_domain = decision_register:sample_attorney_demo:claim_approval
decision_class_domain = decision_class:sample_attorney_demo:
```

Expected class domain format:

```text
decision_class:<registry_name>:<class_id>
```

### 11.5 Permission validation

Allowed values:

```text
policy_rule,human_approval,system_role,workflow_configuration,tool_permission,prior_decision,emergency_exception,unknown
```

### 11.6 Re-query tests

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

- rollup counts group decisions by class;
- edge query returns descendants of `dec_001`;
- no row requires parsing prose to determine class or parent.

---

## 12. Final v0.3 contract

```text
Spreadsheet columns:
  domain,decision_class_domain,parent_domain,parent_relation_type,key1,value1,key2,value2,key3,value3,permission_source_type,permission_source_id,human_required,human_approver_id,created

One row means:
  one material decision clause record

Mapping:
  domain -> registry and decision identity
  decision_class_domain -> class/group analytics
  parent_domain -> optional parent decision
  parent_relation_type -> relation to parent decision
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

Projection targets:
  cdp_projection.decision_registry_flat
  cdp_projection.decision_class_rollup
  cdp_projection.decision_parent_child_edges

Insert behavior:
  one spreadsheet decision row inserts one database decision row

No hidden magic.
No parent-child inference from prose.
No JSON blob pretending to be hierarchy.
```
