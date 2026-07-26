-- CDP Challenge Adjudication DDL
--
-- Status: starter executable DDL for the third end-to-end vertical slice
-- (adjudicate a raised challenge -> update its status -> complete its task
-- -> unblock the workflow instance when nothing else remains open).
-- Scope: one new governed table plus the controlled vocabulary it needs.
--
-- Naming note (challenge-level, not decision-level):
--   RFC-CDP-044 (Adjudicate Protocol) defines a much broader, decision-level
--   judgment: it considers all challenges and tests together, plus
--   Participation Integrity and Sovereignty Claims, and yields dispositions
--   like approve_for_legitimacy_review / reject / revise_and_resubmit /
--   escalate / defer_pending_test / refer_to_repair /
--   refer_to_sovereignty_process. None of RFC-CDP-044's prerequisite
--   artifacts (test records, participation integrity records, sovereignty
--   claims) exist in this schema yet, and implementing that full model is
--   out of scope here. This migration deliberately names its table
--   cdp_core.challenge_adjudication_record, not cdp_core.adjudication_record,
--   to keep the future decision-level RFC-CDP-044 adjudication name free
--   from collision. This slice adjudicates one challenge at a time.
--
-- Outcome vocabulary is intentionally small (sustained / not_sustained /
-- deferred / referred_to_repair) rather than RFC-CDP-044's full disposition
-- list, matching the reduced-vocabulary pattern already used for
-- challenge_status relative to RFC-CDP-042's fuller envelope state machine.
--
-- Multiple adjudications per challenge:
--   A challenge may be adjudicated more than once only while it remains
--   non-terminal (challenge_status IN ('raised', 'under_review')). A
--   'deferred' outcome preserves a real adjudication action (who looked at
--   it, when, why) while leaving the challenge open for a later, final
--   adjudication. Once a challenge reaches a terminal challenge_status
--   ('resolved', 'dismissed', 'withdrawn'), further adjudication attempts
--   are rejected by the service layer (409), not by a DB constraint here,
--   since that check requires reading the challenge's current status at
--   call time.
--
-- Workflow unblock rule:
--   When an adjudication resolves to a terminal outcome (sustained /
--   not_sustained / referred_to_repair), the service unblocks the
--   workflow_instance only if no other challenge_record for the same
--   decision still has challenge_status IN ('raised', 'under_review'). This
--   preserves the invariant that a workflow stays blocked while any
--   unresolved challenge remains; it does not reject, merge, dedupe, or
--   escalate repeat challenges, which stay out of scope. On unblock,
--   workflow_status is reset to 'active' -- workflow_instance does not
--   currently record its pre-blocked status, so this is a known
--   simplification, not full status-history tracking.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS cdp_core;

-- -----------------------------------------------------------------------------
-- Controlled vocabulary: challenge_adjudication_outcome
-- -----------------------------------------------------------------------------

INSERT INTO cdp_core.identifier_registry (
    registry_name, identifier_id, identifier_type_registry_name, identifier_type_id,
    display_label, description, status
)
VALUES
    ('registry', 'challenge_adjudication_outcome', 'lookup_kind', 'registry', 'Challenge Adjudication Outcome Registry', 'Controlled outcomes for challenge-level adjudication judgments.', 'active')
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
    ('challenge_adjudication_outcome', 'sustained', 'lookup_kind', 'enum_value', 'Sustained', 'Challenge upheld.', 'active'),
    ('challenge_adjudication_outcome', 'not_sustained', 'lookup_kind', 'enum_value', 'Not Sustained', 'Challenge rejected.', 'active'),
    ('challenge_adjudication_outcome', 'deferred', 'lookup_kind', 'enum_value', 'Deferred', 'Adjudication deferred pending more information; challenge remains open.', 'active'),
    ('challenge_adjudication_outcome', 'referred_to_repair', 'lookup_kind', 'enum_value', 'Referred To Repair', 'Sustained in a way that should hand off to the repair plane.', 'active')
ON CONFLICT (registry_name, identifier_id)
DO UPDATE SET
    identifier_type_registry_name = EXCLUDED.identifier_type_registry_name,
    identifier_type_id = EXCLUDED.identifier_type_id,
    display_label = EXCLUDED.display_label,
    description = EXCLUDED.description,
    status = EXCLUDED.status,
    updated_at = now();

-- -----------------------------------------------------------------------------
-- cdp_core.challenge_adjudication_record
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cdp_core.challenge_adjudication_record (
    adjudication_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    registry_name TEXT NOT NULL,
    decision_id TEXT NOT NULL,
    challenge_id UUID NOT NULL,

    adjudicated_by_actor_registry_name TEXT NOT NULL DEFAULT 'actor',
    adjudicated_by_actor_id TEXT NOT NULL,

    outcome_registry_name TEXT NOT NULL DEFAULT 'challenge_adjudication_outcome',
    outcome TEXT NOT NULL,

    rationale TEXT NOT NULL,

    -- Snapshot of the challenge_status this specific judgment produced.
    -- challenge_record only holds the challenge's current status, but a
    -- challenge may be adjudicated more than once while non-terminal (see
    -- header note), so each adjudication preserves what status resulted
    -- from that judgment at the time, independent of later adjudications.
    resulting_challenge_status TEXT NOT NULL,

    adjudicated_task_id UUID,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_challenge_adjudication_registry_name_format
        CHECK (registry_name ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_challenge_adjudication_decision_id_format
        CHECK (decision_id ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_challenge_adjudication_actor_registry
        CHECK (adjudicated_by_actor_registry_name = 'actor'),

    CONSTRAINT chk_challenge_adjudication_outcome_registry
        CHECK (outcome_registry_name = 'challenge_adjudication_outcome'),

    CONSTRAINT chk_challenge_adjudication_rationale_not_blank
        CHECK (btrim(rationale) <> ''),

    CONSTRAINT chk_challenge_adjudication_resulting_status
        CHECK (resulting_challenge_status IN ('resolved', 'dismissed', 'under_review')),

    -- Enforce the outcome -> resulting_challenge_status mapping at the DB
    -- level so the two columns cannot drift apart.
    CONSTRAINT chk_challenge_adjudication_outcome_status_mapping
        CHECK (
            (outcome = 'sustained' AND resulting_challenge_status = 'resolved')
            OR (outcome = 'not_sustained' AND resulting_challenge_status = 'dismissed')
            OR (outcome = 'referred_to_repair' AND resulting_challenge_status = 'resolved')
            OR (outcome = 'deferred' AND resulting_challenge_status = 'under_review')
        ),

    CONSTRAINT fk_challenge_adjudication_challenge
        FOREIGN KEY (challenge_id)
        REFERENCES cdp_core.challenge_record (challenge_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_challenge_adjudication_decision
        FOREIGN KEY (registry_name, decision_id)
        REFERENCES cdp_core.decision_registry (registry_name, decision_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_challenge_adjudication_actor
        FOREIGN KEY (adjudicated_by_actor_registry_name, adjudicated_by_actor_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_challenge_adjudication_outcome
        FOREIGN KEY (outcome_registry_name, outcome)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_challenge_adjudication_task
        FOREIGN KEY (adjudicated_task_id)
        REFERENCES cdp_core.workflow_task (task_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.challenge_adjudication_record IS
'Governed judgment over a single raised challenge: who adjudicated it, the outcome, rationale, the resulting challenge status, and its task relationship. Challenge-level only; not the broader RFC-CDP-044 decision-level Adjudicate Protocol.';

CREATE INDEX IF NOT EXISTS idx_challenge_adjudication_decision
    ON cdp_core.challenge_adjudication_record (registry_name, decision_id);

CREATE INDEX IF NOT EXISTS idx_challenge_adjudication_challenge
    ON cdp_core.challenge_adjudication_record (challenge_id);

CREATE INDEX IF NOT EXISTS idx_challenge_adjudication_outcome
    ON cdp_core.challenge_adjudication_record (outcome);
