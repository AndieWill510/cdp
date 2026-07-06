# Nemawashi Workflow and Rules Engine Bones

Status: design sketch v0.1  
Audience: implementers, product builders, corporate attorneys, Trust & Safety reviewers, AI governance leads  
Related docs / RFCs:

- `README.md`
- `rfc/RFC-CDP-023-Decision-Lifecycle-Envelope.md`
- `rfc/RFC-CDP-025-CDP-Persistence-Model.md`
- `docs/identifier-registry.md`
- `docs/decision-lifecycle-review-flow.md`
- `docs/superset-decision-visualization-roadmap.md`
- `db/ddl/001-decision-registry-kernel.sql`

---

## 1. Purpose

Nemawashi needs more than visualization.

It needs a workflow engine, a rules engine, stakeholder mapping, tasking, and communication surfaces.

But the design must not turn `config_lookup` into a magical rules engine.

The bones should be:

```text
Decision Registry
  What decision exists?

Identifier Registry
  What actors, teams, roles, policies, objects, and systems are known?

Stakeholder Map
  Who has standing, responsibility, interest, risk, or review authority?

Workflow Engine
  What stage is the decision in, what work is pending, and what transition is allowed?

Rules Engine
  What rules select stakeholders, create tasks, block transitions, or require challenge/adjudication?

Communication Layer
  How do identified people and teams communicate, object, clarify, witness, or approve?

Lifecycle Envelope
  What governed path records prove that Nemawashi happened or did not happen?
```

---

## 2. Boundary: config lookup is not the rules engine

`cdp_core.config_lookup` is useful.

It should stay useful.

It should not become governance infrastructure by accident.

Allowed uses:

```text
feature flags
batch sizes
timeouts
default display settings
local demo switches
non-governance UI behavior
```

Not allowed:

```text
standing rules
stakeholder selection rules
challenge/adjudication rules
execution blocking rules
permission authority
policy interpretation
review sufficiency
appeal or repair blocking
```

Rule of thumb:

```text
If changing the value changes who gets to participate, who must review, whether a decision can advance, whether execution is blocked, or whether a record is legitimate, it is not config_lookup.
```

Those are governed rules.

They need identity, versioning, status, evidence, auditability, and evaluation results.

---

## 3. Core product problem

For any material decision, CDP must answer:

```text
Who needs to know?
Who has standing?
Who owns the policy?
Who owns the system?
Who is affected?
Who can challenge?
Who must review?
Who can adjudicate?
Who must be notified before execution?
What communication has already happened?
What dissent or unresolved questions remain?
Can this decision move forward?
```

That is Nemawashi operationalized.

---

## 4. Minimum conceptual architecture

```text
cdp_core.decision_registry
        |
        v
cdp_core.stakeholder_map
        |
        v
cdp_core.workflow_instance  <---- cdp_core.workflow_definition
        |
        v
cdp_core.workflow_task      <---- cdp_core.rule_evaluation_result
        |
        v
cdp_core.communication_thread / message / notification
        |
        v
cdp_core.decision_lifecycle_envelope
```

The decision registry tells us what happened or what is proposed.

The stakeholder map tells us who matters.

The workflow instance tells us where the matter is.

The rules engine tells us what must happen next.

The communication layer gives stakeholders a place to respond.

The lifecycle envelope records the governed path.

---

## 5. Stakeholder model

### 5.1 Stakeholder identity

Known stakeholders should be registered in `identifier_registry` as actors, teams, systems, policy owners, organizations, or affected-party proxies.

Examples:

```text
registry_name = actor
identifier_id = user_442
identifier_type_id = human

registry_name = actor
identifier_id = claims_review_agent
identifier_type_id = agent

registry_name = actor
identifier_id = trust_safety_policy_team
identifier_type_id = team

registry_name = actor
identifier_id = privacy_counsel
identifier_type_id = human
```

This keeps identities from floating.

But stakeholder participation needs more than identity.

### 5.2 Stakeholder map

Add a decision-specific stakeholder map.

Conceptual table:

```text
cdp_core.decision_stakeholder
```

Minimum fields:

```text
stakeholder_link_id
decision_id
registry_name
stakeholder_actor_id
stakeholder_role
standing_basis
standing_status
participation_required
notification_required
response_required
response_due_at
participation_status
created_at
updated_at
```

Stakeholder roles should be controlled values, for example:

```text
decision_owner
policy_owner
system_owner
data_owner
affected_party
affected_party_proxy
human_reviewer
challenger
adjudicator
executor
witness
observer
safety_reviewer
privacy_reviewer
legal_reviewer
```

Stakeholder status values:

```text
identified
notified
acknowledged
responded
objected
clarification_requested
recused
delegated
unreachable
waived
closed
```

Standing status values should align with RFC-023 and RFC-CDP-033:

```text
unreviewed
valid
contested
recusal_active
blocked
emergency
```

---

## 6. Workflow engine

The workflow engine should manage stages, tasks, transitions, and blocking conditions.

It should not encode every rule inside application code.

It should also not hide governance inside opaque config.

### 6.1 Workflow definitions

Conceptual table:

```text
cdp_core.workflow_definition
```

Minimum fields:

```text
workflow_definition_id
workflow_code
workflow_version
display_name
applies_to_decision_class_id
status
created_at
updated_at
```

Example workflow codes:

```text
nemawashi_default_v1
benefits_claim_review_v1
restricted_data_access_v1
trust_safety_moderation_v1
```

### 6.2 Workflow stages

Conceptual table:

```text
cdp_core.workflow_stage
```

Minimum fields:

```text
workflow_stage_id
workflow_definition_id
stage_code
stage_order
lifecycle_stage
entry_criteria_ref
exit_criteria_ref
status
```

Example Nemawashi stages:

```text
intake
classify_decision
identify_stakeholders
notify_stakeholders
collect_responses
surface_dissent
resolve_or_preserve_questions
sufficiency_check
ready_for_proposal
```

### 6.3 Workflow instance

Conceptual table:

```text
cdp_core.workflow_instance
```

Minimum fields:

```text
workflow_instance_id
decision_id
workflow_definition_id
current_stage_code
lifecycle_stage
workflow_status
blocked
blocked_reason
created_at
updated_at
```

Workflow statuses:

```text
not_started
active
waiting_on_stakeholder
waiting_on_rule_evaluation
blocked
ready_to_advance
advanced
cancelled
closed
```

### 6.4 Workflow tasks

Conceptual table:

```text
cdp_core.workflow_task
```

Minimum fields:

```text
task_id
workflow_instance_id
decision_id
assigned_actor_id
assigned_role
task_type
task_status
due_at
blocking
created_by_rule_id
created_at
updated_at
```

Task types:

```text
review_decision
provide_context
raise_objection
clarify_boundary
confirm_standing
approve_participation
adjudicate_challenge
provide_evidence
acknowledge_notice
```

Task statuses:

```text
open
in_progress
completed
cancelled
expired
blocked
waived
```

---

## 7. Rules engine

The rules engine should be explicit, governed, versioned, and auditable.

It should answer:

```text
Given this decision, workflow stage, class, object, actor, risk tier, policy source, and stakeholder map, what must happen next?
```

### 7.1 Rule set

Conceptual table:

```text
cdp_core.rule_set
```

Minimum fields:

```text
rule_set_id
rule_set_code
rule_set_version
display_name
scope
status
created_at
updated_at
```

Scopes:

```text
nemawashi
proposal_admission
challenge
test
adjudication
legitimation
execution
repair
```

### 7.2 Rule definition

Conceptual table:

```text
cdp_core.rule_definition
```

Minimum fields:

```text
rule_id
rule_set_id
rule_code
rule_version
description
condition_language
condition_expression
action_type
action_payload
severity
blocking
status
created_at
updated_at
```

Allowed condition languages for MVP:

```text
sql_predicate
json_logic
python_named_function
```

Do not start with arbitrary user-authored code execution.

For MVP, prefer named deterministic functions and SQL predicates.

### 7.3 Rule evaluation result

Conceptual table:

```text
cdp_core.rule_evaluation_result
```

Minimum fields:

```text
rule_evaluation_id
rule_id
workflow_instance_id
decision_id
evaluation_status
matched
action_taken
finding_text
created_task_id
created_stakeholder_link_id
created_challenge_id
blocked_transition
created_at
```

Evaluation statuses:

```text
passed
matched
not_matched
failed_to_evaluate
warning
blocking
```

### 7.4 Rule actions

Rules should produce controlled actions:

```text
create_stakeholder_link
create_workflow_task
send_notification
open_communication_thread
raise_challenge
require_test
block_transition
allow_transition
require_adjudication
require_repair
record_learning_artifact
```

Rules should not silently mutate decisions.

Rules create governed work, findings, blockers, or records.

---

## 8. Communication layer

The app needs a simple communication model that is tied to decisions, stakeholders, tasks, and lifecycle records.

Do not start with a Slack clone.

Start with governed decision threads.

### 8.1 Communication thread

Conceptual table:

```text
cdp_core.communication_thread
```

Minimum fields:

```text
thread_id
decision_id
workflow_instance_id
thread_type
thread_status
created_by_actor_id
created_at
closed_at
```

Thread types:

```text
nemawashi_consultation
clarification
challenge_discussion
adjudication_discussion
execution_review
repair_discussion
```

### 8.2 Communication participant

Conceptual table:

```text
cdp_core.communication_participant
```

Minimum fields:

```text
thread_id
actor_id
participant_role
notification_status
last_seen_at
```

### 8.3 Communication message

Conceptual table:

```text
cdp_core.communication_message
```

Minimum fields:

```text
message_id
thread_id
actor_id
message_type
message_body
message_status
created_at
```

Message types:

```text
comment
objection
clarification_request
clarification_response
boundary_statement
evidence_pointer
standing_statement
approval
recusal
```

Some messages may produce governed records.

Examples:

```text
objection -> challenge_record
boundary_statement -> boundary_condition_record
standing_statement -> standing_record
approval -> human_approval_record
recusal -> recusal_record
```

---

## 9. Nemawashi workflow example

Given a decision:

```text
decision_class_id = access_escalation
object_type = restricted_dataset
permission_source_type = workflow_configuration
human_required = true
```

The workflow engine starts:

```text
workflow_definition = restricted_data_access_v1
current_stage = identify_stakeholders
lifecycle_stage = nemawashi
```

Rules evaluate:

```text
IF object_type = restricted_dataset
THEN add stakeholder role = data_owner

IF permission_source_type = workflow_configuration
THEN add stakeholder role = system_owner

IF human_required = true
THEN create task = assign_human_reviewer

IF decision_class_id = access_escalation
THEN create communication_thread = nemawashi_consultation

IF affected_party exists
THEN notify affected_party_proxy

IF no data_owner identified
THEN block transition to proposal_admission
```

The app surfaces:

```text
Stakeholders identified
Tasks assigned
Consultation thread opened
Missing data owner blocker
Unresolved questions
Early dissent
Ready/not ready for proposal admission
```

The lifecycle envelope gets refs:

```text
stakeholder_map_ref
pre_proposal_consultation_refs
early_dissent_refs
boundary_condition_refs
unresolved_question_refs
```

---

## 10. What belongs where

### 10.1 config_lookup

Use for:

```text
default_response_window_hours = 72
local_demo_auto_notify = false
ui_show_advanced_lifecycle_tabs = true
default_dashboard_refresh_seconds = 60
```

Do not use for:

```text
who must review restricted data access
whether a stakeholder has standing
whether a challenge is blocking
whether a decision can advance
whether execution is allowed
```

### 10.2 identifier_registry

Use for:

```text
actor IDs
team IDs
role IDs
policy IDs
object IDs
workflow codes
rule-set codes
message type controlled values
stakeholder role controlled values
```

### 10.3 rule_definition

Use for:

```text
if decision class = X, require role Y
if risk tier = high, require adjudicator
if human_required = true, require named reviewer
if unresolved blocking challenge exists, block legitimation
if affected party claim unresolved, block closure
```

### 10.4 workflow_instance

Use for:

```text
current stage
current status
blocked state
transition readiness
```

### 10.5 communication_thread / message

Use for:

```text
stakeholder discussion
objections
clarifications
boundary statements
evidence pointers
approvals
recusals
```

### 10.6 lifecycle envelope

Use for:

```text
indexing governed records
showing lifecycle state
recording refs into Nemawashi, challenge, test, adjudication, execution, appeal, repair, and learning
```

---

## 11. First implementation slice

Do not build all of this at once.

The first useful slice is:

```text
1. decision_stakeholder
2. workflow_definition
3. workflow_instance
4. workflow_task
5. rule_set
6. rule_definition
7. rule_evaluation_result
8. communication_thread
9. communication_message
```

Then wire it into one scenario:

```text
restricted_data_access
```

Why this scenario first?

Because stakeholder discovery is obvious:

```text
data owner
system owner
privacy counsel
security reviewer
human approver
affected party or proxy
```

And the Nemawashi failure modes are intuitive:

```text
missing data owner
unnotified privacy counsel
human approver unknown
emergency exception without review
blocking objection unresolved
```

---

## 12. First demo story

The demo should show:

```text
1. A restricted-data access decision is registered.
2. CDP identifies required stakeholder roles.
3. CDP cannot find a data owner.
4. CDP creates a blocking workflow task.
5. CDP opens a Nemawashi consultation thread.
6. Privacy counsel raises an objection.
7. CDP records the objection as a challenge candidate.
8. The workflow cannot advance to proposal admission until the blocker is resolved or waived.
9. The lifecycle envelope records stakeholder_map_ref, early_dissent_refs, unresolved_question_refs, and consultation refs.
```

This shows the product thesis:

```text
CDP does not just ask whether the model was right.
CDP asks whether the right people, rules, evidence, and objections were present before the decision moved forward.
```

---

## 13. DDL direction

Add a new DDL file rather than mutating the current registry kernel too much:

```text
db/ddl/003-nemawashi-workflow-rules.sql
```

Keep `001-decision-registry-kernel.sql` as the decision/identifier core.

Let `003` add workflow and rules bones.

Recommended first tables:

```text
cdp_core.decision_stakeholder
cdp_core.workflow_definition
cdp_core.workflow_stage
cdp_core.workflow_instance
cdp_core.workflow_task
cdp_core.rule_set
cdp_core.rule_definition
cdp_core.rule_evaluation_result
cdp_core.communication_thread
cdp_core.communication_participant
cdp_core.communication_message
```

Projection views:

```text
cdp_projection.nemawashi_stakeholder_map_flat
cdp_projection.workflow_task_queue
cdp_projection.nemawashi_blockers
cdp_projection.communication_thread_flat
cdp_projection.rule_evaluation_findings
```

---

## 14. Tests to add

Add tests like:

```text
test_restricted_data_access_identifies_required_stakeholders
test_missing_required_stakeholder_blocks_transition
test_human_required_creates_reviewer_task
test_privacy_objection_creates_challenge_candidate
test_unresolved_blocking_challenge_blocks_proposal_admission
test_consultation_thread_records_messages
test_nemawashi_refs_are_added_to_lifecycle_envelope
```

---

## 15. Design rules

Do not make `config_lookup` carry governance authority.

Do not hide stakeholder selection inside application code.

Do not let a stakeholder ID float.

Do not treat notification as participation.

Do not treat participation as consent.

Do not treat absence of objection as legitimacy unless a protocol explicitly says so.

Do not let communication threads become ungoverned side chatter.

Do not let the workflow engine adjudicate substance.

Do not let the rules engine silently mutate decisions.

Rules create tasks, findings, blockers, challenges, or transition permissions.

Workflow manages state.

Adjudication resolves conflict.

The lifecycle envelope indexes the governed path.
