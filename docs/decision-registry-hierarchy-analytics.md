# Decision Registry Hierarchy and Analytics

Status: design note v0.4  
Scope: normalized parent-child decision lineage and class/group analytics  
Related DDL: `db/ddl/001-decision-registry-kernel.sql`  
Related ingestion contract: `docs/z-config-lookup-spreadsheet-ingestion.md`  

---

## 1. Core idea

The Decision Registry should not only answer:

```text
What decisions were made?
```

It should also answer:

```text
What kinds of decisions were made?
How are decisions grouped?
Which decisions descend from other decisions?
Which decision classes create the most human-review burden?
Which decision classes contain unknown permission sources?
```

That requires two separate hierarchy surfaces:

1. **Class hierarchy** — what kind of decision is this?
2. **Decision lineage** — what parent decision does this decision descend from or relate to?

Do not collapse these into one field.

A class is a category.

A parent decision is a lineage relationship.

---

## 2. Normal form correction

Earlier drafts used packed domain strings such as:

```text
decision_register:sample_attorney_demo:dec_001
decision_class:sample_attorney_demo:claim_approval
```

and packed actor/predicate values such as:

```text
agent:claims_review_agent
recommend_approval:claim:claim_9981
```

Those are useful display strings, but they violate the normalized shape we want for the control-plane table.

The core registry now stores atomic columns:

```text
registry_name
decision_id
decision_class_id
parent_decision_id
subject_actor_type
subject_actor_id
predicate_verb
object_type
object_id
```

Compatibility strings may be generated in views.

They are not authoritative stored fields.

---

## 3. Class hierarchy

A decision class is a stable category used for grouping and analytics.

In normalized form, class rows use:

```text
registry_name
class_id
parent_class_id
class_label
class_level
```

Examples:

```text
registry_name = sample_attorney_demo
class_id = claim
parent_class_id = <null>
class_label = Claim Decisions
class_level = 0
```

```text
registry_name = sample_attorney_demo
class_id = claim_approval
parent_class_id = claim
class_label = Claim Approval
class_level = 1
```

The class registry supports parent-child class structure:

```text
claim
  claim_intake
  claim_approval
  human_review_escalation

access
  access_denial
```

This allows rollups such as:

```text
all claim decisions
all access decisions
all claim approvals
all human-review escalations
```

---

## 4. Decision lineage

A parent decision is a specific prior decision that the current decision depends on, escalates from, approves, denies, repairs, appeals, or supersedes.

A decision row uses:

```text
parent_decision_id
parent_relation_type
```

Examples:

| Decision | Parent | Relation |
|---|---|---|
| `dec_003` escalates a claim | `dec_001` agent recommendation | `escalates_from` |
| `dec_004` human approval | `dec_003` escalation | `approves` |
| `dec_010` appeal | `dec_002` denial | `appeal_of` |
| `dec_011` repair | `dec_002` denial | `repair_of` |
| `dec_020` corrected result | `dec_002` denial | `supersedes` |

Allowed v0.4 relation types:

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

```text
parent_relation_type = none  -> parent_decision_id must be blank/null
parent_relation_type != none -> parent_decision_id must be populated
```

---

## 5. Why this should not be prose

Do not hide class or parent-child structure inside `antecedent_text`, `predicate_verb`, notes, or rationale prose.

Bad:

```text
antecedent_text = this was a claim approval related to dec_003
```

Better:

```text
decision_class_id = claim_approval
parent_decision_id = dec_003
parent_relation_type = approves
antecedent_text = prior decision dec_003 escalated claim
```

Prose helps humans.

Columns help analytics.

CDP needs both.

---

## 6. Spreadsheet fields

The v0.4 spreadsheet uses atomic fields:

```text
registry_name,decision_id,decision_class_id,parent_decision_id,parent_relation_type,antecedent_text,subject_actor_type,subject_actor_id,predicate_verb,object_type,object_id,permission_source_type,permission_source_id,human_required,human_approver_id,created
```

This keeps the spreadsheet flat enough for non-engineers while making parent-child analytics possible without parsing packed strings.

---

## 7. Analytics views

The v0.4 DDL exposes four read surfaces.

### 7.1 Class registry flat view

```text
cdp_projection.decision_class_registry_flat
```

Use when a display/export surface wants compatibility strings such as:

```text
decision_class:sample_attorney_demo:claim_approval
```

Those strings are derived from atomic columns.

### 7.2 Flat decision registry

```text
cdp_projection.decision_registry_flat
```

Use for attorney-facing review.

### 7.3 Class rollup

```text
cdp_projection.decision_class_rollup
```

Use for grouping questions:

```sql
SELECT decision_class_id,
       decision_count,
       human_required_count,
       unknown_permission_count
FROM cdp_projection.decision_class_rollup
WHERE registry_name = 'sample_attorney_demo'
ORDER BY decision_count DESC;
```

### 7.4 Parent-child edges

```text
cdp_projection.decision_parent_child_edges
```

Use for lineage and graph questions:

```sql
SELECT parent_decision_id,
       child_decision_id,
       parent_relation_type
FROM cdp_projection.decision_parent_child_edges
WHERE parent_decision_id = 'dec_001';
```

---

## 8. Relationship to `z_config_lookup`

A `z_config_lookup`-style table is not the right canonical model for this version because it encourages key/value slots and packed values.

It can be retained only as a staging adapter if it maps into normalized registry fields before control-plane insertion.

The canonical analytics target should be:

```text
cdp_core.decision_registry
```

and the canonical analytics projections should be:

```text
cdp_projection.decision_class_rollup
cdp_projection.decision_parent_child_edges
```

---

## 9. Design rule

Use columns for structure.

Use prose for explanation.

Use classes for categories.

Use parent IDs for lineage.

Use views for compatibility strings.

Do not ask future code to infer hierarchy from words or parse colon-delimited values from core tables.
