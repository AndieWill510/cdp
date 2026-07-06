# Decision Lifecycle Review Flow

Status: design sketch v0.1  
Audience: implementers, demo builders, corporate attorneys, Trust & Safety reviewers, AI governance leads  
Related RFCs / docs:

- `README.md`
- `rfc/RFC-CDP-023-Decision-Lifecycle-Envelope.md`
- `rfc/RFC-CDP-025-CDP-Persistence-Model.md`
- `docs/control-plane-as-decision-registry.md`
- `docs/identifier-registry.md`
- `docs/self-canonicalizing-ingestion.md`
- `docs/product-demo-scenarios-roadmap.md`
- `docs/superset-decision-visualization-roadmap.md`

---

## 1. Purpose

The current demo substrate lets us see decisions:

```text
self-canonicalized workbook
  -> normalized decision registry
  -> identifier validation
  -> projections
  -> Superset cockpit
  -> attorney/safety review packet
```

That gives understanding.

The next step is to move from understanding into CDP's constitutional lifecycle:

```text
Understand -> Test -> Challenge -> Adjudicate -> Legitimize -> Execute / Block -> Record -> Learn / Repair
```

This is the operational bridge from the decision register to the RFC lifecycle.

The demo should not only show that a decision happened.

It should show whether the decision can survive review.

---

## 2. Relationship to the RFC lifecycle

The README defines the Decision Plane flow as:

```text
Nemawashi -> Propose -> Challenge -> Test -> Adjudicate -> Legitimize -> Execute -> Record -> Learn
```

For demo/product purposes, the first reviewable slice can use this practical mapping:

```text
Understanding  -> Nemawashi / Record / Human-readable surface
Testing        -> Test
Challenge      -> Challenge
Adjudication   -> Adjudicate
Legitimation   -> Legitimize
Execution      -> Execute or block execution
Record         -> Record governed artifacts and lifecycle state
Learning       -> Learn / Repair / Appeal
```

The important correction is this:

```text
Visualization is not adjudication.
Understanding is not legitimacy.
A dashboard can reveal a decision, but CDP must govern whether it stands.
```

---

## 3. Conceptual flow

Each material decision should be able to move through this flow:

```text
1. Decision is observed or proposed
2. Decision is registered
3. Decision is understood
4. Tests are selected and run
5. Challenges are raised
6. Evidence and test results are reviewed
7. Adjudication decides whether the decision stands
8. Legitimation records why the adjudicated outcome is valid
9. Execution is allowed, blocked, repaired, or superseded
10. Records are sealed for audit and replay
11. Learning artifacts update future policy, tests, or identifiers
```

This lets a reviewer ask:

```text
What happened?
Why was it allowed?
Who had standing?
What was tested?
Who challenged it?
How was the challenge resolved?
Can this decision execute?
What must be repaired?
What should the system learn?
```

---

## 4. Lifecycle stages as product surfaces

### 4.1 Understanding

Purpose:

```text
Turn raw decision rows into a reviewable decision object.
```

Inputs:

- `cdp_core.decision_registry`
- `cdp_core.identifier_registry`
- `cdp_projection.decision_registry_flat`
- scenario metadata
- source workbook / canonical workbook

Outputs:

- attorney-facing decision row;
- human-readable decision summary;
- known identifiers and types;
- permission source summary;
- parent-child lineage summary;
- initial governance findings.

Reviewer questions:

```text
What decision was made?
Who or what made it?
What was acted upon?
What action was taken?
What permission source allowed it?
Was human review required?
What prior decision does this depend on?
```

Product surface:

- Superset decision cockpit;
- Attorney Decision Register;
- scenario review packet.

Minimum implementation:

```text
one decision row -> one review card / row -> one lifecycle envelope candidate
```

---

### 4.2 Test

Purpose:

```text
Determine whether the decision satisfies objective checks before it can stand.
```

Inputs:

- decision row;
- class-specific test profile;
- policy references;
- identifier registry;
- source evidence;
- parent decision chain.

Example tests:

```text
identifier_integrity_test
permission_source_test
standing_test
human_review_required_test
lineage_integrity_test
policy_threshold_test
source_evidence_presence_test
normal_form_test
appeal_or_repair_block_test
```

Outputs:

```text
test_result_record
```

Minimum fields:

```text
test_result_id
decision_id
test_profile_id
test_name
test_status: passed|failed|warning|not_applicable
test_severity: info|warning|blocking
evidence_refs
finding_text
created_at
created_by
```

Demo examples:

```text
PASS: subject_actor_id exists and is typed correctly.
PASS: permission_source_id exists and is typed correctly.
FAIL: human_required = true but human_approver_id = unknown.
WARNING: permission source is deprecated.
BLOCKING: parent_decision_id references a missing decision.
```

Product surface:

- Test Results tab;
- per-decision test panel;
- rollup by failed/warning/passed tests.

---

### 4.3 Challenge

Purpose:

```text
Allow a reviewer, affected party, policy owner, or automated control to contest a decision.
```

Inputs:

- decision row;
- test results;
- evidence refs;
- policy refs;
- reviewer challenge statement;
- affected party claim, if any.

Challenge types:

```text
standing_challenge
permission_challenge
evidence_challenge
policy_interpretation_challenge
human_review_challenge
lineage_challenge
fairness_or_safety_challenge
repair_or_appeal_challenge
```

Outputs:

```text
challenge_record
```

Minimum fields:

```text
challenge_id
decision_id
challenge_type
raised_by_actor_id
standing_basis
challenge_status: raised|accepted_for_review|rejected_as_out_of_scope|resolved|withdrawn
severity: info|warning|blocking
challenge_summary
requested_remedy
evidence_refs
created_at
```

Demo examples:

```text
Challenge: decision used workflow_access_v1, but the request required policy_rule authority.
Challenge: human approval was required but only unknown was recorded.
Challenge: decision dec_004 approves dec_003, but dec_003 failed its policy-threshold test.
Challenge: moderation removal was appealed by affected party.
```

Product surface:

- Challenge Queue;
- per-decision challenge list;
- challenge severity rollup;
- unresolved blocking challenges.

---

### 4.4 Adjudicate

Purpose:

```text
Resolve tests and challenges into a governed outcome.
```

Inputs:

- decision row;
- test result records;
- challenge records;
- evidence records;
- policy records;
- standing records;
- prior adjudications or precedents.

Adjudication outcomes:

```text
uphold
modify
block
remand_for_human_review
require_repair
supersede
mark_not_reviewable
```

Outputs:

```text
adjudication_record
```

Minimum fields:

```text
adjudication_id
decision_id
adjudicator_actor_id
adjudication_status: draft|final|superseded
outcome
rationale_summary
test_result_refs
challenge_refs
evidence_refs
policy_refs
required_actions
created_at
```

Demo examples:

```text
UPHOLD: access denial stands because identity verification failed and policy source is valid.
REMAND: claim approval requires named human approver before execution.
BLOCK: customer account restriction lacks valid permission source.
REPAIR: moderation removal was appealed and must be reversed.
SUPERSEDE: dispute denial superseded after new evidence.
```

Product surface:

- Adjudication Queue;
- Decision Outcome panel;
- upheld/blocked/remanded/repaired rollup;
- unresolved adjudication blockers.

---

### 4.5 Legitimize

Purpose:

```text
Record why the adjudicated outcome is valid enough to stand or proceed.
```

Inputs:

- adjudication record;
- standing record;
- test summary;
- challenge resolution summary;
- policy basis;
- repair/appeal status.

Outputs:

```text
legitimacy_basis_record
```

Minimum fields:

```text
legitimacy_basis_id
decision_id
adjudication_id
legitimacy_status: legitimized|not_legitimized|conditional|blocked
standing_status
challenge_resolution_status
repair_status
legitimacy_summary
execution_constraints
created_at
```

Demo examples:

```text
Legitimized: automated denial stands and may be recorded.
Conditional: execution allowed only after human approver is named.
Blocked: unresolved appeal prevents closure.
Not legitimized: permission source failed validation.
```

Product surface:

- legitimacy badge per decision;
- execution readiness panel;
- closure-blocked findings.

---

### 4.6 Execute / Block / Repair

Purpose:

```text
Ensure legitimacy does not automatically become action.
```

Inputs:

- legitimacy basis record;
- execution constraints;
- tool permissions;
- human approval status;
- repair or appeal flags.

Execution outcomes:

```text
execution_allowed
execution_queued
execution_blocked
execution_repaired
execution_superseded
```

Outputs:

```text
execution_record
repair_record
appeal_record
supersession_record
```

Minimum fields:

```text
execution_record_id
decision_id
execution_status
tool_or_system_id
execution_constraints
blocked_reason
repair_refs
appeal_refs
created_at
```

Demo examples:

```text
Queued: human approval still required.
Blocked: unresolved appeal exists.
Executed: access denial recorded.
Repaired: content removal reversed after appeal.
Superseded: dispute decision replaced by corrected final resolution.
```

Product surface:

- execution queue;
- blocked execution view;
- repair queue;
- appeal queue;
- final outcome register.

---

### 4.7 Record and Learn

Purpose:

```text
Preserve the governed path and improve future tests, policies, scenarios, and identifiers.
```

Inputs:

- all lifecycle records;
- final outcome;
- appeal/repair artifacts;
- reviewer notes;
- scenario-level findings.

Outputs:

```text
decision_lifecycle_envelope
learning_artifact
governed_path_manifest
```

Minimum learning outputs:

```text
new_test_needed
policy_gap
identifier_registry_update
scenario_fixture_update
dashboard_gap
report_template_update
human_review_rule_update
```

Demo examples:

```text
Learning: add test for named human approver when human_required = true.
Learning: add policy source type for emergency exception.
Learning: add dashboard card for unresolved appeals.
Learning: add scenario fixture for superseded decisions.
```

Product surface:

- learning queue;
- policy/test backlog;
- fixture update backlog;
- governance improvement report.

---

## 5. Data model sketch

The current `decision_registry` is the base observed/proposed decision table.

To support the full lifecycle, add lifecycle tables or governed-record profiles around it.

Minimum new tables:

```text
cdp_core.decision_lifecycle_envelope
cdp_core.decision_test_result
cdp_core.decision_challenge
cdp_core.decision_adjudication
cdp_core.decision_legitimacy_basis
cdp_core.decision_execution_record
cdp_core.decision_learning_artifact
```

Alternative RFC-pure implementation:

```text
cdp_core.decision_lifecycle_envelope
cdp_core.governed_record
cdp_core.envelope_record_ref
cdp_core.event_log
```

Then represent tests/challenges/adjudications/legitimacy/execution/learning as governed record types.

The demo-friendly hybrid is:

```text
Specific lifecycle tables for queryability
+ governed_record references for RFC alignment
+ event log for audit/replay
```

---

## 6. Lifecycle envelope sketch

One decision should have one lifecycle envelope.

The envelope is the governed path index.

It should not duplicate every artifact.

It should point to them.

Minimum columns:

```text
envelope_id
decision_id
registry_name
lifecycle_stage
status
standing_status
repair_status
closure_blocked
closure_blocking_reason
proposal_ref
challenge_refs
test_refs
adjudication_ref
legitimacy_ref
execution_record_ref
appeal_refs
repair_refs
learning_refs
governed_path_hash
created_at
updated_at
```

The envelope lets Superset and reports show:

```text
where the decision is in lifecycle
what unresolved blockers exist
what governed records support the current status
whether the decision can be closed
whether the decision can execute
```

---

## 7. Demo flow across one scenario

Use `benefits_claim_review` as the first lifecycle demo.

### 7.1 Understand

Load claims workbook.

Canonicalize headers.

Register decisions.

Show decisions in Superset.

### 7.2 Test

Run tests:

```text
identifier integrity
permission source validity
human review required
parent-child lineage
policy threshold
```

### 7.3 Challenge

Raise two challenges:

```text
Challenge 1: dec_003 escalated because threshold exceeded, but threshold policy source is missing.
Challenge 2: dec_004 approves dec_003, but dec_003 has an unresolved challenge.
```

### 7.4 Adjudicate

Resolve:

```text
dec_001 upheld
dec_002 upheld
dec_003 remanded for policy source correction
dec_004 blocked until dec_003 is adjudicated
```

### 7.5 Legitimize

Record:

```text
dec_001 legitimized
dec_002 legitimized
dec_003 conditional
dec_004 not_legitimized / blocked
```

### 7.6 Execute / repair

Execute only legitimized decisions.

Queue conditional decisions.

Block non-legitimized decisions.

### 7.7 Record / learn

Generate:

```text
attorney_review_report.md
trust_safety_review_report.md
lifecycle_envelope.json
governed_path_manifest.json
learning_artifact.json
```

Learning:

```text
Add policy-threshold test to all claim escalation decisions.
Add Superset card for blocked dependent decisions.
Add fixture for approval blocked by unresolved parent challenge.
```

---

## 8. Superset surfaces for lifecycle review

Add these Superset dashboard sections after basic decision visualization exists:

### 8.1 Lifecycle status

Shows:

```text
count by lifecycle_stage
count by status
closure_blocked count
repair_status count
```

### 8.2 Test results

Shows:

```text
tests passed/warning/failed/blocking
tests by decision class
tests by scenario
tests by severity
```

### 8.3 Challenge queue

Shows:

```text
open challenges
blocking challenges
challenges by type
challenges by raised_by_actor_id
challenges awaiting adjudication
```

### 8.4 Adjudication queue

Shows:

```text
pending adjudications
adjudication outcomes
blocked decisions
remanded decisions
upheld decisions
repaired decisions
```

### 8.5 Execution readiness

Shows:

```text
execution_allowed
execution_queued
execution_blocked
execution_repaired
execution_superseded
```

### 8.6 Learning backlog

Shows:

```text
new tests needed
policy gaps
identifier registry updates
scenario fixture updates
dashboard gaps
report template updates
```

---

## 9. Test strategy

Unit tests should move from ingestion-only to lifecycle assertions.

Add tests like:

```text
test_decision_creates_lifecycle_envelope
test_identifier_failure_creates_blocking_test_result
test_missing_human_approver_creates_warning_or_blocking_test_result
test_challenge_blocks_legitimation_until_adjudicated
test_adjudication_can_uphold_decision
test_adjudication_can_remand_decision
test_adjudication_can_block_decision
test_legitimized_decision_can_enter_execution_queue
test_blocked_decision_cannot_execute
test_repair_required_blocks_closure
test_learning_artifact_created_from_failed_test
```

Scenario-level tests should verify:

```text
scenario input
  -> canonical decisions
  -> lifecycle envelopes
  -> test results
  -> challenge records
  -> adjudication records
  -> legitimacy records
  -> execution records
  -> review packet
  -> Superset-ready projections
```

---

## 10. What should be built next

### Step 1: Define lifecycle governed record types

Create a controlled list:

```text
test_result_record
challenge_record
adjudication_record
legitimacy_basis_record
execution_record
appeal_record
repair_record
learning_artifact
```

### Step 2: Add lifecycle schema sketch / DDL

Add a new DDL file:

```text
db/ddl/002-decision-lifecycle-review.sql
```

Start with:

```text
decision_lifecycle_envelope
decision_test_result
decision_challenge
decision_adjudication
decision_legitimacy_basis
decision_execution_record
decision_learning_artifact
```

### Step 3: Add lifecycle projection views

Add:

```text
cdp_projection.lifecycle_status_summary
cdp_projection.decision_test_result_flat
cdp_projection.challenge_queue
cdp_projection.adjudication_queue
cdp_projection.execution_readiness
cdp_projection.learning_backlog
```

### Step 4: Add scenario lifecycle fixtures

For `benefits_claim_review`, add:

```text
tests/fixtures/scenarios/benefits_claim_review/test_results.csv
tests/fixtures/scenarios/benefits_claim_review/challenges.csv
tests/fixtures/scenarios/benefits_claim_review/adjudications.csv
tests/fixtures/scenarios/benefits_claim_review/legitimacy_basis.csv
tests/fixtures/scenarios/benefits_claim_review/execution_records.csv
tests/fixtures/scenarios/benefits_claim_review/learning_artifacts.csv
```

### Step 5: Add lifecycle unit tests

Add:

```text
tests/test_decision_lifecycle_review.py
```

### Step 6: Extend Superset roadmap

Add lifecycle sections to the `CDP Scenario Review Cockpit`:

```text
Lifecycle status
Test results
Challenge queue
Adjudication queue
Execution readiness
Learning backlog
```

### Step 7: Extend review reports

Add lifecycle sections to:

```text
attorney_review_report.md
trust_safety_review_report.md
```

---

## 11. Design rules

Understanding is not legitimacy.

Testing is not adjudication.

Challenge is not failure.

Adjudication is not execution.

Execution is not closure.

Closure is not allowed while repair or appeal remains unresolved.

Dashboards reveal lifecycle state.

CDP records lifecycle authority.

The decision register tells us what happened.

The lifecycle envelope tells us whether it can stand.
