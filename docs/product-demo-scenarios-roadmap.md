# Product Demo Scenarios Roadmap

Status: demo planning note v0.1  
Audience: corporate attorneys, Trust & Safety teams, AI governance teams, product leaders, implementers  
Related docs:

- `docs/attorney-decision-register.md`
- `docs/control-plane-as-decision-registry.md`
- `docs/identifier-registry.md`
- `docs/self-canonicalizing-ingestion.md`
- `docs/z-config-lookup-spreadsheet-ingestion.md`
- `db/ddl/001-decision-registry-kernel.sql`
- `tests/test_self_canonicalizing_ingestion.py`

---

## 1. Purpose

CDP now has the start of the control-plane substrate:

- normalized decision registry;
- decision class registry;
- identifier registry;
- self-canonicalizing spreadsheet ingestion;
- no-floating-ID validation;
- class rollups;
- parent-child decision lineage;
- attorney-facing flat projections;
- unit-test fixtures.

That is the engine room.

The next product move is to build **scenario packs** that let a corporate attorney, safety reviewer, or Trust & Safety organization see CDP work end to end.

The goal is a BizTalk-style demo:

```text
load scenario workbook
canonicalize messy input
validate identifiers
insert governed decision rows
show what decisions happened
show what allowed them
show where they cluster
show parent-child lineage
show review/audit outputs
```

The demo should feel like a working control plane, not an architecture lecture.

---

## 2. Demo principle

Each scenario pack should answer a concrete governance question.

Not:

```text
Here is a database schema.
```

But:

```text
Here is a corporate/legal/safety problem.
Here are the agentic decisions.
Here is what the agent did.
Here is what permission source allowed it.
Here is where a human was required.
Here are the exceptions.
Here is the lineage.
Here is the report an attorney can review.
```

The product demo should show the path from messy operational artifact to governed decision visibility.

---

## 3. Scenario-pack shape

Each scenario pack should live under:

```text
tests/fixtures/scenarios/<scenario_slug>/
```

Recommended files:

```text
README.md
identifier_registry.csv
decision_classes.csv
decisions.csv
expected_decision_registry_flat.csv
expected_class_rollup.csv
expected_parent_child_edges.csv
expected_ingestion_report.json
```

Optional later files:

```text
source_workbook.xlsx
canonical_workbook.xlsx
attorney_review_report.md
trust_safety_review_report.md
scenario_dashboard.json
scenario_notes.md
```

The test suite should be able to load any scenario pack and verify:

1. bad/missing headers do not matter;
2. canonical headers are generated;
3. identifiers are registered before decisions;
4. decisions insert only if identifiers are known and correctly typed;
5. class rollups match expected outputs;
6. parent-child edges match expected outputs;
7. attorney-facing flat rows are reproducible;
8. governance findings are explicit.

---

## 4. Core demo flow

Every scenario should run the same story:

```text
1. Receive workbook
2. Detect ingestion profile
3. Identify sheet roles
4. Ignore human-authored headers
5. Generate canonical headers
6. Normalize values
7. Register or validate identifiers
8. Validate classes
9. Validate decision rows
10. Insert canonical rows
11. Produce projections
12. Produce visualizations
13. Produce attorney/safety review report
```

The product should emphasize:

```text
No data cleansing project.
No floating IDs.
No hidden chain-of-thought request.
No prose-parsing for governance.
No post-hoc model confession booth.
```

---

## 5. Scenario 1: Benefits claim approval and escalation

### Audience

Corporate attorney, compliance reviewer, AI governance lead.

### Business question

```text
What benefit-claim decisions did the agent make or recommend, which ones required human approval, and what policy allowed each one?
```

### Why it matters

This is the cleanest first demo because it resembles the current sample fixtures and has obvious decision types:

- claim intake;
- recommendation;
- escalation;
- human approval;
- denial or repair.

### Story

An AI claims-review agent reviews four claims.

Some are straightforward recommendations.

One crosses an auto-approval threshold and escalates to human review.

A human reviewer approves or modifies the recommendation.

### Decision classes

```text
claim
claim_intake
claim_recommendation
claim_escalation
claim_approval
claim_denial
claim_repair
```

### Identifier registries needed

```text
actor_type
actor
object_type
object
predicate_verb
permission_source_type
permission_source
parent_relation_type
source_system
```

### Example decisions

```text
dec_001: agent recommends approval of claim_9981 under policy_claims_approval_v2
dec_002: agent denies claim_9982 under policy_claims_denial_v1
dec_003: agent escalates claim_9983 because threshold exceeded
dec_004: human approves the escalated claim recommendation
```

### Visualizations

- decisions by class;
- human-required count by class;
- permission-source distribution;
- parent-child lineage for escalated decisions;
- unknown-permission findings.

### Demo punchline

```text
The attorney can see every material AI claim decision, what allowed it, where human review occurred, and which decisions depended on prior decisions.
```

---

## 6. Scenario 2: Access request and restricted-data decisioning

### Audience

Corporate attorney, privacy counsel, security governance, compliance team.

### Business question

```text
Who or what approved, denied, or escalated access to restricted data, and under what permission source?
```

### Why it matters

Access decisions are easy for lawyers and security teams to understand. They also expose the difference between:

- identity;
- role;
- policy;
- workflow;
- human approval;
- exception.

### Story

An access agent evaluates requests to a restricted dataset.

Some requests are approved because the requester has an approved role.

Some are denied because identity verification or purpose limitation fails.

One request is escalated due to emergency exception handling.

### Decision classes

```text
access
access_intake
access_approval
access_denial
access_escalation
emergency_exception
```

### Example decisions

```text
dec_101: agent denies access_request_7731 because identity verification failed
dec_102: agent approves access_request_7732 because role_data_scientist was authorized
dec_103: agent escalates access_request_7733 under emergency exception workflow
dec_104: human approves emergency exception access
```

### Visualizations

- access approvals vs denials;
- emergency exceptions by source;
- human approval burden;
- parent-child chain from emergency request to approval;
- requests with unknown or deprecated permission sources.

### Demo punchline

```text
Security and legal can distinguish routine access decisions from exceptions and can see which agentic decisions required human approval.
```

---

## 7. Scenario 3: Trust & Safety content moderation escalation

### Audience

Trust & Safety organization, platform counsel, policy team, safety operations.

### Business question

```text
What content moderation decisions did the AI agent recommend or execute, which policy class was involved, and where did human review happen?
```

### Why it matters

This scenario shows CDP beyond enterprise workflow and into safety operations.

It is useful because Trust & Safety work already thinks in terms of:

- policy taxonomies;
- queues;
- escalations;
- moderator decisions;
- appeal and repair.

### Story

A moderation agent evaluates flagged content.

It recommends allow, label, remove, escalate, or suspend action.

Some decisions are routed to a human reviewer.

One removal is appealed and later repaired.

### Decision classes

```text
content_moderation
content_label
content_removal
account_action
human_review_escalation
appeal
repair
```

### Example decisions

```text
dec_201: agent labels content_item_1001 under misinformation_policy_v3
dec_202: agent removes content_item_1002 under harassment_policy_v2
dec_203: agent escalates content_item_1003 for human review
dec_204: human upholds removal decision
dec_205: user appeal is granted and prior removal is repaired
```

### Visualizations

- decisions by moderation class;
- removals vs labels vs escalations;
- human-review burden by policy area;
- appeal/repair lineage;
- unknown policy source findings.

### Demo punchline

```text
Trust & Safety can audit not only what happened, but how moderation decisions moved through escalation, appeal, and repair.
```

---

## 8. Scenario 4: Customer-support agent refunds and account actions

### Audience

Corporate counsel, customer operations, risk, safety, product trust.

### Business question

```text
What customer-impacting actions did the agent take, which actions were automatic, and which required human approval?
```

### Why it matters

This scenario is commercially intuitive and lower-regulatory-friction than benefits or healthcare.

It demonstrates state-changing tool use:

- refund issued;
- refund denied;
- account credited;
- case escalated;
- account restricted;
- task created.

### Story

A customer-support agent reviews support cases.

It issues small refunds automatically.

It escalates larger refunds.

It denies a refund when policy conditions are not met.

It creates a review task when account abuse is suspected.

### Decision classes

```text
customer_support
refund_approval
refund_denial
account_credit
account_restriction
review_task
human_review_escalation
```

### Example decisions

```text
dec_301: agent approves refund_2001 under refund_policy_small_amount_v1
dec_302: agent escalates refund_2002 because amount exceeded threshold
dec_303: human approves escalated refund_2002
dec_304: agent creates review_task_901 for suspected account abuse
```

### Visualizations

- automatic vs human-approved customer actions;
- refund decisions by amount class;
- escalations by policy;
- parent-child chain from agent escalation to human approval;
- review tasks created by agent.

### Demo punchline

```text
A company can audit customer-impacting agent actions without asking the model to explain itself after the fact.
```

---

## 9. Scenario 5: HR screening / employment decision support

### Audience

Employment counsel, HR compliance, AI governance, risk committee.

### Business question

```text
What employment-related recommendations did the AI system make, what was the decision class, and where was human decision-making required?
```

### Why it matters

This is a high-sensitivity scenario. It should be handled carefully as a governance demo, not as an endorsement of automated hiring.

It is useful because it shows CDP can separate:

- recommendation;
- routing;
- human review;
- final decision;
- appeal/repair.

### Story

An AI screening assistant sorts candidate records into review queues.

It does not make final hiring decisions.

It recommends follow-up, escalates borderline records, and records human reviewer decisions.

### Decision classes

```text
employment_screening
candidate_routing
candidate_follow_up
human_review_escalation
human_review_decision
appeal
repair
```

### Example decisions

```text
dec_401: agent recommends candidate_5001 for recruiter follow-up
dec_402: agent escalates candidate_5002 due to insufficient evidence
dec_403: human reviewer approves candidate_5002 for phone screen
dec_404: appeal/review corrects an earlier routing decision
```

### Visualizations

- agent recommendations vs human decisions;
- escalation rate;
- classes with unknown permission sources;
- appeal/repair lineage;
- final human review count.

### Demo punchline

```text
The system shows where AI provided decision support while preserving human accountability for sensitive employment outcomes.
```

---

## 10. Scenario 6: Financial dispute / chargeback workflow

### Audience

Financial-services counsel, risk, compliance, trust operations.

### Business question

```text
What dispute decisions did the AI recommend, what evidence/policy source allowed them, and which decisions were repaired or superseded?
```

### Why it matters

Financial disputes naturally contain chains:

- intake;
- evidence review;
- provisional credit;
- denial;
- escalation;
- final resolution;
- reversal/repair.

This scenario is excellent for parent-child lineage.

### Decision classes

```text
dispute
chargeback_intake
evidence_review
provisional_credit
dispute_denial
human_review_escalation
final_resolution
repair
```

### Example decisions

```text
dec_501: agent recommends provisional credit for dispute_7001
dec_502: agent denies dispute_7002 due to missing evidence
dec_503: human review supersedes dec_502 after new evidence
dec_504: repair decision records corrected customer outcome
```

### Visualizations

- dispute outcomes by class;
- superseded decisions;
- repair lineage;
- human-required decisions;
- permission-source distribution.

### Demo punchline

```text
The control plane shows how a decision changed over time and why the final outcome differs from the first agent recommendation.
```

---

## 11. Recommended first three scenario packs

Build these first:

1. `benefits_claim_review`
2. `restricted_data_access`
3. `trust_safety_moderation`

Why these three?

```text
benefits_claim_review      -> clear legal/compliance story
restricted_data_access     -> clear security/privacy story
trust_safety_moderation    -> clear safety/escalation/appeal story
```

Together they demonstrate:

- decisions;
- classes;
- identifiers;
- permissions;
- human review;
- parent-child lineage;
- analytics;
- attorney-facing outputs;
- safety-facing outputs;
- exceptions and repair.

---

## 12. Demo visualizations to build

Each scenario should produce the same core visualizations so the product feels repeatable.

### 12.1 Decision volume by class

Question:

```text
What kinds of decisions happened?
```

Data source:

```text
cdp_projection.decision_class_rollup
```

Output:

```text
bar chart by decision_class_id
```

### 12.2 Human review burden

Question:

```text
Which classes required human review?
```

Data source:

```text
cdp_projection.decision_class_rollup
```

Output:

```text
bar chart: decision_count vs human_required_count
```

### 12.3 Permission-source distribution

Question:

```text
What allowed these decisions to happen?
```

Data source:

```text
cdp_projection.decision_registry_flat
```

Output:

```text
counts by permission_source_type
```

### 12.4 Unknown/deprecated identifier findings

Question:

```text
Where is governance weak or incomplete?
```

Data source:

```text
identifier_registry + decision projections
```

Output:

```text
findings table and count cards
```

### 12.5 Parent-child lineage graph

Question:

```text
Which decisions descended from which prior decisions?
```

Data source:

```text
cdp_projection.decision_parent_child_edges
```

Output:

```text
graph / edge list / simple tree
```

### 12.6 Attorney Decision Register

Question:

```text
Can I review every material decision in plain English?
```

Data source:

```text
cdp_projection.decision_registry_flat
```

Output:

```text
spreadsheet / markdown table / PDF-ready report
```

---

## 13. Demo screens / outputs

A usable end-to-end demo should have these screens or generated artifacts:

1. **Scenario selection**
   - choose benefits, access, moderation, support, HR, or dispute scenario.

2. **Source workbook preview**
   - show messy headers and body.

3. **Self-canonicalization result**
   - show generated canonical headers.
   - show row counts and normalized fields.

4. **Identifier validation**
   - show registered IDs.
   - show missing/mistyped IDs if any.

5. **Decision Register**
   - show attorney-facing flat rows.

6. **Class analytics**
   - show counts by class and human-review burden.

7. **Lineage view**
   - show parent-child decision edges.

8. **Governance findings**
   - show unknown/deprecated IDs, unknown permission sources, missing approvals, invalid lineage.

9. **Export package**
   - canonical workbook;
   - decision register;
   - ingestion report;
   - governance findings report.

---

## 14. What should be done next

### Step 1: Create scenario-pack directory structure

Create:

```text
tests/fixtures/scenarios/benefits_claim_review/
tests/fixtures/scenarios/restricted_data_access/
tests/fixtures/scenarios/trust_safety_moderation/
```

Each scenario should include:

```text
README.md
identifier_registry_bad_headers.csv
decision_classes_bad_headers.csv
decisions_bad_headers.csv
expected_rollup.json
expected_edges.json
expected_findings.json
```

### Step 2: Generalize tests to load scenario packs

Refactor `tests/test_self_canonicalizing_ingestion.py` so it can run the same assertions against every scenario directory.

Target test style:

```text
for scenario in scenarios:
    load identifiers
    load classes
    load decisions
    canonicalize
    validate
    compare rollup
    compare edges
    compare findings
```

### Step 3: Add an ingestion-report object

Add a small in-memory or persisted report shape:

```text
batch_id
scenario_slug
profile_version
rows_received
rows_canonicalized
rows_inserted
rows_rejected
missing_identifier_count
mistyped_identifier_count
packed_field_count
unknown_permission_count
human_required_count
canonical_artifact_refs
```

### Step 4: Add expected projection fixtures

For each scenario, add expected outputs:

```text
expected_decision_registry_flat.csv
expected_decision_class_rollup.csv
expected_decision_parent_child_edges.csv
```

This turns the demo into a regression suite.

### Step 5: Add a demo runner

Add a script such as:

```text
scripts/run_demo_scenario.py
```

Example usage:

```text
python scripts/run_demo_scenario.py benefits_claim_review
```

Expected outputs:

```text
out/demo/benefits_claim_review/canonical_identifier_registry.csv
out/demo/benefits_claim_review/canonical_decision_classes.csv
out/demo/benefits_claim_review/canonical_decisions.csv
out/demo/benefits_claim_review/decision_register.md
out/demo/benefits_claim_review/ingestion_report.json
out/demo/benefits_claim_review/governance_findings.md
```

### Step 6: Add visualizations

Start with generated static artifacts:

```text
class_rollup.json
permission_source_distribution.json
human_review_burden.json
parent_child_edges.json
```

Later render them as:

```text
PNG
SVG
HTML dashboard
PowerPoint slide
```

### Step 7: Add attorney/safety report templates

Create templates:

```text
docs/templates/attorney_review_report.md
docs/templates/trust_safety_review_report.md
```

Each report should include:

- scenario summary;
- ingestion summary;
- decision register;
- class rollup;
- human-review burden;
- permission-source summary;
- lineage findings;
- governance findings;
- unresolved questions.

### Step 8: Add a narrative demo script

Create:

```text
docs/demo-script.md
```

The script should tell the end-to-end story in 8-10 minutes:

1. Here is the messy workbook.
2. Headers are wrong, but body is structurally right.
3. CDP derives canonical headers.
4. CDP validates identifiers.
5. CDP rejects floating IDs.
6. CDP loads decisions.
7. CDP shows attorney-facing decision register.
8. CDP shows analytics.
9. CDP shows lineage.
10. CDP exports a review packet.

---

## 15. Acceptance criteria for the next milestone

The next milestone is complete when:

1. At least three scenario packs exist.
2. Each scenario pack has messy-header fixtures.
3. Unit tests load all scenario packs.
4. Each scenario produces class rollups and parent-child edges.
5. Each scenario produces an attorney-facing decision register.
6. Each scenario produces an ingestion report.
7. Missing IDs fail deterministically.
8. Mistyped IDs fail deterministically.
9. Packed fields fail deterministically.
10. A demo runner can produce a review packet for at least one scenario.

---

## 16. Product positioning

The demo should position CDP as:

```text
A decision control plane for agentic systems.
```

Not just observability.

Not just logging.

Not just prompt auditing.

The distinction:

```text
Observability tells you what the system emitted.
CDP tells you what decisions were made, what allowed them, how they relate, and whether they can be reviewed.
```

For corporate attorneys and Trust & Safety teams, the key promise is:

```text
No mystery decisions.
No floating IDs.
No cleanup project.
No post-hoc model confession booth.
A reviewable decision register from governed ingestion.
```

---

## 17. Immediate next files to create

Recommended next files:

```text
tests/fixtures/scenarios/benefits_claim_review/README.md
tests/fixtures/scenarios/benefits_claim_review/identifier_registry_bad_headers.csv
tests/fixtures/scenarios/benefits_claim_review/decision_classes_bad_headers.csv
tests/fixtures/scenarios/benefits_claim_review/decisions_bad_headers.csv
tests/fixtures/scenarios/benefits_claim_review/expected_rollup.json
tests/fixtures/scenarios/benefits_claim_review/expected_edges.json
```

Then repeat for:

```text
restricted_data_access
trust_safety_moderation
```

After that, add:

```text
scripts/run_demo_scenario.py
docs/demo-script.md
```

That is the next durable product slice.
