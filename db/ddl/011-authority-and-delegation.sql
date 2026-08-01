-- CDP Authority and Delegation DDL
--
-- Status: starter executable DDL for the Authority vertical slice
-- (RFC-CDP-032 Authority and Delegation Model), scoped to RFC-CDP-032 §19
-- Minimal Compliance.
--
-- Constitutional scope note:
--   RFC-CDP-032 §3's core principle is the reason this exists: "No
--   anonymous authority. No ambient authority. No authority without
--   scope. No authority without record." This slice implements exactly
--   that minimum, deliberately deferring the rest of the RFC:
--
--   IMPLEMENTED: a governed Authority Grant (one authority per row, a
--   two-level scope with wildcard -- see "Scope model" below), a governed
--   Authority Evaluation Result recording every pass/fail decision, and a
--   single bounded actor authorized to issue or revoke grants (the same
--   discipline the Identity and Attestation slice's v0.2 review
--   correction established for cdp_identity_recognition_authority,
--   applied here from the start rather than as a follow-up fix).
--
--   NOT IMPLEMENTED, deliberately: delegation (RFC-CDP-032 §8 -- no
--   delegator, no delegation chain, no `may_delegate`), quorum authority
--   (§12), presence authority (§15 -- already partially covered by a
--   different table, execution_authorization_record, predating this
--   slice), emergency/repair/sovereignty grant types (§14), separation-
--   of-duties enforcement (§11), and authority decay beyond a simple
--   expires_at comparison (§9 describes decay from many triggers --
--   policy version change, role change, risk reclassification -- none of
--   which this slice tracks). `grant_type` is not modeled at all: every
--   grant issued by this slice is implicitly RFC-CDP-032's "direct" type.
--   See docs/session-028-authority-and-delegation.md for the full
--   boundary statement.
--
-- Scope model (the "richer purpose/scope semantics" this slice adds over
-- 010's flat purpose_scope string-equality check):
--   A grant's scope is two-level: scope_registry_name (required) and
--   scope_decision_class_id (nullable). NULL means "every decision class
--   in that registry" -- a wildcard, not "no scope" (a grant can never
--   have a NULL scope_registry_name). This is still far short of
--   RFC-CDP-032 §6's full scope object (jurisdiction, risk_level_max,
--   environment, target_systems, affected_parties, repair_agenda_ids),
--   but it is a real two-level hierarchy with an explicit wildcard rule,
--   not a single string compared for equality.
--
-- Proof-path integration note:
--   attest_and_create_decision (cdp/core/services.py) is extended, not
--   replaced or duplicated behind a new route -- see its docstring for
--   why completing the same proof path is correct here rather than
--   introducing a second, competing "fullest" decision-creation path.
--   POST /decisions (create_decision_with_workflow) remains completely
--   unaffected.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS cdp_core;

-- -----------------------------------------------------------------------------
-- Controlled vocabulary
-- -----------------------------------------------------------------------------

INSERT INTO cdp_core.identifier_registry (
    registry_name, identifier_id, identifier_type_registry_name, identifier_type_id,
    display_label, description, status
)
VALUES
    ('registry', 'authority_type', 'lookup_kind', 'registry', 'Authority Type Registry', 'Controlled authority types (RFC-CDP-032 SS5).', 'active'),
    ('registry', 'authority_grant_status', 'lookup_kind', 'registry', 'Authority Grant Status Registry', 'Controlled lifecycle status for an Authority Grant.', 'active'),
    ('registry', 'authority_grant_basis', 'lookup_kind', 'registry', 'Authority Grant Basis Registry', 'Controlled provenance basis for an Authority Grant (RFC-CDP-032 SS6 provenance.basis).', 'active'),
    ('registry', 'authority_evaluation_result', 'lookup_kind', 'registry', 'Authority Evaluation Result Registry', 'Controlled outcomes for an Authority Evaluation Result (RFC-CDP-032 SS16).', 'active')
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
    -- authority_type: the full RFC-CDP-032 SS5 vocabulary. Seeding the
    -- complete list is not a claim that every type is enforced -- only
    -- 'PROPOSE' is evaluated anywhere in this slice (see the proof-path
    -- integration note above). The rest exist so a future slice can grant
    -- and evaluate them without a schema change.
    ('authority_type', 'IDENTIFY', 'lookup_kind', 'enum_value', 'Identify', 'Establish or update actor identity.', 'active'),
    ('authority_type', 'ATTEST', 'lookup_kind', 'enum_value', 'Attest', 'Bind actor, authority claim, and act through verifiable proof.', 'active'),
    ('authority_type', 'ALIGN', 'lookup_kind', 'enum_value', 'Align', 'Facilitate Nemawashi or pre-formal alignment.', 'active'),
    ('authority_type', 'PROPOSE', 'lookup_kind', 'enum_value', 'Propose', 'Introduce, amend, or resubmit a Decision.', 'active'),
    ('authority_type', 'CHALLENGE', 'lookup_kind', 'enum_value', 'Challenge', 'Enter structured dissent, objection, or contestation.', 'active'),
    ('authority_type', 'TEST', 'lookup_kind', 'enum_value', 'Test', 'Run or submit validation, simulation, precedent, or evidence tests.', 'active'),
    ('authority_type', 'ADJUDICATE', 'lookup_kind', 'enum_value', 'Adjudicate', 'Render formal judgment on deliberative posture.', 'active'),
    ('authority_type', 'LEGITIMIZE', 'lookup_kind', 'enum_value', 'Legitimize', 'Confer institutional enactability under policy.', 'active'),
    ('authority_type', 'REQUEST_EXECUTION', 'lookup_kind', 'enum_value', 'Request Execution', 'Request execution of a legitimized Decision.', 'active'),
    ('authority_type', 'AUTHORIZE_EXECUTION', 'lookup_kind', 'enum_value', 'Authorize Execution', 'Approve execution under scope and policy.', 'active'),
    ('authority_type', 'EXECUTE', 'lookup_kind', 'enum_value', 'Execute', 'Perform the bounded action.', 'active'),
    ('authority_type', 'PAUSE_EXECUTION', 'lookup_kind', 'enum_value', 'Pause Execution', 'Pause an execution in progress.', 'active'),
    ('authority_type', 'ROLLBACK', 'lookup_kind', 'enum_value', 'Rollback', 'Reverse, compensate, or mitigate an execution.', 'active'),
    ('authority_type', 'OVERRIDE', 'lookup_kind', 'enum_value', 'Override', 'Invoke an exceptional emergency path.', 'active'),
    ('authority_type', 'RECORD', 'lookup_kind', 'enum_value', 'Record', 'Write or finalize official record.', 'active'),
    ('authority_type', 'LEARN', 'lookup_kind', 'enum_value', 'Learn', 'Produce learning, policy, precedent, or schema updates.', 'active'),
    ('authority_type', 'COVENANT_PARTICIPATE', 'lookup_kind', 'enum_value', 'Covenant Participate', 'Participate under covenantal role boundaries.', 'active'),
    ('authority_type', 'AIITL_CHALLENGE', 'lookup_kind', 'enum_value', 'AIITL Challenge', 'Surface contradiction, uncertainty, schema drift, or risk as AIITL.', 'active'),
    ('authority_type', 'REPAIR_CLAIM', 'lookup_kind', 'enum_value', 'Repair Claim', 'Submit or preserve a repair claim or repair agenda.', 'active'),
    ('authority_type', 'REPAIR_REVIEW', 'lookup_kind', 'enum_value', 'Repair Review', 'Review, contest, or validate repair record or closure.', 'active'),
    ('authority_type', 'REPAIR_COMMIT', 'lookup_kind', 'enum_value', 'Repair Commit', 'Commit resources, duties, timelines, or institutional response.', 'active'),
    ('authority_type', 'REVOKE', 'lookup_kind', 'enum_value', 'Revoke', 'Revoke an authority grant or delegation.', 'active'),
    ('authority_type', 'DELEGATE', 'lookup_kind', 'enum_value', 'Delegate', 'Delegate authority within scope. Not implemented by this slice -- see the DDL header.', 'active'),

    -- authority_grant_status: 'active' and 'revoked' are the only values
    -- this slice's service layer ever writes. 'expired' is deliberately
    -- not a stored status -- it is computed at evaluation time by
    -- comparing expires_at to the evaluation clock, not flipped by a
    -- background job. 'suspended' and 'superseded' are schema-supported
    -- for a future re-grant/suspension flow, unused here.
    ('authority_grant_status', 'active', 'lookup_kind', 'enum_value', 'Active', 'Grant is currently valid, subject to its expires_at.', 'active'),
    ('authority_grant_status', 'expired', 'lookup_kind', 'enum_value', 'Expired', 'Reserved: computed from expires_at at evaluation time, never stored by this slice.', 'active'),
    ('authority_grant_status', 'revoked', 'lookup_kind', 'enum_value', 'Revoked', 'Grant was explicitly revoked before its natural expiry.', 'active'),
    ('authority_grant_status', 'suspended', 'lookup_kind', 'enum_value', 'Suspended', 'Reserved for a future suspension flow; not written by this slice.', 'active'),
    ('authority_grant_status', 'superseded', 'lookup_kind', 'enum_value', 'Superseded', 'Reserved for a future re-grant flow; not written by this slice.', 'active'),

    ('authority_grant_basis', 'policy', 'lookup_kind', 'enum_value', 'Policy', 'Granted under a named policy.', 'active'),
    ('authority_grant_basis', 'role', 'lookup_kind', 'enum_value', 'Role', 'Granted on the basis of an institutional role.', 'active'),
    ('authority_grant_basis', 'consent', 'lookup_kind', 'enum_value', 'Consent', 'Granted on the basis of consent.', 'active'),
    ('authority_grant_basis', 'treaty', 'lookup_kind', 'enum_value', 'Treaty', 'Granted on the basis of a treaty obligation.', 'active'),
    ('authority_grant_basis', 'law', 'lookup_kind', 'enum_value', 'Law', 'Granted on the basis of legal requirement.', 'active'),
    ('authority_grant_basis', 'community_authority', 'lookup_kind', 'enum_value', 'Community Authority', 'Granted on the basis of community authority.', 'active'),
    ('authority_grant_basis', 'emergency', 'lookup_kind', 'enum_value', 'Emergency', 'Granted on the basis of an emergency condition.', 'active'),

    -- authority_evaluation_result: only 'pass' and 'fail' are written by
    -- this slice's synchronous evaluation path. 'conditional' and
    -- 'escalated' are schema-supported for a future asynchronous or
    -- multi-party evaluation flow.
    ('authority_evaluation_result', 'pass', 'lookup_kind', 'enum_value', 'Pass', 'The actor held a matching, active, unexpired grant.', 'active'),
    ('authority_evaluation_result', 'fail', 'lookup_kind', 'enum_value', 'Fail', 'No matching, active, unexpired grant was found.', 'active'),
    ('authority_evaluation_result', 'conditional', 'lookup_kind', 'enum_value', 'Conditional', 'Reserved for a future conditional-evaluation flow; not written by this slice.', 'active'),
    ('authority_evaluation_result', 'escalated', 'lookup_kind', 'enum_value', 'Escalated', 'Reserved for a future escalation flow; not written by this slice.', 'active')
ON CONFLICT (registry_name, identifier_id)
DO UPDATE SET
    identifier_type_registry_name = EXCLUDED.identifier_type_registry_name,
    identifier_type_id = EXCLUDED.identifier_type_id,
    display_label = EXCLUDED.display_label,
    description = EXCLUDED.description,
    status = EXCLUDED.status,
    updated_at = now();

-- A system actor for the record-keeping side of evaluation (kept distinct
-- from the grant issuer below, which is a governance role, not a system
-- process).
INSERT INTO cdp_core.identifier_registry (
    registry_name, identifier_id, identifier_type_registry_name, identifier_type_id,
    display_label, description, status
)
VALUES
    ('actor', 'cdp_authority_grant_issuer', 'actor_type', 'institution', 'CDP Authority Grant Issuer', 'The single governed process authorized to issue or revoke Authority Grants in this slice.', 'active')
ON CONFLICT (registry_name, identifier_id)
DO UPDATE SET
    identifier_type_registry_name = EXCLUDED.identifier_type_registry_name,
    identifier_type_id = EXCLUDED.identifier_type_id,
    display_label = EXCLUDED.display_label,
    description = EXCLUDED.description,
    status = EXCLUDED.status,
    updated_at = now();

-- -----------------------------------------------------------------------------
-- cdp_core.authority_grant
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cdp_core.authority_grant (
    authority_grant_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    actor_registry_name TEXT NOT NULL DEFAULT 'actor',
    actor_id TEXT NOT NULL,

    authority_type_registry_name TEXT NOT NULL DEFAULT 'authority_type',
    authority TEXT NOT NULL,

    -- Two-level scope with an explicit wildcard rule: NULL
    -- scope_decision_class_id means "every decision class in
    -- scope_registry_name", not "no scope" -- scope_registry_name itself
    -- is never NULL. See the DDL file header's "Scope model" note.
    scope_registry_name TEXT NOT NULL,
    scope_decision_class_id TEXT,

    status_registry_name TEXT NOT NULL DEFAULT 'authority_grant_status',
    status TEXT NOT NULL DEFAULT 'active',

    basis_registry_name TEXT NOT NULL DEFAULT 'authority_grant_basis',
    basis TEXT NOT NULL,

    issued_at TIMESTAMPTZ NOT NULL,
    effective_at TIMESTAMPTZ NOT NULL,
    -- Mandatory, not optional: RFC-CDP-032 SS9 states "CDP assumes
    -- authority decays unless policy states otherwise." A NULL here would
    -- silently mean "forever," which is exactly the ambient-authority
    -- failure mode SS3 forbids -- so every grant must declare its own
    -- expiry rather than defaulting to indefinite.
    expires_at TIMESTAMPTZ NOT NULL,

    issuer_actor_registry_name TEXT NOT NULL DEFAULT 'actor',
    issuer_actor_id TEXT NOT NULL,

    revoked_at TIMESTAMPTZ,
    revoked_by_actor_registry_name TEXT DEFAULT 'actor',
    revoked_by_actor_id TEXT,
    revocation_reason TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_authority_grant_actor_registry
        CHECK (actor_registry_name = 'actor'),

    CONSTRAINT chk_authority_grant_authority_type_registry
        CHECK (authority_type_registry_name = 'authority_type'),

    CONSTRAINT chk_authority_grant_status_registry
        CHECK (status_registry_name = 'authority_grant_status'),

    CONSTRAINT chk_authority_grant_basis_registry
        CHECK (basis_registry_name = 'authority_grant_basis'),

    CONSTRAINT chk_authority_grant_issuer_registry
        CHECK (issuer_actor_registry_name = 'actor'),

    CONSTRAINT chk_authority_grant_revoked_by_registry
        CHECK (revoked_by_actor_registry_name IS NULL OR revoked_by_actor_registry_name = 'actor'),

    CONSTRAINT chk_authority_grant_status_value
        CHECK (status IN ('active', 'revoked')),

    CONSTRAINT chk_authority_grant_expires_after_effective
        CHECK (expires_at > effective_at),

    CONSTRAINT chk_authority_grant_revocation_pairing
        CHECK (
            (status = 'active' AND revoked_at IS NULL AND revoked_by_actor_id IS NULL AND revocation_reason IS NULL)
            OR
            (status = 'revoked' AND revoked_at IS NOT NULL AND revoked_by_actor_id IS NOT NULL AND revocation_reason IS NOT NULL)
        ),

    CONSTRAINT fk_authority_grant_actor
        FOREIGN KEY (actor_registry_name, actor_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_authority_grant_authority_type
        FOREIGN KEY (authority_type_registry_name, authority)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_authority_grant_status
        FOREIGN KEY (status_registry_name, status)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_authority_grant_basis
        FOREIGN KEY (basis_registry_name, basis)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_authority_grant_issuer
        FOREIGN KEY (issuer_actor_registry_name, issuer_actor_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_authority_grant_revoked_by
        FOREIGN KEY (revoked_by_actor_registry_name, revoked_by_actor_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.authority_grant IS
'Authority Grant (RFC-CDP-032 SS6), scoped to SS19 Minimal Compliance: one authority per row, a two-level scope with wildcard, mandatory expiry, no delegation/quorum/presence. Revocation is a status transition, never a delete -- see the forbid-delete trigger below.';

CREATE INDEX IF NOT EXISTS idx_authority_grant_actor
    ON cdp_core.authority_grant (actor_registry_name, actor_id);

CREATE INDEX IF NOT EXISTS idx_authority_grant_lookup
    ON cdp_core.authority_grant (actor_id, authority, status, scope_registry_name, scope_decision_class_id);

CREATE OR REPLACE FUNCTION cdp_core.forbid_authority_grant_delete()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION
        'cdp_core.authority_grant rows cannot be deleted (authority_grant_id=%); use status to revoke a grant',
        OLD.authority_grant_id;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_authority_grant_forbid_delete ON cdp_core.authority_grant;
CREATE TRIGGER trg_authority_grant_forbid_delete
BEFORE DELETE ON cdp_core.authority_grant
FOR EACH ROW EXECUTE FUNCTION cdp_core.forbid_authority_grant_delete();

-- -----------------------------------------------------------------------------
-- cdp_core.authority_evaluation_result
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cdp_core.authority_evaluation_result (
    authority_evaluation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    actor_registry_name TEXT NOT NULL DEFAULT 'actor',
    actor_id TEXT NOT NULL,

    required_authority_type_registry_name TEXT NOT NULL DEFAULT 'authority_type',
    required_authority TEXT NOT NULL,

    governed_act_type_registry_name TEXT NOT NULL DEFAULT 'governed_act_type',
    governed_act_type TEXT NOT NULL,

    -- The specific governed act instance this evaluation covers. For this
    -- slice, always a cdp_core.decision_registry row -- reuses the same
    -- governed_act_type registry 010-identity-and-attestation.sql seeded,
    -- since "kinds of governed act" is one vocabulary, not two.
    governed_act_registry_name TEXT NOT NULL,
    governed_act_decision_id TEXT NOT NULL,

    matched_authority_grant_id UUID,

    result_registry_name TEXT NOT NULL DEFAULT 'authority_evaluation_result',
    result TEXT NOT NULL,

    failure_reason TEXT,

    evaluated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_authority_evaluation_actor_registry
        CHECK (actor_registry_name = 'actor'),

    CONSTRAINT chk_authority_evaluation_required_authority_type_registry
        CHECK (required_authority_type_registry_name = 'authority_type'),

    CONSTRAINT chk_authority_evaluation_governed_act_type_registry
        CHECK (governed_act_type_registry_name = 'governed_act_type'),

    CONSTRAINT chk_authority_evaluation_result_registry
        CHECK (result_registry_name = 'authority_evaluation_result'),

    CONSTRAINT chk_authority_evaluation_result_value
        CHECK (result IN ('pass', 'fail')),

    CONSTRAINT chk_authority_evaluation_pass_has_match
        CHECK (
            (result = 'pass' AND matched_authority_grant_id IS NOT NULL AND failure_reason IS NULL)
            OR
            (result = 'fail' AND matched_authority_grant_id IS NULL AND failure_reason IS NOT NULL)
        ),

    CONSTRAINT fk_authority_evaluation_actor
        FOREIGN KEY (actor_registry_name, actor_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_authority_evaluation_required_authority
        FOREIGN KEY (required_authority_type_registry_name, required_authority)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_authority_evaluation_governed_act_type
        FOREIGN KEY (governed_act_type_registry_name, governed_act_type)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_authority_evaluation_governed_act_decision
        FOREIGN KEY (governed_act_registry_name, governed_act_decision_id)
        REFERENCES cdp_core.decision_registry (registry_name, decision_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_authority_evaluation_result
        FOREIGN KEY (result_registry_name, result)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_authority_evaluation_matched_grant
        FOREIGN KEY (matched_authority_grant_id)
        REFERENCES cdp_core.authority_grant (authority_grant_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.authority_evaluation_result IS
'Authority Evaluation Result (RFC-CDP-032 SS16): the governed record of whether an actor held matching authority for a governed act, and which grant (if any) satisfied it. Only pass/fail are written synchronously -- see the DDL header.';

CREATE INDEX IF NOT EXISTS idx_authority_evaluation_actor
    ON cdp_core.authority_evaluation_result (actor_registry_name, actor_id);

CREATE INDEX IF NOT EXISTS idx_authority_evaluation_governed_act
    ON cdp_core.authority_evaluation_result (governed_act_registry_name, governed_act_decision_id);

CREATE OR REPLACE FUNCTION cdp_core.forbid_authority_evaluation_result_delete()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION
        'cdp_core.authority_evaluation_result rows cannot be deleted (authority_evaluation_id=%)',
        OLD.authority_evaluation_id;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_authority_evaluation_result_forbid_delete ON cdp_core.authority_evaluation_result;
CREATE TRIGGER trg_authority_evaluation_result_forbid_delete
BEFORE DELETE ON cdp_core.authority_evaluation_result
FOR EACH ROW EXECUTE FUNCTION cdp_core.forbid_authority_evaluation_result_delete();
