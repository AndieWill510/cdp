# Control Plane as Decision Registry

Status: Architectural clarification v0.4  
Scope: CDP control-plane core and first-demo persistence direction  
Audience: implementers, reviewers, attorney-facing demo builders  
Related DDL: `db/ddl/001-decision-registry-kernel.sql`  
Related ingestion contract: `docs/z-config-lookup-spreadsheet-ingestion.md`  
Related analytics note: `docs/decision-registry-hierarchy-analytics.md`  

---

## 1. Core claim

At its irreducible core, the CDP control plane is a **Decision Registry**.

The control plane may later include governed records, lifecycle envelopes, wire messages, challenge records, standing records, repair records, event logs, projections, payload registries, and controlled vocabularies.

But those are governance surfaces around the central thing:

> a durable registry of decisions.

If CDP cannot answer:

> What decisions exist?

then it does not yet have a control-plane core.

If CDP cannot also answer:

> What kinds of decisions exist, and how do they relate?

then it does not yet have a useful analytic control-plane surface.

---

## 2. Normal form correction

Earlier drafts used a compact key/value shape:

```text
domain
key1/value1
key2/value2
key3/value3
```

and packed values such as:

```text
agent:claims_review_agent
recommend_approval:claim:claim_9981
decision_register:sample_attorney_demo:dec_001
```

That is not the right core database model.

It is too close to an entity-attribute-value or lookup-table pattern, and it asks future code to parse meaning out of strings.

The v0.4 registry corrects that by storing atomic columns in the core table and deriving compatibility strings only in views.

---

## 3. What a normalized Decision Registry means

A normalized Decision Registry is the durable place where every material decision receives:

1. an atomic registry name;
2. an atomic decision ID;
3. an atomic class/category ID;
4. an optional atomic parent decision ID;
5. a relation to the parent decision;
6. a plain antecedent text surface;
7. atomic subject actor type and actor ID;
8. atomic predicate verb, object type, and object ID;
9. atomic permission source fields;
10. a human-approval surface;
11. a created timestamp;
12. a path to later governance.

In table terms:

```text
registry_name
decision_id
decision_class_id
parent_decision_id
parent_relation_type
antecedent_text
subject_actor_type
subject_actor_id
predicate_verb
object_type
object_id
permission_source_type
permission_source_id
human_required
human_approver_id
created
```

Compatibility display strings can be derived:

```text
decision_domain = decision_register:<registry_name>:<decision_id>
decision_class_domain = decision_class:<registry_name>:<decision_class_id>
```

But those strings are not authoritative stored fields.

---

## 4. Why `z_config_lookup` is not enough as the architectural noun

`z_config_lookup` may be useful as a temporary compatibility table, staging table, or simple lookup shape.

But `z_config_lookup` is not the architecture.

The architecture is not configuration lookup.

The architecture is decision governance.

Therefore the architectural noun should be:

```text
decision_registry
```

A lookup table can carry an early sketch.

It should not define the mental model.

The canonical target should be:

```text
cdp_core.decision_registry
```

---

## 5. Minimum viable control-plane DDL

The first executable control-plane DDL should create a real normalized decision registry table.

The actual starter DDL lives at:

```text
db/ddl/001-decision-registry-kernel.sql
```

It creates:

```text
cdp_core.decision_class_registry
cdp_core.decision_registry
cdp_projection.decision_class_registry_flat
cdp_projection.decision_registry_flat
cdp_projection.decision_class_rollup
cdp_projection.decision_parent_child_edges
```

The core table stores normalized facts.

The projection views derive attorney-facing and compatibility surfaces.

This is intentionally not yet the full RFC-025 persistence model.

It is the first concrete normalized registry kernel.

---

## 6. Relationship to `z_config_lookup`

The older compatibility shape is:

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

That shape can represent a rough early sketch:

```text
antecedent -> subject -> predicate
```

But it violates the normalized direction because:

- `domain` packed registry and decision ID;
- `key1/key2/key3` stored field names as row data;
- `value2` packed actor type and actor ID;
- `value3` packed verb, object type, and object ID.

That is no longer acceptable for the canonical control-plane table.

Recommended flow:

```text
spreadsheet -> parser/validator -> cdp_core.decision_class_registry
spreadsheet -> parser/validator -> cdp_core.decision_registry
registry -> projections
```

Temporary compatibility flow, if required:

```text
legacy lookup-shaped spreadsheet -> parser/validator -> normalized decision_registry
```

Do not let a temporary lookup table become the canonical model by accident.

---

## 7. What belongs in the Decision Registry now

For the first demo, the Decision Registry should hold:

| Field | Meaning |
|---|---|
| `registry_name` | bounded registry name |
| `decision_id` | stable decision ID within registry |
| `decision_class_id` | class/group for analytics |
| `parent_decision_id` | optional parent decision ID |
| `parent_relation_type` | relationship to the parent decision |
| `antecedent_text` | antecedent or `none_supplied` |
| `subject_actor_type` | actor type |
| `subject_actor_id` | actor ID |
| `predicate_verb` | decision/action verb |
| `object_type` | affected object type |
| `object_id` | affected object ID |
| `permission_source_type` | category of permission source |
| `permission_source_id` | specific source identifier |
| `human_required` | whether human approval was required |
| `human_approver_id` | approver ID, `none`, or `unknown` |
| `created` | decision record timestamp |
| `ingested_at` | system ingestion timestamp |
| `source_system` | source category, default `spreadsheet` |
| `source_ref` | optional spreadsheet/file/batch reference |
| `row_hash` | integrity/test hash over normalized row fields |

This keeps the table small but honest.

---

## 8. What does not belong in the Decision Registry yet

Do not force the whole future governance model into the first table.

These are important, but later:

- full Decision Lifecycle Envelope;
- Wire Message Envelope;
- governed record body;
- standing determinations;
- recusal control;
- evidence records;
- policy reference records;
- tool-call audit records;
- appeal and repair records;
- controlled vocabulary registry;
- event replay table.

Those may become separate CDP tables.

The registry should remain the spine, not the junk drawer.

---

## 9. Attorney-facing implication

For attorneys, the first useful output is still a Decision Register.

The database table and the attorney-facing spreadsheet are related but not identical.

The database table is the normalized control-plane core.

The attorney-facing register is a review projection.

The attorney should be able to ask:

```text
Show me the decisions in this matter or time period, including what allowed each decision to occur and what class of decision it was.
```

The control plane should be able to answer from `decision_registry` without parsing logs, guessing from chat transcripts, or asking the model to summarize itself after the fact.

---

## 10. Analytics implication

The registry should support questions such as:

```text
How many access denials occurred?
How many claim approvals required a human?
Which decision classes have unknown permission sources?
Which decisions descended from this prior recommendation?
Which decisions repaired, appealed, or superseded earlier decisions?
```

Those questions need explicit columns and projections.

They should not require prose parsing or colon-delimited string parsing.

---

## 11. Implementation posture

Build the normalized registry first.

Then build analytics over it.

Then build governance around it.

A decision plane without a decision registry is protocol without a floor.

A registry without normalization is a clever spreadsheet.

A registry without hierarchy is a flat ledger.

A registry without later governance is only an inventory.

CDP needs all of it: normalized registry, hierarchy, and governance.
