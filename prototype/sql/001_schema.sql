CREATE TABLE IF NOT EXISTS cdp_proposal (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    domain VARCHAR(100) NOT NULL,
    proposer VARCHAR(200) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'proposed',
    policy_basis TEXT NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cdp_challenge (
    id BIGSERIAL PRIMARY KEY,
    proposal_id BIGINT NOT NULL REFERENCES cdp_proposal(id) ON DELETE CASCADE,
    challenger VARCHAR(200) NOT NULL,
    challenge_type VARCHAR(100) NOT NULL,
    reason TEXT NOT NULL,
    evidence JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cdp_adjudication (
    id BIGSERIAL PRIMARY KEY,
    proposal_id BIGINT NOT NULL REFERENCES cdp_proposal(id) ON DELETE CASCADE,
    adjudicator VARCHAR(200) NOT NULL,
    decision VARCHAR(50) NOT NULL,
    rationale TEXT NOT NULL,
    conditions JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cdp_legitimation (
    id BIGSERIAL PRIMARY KEY,
    proposal_id BIGINT NOT NULL REFERENCES cdp_proposal(id) ON DELETE CASCADE,
    legitimizer VARCHAR(200) NOT NULL,
    status VARCHAR(50) NOT NULL,
    basis TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cdp_execution (
    id BIGSERIAL PRIMARY KEY,
    proposal_id BIGINT NOT NULL REFERENCES cdp_proposal(id) ON DELETE CASCADE,
    executor VARCHAR(200) NOT NULL,
    execution_target VARCHAR(250) NOT NULL,
    execution_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    status VARCHAR(50) NOT NULL DEFAULT 'submitted',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cdp_event (
    id BIGSERIAL PRIMARY KEY,
    proposal_id BIGINT NOT NULL REFERENCES cdp_proposal(id) ON DELETE CASCADE,
    event_type VARCHAR(100) NOT NULL,
    actor VARCHAR(200) NOT NULL,
    body JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_cdp_proposal_status ON cdp_proposal(status);
CREATE INDEX IF NOT EXISTS ix_cdp_challenge_proposal_id ON cdp_challenge(proposal_id);
CREATE INDEX IF NOT EXISTS ix_cdp_adjudication_proposal_id ON cdp_adjudication(proposal_id);
CREATE INDEX IF NOT EXISTS ix_cdp_legitimation_proposal_id ON cdp_legitimation(proposal_id);
CREATE INDEX IF NOT EXISTS ix_cdp_execution_proposal_id ON cdp_execution(proposal_id);
CREATE INDEX IF NOT EXISTS ix_cdp_event_proposal_id ON cdp_event(proposal_id);

INSERT INTO cdp_proposal (title, domain, proposer, status, policy_basis, payload)
VALUES (
    'Seed proposal: manual review for anomalous claim cluster',
    'cms',
    'seed-script',
    'proposed',
    'cluster_risk_score > 0.90',
    '{"cluster_id":"CLUSTER-001","risk_score":0.93}'::jsonb
)
ON CONFLICT DO NOTHING;
