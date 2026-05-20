CREATE TABLE IF NOT EXISTS decision_envelopes (
    id UUID PRIMARY KEY,
    status TEXT NOT NULL,
    actor_id TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    record_hash TEXT NOT NULL,
    envelope JSONB NOT NULL
);
