-- CDP local Postgres initialization
--
-- Mounted by docker/docker-compose.yml into:
--   /docker-entrypoint-initdb.d
--
-- This script creates the first local schemas and extensions needed for a
-- runnable CDP development database. It intentionally avoids creating the full
-- domain model. Canonical tables should move into explicit migrations once the
-- package skeleton and migration tooling are established.

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS cdp_core;
CREATE SCHEMA IF NOT EXISTS cdp_audit;
CREATE SCHEMA IF NOT EXISTS cdp_repair;
CREATE SCHEMA IF NOT EXISTS cdp_projection;

COMMENT ON SCHEMA cdp_core IS 'Transactional CDP governance state: decisions, envelopes, authority, and execution state.';
COMMENT ON SCHEMA cdp_audit IS 'Append-only audit/event records for replay, challenge, appeal, and repair.';
COMMENT ON SCHEMA cdp_repair IS 'Appeal, breach, affected-party review, repair agenda, and remedy tracking.';
COMMENT ON SCHEMA cdp_projection IS 'Read-optimized projections for reporting, dashboards, and replay views.';

-- Minimal smoke-test table. This gives local developers a fast way to confirm
-- the database is initialized without committing to the full schema yet.
CREATE TABLE IF NOT EXISTS cdp_core.schema_version (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    component TEXT NOT NULL UNIQUE,
    version TEXT NOT NULL,
    initialized_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO cdp_core.schema_version (component, version)
VALUES ('local-postgres-bootstrap', '0.1.0')
ON CONFLICT (component)
DO UPDATE SET
    version = EXCLUDED.version;

-- Minimal append-only event table for early local testing.
CREATE TABLE IF NOT EXISTS cdp_audit.event_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type TEXT NOT NULL,
    aggregate_type TEXT NOT NULL,
    aggregate_id TEXT NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_event_log_aggregate
    ON cdp_audit.event_log (aggregate_type, aggregate_id, created_at);

CREATE INDEX IF NOT EXISTS idx_event_log_event_type
    ON cdp_audit.event_log (event_type, created_at);

-- Minimal vector smoke-test table. Dimension is intentionally small for local
-- verification only; real embedding dimensions belong in migrations.
CREATE TABLE IF NOT EXISTS cdp_projection.vector_smoke_test (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    label TEXT NOT NULL,
    embedding vector(3),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO cdp_projection.vector_smoke_test (label, embedding)
VALUES ('bootstrap', '[0.1,0.2,0.3]')
ON CONFLICT DO NOTHING;
