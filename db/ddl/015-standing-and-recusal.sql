-- CDP Standing and Recusal DDL
--
-- Status: starter executable DDL for the first bounded Standing slice
-- (RFC-CDP-033-Standing-and-Recusal-Model.md, Draft v0.7): Affected-Party
-- Standing gating Challenge-raising only. See
-- docs/session-035-affected-party-standing-challenge.md for the full
-- scope statement this migration implements.
--
-- Constitutional scope note:
--   This is deliberately the narrowest slice of RFC-CDP-033 that reaches
--   E4. IMPLEMENTED: Constitutional Standing's Affected-Party subtype
--   only, submitted as a Standing Claim (SS9.1) and separately determined
--   by a Standing Recognition Determination (SS9.2), as two distinct,
--   append-only records -- never one mutable row, per RFC-CDP-033 SS9's
--   explicit requirement that claim/recognition/recusal/contest never
--   collapse into a single row a later act overwrites.
--
--   NOT IMPLEMENTED, deliberately: Recusal in its entirety (no table, no
--   check, no route -- RFC-CDP-033 SS7/SS10 remain unenforced code);
--   every Standing type other than Constitutional Affected-Party
--   (Evidence-Custodian, Record-Keeper, Delegated, Emergency, Repair,
--   Appeal, AI Functional -- RFC-CDP-033 SS11.4); automatic Breach Record
--   generation on a `denied` outcome (RFC-CDP-033 SS11.6 -- RFC-CDP-072
--   itself remains E0 in this repository, so there is nothing to generate
--   a Breach Record in); Standing for any lifecycle stage other than
--   Challenge; the enforcement-projection half of RFC-CDP-033 SS12's
--   two-layer persistence model (only the canonical claim/determination
--   shape exists here); chained/superseding determinations (RFC-CDP-033
--   SS9.2 allows a later determination to reference and correct an
--   earlier one via supersedes_determination_id -- this slice allows
--   exactly one determination per claim, enforced by a UNIQUE constraint
--   below, and treats re-determination as future work, not as something
--   silently permitted or silently forbidden without a schema signal).
--
-- Minimal sufficiency, encoded at the database layer:
--   RFC-CDP-033 SS11.4 (as clarified in Draft v0.7): "A minimally
--   sufficient claim -- one that identifies a possible consequence and
--   the relationship that makes the actor answerable to it -- creates
--   provisional Standing immediately upon submission." This migration
--   operationalizes both halves of that test as NOT-NULL/CHECK
--   constraints on cdp_core.standing_claim, not as application-layer
--   judgment: claimed_impact (the possible consequence) must be
--   non-blank, and at least one of standing_basis_role /
--   standing_basis_accountability / standing_basis_contextual_relationship
--   (the relationship) must be non-blank. A row that satisfies both is,
--   by construction, always minimally sufficient -- the service layer
--   never needs to re-check this at read time. This is the same honest
--   limit every other not-blank CHECK in this codebase has (it proves
--   non-blank content, not truthful or meaningful content) -- see
--   010-identity-and-attestation.sql's chk_identity_claim_descriptor_not_blank
--   for the same limitation stated there.
--
-- Recognition authority, per RFC-CDP-033 SS11.5 (Draft v0.7):
--   A binding Standing recognition determination must be made by an actor
--   that is bounded, non-self-interested, procedurally authorized, and
--   auditable. This slice satisfies that with the same narrow pattern
--   sessions 027 (cdp_identity_recognition_authority) and 028
--   (cdp_authority_grant_issuer) already established: a single, seeded,
--   institution-type actor (cdp_standing_recognition_authority) is the
--   only actor cdp/core/services.py's determine-standing-claim path will
--   accept as determined_by_actor_id, and it may not determine a claim
--   where it is itself the claimant. RFC-CDP-033 does not name this
--   specific actor -- naming a concrete actor is explicitly left to
--   implementation, per SS11.5's closing sentence -- so this is a
--   documented interpretation satisfying the RFC's stated properties, not
--   a literal transcription of RFC text.
--
-- Provisional Standing is opt-in on the Challenge path, not a new
-- blanket requirement:
--   RFC-CDP-033 SS6's stage-specific Standing matrix names multiple bases
--   for Challenge standing (affected party, domain expert, governance
--   authority) -- this slice implements only one of them. Consequently,
--   cdp/core/services.py's attest_and_raise_challenge gains an *optional*
--   standing_claim_id parameter, not a mandatory Standing gate: when a
--   caller supplies one, the referenced claim is verified (ownership,
--   decision/stage match, and that no `rejected`/`denied` determination
--   exists against it) before the challenge is raised; when omitted,
--   challenge-raising behaves exactly as it did before this migration.
--   Making this mandatory for every challenger would functionally deny
--   standing to every legitimate non-affected-party challenger this
--   slice does not model -- the opposite of what RFC-CDP-033 SS11.2
--   requires (non-recognition must never be read as non-existence). See
--   attest_and_raise_challenge's docstring for the enforcement detail.
--
-- Design pattern note: mirrors cdp_core.identity_claim / authority_grant's
-- registry-qualified enum + FK pattern, and 010/011's seeded-bounded-actor
-- pattern. Unlike identity_claim (a single row whose recognition_status
-- transitions in place), standing_claim and standing_recognition_determination
-- are each independently immutable once inserted -- both a forbid-delete
-- AND a forbid-update trigger apply to both tables, since RFC-CDP-033 SS9
-- requires a correction to be a new record, not an edit to an existing one.

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
    ('registry', 'standing_stage', 'lookup_kind', 'registry', 'Standing Stage Registry', 'Controlled lifecycle stages a Standing Claim may be submitted for (RFC-CDP-033 SS4.1).', 'active'),
    ('registry', 'standing_type', 'lookup_kind', 'registry', 'Standing Type Registry', 'Controlled Standing types (RFC-CDP-033 SS11.4 Standing Type Taxonomy).', 'active'),
    ('registry', 'standing_recognition_outcome', 'lookup_kind', 'registry', 'Standing Recognition Outcome Registry', 'Controlled outcomes for a Standing Recognition Determination (RFC-CDP-033 SS11.8).', 'active')
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
    -- standing_stage: the full RFC-CDP-033 SS4.1/SS6 lifecycle-stage
    -- vocabulary. Seeding the complete list is not a claim that every
    -- stage is enforced -- only 'challenge' is ever accepted by this
    -- slice's service layer (see the DDL header). The rest exist so a
    -- future slice can extend Standing to another stage without a schema
    -- change, mirroring 011-authority-and-delegation.sql's authority_type
    -- precedent.
    ('standing_stage', 'propose', 'lookup_kind', 'enum_value', 'Propose', 'RFC-CDP-041 Propose stage.', 'active'),
    ('standing_stage', 'challenge', 'lookup_kind', 'enum_value', 'Challenge', 'RFC-CDP-042 Challenge stage. The only stage this slice''s service layer accepts.', 'active'),
    ('standing_stage', 'test', 'lookup_kind', 'enum_value', 'Test', 'RFC-CDP-043 Test stage.', 'active'),
    ('standing_stage', 'adjudicate', 'lookup_kind', 'enum_value', 'Adjudicate', 'RFC-CDP-044 Adjudicate stage.', 'active'),
    ('standing_stage', 'legitimize', 'lookup_kind', 'enum_value', 'Legitimize', 'RFC-CDP-045 Legitimize stage.', 'active'),
    ('standing_stage', 'execute', 'lookup_kind', 'enum_value', 'Execute', 'RFC-CDP-046 Execute stage.', 'active'),
    ('standing_stage', 'record', 'lookup_kind', 'enum_value', 'Record', 'RFC-CDP-047 Record stage.', 'active'),
    ('standing_stage', 'learn', 'lookup_kind', 'enum_value', 'Learn', 'RFC-CDP-048 Learn stage.', 'active'),

    -- standing_type: the full RFC-CDP-033 SS11.4 taxonomy. Only
    -- 'constitutional_affected_party' is accepted by this slice's service
    -- layer -- see the DDL header. The rest are seeded so extending
    -- Standing to another type does not require a schema change, mirroring
    -- authority_type's precedent of seeding 23 values while enforcing 5.
    ('standing_type', 'constitutional_affected_party', 'lookup_kind', 'enum_value', 'Constitutional -- Affected Party', 'RFC-CDP-033 SS11.4. The only Standing type this slice''s service layer accepts.', 'active'),
    ('standing_type', 'constitutional_evidence_custodian', 'lookup_kind', 'enum_value', 'Constitutional -- Evidence Custodian', 'RFC-CDP-033 SS11.4. Not yet implemented.', 'active'),
    ('standing_type', 'constitutional_record_keeper', 'lookup_kind', 'enum_value', 'Constitutional -- Record Keeper', 'RFC-CDP-033 SS11.4. Not yet implemented.', 'active'),
    ('standing_type', 'delegated', 'lookup_kind', 'enum_value', 'Delegated', 'RFC-CDP-033 SS11.4. Not yet implemented.', 'active'),
    ('standing_type', 'emergency', 'lookup_kind', 'enum_value', 'Emergency', 'RFC-CDP-033 SS11.4. Not yet implemented.', 'active'),
    ('standing_type', 'repair', 'lookup_kind', 'enum_value', 'Repair', 'RFC-CDP-033 SS11.4. Not yet implemented.', 'active'),
    ('standing_type', 'appeal', 'lookup_kind', 'enum_value', 'Appeal', 'RFC-CDP-033 SS11.4. Not yet implemented.', 'active'),

    -- standing_recognition_outcome: the full RFC-CDP-033 SS11.8 five-value
    -- vocabulary. Only 'recognized' and 'denied' are written by this
    -- slice's service layer (cdp_core.standing_recognition_determination's
    -- own CHECK constraint below restricts the column further, to exactly
    -- those two, mirroring authority_evaluation_result's
    -- chk_authority_evaluation_result_value precedent of seeding a wider
    -- vocabulary than a table-level CHECK currently admits). 'narrowed',
    -- 'deferred', and 'rejected' are reserved for a future session.
    -- 'narrowed' specifically is deferred rather than implemented now
    -- because this table has no outcome_scope column (RFC-CDP-033 SS9.2)
    -- to record what a narrowing actually narrows to -- writing 'narrowed'
    -- without a recorded scope would make it enforcement-indistinguishable
    -- from 'recognized' while still claiming something the table cannot
    -- support (review finding on PR #53; see the DDL determination-table
    -- comment below and docs/session-035-affected-party-standing-challenge.md).
    ('standing_recognition_outcome', 'recognized', 'lookup_kind', 'enum_value', 'Recognized', 'RFC-CDP-033 SS11.8. The claim is confirmed as presented.', 'active'),
    ('standing_recognition_outcome', 'narrowed', 'lookup_kind', 'enum_value', 'Narrowed', 'RFC-CDP-033 SS11.8. The claim is confirmed at a smaller scope than claimed. Reserved: not written by this slice, which has no outcome_scope column to record the narrowed scope.', 'active'),
    ('standing_recognition_outcome', 'deferred', 'lookup_kind', 'enum_value', 'Deferred', 'RFC-CDP-033 SS11.8. Reserved: not written by this slice.', 'active'),
    ('standing_recognition_outcome', 'rejected', 'lookup_kind', 'enum_value', 'Rejected', 'RFC-CDP-033 SS11.8. Reserved: not written by this slice.', 'active'),
    ('standing_recognition_outcome', 'denied', 'lookup_kind', 'enum_value', 'Denied', 'RFC-CDP-033 SS11.6/SS11.8. The only outcome that (in a future session, once RFC-CDP-072 is implemented) triggers the automatic Breach Record rule.', 'active')
ON CONFLICT (registry_name, identifier_id)
DO UPDATE SET
    identifier_type_registry_name = EXCLUDED.identifier_type_registry_name,
    identifier_type_id = EXCLUDED.identifier_type_id,
    display_label = EXCLUDED.display_label,
    description = EXCLUDED.description,
    status = EXCLUDED.status,
    updated_at = now();

-- The single, bounded, seeded actor authorized to determine (recognize or
-- deny) a Standing Claim in this slice -- see the DDL header's
-- "Recognition authority" note. Mirrors cdp_identity_recognition_authority
-- (010) and cdp_authority_grant_issuer (011) exactly: an
-- identifier_registry row plus a governed cdp_core.actor row, no token
-- seeded here (see "No privileged tokens are seeded here" in
-- 014-caller-authentication.sql's header and
-- db/seed/dev-caller-authentication-tokens.sql for local/dev/test
-- bootstrapping of this actor's token).
INSERT INTO cdp_core.identifier_registry (
    registry_name, identifier_id, identifier_type_registry_name, identifier_type_id,
    display_label, description, status
)
VALUES
    ('actor', 'cdp_standing_recognition_authority', 'actor_type', 'institution', 'CDP Standing Recognition Authority', 'The single governed process authorized to recognize or deny Standing Claims in this slice.', 'active')
ON CONFLICT (registry_name, identifier_id)
DO UPDATE SET
    identifier_type_registry_name = EXCLUDED.identifier_type_registry_name,
    identifier_type_id = EXCLUDED.identifier_type_id,
    display_label = EXCLUDED.display_label,
    description = EXCLUDED.description,
    status = EXCLUDED.status,
    updated_at = now();

INSERT INTO cdp_core.actor (actor_id, actor_type, display_mode, actor_status)
VALUES ('cdp_standing_recognition_authority', 'institution', 'public', 'active')
ON CONFLICT (actor_registry_name, actor_id) DO NOTHING;

-- -----------------------------------------------------------------------------
-- cdp_core.standing_claim
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cdp_core.standing_claim (
    claim_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- The decision this claim concerns. Named decision_registry_name /
    -- decision_id (not governed_act_registry_name / governed_act_decision_id,
    -- attestation_record's naming) because a claim is about a
    -- (decision, stage) pair, submitted before -- and independent of --
    -- any specific governed-act instance (e.g. before a challenge_id
    -- exists to raise it against).
    decision_registry_name TEXT NOT NULL,
    decision_id TEXT NOT NULL,

    stage_registry_name TEXT NOT NULL DEFAULT 'standing_stage',
    stage TEXT NOT NULL DEFAULT 'challenge',

    -- The claimant: the actor asserting Standing.
    actor_registry_name TEXT NOT NULL DEFAULT 'actor',
    actor_id TEXT NOT NULL,

    standing_type_registry_name TEXT NOT NULL DEFAULT 'standing_type',
    standing_type TEXT NOT NULL DEFAULT 'constitutional_affected_party',

    -- The "possible consequence" half of RFC-CDP-033 SS11.4's minimal-
    -- sufficiency test -- what the claimant asserts could happen to them.
    claimed_impact TEXT NOT NULL,

    -- The "relationship that makes the actor answerable to it" half of
    -- the same test -- at least one of the three must be non-blank (see
    -- chk_standing_claim_basis_minimally_sufficient below). Mirrors
    -- RFC-CDP-033 SS9.1's standing_basis list fields exactly.
    standing_basis_role TEXT,
    standing_basis_accountability TEXT,
    standing_basis_contextual_relationship TEXT,

    submitted_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_standing_claim_decision_registry
        CHECK (btrim(decision_registry_name) <> ''),

    CONSTRAINT chk_standing_claim_stage_registry
        CHECK (stage_registry_name = 'standing_stage'),

    CONSTRAINT chk_standing_claim_actor_registry
        CHECK (actor_registry_name = 'actor'),

    CONSTRAINT chk_standing_claim_standing_type_registry
        CHECK (standing_type_registry_name = 'standing_type'),

    CONSTRAINT chk_standing_claim_impact_not_blank
        CHECK (btrim(claimed_impact) <> ''),

    -- Minimal sufficiency, database-enforced: at least one of the three
    -- relationship-basis fields must be non-blank. See the DDL header.
    CONSTRAINT chk_standing_claim_basis_minimally_sufficient
        CHECK (
            (standing_basis_role IS NOT NULL AND btrim(standing_basis_role) <> '')
            OR (standing_basis_accountability IS NOT NULL AND btrim(standing_basis_accountability) <> '')
            OR (standing_basis_contextual_relationship IS NOT NULL AND btrim(standing_basis_contextual_relationship) <> '')
        ),

    CONSTRAINT fk_standing_claim_decision
        FOREIGN KEY (decision_registry_name, decision_id)
        REFERENCES cdp_core.decision_registry (registry_name, decision_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_standing_claim_stage
        FOREIGN KEY (stage_registry_name, stage)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_standing_claim_actor
        FOREIGN KEY (actor_registry_name, actor_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_standing_claim_standing_type
        FOREIGN KEY (standing_type_registry_name, standing_type)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.standing_claim IS
'Standing Claim (RFC-CDP-033 SS9.1). Immutable once created -- a correction or withdrawal is a new claim row, never an edit to this one (enforced by trigger below). A row satisfying chk_standing_claim_impact_not_blank and chk_standing_claim_basis_minimally_sufficient is, by construction, minimally sufficient under RFC-CDP-033 SS11.4 and grounds provisional Standing immediately, independent of whether a Standing Recognition Determination exists yet.';

CREATE INDEX IF NOT EXISTS idx_standing_claim_actor
    ON cdp_core.standing_claim (actor_registry_name, actor_id);

CREATE INDEX IF NOT EXISTS idx_standing_claim_decision_stage
    ON cdp_core.standing_claim (decision_registry_name, decision_id, stage);

CREATE OR REPLACE FUNCTION cdp_core.forbid_standing_claim_delete()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION
        'cdp_core.standing_claim rows cannot be deleted (claim_id=%); submit a new claim instead',
        OLD.claim_id;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_standing_claim_forbid_delete ON cdp_core.standing_claim;
CREATE TRIGGER trg_standing_claim_forbid_delete
BEFORE DELETE ON cdp_core.standing_claim
FOR EACH ROW EXECUTE FUNCTION cdp_core.forbid_standing_claim_delete();

CREATE OR REPLACE FUNCTION cdp_core.forbid_standing_claim_update()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION
        'cdp_core.standing_claim rows are immutable and cannot be updated (claim_id=%); submit a new claim instead',
        OLD.claim_id;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_standing_claim_forbid_update ON cdp_core.standing_claim;
CREATE TRIGGER trg_standing_claim_forbid_update
BEFORE UPDATE ON cdp_core.standing_claim
FOR EACH ROW EXECUTE FUNCTION cdp_core.forbid_standing_claim_update();

-- -----------------------------------------------------------------------------
-- cdp_core.standing_recognition_determination
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cdp_core.standing_recognition_determination (
    determination_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    claim_id UUID NOT NULL,

    outcome_registry_name TEXT NOT NULL DEFAULT 'standing_recognition_outcome',
    outcome TEXT NOT NULL,

    outcome_basis TEXT NOT NULL,

    determined_by_actor_registry_name TEXT NOT NULL DEFAULT 'actor',
    determined_by_actor_id TEXT NOT NULL,

    determined_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_standing_determination_outcome_registry
        CHECK (outcome_registry_name = 'standing_recognition_outcome'),

    -- Only the two outcomes this slice's service layer actually writes.
    -- 'narrowed', 'deferred', and 'rejected' remain schema-supported in
    -- the standing_recognition_outcome vocabulary above but are not yet
    -- reachable through this table -- see the DDL header and
    -- authority_evaluation_result's chk_authority_evaluation_result_value
    -- for the identical precedent. 'narrowed' is withheld specifically
    -- because this table has no outcome_scope column: writing 'narrowed'
    -- without a recorded scope would be enforcement-indistinguishable
    -- from 'recognized' while still claiming a narrowing the table cannot
    -- describe (review finding on PR #53).
    CONSTRAINT chk_standing_determination_outcome_value
        CHECK (outcome IN ('recognized', 'denied')),

    CONSTRAINT chk_standing_determination_outcome_basis_not_blank
        CHECK (btrim(outcome_basis) <> ''),

    CONSTRAINT chk_standing_determination_determined_by_registry
        CHECK (determined_by_actor_registry_name = 'actor'),

    -- One determination per claim in this slice -- narrower than
    -- RFC-CDP-033 SS9.2's general model, which allows a later
    -- determination to supersede an earlier one via
    -- supersedes_determination_id. Chained/corrected determinations are
    -- explicit future work (see the DDL header), not silently permitted
    -- or silently forbidden.
    CONSTRAINT uq_standing_determination_claim
        UNIQUE (claim_id),

    CONSTRAINT fk_standing_determination_claim
        FOREIGN KEY (claim_id)
        REFERENCES cdp_core.standing_claim (claim_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_standing_determination_outcome
        FOREIGN KEY (outcome_registry_name, outcome)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_standing_determination_determined_by
        FOREIGN KEY (determined_by_actor_registry_name, determined_by_actor_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.standing_recognition_determination IS
'Standing Recognition Determination (RFC-CDP-033 SS9.2, SS11.8). Immutable once created (enforced by trigger below) -- a correction is a new record referencing the prior one in a future session, never an edit to this one. This slice permits exactly one determination per claim (uq_standing_determination_claim) -- see the DDL header.';

CREATE INDEX IF NOT EXISTS idx_standing_determination_claim
    ON cdp_core.standing_recognition_determination (claim_id);

CREATE OR REPLACE FUNCTION cdp_core.forbid_standing_determination_delete()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION
        'cdp_core.standing_recognition_determination rows cannot be deleted (determination_id=%)',
        OLD.determination_id;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_standing_determination_forbid_delete ON cdp_core.standing_recognition_determination;
CREATE TRIGGER trg_standing_determination_forbid_delete
BEFORE DELETE ON cdp_core.standing_recognition_determination
FOR EACH ROW EXECUTE FUNCTION cdp_core.forbid_standing_determination_delete();

CREATE OR REPLACE FUNCTION cdp_core.forbid_standing_determination_update()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION
        'cdp_core.standing_recognition_determination rows are immutable and cannot be updated (determination_id=%)',
        OLD.determination_id;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_standing_determination_forbid_update ON cdp_core.standing_recognition_determination;
CREATE TRIGGER trg_standing_determination_forbid_update
BEFORE UPDATE ON cdp_core.standing_recognition_determination
FOR EACH ROW EXECUTE FUNCTION cdp_core.forbid_standing_determination_update();
