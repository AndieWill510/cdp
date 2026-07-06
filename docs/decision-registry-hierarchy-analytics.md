# Decision Registry Hierarchy and Analytics

Status: design note v0.3  
Scope: parent-child decision lineage and class/group analytics  
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

## 2. Class hierarchy

A decision class is a stable category used for grouping and analytics.

Examples:

```text
decision_class:sample_attorney_demo:claim
decision_class:sample_attorney_demo:claim_intake
decision_class:sample_attorney_demo:claim_approval
decision_class:sample_attorney_demo:human_review_escalation
decision_class:sample_attorney_demo:access
decision_class:sample_attorney_demo:access_denial
```

Class rows may be stored in:

```text
cdp_core.decision_class_registry
```

A decision row points to a class using:

```text
decision_class_domain
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

## 3. Decision lineage

A parent decision is a specific prior decision that the current decision depends on, escalates from, approves, denies, repairs, appeals, or supersedes.

A decision row uses:

```text
parent_domain
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

Allowed v0.3 relation types:

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
parent_relation_type = none  -> parent_domain must be blank/null
parent_relation_type != none -> parent_domain must be populated
```

---

## 4. Why this should not be prose

Do not hide class or parent-child structure inside `antecedent`, `predicate`, notes, or rationale prose.

Bad:

```text
value1 = this was a claim approval related to dec_003
```

Better:

```text
decision_class_domain = decision_class:sample_attorney_demo:claim_approval
parent_domain = decision_register:sample_attorney_demo:dec_003
parent_relation_type = approves
value1 = prior decision dec_003 escalated claim
```

Prose helps humans.

Columns help analytics.

CDP needs both.

---

## 5. Spreadsheet fields

The v0.3 spreadsheet adds:

```text
decision_class_domain
parent_domain
parent_relation_type
```

These sit beside the existing grammar and permission fields:

```text
domain,decision_class_domain,parent_domain,parent_relation_type,key1,value1,key2,value2,key3,value3,permission_source_type,permission_source_id,human_required,human_approver_id,created
```

This keeps the spreadsheet flat enough for non-engineers while making parent-child analytics possible.

---

## 6. Analytics views

The v0.3 DDL exposes three read surfaces.

### 6.1 Flat registry

```text
cdp_projection.decision_registry_flat
```

Use for attorney-facing review.

### 6.2 Class rollup

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

### 6.3 Parent-child edges

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

## 7. Relationship to `z_config_lookup`

A `z_config_lookup`-style table can support this pattern only if it can carry the extra hierarchy fields:

```text
decision_class_domain
parent_domain
parent_relation_type
```

If it cannot, then `z_config_lookup` can only be a staging/compatibility table for the older flat grammar.

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

## 8. Design rule

Use columns for structure.

Use prose for explanation.

Use classes for categories.

Use parent domains for lineage.

Use projections for attorney-facing views.

Do not ask future code to infer hierarchy from words.
