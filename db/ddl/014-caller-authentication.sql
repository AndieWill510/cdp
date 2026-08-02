-- CDP Caller Authentication DDL
--
-- Status: additive-only migration for session 032 (real authentication /
-- caller binding) -- the last of the five follow-up items named in review
-- of PR #41's evidence layer, and the one every prior session (027-031)
-- explicitly named as *not* implemented: RFC-CDP-030 SS6 and RFC-CDP-031
-- SS7 both state plainly that the API accepts a submitted actor_id at
-- face value, with nothing proving the HTTP caller controls it.
--
-- Scope: one new governed table, cdp_core.actor_bearer_token. An actor
-- receives an opaque bearer token when registered (register_actor,
-- cdp/core/services.py), shown once in that response and never again --
-- only its SHA-256 hash is stored here. Every route that accepts an
-- actor-asserting field at face value (submitted_by_actor_id,
-- decided_by_actor_id, issued_by_actor_id, revoked_by_actor_id,
-- claimant_actor_id on claim submission) now additionally requires an
-- `Authorization: Bearer <token>` header whose token hashes to an active
-- row here belonging to that exact actor_id -- see
-- verify_bearer_token in cdp/core/services.py.
--
-- What this closes, and what it does not:
--   This proves the HTTP caller controls a token issued to actor_id --
--   it is real, in the sense that a request asserting an actor_id it does
--   not hold a valid token for is rejected (401/403), not merely logged.
--   It is NOT OAuth/OIDC/SSO, not a session model, not a password, and
--   not cryptographic signing (RFC-CDP-031 SS4's signature-validity
--   requirement remains unmet -- a bearer token is presented, not signed
--   over). Token issuance has no rotation mechanism in this slice: a
--   revoked token's actor cannot obtain a replacement, and a lost token
--   is unrecoverable. See docs/session-032-caller-authentication.md for
--   the full boundary statement.
--
-- Design pattern note: mirrors cdp_core.identity_claim /
-- cdp_core.authority_grant's registry-qualified enum + FK pattern for
-- status, and their anti-erasure discipline -- a revoked token's row is
-- never deleted, only marked revoked (BEFORE DELETE trigger below).
--
-- Seeded actor tokens (local/dev/test use only -- see the block below):
--   The two bounded system actors that already exist only via direct SQL
--   seed rows (cdp_identity_recognition_authority,
--   cdp_authority_grant_issuer -- db/ddl/010, 011) were never created
--   through register_actor, so they have no token from that path. Fixed,
--   published plaintext tokens are seeded here so the bounded-actor
--   routes those two actors alone may call (claim recognition, authority
--   grant issuance/revocation) can also be caller-bound. THESE ARE
--   PUBLISHED IN THIS FILE, IN PLAINTEXT, IN VERSION CONTROL -- they
--   provide zero secrecy and MUST NOT be treated as credentials in any
--   deployment that matters. They exist so this repository's own tests
--   and local Docker stack can exercise the caller-binding check against
--   these two bounded actors without a chicken-and-egg problem. A real
--   deployment would need to rotate these before going anywhere near
--   production -- and this slice provides no rotation mechanism to do so
--   (see the "what this closes" note above).

CREATE EXTENSION IF NOT EXISTS pgcrypto;

INSERT INTO cdp_core.identifier_registry (
    registry_name, identifier_id, identifier_type_registry_name, identifier_type_id,
    display_label, description, status
)
VALUES
    ('registry', 'actor_bearer_token_status', 'lookup_kind', 'registry', 'Actor Bearer Token Status Registry', 'Controlled lifecycle status for a governed Actor Bearer Token.', 'active')
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
    ('actor_bearer_token_status', 'active', 'lookup_kind', 'enum_value', 'Active', 'Token may currently be used to authenticate its actor as an HTTP caller.', 'active'),
    ('actor_bearer_token_status', 'revoked', 'lookup_kind', 'enum_value', 'Revoked', 'Token has been revoked and may no longer be used. The row is preserved, not deleted.', 'active')
ON CONFLICT (registry_name, identifier_id)
DO UPDATE SET
    identifier_type_registry_name = EXCLUDED.identifier_type_registry_name,
    identifier_type_id = EXCLUDED.identifier_type_id,
    display_label = EXCLUDED.display_label,
    description = EXCLUDED.description,
    status = EXCLUDED.status,
    updated_at = now();

-- -----------------------------------------------------------------------------
-- cdp_core.actor_bearer_token
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cdp_core.actor_bearer_token (
    token_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    actor_registry_name TEXT NOT NULL DEFAULT 'actor',
    actor_id TEXT NOT NULL,

    -- SHA-256 hex digest of the bearer token. The plaintext token is
    -- never stored -- it is generated, returned once in the
    -- register_actor response, and discarded by this system immediately
    -- after hashing.
    token_hash TEXT NOT NULL,

    status_registry_name TEXT NOT NULL DEFAULT 'actor_bearer_token_status',
    status TEXT NOT NULL DEFAULT 'active',

    issued_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    revoked_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_actor_bearer_token_actor_registry
        CHECK (actor_registry_name = 'actor'),

    CONSTRAINT chk_actor_bearer_token_status_registry
        CHECK (status_registry_name = 'actor_bearer_token_status'),

    CONSTRAINT chk_actor_bearer_token_hash_not_blank
        CHECK (btrim(token_hash) <> ''),

    -- revoked_at recorded if and only if status = 'revoked'.
    CONSTRAINT chk_actor_bearer_token_revocation_consistency
        CHECK (
            (status = 'revoked' AND revoked_at IS NOT NULL)
            OR (status <> 'revoked' AND revoked_at IS NULL)
        ),

    CONSTRAINT uq_actor_bearer_token_hash
        UNIQUE (token_hash),

    CONSTRAINT fk_actor_bearer_token_actor
        FOREIGN KEY (actor_registry_name, actor_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_actor_bearer_token_status
        FOREIGN KEY (status_registry_name, status)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED
);

-- One active token per actor at a time -- a partial unique index rather
-- than a table-wide UNIQUE(actor_id), since a revoked token's row is
-- preserved (anti-erasure), so multiple historical rows for the same
-- actor_id are expected; only one may be 'active' at once.
CREATE UNIQUE INDEX IF NOT EXISTS uq_actor_bearer_token_one_active_per_actor
    ON cdp_core.actor_bearer_token (actor_id)
    WHERE status = 'active';

CREATE INDEX IF NOT EXISTS ix_actor_bearer_token_hash
    ON cdp_core.actor_bearer_token (token_hash);

-- Anti-erasure: a token's row is never deleted, only marked revoked --
-- same discipline as cdp_core.identity_claim / cdp_core.authority_grant.
CREATE OR REPLACE FUNCTION cdp_core.forbid_actor_bearer_token_delete()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'cdp_core.actor_bearer_token rows cannot be deleted; revoke the token instead (status = ''revoked'')';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_actor_bearer_token_forbid_delete ON cdp_core.actor_bearer_token;
CREATE TRIGGER trg_actor_bearer_token_forbid_delete
    BEFORE DELETE ON cdp_core.actor_bearer_token
    FOR EACH ROW
    EXECUTE FUNCTION cdp_core.forbid_actor_bearer_token_delete();

-- -----------------------------------------------------------------------------
-- Seeded tokens for the two bounded system actors (local/dev/test use
-- only -- see the file header's "Seeded actor tokens" note above).
-- -----------------------------------------------------------------------------

INSERT INTO cdp_core.actor_bearer_token (actor_id, token_hash)
VALUES
    -- cdp_identity_recognition_authority
    -- plaintext (local/dev/test only, published, not a secret):
    -- seed-token-recognition-authority-local-dev-only-do-not-use-in-production
    ('cdp_identity_recognition_authority', '5809bb38a5cb422495b2ff3915df4cc96f48f2dc193c47c758a0f67ee065d68c'),
    -- cdp_authority_grant_issuer
    -- plaintext (local/dev/test only, published, not a secret):
    -- seed-token-grant-issuer-local-dev-only-do-not-use-in-production
    ('cdp_authority_grant_issuer', '42d009f04ee5e8a531669e3af23a0b193683b9b8d39c30004a03559948a9fe2f')
ON CONFLICT (token_hash) DO NOTHING;
