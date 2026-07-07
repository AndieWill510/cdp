-- CDP Nemawashi Workflow and Rules Engine DDL
--
-- Status: starter executable DDL for stakeholder discovery, workflow state,
-- rules evaluation, governed communication, and Nemawashi projections.
-- Scope: extends the decision-registry kernel without turning config_lookup
-- into a governance rules engine.
--
-- Design rule:
--   config_lookup may hold boring non-governance defaults.
--   Governed workflow/rule/stakeholder authority belongs here.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS cdp_core;
CREATE SCHEMA IF NOT EXISTS cdp_projection;

-- -----------------------------------------------------------------------------
-- Additional identifier registries and controlled values for Nemawashi workflow.
-- -----------------------------------------------------------------------------
-- These rows register controlled namespaces used by workflow, rules, stakeholder,
-- and communication tables. The rows are controlled identifiers, not executable
-- rules and not decision records.

INSERT INTO cdp_core.identifier_registry (
    registry_name, identifier_id, identifier_type_registry_name, identifier_type_id,
    display_label, description, status
)
VALUES
    ('registry', 'stakeholder_role', 'lookup_kind', 'registry', 'Stakeholder Role Registry', 'Controlled stakeholder roles for decision participation.', 'active'),
    ('registry', 'participation_status', 'lookup_kind', 'registry', 'Participation Status Registry', 'Controlled stakeholder participation states.', 'active'),
    ('registry', 'standing_status', 'lookup_kind', 'registry', 'Standing Status Registry', 'Controlled standing states aligned to lifecycle envelopes.', 'active'),
    ('registry', 'workflow_definition_code', 'lookup_kind', 'registry', 'Workflow Definition Code Registry', 'Registered workflow definitions.', 'active'),
    ('registry', 'workflow_stage_code', 'lookup_kind', 'registry', 'Workflow Stage Code Registry', 'Registered workflow stage codes.', 'active'),
    ('registry', 'workflow_status', 'lookup_kind', 'registry', 'Workflow Status Registry', 'Controlled workflow instance states.', 'active'),
    ('registry', 'workflow_task_type', 'lookup_kind', 'registry', 'Workflow Task Type Registry', 'Controlled workflow task types.', 'active'),
    ('registry', 'workflow_task_status', 'lookup_kind', 'registry', 'Workflow Task Status Registry', 'Controlled workflow task states.', 'active'),
    ('registry', 'rule_set_code', 'lookup_kind', 'registry', 'Rule Set Code Registry', 'Registered rule sets.', 'active'),
    ('registry', 'rule_scope', 'lookup_kind', 'registry', 'Rule Scope Registry', 'Controlled scopes for governed rules.', 'active'),
    ('registry', 'rule_condition_language', 'lookup_kind', 'registry', 'Rule Condition Language Registry', 'Allowed deterministic condition languages.', 'active'),
    ('registry', 'rule_action_type', 'lookup_kind', 'registry', 'Rule Action Type Registry', 'Controlled actions produced by rules.', 'active'),
    ('registry', 'rule_evaluation_status', 'lookup_kind', 'registry', 'Rule Evaluation Status Registry', 'Controlled outcomes for rule evaluation.', 'active'),
    ('registry', 'communication_thread_type', 'lookup_kind', 'registry', 'Communication Thread Type Registry', 'Controlled governed thread types.', 'active'),
    ('registry', 'communication_thread_status', 'lookup_kind', 'registry', 'Communication Thread Status Registry', 'Controlled governed thread states.', 'active'),
    ('registry', 'communication_message_type', 'lookup_kind', 'registry', 'Communication Message Type Registry', 'Controlled governed message types.', 'active'),
    ('registry', 'communication_message_status', 'lookup_kind', 'registry', 'Communication Message Status Registry', 'Controlled governed message states.', 'active'),
    ('registry', 'notification_status', 'lookup_kind', 'registry', 'Notification Status Registry', 'Controlled notification states.', 'active'),
    ('registry', 'lifecycle_stage', 'lookup_kind', 'registry', 'Lifecycle Stage Registry', 'Controlled lifecycle stages for workflow alignment.', 'active')
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
    -- Actor types and demo actors used by stakeholder maps.
    ('actor_type', 'team', 'lookup_kind', 'enum_value', 'Team', 'Team actor.', 'active'),
    ('actor_type', 'organization', 'lookup_kind', 'enum_value', 'Organization', 'Organization actor.', 'active'),

    ('actor', 'privacy_counsel', 'actor_type', 'human', 'Privacy Counsel', 'Demo privacy counsel stakeholder.', 'active'),
    ('actor', 'security_reviewer', 'actor_type', 'human', 'Security Reviewer', 'Demo security reviewer stakeholder.', 'active'),
    ('actor', 'data_owner', 'actor_type', 'human', 'Data Owner', 'Demo restricted-data owner stakeholder.', 'active'),
    ('actor', 'system_owner', 'actor_type', 'human', 'System Owner', 'Demo system owner stakeholder.', 'active'),
    ('actor', 'affected_party_proxy', 'actor_type', 'human', 'Affected Party Proxy', 'Demo affected-party proxy stakeholder.', 'active'),
    ('actor', 'trust_safety_policy_team', 'actor_type', 'team', 'Trust & Safety Policy Team', 'Demo Trust & Safety policy team stakeholder.', 'active'),

    -- Lifecycle stages.
    ('lifecycle_stage', 'nemawashi', 'lookup_kind', 'enum_value', 'Nemawashi', 'Pre-proposal alignment and dissent-discovery stage.', 'active'),
    ('lifecycle_stage', 'propose', 'lookup_kind', 'enum_value', 'Propose', 'Proposal stage.', 'active'),
    ('lifecycle_stage', 'challenge', 'lookup_kind', 'enum_value', 'Challenge', 'Challenge stage.', 'active'),
    ('lifecycle_stage', 'test', 'lookup_kind', 'enum_value', 'Test', 'Test stage.', 'active'),
    ('lifecycle_stage', 'adjudicate', 'lookup_kind', 'enum_value', 'Adjudicate', 'Adjudication stage.', 'active'),
    ('lifecycle_stage', 'legitimize', 'lookup_kind', 'enum_value', 'Legitimize', 'Legitimation stage.', 'active'),
    ('lifecycle_stage', 'execute', 'lookup_kind', 'enum_value', 'Execute', 'Execution stage.', 'active'),
    ('lifecycle_stage', 'record', 'lookup_kind', 'enum_value', 'Record', 'Record stage.', 'active'),
    ('lifecycle_stage', 'learn', 'lookup_kind', 'enum_value', 'Learn', 'Learning stage.', 'active'),
    ('lifecycle_stage', 'repair', 'lookup_kind', 'enum_value', 'Repair', 'Repair stage.', 'active'),
    ('lifecycle_stage', 'appeal', 'lookup_kind', 'enum_value', 'Appeal', 'Appeal stage.', 'active'),

    -- Stakeholder roles.
    ('stakeholder_role', 'decision_owner', 'lookup_kind', 'enum_value', 'Decision Owner', 'Actor accountable for the decision.', 'active'),
    ('stakeholder_role', 'policy_owner', 'lookup_kind', 'enum_value', 'Policy Owner', 'Actor accountable for policy basis.', 'active'),
    ('stakeholder_role', 'system_owner', 'lookup_kind', 'enum_value', 'System Owner', 'Actor accountable for the system.', 'active'),
    ('stakeholder_role', 'data_owner', 'lookup_kind', 'enum_value', 'Data Owner', 'Actor accountable for data access or use.', 'active'),
    ('stakeholder_role', 'affected_party', 'lookup_kind', 'enum_value', 'Affected Party', 'Party affected by the decision.', 'active'),
    ('stakeholder_role', 'affected_party_proxy', 'lookup_kind', 'enum_value', 'Affected Party Proxy', 'Proxy for an affected party.', 'active'),
    ('stakeholder_role', 'human_reviewer', 'lookup_kind', 'enum_value', 'Human Reviewer', 'Human reviewer for a decision.', 'active'),
    ('stakeholder_role', 'challenger', 'lookup_kind', 'enum_value', 'Challenger', 'Actor with challenge participation.', 'active'),
    ('stakeholder_role', 'adjudicator', 'lookup_kind', 'enum_value', 'Adjudicator', 'Actor responsible for adjudication.', 'active'),
    ('stakeholder_role', 'executor', 'lookup_kind', 'enum_value', 'Executor', 'Actor or system responsible for execution.', 'active'),
    ('stakeholder_role', 'witness', 'lookup_kind', 'enum_value', 'Witness', 'Actor who witnesses or records participation.', 'active'),
    ('stakeholder_role', 'observer', 'lookup_kind', 'enum_value', 'Observer', 'Non-blocking observer.', 'active'),
    ('stakeholder_role', 'safety_reviewer', 'lookup_kind', 'enum_value', 'Safety Reviewer', 'Safety reviewer stakeholder.', 'active'),
    ('stakeholder_role', 'privacy_reviewer', 'lookup_kind', 'enum_value', 'Privacy Reviewer', 'Privacy reviewer stakeholder.', 'active'),
    ('stakeholder_role', 'legal_reviewer', 'lookup_kind', 'enum_value', 'Legal Reviewer', 'Legal reviewer stakeholder.', 'active'),

    -- Participation and standing status.
    ('participation_status', 'identified', 'lookup_kind', 'enum_value', 'Identified', 'Stakeholder identified.', 'active'),
    ('participation_status', 'notified', 'lookup_kind', 'enum_value', 'Notified', 'Stakeholder notified.', 'active'),
    ('participation_status', 'acknowledged', 'lookup_kind', 'enum_value', 'Acknowledged', 'Stakeholder acknowledged notice.', 'active'),
    ('participation_status', 'responded', 'lookup_kind', 'enum_value', 'Responded', 'Stakeholder responded.', 'active'),
    ('participation_status', 'objected', 'lookup_kind', 'enum_value', 'Objected', 'Stakeholder objected.', 'active'),
    ('participation_status', 'clarification_requested', 'lookup_kind', 'enum_value', 'Clarification Requested', 'Stakeholder requested clarification.', 'active'),
    ('participation_status', 'recused', 'lookup_kind', 'enum_value', 'Recused', 'Stakeholder recused.', 'active'),
    ('participation_status', 'delegated', 'lookup_kind', 'enum_value', 'Delegated', 'Stakeholder delegated participation.', 'active'),
    ('participation_status', 'unreachable', 'lookup_kind', 'enum_value', 'Unreachable', 'Stakeholder could not be reached.', 'active'),
    ('participation_status', 'waived', 'lookup_kind', 'enum_value', 'Waived', 'Participation requirement waived.', 'active'),
    ('participation_status', 'closed', 'lookup_kind', 'enum_value', 'Closed', 'Stakeholder participation closed.', 'active'),

    ('standing_status', 'unreviewed', 'lookup_kind', 'enum_value', 'Unreviewed', 'Standing not yet reviewed.', 'active'),
    ('standing_status', 'valid', 'lookup_kind', 'enum_value', 'Valid', 'Standing validated.', 'active'),
    ('standing_status', 'contested', 'lookup_kind', 'enum_value', 'Contested', 'Standing contested.', 'active'),
    ('standing_status', 'recusal_active', 'lookup_kind', 'enum_value', 'Recusal Active', 'Recusal active.', 'active'),
    ('standing_status', 'blocked', 'lookup_kind', 'enum_value', 'Blocked', 'Standing blocked.', 'active'),
    ('standing_status', 'emergency', 'lookup_kind', 'enum_value', 'Emergency', 'Emergency standing path.', 'active'),

    -- Workflow definition and stages.
    ('workflow_definition_code', 'nemawashi_default_v1', 'lookup_kind', 'identifier', 'Nemawashi Default v1', 'Default Nemawashi workflow.', 'active'),
    ('workflow_definition_code', 'restricted_data_access_v1', 'lookup_kind', 'identifier', 'Restricted Data Access v1', 'Restricted data access workflow.', 'active'),

    ('workflow_stage_code', 'intake', 'lookup_kind', 'enum_value', 'Intake', 'Initial workflow intake.', 'active'),
    ('workflow_stage_code', 'classify_decision', 'lookup_kind', 'enum_value', 'Classify Decision', 'Classify the decision.', 'active'),
    ('workflow_stage_code', 'identify_stakeholders', 'lookup_kind', 'enum_value', 'Identify Stakeholders', 'Identify required stakeholders.', 'active'),
    ('workflow_stage_code', 'notify_stakeholders', 'lookup_kind', 'enum_value', 'Notify Stakeholders', 'Notify stakeholders.', 'active'),
    ('workflow_stage_code', 'collect_responses', 'lookup_kind', 'enum_value', 'Collect Responses', 'Collect stakeholder responses.', 'active'),
    ('workflow_stage_code', 'surface_dissent', 'lookup_kind', 'enum_value', 'Surface Dissent', 'Surface dissent and objections.', 'active'),
    ('workflow_stage_code', 'resolve_or_preserve_questions', 'lookup_kind', 'enum_value', 'Resolve Or Preserve Questions', 'Resolve or preserve unresolved questions.', 'active'),
    ('workflow_stage_code', 'sufficiency_check', 'lookup_kind', 'enum_value', 'Sufficiency Check', 'Check readiness for proposal admission.', 'active'),
    ('workflow_stage_code', 'ready_for_proposal', 'lookup_kind', 'enum_value', 'Ready For Proposal', 'Ready to advance to proposal.', 'active'),

    ('workflow_status', 'not_started', 'lookup_kind', 'enum_value', 'Not Started', 'Workflow not started.', 'active'),
    ('workflow_status', 'active', 'lookup_kind', 'enum_value', 'Active', 'Workflow active.', 'active'),
    ('workflow_status', 'waiting_on_stakeholder', 'lookup_kind', 'enum_value', 'Waiting On Stakeholder', 'Workflow waiting on stakeholder.', 'active'),
    ('workflow_status', 'waiting_on_rule_evaluation', 'lookup_kind', 'enum_value', 'Waiting On Rule Evaluation', 'Workflow waiting on rule evaluation.', 'active'),
    ('workflow_status', 'blocked', 'lookup_kind', 'enum_value', 'Blocked', 'Workflow blocked.', 'active'),
    ('workflow_status', 'ready_to_advance', 'lookup_kind', 'enum_value', 'Ready To Advance', 'Workflow ready to advance.', 'active'),
    ('workflow_status', 'advanced', 'lookup_kind', 'enum_value', 'Advanced', 'Workflow advanced.', 'active'),
    ('workflow_status', 'cancelled', 'lookup_kind', 'enum_value', 'Cancelled', 'Workflow cancelled.', 'active'),
    ('workflow_status', 'closed', 'lookup_kind', 'enum_value', 'Closed', 'Workflow closed.', 'active'),

    -- Task control.
    ('workflow_task_type', 'review_decision', 'lookup_kind', 'enum_value', 'Review Decision', 'Review a decision.', 'active'),
    ('workflow_task_type', 'provide_context', 'lookup_kind', 'enum_value', 'Provide Context', 'Provide context.', 'active'),
    ('workflow_task_type', 'raise_objection', 'lookup_kind', 'enum_value', 'Raise Objection', 'Raise an objection.', 'active'),
    ('workflow_task_type', 'clarify_boundary', 'lookup_kind', 'enum_value', 'Clarify Boundary', 'Clarify a boundary.', 'active'),
    ('workflow_task_type', 'confirm_standing', 'lookup_kind', 'enum_value', 'Confirm Standing', 'Confirm standing.', 'active'),
    ('workflow_task_type', 'approve_participation', 'lookup_kind', 'enum_value', 'Approve Participation', 'Approve participation.', 'active'),
    ('workflow_task_type', 'adjudicate_challenge', 'lookup_kind', 'enum_value', 'Adjudicate Challenge', 'Adjudicate a challenge.', 'active'),
    ('workflow_task_type', 'provide_evidence', 'lookup_kind', 'enum_value', 'Provide Evidence', 'Provide evidence.', 'active'),
    ('workflow_task_type', 'acknowledge_notice', 'lookup_kind', 'enum_value', 'Acknowledge Notice', 'Acknowledge notice.', 'active'),

    ('workflow_task_status', 'open', 'lookup_kind', 'enum_value', 'Open', 'Task open.', 'active'),
    ('workflow_task_status', 'in_progress', 'lookup_kind', 'enum_value', 'In Progress', 'Task in progress.', 'active'),
    ('workflow_task_status', 'completed', 'lookup_kind', 'enum_value', 'Completed', 'Task completed.', 'active'),
    ('workflow_task_status', 'cancelled', 'lookup_kind', 'enum_value', 'Cancelled', 'Task cancelled.', 'active'),
    ('workflow_task_status', 'expired', 'lookup_kind', 'enum_value', 'Expired', 'Task expired.', 'active'),
    ('workflow_task_status', 'blocked', 'lookup_kind', 'enum_value', 'Blocked', 'Task blocked.', 'active'),
    ('workflow_task_status', 'waived', 'lookup_kind', 'enum_value', 'Waived', 'Task waived.', 'active'),

    -- Rule sets, scopes, conditions, actions, and evaluation status.
    ('rule_set_code', 'nemawashi_default_rules_v1', 'lookup_kind', 'identifier', 'Nemawashi Default Rules v1', 'Default Nemawashi rule set.', 'active'),
    ('rule_set_code', 'restricted_data_access_rules_v1', 'lookup_kind', 'identifier', 'Restricted Data Access Rules v1', 'Restricted data access rule set.', 'active'),

    ('rule_scope', 'nemawashi', 'lookup_kind', 'enum_value', 'Nemawashi', 'Nemawashi rule scope.', 'active'),
    ('rule_scope', 'proposal_admission', 'lookup_kind', 'enum_value', 'Proposal Admission', 'Proposal admission rule scope.', 'active'),
    ('rule_scope', 'challenge', 'lookup_kind', 'enum_value', 'Challenge', 'Challenge rule scope.', 'active'),
    ('rule_scope', 'test', 'lookup_kind', 'enum_value', 'Test', 'Test rule scope.', 'active'),
    ('rule_scope', 'adjudication', 'lookup_kind', 'enum_value', 'Adjudication', 'Adjudication rule scope.', 'active'),
    ('rule_scope', 'legitimation', 'lookup_kind', 'enum_value', 'Legitimation', 'Legitimation rule scope.', 'active'),
    ('rule_scope', 'execution', 'lookup_kind', 'enum_value', 'Execution', 'Execution rule scope.', 'active'),
    ('rule_scope', 'repair', 'lookup_kind', 'enum_value', 'Repair', 'Repair rule scope.', 'active'),

    ('rule_condition_language', 'sql_predicate', 'lookup_kind', 'enum_value', 'SQL Predicate', 'Deterministic SQL predicate.', 'active'),
    ('rule_condition_language', 'json_logic', 'lookup_kind', 'enum_value', 'JSON Logic', 'JSON Logic expression.', 'active'),
    ('rule_condition_language', 'python_named_function', 'lookup_kind', 'enum_value', 'Python Named Function', 'Named deterministic function; not arbitrary user code.', 'active'),

    ('rule_action_type', 'create_stakeholder_link', 'lookup_kind', 'enum_value', 'Create Stakeholder Link', 'Create a decision stakeholder link.', 'active'),
    ('rule_action_type', 'create_workflow_task', 'lookup_kind', 'enum_value', 'Create Workflow Task', 'Create a workflow task.', 'active'),
    ('rule_action_type', 'send_notification', 'lookup_kind', 'enum_value', 'Send Notification', 'Send a notification.', 'active'),
    ('rule_action_type', 'open_communication_thread', 'lookup_kind', 'enum_value', 'Open Communication Thread', 'Open a governed communication thread.', 'active'),
    ('rule_action_type', 'raise_challenge', 'lookup_kind', 'enum_value', 'Raise Challenge', 'Create or propose a challenge.', 'active'),
    ('rule_action_type', 'require_test', 'lookup_kind', 'enum_value', 'Require Test', 'Require a test result.', 'active'),
    ('rule_action_type', 'block_transition', 'lookup_kind', 'enum_value', 'Block Transition', 'Block workflow transition.', 'active'),
    ('rule_action_type', 'allow_transition', 'lookup_kind', 'enum_value', 'Allow Transition', 'Allow workflow transition.', 'active'),
    ('rule_action_type', 'require_adjudication', 'lookup_kind', 'enum_value', 'Require Adjudication', 'Require adjudication.', 'active'),
    ('rule_action_type', 'require_repair', 'lookup_kind', 'enum_value', 'Require Repair', 'Require repair.', 'active'),
    ('rule_action_type', 'record_learning_artifact', 'lookup_kind', 'enum_value', 'Record Learning Artifact', 'Record a learning artifact.', 'active'),

    ('rule_evaluation_status', 'passed', 'lookup_kind', 'enum_value', 'Passed', 'Rule passed.', 'active'),
    ('rule_evaluation_status', 'matched', 'lookup_kind', 'enum_value', 'Matched', 'Rule matched.', 'active'),
    ('rule_evaluation_status', 'not_matched', 'lookup_kind', 'enum_value', 'Not Matched', 'Rule did not match.', 'active'),
    ('rule_evaluation_status', 'failed_to_evaluate', 'lookup_kind', 'enum_value', 'Failed To Evaluate', 'Rule could not be evaluated.', 'active'),
    ('rule_evaluation_status', 'warning', 'lookup_kind', 'enum_value', 'Warning', 'Rule warning.', 'active'),
    ('rule_evaluation_status', 'blocking', 'lookup_kind', 'enum_value', 'Blocking', 'Rule blocks transition.', 'active'),

    -- Communication.
    ('communication_thread_type', 'nemawashi_consultation', 'lookup_kind', 'enum_value', 'Nemawashi Consultation', 'Nemawashi consultation thread.', 'active'),
    ('communication_thread_type', 'clarification', 'lookup_kind', 'enum_value', 'Clarification', 'Clarification thread.', 'active'),
    ('communication_thread_type', 'challenge_discussion', 'lookup_kind', 'enum_value', 'Challenge Discussion', 'Challenge discussion thread.', 'active'),
    ('communication_thread_type', 'adjudication_discussion', 'lookup_kind', 'enum_value', 'Adjudication Discussion', 'Adjudication discussion thread.', 'active'),
    ('communication_thread_type', 'execution_review', 'lookup_kind', 'enum_value', 'Execution Review', 'Execution review thread.', 'active'),
    ('communication_thread_type', 'repair_discussion', 'lookup_kind', 'enum_value', 'Repair Discussion', 'Repair discussion thread.', 'active'),

    ('communication_thread_status', 'open', 'lookup_kind', 'enum_value', 'Open', 'Thread open.', 'active'),
    ('communication_thread_status', 'closed', 'lookup_kind', 'enum_value', 'Closed', 'Thread closed.', 'active'),
    ('communication_thread_status', 'archived', 'lookup_kind', 'enum_value', 'Archived', 'Thread archived.', 'active'),

    ('communication_message_type', 'comment', 'lookup_kind', 'enum_value', 'Comment', 'General comment.', 'active'),
    ('communication_message_type', 'objection', 'lookup_kind', 'enum_value', 'Objection', 'Objection that may produce a challenge record.', 'active'),
    ('communication_message_type', 'clarification_request', 'lookup_kind', 'enum_value', 'Clarification Request', 'Request for clarification.', 'active'),
    ('communication_message_type', 'clarification_response', 'lookup_kind', 'enum_value', 'Clarification Response', 'Response to clarification.', 'active'),
    ('communication_message_type', 'boundary_statement', 'lookup_kind', 'enum_value', 'Boundary Statement', 'Boundary statement.', 'active'),
    ('communication_message_type', 'evidence_pointer', 'lookup_kind', 'enum_value', 'Evidence Pointer', 'Pointer to evidence.', 'active'),
    ('communication_message_type', 'standing_statement', 'lookup_kind', 'enum_value', 'Standing Statement', 'Standing statement.', 'active'),
    ('communication_message_type', 'approval', 'lookup_kind', 'enum_value', 'Approval', 'Approval message.', 'active'),
    ('communication_message_type', 'recusal', 'lookup_kind', 'enum_value', 'Recusal', 'Recusal message.', 'active'),

    ('communication_message_status', 'posted', 'lookup_kind', 'enum_value', 'Posted', 'Message posted.', 'active'),
    ('communication_message_status', 'superseded', 'lookup_kind', 'enum_value', 'Superseded', 'Message superseded.', 'active'),
    ('communication_message_status', 'withdrawn', 'lookup_kind', 'enum_value', 'Withdrawn', 'Message withdrawn.', 'active'),

    ('notification_status', 'not_required', 'lookup_kind', 'enum_value', 'Not Required', 'Notification not required.', 'active'),
    ('notification_status', 'pending', 'lookup_kind', 'enum_value', 'Pending', 'Notification pending.', 'active'),
    ('notification_status', 'sent', 'lookup_kind', 'enum_value', 'Sent', 'Notification sent.', 'active'),
    ('notification_status', 'acknowledged', 'lookup_kind', 'enum_value', 'Acknowledged', 'Notification acknowledged.', 'active'),
    ('notification_status', 'failed', 'lookup_kind', 'enum_value', 'Failed', 'Notification failed.', 'active')
ON CONFLICT (registry_name, identifier_id)
DO UPDATE SET
    identifier_type_registry_name = EXCLUDED.identifier_type_registry_name,
    identifier_type_id = EXCLUDED.identifier_type_id,
    display_label = EXCLUDED.display_label,
    description = EXCLUDED.description,
    status = EXCLUDED.status,
    updated_at = now();

-- -----------------------------------------------------------------------------
-- cdp_core.decision_stakeholder
-- -----------------------------------------------------------------------------
-- Decision-specific stakeholder map. Identity lives in identifier_registry;
-- participation relationship lives here.

CREATE TABLE IF NOT EXISTS cdp_core.decision_stakeholder (
    stakeholder_link_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    registry_name TEXT NOT NULL,
    decision_id TEXT NOT NULL,

    stakeholder_actor_registry_name TEXT NOT NULL DEFAULT 'actor',
    stakeholder_actor_id TEXT NOT NULL,

    stakeholder_role_registry_name TEXT NOT NULL DEFAULT 'stakeholder_role',
    stakeholder_role TEXT NOT NULL,

    standing_basis TEXT,
    standing_status_registry_name TEXT NOT NULL DEFAULT 'standing_status',
    standing_status TEXT NOT NULL DEFAULT 'unreviewed',

    participation_required BOOLEAN NOT NULL DEFAULT false,
    notification_required BOOLEAN NOT NULL DEFAULT true,
    response_required BOOLEAN NOT NULL DEFAULT false,
    response_due_at TIMESTAMPTZ,

    participation_status_registry_name TEXT NOT NULL DEFAULT 'participation_status',
    participation_status TEXT NOT NULL DEFAULT 'identified',

    source_ref TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_decision_stakeholder_actor_registry
        CHECK (stakeholder_actor_registry_name = 'actor'),

    CONSTRAINT chk_decision_stakeholder_role_registry
        CHECK (stakeholder_role_registry_name = 'stakeholder_role'),

    CONSTRAINT chk_decision_stakeholder_standing_registry
        CHECK (standing_status_registry_name = 'standing_status'),

    CONSTRAINT chk_decision_stakeholder_participation_registry
        CHECK (participation_status_registry_name = 'participation_status'),

    CONSTRAINT chk_decision_stakeholder_registry_name_format
        CHECK (registry_name ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_decision_stakeholder_decision_id_format
        CHECK (decision_id ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_decision_stakeholder_response_due_required
        CHECK (response_due_at IS NULL OR response_required),

    CONSTRAINT uq_decision_stakeholder_identity
        UNIQUE (registry_name, decision_id, stakeholder_actor_id, stakeholder_role),

    CONSTRAINT fk_decision_stakeholder_decision
        FOREIGN KEY (registry_name, decision_id)
        REFERENCES cdp_core.decision_registry (registry_name, decision_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_decision_stakeholder_actor
        FOREIGN KEY (stakeholder_actor_registry_name, stakeholder_actor_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_decision_stakeholder_role
        FOREIGN KEY (stakeholder_role_registry_name, stakeholder_role)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_decision_stakeholder_standing_status
        FOREIGN KEY (standing_status_registry_name, standing_status)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_decision_stakeholder_participation_status
        FOREIGN KEY (participation_status_registry_name, participation_status)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.decision_stakeholder IS
'Decision-specific stakeholder map for Nemawashi, standing, notification, and participation tracking.';

CREATE INDEX IF NOT EXISTS idx_nemawashi_stakeholder_decision
    ON cdp_core.decision_stakeholder (registry_name, decision_id);

CREATE INDEX IF NOT EXISTS idx_nemawashi_stakeholder_actor
    ON cdp_core.decision_stakeholder (stakeholder_actor_id);

CREATE INDEX IF NOT EXISTS idx_nemawashi_stakeholder_role
    ON cdp_core.decision_stakeholder (stakeholder_role, participation_status);

CREATE INDEX IF NOT EXISTS idx_nemawashi_stakeholder_required
    ON cdp_core.decision_stakeholder (registry_name, participation_required, response_required, participation_status);

-- -----------------------------------------------------------------------------
-- cdp_core.rule_set and cdp_core.rule_definition
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cdp_core.rule_set (
    rule_set_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    rule_set_code_registry_name TEXT NOT NULL DEFAULT 'rule_set_code',
    rule_set_code TEXT NOT NULL,
    rule_set_version TEXT NOT NULL,
    display_name TEXT NOT NULL,

    scope_registry_name TEXT NOT NULL DEFAULT 'rule_scope',
    scope TEXT NOT NULL,

    status TEXT NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_rule_set_code_registry
        CHECK (rule_set_code_registry_name = 'rule_set_code'),

    CONSTRAINT chk_rule_set_scope_registry
        CHECK (scope_registry_name = 'rule_scope'),

    CONSTRAINT chk_rule_set_version_not_blank
        CHECK (btrim(rule_set_version) <> ''),

    CONSTRAINT chk_rule_set_display_name_not_blank
        CHECK (btrim(display_name) <> ''),

    CONSTRAINT chk_rule_set_status
        CHECK (status IN ('active', 'deprecated', 'inactive', 'retired')),

    CONSTRAINT uq_rule_set_identity
        UNIQUE (rule_set_code, rule_set_version),

    CONSTRAINT fk_rule_set_code
        FOREIGN KEY (rule_set_code_registry_name, rule_set_code)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_rule_set_scope
        FOREIGN KEY (scope_registry_name, scope)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.rule_set IS
'Governed, versioned rule set. Not config_lookup.';

CREATE TABLE IF NOT EXISTS cdp_core.rule_definition (
    rule_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    rule_set_id UUID NOT NULL,
    rule_code TEXT NOT NULL,
    rule_version TEXT NOT NULL,
    description TEXT NOT NULL,

    condition_language_registry_name TEXT NOT NULL DEFAULT 'rule_condition_language',
    condition_language TEXT NOT NULL,
    condition_expression TEXT NOT NULL,

    action_type_registry_name TEXT NOT NULL DEFAULT 'rule_action_type',
    action_type TEXT NOT NULL,
    action_payload JSONB NOT NULL DEFAULT '{}'::jsonb,

    severity TEXT NOT NULL DEFAULT 'info',
    blocking BOOLEAN NOT NULL DEFAULT false,
    status TEXT NOT NULL DEFAULT 'active',

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_rule_definition_code_format
        CHECK (rule_code ~ '^[A-Za-z0-9_-]+$'),

    CONSTRAINT chk_rule_definition_version_not_blank
        CHECK (btrim(rule_version) <> ''),

    CONSTRAINT chk_rule_definition_description_not_blank
        CHECK (btrim(description) <> ''),

    CONSTRAINT chk_rule_definition_condition_language_registry
        CHECK (condition_language_registry_name = 'rule_condition_language'),

    CONSTRAINT chk_rule_definition_action_type_registry
        CHECK (action_type_registry_name = 'rule_action_type'),

    CONSTRAINT chk_rule_definition_condition_expression_not_blank
        CHECK (btrim(condition_expression) <> ''),

    CONSTRAINT chk_rule_definition_severity
        CHECK (severity IN ('info', 'warning', 'blocking')),

    CONSTRAINT chk_rule_definition_status
        CHECK (status IN ('active', 'deprecated', 'inactive', 'retired')),

    CONSTRAINT uq_rule_definition_identity
        UNIQUE (rule_set_id, rule_code, rule_version),

    CONSTRAINT fk_rule_definition_set
        FOREIGN KEY (rule_set_id)
        REFERENCES cdp_core.rule_set (rule_set_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_rule_definition_condition_language
        FOREIGN KEY (condition_language_registry_name, condition_language)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_rule_definition_action_type
        FOREIGN KEY (action_type_registry_name, action_type)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.rule_definition IS
'Governed rule definitions that create work, findings, blockers, or transition permissions. Rules do not silently mutate decisions.';

CREATE INDEX IF NOT EXISTS idx_rule_definition_set_status
    ON cdp_core.rule_definition (rule_set_id, status);

CREATE INDEX IF NOT EXISTS idx_rule_definition_action
    ON cdp_core.rule_definition (action_type, blocking);

-- -----------------------------------------------------------------------------
-- cdp_core.workflow_definition, stage, and instance
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cdp_core.workflow_definition (
    workflow_definition_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    workflow_code_registry_name TEXT NOT NULL DEFAULT 'workflow_definition_code',
    workflow_code TEXT NOT NULL,
    workflow_version TEXT NOT NULL,
    display_name TEXT NOT NULL,

    applies_to_registry_name TEXT,
    applies_to_decision_class_id TEXT,

    status TEXT NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_workflow_definition_code_registry
        CHECK (workflow_code_registry_name = 'workflow_definition_code'),

    CONSTRAINT chk_workflow_definition_version_not_blank
        CHECK (btrim(workflow_version) <> ''),

    CONSTRAINT chk_workflow_definition_display_name_not_blank
        CHECK (btrim(display_name) <> ''),

    CONSTRAINT chk_workflow_definition_applies_pairing
        CHECK (
            (applies_to_registry_name IS NULL AND applies_to_decision_class_id IS NULL)
            OR
            (applies_to_registry_name IS NOT NULL AND applies_to_decision_class_id IS NOT NULL)
        ),

    CONSTRAINT chk_workflow_definition_status
        CHECK (status IN ('active', 'deprecated', 'inactive', 'retired')),

    CONSTRAINT uq_workflow_definition_identity
        UNIQUE (workflow_code, workflow_version),

    CONSTRAINT fk_workflow_definition_code
        FOREIGN KEY (workflow_code_registry_name, workflow_code)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_workflow_definition_decision_class
        FOREIGN KEY (applies_to_registry_name, applies_to_decision_class_id)
        REFERENCES cdp_core.decision_class_registry (registry_name, class_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.workflow_definition IS
'Versioned workflow definition. Workflow manages state; it does not adjudicate substance.';

CREATE TABLE IF NOT EXISTS cdp_core.workflow_stage (
    workflow_stage_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    workflow_definition_id UUID NOT NULL,
    stage_code_registry_name TEXT NOT NULL DEFAULT 'workflow_stage_code',
    stage_code TEXT NOT NULL,
    stage_order INTEGER NOT NULL,

    lifecycle_stage_registry_name TEXT NOT NULL DEFAULT 'lifecycle_stage',
    lifecycle_stage TEXT NOT NULL,

    entry_criteria_ref TEXT,
    exit_criteria_ref TEXT,
    status TEXT NOT NULL DEFAULT 'active',

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_workflow_stage_code_registry
        CHECK (stage_code_registry_name = 'workflow_stage_code'),

    CONSTRAINT chk_workflow_stage_lifecycle_registry
        CHECK (lifecycle_stage_registry_name = 'lifecycle_stage'),

    CONSTRAINT chk_workflow_stage_order_positive
        CHECK (stage_order > 0),

    CONSTRAINT chk_workflow_stage_status
        CHECK (status IN ('active', 'deprecated', 'inactive', 'retired')),

    CONSTRAINT uq_workflow_stage_code
        UNIQUE (workflow_definition_id, stage_code),

    CONSTRAINT uq_workflow_stage_order
        UNIQUE (workflow_definition_id, stage_order),

    CONSTRAINT fk_workflow_stage_definition
        FOREIGN KEY (workflow_definition_id)
        REFERENCES cdp_core.workflow_definition (workflow_definition_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_workflow_stage_code
        FOREIGN KEY (stage_code_registry_name, stage_code)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_workflow_stage_lifecycle
        FOREIGN KEY (lifecycle_stage_registry_name, lifecycle_stage)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.workflow_stage IS
'Ordered workflow stages aligned to CDP lifecycle stages.';

CREATE TABLE IF NOT EXISTS cdp_core.workflow_instance (
    workflow_instance_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    registry_name TEXT NOT NULL,
    decision_id TEXT NOT NULL,
    workflow_definition_id UUID NOT NULL,
    current_stage_id UUID,

    lifecycle_stage_registry_name TEXT NOT NULL DEFAULT 'lifecycle_stage',
    lifecycle_stage TEXT NOT NULL DEFAULT 'nemawashi',

    workflow_status_registry_name TEXT NOT NULL DEFAULT 'workflow_status',
    workflow_status TEXT NOT NULL DEFAULT 'active',

    blocked BOOLEAN NOT NULL DEFAULT false,
    blocked_reason TEXT,

    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    closed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_workflow_instance_lifecycle_registry
        CHECK (lifecycle_stage_registry_name = 'lifecycle_stage'),

    CONSTRAINT chk_workflow_instance_status_registry
        CHECK (workflow_status_registry_name = 'workflow_status'),

    CONSTRAINT chk_workflow_instance_blocked_reason
        CHECK ((blocked AND blocked_reason IS NOT NULL) OR (NOT blocked)),

    CONSTRAINT chk_workflow_instance_closed_status
        CHECK (closed_at IS NULL OR workflow_status IN ('closed', 'cancelled', 'advanced')),

    CONSTRAINT uq_workflow_instance_decision_definition
        UNIQUE (registry_name, decision_id, workflow_definition_id),

    CONSTRAINT fk_workflow_instance_decision
        FOREIGN KEY (registry_name, decision_id)
        REFERENCES cdp_core.decision_registry (registry_name, decision_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_workflow_instance_definition
        FOREIGN KEY (workflow_definition_id)
        REFERENCES cdp_core.workflow_definition (workflow_definition_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_workflow_instance_current_stage
        FOREIGN KEY (current_stage_id)
        REFERENCES cdp_core.workflow_stage (workflow_stage_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_workflow_instance_lifecycle
        FOREIGN KEY (lifecycle_stage_registry_name, lifecycle_stage)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_workflow_instance_status
        FOREIGN KEY (workflow_status_registry_name, workflow_status)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.workflow_instance IS
'Decision-specific workflow state, blockers, and transition readiness.';

CREATE INDEX IF NOT EXISTS idx_workflow_instance_decision
    ON cdp_core.workflow_instance (registry_name, decision_id);

CREATE INDEX IF NOT EXISTS idx_workflow_instance_status
    ON cdp_core.workflow_instance (workflow_status, blocked);

-- -----------------------------------------------------------------------------
-- cdp_core.workflow_task
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cdp_core.workflow_task (
    task_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    workflow_instance_id UUID NOT NULL,
    registry_name TEXT NOT NULL,
    decision_id TEXT NOT NULL,

    assigned_actor_registry_name TEXT NOT NULL DEFAULT 'actor',
    assigned_actor_id TEXT,

    assigned_role_registry_name TEXT NOT NULL DEFAULT 'stakeholder_role',
    assigned_role TEXT NOT NULL,

    task_type_registry_name TEXT NOT NULL DEFAULT 'workflow_task_type',
    task_type TEXT NOT NULL,

    task_status_registry_name TEXT NOT NULL DEFAULT 'workflow_task_status',
    task_status TEXT NOT NULL DEFAULT 'open',

    due_at TIMESTAMPTZ,
    blocking BOOLEAN NOT NULL DEFAULT false,
    created_by_rule_id UUID,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at TIMESTAMPTZ,

    CONSTRAINT chk_workflow_task_actor_registry
        CHECK (assigned_actor_registry_name = 'actor'),

    CONSTRAINT chk_workflow_task_role_registry
        CHECK (assigned_role_registry_name = 'stakeholder_role'),

    CONSTRAINT chk_workflow_task_type_registry
        CHECK (task_type_registry_name = 'workflow_task_type'),

    CONSTRAINT chk_workflow_task_status_registry
        CHECK (task_status_registry_name = 'workflow_task_status'),

    CONSTRAINT chk_workflow_task_completed_status
        CHECK (completed_at IS NULL OR task_status IN ('completed', 'cancelled', 'waived')),

    CONSTRAINT fk_workflow_task_instance
        FOREIGN KEY (workflow_instance_id)
        REFERENCES cdp_core.workflow_instance (workflow_instance_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_workflow_task_decision
        FOREIGN KEY (registry_name, decision_id)
        REFERENCES cdp_core.decision_registry (registry_name, decision_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_workflow_task_assigned_actor
        FOREIGN KEY (assigned_actor_registry_name, assigned_actor_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_workflow_task_assigned_role
        FOREIGN KEY (assigned_role_registry_name, assigned_role)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_workflow_task_type
        FOREIGN KEY (task_type_registry_name, task_type)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_workflow_task_status
        FOREIGN KEY (task_status_registry_name, task_status)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_workflow_task_created_by_rule
        FOREIGN KEY (created_by_rule_id)
        REFERENCES cdp_core.rule_definition (rule_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.workflow_task IS
'Governed workflow work item. Tasks may block transitions but do not adjudicate substance.';

CREATE INDEX IF NOT EXISTS idx_workflow_task_queue
    ON cdp_core.workflow_task (task_status, blocking, due_at);

CREATE INDEX IF NOT EXISTS idx_workflow_task_decision
    ON cdp_core.workflow_task (registry_name, decision_id);

CREATE INDEX IF NOT EXISTS idx_workflow_task_assignee
    ON cdp_core.workflow_task (assigned_actor_id, assigned_role, task_status);

-- -----------------------------------------------------------------------------
-- cdp_core.rule_evaluation_result
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cdp_core.rule_evaluation_result (
    rule_evaluation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    rule_id UUID NOT NULL,
    workflow_instance_id UUID,
    registry_name TEXT NOT NULL,
    decision_id TEXT NOT NULL,

    evaluation_status_registry_name TEXT NOT NULL DEFAULT 'rule_evaluation_status',
    evaluation_status TEXT NOT NULL,

    matched BOOLEAN NOT NULL DEFAULT false,
    action_taken TEXT,
    finding_text TEXT,

    created_task_id UUID,
    created_stakeholder_link_id UUID,
    created_challenge_id TEXT,
    blocked_transition BOOLEAN NOT NULL DEFAULT false,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_rule_evaluation_status_registry
        CHECK (evaluation_status_registry_name = 'rule_evaluation_status'),

    CONSTRAINT chk_rule_evaluation_finding_required_for_block
        CHECK ((NOT blocked_transition) OR finding_text IS NOT NULL),

    CONSTRAINT fk_rule_evaluation_rule
        FOREIGN KEY (rule_id)
        REFERENCES cdp_core.rule_definition (rule_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_rule_evaluation_workflow
        FOREIGN KEY (workflow_instance_id)
        REFERENCES cdp_core.workflow_instance (workflow_instance_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_rule_evaluation_decision
        FOREIGN KEY (registry_name, decision_id)
        REFERENCES cdp_core.decision_registry (registry_name, decision_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_rule_evaluation_status
        FOREIGN KEY (evaluation_status_registry_name, evaluation_status)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_rule_evaluation_created_task
        FOREIGN KEY (created_task_id)
        REFERENCES cdp_core.workflow_task (task_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_rule_evaluation_created_stakeholder
        FOREIGN KEY (created_stakeholder_link_id)
        REFERENCES cdp_core.decision_stakeholder (stakeholder_link_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.rule_evaluation_result IS
'Auditable result of governed rule evaluation. Results may create tasks, stakeholder links, findings, blockers, or transition permissions.';

CREATE INDEX IF NOT EXISTS idx_rule_evaluation_decision
    ON cdp_core.rule_evaluation_result (registry_name, decision_id);

CREATE INDEX IF NOT EXISTS idx_rule_evaluation_status
    ON cdp_core.rule_evaluation_result (evaluation_status, blocked_transition);

-- -----------------------------------------------------------------------------
-- cdp_core.communication_thread, participant, and message
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS cdp_core.communication_thread (
    thread_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    registry_name TEXT NOT NULL,
    decision_id TEXT NOT NULL,
    workflow_instance_id UUID,

    thread_type_registry_name TEXT NOT NULL DEFAULT 'communication_thread_type',
    thread_type TEXT NOT NULL,

    thread_status_registry_name TEXT NOT NULL DEFAULT 'communication_thread_status',
    thread_status TEXT NOT NULL DEFAULT 'open',

    created_by_actor_registry_name TEXT NOT NULL DEFAULT 'actor',
    created_by_actor_id TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    closed_at TIMESTAMPTZ,

    CONSTRAINT chk_communication_thread_type_registry
        CHECK (thread_type_registry_name = 'communication_thread_type'),

    CONSTRAINT chk_communication_thread_status_registry
        CHECK (thread_status_registry_name = 'communication_thread_status'),

    CONSTRAINT chk_communication_thread_actor_registry
        CHECK (created_by_actor_registry_name = 'actor'),

    CONSTRAINT chk_communication_thread_closed_status
        CHECK (closed_at IS NULL OR thread_status IN ('closed', 'archived')),

    CONSTRAINT fk_communication_thread_decision
        FOREIGN KEY (registry_name, decision_id)
        REFERENCES cdp_core.decision_registry (registry_name, decision_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_communication_thread_workflow
        FOREIGN KEY (workflow_instance_id)
        REFERENCES cdp_core.workflow_instance (workflow_instance_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_communication_thread_type
        FOREIGN KEY (thread_type_registry_name, thread_type)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_communication_thread_status
        FOREIGN KEY (thread_status_registry_name, thread_status)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_communication_thread_created_by
        FOREIGN KEY (created_by_actor_registry_name, created_by_actor_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.communication_thread IS
'Governed decision-specific communication thread. Not a general chat room.';

CREATE INDEX IF NOT EXISTS idx_communication_thread_decision
    ON cdp_core.communication_thread (registry_name, decision_id);

CREATE INDEX IF NOT EXISTS idx_communication_thread_status
    ON cdp_core.communication_thread (thread_type, thread_status);

CREATE TABLE IF NOT EXISTS cdp_core.communication_participant (
    participant_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    thread_id UUID NOT NULL,
    actor_registry_name TEXT NOT NULL DEFAULT 'actor',
    actor_id TEXT NOT NULL,

    participant_role_registry_name TEXT NOT NULL DEFAULT 'stakeholder_role',
    participant_role TEXT NOT NULL,

    notification_status_registry_name TEXT NOT NULL DEFAULT 'notification_status',
    notification_status TEXT NOT NULL DEFAULT 'pending',
    last_seen_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_communication_participant_actor_registry
        CHECK (actor_registry_name = 'actor'),

    CONSTRAINT chk_communication_participant_role_registry
        CHECK (participant_role_registry_name = 'stakeholder_role'),

    CONSTRAINT chk_communication_participant_notification_registry
        CHECK (notification_status_registry_name = 'notification_status'),

    CONSTRAINT uq_communication_participant_identity
        UNIQUE (thread_id, actor_id, participant_role),

    CONSTRAINT fk_communication_participant_thread
        FOREIGN KEY (thread_id)
        REFERENCES cdp_core.communication_thread (thread_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_communication_participant_actor
        FOREIGN KEY (actor_registry_name, actor_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_communication_participant_role
        FOREIGN KEY (participant_role_registry_name, participant_role)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_communication_participant_notification_status
        FOREIGN KEY (notification_status_registry_name, notification_status)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.communication_participant IS
'Participants in governed decision communication threads.';

CREATE INDEX IF NOT EXISTS idx_communication_participant_actor
    ON cdp_core.communication_participant (actor_id, notification_status);

CREATE TABLE IF NOT EXISTS cdp_core.communication_message (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    thread_id UUID NOT NULL,
    actor_registry_name TEXT NOT NULL DEFAULT 'actor',
    actor_id TEXT NOT NULL,

    message_type_registry_name TEXT NOT NULL DEFAULT 'communication_message_type',
    message_type TEXT NOT NULL,
    message_body TEXT NOT NULL,

    message_status_registry_name TEXT NOT NULL DEFAULT 'communication_message_status',
    message_status TEXT NOT NULL DEFAULT 'posted',

    governed_record_ref TEXT,
    created_task_id UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_communication_message_actor_registry
        CHECK (actor_registry_name = 'actor'),

    CONSTRAINT chk_communication_message_type_registry
        CHECK (message_type_registry_name = 'communication_message_type'),

    CONSTRAINT chk_communication_message_status_registry
        CHECK (message_status_registry_name = 'communication_message_status'),

    CONSTRAINT chk_communication_message_body_not_blank
        CHECK (btrim(message_body) <> ''),

    CONSTRAINT fk_communication_message_thread
        FOREIGN KEY (thread_id)
        REFERENCES cdp_core.communication_thread (thread_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_communication_message_actor
        FOREIGN KEY (actor_registry_name, actor_id)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_communication_message_type
        FOREIGN KEY (message_type_registry_name, message_type)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_communication_message_status
        FOREIGN KEY (message_status_registry_name, message_status)
        REFERENCES cdp_core.identifier_registry (registry_name, identifier_id)
        DEFERRABLE INITIALLY DEFERRED,

    CONSTRAINT fk_communication_message_created_task
        FOREIGN KEY (created_task_id)
        REFERENCES cdp_core.workflow_task (task_id)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON TABLE cdp_core.communication_message IS
'Governed message in a decision-specific communication thread. Some message types may later produce governed records.';

CREATE INDEX IF NOT EXISTS idx_communication_message_thread
    ON cdp_core.communication_message (thread_id, created_at);

CREATE INDEX IF NOT EXISTS idx_communication_message_type
    ON cdp_core.communication_message (message_type, message_status);

-- -----------------------------------------------------------------------------
-- Seed minimal workflow and rule bones.
-- -----------------------------------------------------------------------------

INSERT INTO cdp_core.workflow_definition (
    workflow_code, workflow_version, display_name, status
)
VALUES
    ('nemawashi_default_v1', 'v1', 'Nemawashi Default Workflow v1', 'active'),
    ('restricted_data_access_v1', 'v1', 'Restricted Data Access Workflow v1', 'active')
ON CONFLICT (workflow_code, workflow_version)
DO UPDATE SET
    display_name = EXCLUDED.display_name,
    status = EXCLUDED.status,
    updated_at = now();

INSERT INTO cdp_core.workflow_stage (
    workflow_definition_id, stage_code, stage_order, lifecycle_stage, status
)
SELECT
    wd.workflow_definition_id,
    v.stage_code,
    v.stage_order,
    'nemawashi',
    'active'
FROM cdp_core.workflow_definition wd
CROSS JOIN (
    VALUES
        ('intake', 1),
        ('classify_decision', 2),
        ('identify_stakeholders', 3),
        ('notify_stakeholders', 4),
        ('collect_responses', 5),
        ('surface_dissent', 6),
        ('resolve_or_preserve_questions', 7),
        ('sufficiency_check', 8),
        ('ready_for_proposal', 9)
) AS v(stage_code, stage_order)
WHERE wd.workflow_code IN ('nemawashi_default_v1', 'restricted_data_access_v1')
  AND wd.workflow_version = 'v1'
ON CONFLICT (workflow_definition_id, stage_code)
DO UPDATE SET
    stage_order = EXCLUDED.stage_order,
    lifecycle_stage = EXCLUDED.lifecycle_stage,
    status = EXCLUDED.status,
    updated_at = now();

INSERT INTO cdp_core.rule_set (
    rule_set_code, rule_set_version, display_name, scope, status
)
VALUES
    ('nemawashi_default_rules_v1', 'v1', 'Nemawashi Default Rules v1', 'nemawashi', 'active'),
    ('restricted_data_access_rules_v1', 'v1', 'Restricted Data Access Rules v1', 'nemawashi', 'active')
ON CONFLICT (rule_set_code, rule_set_version)
DO UPDATE SET
    display_name = EXCLUDED.display_name,
    scope = EXCLUDED.scope,
    status = EXCLUDED.status,
    updated_at = now();

INSERT INTO cdp_core.rule_definition (
    rule_set_id,
    rule_code,
    rule_version,
    description,
    condition_language,
    condition_expression,
    action_type,
    action_payload,
    severity,
    blocking,
    status
)
SELECT
    rs.rule_set_id,
    v.rule_code,
    'v1',
    v.description,
    v.condition_language,
    v.condition_expression,
    v.action_type,
    v.action_payload::jsonb,
    v.severity,
    v.blocking,
    'active'
FROM cdp_core.rule_set rs
JOIN (
    VALUES
        (
            'restricted_dataset_requires_data_owner',
            'Restricted-data decisions require a data owner stakeholder.',
            'sql_predicate',
            'object_type = ''restricted_dataset'' OR decision_class_id LIKE ''%access%''',
            'create_stakeholder_link',
            '{"stakeholder_role":"data_owner","participation_required":true,"response_required":true}',
            'blocking',
            true
        ),
        (
            'workflow_configuration_requires_system_owner',
            'Workflow-configuration permission sources require a system owner stakeholder.',
            'sql_predicate',
            'permission_source_type = ''workflow_configuration''',
            'create_stakeholder_link',
            '{"stakeholder_role":"system_owner","participation_required":true,"response_required":true}',
            'warning',
            false
        ),
        (
            'human_required_creates_reviewer_task',
            'Human-required decisions create a human reviewer task.',
            'sql_predicate',
            'human_required = true',
            'create_workflow_task',
            '{"task_type":"review_decision","assigned_role":"human_reviewer","blocking":true}',
            'blocking',
            true
        ),
        (
            'access_escalation_opens_consultation_thread',
            'Access escalation decisions open a Nemawashi consultation thread.',
            'sql_predicate',
            'decision_class_id LIKE ''%access%''',
            'open_communication_thread',
            '{"thread_type":"nemawashi_consultation"}',
            'info',
            false
        ),
        (
            'missing_required_stakeholder_blocks_admission',
            'Missing required stakeholders block proposal admission.',
            'python_named_function',
            'missing_required_stakeholder_for_decision',
            'block_transition',
            '{"blocked_stage":"proposal_admission"}',
            'blocking',
            true
        )
) AS v(rule_code, description, condition_language, condition_expression, action_type, action_payload, severity, blocking)
  ON rs.rule_set_code = 'restricted_data_access_rules_v1'
 AND rs.rule_set_version = 'v1'
ON CONFLICT (rule_set_id, rule_code, rule_version)
DO UPDATE SET
    description = EXCLUDED.description,
    condition_language = EXCLUDED.condition_language,
    condition_expression = EXCLUDED.condition_expression,
    action_type = EXCLUDED.action_type,
    action_payload = EXCLUDED.action_payload,
    severity = EXCLUDED.severity,
    blocking = EXCLUDED.blocking,
    status = EXCLUDED.status,
    updated_at = now();

-- -----------------------------------------------------------------------------
-- Projections for app/Superset/demo surfaces.
-- -----------------------------------------------------------------------------

CREATE OR REPLACE VIEW cdp_projection.nemawashi_stakeholder_map_flat AS
SELECT
    ds.stakeholder_link_id,
    ds.registry_name,
    ds.decision_id,
    'decision_register:' || ds.registry_name || ':' || ds.decision_id AS decision_domain,
    ds.stakeholder_actor_id,
    actor.display_label AS stakeholder_actor_label,
    actor.identifier_type_id AS stakeholder_actor_type,
    ds.stakeholder_role,
    role.display_label AS stakeholder_role_label,
    ds.standing_basis,
    ds.standing_status,
    ds.participation_required,
    ds.notification_required,
    ds.response_required,
    ds.response_due_at,
    ds.participation_status,
    ds.source_ref,
    ds.created_at,
    ds.updated_at
FROM cdp_core.decision_stakeholder ds
LEFT JOIN cdp_core.identifier_registry actor
  ON actor.registry_name = 'actor'
 AND actor.identifier_id = ds.stakeholder_actor_id
LEFT JOIN cdp_core.identifier_registry role
  ON role.registry_name = 'stakeholder_role'
 AND role.identifier_id = ds.stakeholder_role;

COMMENT ON VIEW cdp_projection.nemawashi_stakeholder_map_flat IS
'Flat stakeholder map for Nemawashi review, Superset, and review packets.';

CREATE OR REPLACE VIEW cdp_projection.workflow_task_queue AS
SELECT
    wt.task_id,
    wt.workflow_instance_id,
    wi.workflow_definition_id,
    wd.workflow_code,
    wd.workflow_version,
    wt.registry_name,
    wt.decision_id,
    'decision_register:' || wt.registry_name || ':' || wt.decision_id AS decision_domain,
    wi.lifecycle_stage,
    wi.workflow_status,
    wi.blocked AS workflow_blocked,
    wi.blocked_reason,
    wt.assigned_actor_id,
    actor.display_label AS assigned_actor_label,
    wt.assigned_role,
    wt.task_type,
    wt.task_status,
    wt.due_at,
    wt.blocking,
    wt.created_by_rule_id,
    wt.created_at,
    wt.updated_at,
    wt.completed_at
FROM cdp_core.workflow_task wt
JOIN cdp_core.workflow_instance wi
  ON wi.workflow_instance_id = wt.workflow_instance_id
JOIN cdp_core.workflow_definition wd
  ON wd.workflow_definition_id = wi.workflow_definition_id
LEFT JOIN cdp_core.identifier_registry actor
  ON actor.registry_name = 'actor'
 AND actor.identifier_id = wt.assigned_actor_id;

COMMENT ON VIEW cdp_projection.workflow_task_queue IS
'Task queue projection for open, blocking, assigned, and completed workflow work.';

CREATE OR REPLACE VIEW cdp_projection.nemawashi_blockers AS
SELECT
    'workflow_instance_blocked' AS blocker_type,
    wi.registry_name,
    wi.decision_id,
    wi.workflow_instance_id,
    NULL::UUID AS task_id,
    NULL::UUID AS stakeholder_link_id,
    NULL::UUID AS rule_evaluation_id,
    'blocking' AS severity,
    wi.blocked_reason AS blocker_text,
    wi.updated_at AS observed_at
FROM cdp_core.workflow_instance wi
WHERE wi.blocked

UNION ALL

SELECT
    'blocking_task' AS blocker_type,
    wt.registry_name,
    wt.decision_id,
    wt.workflow_instance_id,
    wt.task_id,
    NULL::UUID AS stakeholder_link_id,
    NULL::UUID AS rule_evaluation_id,
    'blocking' AS severity,
    'Blocking task is not complete: ' || wt.task_type AS blocker_text,
    wt.updated_at AS observed_at
FROM cdp_core.workflow_task wt
WHERE wt.blocking
  AND wt.task_status NOT IN ('completed', 'cancelled', 'waived')

UNION ALL

SELECT
    'required_stakeholder_response' AS blocker_type,
    ds.registry_name,
    ds.decision_id,
    NULL::UUID AS workflow_instance_id,
    NULL::UUID AS task_id,
    ds.stakeholder_link_id,
    NULL::UUID AS rule_evaluation_id,
    'blocking' AS severity,
    'Required stakeholder response is not complete: ' || ds.stakeholder_role || ' / ' || ds.stakeholder_actor_id AS blocker_text,
    ds.updated_at AS observed_at
FROM cdp_core.decision_stakeholder ds
WHERE ds.response_required
  AND ds.participation_status NOT IN ('responded', 'waived', 'closed')

UNION ALL

SELECT
    'rule_blocked_transition' AS blocker_type,
    rer.registry_name,
    rer.decision_id,
    rer.workflow_instance_id,
    rer.created_task_id AS task_id,
    rer.created_stakeholder_link_id AS stakeholder_link_id,
    rer.rule_evaluation_id,
    'blocking' AS severity,
    coalesce(rer.finding_text, 'Rule blocked transition') AS blocker_text,
    rer.created_at AS observed_at
FROM cdp_core.rule_evaluation_result rer
WHERE rer.blocked_transition;

COMMENT ON VIEW cdp_projection.nemawashi_blockers IS
'Unified blocker projection for workflow, task, stakeholder-response, and rule-evaluation blockers.';

CREATE OR REPLACE VIEW cdp_projection.communication_thread_flat AS
SELECT
    ct.thread_id,
    ct.registry_name,
    ct.decision_id,
    'decision_register:' || ct.registry_name || ':' || ct.decision_id AS decision_domain,
    ct.workflow_instance_id,
    ct.thread_type,
    ct.thread_status,
    ct.created_by_actor_id,
    creator.display_label AS created_by_actor_label,
    ct.created_at,
    ct.closed_at,
    count(DISTINCT cp.participant_id) AS participant_count,
    count(DISTINCT cm.message_id) AS message_count,
    max(cm.created_at) AS latest_message_at
FROM cdp_core.communication_thread ct
LEFT JOIN cdp_core.identifier_registry creator
  ON creator.registry_name = 'actor'
 AND creator.identifier_id = ct.created_by_actor_id
LEFT JOIN cdp_core.communication_participant cp
  ON cp.thread_id = ct.thread_id
LEFT JOIN cdp_core.communication_message cm
  ON cm.thread_id = ct.thread_id
GROUP BY
    ct.thread_id,
    ct.registry_name,
    ct.decision_id,
    ct.workflow_instance_id,
    ct.thread_type,
    ct.thread_status,
    ct.created_by_actor_id,
    creator.display_label,
    ct.created_at,
    ct.closed_at;

COMMENT ON VIEW cdp_projection.communication_thread_flat IS
'Flat governed communication thread projection with participant and message counts.';

CREATE OR REPLACE VIEW cdp_projection.rule_evaluation_findings AS
SELECT
    rer.rule_evaluation_id,
    rer.rule_id,
    rd.rule_code,
    rd.rule_version,
    rs.rule_set_code,
    rs.rule_set_version,
    rs.scope,
    rer.workflow_instance_id,
    rer.registry_name,
    rer.decision_id,
    'decision_register:' || rer.registry_name || ':' || rer.decision_id AS decision_domain,
    rer.evaluation_status,
    rer.matched,
    rd.action_type,
    rer.action_taken,
    rd.severity,
    rd.blocking AS rule_blocking,
    rer.blocked_transition,
    rer.finding_text,
    rer.created_task_id,
    rer.created_stakeholder_link_id,
    rer.created_challenge_id,
    rer.created_at
FROM cdp_core.rule_evaluation_result rer
JOIN cdp_core.rule_definition rd
  ON rd.rule_id = rer.rule_id
JOIN cdp_core.rule_set rs
  ON rs.rule_set_id = rd.rule_set_id;

COMMENT ON VIEW cdp_projection.rule_evaluation_findings IS
'Rule evaluation finding projection for governed work, blockers, actions, and Superset review.';
