-- CDP Decision Registry Kernel DDL
--
-- Status: starter executable DDL for the first control-plane registry kernel
-- Scope: decision-registry core compatible with spreadsheet/key-value ingestion
--
-- This file intentionally defines the smallest durable control-plane kernel:
-- one row per material decision clause, plus lightweight classification and
-- parent-child surfaces for analytics.
--
-- It does not replace the full RFC-025 persistence model. It gives the demo
-- a concrete registry kernel that can later feed Decision Lifecycle Envelopes,
-- governed records, standing projections, challenge records, and repair paths.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS cdp_core;
CREATE SCHEMA IF NOT EXISTS cdp_projection;

-- -----------------------------------------------------------------------------
-- cdp_core.decision_class_registry
-- -----------------------------------------------------------------------------
-- Lightweight classification registry for decision analytics.
--
-- This table lets a demo define parent-child classes such as:
--   decision_class:sample_attorney_demo:claim
--   decision_class:sample_attorney_demo:claim_approval
--   decision_class:sample_attorney_demo:claim_escalation
--
-- Decision rows soft-reference class domains through decision_class_domain.
-- Soft reference is intentional for v0.3 so spreadsheet ingestion order does not
-- have to load class rows before decision rows. Later profiles may harden this.

CREATE TABLE IF NOT EXISTS cdp_core.decision_class_registry (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    domain TEXT NOT NULL UNIQUE,
    parent_domain TEXT,

    class_id TEXT NOT NULL,
    class_label TEXT NOT NULL,
    class_level INTEGER NOT NULL DEFAULT 0,

    created TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_decision_class_domain_format
        CHECK (domain ~ '^decision_class:[A-Za-z0-9_-]+:[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_decision_class_parent_domain_format
        CHECK (parent_domain IS NULL OR parent_domain ~ '^decision_class:[A-Za-z0-9_-]+:[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_decision_class_id_not_blank
        CHECK (btrim(class_id) <> ''),

    CONSTRAINT chk_decision_class_label_not_blank
        CHECK (btrim(class_label) <> ''),

    CONSTRAINT chk_decision_class_level_nonnegative
        CHECK (class_level >= 0)
);

COMMENT ON TABLE cdp_core.decision_class_registry IS
'Lightweight parent-child classification registry for decision analytics.';

CREATE INDEX IF NOT EXISTS idx_decision_class_parent_domain
    ON cdp_core.decision_class_registry (parent_domain);

CREATE INDEX IF NOT EXISTS idx_decision_class_level
    ON cdp_core.decision_class_registry (class_level);

-- -----------------------------------------------------------------------------
-- cdp_core.decision_registry
-- -----------------------------------------------------------------------------
-- The decision registry is the control-plane kernel.
--
-- For v0.3, it preserves the current key/value decision grammar, includes the
-- four attorney-facing governance fields, and adds lightweight hierarchy fields
-- for class/group analytics and parent-child decision lineage.
--
-- Core convention:
--   domain                = decision_register:<registry_name>:<decision_id>
--   decision_class_domain = decision_class:<registry_name>:<class_id>
--   parent_domain         = optional parent decision domain
--   parent_relation_type  = relation from this decision to parent_domain
--   key1/value1           = antecedent
--   key2/value2           = subject
--   key3/value3           = predicate
--
-- This is deliberately stricter than a generic lookup table. A registry table
-- may start from key/value ingestion, but it must make decision identity,
-- validation, ordering, permission traceability, hierarchy, and queryability
-- explicit.

CREATE TABLE IF NOT EXISTS cdp_core.decision_registry (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    domain TEXT NOT NULL,
    decision_class_domain TEXT NOT NULL,
    parent_domain TEXT,
    parent_relation_type TEXT NOT NULL DEFAULT 'none',

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
                decision_class_domain || '|' || coalesce(parent_domain, '') || '|' || parent_relation_type || '|' ||
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

    CONSTRAINT chk_decision_registry_class_domain_format
        CHECK (decision_class_domain ~ '^decision_class:[A-Za-z0-9_-]+:[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_decision_registry_parent_domain_format
        CHECK (parent_domain IS NULL OR parent_domain ~ '^decision_register:[A-Za-z0-9_-]+:[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_decision_registry_parent_relation_type
        CHECK (parent_relation_type IN (
            'none',
            'child_of',
            'depends_on',
            'derived_from',
            'escalates_from',
            'approves',
            'denies',
            'appeal_of',
            'repair_of',
            'supersedes'
        )),

    CONSTRAINT chk_decision_registry_parent_pairing
        CHECK (
            (parent_relation_type = 'none' AND parent_domain IS NULL)
            OR
            (parent_relation_type <> 'none' AND parent_domain IS NOT NULL)
        ),

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
'Control-plane kernel: one row per material decision clause ingested into CDP v0.3.';

COMMENT ON COLUMN cdp_core.decision_registry.domain IS
'Decision identity path: decision_register:<registry_name>:<decision_id>.';

COMMENT ON COLUMN cdp_core.decision_registry.decision_class_domain IS
'Classification path for analytics: decision_class:<registry_name>:<class_id>.';

COMMENT ON COLUMN cdp_core.decision_registry.parent_domain IS
'Optional parent decision domain for parent-child decision lineage.';

COMMENT ON COLUMN cdp_core.decision_registry.parent_relation_type IS
'Relationship from this decision to parent_domain, such as child_of, depends_on, escalates_from, appeal_of, or repair_of.';

COMMENT ON COLUMN cdp_core.decision_registry.key1 IS
'Field name for antecedent. v0.3 requires key1 = antecedent.';

COMMENT ON COLUMN cdp_core.decision_registry.value1 IS
'Antecedent value: condition, trigger, dependency, or none_supplied.';

COMMENT ON COLUMN cdp_core.decision_registry.key2 IS
'Field name for subject. v0.3 requires key2 = subject.';

COMMENT ON COLUMN cdp_core.decision_registry.value2 IS
'Subject value formatted as <actor_type>:<actor_id>.';

COMMENT ON COLUMN cdp_core.decision_registry.key3 IS
'Field name for predicate. v0.3 requires key3 = predicate.';

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

CREATE INDEX IF NOT EXISTS idx_decision_registry_class_domain
    ON cdp_core.decision_registry (decision_class_domain);

CREATE INDEX IF NOT EXISTS idx_decision_registry_parent_domain
    ON cdp_core.decision_registry (parent_domain);

CREATE INDEX IF NOT EXISTS idx_decision_registry_parent_relation
    ON cdp_core.decision_registry (parent_relation_type, parent_domain);

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
-- v0.3 registry format without changing the underlying decision grammar.

CREATE OR REPLACE VIEW cdp_projection.decision_registry_flat AS
SELECT
    d.id,
    split_part(d.domain, ':', 2) AS registry_name,
    split_part(d.domain, ':', 3) AS decision_id,
    d.domain,
    d.decision_class_domain,
    split_part(d.decision_class_domain, ':', 3) AS decision_class_id,
    c.parent_domain AS parent_class_domain,
    c.class_label AS decision_class_label,
    c.class_level AS decision_class_level,
    d.parent_domain,
    split_part(d.parent_domain, ':', 3) AS parent_decision_id,
    d.parent_relation_type,
    d.created,
    d.value1 AS antecedent,
    split_part(d.value2, ':', 1) AS subject_type,
    split_part(d.value2, ':', 2) AS subject_id,
    split_part(d.value3, ':', 1) AS predicate_verb,
    split_part(d.value3, ':', 2) AS object_type,
    split_part(d.value3, ':', 3) AS object_id,
    d.permission_source_type,
    d.permission_source_id,
    d.human_required,
    d.human_approver_id,
    'Because ' || d.value1 || ', ' ||
        split_part(d.value2, ':', 1) || ' ' || split_part(d.value2, ':', 2) ||
        ' performed ' || split_part(d.value3, ':', 1) ||
        ' on ' || split_part(d.value3, ':', 2) || ' ' || split_part(d.value3, ':', 3) ||
        '. Class: ' || split_part(d.decision_class_domain, ':', 3) ||
        '. Parent relation: ' || d.parent_relation_type ||
        coalesce(' -> ' || split_part(d.parent_domain, ':', 3), '') ||
        '. Permission source: ' || d.permission_source_type || ':' || d.permission_source_id ||
        '. Human required: ' || d.human_required::TEXT ||
        '. Human approver: ' || d.human_approver_id || '.'
        AS plain_english_decision,
    d.row_hash,
    d.source_system,
    d.source_ref,
    d.ingested_at
FROM cdp_core.decision_registry d
LEFT JOIN cdp_core.decision_class_registry c
    ON c.domain = d.decision_class_domain;

COMMENT ON VIEW cdp_projection.decision_registry_flat IS
'Read projection over the v0.3 decision registry kernel for attorney-facing/demo output.';

-- -----------------------------------------------------------------------------
-- Projection: cdp_projection.decision_class_rollup
-- -----------------------------------------------------------------------------
-- Simple class-level analytics surface.

CREATE OR REPLACE VIEW cdp_projection.decision_class_rollup AS
SELECT
    coalesce(c.domain, d.decision_class_domain) AS decision_class_domain,
    split_part(coalesce(c.domain, d.decision_class_domain), ':', 2) AS registry_name,
    split_part(coalesce(c.domain, d.decision_class_domain), ':', 3) AS decision_class_id,
    c.parent_domain AS parent_class_domain,
    c.class_label,
    c.class_level,
    count(d.id) AS decision_count,
    min(d.created) AS first_decision_created,
    max(d.created) AS last_decision_created,
    count(*) FILTER (WHERE d.human_required) AS human_required_count,
    count(*) FILTER (WHERE d.permission_source_type = 'unknown') AS unknown_permission_count
FROM cdp_core.decision_registry d
LEFT JOIN cdp_core.decision_class_registry c
    ON c.domain = d.decision_class_domain
GROUP BY
    coalesce(c.domain, d.decision_class_domain),
    c.parent_domain,
    c.class_label,
    c.class_level;

COMMENT ON VIEW cdp_projection.decision_class_rollup IS
'Class-level analytics surface for counts, date ranges, human-review burden, and unknown-permission findings.';

-- -----------------------------------------------------------------------------
-- Projection: cdp_projection.decision_parent_child_edges
-- -----------------------------------------------------------------------------
-- Simple edge list for graph/tree analytics over parent-child decisions.

CREATE OR REPLACE VIEW cdp_projection.decision_parent_child_edges AS
SELECT
    child.domain AS child_domain,
    split_part(child.domain, ':', 3) AS child_decision_id,
    child.parent_domain,
    split_part(child.parent_domain, ':', 3) AS parent_decision_id,
    child.parent_relation_type,
    child.decision_class_domain AS child_class_domain,
    parent.decision_class_domain AS parent_class_domain,
    child.created AS child_created,
    parent.created AS parent_created
FROM cdp_core.decision_registry child
LEFT JOIN cdp_core.decision_registry parent
    ON parent.domain = child.parent_domain
WHERE child.parent_domain IS NOT NULL;

COMMENT ON VIEW cdp_projection.decision_parent_child_edges IS
'Edge-list projection for parent-child decision lineage analytics.';
