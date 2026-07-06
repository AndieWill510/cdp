-- CDP initial Decision Registry DDL
--
-- Purpose:
--   Establish the irreducible control-plane core: a durable registry of decisions.
--
-- Scope:
--   This is not the full RFC-025 persistence model.
--   It is the first concrete registry table for spreadsheet/demo ingestion.
--
-- Relationship to z_config_lookup:
--   z_config_lookup may remain a staging or compatibility surface.
--   cdp_core.decision_registry is the named control-plane target.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS cdp_core;

CREATE TABLE IF NOT EXISTS cdp_core.decision_registry (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Stable identity for one decision record.
    decision_id TEXT NOT NULL UNIQUE,

    -- Bounded registry or decision set.
    -- Example: decision_register:sample_attorney_demo
    domain TEXT NOT NULL,

    -- Minimal grammatical slots.
    -- Default v0.1 interpretation:
    --   key1/value1 = antecedent
    --   key2/value2 = subject
    --   key3/value3 = predicate
    key1 TEXT NOT NULL,
    value1 TEXT NOT NULL,
    key2 TEXT NOT NULL,
    value2 TEXT NOT NULL,
    key3 TEXT NOT NULL,
    value3 TEXT NOT NULL,

    -- Source-created timestamp from spreadsheet or upstream event.
    created TIMESTAMPTZ NOT NULL,

    -- System ingestion timestamp.
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- Optional source metadata for audit/debugging.
    source_ref TEXT,
    source_row_number INTEGER,

    -- Optional normalized raw row snapshot for replay and diagnostics.
    raw_row JSONB NOT NULL DEFAULT '{}'::jsonb,

    CONSTRAINT chk_decision_registry_decision_id_not_blank
        CHECK (length(trim(decision_id)) > 0),

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
        CHECK (length(trim(value3)) > 0),

    CONSTRAINT chk_decision_registry_source_row_positive
        CHECK (source_row_number IS NULL OR source_row_number > 0)
);

COMMENT ON TABLE cdp_core.decision_registry IS
    'Irreducible CDP control-plane core: a durable registry of material decisions.';

COMMENT ON COLUMN cdp_core.decision_registry.decision_id IS
    'Stable identity for one decision record.';

COMMENT ON COLUMN cdp_core.decision_registry.domain IS
    'Bounded registry or decision set; e.g., decision_register:sample_attorney_demo.';

COMMENT ON COLUMN cdp_core.decision_registry.key1 IS
    'First grammatical key. Default v0.1 meaning: antecedent.';

COMMENT ON COLUMN cdp_core.decision_registry.value1 IS
    'First grammatical value. Default v0.1 meaning: antecedent value.';

COMMENT ON COLUMN cdp_core.decision_registry.key2 IS
    'Second grammatical key. Default v0.1 meaning: subject.';

COMMENT ON COLUMN cdp_core.decision_registry.value2 IS
    'Second grammatical value. Default v0.1 meaning: subject actor.';

COMMENT ON COLUMN cdp_core.decision_registry.key3 IS
    'Third grammatical key. Default v0.1 meaning: predicate.';

COMMENT ON COLUMN cdp_core.decision_registry.value3 IS
    'Third grammatical value. Default v0.1 meaning: predicate/action/object.';

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

CREATE INDEX IF NOT EXISTS idx_decision_registry_source_ref
    ON cdp_core.decision_registry (source_ref)
    WHERE source_ref IS NOT NULL;
