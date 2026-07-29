-- CDP Execution Record DDL
--
-- Status: starter executable DDL for the fifth end-to-end vertical slice
-- (record a completed execution attempt against an authorized decision).
-- Scope: one new governed table plus the controlled vocabulary it needs.
--
-- This slice records an external act; it does not perform or orchestrate
-- execution itself. There is no adapter, no external call, no async job --
-- the API is "tell CDP what happened," where "what happened" already
-- concluded (succeeded, failed, or partial) by the time it is recorded.
-- There is no in-flight/pending execution_status value.
--
-- Constitutional invariant -- repair is mandatory, not conditional:
--   Earlier drafts of this slice considered closing the decision's
--   workflow_instance (workflow_status = 'closed') on a successful
--   execution. That has been corrected. CDP's governing principle is:
--
--     Nemawashi is always required.
--     Repair is always required.
--     Learning may not bypass repair.
--
--   Every persistent decision changes relationships, obligations, and
--   trust -- even when execution succeeds. Repair consultation is not
--   conditional on failure or detected harm, so execution must not close
--   the workflow or advance it toward learning on any outcome. This
--   migration and the service built on it therefore never write to
--   cdp_core.workflow_instance at all: execution_record only reads it (to
--   verify eligibility and to link workflow_instance_id), and leaves
--   workflow_status, blocked, and closed_at exactly as authorization left
--   them, on every outcome, so a future mandatory repair slice has an open
--   workflow instance to act on. This principle is being captured
--   deliberately in its own architecture checkpoint after this slice, not
--   implemented here -- no repair schema or logic is added in this
--   migration.
--
-- Required link to execution_authorization_record:
--   authorization_id is NOT NULL and resolved by the service from
--   (registry_name, decision_id) -- the API does not accept a
--   client-supplied authorization_id. This is how "the authorization
--   belongs to the same decision" is satisfied by construction: there is
--   no field for a caller to supply a mismatched one.
--
-- Retries are expected; success is not repeatable:
--   Multiple execution_record rows may exist for the same authorization_id
--   (a failed or partial attempt does not block a retry -- every attempt,
--   regardless of outcome, is its own durable, audited row). But once one
--   attempt for an authorization has succeeded, no further row for that
--   authorization may also be 'succeeded' -- enforced by the partial
--   unique index below, not by forbidding additional rows outright.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS cdp_core;

-- -----------------------------------------------------------------------------
-- Controlled vocabulary: execution_status
-- -----------------------------------------------------------------------------

INSERT INTO cdp_core.identifier_registry (
    registry_name, identifier_id, identifier_type_registry_name, identifier_type_id,
    display_label, description, status
)
VALUES
    ('registry', 'execution_status', 'lookup_kind', 'registry', 'Execution Status Registry', 'Controlled outcomes for recorded execution attempts.', 'active')
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
    ('execution_status', 'succeeded', 'lookup_kind', 'enum_value', 'Succeeded', 'The execution attempt completed successfully.', 'active'),
    ('execution_status', 'failed', 'lookup_kind', 'enum_value', 'Failed', 'The execution attempt did not complete successfully.', 'active'),
    ('execution_status', 'partial', 'lookup_kind', 'enum_value', 'Partial', 'The execution attempt completed only partially.', 'active')
ON CONFLICT (registry_name, identifier_id)
DO UPDATE SET
    identifier_type_registry_name = EXCLUDED.identifier_type_registry_name,
    identifier_type_id = EXCLUDED.identifier_type_id,
    display_label = EXCLUDED.display_label,
    description = EXCLUDED.description,
    status = EXCLUDED.status,
    updated_at = now();

-- -----------------------------------------------------------------------------
-- cdp_core.execution_record
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cdp_core.execution_record (
    execution_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    registry_name TEXT NOT NULL,
    decision_id TEXT NOT NULL,
    authorization_id UUID NOT NULL,
    workflow_instance_id UUID NOT NULL,

    executed_by_actor_registry_name TEXT NOT NULL DEFAULT 'actor',
    executed_by_actor_id TEXT NOT NULL,

    execution_status_registry_name TEXT NOT NULL DEFAULT 'execution_status',
    execution_status TEXT NOT NULL,

    result_summary TEXT NOT NULL,

    attempted_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ NOT NULL,

    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_execution_record_registry_name_format
        CHECK (registry_name ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_execution_record_decision_id_format
        CHECK (decision_id ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_execution_record_actor_registry
        CHECK (executed_by_actor_registry_name = 'actor'),

    CONSTRAINT chk_execution_record_status_registry
        CHECK (execution_status_registry_name = 'execution_status'),

    CONSTRAINT chk_execution_record_result_summary_not_blank
        CHECK (btrim(result_summary) <> ''),

    CONSTRAINT chk_execution_record_completed_not_before_attempted
        CHECK (completed_at >= attempted_at),

    CONSTRAINT fk_execution_record_decision
        FOREIGN KEY (registry_name, decision_id)
        REFERENCES cdp_core.decision_registry (registry_name, decision_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_execution_record_authorization
        FOREIGN KEY (authorization_id)
        REFERENCES cdp_core.execution_authorization_record (authorization_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_execution_record_workflow_instance
        FOREIGN KEY (workflow_instance_id)
        REFERENCES cdp_core.workflow_instance (workflow_instance_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_execution_record_actor
        FOREIGN KEY (executed_by_actor_registry_name, executed_by_actor_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_execution_record_status
        FOREIGN KEY (execution_status_registry_name, execution_status)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.execution_record IS
'Governed record of one completed execution attempt against an authorized decision: who executed it, outcome, result summary, and timing. Retries are expected (multiple rows per authorization_id); at most one may be succeeded, enforced by uq_execution_record_one_success_per_authorization. Never closes or transitions the workflow instance -- repair is mandatory on every outcome, not conditional on failure.';

CREATE INDEX IF NOT EXISTS idx_execution_record_decision
    ON cdp_core.execution_record (registry_name, decision_id);

CREATE INDEX IF NOT EXISTS idx_execution_record_authorization
    ON cdp_core.execution_record (authorization_id);

CREATE INDEX IF NOT EXISTS idx_execution_record_status
    ON cdp_core.execution_record (execution_status);

-- At most one succeeded execution_record per authorization. Additional
-- failed/partial attempts remain unrestricted.
CREATE UNIQUE INDEX IF NOT EXISTS uq_execution_record_one_success_per_authorization
    ON cdp_core.execution_record (authorization_id)
    WHERE execution_status = 'succeeded';
