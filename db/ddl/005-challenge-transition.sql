-- CDP Challenge Transition DDL
--
-- Status: starter executable DDL for the second end-to-end vertical slice
-- (raise a challenge against an existing decision -> block its workflow ->
-- open an adjudication task).
-- Scope: one new governed table plus the controlled vocabulary it needs.
--
-- A challenge is a governed artifact, not a loose text field on a decision.
-- It has its own durable identity, a relationship to the decision it
-- contests, a raising actor, controlled status/type vocabulary, and
-- timestamps, following the same registry-qualified enum + FK + CHECK
-- pattern used by cdp_core.decision_stakeholder and cdp_core.workflow_task
-- in 003-nemawashi-workflow-rules.sql. This is not a new schema pattern.
--
-- Scope note on vocabulary:
--   challenge_type below adopts the ordinary-Challenge type taxonomy from
--   RFC-CDP-042 (Challenge Protocol) section 9 (logical, evidentiary,
--   policy, ethical, operational, authority, standing, repair, apc, other),
--   since that vocabulary is already designed and stable. It intentionally
--   does NOT implement RFC-CDP-042 in full (no proposal_sufficiency_ref,
--   no Formation Challenge boundary, no APC gate linkage, no severity
--   enforcement) -- this is the smallest durable model needed for this
--   slice, not the full RFC. challenge_status is a reduced, slice-local
--   lifecycle (raised / under_review / resolved / dismissed / withdrawn),
--   not RFC-CDP-042's richer envelope-level state machine
--   (admitted -> under_challenge -> challenge_resolved / challenge_blocked).
--   Reconciling the two is deferred to a later slice.
--
-- Workflow-awareness note:
--   No workflow_stage row anywhere currently uses lifecycle_stage =
--   'challenge' (003's nemawashi_default_v1 stages are all lifecycle_stage
--   = 'nemawashi'), and no rule_definition wires the already-registered
--   raise_challenge action_type to any workflow. So "the workflow permits a
--   challenge" cannot yet be resolved from an explicit challenge stage or
--   rule. Until that gating exists, this slice permits a challenge whenever
--   the decision has a non-terminal workflow_instance (workflow_status not
--   in ('closed', 'cancelled')). This is a transitional workflow-status
--   gate, not a full challenge-policy model -- it will be superseded once
--   an explicit challenge stage or rule is configured. Raising a challenge
--   blocks that workflow_instance and opens an adjudicate_challenge task;
--   it does not move current_stage_id or lifecycle_stage, since no
--   configured stage exists to move it to.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS cdp_core;

-- -----------------------------------------------------------------------------
-- Controlled vocabulary: challenge_type, challenge_status
-- -----------------------------------------------------------------------------

INSERT INTO cdp_core.identifier_registry (
    registry_name, identifier_id, identifier_type_registry_name, identifier_type_id,
    display_label, description, status
)
VALUES
    ('registry', 'challenge_type', 'lookup_kind', 'registry', 'Challenge Type Registry', 'Controlled ordinary-challenge types (RFC-CDP-042 section 9).', 'active'),
    ('registry', 'challenge_status', 'lookup_kind', 'registry', 'Challenge Status Registry', 'Controlled challenge lifecycle states for this slice.', 'active')
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
    ('challenge_type', 'logical', 'lookup_kind', 'enum_value', 'Logical', 'Challenges reasoning, inference, or internal consistency.', 'active'),
    ('challenge_type', 'evidentiary', 'lookup_kind', 'enum_value', 'Evidentiary', 'Challenges evidence sufficiency, quality, provenance, or interpretation.', 'active'),
    ('challenge_type', 'policy', 'lookup_kind', 'enum_value', 'Policy', 'Challenges alignment with policy, rule, authority, or constraint.', 'active'),
    ('challenge_type', 'ethical', 'lookup_kind', 'enum_value', 'Ethical', 'Challenges harm, fairness, dignity, equity, erasure, or relational consequences.', 'active'),
    ('challenge_type', 'operational', 'lookup_kind', 'enum_value', 'Operational', 'Challenges feasibility, implementation, resilience, or operational risk.', 'active'),
    ('challenge_type', 'authority', 'lookup_kind', 'enum_value', 'Authority', 'Challenges whether claimed authority is valid.', 'active'),
    ('challenge_type', 'standing', 'lookup_kind', 'enum_value', 'Standing', 'Challenges whether an actor has valid standing or whether recusal applies.', 'active'),
    ('challenge_type', 'repair', 'lookup_kind', 'enum_value', 'Repair', 'Challenges whether appeal, repair, breach, or affected-party review is required.', 'active'),
    ('challenge_type', 'apc', 'lookup_kind', 'enum_value', 'APC', 'Challenges premature certainty, failed APC criteria, waivers, or sufficiency performance that survived admission.', 'active'),
    ('challenge_type', 'other', 'lookup_kind', 'enum_value', 'Other', 'Reserved for extension or implementation-profile use.', 'active'),

    ('challenge_status', 'raised', 'lookup_kind', 'enum_value', 'Raised', 'Challenge raised and pending adjudication.', 'active'),
    ('challenge_status', 'under_review', 'lookup_kind', 'enum_value', 'Under Review', 'Challenge is under active review.', 'active'),
    ('challenge_status', 'resolved', 'lookup_kind', 'enum_value', 'Resolved', 'Challenge resolved.', 'active'),
    ('challenge_status', 'dismissed', 'lookup_kind', 'enum_value', 'Dismissed', 'Challenge dismissed by a valid authority.', 'active'),
    ('challenge_status', 'withdrawn', 'lookup_kind', 'enum_value', 'Withdrawn', 'Challenge withdrawn by the raising actor.', 'active')
ON CONFLICT (registry_name, identifier_id)
DO UPDATE SET
    identifier_type_registry_name = EXCLUDED.identifier_type_registry_name,
    identifier_type_id = EXCLUDED.identifier_type_id,
    display_label = EXCLUDED.display_label,
    description = EXCLUDED.description,
    status = EXCLUDED.status,
    updated_at = now();

-- -----------------------------------------------------------------------------
-- cdp_core.challenge_record
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cdp_core.challenge_record (
    challenge_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    registry_name TEXT NOT NULL,
    decision_id TEXT NOT NULL,
    workflow_instance_id UUID NOT NULL,

    raised_by_actor_registry_name TEXT NOT NULL DEFAULT 'actor',
    raised_by_actor_id TEXT NOT NULL,

    challenge_type_registry_name TEXT NOT NULL DEFAULT 'challenge_type',
    challenge_type TEXT NOT NULL DEFAULT 'other',

    challenge_status_registry_name TEXT NOT NULL DEFAULT 'challenge_status',
    challenge_status TEXT NOT NULL DEFAULT 'raised',

    challenge_text TEXT NOT NULL,

    created_task_id UUID,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    resolved_at TIMESTAMPTZ,

    CONSTRAINT chk_challenge_record_registry_name_format
        CHECK (registry_name ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_challenge_record_decision_id_format
        CHECK (decision_id ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_challenge_record_raised_by_actor_registry
        CHECK (raised_by_actor_registry_name = 'actor'),

    CONSTRAINT chk_challenge_record_challenge_type_registry
        CHECK (challenge_type_registry_name = 'challenge_type'),

    CONSTRAINT chk_challenge_record_challenge_status_registry
        CHECK (challenge_status_registry_name = 'challenge_status'),

    CONSTRAINT chk_challenge_record_challenge_text_not_blank
        CHECK (btrim(challenge_text) <> ''),

    CONSTRAINT chk_challenge_record_resolved_status
        CHECK (resolved_at IS NULL OR challenge_status IN ('resolved', 'dismissed', 'withdrawn')),

    CONSTRAINT fk_challenge_record_decision
        FOREIGN KEY (registry_name, decision_id)
        REFERENCES cdp_core.decision_registry (registry_name, decision_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_challenge_record_workflow_instance
        FOREIGN KEY (workflow_instance_id)
        REFERENCES cdp_core.workflow_instance (workflow_instance_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_challenge_record_raised_by_actor
        FOREIGN KEY (raised_by_actor_registry_name, raised_by_actor_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_challenge_record_challenge_type
        FOREIGN KEY (challenge_type_registry_name, challenge_type)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_challenge_record_challenge_status
        FOREIGN KEY (challenge_status_registry_name, challenge_status)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_challenge_record_created_task
        FOREIGN KEY (created_task_id)
        REFERENCES cdp_core.workflow_task (task_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.challenge_record IS
'Governed challenge raised against a decision: durable identity, relationship to the decision and its workflow instance, raising actor, and controlled status/type vocabulary. Not a text field on decision_registry.';

CREATE INDEX IF NOT EXISTS idx_challenge_record_decision
    ON cdp_core.challenge_record (registry_name, decision_id);

CREATE INDEX IF NOT EXISTS idx_challenge_record_workflow_instance
    ON cdp_core.challenge_record (workflow_instance_id);

CREATE INDEX IF NOT EXISTS idx_challenge_record_status
    ON cdp_core.challenge_record (challenge_status);

CREATE INDEX IF NOT EXISTS idx_challenge_record_created_task
    ON cdp_core.challenge_record (created_task_id);
