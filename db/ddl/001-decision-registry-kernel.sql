-- CDP Decision Registry Kernel DDL
--
-- Status: starter executable DDL for the first control-plane registry kernel
-- Scope: decision-registry core compatible with spreadsheet/key-value ingestion
--
-- This file intentionally defines the smallest durable control-plane table:
-- one row per material decision clause.
--
-- It does not replace the full RFC-025 persistence model. It gives the demo
-- a concrete registry kernel that can later feed Decision Lifecycle Envelopes,
-- governed records, standing projections, challenge records, and repair paths.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS cdp_core;
CREATE SCHEMA IF NOT EXISTS cdp_projection;

-- -----------------------------------------------------------------------------
-- cdp_core.decision_registry
-- -----------------------------------------------------------------------------
-- The decision registry is the control-plane kernel.
--
-- For v0.2, it preserves the current key/value decision grammar and adds the
-- four attorney-facing governance fields required in the spreadsheet:
--   permission_source_type
--   permission_source_id
--   human_required
--   human_approver_id
--
-- Core convention:
--   domain      = decision_register:<registry_name>:<decision_id>
--   key1/value1 = antecedent
--   key2/value2 = subject
--   key3/value3 = predicate
--
-- This is deliberately stricter than a generic lookup table. A registry table
-- may start from key/value ingestion, but it must make decision identity,
-- validation, ordering, permission traceability, and queryability explicit.

CREATE TABLE IF NOT EXISTS cdp_core.decision_registry (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    domain TEXT NOT NULL,

    key1 TEXT NOT NULL,
    value1 TEXT NOT NULL,

    key2 TEXT NOT NULL,
    value2 TEXT NOT NULL,

    key3 TEXT NOT NULL,
    value3 TEXT NOT NULL,

    permission_source_type TEXT NOT NULL,
    permission_source_id TEXT NOT NULL,
    human_required BOOLEAN NOT NULL,
    human_approver_id TEXT NOT NULL DEFAULT 'none',

    created TIMESTAMPTZ NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    source_system TEXT NOT NULL DEFAULT 'spreadsheet',
    source_ref TEXT,

    row_hash TEXT GENERATED ALWAYS AS (
        encode(
            digest(
                domain || '|' ||
                key1 || '|' || value1 || '|' ||
                key2 || '|' || value2 || '|' ||
                key3 || '|' || value3 || '|' ||
                permission_source_type || '|' || permission_source_id || '|' ||
                human_required::TEXT || '|' || human_approver_id || '|' ||
                created::TEXT,
                'sha256'
            ),
            'hex'
        )
    ) STORED,

    CONSTRAINT chk_decision_registry_domain_format
        CHECK (domain ~ '^decision_register:[A-Za-z0-9_-]+:[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_decision_registry_key1
        CHECK (key1 = 'antecedent'),

    CONSTRAINT chk_decision_registry_key2
        CHECK (key2 = 'subject'),

    CONSTRAINT chk_decision_registry_key3
        CHECK (key3 = 'predicate'),

    CONSTRAINT chk_decision_registry_value1_not_blank
        CHECK (btrim(value1) <> ''),

    CONSTRAINT chk_decision_registry_subject_format
        CHECK (value2 ~ '^(agent|human|system|institution|unknown):[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_decision_registry_predicate_format
        CHECK (value3 ~ '^[A-Za-z][A-Za-z0-9_]*:[A-Za-z][A-Za-z0-9_]*:[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_decision_registry_permission_source_type
        CHECK (permission_source_type IN (
            'policy_rule',
            'human_approval',
            'system_role',
            'workflow_configuration',
            'tool_permission',
            'prior_decision',
            'emergency_exception',
            'unknown'
        )),

    CONSTRAINT chk_decision_registry_permission_source_id_not_blank
        CHECK (btrim(permission_source_id) <> ''),

    CONSTRAINT chk_decision_registry_human_approver_id_not_blank
        CHECK (btrim(human_approver_id) <> ''),

    CONSTRAINT chk_decision_registry_human_approver_when_not_required
        CHECK (human_required OR human_approver_id = 'none'),

    CONSTRAINT uq_decision_registry_domain
        UNIQUE (domain)
);

COMMENT ON TABLE cdp_core.decision_registry IS
'Control-plane kernel: one row per material decision clause ingested into CDP v0.2.';

COMMENT ON COLUMN cdp_core.decision_registry.domain IS
'Decision identity path: decision_register:<registry_name>:<decision_id>.';

COMMENT ON COLUMN cdp_core.decision_registry.key1 IS
'Field name for antecedent. v0.2 requires key1 = antecedent.';

COMMENT ON COLUMN cdp_core.decision_registry.value1 IS
'Antecedent value: condition, trigger, dependency, or none_supplied.';

COMMENT ON COLUMN cdp_core.decision_registry.key2 IS
'Field name for subject. v0.2 requires key2 = subject.';

COMMENT ON COLUMN cdp_core.decision_registry.value2 IS
'Subject value formatted as <actor_type>:<actor_id>.';

COMMENT ON COLUMN cdp_core.decision_registry.key3 IS
'Field name for predicate. v0.2 requires key3 = predicate.';

COMMENT ON COLUMN cdp_core.decision_registry.value3 IS
'Predicate value formatted as <verb>:<object_type>:<object_id>.';

COMMENT ON COLUMN cdp_core.decision_registry.permission_source_type IS
'Attorney-facing permission category, e.g. policy_rule, human_approval, system_role, workflow_configuration, tool_permission, prior_decision, emergency_exception, or unknown.';

COMMENT ON COLUMN cdp_core.decision_registry.permission_source_id IS
'Identifier of the policy, rule, role, workflow, tool permission, prior decision, emergency exception, or unknown permission source.';

COMMENT ON COLUMN cdp_core.decision_registry.human_required IS
'Whether human approval was required before the decision or action could take effect.';

COMMENT ON COLUMN cdp_core.decision_registry.human_approver_id IS
'Human approver ID when applicable; use none when human approval was not required or no approver is recorded.';

COMMENT ON COLUMN cdp_core.decision_registry.row_hash IS
'SHA-256 hash of normalized registry row fields for basic integrity and test assertions.';

CREATE INDEX IF NOT EXISTS idx_decision_registry_created
    ON cdp_core.decision_registry (created);

CREATE INDEX IF NOT EXISTS idx_decision_registry_domain_prefix
    ON cdp_core.decision_registry (domain text_pattern_ops);

CREATE INDEX IF NOT EXISTS idx_decision_registry_subject
    ON cdp_core.decision_registry (value2);

CREATE INDEX IF NOT EXISTS idx_decision_registry_predicate
    ON cdp_core.decision_registry (value3);

CREATE INDEX IF NOT EXISTS idx_decision_registry_permission_source
    ON cdp_core.decision_registry (permission_source_type, permission_source_id);

CREATE INDEX IF NOT EXISTS idx_decision_registry_human_required
    ON cdp_core.decision_registry (human_required, human_approver_id);

-- -----------------------------------------------------------------------------
-- Projection: cdp_projection.decision_registry_flat
-- -----------------------------------------------------------------------------
-- This view derives attorney-readable and test-friendly fields from the strict
-- v0.2 registry format without changing the underlying decision grammar.

CREATE OR REPLACE VIEW cdp_projection.decision_registry_flat AS
SELECT
    id,
    split_part(domain, ':', 2) AS registry_name,
    split_part(domain, ':', 3) AS decision_id,
    domain,
    created,
    value1 AS antecedent,
    split_part(value2, ':', 1) AS subject_type,
    split_part(value2, ':', 2) AS subject_id,
    split_part(value3, ':', 1) AS predicate_verb,
    split_part(value3, ':', 2) AS object_type,
    split_part(value3, ':', 3) AS object_id,
    permission_source_type,
    permission_source_id,
    human_required,
    human_approver_id,
    'Because ' || value1 || ', ' ||
        split_part(value2, ':', 1) || ' ' || split_part(value2, ':', 2) ||
        ' performed ' || split_part(value3, ':', 1) ||
        ' on ' || split_part(value3, ':', 2) || ' ' || split_part(value3, ':', 3) ||
        '. Permission source: ' || permission_source_type || ':' || permission_source_id ||
        '. Human required: ' || human_required::TEXT ||
        '. Human approver: ' || human_approver_id || '.'
        AS plain_english_decision,
    row_hash,
    source_system,
    source_ref,
    ingested_at
FROM cdp_core.decision_registry;

COMMENT ON VIEW cdp_projection.decision_registry_flat IS
'Read projection over the v0.2 decision registry kernel for attorney-facing/demo output.';
