-- CDP Execution Authorization DDL
--
-- Status: starter executable DDL for the fourth end-to-end vertical slice
-- (authorize a decision to proceed to execution once no blocking challenge
-- work remains -- not execution itself).
-- Scope: one new governed table plus the controlled vocabulary it needs.
--
-- Naming note (authorization gate, not final legitimacy):
--   The seeded lifecycle_stage vocabulary already has 'legitimize' (see
--   003-nemawashi-workflow-rules.sql). This table is deliberately NOT named
--   cdp_core.legitimation_record. "Legitimation" as an operational artifact
--   name risks reading as a declaration that a decision is procedurally,
--   finally legitimate -- a much bigger claim than what this slice does,
--   and one that invites a short-circuit reading (proposal created ->
--   authorized -> execute, with no check that challenge work is resolved).
--   What this slice actually means is narrower: "this decision is
--   authorized to proceed to execution under the current workflow
--   conditions." Table, columns, events, and API all use
--   execution_authorization language, not legitimation language.
--
-- The gate must not bypass unresolved challenges:
--   A decision may receive execution authorization only when no
--   challenge_record for it is still 'raised' or 'under_review'
--   (challenge_status values 'resolved', 'dismissed', 'withdrawn' do not
--   block), and only when no 'adjudicate_challenge' workflow_task remains
--   open (defense-in-depth alongside the challenge_status check). Both
--   checks are enforced by the service layer at call time, not by a DB
--   constraint here, since they require reading related tables' current
--   state.
--
-- One terminal authorization per decision, not a repeatable judgment:
--   Unlike challenge_adjudication_record (which allows multiple rows while
--   a challenge stays non-terminal), execution authorization has no
--   intermediate state -- the eligibility gate is a pure function of
--   current challenge/task state at call time. A failed check persists no
--   row at all. A second call after authorization already exists hits the
--   unique constraint below and is mapped to a clean 409 by the service
--   layer, not treated as a new attempt.
--
-- Task behavior: completes, does not create:
--   This slice does not create a new workflow_task. It completes the
--   existing open 'review_decision' task created at decision creation
--   (see 001-decision-registry-kernel.sql / cdp/core/services.py
--   create_decision_with_workflow) -- leaving that task open while
--   workflow_status moves to 'advanced' would be internally inconsistent.
--   If no eligible open review_decision task exists, the service layer
--   returns 409 rather than persisting anything.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS cdp_core;

-- -----------------------------------------------------------------------------
-- Controlled vocabulary: execution_authorization_status
-- -----------------------------------------------------------------------------

INSERT INTO cdp_core.identifier_registry (
    registry_name, identifier_id, identifier_type_registry_name, identifier_type_id,
    display_label, description, status
)
VALUES
    ('registry', 'execution_authorization_status', 'lookup_kind', 'registry', 'Execution Authorization Status Registry', 'Controlled statuses for execution-authorization records.', 'active')
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
    ('execution_authorization_status', 'authorized', 'lookup_kind', 'enum_value', 'Authorized', 'Decision is authorized to proceed to execution under current workflow conditions.', 'active')
ON CONFLICT (registry_name, identifier_id)
DO UPDATE SET
    identifier_type_registry_name = EXCLUDED.identifier_type_registry_name,
    identifier_type_id = EXCLUDED.identifier_type_id,
    display_label = EXCLUDED.display_label,
    description = EXCLUDED.description,
    status = EXCLUDED.status,
    updated_at = now();

-- -----------------------------------------------------------------------------
-- cdp_core.execution_authorization_record
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cdp_core.execution_authorization_record (
    authorization_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    registry_name TEXT NOT NULL,
    decision_id TEXT NOT NULL,
    workflow_instance_id UUID NOT NULL,

    authorized_by_actor_registry_name TEXT NOT NULL DEFAULT 'actor',
    authorized_by_actor_id TEXT NOT NULL,

    authorization_status_registry_name TEXT NOT NULL DEFAULT 'execution_authorization_status',
    authorization_status TEXT NOT NULL DEFAULT 'authorized',

    rationale TEXT NOT NULL,

    -- The workflow_task this authorization completed (the decision's
    -- original review_decision task), not a task this slice created. A
    -- successful authorization always completes exactly one such task, so
    -- this is NOT NULL -- the DB enforces the same invariant as the
    -- service: no authorization record may exist that cannot identify the
    -- review task it completed.
    completed_task_id UUID NOT NULL,

    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_execution_authorization_registry_name_format
        CHECK (registry_name ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_execution_authorization_decision_id_format
        CHECK (decision_id ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_execution_authorization_actor_registry
        CHECK (authorized_by_actor_registry_name = 'actor'),

    CONSTRAINT chk_execution_authorization_status_registry
        CHECK (authorization_status_registry_name = 'execution_authorization_status'),

    CONSTRAINT chk_execution_authorization_rationale_not_blank
        CHECK (btrim(rationale) <> ''),

    CONSTRAINT uq_execution_authorization_decision
        UNIQUE (registry_name, decision_id),

    CONSTRAINT fk_execution_authorization_decision
        FOREIGN KEY (registry_name, decision_id)
        REFERENCES cdp_core.decision_registry (registry_name, decision_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_execution_authorization_workflow_instance
        FOREIGN KEY (workflow_instance_id)
        REFERENCES cdp_core.workflow_instance (workflow_instance_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_execution_authorization_actor
        FOREIGN KEY (authorized_by_actor_registry_name, authorized_by_actor_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_execution_authorization_status
        FOREIGN KEY (authorization_status_registry_name, authorization_status)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_execution_authorization_completed_task
        FOREIGN KEY (completed_task_id)
        REFERENCES cdp_core.workflow_task (task_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.execution_authorization_record IS
'Governed authorization for a decision to proceed to execution: who authorized it, rationale, the workflow instance and review task it applies to. Not a declaration of final legitimacy, and not execution itself.';

CREATE INDEX IF NOT EXISTS idx_execution_authorization_workflow_instance
    ON cdp_core.execution_authorization_record (workflow_instance_id);

CREATE INDEX IF NOT EXISTS idx_execution_authorization_completed_task
    ON cdp_core.execution_authorization_record (completed_task_id);
