-- CDP Identity Claim Scope DDL
--
-- Status: additive-only migration for session 030 (richer purpose/scope
-- semantics for Identity Claims -- one of the follow-up items named in
-- review of the Identity/Attestation and Authority slices' evidence
-- layer).
--
-- Scope model (mirrors the two-level scope authority_grant already has --
-- see 011-authority-and-delegation.sql's "Scope model" note):
--   scope_registry_name (nullable) + scope_decision_class_id (nullable).
--   A NULL scope_registry_name means "not scoped to any particular
--   registry" -- the claim's purpose_scope alone continues to govern which
--   governed acts it covers, exactly as every claim submitted before this
--   migration already behaves (see cdp/core/services.py's
--   _check_claim_recognized_and_scoped). A non-NULL scope_registry_name
--   requires an exact match against the governed act's registry_name. A
--   NULL scope_decision_class_id, with scope_registry_name set, means
--   "every decision class in that registry" -- the wildcard rule, same as
--   authority_grant's. scope_decision_class_id is never meaningful without
--   scope_registry_name also being set (enforced by a CHECK constraint
--   below).
--
-- Why nullable, unlike authority_grant.scope_registry_name (mandatory
-- there): authority_grant was a new table introduced with this scope
-- model from the start, so it could require it outright.
-- cdp_core.identity_claim already has rows, and a purpose_scope-only proof
-- path already Integration Tested (E4) across sessions 027-029, that this
-- migration must not retroactively invalidate -- an additive migration
-- cannot silently rewrite what an existing row means. Making the columns
-- nullable, with NULL meaning "governed by purpose_scope alone," is what
-- makes this genuinely additive rather than a breaking change disguised
-- as one: every claim submitted before this migration, and every claim
-- submitted after it that simply omits the new fields, behaves exactly as
-- it did before.
--
-- This is still not RFC-CDP-032 Authority's model or a general governed
-- scope grammar -- it composes the same two fixed dimensions (registry,
-- decision class) authority_grant already does, not a jurisdiction/
-- risk-level/environment/affected-parties model. See
-- docs/session-030-identity-claim-scope.md.

ALTER TABLE cdp_core.identity_claim
    ADD COLUMN IF NOT EXISTS scope_registry_name TEXT;

ALTER TABLE cdp_core.identity_claim
    ADD COLUMN IF NOT EXISTS scope_decision_class_id TEXT;

-- Postgres has no ADD CONSTRAINT IF NOT EXISTS; guard manually so this
-- migration stays rerun-safe (same pattern as
-- 006-audit-event-ordering.sql's uq_event_log_event_sequence).
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'chk_identity_claim_scope_decision_class_requires_registry'
    ) THEN
        ALTER TABLE cdp_core.identity_claim
            ADD CONSTRAINT chk_identity_claim_scope_decision_class_requires_registry
            CHECK (scope_decision_class_id IS NULL OR scope_registry_name IS NOT NULL);
    END IF;
END;
$$;

COMMENT ON COLUMN cdp_core.identity_claim.scope_registry_name IS
'Nullable registry-level scope, exact-match. NULL means this claim is not scoped to a particular registry and only purpose_scope governs coverage -- see this file''s header.';

COMMENT ON COLUMN cdp_core.identity_claim.scope_decision_class_id IS
'Nullable decision-class-level scope. NULL with scope_registry_name set means "every decision class in that registry" (wildcard); meaningless if scope_registry_name is NULL (enforced by CHECK).';
