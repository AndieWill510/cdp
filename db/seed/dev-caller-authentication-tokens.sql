-- CDP Caller Authentication — Local/Dev/Test Bootstrap Tokens
--
-- ============================================================================
-- DO NOT APPLY THIS FILE TO ANY DEPLOYMENT THAT MATTERS.
-- Every token seeded below is PUBLISHED IN PLAINTEXT IN THIS FILE, IN
-- VERSION CONTROL. It provides ZERO secrecy. It exists solely so this
-- repository's own automated tests and local Docker Compose stack can
-- exercise caller-binding (db/ddl/014-caller-authentication.sql) against
-- the three bounded system actors below without a chicken-and-egg problem
-- (they are seeded directly by SQL in db/ddl/010, db/ddl/011, and
-- db/ddl/015, not through register_actor, so they have no token from
-- that path).
-- ============================================================================
--
-- Why this file is not part of db/ddl/: db/ddl/ is the canonical
-- migration path -- every file there is meant to be applied, unmodified,
-- to any environment, including a real deployment. This file previously
-- lived inside db/ddl/014-caller-authentication.sql itself; a review
-- before merging PR #48 correctly identified that this meant a
-- deployment applying the normal migrations was born with known, active,
-- privileged credentials for cdp_identity_recognition_authority (who may
-- recognize/deny/contest any Identity Claim) and cdp_authority_grant_issuer
-- (who may issue/revoke any Authority Grant) -- and that a documentation
-- warning cannot turn that into a safe default. See
-- db/ddl/014-caller-authentication.sql's header for the corrected note.
--
-- How this is applied:
--   - Locally: docker/postgres/init/02_initialize_repository.sh applies
--     everything under db/seed/ (this directory), read-only mounted into
--     the Postgres init container, after db/ddl/ -- see
--     docker/docker-compose.yml's postgres volume mount.
--   - In CI: .github/workflows/cdp-ci.yml's full-cdp-slice-tests job
--     applies this directory explicitly, after db/ddl/, in its own
--     dedicated "Seed dev/test-only data" step -- never folded into the
--     "Seed canonical schema" step that mirrors what a real deployment
--     would run.
--   - Nowhere else. A real deployment's migration path applies only
--     db/ddl/*.sql and must provision credentials for these three actors
--     through its own out-of-band mechanism this repository does not
--     provide (see db/ddl/014-caller-authentication.sql's header for the
--     same limitation restated: this slice has no token rotation
--     mechanism either, so replacing these seed tokens with real ones
--     requires direct SQL against cdp_core.actor_bearer_token, not a
--     governed act).

INSERT INTO cdp_core.actor_bearer_token (actor_id, token_hash)
VALUES
    -- cdp_identity_recognition_authority
    -- plaintext (local/dev/test only, published, not a secret):
    -- seed-token-recognition-authority-local-dev-only-do-not-use-in-production
    ('cdp_identity_recognition_authority', '5809bb38a5cb422495b2ff3915df4cc96f48f2dc193c47c758a0f67ee065d68c'),
    -- cdp_authority_grant_issuer
    -- plaintext (local/dev/test only, published, not a secret):
    -- seed-token-grant-issuer-local-dev-only-do-not-use-in-production
    ('cdp_authority_grant_issuer', '42d009f04ee5e8a531669e3af23a0b193683b9b8d39c30004a03559948a9fe2f'),
    -- cdp_standing_recognition_authority (RFC-CDP-033, session 035)
    -- plaintext (local/dev/test only, published, not a secret):
    -- seed-token-standing-recognition-authority-local-dev-only-do-not-use-in-production
    ('cdp_standing_recognition_authority', '9881e65640b26313daac685f5efb43b0a394d6763b30f6f4e662be505361a1f8')
ON CONFLICT (token_hash) DO NOTHING;
