-- CDP Identity and Attestation DDL
--
-- Status: starter executable DDL for the Identity and Attestation vertical
-- slice (RFC-CDP-030 Identify Protocol, RFC-CDP-031 Attest Protocol).
-- Scope: three new governed tables plus the controlled vocabulary they need.
--
-- Constitutional scope note:
--   RFC-CDP-030 and RFC-CDP-031 are both thin (Draft v0.3, no persistence
--   schema section) and do not themselves specify Identity Claim or
--   Attestation Record schemas. This migration composes their minimal
--   required-properties lists with RFC-CDP-033's existence/recognition/
--   scope distinction (RFC-CDP-033 SS11.2) and non-erasure rule
--   (RFC-CDP-033 SS11.6, "denial of standing does not extinguish the
--   underlying relationship") to design the Identity Claim state machine
--   below. This is a documented interpretation of an underspecified corpus
--   area, not a silent invention -- see docs/session-027-identity-and-attestation.md.
--
--   This slice deliberately does NOT implement Authority (RFC-CDP-032),
--   Standing (RFC-CDP-033), Legitimize (RFC-CDP-045), or Repair. It does
--   not implement real cryptographic signature verification, OAuth, SSO,
--   or password/biometric storage -- attestation_method/credential_reference
--   record a claimed, opaque, non-secret evidence handle, and verification
--   here means "the actor is active and holds a recognized, in-scope
--   Identity Claim," not cryptographic proof. See the session doc for the
--   honest scope of what "verified" means in this slice.
--
-- Design pattern note:
--   Actors already exist today only as rows in cdp_core.identifier_registry
--   (registry_name = 'actor'), referenced by every other table via
--   (registry_name, identifier_id). cdp_core.actor below is a governed
--   elaboration table that sits on top of an identifier_registry row (FK'd
--   to it, not replacing it) and adds the richness (type, display mode,
--   lifecycle status, immutable continuity key) that identifier_registry
--   itself does not carry. Every controlled-vocabulary column follows the
--   existing registry-qualified enum + FK pattern from
--   005-challenge-transition.sql / 007-challenge-adjudication.sql: a
--   dedicated identifier_registry registry per column, not a bare CHECK.
--
-- Identity is not personhood:
--   cdp_core.actor stores no legal-name, credential, or secret field.
--   display_label (on the underlying identifier_registry row) is the only
--   human-readable label and is never treated as proof of identity --
--   identity_claim.claimed_identity_descriptor is a separate, contestable
--   claim, and recognition of it is a separate governed act again.
--
-- Anti-erasure:
--   cdp_core.identity_claim rows can never be deleted (enforced by a
--   BEFORE DELETE trigger, not merely by convention) -- denial, contest, or
--   supersession are recorded as recognition_status transitions on the
--   existing row (or a new row linked via supersedes_claim_id /
--   superseded_by_claim_id), never as erasure. cdp_core.actor's
--   identity_continuity_key is immutable once set (enforced by a BEFORE
--   UPDATE trigger) so accountable continuity cannot be silently
--   re-pointed even by a later update.

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
    ('registry', 'cdp_actor_type', 'lookup_kind', 'registry', 'CDP Actor Type Registry', 'Controlled actor types for the governed Actor Registry (RFC-CDP-030).', 'active'),
    ('registry', 'actor_display_mode', 'lookup_kind', 'registry', 'Actor Display Mode Registry', 'Controlled display-exposure modes for a governed actor.', 'active'),
    ('registry', 'actor_status', 'lookup_kind', 'registry', 'Actor Status Registry', 'Controlled lifecycle status for a governed actor.', 'active'),
    ('registry', 'identity_claim_recognition_status', 'lookup_kind', 'registry', 'Identity Claim Recognition Status Registry', 'Controlled recognition states for an Identity Claim (RFC-CDP-030/033).', 'active'),
    ('registry', 'attestation_method', 'lookup_kind', 'registry', 'Attestation Method Registry', 'Controlled attestation/signing methods (RFC-CDP-031).', 'active'),
    ('registry', 'governed_act_type', 'lookup_kind', 'registry', 'Governed Act Type Registry', 'Controlled governed-act types eligible for attestation.', 'active'),
    ('registry', 'attestation_verification_result', 'lookup_kind', 'registry', 'Attestation Verification Result Registry', 'Controlled verification outcomes for an Attestation Record.', 'active')
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
    -- cdp_actor_type: RFC-CDP-030 SS2 minimum (human, institution, synthetic)
    -- plus 'collective' for community/collective actors, both explicitly
    -- required by this slice's constitutional constraints. Distinct from
    -- the legacy 'actor_type' registry (agent/human/system/institution/
    -- unknown) already seeded by 001 and used by cdp_core.decision_registry
    -- -- that registry is not modified here, so existing decision-creation
    -- behavior is unaffected.
    ('cdp_actor_type', 'human', 'lookup_kind', 'enum_value', 'Human', 'A human actor.', 'active'),
    ('cdp_actor_type', 'institution', 'lookup_kind', 'enum_value', 'Institution', 'An institutional actor.', 'active'),
    ('cdp_actor_type', 'synthetic', 'lookup_kind', 'enum_value', 'Synthetic', 'A synthetic (AI/automated) actor.', 'active'),
    ('cdp_actor_type', 'collective', 'lookup_kind', 'enum_value', 'Collective', 'A collective or community actor.', 'active'),

    -- actor_display_mode: a capability of any actor_type, not a type
    -- itself -- a human, institution, synthetic, or collective actor may
    -- each be protected or pseudonymous. This is what lets accountable
    -- continuity (actor_id, identity_continuity_key) coexist with a public
    -- surface that need not expose more than a pseudonym.
    ('actor_display_mode', 'public', 'lookup_kind', 'enum_value', 'Public', 'Actor may be displayed by its registered display label without restriction.', 'active'),
    ('actor_display_mode', 'protected', 'lookup_kind', 'enum_value', 'Protected', 'Actor identity details are restricted from public/API display beyond the registered display label.', 'active'),
    ('actor_display_mode', 'pseudonymous', 'lookup_kind', 'enum_value', 'Pseudonymous', 'Actor participates under a stable pseudonym; underlying identity claim detail is not publicly exposed.', 'active'),

    ('actor_status', 'active', 'lookup_kind', 'enum_value', 'Active', 'Actor may currently participate and be attested for.', 'active'),
    ('actor_status', 'suspended', 'lookup_kind', 'enum_value', 'Suspended', 'Actor participation is temporarily suspended.', 'active'),
    ('actor_status', 'revoked', 'lookup_kind', 'enum_value', 'Revoked', 'Actor participation has been revoked.', 'active'),
    ('actor_status', 'superseded', 'lookup_kind', 'enum_value', 'Superseded', 'Actor record has been superseded by a later governed actor record.', 'active'),

    -- identity_claim_recognition_status: existence (the actor) / claim
    -- (this row) / recognition (this status) are kept distinct per
    -- RFC-CDP-033 SS11.2. 'denied', 'contested', and 'superseded' are all
    -- reachable without ever deleting the row (enforced by trigger below).
    ('identity_claim_recognition_status', 'pending', 'lookup_kind', 'enum_value', 'Pending', 'Claim submitted; recognition not yet decided.', 'active'),
    ('identity_claim_recognition_status', 'recognized', 'lookup_kind', 'enum_value', 'Recognized', 'CDP has accepted the claim for its declared purpose_scope.', 'active'),
    ('identity_claim_recognition_status', 'denied', 'lookup_kind', 'enum_value', 'Denied', 'CDP has declined to recognize the claim. The claim itself is preserved, not erased.', 'active'),
    ('identity_claim_recognition_status', 'contested', 'lookup_kind', 'enum_value', 'Contested', 'The claim or its recognition is under active dispute.', 'active'),
    ('identity_claim_recognition_status', 'superseded', 'lookup_kind', 'enum_value', 'Superseded', 'A later claim supersedes this one; this row is preserved and linked via superseded_by_claim_id.', 'active'),
    ('identity_claim_recognition_status', 'withdrawn', 'lookup_kind', 'enum_value', 'Withdrawn', 'The claimant withdrew the claim. The row is preserved, not deleted.', 'active'),

    -- attestation_method: a claimed, opaque evidence category, not a
    -- cryptographic guarantee -- see the header note on this slice's
    -- honest verification scope.
    ('attestation_method', 'shared_secret_reference', 'lookup_kind', 'enum_value', 'Shared Secret Reference', 'Attestation backed by a reference to an out-of-band shared secret; the secret itself is never stored here.', 'active'),
    ('attestation_method', 'cryptographic_signature', 'lookup_kind', 'enum_value', 'Cryptographic Signature', 'Attestation backed by a cryptographic signature; only a reference/digest is stored here, never key material.', 'active'),
    ('attestation_method', 'delegated_trust_reference', 'lookup_kind', 'enum_value', 'Delegated Trust Reference', 'Attestation backed by a reference to a delegated trust relationship (e.g. an upstream identity provider assertion), recorded by reference only.', 'active'),

    -- governed_act_type: intentionally minimal for this slice -- only the
    -- one proof-path act (decision creation) is seeded. Extending this
    -- registry to cover other mutating acts is future work, not a schema
    -- change.
    ('governed_act_type', 'decision_created', 'lookup_kind', 'enum_value', 'Decision Created', 'A decision-creation governed act (RFC-CDP-041 Propose).', 'active'),

    ('attestation_verification_result', 'verified', 'lookup_kind', 'enum_value', 'Verified', 'The attestation was verified against the actor''s recognized, in-scope identity claim.', 'active'),
    ('attestation_verification_result', 'failed', 'lookup_kind', 'enum_value', 'Failed', 'Verification failed. Reserved for future asynchronous/out-of-band verification flows; this slice''s synchronous service path fails closed via exception instead of persisting a failed row (see docs/session-027-identity-and-attestation.md).', 'active')
ON CONFLICT (registry_name, identifier_id)
DO UPDATE SET
    identifier_type_registry_name = EXCLUDED.identifier_type_registry_name,
    identifier_type_id = EXCLUDED.identifier_type_id,
    display_label = EXCLUDED.display_label,
    description = EXCLUDED.description,
    status = EXCLUDED.status,
    updated_at = now();

-- A system actor for the verifier_actor_id role in attestation_record. This
-- slice's verification is a governed CDP process, not a human/institutional
-- decision, so it is attributed to a named system actor rather than left
-- implicit.
INSERT INTO cdp_core.identifier_registry (
    registry_name, identifier_id, identifier_type_registry_name, identifier_type_id,
    display_label, description, status
)
VALUES
    ('actor', 'cdp_attestation_service', 'actor_type', 'system', 'CDP Attestation Service', 'System actor that performs claim-based attestation verification for this slice.', 'active')
ON CONFLICT (registry_name, identifier_id)
DO UPDATE SET
    identifier_type_registry_name = EXCLUDED.identifier_type_registry_name,
    identifier_type_id = EXCLUDED.identifier_type_id,
    display_label = EXCLUDED.display_label,
    description = EXCLUDED.description,
    status = EXCLUDED.status,
    updated_at = now();

-- -----------------------------------------------------------------------------
-- cdp_core.actor
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cdp_core.actor (
    actor_pk UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    actor_registry_name TEXT NOT NULL DEFAULT 'actor',
    actor_id TEXT NOT NULL,

    actor_type_registry_name TEXT NOT NULL DEFAULT 'cdp_actor_type',
    actor_type TEXT NOT NULL,

    display_mode_registry_name TEXT NOT NULL DEFAULT 'actor_display_mode',
    display_mode TEXT NOT NULL DEFAULT 'public',

    actor_status_registry_name TEXT NOT NULL DEFAULT 'actor_status',
    actor_status TEXT NOT NULL DEFAULT 'active',

    -- Immutable once set (enforced by trigger below). This is the stable
    -- anchor for "internal continuity remains accountable" even when
    -- display_mode hides the actor's presentation from public/API surfaces.
    identity_continuity_key UUID NOT NULL DEFAULT gen_random_uuid(),

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_actor_registry
        CHECK (actor_registry_name = 'actor'),

    CONSTRAINT chk_actor_type_registry
        CHECK (actor_type_registry_name = 'cdp_actor_type'),

    CONSTRAINT chk_actor_display_mode_registry
        CHECK (display_mode_registry_name = 'actor_display_mode'),

    CONSTRAINT chk_actor_status_registry
        CHECK (actor_status_registry_name = 'actor_status'),

    CONSTRAINT uq_actor_identity
        UNIQUE (actor_registry_name, actor_id),

    CONSTRAINT fk_actor_identifier
        FOREIGN KEY (actor_registry_name, actor_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_actor_type
        FOREIGN KEY (actor_type_registry_name, actor_type)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_actor_display_mode
        FOREIGN KEY (display_mode_registry_name, display_mode)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_actor_status
        FOREIGN KEY (actor_status_registry_name, actor_status)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.actor IS
'Governed Actor Registry (RFC-CDP-030). Elaborates an existing cdp_core.identifier_registry (registry_name=actor) row with type, display mode, lifecycle status, and an immutable continuity key. Not a claim about personhood, legal identity, or dignity -- see the DDL file header.';

CREATE INDEX IF NOT EXISTS idx_actor_type
    ON cdp_core.actor (actor_type);

CREATE INDEX IF NOT EXISTS idx_actor_status
    ON cdp_core.actor (actor_status);

CREATE OR REPLACE FUNCTION cdp_core.enforce_actor_identity_continuity()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.identity_continuity_key IS DISTINCT FROM OLD.identity_continuity_key THEN
        RAISE EXCEPTION
            'cdp_core.actor.identity_continuity_key is immutable and cannot be changed (actor_id=%)',
            OLD.actor_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_actor_identity_continuity_immutable ON cdp_core.actor;
CREATE TRIGGER trg_actor_identity_continuity_immutable
BEFORE UPDATE ON cdp_core.actor
FOR EACH ROW EXECUTE FUNCTION cdp_core.enforce_actor_identity_continuity();

CREATE OR REPLACE FUNCTION cdp_core.forbid_actor_delete()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION
        'cdp_core.actor rows cannot be deleted (actor_id=%); use actor_status to retire an actor',
        OLD.actor_id;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_actor_forbid_delete ON cdp_core.actor;
CREATE TRIGGER trg_actor_forbid_delete
BEFORE DELETE ON cdp_core.actor
FOR EACH ROW EXECUTE FUNCTION cdp_core.forbid_actor_delete();

-- -----------------------------------------------------------------------------
-- cdp_core.identity_claim
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cdp_core.identity_claim (
    claim_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    actor_registry_name TEXT NOT NULL DEFAULT 'actor',
    actor_id TEXT NOT NULL,

    claimant_actor_registry_name TEXT NOT NULL DEFAULT 'actor',
    claimant_actor_id TEXT NOT NULL,

    -- Free-text descriptor of what is claimed (e.g. "continuity of actor
    -- X under pseudonym Y", "institutional signer for org Z"). Not a
    -- legal-name field -- this is a claim, not a verified fact, and
    -- recognition below does not turn it into one either.
    claimed_identity_descriptor TEXT NOT NULL,

    -- Free-text governed purpose/scope this claim is submitted for
    -- (proportionality principle: a claim is scoped to a purpose, not
    -- universal). Not a controlled vocabulary -- scope is inherently
    -- contextual, matching RFC-CDP-032's flexible `scope` object rather
    -- than a fixed enum.
    purpose_scope TEXT NOT NULL,

    -- Opaque references to evidence, never the evidence/secret itself.
    evidence_refs JSONB NOT NULL DEFAULT '[]'::jsonb,

    recognition_status_registry_name TEXT NOT NULL DEFAULT 'identity_claim_recognition_status',
    recognition_status TEXT NOT NULL DEFAULT 'pending',

    recognized_by_actor_registry_name TEXT DEFAULT 'actor',
    recognized_by_actor_id TEXT,
    recognition_rationale TEXT,
    decided_at TIMESTAMPTZ,

    -- Supersession: a new claim may supersede an old one without deleting
    -- it. Both link fields are maintained together by the repository layer.
    supersedes_claim_id UUID,
    superseded_by_claim_id UUID,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_identity_claim_actor_registry
        CHECK (actor_registry_name = 'actor'),

    CONSTRAINT chk_identity_claim_claimant_registry
        CHECK (claimant_actor_registry_name = 'actor'),

    CONSTRAINT chk_identity_claim_recognition_status_registry
        CHECK (recognition_status_registry_name = 'identity_claim_recognition_status'),

    CONSTRAINT chk_identity_claim_recognized_by_registry
        CHECK (recognized_by_actor_registry_name IS NULL OR recognized_by_actor_registry_name = 'actor'),

    CONSTRAINT chk_identity_claim_descriptor_not_blank
        CHECK (btrim(claimed_identity_descriptor) <> ''),

    CONSTRAINT chk_identity_claim_purpose_scope_not_blank
        CHECK (btrim(purpose_scope) <> ''),

    -- 'pending', 'superseded', and 'withdrawn' do not require a recognition
    -- decision to have been made by anyone; 'recognized', 'denied', and
    -- 'contested' do -- who decided, why, and when must be recorded, not
    -- just the resulting label.
    CONSTRAINT chk_identity_claim_decision_requires_rationale
        CHECK (
            recognition_status IN ('pending', 'superseded', 'withdrawn')
            OR (
                recognized_by_actor_id IS NOT NULL
                AND recognition_rationale IS NOT NULL
                AND decided_at IS NOT NULL
            )
        ),

    CONSTRAINT fk_identity_claim_actor
        FOREIGN KEY (actor_registry_name, actor_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_identity_claim_claimant
        FOREIGN KEY (claimant_actor_registry_name, claimant_actor_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_identity_claim_recognition_status
        FOREIGN KEY (recognition_status_registry_name, recognition_status)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_identity_claim_recognized_by
        FOREIGN KEY (recognized_by_actor_registry_name, recognized_by_actor_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_identity_claim_supersedes
        FOREIGN KEY (supersedes_claim_id)
        REFERENCES cdp_core.identity_claim (claim_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_identity_claim_superseded_by
        FOREIGN KEY (superseded_by_claim_id)
        REFERENCES cdp_core.identity_claim (claim_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.identity_claim IS
'Identity Claim (RFC-CDP-030, RFC-CDP-033 SS11.2 existence/recognition/scope distinction). Denial, contest, or supersession are recorded as recognition_status transitions on this row or a linked successor row -- never as deletion (enforced by trigger below).';

CREATE INDEX IF NOT EXISTS idx_identity_claim_actor
    ON cdp_core.identity_claim (actor_registry_name, actor_id);

CREATE INDEX IF NOT EXISTS idx_identity_claim_status
    ON cdp_core.identity_claim (recognition_status);

CREATE OR REPLACE FUNCTION cdp_core.forbid_identity_claim_delete()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION
        'cdp_core.identity_claim rows cannot be deleted (claim_id=%); denial, contest, and supersession must be recorded as status transitions, not erasure',
        OLD.claim_id;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_identity_claim_forbid_delete ON cdp_core.identity_claim;
CREATE TRIGGER trg_identity_claim_forbid_delete
BEFORE DELETE ON cdp_core.identity_claim
FOR EACH ROW EXECUTE FUNCTION cdp_core.forbid_identity_claim_delete();

-- -----------------------------------------------------------------------------
-- cdp_core.attestation_record
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cdp_core.attestation_record (
    attestation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    actor_registry_name TEXT NOT NULL DEFAULT 'actor',
    actor_id TEXT NOT NULL,

    identity_claim_id UUID NOT NULL,

    governed_act_type_registry_name TEXT NOT NULL DEFAULT 'governed_act_type',
    governed_act_type TEXT NOT NULL,

    -- The specific governed act instance this attestation covers. For this
    -- slice, always a cdp_core.decision_registry row.
    governed_act_registry_name TEXT NOT NULL,
    governed_act_decision_id TEXT NOT NULL,

    attestation_method_registry_name TEXT NOT NULL DEFAULT 'attestation_method',
    attestation_method TEXT NOT NULL,

    -- Opaque, non-secret evidence handle. Never a raw secret, token,
    -- password, or private key -- see the DDL file header and
    -- chk_attestation_credential_reference_not_secret_named below.
    credential_reference TEXT NOT NULL,

    issued_at TIMESTAMPTZ NOT NULL,

    verification_result_registry_name TEXT NOT NULL DEFAULT 'attestation_verification_result',
    verification_result TEXT NOT NULL,

    verifier_actor_registry_name TEXT NOT NULL DEFAULT 'actor',
    verifier_actor_id TEXT NOT NULL,

    failure_reason TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_attestation_actor_registry
        CHECK (actor_registry_name = 'actor'),

    CONSTRAINT chk_attestation_governed_act_type_registry
        CHECK (governed_act_type_registry_name = 'governed_act_type'),

    CONSTRAINT chk_attestation_method_registry
        CHECK (attestation_method_registry_name = 'attestation_method'),

    CONSTRAINT chk_attestation_verification_result_registry
        CHECK (verification_result_registry_name = 'attestation_verification_result'),

    CONSTRAINT chk_attestation_verifier_registry
        CHECK (verifier_actor_registry_name = 'actor'),

    CONSTRAINT chk_attestation_credential_reference_not_blank
        CHECK (btrim(credential_reference) <> ''),

    -- Cheap guardrail against accidentally pasting a raw secret into the
    -- reference field: forbid the literal substrings a raw credential
    -- value would never need but a careless caller might use as a key
    -- name. This cannot detect all secrets; it is a backstop, not a
    -- substitute for the "reference, not the secret" contract the
    -- application layer is responsible for.
    CONSTRAINT chk_attestation_credential_reference_not_secret_named
        CHECK (
            credential_reference !~* '(^|[^a-z])(password|passwd)([^a-z]|$)'
        ),

    CONSTRAINT chk_attestation_failure_reason_pairing
        CHECK (
            (verification_result = 'verified' AND failure_reason IS NULL)
            OR (verification_result = 'failed' AND failure_reason IS NOT NULL)
        ),

    CONSTRAINT fk_attestation_actor
        FOREIGN KEY (actor_registry_name, actor_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_attestation_identity_claim
        FOREIGN KEY (identity_claim_id)
        REFERENCES cdp_core.identity_claim (claim_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_attestation_governed_act_type
        FOREIGN KEY (governed_act_type_registry_name, governed_act_type)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_attestation_governed_act_decision
        FOREIGN KEY (governed_act_registry_name, governed_act_decision_id)
        REFERENCES cdp_core.decision_registry (registry_name, decision_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_attestation_method
        FOREIGN KEY (attestation_method_registry_name, attestation_method)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_attestation_verification_result
        FOREIGN KEY (verification_result_registry_name, verification_result)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_attestation_verifier
        FOREIGN KEY (verifier_actor_registry_name, verifier_actor_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.attestation_record IS
'Attestation Record (RFC-CDP-031) binding an actor and a recognized, in-scope Identity Claim to one governed act. Distinct from RFC-CDP-034 Participation Integrity Attestation, which is a different, higher-level lifecycle artifact not implemented by this slice. Records a claimed evidence reference, never a secret.';

CREATE INDEX IF NOT EXISTS idx_attestation_actor
    ON cdp_core.attestation_record (actor_registry_name, actor_id);

CREATE INDEX IF NOT EXISTS idx_attestation_governed_act
    ON cdp_core.attestation_record (governed_act_registry_name, governed_act_decision_id);

CREATE OR REPLACE FUNCTION cdp_core.forbid_attestation_record_delete()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION
        'cdp_core.attestation_record rows cannot be deleted (attestation_id=%)',
        OLD.attestation_id;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_attestation_record_forbid_delete ON cdp_core.attestation_record;
CREATE TRIGGER trg_attestation_record_forbid_delete
BEFORE DELETE ON cdp_core.attestation_record
FOR EACH ROW EXECUTE FUNCTION cdp_core.forbid_attestation_record_delete();
