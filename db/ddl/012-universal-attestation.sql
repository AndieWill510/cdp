-- CDP Universal Attestation DDL
--
-- Status: starter executable DDL for the Universal Attestation vertical
-- slice (RFC-CDP-031 SS2: "All mutating acts MUST be attested"), extending
-- the Identity/Attestation and Authority proof path (sessions 027, 028)
-- from decision creation alone to the other mutating governed acts this
-- repository already implements: raising a challenge, adjudicating a
-- challenge, authorizing execution, and recording an execution attempt.
--
-- Scope note:
--   "Universal" here means "every mutating act this repository's
--   canonical implementation path already has a governed service
--   function for" -- it does NOT mean every RFC-CDP-04x lifecycle stage
--   (Test, Legitimize, Learn have no implementation to attest yet) and it
--   does NOT extend to the Identity/Attestation/Authority slices'  own
--   mutations (register_actor, submit_identity_claim,
--   recognize/deny/contest_identity_claim, grant_authority,
--   revoke_authority). Attesting those would be circular -- they are the
--   foundation attestation itself depends on, not acts attestation can be
--   layered on top of. See docs/session-029-universal-attestation.md for
--   the full boundary statement.
--
-- Two additive changes:
--
--   1. governed_act_type vocabulary gains four new values:
--      challenge_raised, challenge_adjudicated, execution_authorized,
--      execution_recorded (decision_created already existed from
--      010-identity-and-attestation.sql).
--
--   2. cdp_core.attestation_record and cdp_core.authority_evaluation_result
--      both gain a nullable governed_act_ref_id UUID column. Both tables'
--      existing governed_act_registry_name/governed_act_decision_id pair
--      is sufficient to identify a *decision* uniquely, but not a
--      specific *sub-record* of it -- a decision can have many challenges,
--      and a challenge can be adjudicated more than once while
--      non-terminal (see 007-challenge-adjudication.sql's header), so
--      "which challenge" or "which adjudication" needs its own reference.
--      NULL for decision_created (unchanged, backward compatible with
--      every row 010/011 already wrote); populated with the challenge_id,
--      adjudication_id, authorization_id, or execution_id for the four
--      new act types. This is a polymorphic reference (its target table
--      depends on governed_act_type) and is deliberately not FK-enforced
--      -- no single FK target is correct for all four cases, and adding
--      four mutually-exclusive nullable FK columns instead was judged
--      more complex for no additional integrity benefit at this scope.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS cdp_core;

-- -----------------------------------------------------------------------------
-- Controlled vocabulary: four new governed_act_type values
-- -----------------------------------------------------------------------------

INSERT INTO cdp_core.identifier_registry (
    registry_name, identifier_id, identifier_type_registry_name, identifier_type_id,
    display_label, description, status
)
VALUES
    ('governed_act_type', 'challenge_raised', 'lookup_kind', 'enum_value', 'Challenge Raised', 'A challenge-raising governed act (RFC-CDP-042 Challenge).', 'active'),
    ('governed_act_type', 'challenge_adjudicated', 'lookup_kind', 'enum_value', 'Challenge Adjudicated', 'A challenge-adjudication governed act (challenge-level, not the full RFC-CDP-044 Adjudicate Protocol -- see 007-challenge-adjudication.sql).', 'active'),
    ('governed_act_type', 'execution_authorized', 'lookup_kind', 'enum_value', 'Execution Authorized', 'An execution-authorization governed act (RFC-CDP-046/051-adjacent; see 008-execution-authorization.sql for why this is an authorization gate, not legitimation).', 'active'),
    ('governed_act_type', 'execution_recorded', 'lookup_kind', 'enum_value', 'Execution Recorded', 'An execution-record governed act (RFC-CDP-047 Record; see 009-execution-record.sql).', 'active')
ON CONFLICT (registry_name, identifier_id)
DO UPDATE SET
    identifier_type_registry_name = EXCLUDED.identifier_type_registry_name,
    identifier_type_id = EXCLUDED.identifier_type_id,
    display_label = EXCLUDED.display_label,
    description = EXCLUDED.description,
    status = EXCLUDED.status,
    updated_at = now();

-- -----------------------------------------------------------------------------
-- cdp_core.attestation_record: add governed_act_ref_id
-- -----------------------------------------------------------------------------

ALTER TABLE cdp_core.attestation_record
    ADD COLUMN IF NOT EXISTS governed_act_ref_id UUID;

COMMENT ON COLUMN cdp_core.attestation_record.governed_act_ref_id IS
'Polymorphic sub-record reference (challenge_id / adjudication_id / authorization_id / execution_id), NULL for decision_created. See 012-universal-attestation.sql header.';

-- -----------------------------------------------------------------------------
-- cdp_core.authority_evaluation_result: add governed_act_ref_id
-- -----------------------------------------------------------------------------

ALTER TABLE cdp_core.authority_evaluation_result
    ADD COLUMN IF NOT EXISTS governed_act_ref_id UUID;

COMMENT ON COLUMN cdp_core.authority_evaluation_result.governed_act_ref_id IS
'Polymorphic sub-record reference (challenge_id / adjudication_id / authorization_id / execution_id), NULL for decision_created. See 012-universal-attestation.sql header.';
