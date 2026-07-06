# Control Plane as Decision Registry

Status: Architectural clarification v0.2  
Scope: CDP control-plane core and first-demo persistence direction  
Audience: implementers, reviewers, attorney-facing demo builders  
Related DDL: `db/ddl/001-decision-registry-kernel.sql`  
Related ingestion contract: `docs/z-config-lookup-spreadsheet-ingestion.md`  

---

## 1. Core claim

Yes.

At its irreducible core, the CDP control plane is a **Decision Registry**.

The control plane may later include governed records, lifecycle envelopes, wire messages, challenge records, standing records, repair records, event logs, projections, payload registries, and controlled vocabularies.

But those are governance surfaces around the central thing:

> a durable registry of decisions.

If CDP cannot answer:

> What decisions exist?

then it does not yet have a control-plane core.

---

## 2. What a Decision Registry means

A Decision Registry is the durable place where every material decision receives:

1. an identity;
2. a bounded domain;
3. a minimal grammatical structure;
4. a permission source surface;
5. a human-approval surface;
6. a created timestamp;
7. a path to later governance.

For the first demo, the minimal grammar is:

```text
antecedent -> subject -> predicate
```

In table terms:

```text
domain
key1/value1
key2/value2
key3/value3
permission_source_type
permission_source_id
human_required
human_approver_id
created
```

Where the recommended default meaning is:

```text
domain                 = decision set and decision identity
key1/value1            = antecedent
key2/value2            = subject
key3/value3            = predicate
permission_source_type = kind of permission source
permission_source_id   = identifier for the source
human_required         = whether human approval was required
human_approver_id      = approver ID, none, or unknown
created                = decision record creation timestamp
```

Decision ID is derived from `domain` for v0.2:

```text
domain = decision_register:<registry_name>:<decision_id>
```

This is not the final CDP schema.

It is the registry spine.

---

## 3. Why `z_config_lookup` is not enough as the architectural noun

`z_config_lookup` may be useful as a temporary compatibility table, staging table, or simple lookup shape.

But `z_config_lookup` is not the architecture.

The architecture is not configuration lookup.

The architecture is decision governance.

Therefore the architectural noun should be:

```text
decision_registry
```

A lookup table can carry the first grammar shape.

It should not define the mental model.

Once the spreadsheet includes the four permission fields, the canonical target should be `cdp_core.decision_registry` unless `z_config_lookup` is explicitly extended.

---

## 4. Minimum viable control-plane DDL

The first executable control-plane DDL should create a real decision registry table.

The table preserves the current lookup-shaped grammar while naming the thing correctly and adding the four attorney-facing permission fields.

The actual starter DDL lives at:

```text
db/ddl/001-decision-registry-kernel.sql
```

It creates:

```text
cdp_core.decision_registry
cdp_projection.decision_registry_flat
```

The control-plane table includes:

```text
id
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
ingested_at
source_system
source_ref
row_hash
```

The projection derives:

```text
registry_name
decision_id
antecedent
subject_type
subject_id
predicate_verb
object_type
object_id
permission_source_type
permission_source_id
human_required
human_approver_id
plain_english_decision
```

This is intentionally not yet the full RFC-025 persistence model.

It is the first concrete registry kernel.

---

## 5. Relationship to `z_config_lookup`

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

That shape can represent:

```text
antecedent -> subject -> predicate
```

It cannot represent the four permission fields unless it is extended.

Those fields are now first-class in the spreadsheet and the registry:

```text
permission_source_type
permission_source_id
human_required
human_approver_id
```

Recommended flow:

```text
spreadsheet -> parser/validator -> cdp_core.decision_registry -> cdp_projection.decision_registry_flat
```

Temporary compatibility flow, if required:

```text
spreadsheet -> parser/validator -> extended z_config_lookup -> cdp_core.decision_registry
```

Do not let a temporary lookup table become the canonical model by accident.

---

## 6. What belongs in the Decision Registry now

For the first demo, the Decision Registry should hold:

| Field | Meaning |
|---|---|
| `domain` | bounded registry and decision identity path |
| `key1/value1` | antecedent |
| `key2/value2` | subject |
| `key3/value3` | predicate |
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

## 7. What does not belong in the Decision Registry yet

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

## 8. Attorney-facing implication

For attorneys, the first useful output is still a Decision Register.

The database table and the attorney-facing spreadsheet are related but not identical.

The database table is the control-plane core.

The attorney-facing register is a review projection.

The attorney should be able to ask:

```text
Show me the decisions in this matter or time period, including what allowed each decision to occur.
```

The control plane should be able to answer from `decision_registry` without parsing logs, guessing from chat transcripts, or asking the model to summarize itself after the fact.

---

## 9. Implementation posture

Build the registry first.

Then build governance around it.

A decision plane without a decision registry is protocol without a floor.

A registry without later governance is only a ledger.

CDP needs both.

But the first concrete DDL should name the floor:

```text
cdp_core.decision_registry
```
