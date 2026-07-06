-- CDP Decision Registry Kernel DDL
--
-- Status: starter executable DDL for the first normalized control-plane registry kernel
-- Scope: decision-registry core, identifier registry, and spreadsheet ingestion
--
-- This file defines the smallest durable control-plane kernel:
--   1. a generic config lookup for non-governance runtime settings;
--   2. an identifier registry for all non-decision IDs used by decisions;
--   3. a decision class registry;
--   4. a normalized decision registry;
--   5. projections for attorney-facing review and analytics.
--
-- v0.5 keeps the decision registry in normal form and adds a no-floating-ID
-- identifier registry. Compatibility strings such as
-- decision_register:<registry_name>:<decision_id> are derived in views only.
-- They are not authoritative stored fields.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS cdp_core;
CREATE SCHEMA IF NOT EXISTS cdp_projection;

-- -----------------------------------------------------------------------------
-- cdp_core.config_lookup
-- -----------------------------------------------------------------------------
-- Generic config lookup for non-governance-critical knobs.
--
-- This is intentionally not the identifier authority for the control plane.
-- Do not use config_lookup to validate decision actors, objects, predicates,
-- permission sources, or other decision references.

CREATE TABLE IF NOT EXISTS cdp_core.config_lookup (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    config_domain TEXT NOT NULL,
    config_key TEXT NOT NULL,
    config_value TEXT,
    config_json JSONB NOT NULL DEFAULT '{}'::jsonb,

    description TEXT,
    status TEXT NOT NULL DEFAULT 'active',

    created TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_config_lookup_domain_format
        CHECK (config_domain ~ '^[A-Za-z0-9_.-]+$'),

    CONSTRAINT chk_config_lookup_key_format
        CHECK (config_key ~ '^[A-Za-z0-9_.-]+$'),

    CONSTRAINT chk_config_lookup_status
        CHECK (status IN ('active', 'deprecated', 'inactive', 'retired')),

    CONSTRAINT uq_config_lookup
        UNIQUE (config_domain, config_key)
);

COMMENT ON TABLE cdp_core.config_lookup IS
'Generic non-governance config lookup. Not the identifier authority for decision registry references.';

CREATE INDEX IF NOT EXISTS idx_config_lookup_domain
    ON cdp_core.config_lookup (config_domain);

-- -----------------------------------------------------------------------------
-- cdp_core.identifier_registry
-- -----------------------------------------------------------------------------
-- The identifier registry is the no-floating-ID authority for the control plane.
--
-- Decision rows may contain atomic IDs, but those IDs must be registered here
-- unless they are self-references within decision_registry or references to
-- decision_class_registry.
--
-- Examples:
--   registry_name = actor, identifier_id = claims_review_agent
--   registry_name = actor_type, identifier_id = agent
--   registry_name = object, identifier_id = claim_9981
--   registry_name = object_type, identifier_id = claim
--   registry_name = permission_source, identifier_id = policy_claims_approval_v2
--   registry_name = permission_source_type, identifier_id = policy_rule
--
-- The registry is itself registered here using registry_name = registry.

CREATE TABLE IF NOT EXISTS cdp_core.identifier_registry (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    registry_name TEXT NOT NULL,
    identifier_id TEXT NOT NULL,

    identifier_type_registry_name TEXT,
    identifier_type_id TEXT,

    parent_registry_name TEXT,
    parent_identifier_id TEXT,

    display_label TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'active',

    created TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_identifier_registry_name_format
        CHECK (registry_name ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_identifier_id_format
        CHECK (identifier_id ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_identifier_type_registry_name_format
        CHECK (identifier_type_registry_name IS NULL OR identifier_type_registry_name ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_identifier_type_id_format
        CHECK (identifier_type_id IS NULL OR identifier_type_id ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_identifier_parent_registry_name_format
        CHECK (parent_registry_name IS NULL OR parent_registry_name ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_identifier_parent_id_format
        CHECK (parent_identifier_id IS NULL OR parent_identifier_id ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_identifier_type_pairing
        CHECK (
            (identifier_type_registry_name IS NULL AND identifier_type_id IS NULL)
            OR
            (identifier_type_registry_name IS NOT NULL AND identifier_type_id IS NOT NULL)
        ),

    CONSTRAINT chk_identifier_parent_pairing
        CHECK (
            (parent_registry_name IS NULL AND parent_identifier_id IS NULL)
            OR
            (parent_registry_name IS NOT NULL AND parent_identifier_id IS NOT NULL)
        ),

    CONSTRAINT chk_identifier_display_label_not_blank
        CHECK (btrim(display_label) <> ''),

    CONSTRAINT chk_identifier_status
        CHECK (status IN ('active', 'deprecated', 'inactive', 'retired')),

    CONSTRAINT uq_identifier_registry
        UNIQUE (registry_name, identifier_id),

    CONSTRAINT fk_identifier_type
        FOREIGN KEY (identifier_type_registry_name, identifier_type_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_identifier_parent
        FOREIGN KEY (parent_registry_name, parent_identifier_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.identifier_registry IS
'No-floating-ID authority for non-decision identifiers referenced by the CDP decision registry.';

COMMENT ON COLUMN cdp_core.identifier_registry.registry_name IS
'Identifier namespace, such as actor, actor_type, object, object_type, predicate_verb, permission_source, permission_source_type, parent_relation_type, source_system, or registry.';

COMMENT ON COLUMN cdp_core.identifier_registry.identifier_id IS
'Atomic identifier within registry_name.';

COMMENT ON COLUMN cdp_core.identifier_registry.identifier_type_registry_name IS
'Optional registry that defines the type of this identifier, such as actor_type or object_type.';

COMMENT ON COLUMN cdp_core.identifier_registry.identifier_type_id IS
'Optional type identifier within identifier_type_registry_name.';

COMMENT ON COLUMN cdp_core.identifier_registry.parent_registry_name IS
'Optional parent identifier registry name for hierarchy.';

COMMENT ON COLUMN cdp_core.identifier_registry.parent_identifier_id IS
'Optional parent identifier ID within parent_registry_name.';

CREATE INDEX IF NOT EXISTS idx_identifier_registry_type
    ON cdp_core.identifier_registry (identifier_type_registry_name, identifier_type_id);

CREATE INDEX IF NOT EXISTS idx_identifier_registry_parent
    ON cdp_core.identifier_registry (parent_registry_name, parent_identifier_id);

CREATE INDEX IF NOT EXISTS idx_identifier_registry_status
    ON cdp_core.identifier_registry (registry_name, status);

-- -----------------------------------------------------------------------------
-- Seed minimum identifier registries and controlled values.
-- -----------------------------------------------------------------------------
-- These are not sample decisions. They are the minimum registries and controlled
-- values needed for the demo control plane to reject floating IDs.

INSERT INTO cdp_core.identifier_registry (
    registry_name, identifier_id, identifier_type_registry_name, identifier_type_id,
    display_label, description, status
)
VALUES
    ('registry', 'registry', NULL, NULL, 'Registry Registry', 'Registers identifier registries.', 'active'),
    ('registry', 'lookup_kind', NULL, NULL, 'Lookup Kind Registry', 'Kinds used to type registry rows.', 'active')
ON CONFLICT (registry_name, identifier_id)
DO UPDATE SET
    display_label = EXCLUDED.display_label,
    description = EXCLUDED.description,
    status = EXCLUDED.status,
    updated_at = now();

INSERT INTO cdp_core.identifier_registry (
    registry_name, identifier_id, identifier_type_registry_name, identifier_type_id,
    display_label, description, status
)
VALUES
    ('lookup_kind', 'registry', 'lookup_kind', 'registry', 'Registry', 'A registry namespace.', 'active'),
    ('lookup_kind', 'enum_value', 'lookup_kind', 'registry', 'Enum Value', 'A controlled vocabulary value.', 'active'),
    ('lookup_kind', 'identifier', 'lookup_kind', 'registry', 'Identifier', 'A registered identifier.', 'active'),
    ('lookup_kind', 'business_object', 'lookup_kind', 'registry', 'Business Object', 'A business object type.', 'active'),
    ('lookup_kind', 'actor', 'lookup_kind', 'registry', 'Actor', 'An actor identity.', 'active'),
    ('lookup_kind', 'policy', 'lookup_kind', 'registry', 'Policy', 'A policy or rule identifier.', 'active'),
    ('lookup_kind', 'system', 'lookup_kind', 'registry', 'System', 'A system identifier.', 'active'),
    ('lookup_kind', 'source_system', 'lookup_kind', 'registry', 'Source System', 'An ingestion source system.', 'active')
ON CONFLICT (registry_name, identifier_id)
DO UPDATE SET
    identifier_type_registry_name = EXCLUDED.identifier_type_registry_name,
    identifier_type_id = EXCLUDED.identifier_type_id,
    display_label = EXCLUDED.display_label,
    description = EXCLUDED.description,
    status = EXCLUDED.status,
    updated_at = now();

INSERT INTO cdp_core.identifier_registry (
    registry_name, identifier_id, identifier_type_registry_name, identifier_type_id,
    display_label, description, status
)
VALUES
    ('registry', 'actor', 'lookup_kind', 'registry', 'Actor Registry', 'Registered actors usable in decision rows.', 'active'),
    ('registry', 'actor_type', 'lookup_kind', 'registry', 'Actor Type Registry', 'Controlled actor types.', 'active'),
    ('registry', 'object', 'lookup_kind', 'registry', 'Object Registry', 'Registered objects usable in decision rows.', 'active'),
    ('registry', 'object_type', 'lookup_kind', 'registry', 'Object Type Registry', 'Controlled object types.', 'active'),
    ('registry', 'predicate_verb', 'lookup_kind', 'registry', 'Predicate Verb Registry', 'Controlled decision/action verbs.', 'active'),
    ('registry', 'permission_source', 'lookup_kind', 'registry', 'Permission Source Registry', 'Registered permission sources usable in decision rows.', 'active'),
    ('registry', 'permission_source_type', 'lookup_kind', 'registry', 'Permission Source Type Registry', 'Controlled permission source types.', 'active'),
    ('registry', 'parent_relation_type', 'lookup_kind', 'registry', 'Parent Relation Type Registry', 'Controlled decision lineage relation types.', 'active'),
    ('registry', 'source_system', 'lookup_kind', 'registry', 'Source System Registry', 'Controlled ingestion source systems.', 'active')
ON CONFLICT (registry_name, identifier_id)
DO UPDATE SET
    identifier_type_registry_name = EXCLUDED.identifier_type_registry_name,
    identifier_type_id = EXCLUDED.identifier_type_id,
    display_label = EXCLUDED.display_label,
    description = EXCLUDED.description,
    status = EXCLUDED.status,
    updated_at = now();

INSERT INTO cdp_core.identifier_registry (
    registry_name, identifier_id, identifier_type_registry_name, identifier_type_id,
    display_label, description, status
)
VALUES
    ('actor_type', 'agent', 'lookup_kind', 'enum_value', 'Agent', 'AI or automated agent actor.', 'active'),
    ('actor_type', 'human', 'lookup_kind', 'enum_value', 'Human', 'Human actor.', 'active'),
    ('actor_type', 'system', 'lookup_kind', 'enum_value', 'System', 'System actor.', 'active'),
    ('actor_type', 'institution', 'lookup_kind', 'enum_value', 'Institution', 'Institutional actor.', 'active'),
    ('actor_type', 'unknown', 'lookup_kind', 'enum_value', 'Unknown Actor Type', 'Unknown actor type.', 'active'),

    ('parent_relation_type', 'none', 'lookup_kind', 'enum_value', 'None', 'No parent decision relation.', 'active'),
    ('parent_relation_type', 'child_of', 'lookup_kind', 'enum_value', 'Child Of', 'Generic child relation.', 'active'),
    ('parent_relation_type', 'depends_on', 'lookup_kind', 'enum_value', 'Depends On', 'Decision depends on another decision.', 'active'),
    ('parent_relation_type', 'derived_from', 'lookup_kind', 'enum_value', 'Derived From', 'Decision is derived from another decision.', 'active'),
    ('parent_relation_type', 'escalates_from', 'lookup_kind', 'enum_value', 'Escalates From', 'Decision escalates from a prior decision.', 'active'),
    ('parent_relation_type', 'approves', 'lookup_kind', 'enum_value', 'Approves', 'Decision approves a prior decision/recommendation.', 'active'),
    ('parent_relation_type', 'denies', 'lookup_kind', 'enum_value', 'Denies', 'Decision denies a prior decision/recommendation.', 'active'),
    ('parent_relation_type', 'appeal_of', 'lookup_kind', 'enum_value', 'Appeal Of', 'Decision is an appeal of a prior decision.', 'active'),
    ('parent_relation_type', 'repair_of', 'lookup_kind', 'enum_value', 'Repair Of', 'Decision repairs a prior decision.', 'active'),
    ('parent_relation_type', 'supersedes', 'lookup_kind', 'enum_value', 'Supersedes', 'Decision supersedes a prior decision.', 'active'),

    ('permission_source_type', 'policy_rule', 'lookup_kind', 'enum_value', 'Policy Rule', 'A named policy or rule allowed the decision.', 'active'),
    ('permission_source_type', 'human_approval', 'lookup_kind', 'enum_value', 'Human Approval', 'A human approved the decision.', 'active'),
    ('permission_source_type', 'system_role', 'lookup_kind', 'enum_value', 'System Role', 'A configured role allowed the decision.', 'active'),
    ('permission_source_type', 'workflow_configuration', 'lookup_kind', 'enum_value', 'Workflow Configuration', 'A configured workflow step allowed the decision.', 'active'),
    ('permission_source_type', 'tool_permission', 'lookup_kind', 'enum_value', 'Tool Permission', 'A tool/API permission allowed the action.', 'active'),
    ('permission_source_type', 'prior_decision', 'lookup_kind', 'enum_value', 'Prior Decision', 'A prior decision authorized this decision.', 'active'),
    ('permission_source_type', 'emergency_exception', 'lookup_kind', 'enum_value', 'Emergency Exception', 'An emergency exception path was used.', 'active'),
    ('permission_source_type', 'unknown', 'lookup_kind', 'enum_value', 'Unknown Permission Source Type', 'Permission source type is unknown.', 'active'),

    ('source_system', 'spreadsheet', 'lookup_kind', 'source_system', 'Spreadsheet', 'Spreadsheet ingestion source.', 'active'),
    ('source_system', 'api', 'lookup_kind', 'source_system', 'API', 'API ingestion source.', 'active'),
    ('source_system', 'seed_fixture', 'lookup_kind', 'source_system', 'Seed Fixture', 'Seed or test fixture source.', 'active')
ON CONFLICT (registry_name, identifier_id)
DO UPDATE SET
    identifier_type_registry_name = EXCLUDED.identifier_type_registry_name,
    identifier_type_id = EXCLUDED.identifier_type_id,
    display_label = EXCLUDED.display_label,
    description = EXCLUDED.description,
    status = EXCLUDED.status,
    updated_at = now();

-- Demo-friendly baseline identifiers. Tests may add more rows before ingesting
-- new decision fixtures.
INSERT INTO cdp_core.identifier_registry (
    registry_name, identifier_id, identifier_type_registry_name, identifier_type_id,
    display_label, description, status
)
VALUES
    ('actor', 'claims_review_agent', 'actor_type', 'agent', 'Claims Review Agent', 'Demo claims review agent.', 'active'),
    ('actor', 'access_agent', 'actor_type', 'agent', 'Access Agent', 'Demo access review agent.', 'active'),
    ('actor', 'user_442', 'actor_type', 'human', 'User 442', 'Demo human reviewer/approver.', 'active'),
    ('actor', 'workflow_engine', 'actor_type', 'system', 'Workflow Engine', 'Demo workflow engine.', 'active'),
    ('actor', 'review_board', 'actor_type', 'institution', 'Review Board', 'Demo review board.', 'active'),
    ('actor', 'unknown', 'actor_type', 'unknown', 'Unknown Actor', 'Unknown actor placeholder.', 'active'),

    ('object_type', 'claim', 'lookup_kind', 'business_object', 'Claim', 'Claim object type.', 'active'),
    ('object_type', 'access_request', 'lookup_kind', 'business_object', 'Access Request', 'Access request object type.', 'active'),
    ('object_type', 'review_task', 'lookup_kind', 'business_object', 'Review Task', 'Review task object type.', 'active'),

    ('object', 'claim_9981', 'object_type', 'claim', 'Claim 9981', 'Demo claim object.', 'active'),
    ('object', 'claim_9982', 'object_type', 'claim', 'Claim 9982', 'Demo claim object.', 'active'),
    ('object', 'access_7731', 'object_type', 'access_request', 'Access Request 7731', 'Demo access request object.', 'active'),
    ('object', 'task_1001', 'object_type', 'review_task', 'Review Task 1001', 'Demo review task object.', 'active'),

    ('predicate_verb', 'recommend_approval', 'lookup_kind', 'enum_value', 'Recommend Approval', 'Recommend approval action.', 'active'),
    ('predicate_verb', 'deny_access', 'lookup_kind', 'enum_value', 'Deny Access', 'Deny access action.', 'active'),
    ('predicate_verb', 'escalate_review', 'lookup_kind', 'enum_value', 'Escalate Review', 'Escalate for review action.', 'active'),
    ('predicate_verb', 'approve_review', 'lookup_kind', 'enum_value', 'Approve Review', 'Approve review action.', 'active'),
    ('predicate_verb', 'create_task', 'lookup_kind', 'enum_value', 'Create Task', 'Create task action.', 'active'),

    ('permission_source', 'policy_claims_approval_v2', 'permission_source_type', 'policy_rule', 'Claims Approval Policy v2', 'Demo claims approval policy.', 'active'),
    ('permission_source', 'workflow_access_v1', 'permission_source_type', 'workflow_configuration', 'Access Workflow v1', 'Demo access workflow configuration.', 'active'),
    ('permission_source', 'claims_api_recommend_permission', 'permission_source_type', 'tool_permission', 'Claims API Recommend Permission', 'Demo tool permission.', 'active'),
    ('permission_source', 'user_442', 'permission_source_type', 'human_approval', 'User 442 Approval', 'Demo human approval source.', 'active'),
    ('permission_source', 'unknown', 'permission_source_type', 'unknown', 'Unknown Permission Source', 'Unknown permission source placeholder.', 'active')
ON CONFLICT (registry_name, identifier_id)
DO UPDATE SET
    identifier_type_registry_name = EXCLUDED.identifier_type_registry_name,
    identifier_type_id = EXCLUDED.identifier_type_id,
    display_label = EXCLUDED.display_label,
    description = EXCLUDED.description,
    status = EXCLUDED.status,
    updated_at = now();

-- -----------------------------------------------------------------------------
-- cdp_core.decision_class_registry
-- -----------------------------------------------------------------------------
-- Normalized classification registry for decision analytics.

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
                source_system || '|' || created::TEXT,
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
'Normalized control-plane kernel: one row per material decision clause ingested into CDP v0.5.';

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
-- Identifier validation helpers and decision trigger.
-- -----------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION cdp_core.assert_registered_identifier(
    p_registry_name TEXT,
    p_identifier_id TEXT,
    p_context TEXT
) RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM cdp_core.identifier_registry i
        WHERE i.registry_name = p_registry_name
          AND i.identifier_id = p_identifier_id
          AND i.status IN ('active', 'deprecated')
    ) THEN
        RAISE EXCEPTION 'Unregistered identifier for %: %.%', p_context, p_registry_name, p_identifier_id;
    END IF;
END;
$$;

CREATE OR REPLACE FUNCTION cdp_core.assert_registered_identifier_of_type(
    p_registry_name TEXT,
    p_identifier_id TEXT,
    p_type_registry_name TEXT,
    p_type_id TEXT,
    p_context TEXT
) RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM cdp_core.identifier_registry i
        WHERE i.registry_name = p_registry_name
          AND i.identifier_id = p_identifier_id
          AND i.identifier_type_registry_name = p_type_registry_name
          AND i.identifier_type_id = p_type_id
          AND i.status IN ('active', 'deprecated')
    ) THEN
        RAISE EXCEPTION 'Unregistered or mistyped identifier for %: %.% is not typed as %.%',
            p_context, p_registry_name, p_identifier_id, p_type_registry_name, p_type_id;
    END IF;
END;
$$;

CREATE OR REPLACE FUNCTION cdp_core.validate_decision_registry_identifiers()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    PERFORM cdp_core.assert_registered_identifier('parent_relation_type', NEW.parent_relation_type, 'parent_relation_type');

    PERFORM cdp_core.assert_registered_identifier('actor_type', NEW.subject_actor_type, 'subject_actor_type');
    PERFORM cdp_core.assert_registered_identifier_of_type(
        'actor', NEW.subject_actor_id,
        'actor_type', NEW.subject_actor_type,
        'subject_actor_id'
    );

    PERFORM cdp_core.assert_registered_identifier('predicate_verb', NEW.predicate_verb, 'predicate_verb');

    PERFORM cdp_core.assert_registered_identifier('object_type', NEW.object_type, 'object_type');
    PERFORM cdp_core.assert_registered_identifier_of_type(
        'object', NEW.object_id,
        'object_type', NEW.object_type,
        'object_id'
    );

    PERFORM cdp_core.assert_registered_identifier('permission_source_type', NEW.permission_source_type, 'permission_source_type');
    PERFORM cdp_core.assert_registered_identifier_of_type(
        'permission_source', NEW.permission_source_id,
        'permission_source_type', NEW.permission_source_type,
        'permission_source_id'
    );

    IF NEW.human_approver_id = 'none' THEN
        -- No human approver required or recorded.
        NULL;
    ELSIF NEW.human_approver_id = 'unknown' THEN
        PERFORM cdp_core.assert_registered_identifier_of_type(
            'actor', NEW.human_approver_id,
            'actor_type', 'unknown',
            'human_approver_id'
        );
    ELSE
        PERFORM cdp_core.assert_registered_identifier_of_type(
            'actor', NEW.human_approver_id,
            'actor_type', 'human',
            'human_approver_id'
        );
    END IF;

    PERFORM cdp_core.assert_registered_identifier('source_system', NEW.source_system, 'source_system');

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_validate_decision_registry_identifiers
ON cdp_core.decision_registry;

CREATE TRIGGER trg_validate_decision_registry_identifiers
BEFORE INSERT OR UPDATE ON cdp_core.decision_registry
FOR EACH ROW
EXECUTE FUNCTION cdp_core.validate_decision_registry_identifiers();

-- -----------------------------------------------------------------------------
-- Projection: cdp_projection.identifier_registry_flat
-- -----------------------------------------------------------------------------

CREATE OR REPLACE VIEW cdp_projection.identifier_registry_flat AS
SELECT
    id,
    registry_name,
    identifier_id,
    'identifier:' || registry_name || ':' || identifier_id AS identifier_domain,
    identifier_type_registry_name,
    identifier_type_id,
    CASE
        WHEN identifier_type_registry_name IS NULL THEN NULL
        ELSE 'identifier:' || identifier_type_registry_name || ':' || identifier_type_id
    END AS identifier_type_domain,
    parent_registry_name,
    parent_identifier_id,
    CASE
        WHEN parent_registry_name IS NULL THEN NULL
        ELSE 'identifier:' || parent_registry_name || ':' || parent_identifier_id
    END AS parent_identifier_domain,
    display_label,
    description,
    status,
    created,
    updated_at
FROM cdp_core.identifier_registry;

COMMENT ON VIEW cdp_projection.identifier_registry_flat IS
'Flat view of registered identifiers. Identifier domain strings are derived, not authoritative.';

-- -----------------------------------------------------------------------------
-- Projection: cdp_projection.decision_class_registry_flat
-- -----------------------------------------------------------------------------

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
    subject_actor.display_label AS subject_actor_label,
    d.predicate_verb,
    predicate.display_label AS predicate_label,
    d.object_type,
    d.object_id,
    object_ref.display_label AS object_label,
    d.permission_source_type,
    d.permission_source_id,
    permission_source.display_label AS permission_source_label,
    d.human_required,
    d.human_approver_id,
    human_approver.display_label AS human_approver_label,
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
   AND c.class_id = d.decision_class_id
LEFT JOIN cdp_core.identifier_registry subject_actor
    ON subject_actor.registry_name = 'actor'
   AND subject_actor.identifier_id = d.subject_actor_id
LEFT JOIN cdp_core.identifier_registry predicate
    ON predicate.registry_name = 'predicate_verb'
   AND predicate.identifier_id = d.predicate_verb
LEFT JOIN cdp_core.identifier_registry object_ref
    ON object_ref.registry_name = 'object'
   AND object_ref.identifier_id = d.object_id
LEFT JOIN cdp_core.identifier_registry permission_source
    ON permission_source.registry_name = 'permission_source'
   AND permission_source.identifier_id = d.permission_source_id
LEFT JOIN cdp_core.identifier_registry human_approver
    ON human_approver.registry_name = 'actor'
   AND human_approver.identifier_id = d.human_approver_id;

COMMENT ON VIEW cdp_projection.decision_registry_flat IS
'Read projection over the normalized v0.5 decision registry kernel for attorney-facing/demo output.';

-- -----------------------------------------------------------------------------
-- Projection: cdp_projection.decision_class_rollup
-- -----------------------------------------------------------------------------

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
