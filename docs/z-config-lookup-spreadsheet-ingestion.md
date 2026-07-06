# Spreadsheet Ingestion Contract for the Normalized Decision Registry

Status: Demo ingestion contract v0.5  
Scope: Identifier registry, class registry, and decision registry spreadsheet ingestion  
Audience: implementers, test authors, attorney-facing demo builders  
Related DDL: `db/ddl/001-decision-registry-kernel.sql`  
Related design note: `docs/identifier-registry.md`  

---

## 1. Purpose

This document defines the spreadsheet ingestion sequence for the normalized CDP control-plane registry.

The canonical targets are:

```text
cdp_core.identifier_registry
cdp_core.decision_class_registry
cdp_core.decision_registry
```

The old `z_config_lookup` / key-value idea is not the canonical control-plane model.

The canonical model uses atomic columns and a no-floating-ID identifier registry.

---

## 2. Ingestion order

Load spreadsheets in this order:

```text
1. identifier_registry seed rows
2. decision_class_registry rows
3. additional identifier_registry rows for actors, objects, policies, tools, etc.
4. decision_registry rows
5. projection queries
```

Why this order?

Because `decision_registry` rows are validated against `identifier_registry` and `decision_class_registry`.

A decision row that references an actor, object, predicate, permission source, source system, or relation type must not insert unless those identifiers already exist.

No floating IDs.

---

## 3. Identifier registry spreadsheet

Target table:

```text
cdp_core.identifier_registry
```

Required header:

```text
registry_name,identifier_id,identifier_type_registry_name,identifier_type_id,parent_registry_name,parent_identifier_id,display_label,description,status,created
```

Field rules:

| Column | Required | Meaning |
|---|---:|---|
| `registry_name` | yes | Identifier namespace, e.g. `actor`, `object`, `permission_source` |
| `identifier_id` | yes | Atomic ID within registry |
| `identifier_type_registry_name` | conditional | Registry that types this identifier |
| `identifier_type_id` | conditional | Type ID within type registry |
| `parent_registry_name` | conditional | Optional parent identifier registry |
| `parent_identifier_id` | conditional | Optional parent identifier ID |
| `display_label` | yes | Human-readable label |
| `description` | no | Explanation |
| `status` | yes | `active`, `deprecated`, `inactive`, or `retired` |
| `created` | yes | ISO timestamp or date |

Pairing rules:

```text
identifier_type_registry_name and identifier_type_id must both be blank or both populated.
parent_registry_name and parent_identifier_id must both be blank or both populated.
```

Decision validation accepts identifiers whose status is:

```text
active
deprecated
```

It rejects:

```text
inactive
retired
missing rows
```

### Minimal identifier fixture

The DDL seeds the minimum registry rows and demo identifiers.

Additional fixture rows can be loaded when the sample decisions introduce new actors, objects, policies, tools, or source systems.

Example additional object:

```csv
registry_name,identifier_id,identifier_type_registry_name,identifier_type_id,parent_registry_name,parent_identifier_id,display_label,description,status,created
object,claim_9999,object_type,claim,,,Claim 9999,Additional demo claim object,active,2026-07-06T18:00:00Z
```

---

## 4. Decision class spreadsheet

Target table:

```text
cdp_core.decision_class_registry
```

Required header:

```text
registry_name,class_id,parent_class_id,class_label,class_level,created
```

Example fixture:

```csv
registry_name,class_id,parent_class_id,class_label,class_level,created
sample_attorney_demo,claim,,Claim Decisions,0,2026-07-06T18:00:00Z
sample_attorney_demo,claim_intake,claim,Claim Intake,1,2026-07-06T18:00:00Z
sample_attorney_demo,claim_approval,claim,Claim Approval,1,2026-07-06T18:00:00Z
sample_attorney_demo,human_review_escalation,claim,Human Review Escalation,1,2026-07-06T18:00:00Z
sample_attorney_demo,access,,Access Decisions,0,2026-07-06T18:00:00Z
sample_attorney_demo,access_denial,access,Access Denial,1,2026-07-06T18:00:00Z
```

Blank `parent_class_id` should be normalized to SQL `NULL`.

---

## 5. Decision spreadsheet

Target table:

```text
cdp_core.decision_registry
```

Required header:

```text
registry_name,decision_id,decision_class_id,parent_decision_id,parent_relation_type,antecedent_text,subject_actor_type,subject_actor_id,predicate_verb,object_type,object_id,permission_source_type,permission_source_id,human_required,human_approver_id,created
```

Example fixture:

```csv
registry_name,decision_id,decision_class_id,parent_decision_id,parent_relation_type,antecedent_text,subject_actor_type,subject_actor_id,predicate_verb,object_type,object_id,permission_source_type,permission_source_id,human_required,human_approver_id,created
sample_attorney_demo,dec_001,claim_intake,,none,claim submitted,agent,claims_review_agent,recommend_approval,claim,claim_9981,policy_rule,policy_claims_approval_v2,yes,user_442,2026-07-06T18:42:11Z
sample_attorney_demo,dec_002,access_denial,,none,identity verification failed,agent,access_agent,deny_access,access_request,access_7731,workflow_configuration,workflow_access_v1,no,none,2026-07-06T18:44:09Z
sample_attorney_demo,dec_003,human_review_escalation,dec_001,escalates_from,claim amount exceeded auto-approval threshold,agent,claims_review_agent,escalate_review,claim,claim_9982,policy_rule,policy_claims_approval_v2,yes,unknown,2026-07-06T18:45:33Z
sample_attorney_demo,dec_004,claim_approval,dec_003,approves,prior decision dec_003 escalated claim,human,user_442,approve_review,claim,claim_9982,human_approval,user_442,yes,user_442,2026-07-06T18:52:10Z
```

---

## 6. Decision validation rules

A decision row is valid when:

1. `registry_name`, `decision_id`, and `decision_class_id` are simple atomic IDs.
2. `(registry_name, decision_class_id)` exists in `decision_class_registry`.
3. If `parent_relation_type = none`, `parent_decision_id` is blank/null.
4. If `parent_relation_type != none`, `parent_decision_id` is populated and references an existing decision in the same registry.
5. `parent_relation_type` exists in `identifier_registry` under `parent_relation_type`.
6. `subject_actor_type` exists in `identifier_registry` under `actor_type`.
7. `subject_actor_id` exists in `identifier_registry` under `actor` and is typed by `subject_actor_type`.
8. `predicate_verb` exists in `identifier_registry` under `predicate_verb`.
9. `object_type` exists in `identifier_registry` under `object_type`.
10. `object_id` exists in `identifier_registry` under `object` and is typed by `object_type`.
11. `permission_source_type` exists in `identifier_registry` under `permission_source_type`.
12. `permission_source_id` exists in `identifier_registry` under `permission_source` and is typed by `permission_source_type`.
13. `human_required` is normalized to Boolean.
14. `human_approver_id = none` is allowed only when human approval is not required or no approver is recorded.
15. `human_approver_id = unknown` must exist as an unknown actor.
16. Any other `human_approver_id` must exist as an actor typed `human`.
17. `source_system` defaults to `spreadsheet` and must exist in `identifier_registry` under `source_system`.

The database trigger performs these checks at insert/update time.

---

## 7. Normal form rule

The v0.5 registry is normalized. It does not use:

```text
domain
key1/value1
key2/value2
key3/value3
actor_type:actor_id
verb:object_type:object_id
```

Compatibility strings such as:

```text
decision_register:<registry_name>:<decision_id>
decision_class:<registry_name>:<class_id>
identifier:<registry_name>:<identifier_id>
```

may still appear in projection views.

They are not authoritative stored fields.

---

## 8. Analytics targets

The DDL exposes these read surfaces:

```text
cdp_projection.identifier_registry_flat
cdp_projection.decision_class_registry_flat
cdp_projection.decision_registry_flat
cdp_projection.decision_class_rollup
cdp_projection.decision_parent_child_edges
```

Use `decision_registry_flat` for attorney-facing review rows.

Use `decision_class_rollup` for class counts, human-review burden, and unknown-permission findings.

Use `decision_parent_child_edges` for lineage and graph/tree analysis.

Use `identifier_registry_flat` to inspect registered IDs and their types.

---

## 9. Unit test plan

### 9.1 Happy path

Input:

- valid identifier rows;
- valid class rows;
- valid decision rows.

Expected:

- identifiers insert;
- classes insert;
- decisions insert;
- no validation errors;
- flat projection returns attorney-readable rows;
- rollup projection groups decisions by class;
- edge projection returns parent-child lineage.

### 9.2 Missing identifier failures

Expected failures:

```text
subject_actor_id = unregistered_agent
object_id = unregistered_claim
predicate_verb = unregistered_action
permission_source_id = unregistered_policy
source_system = unregistered_loader
```

### 9.3 Mistyped identifier failures

Expected failures:

```text
subject_actor_id = user_442 with subject_actor_type = agent
object_id = claim_9981 with object_type = access_request
permission_source_id = workflow_access_v1 with permission_source_type = policy_rule
human_approver_id = claims_review_agent
```

### 9.4 Normal form failures

Expected failures before insert:

```text
subject_actor_id = agent:claims_review_agent
predicate_verb = recommend_approval:claim:claim_9981
registry_name = decision_register:sample_attorney_demo:dec_001
decision_class_id = decision_class:sample_attorney_demo:claim_approval
```

---

## 10. Final v0.5 contract

```text
Identifier registry:
  cdp_core.identifier_registry

Decision classes:
  cdp_core.decision_class_registry

Decisions:
  cdp_core.decision_registry

Generic config:
  cdp_core.config_lookup

No hidden magic.
No key/value pseudo-columns.
No packed colon-delimited facts in core tables.
No parent-child inference from prose.
No floating IDs.
```
