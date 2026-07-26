-- CDP Decision Class and Workflow Applicability Seed
--
-- Status: starter executable DDL for the first end-to-end decision vertical
-- slice (create decision -> start configured workflow -> initial task).
-- Scope: configuration data only. No new tables or columns.
--
-- This migration registers the decision class used by the seeded claim
-- example (see identifier_registry rows for actor=claims_review_agent,
-- object=claim_9981, predicate_verb=recommend_approval, and
-- permission_source=policy_claims_approval_v2 in 001), and configures
-- nemawashi_default_v1 v1 as the workflow applicable to that class.
--
-- registry_name = sample_attorney_demo, class_id = claim / claim_approval
-- follows the existing repository convention documented in
-- docs/decision-registry-hierarchy-analytics.md.
--
-- Row_hash and schema_version note:
--   cdp_core.schema_version is owned exclusively by the native Postgres
--   bootstrap script (docker/postgres/init/01-init-cdp.sql), which inserts
--   the single 'local-postgres-bootstrap' component row. Neither
--   001-decision-registry-kernel.sql nor 003-nemawashi-workflow-rules.sql
--   touch cdp_core.schema_version, so this migration does not either.

-- -----------------------------------------------------------------------------
-- Decision class: sample_attorney_demo / claim (parent) and claim_approval
-- -----------------------------------------------------------------------------

INSERT INTO cdp_core.decision_class_registry (
    registry_name, class_id, parent_class_id, class_label, class_level
)
VALUES
    ('sample_attorney_demo', 'claim', NULL, 'Claim Decisions', 0),
    ('sample_attorney_demo', 'claim_approval', 'claim', 'Claim Approval', 1)
ON CONFLICT (registry_name, class_id)
DO UPDATE SET
    parent_class_id = EXCLUDED.parent_class_id,
    class_label = EXCLUDED.class_label,
    class_level = EXCLUDED.class_level,
    updated_at = now();

-- -----------------------------------------------------------------------------
-- Workflow applicability: nemawashi_default_v1 v1 applies to claim_approval
-- -----------------------------------------------------------------------------
-- Only this single, already-seeded workflow_definition row is touched.
-- restricted_data_access_v1 and any other workflow_definition rows are left
-- untouched by this statement.

UPDATE cdp_core.workflow_definition
SET
    applies_to_registry_name = 'sample_attorney_demo',
    applies_to_decision_class_id = 'claim_approval',
    status = 'active',
    updated_at = now()
WHERE workflow_code = 'nemawashi_default_v1'
  AND workflow_version = 'v1';
