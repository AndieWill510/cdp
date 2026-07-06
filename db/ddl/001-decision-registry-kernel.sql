-- CDP Decision Registry Kernel DDL
--
-- Status: starter executable DDL for the first normalized control-plane registry kernel
-- Scope: decision-registry core compatible with spreadsheet ingestion
--
-- This file intentionally defines the smallest durable control-plane kernel:
-- one row per material decision clause, with normalized atomic columns for
-- identity, classification, lineage, subject, predicate, object, permission,
-- human approval, and timing.
--
-- v0.4 removes the packed-string/key-value design from the core table.
-- Compatibility strings such as decision_register:<registry_name>:<decision_id>
-- are derived in views only. They are not authoritative stored fields.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS cdp_core;
CREATE SCHEMA IF NOT EXISTS cdp_projection;

-- -----------------------------------------------------------------------------
-- cdp_core.decision_class_registry
-- -----------------------------------------------------------------------------
-- Lightweight normalized classification registry for decision analytics.
--
-- Normal form rule:
--   Store registry_name, class_id, and parent_class_id as separate columns.
--   Do not store decision_class:<registry_name>:<class_id> as the authoritative key.
--   Views may derive that compatibility string for display/interchange.

CREATE TABLE IF NOT EXISTS cdp_core.decision_class_registry (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    registry_name TEXT NOT NULL,
    class_id TEXT NOT NULL,
    parent_class_id TEXT,

    class_label TEXT NOT NULL,
    class_level INTEGER NOT NULL DEFAULT 0,

    created TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_decision_class_registry_name_format
        CHECK (registry_name ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_decision_class_id_format
        CHECK (class_id ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_decision_class_parent_class_id_format
        CHECK (parent_class_id IS NULL OR parent_class_id ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_decision_class_label_not_blank
        CHECK (btrim(class_label) <> ''),

    CONSTRAINT chk_decision_class_level_nonnegative
        CHECK (class_level >= 0),

    CONSTRAINT uq_decision_class_registry
        UNIQUE (registry_name, class_id),

    CONSTRAINT fk_decision_class_parent
        FOREIGN KEY (registry_name, parent_class_id)
        REFERENCES cdp_core.decision_class_registry (registry_name, class_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.decision_class_registry IS
'Normalized parent-child classification registry for decision analytics.';

COMMENT ON COLUMN cdp_core.decision_class_registry.registry_name IS
'Atomic registry name. Do not pack into a decision_class domain string in the core table.';

COMMENT ON COLUMN cdp_core.decision_class_registry.class_id IS
'Atomic decision class identifier.';

COMMENT ON COLUMN cdp_core.decision_class_registry.parent_class_id IS
'Optional atomic parent class identifier within the same registry.';

CREATE INDEX IF NOT EXISTS idx_decision_class_parent
    ON cdp_core.decision_class_registry (registry_name, parent_class_id);

CREATE INDEX IF NOT EXISTS idx_decision_class_level
    ON cdp_core.decision_class_registry (registry_name, class_level);

-- -----------------------------------------------------------------------------
-- cdp_core.decision_registry
-- -----------------------------------------------------------------------------
-- The decision registry is the control-plane kernel.
--
-- Normal form rule:
--   Do not store key1/value1, key2/value2, key3/value3.
--   Do not store actor_type:actor_id.
--   Do not store verb:object_type:object_id.
--   Do not store decision_register:<registry_name>:<decision_id> as the
--   authoritative key.
--
-- Store each fact in its own atomic column.

CREATE TABLE IF NOT EXISTS cdp_core.decision_registry (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    registry_name TEXT NOT NULL,
    decision_id TEXT NOT NULL,

    decision_class_id TEXT NOT NULL,
    parent_decision_id TEXT,
    parent_relation_type TEXT NOT NULL DEFAULT 'none',

    antecedent_text TEXT NOT NULL,

    subject_actor_type TEXT NOT NULL,
    subject_actor_id TEXT NOT NULL,

    predicate_verb TEXT NOT NULL,
    object_type TEXT NOT NULL,
    object_id TEXT NOT NULL,

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
                registry_name || '|' ||
                decision_id || '|' ||
                decision_class_id || '|' ||
                coalesce(parent_decision_id, '') || '|' || parent_relation_type || '|' ||
                antecedent_text || '|' ||
                subject_actor_type || '|' || subject_actor_id || '|' ||
                predicate_verb || '|' || object_type || '|' || object_id || '|' ||
                permission_source_type || '|' || permission_source_id || '|' ||
                human_required::TEXT || '|' || human_approver_id || '|' ||
                created::TEXT,
                'sha256'
            ),
            'hex'
        )
    ) STORED,

    CONSTRAINT chk_decision_registry_registry_name_format
        CHECK (registry_name ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_decision_registry_decision_id_format
        CHECK (decision_id ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_decision_registry_class_id_format
        CHECK (decision_class_id ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_decision_registry_parent_decision_id_format
        CHECK (parent_decision_id IS NULL OR parent_decision_id ~ '^[A-Za-z0-9_-]+$'),

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
            (parent_relation_type = 'none' AND parent_decision_id IS NULL)
            OR
            (parent_relation_type <> 'none' AND parent_decision_id IS NOT NULL)
        ),

    CONSTRAINT chk_decision_registry_antecedent_text_not_blank
        CHECK (btrim(antecedent_text) <> ''),

    CONSTRAINT chk_decision_registry_subject_actor_type
        CHECK (subject_actor_type IN ('agent', 'human', 'system', 'institution', 'unknown')),

    CONSTRAINT chk_decision_registry_subject_actor_id_format
        CHECK (subject_actor_id ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_decision_registry_predicate_verb_format
        CHECK (predicate_verb ~ '^[A-Za-z][A-Za-z0-9_]*$'),

    CONSTRAINT chk_decision_registry_object_type_format
        CHECK (object_type ~ '^[A-Za-z][A-Za-z0-9_]*$'),

    CONSTRAINT chk_decision_registry_object_id_format
        CHECK (object_id ~ '^[A-Za-z0-9_-]+$'),

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

    CONSTRAINT uq_decision_registry_identity
        UNIQUE (registry_name, decision_id),

    CONSTRAINT fk_decision_registry_class
        FOREIGN KEY (registry_name, decision_class_id)
        REFERENCES cdp_core.decision_class_registry (registry_name, class_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_decision_registry_parent_decision
        FOREIGN KEY (registry_name, parent_decision_id)
        REFERENCES cdp_core.decision_registry (registry_name, decision_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.decision_registry IS
'Normalized control-plane kernel: one row per material decision clause ingested into CDP v0.4.';

COMMENT ON COLUMN cdp_core.decision_registry.registry_name IS
'Atomic registry name. Views may derive decision_register:<registry_name>:<decision_id> for compatibility.';

COMMENT ON COLUMN cdp_core.decision_registry.decision_id IS
'Atomic decision identifier within registry_name.';

COMMENT ON COLUMN cdp_core.decision_registry.decision_class_id IS
'Atomic decision class identifier within registry_name.';

COMMENT ON COLUMN cdp_core.decision_registry.parent_decision_id IS
'Optional atomic parent decision identifier within registry_name.';

COMMENT ON COLUMN cdp_core.decision_registry.parent_relation_type IS
'Relationship from this decision to parent_decision_id, such as depends_on, escalates_from, appeal_of, repair_of, or supersedes.';

COMMENT ON COLUMN cdp_core.decision_registry.antecedent_text IS
'Atomic antecedent text: condition, trigger, dependency, or none_supplied.';

COMMENT ON COLUMN cdp_core.decision_registry.subject_actor_type IS
'Atomic subject actor type: agent, human, system, institution, or unknown.';

COMMENT ON COLUMN cdp_core.decision_registry.subject_actor_id IS
'Atomic subject actor identifier.';

COMMENT ON COLUMN cdp_core.decision_registry.predicate_verb IS
'Atomic predicate verb, e.g. recommend_approval, deny_access, escalate_review, approve_review.';

COMMENT ON COLUMN cdp_core.decision_registry.object_type IS
'Atomic object type affected by the decision.';

COMMENT ON COLUMN cdp_core.decision_registry.object_id IS
'Atomic object identifier affected by the decision.';

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

CREATE INDEX IF NOT EXISTS idx_decision_registry_identity
    ON cdp_core.decision_registry (registry_name, decision_id);

CREATE INDEX IF NOT EXISTS idx_decision_registry_class
    ON cdp_core.decision_registry (registry_name, decision_class_id);

CREATE INDEX IF NOT EXISTS idx_decision_registry_parent
    ON cdp_core.decision_registry (registry_name, parent_decision_id);

CREATE INDEX IF NOT EXISTS idx_decision_registry_parent_relation
    ON cdp_core.decision_registry (registry_name, parent_relation_type, parent_decision_id);

CREATE INDEX IF NOT EXISTS idx_decision_registry_subject
    ON cdp_core.decision_registry (registry_name, subject_actor_type, subject_actor_id);

CREATE INDEX IF NOT EXISTS idx_decision_registry_predicate
    ON cdp_core.decision_registry (registry_name, predicate_verb, object_type);

CREATE INDEX IF NOT EXISTS idx_decision_registry_permission_source
    ON cdp_core.decision_registry (registry_name, permission_source_type, permission_source_id);

CREATE INDEX IF NOT EXISTS idx_decision_registry_human_required
    ON cdp_core.decision_registry (registry_name, human_required, human_approver_id);

-- -----------------------------------------------------------------------------
-- Projection: cdp_projection.decision_class_registry_flat
-- -----------------------------------------------------------------------------
-- Compatibility/read projection. Packs display domains only in the view.

CREATE OR REPLACE VIEW cdp_projection.decision_class_registry_flat AS
SELECT
    id,
    registry_name,
    class_id,
    'decision_class:' || registry_name || ':' || class_id AS decision_class_domain,
    parent_class_id,
    CASE
        WHEN parent_class_id IS NULL THEN NULL
        ELSE 'decision_class:' || registry_name || ':' || parent_class_id
    END AS parent_class_domain,
    class_label,
    class_level,
    created,
    updated_at
FROM cdp_core.decision_class_registry;

COMMENT ON VIEW cdp_projection.decision_class_registry_flat IS
'Compatibility projection over normalized decision classes; domain strings are derived, not authoritative.';

-- -----------------------------------------------------------------------------
-- Projection: cdp_projection.decision_registry_flat
-- -----------------------------------------------------------------------------
-- Attorney-readable and test-friendly projection over normalized atomic columns.

CREATE OR REPLACE VIEW cdp_projection.decision_registry_flat AS
SELECT
    d.id,
    d.registry_name,
    d.decision_id,
    'decision_register:' || d.registry_name || ':' || d.decision_id AS decision_domain,
    d.decision_class_id,
    'decision_class:' || d.registry_name || ':' || d.decision_class_id AS decision_class_domain,
    c.parent_class_id,
    CASE
        WHEN c.parent_class_id IS NULL THEN NULL
        ELSE 'decision_class:' || d.registry_name || ':' || c.parent_class_id
    END AS parent_class_domain,
    c.class_label AS decision_class_label,
    c.class_level AS decision_class_level,
    d.parent_decision_id,
    CASE
        WHEN d.parent_decision_id IS NULL THEN NULL
        ELSE 'decision_register:' || d.registry_name || ':' || d.parent_decision_id
    END AS parent_domain,
    d.parent_relation_type,
    d.created,
    d.antecedent_text,
    d.subject_actor_type,
    d.subject_actor_id,
    d.predicate_verb,
    d.object_type,
    d.object_id,
    d.permission_source_type,
    d.permission_source_id,
    d.human_required,
    d.human_approver_id,
    'Because ' || d.antecedent_text || ', ' ||
        d.subject_actor_type || ' ' || d.subject_actor_id ||
        ' performed ' || d.predicate_verb ||
        ' on ' || d.object_type || ' ' || d.object_id ||
        '. Class: ' || d.decision_class_id ||
        '. Parent relation: ' || d.parent_relation_type ||
        coalesce(' -> ' || d.parent_decision_id, '') ||
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
    ON c.registry_name = d.registry_name
   AND c.class_id = d.decision_class_id;

COMMENT ON VIEW cdp_projection.decision_registry_flat IS
'Read projection over the normalized v0.4 decision registry kernel for attorney-facing/demo output.';

-- -----------------------------------------------------------------------------
-- Projection: cdp_projection.decision_class_rollup
-- -----------------------------------------------------------------------------
-- Simple class-level analytics surface over atomic columns.

CREATE OR REPLACE VIEW cdp_projection.decision_class_rollup AS
SELECT
    d.registry_name,
    d.decision_class_id,
    'decision_class:' || d.registry_name || ':' || d.decision_class_id AS decision_class_domain,
    c.parent_class_id,
    CASE
        WHEN c.parent_class_id IS NULL THEN NULL
        ELSE 'decision_class:' || d.registry_name || ':' || c.parent_class_id
    END AS parent_class_domain,
    c.class_label,
    c.class_level,
    count(d.id) AS decision_count,
    min(d.created) AS first_decision_created,
    max(d.created) AS last_decision_created,
    count(*) FILTER (WHERE d.human_required) AS human_required_count,
    count(*) FILTER (WHERE d.permission_source_type = 'unknown') AS unknown_permission_count
FROM cdp_core.decision_registry d
LEFT JOIN cdp_core.decision_class_registry c
    ON c.registry_name = d.registry_name
   AND c.class_id = d.decision_class_id
GROUP BY
    d.registry_name,
    d.decision_class_id,
    c.parent_class_id,
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
    child.registry_name,
    child.decision_id AS child_decision_id,
    'decision_register:' || child.registry_name || ':' || child.decision_id AS child_domain,
    child.parent_decision_id,
    CASE
        WHEN child.parent_decision_id IS NULL THEN NULL
        ELSE 'decision_register:' || child.registry_name || ':' || child.parent_decision_id
    END AS parent_domain,
    child.parent_relation_type,
    child.decision_class_id AS child_class_id,
    parent.decision_class_id AS parent_class_id,
    child.created AS child_created,
    parent.created AS parent_created
FROM cdp_core.decision_registry child
LEFT JOIN cdp_core.decision_registry parent
    ON parent.registry_name = child.registry_name
   AND parent.decision_id = child.parent_decision_id
WHERE child.parent_decision_id IS NOT NULL;

COMMENT ON VIEW cdp_projection.decision_parent_child_edges IS
'Edge-list projection for parent-child decision lineage analytics over atomic decision identifiers.';
