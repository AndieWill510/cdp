# Control Plane as Decision Registry

Status: Architectural clarification  
Scope: CDP control-plane core and first-demo persistence direction  
Audience: implementers, reviewers, attorney-facing demo builders  

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
4. a created timestamp;
5. a path to later governance.

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
created
```

Where the recommended default meaning is:

```text
domain      = decision set and decision identity
key1/value1 = antecedent
key2/value2 = subject
key3/value3 = predicate
created     = decision record creation timestamp
```

This is not the final CDP schema.

It is the registry spine.

---

## 3. Why `z_config_lookup` is not enough as the architectural noun

`z_config_lookup` may be useful as a temporary compatibility table, staging table, or simple lookup shape.

But `z_config_lookup` is not the architecture.

The architecture is not "configuration lookup."

The architecture is decision governance.

Therefore the architectural noun should be:

```text
decision_registry
```

A lookup table can carry the first demo record shape.

It should not define the mental model.

---

## 4. Minimum viable control-plane DDL

The first executable control-plane DDL should create a real decision registry table.

The table can preserve the current lookup-shaped fields while naming the thing correctly.

Recommended first table:

```sql
CREATE SCHEMA IF NOT EXISTS cdp_core;

CREATE TABLE IF NOT EXISTS cdp_core.decision_registry (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Stable decision identity.
    decision_id TEXT NOT NULL UNIQUE,

    -- Bounded registry/domain, for example:
    -- decision_register:sample_attorney_demo
    domain TEXT NOT NULL,

    -- Minimal grammatical slots.
    key1 TEXT NOT NULL,
    value1 TEXT NOT NULL,
    key2 TEXT NOT NULL,
    value2 TEXT NOT NULL,
    key3 TEXT NOT NULL,
    value3 TEXT NOT NULL,

    -- Source-created timestamp from spreadsheet or upstream event.
    created TIMESTAMPTZ NOT NULL,

    -- Ingestion timestamp.
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- Optional source metadata for audit/debugging.
    source_ref TEXT,
    source_row_number INTEGER,

    -- Optional raw normalized row, useful for replay and test diagnostics.
    raw_row JSONB NOT NULL DEFAULT '{}'::jsonb,

    CONSTRAINT chk_decision_registry_domain_not_blank
        CHECK (length(trim(domain)) > 0),

    CONSTRAINT chk_decision_registry_key1_not_blank
        CHECK (length(trim(key1)) > 0),

    CONSTRAINT chk_decision_registry_value1_not_blank
        CHECK (length(trim(value1)) > 0),

    CONSTRAINT chk_decision_registry_key2_not_blank
        CHECK (length(trim(key2)) > 0),

    CONSTRAINT chk_decision_registry_value2_not_blank
        CHECK (length(trim(value2)) > 0),

    CONSTRAINT chk_decision_registry_key3_not_blank
        CHECK (length(trim(key3)) > 0),

    CONSTRAINT chk_decision_registry_value3_not_blank
        CHECK (length(trim(value3)) > 0)
);

CREATE INDEX IF NOT EXISTS idx_decision_registry_domain
    ON cdp_core.decision_registry (domain);

CREATE INDEX IF NOT EXISTS idx_decision_registry_created
    ON cdp_core.decision_registry (created);

CREATE INDEX IF NOT EXISTS idx_decision_registry_key1
    ON cdp_core.decision_registry (key1, value1);

CREATE INDEX IF NOT EXISTS idx_decision_registry_key2
    ON cdp_core.decision_registry (key2, value2);

CREATE INDEX IF NOT EXISTS idx_decision_registry_key3
    ON cdp_core.decision_registry (key3, value3);
```

This is intentionally not yet the full RFC-025 persistence model.

It is the first concrete registry table.

---

## 5. Relationship to `z_config_lookup`

If the current implementation already has this shape:

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

then `z_config_lookup` can be treated as a temporary staging table or compatibility adapter.

But the first control-plane DDL should make the target explicit:

```text
cdp_core.decision_registry
```

Recommended flow:

```text
spreadsheet -> parser/validator -> decision_registry
```

Temporary compatibility flow, if needed:

```text
spreadsheet -> parser/validator -> z_config_lookup -> decision_registry
```

Do not let the temporary table become the canonical model by accident.

---

## 6. What belongs in the Decision Registry now

For the first demo, the Decision Registry should hold:

| Field | Meaning |
|---|---|
| `decision_id` | stable identity for one decision record |
| `domain` | bounded registry or decision set |
| `key1/value1` | antecedent |
| `key2/value2` | subject |
| `key3/value3` | predicate |
| `created` | decision record timestamp |
| `ingested_at` | system ingestion timestamp |
| `source_ref` | optional spreadsheet/file/batch reference |
| `source_row_number` | optional row number for error repair |
| `raw_row` | optional normalized row snapshot |

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
- human approval records;
- evidence records;
- policy references;
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
Show me the decisions in this matter or time period.
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
