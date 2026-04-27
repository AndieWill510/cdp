# RFC-CDP-007A: Decision-Type Maturity and Queued Execution Gates

**Status:** Draft  
**Category:** Standards Track  
**Extends:** RFC-CDP-007 Execute Protocol; RFC-CDP-008 Record Protocol; RFC-CDP-009 Learn Protocol  
**Author:** CDP Project  
**Created:** 2026-04-27  
**Filename:** `RFC-CDP-007A-Decision-Type-Maturity-and-Queued-Execution-Gates.md`

---

## Abstract

This RFC defines a CDP extension for **Decision-Type Maturity** and **Queued Execution Gates**.

The purpose of this extension is to prevent new, unproven, or risky classes of decisions from being automatically executed without supervised review. Instead of treating automation as a binary state, CDP SHALL treat each `decision_type` as a governable object that can mature through evidence, review, successful execution, and recorded outcomes.

This RFC introduces a vendor-neutral queue-based execution pattern in which decisions may be routed to review, challenge, approval, rejection, execution, or dead-letter queues according to policy. Cloud implementations MAY use services such as AWS SQS, Azure Service Bus, Google Pub/Sub, Kafka, RabbitMQ, NATS, or other durable messaging systems, but no specific vendor or queue implementation is required.

In short:

> Agentic systems MUST NOT be trusted all at once.  
> Decision types SHOULD mature through governed experience.

---

## 1. Motivation

Agentic AI systems can produce decisions, recommendations, or executable actions at scale. Without gating, a new class of automated decision may move directly from proposal to execution before humans understand its failure modes, boundary conditions, or policy implications.

Traditional human-in-the-loop patterns often focus on individual actions. That is useful but incomplete. CDP also requires governance over the **type of decision being automated**.

This RFC addresses the following problem:

> When a system encounters a new or insufficiently proven `decision_type`, execution SHOULD be delayed, queued, reviewed, and recorded until that decision type earns greater autonomy.

This creates a pattern analogous to canary deployment in software engineering. Instead of deploying code globally on first release, organizations progressively expose it, observe it, and promote it only after it demonstrates acceptable behavior.

CDP applies this same discipline to decisions.

---

## 2. Relationship to Existing CDP RFCs

### 2.1 RFC-CDP-007 Execute Protocol

This RFC extends the Execute Protocol by adding an **Execution Gate Policy** evaluation before an approved decision may be executed.

An execution gate determines whether a decision:

- MAY execute automatically;
- MUST be queued for human review;
- MUST be challenged;
- MUST receive quorum approval;
- MUST be blocked;
- MUST be routed to a dead-letter or exception process.

### 2.2 RFC-CDP-008 Record Protocol

This RFC extends the Record Protocol by requiring durable evidence of:

- gate evaluation;
- queue routing;
- reviewer identity or role;
- approval, rejection, escalation, or challenge outcome;
- maturity level at time of decision;
- graduation or demotion events;
- policy version used for gate evaluation.

### 2.3 RFC-CDP-009 Learn Protocol

This RFC extends the Learn Protocol by allowing CDP to update decision-type maturity based on recorded outcomes, human reviews, defects, reversals, appeals, and drift signals.

Learning MUST NOT silently increase autonomy without recordable policy support.

---

## 3. Terminology

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**, **MAY**, and **OPTIONAL** are to be interpreted as described in RFC 2119.

### 3.1 Decision Type

A `decision_type` is a stable classification for a recurring kind of decision.

Examples:

- `vendor_invoice_auto_approval`
- `claim_priority_reclassification`
- `customer_refund_authorization`
- `access_request_approval`
- `model_generated_policy_exception`
- `case_routing_assignment`

A `decision_type` SHOULD be specific enough to support meaningful governance, but general enough to accumulate evidence across repeated decisions.

### 3.2 Decision-Type Maturity

Decision-type maturity is the current governance state of a `decision_type`. It indicates how much autonomy CDP permits for that class of decisions.

Maturity is not a measure of model confidence alone. It is a governance state based on policy, evidence, review history, failure history, and risk.

### 3.3 Execution Gate

An execution gate is a policy-controlled checkpoint between a legitimate decision and an executable action.

A decision may be validly proposed, challenged, tested, adjudicated, and legitimated, yet still be prevented from execution if its decision type is immature, risky, disputed, or outside policy bounds.

### 3.4 Durable Queue

A durable queue is a reliable message routing mechanism that preserves a decision or execution request until it is processed, reviewed, retried, rejected, or expired.

This RFC is queue-implementation neutral.

### 3.5 Human Review

Human review is an explicit review action by an authorized person or role. Human review MAY approve, reject, challenge, modify, escalate, or defer a decision.

Human review MUST be recorded.

### 3.6 Graduation

Graduation is a policy-authorized maturity increase that permits a decision type to move to lower-friction execution.

Example:

- `experimental` → `supervised`
- `supervised` → `sampled`
- `sampled` → `autonomous`

### 3.7 Demotion

Demotion is a maturity decrease caused by policy changes, adverse outcomes, drift, failed review, appeal, defect detection, or other governance signals.

Example:

- `autonomous` → `sampled`
- `sampled` → `supervised`
- `supervised` → `restricted`

---

## 4. Maturity Levels

CDP implementations SHOULD support the following maturity levels.

| Level | Meaning | Default execution behavior |
|---|---|---|
| `experimental` | New or unproven decision type | Queue every decision for review |
| `supervised` | Early governed use | Require review for first N decisions or until policy threshold is met |
| `sampled` | Mostly trusted within bounds | Auto-execute most decisions; route sampled or risky cases for review |
| `autonomous` | Trusted within defined policy limits | Auto-execute if all policy checks pass |
| `restricted` | Sensitive, high-risk, disputed, or legally constrained | Always require human approval, quorum, or presence-bound authorization |
| `blocked` | Not permitted to execute | Reject or route to exception process |

Implementations MAY define additional maturity levels, but they SHOULD preserve the distinction between new, supervised, sampled, autonomous, restricted, and blocked behavior.

---

## 5. Execution Gate Policy

An Execution Gate Policy defines how CDP SHALL handle a decision before execution.

A policy SHOULD include:

- `decision_type`
- `maturity_level`
- first-N review requirements
- success thresholds for graduation
- failure thresholds for demotion
- sampling rules after graduation
- reviewer role requirements
- quorum requirements, if any
- presence-bound authorization requirements, if any
- emergency override handling
- expiration and retry behavior
- queue routing rules
- record requirements

### 5.1 Example Policy

```json
{
  "policy_id": "egp_vendor_invoice_auto_approval_v1",
  "policy_version": "1.0.0",
  "decision_type": "vendor_invoice_auto_approval",
  "maturity_level": "supervised",
  "first_n_requires_review": 10,
  "required_successes_to_graduate": 10,
  "failure_demotes": true,
  "demotion_failure_threshold": 1,
  "review_mode": "human_approval",
  "required_reviewer_roles": ["finance_controller"],
  "sample_rate_after_graduation": 0.05,
  "presence_bound_execution_required": false,
  "quorum_required": false,
  "queue_routes": {
    "pending_review": "cdp.decisions.pending_review",
    "approved_execution": "cdp.decisions.approved_execution",
    "rejected": "cdp.decisions.rejected",
    "challenge_required": "cdp.decisions.challenge_required",
    "dead_letter": "cdp.decisions.dead_letter"
  },
  "record_required": true
}
```

---

## 6. Queue-Based Execution Pattern

CDP implementations SHOULD support queue-based execution gates for decision types that are immature, sensitive, or under review.

A reference flow is shown below:

```text
Decision Created
   ↓
Classify decision_type
   ↓
Evaluate Execution Gate Policy
   ↓
If gated → route to pending review queue
   ↓
Reviewer approves, rejects, challenges, escalates, or defers
   ↓
If approved → route to approved execution queue
   ↓
Executor performs action
   ↓
Record writes audit evidence
   ↓
Learn evaluates maturity update
```

### 6.1 Reference Queues

Implementations MAY use the following logical queues:

```text
cdp.decisions.pending_review
cdp.decisions.approved_execution
cdp.decisions.rejected
cdp.decisions.challenge_required
cdp.decisions.deferred
cdp.decisions.dead_letter
cdp.decisions.maturity_events
```

Queue names are illustrative. Implementations MAY use any equivalent routing topology.

---

## 7. First-N Review

A CDP implementation SHOULD support first-N review for new or newly modified decision types.

First-N review means that the first `N` decisions of a given `decision_type` MUST be manually reviewed before execution.

Example:

```json
{
  "decision_type": "case_routing_assignment",
  "maturity_level": "supervised",
  "first_n_requires_review": 25,
  "required_successes_to_graduate": 25,
  "sample_rate_after_graduation": 0.10
}
```

This policy means:

1. The first 25 decisions of type `case_routing_assignment` MUST be reviewed.
2. If all required review outcomes satisfy policy, the decision type MAY graduate.
3. After graduation, at least 10% of decisions remain subject to review sampling.

Graduation MUST be recorded as a governance event.

---

## 8. Risk-Weighted Review

First-N review is necessary but not sufficient. CDP implementations SHOULD also support risk-weighted review.

Even after a decision type graduates, individual decisions SHOULD be routed to review when risk indicators exceed policy thresholds.

Risk indicators MAY include:

- high monetary value;
- legal or regulatory impact;
- impact on benefits, access, eligibility, employment, housing, healthcare, credit, or liberty;
- low model confidence;
- missing evidence;
- conflicting evidence;
- prior appeal or reversal patterns;
- unusual input distribution;
- policy drift;
- reviewer disagreement;
- affected-party contestation;
- elevated severity classification.

Example:

```json
{
  "decision_type": "customer_refund_authorization",
  "maturity_level": "sampled",
  "base_sample_rate": 0.05,
  "risk_weighted_review": true,
  "risk_thresholds": {
    "amount_usd_greater_than": 1000,
    "model_confidence_less_than": 0.80,
    "evidence_completeness_less_than": 0.90
  },
  "risk_threshold_action": "route_to_pending_review"
}
```

---

## 9. Graduation Rules

A decision type MUST NOT graduate solely because a model reports high confidence.

Graduation SHOULD require:

- completed first-N review, if applicable;
- sufficient successful reviewed decisions;
- no unresolved critical defects;
- no unresolved policy violations;
- acceptable reversal or appeal rate;
- acceptable reviewer disagreement rate;
- evidence completeness above policy threshold;
- record completeness above policy threshold;
- explicit graduation event recorded by CDP.

### 9.1 Graduation Event Example

```json
{
  "event_type": "decision_type_graduated",
  "decision_type": "vendor_invoice_auto_approval",
  "from_maturity_level": "supervised",
  "to_maturity_level": "sampled",
  "policy_id": "egp_vendor_invoice_auto_approval_v1",
  "policy_version": "1.0.0",
  "evidence": {
    "reviewed_count": 10,
    "approved_count": 10,
    "rejected_count": 0,
    "challenge_count": 0,
    "appeal_count": 0,
    "critical_defect_count": 0
  },
  "approved_by": {
    "role": "governance_owner",
    "subject_id": "user-or-service-principal-id"
  },
  "recorded_at": "2026-04-27T00:00:00Z"
}
```

---

## 10. Demotion Rules

A decision type SHOULD be demoted when evidence indicates that its current maturity level is no longer justified.

Demotion triggers MAY include:

- failed human review;
- successful appeal;
- detected harm;
- policy violation;
- drift detection;
- anomalous execution pattern;
- regulatory change;
- material model change;
- data source change;
- prompt, tool, or policy version change;
- reviewer disagreement above threshold;
- missing or corrupted records;
- dead-letter rate above threshold.

### 10.1 Demotion Event Example

```json
{
  "event_type": "decision_type_demoted",
  "decision_type": "claim_priority_reclassification",
  "from_maturity_level": "sampled",
  "to_maturity_level": "supervised",
  "reason_code": "appeal_rate_above_threshold",
  "policy_id": "egp_claim_priority_reclassification_v3",
  "policy_version": "3.2.1",
  "evidence": {
    "appeal_rate": 0.14,
    "allowed_appeal_rate": 0.05,
    "review_window_days": 30
  },
  "recorded_at": "2026-04-27T00:00:00Z"
}
```

---

## 11. Queue Message Schema

A queued execution gate message SHOULD include the following fields.

```json
{
  "message_type": "cdp.execution_gate.request",
  "schema_version": "1.0.0",
  "decision_id": "dec_01JABCDEF1234567890",
  "decision_type": "vendor_invoice_auto_approval",
  "decision_version": "1.0.0",
  "maturity_level": "supervised",
  "policy_id": "egp_vendor_invoice_auto_approval_v1",
  "policy_version": "1.0.0",
  "gate_reason": "first_n_review_required",
  "gate_action": "route_to_pending_review",
  "risk_score": 0.42,
  "requires_human_review": true,
  "requires_quorum": false,
  "requires_presence_bound_execution": false,
  "proposed_action": {
    "action_type": "approve_invoice",
    "target_system": "accounts_payable",
    "target_resource_id": "invoice_12345"
  },
  "review_context": {
    "evidence_uri": "cdp://records/dec_01JABCDEF1234567890/evidence",
    "summary": "Invoice matches purchase order and receipt; amount under threshold."
  },
  "created_at": "2026-04-27T00:00:00Z",
  "expires_at": "2026-04-30T00:00:00Z",
  "correlation_id": "corr_01JABCDEF1234567890",
  "record_required": true
}
```

---

## 12. Review Outcome Schema

Human or quorum review SHOULD produce a durable review outcome.

```json
{
  "message_type": "cdp.execution_gate.review_outcome",
  "schema_version": "1.0.0",
  "decision_id": "dec_01JABCDEF1234567890",
  "decision_type": "vendor_invoice_auto_approval",
  "review_id": "rev_01JABCDEFXYZ",
  "review_outcome": "approved",
  "reviewer": {
    "subject_id": "user_123",
    "role": "finance_controller"
  },
  "review_notes": "Approved. Evidence is complete and amount is within policy threshold.",
  "next_route": "cdp.decisions.approved_execution",
  "policy_id": "egp_vendor_invoice_auto_approval_v1",
  "policy_version": "1.0.0",
  "reviewed_at": "2026-04-27T00:00:00Z"
}
```

Allowed `review_outcome` values SHOULD include:

- `approved`
- `rejected`
- `challenge_required`
- `escalated`
- `deferred`
- `expired`
- `error`

---

## 13. Execution Behavior

A CDP executor MUST NOT execute a gated decision unless one of the following is true:

1. The Execution Gate Policy permits autonomous execution; or
2. A valid review outcome permits execution; or
3. A valid quorum outcome permits execution; or
4. A valid emergency override permits execution; or
5. A valid presence-bound execution grant permits execution, when required.

If none of these conditions is met, the executor MUST reject the execution attempt or route it to the appropriate queue.

---

## 14. Emergency Override

Emergency override MAY be supported, but MUST be tightly controlled.

An emergency override MUST include:

- reason code;
- human or quorum authorization;
- scope;
- expiration;
- affected decision IDs or decision types;
- post-execution review requirement;
- record requirement.

Emergency override MUST NOT silently graduate a decision type.

---

## 15. Agentic AI Constraints

Agentic AI systems operating under CDP MUST NOT independently graduate their own decision types.

An agent MAY recommend graduation or demotion, but the recommendation MUST be recorded and reviewed according to policy.

An agent MUST NOT bypass a queue by directly invoking execution tools when an execution gate requires review.

An agent MUST NOT treat repeated unreviewed success as governance evidence unless the applicable policy explicitly permits that evidence type.

An agent MUST NOT modify its own Execution Gate Policy unless explicitly authorized by CDP governance.

---

## 16. Record Requirements

For every gated decision, CDP MUST record:

- `decision_id`
- `decision_type`
- maturity level at time of gate evaluation
- policy ID and version
- gate evaluation result
- queue route selected
- review requirement
- reviewer or quorum identity, when applicable
- review outcome
- execution outcome
- timestamps for routing, review, execution, and recording
- correlation ID
- evidence references
- graduation or demotion impact, if any

Records SHOULD be immutable or append-only.

---

## 17. Observability Metrics

CDP implementations SHOULD expose operational and governance metrics for decision-type maturity.

Recommended metrics include:

- decisions by type;
- decisions by maturity level;
- pending review count;
- average review latency;
- approval rate;
- rejection rate;
- challenge rate;
- escalation rate;
- appeal rate;
- reversal rate;
- dead-letter rate;
- autonomous execution rate;
- sampled review rate;
- graduation events;
- demotion events;
- policy version distribution.

These metrics SHOULD be available to governance, audit, operations, and affected oversight functions.

---

## 18. Security Considerations

Queue-based execution gates introduce security obligations.

Implementations MUST protect queues from unauthorized producers and consumers.

Implementations MUST ensure that only authorized reviewers can approve gated decisions.

Implementations SHOULD sign or otherwise protect queue messages against tampering.

Implementations MUST prevent replay of stale approvals.

Implementations MUST bind review outcomes to the original decision, policy version, and execution scope.

Implementations SHOULD define expiration semantics for queued decisions and approvals.

Implementations SHOULD route malformed, expired, or unverifiable messages to a dead-letter process.

---

## 19. Privacy and Civil Rights Considerations

Some decision types may affect access to healthcare, benefits, employment, credit, housing, education, liberty, identity, or other protected interests.

For such decisions, CDP SHOULD default to `restricted` or `supervised` maturity unless policy explicitly permits otherwise.

CDP SHOULD require additional record evidence for high-impact decisions, including:

- source evidence;
- policy basis;
- adverse impact review, where applicable;
- affected-party notice, where applicable;
- contestability or appeal pathway, where applicable;
- reviewer accountability.

Automation maturity MUST NOT be used to launder illegitimate, discriminatory, or unreviewable decisions into autonomous execution.

---

## 20. Implementation Notes

### 20.1 AWS Example

An AWS implementation MAY use:

- SQS for durable queues;
- Lambda or Step Functions for orchestration;
- DynamoDB, Aurora, Redshift, or S3 for record storage;
- EventBridge for maturity events;
- IAM for producer, consumer, and reviewer authorization.

Example queue mapping:

```text
cdp.decisions.pending_review       → SQS queue for review work items
cdp.decisions.approved_execution   → SQS queue consumed by executors
cdp.decisions.rejected             → SQS queue for rejected decisions
cdp.decisions.challenge_required   → SQS queue for CDP Challenge Protocol
cdp.decisions.dead_letter          → SQS dead-letter queue
cdp.decisions.maturity_events      → EventBridge or SQS maturity event stream
```

### 20.2 Non-AWS Implementations

Equivalent implementations MAY use:

- Azure Service Bus;
- Google Pub/Sub;
- Apache Kafka;
- RabbitMQ;
- NATS JetStream;
- PostgreSQL-backed job queues;
- Redis streams, where durability requirements are satisfied.

The protocol requirement is durable, auditable routing, not any specific queue technology.

---

## 21. Example End-to-End Scenario

A CDP-enabled accounts payable system introduces a new `decision_type`:

```text
vendor_invoice_auto_approval
```

The governance owner sets the maturity level to `supervised` and requires first-N review for the first 10 decisions.

For each of the first 10 invoices:

1. The agent proposes approval.
2. CDP classifies the decision type.
3. CDP evaluates the Execution Gate Policy.
4. The decision is routed to `cdp.decisions.pending_review`.
5. A finance controller reviews the evidence.
6. If approved, the decision is routed to `cdp.decisions.approved_execution`.
7. The executor approves the invoice in the target system.
8. CDP records the review and execution evidence.
9. CDP updates maturity evidence.

After 10 successful reviewed decisions and no policy defects, the decision type may graduate to `sampled`, where 5% of future decisions are reviewed unless risk thresholds require additional review.

If an appeal, defect, or anomalous pattern appears, the decision type may be demoted back to `supervised` or `restricted`.

---

## 22. Design Principle

This RFC establishes the following CDP design principle:

> Automation is not a switch.  
> Automation is a governed maturity state.

A decision type earns autonomy through policy, evidence, review, record, and continued accountability.

---

## 23. Open Questions

Future RFCs MAY define:

- canonical maturity scoring formulas;
- standard risk taxonomy;
- minimum review thresholds by domain;
- model-change demotion rules;
- regulatory mappings for high-impact decision types;
- standard queue message envelopes;
- reviewer credential and role binding;
- integration with Presence-Bound Execution Authority;
- appeal and reversal feedback into maturity state.

---

## 24. Compatibility

This RFC is backward-compatible with the CDP lifecycle.

It does not replace RFC-CDP-007 Execute Protocol. It adds a maturity-aware gate between legitimate decision approval and executable action.

Existing CDP implementations MAY adopt this RFC incrementally by adding:

1. `decision_type` classification;
2. execution gate policy lookup;
3. pending review queue;
4. review outcome record;
5. maturity event record.

---

## 25. Summary

This RFC adds queue-based execution gates and maturity states to CDP.

It allows CDP to say:

- new decision types require supervision;
- trusted decision types may graduate;
- risky decisions can always be pulled back into review;
- automation remains accountable over time;
- queues provide a durable, vendor-neutral mechanism for human-in-the-loop and human-over-the-loop governance.

The resulting pattern is best understood as:

> Canary deployment for decisions.  
> Constitutional apprenticeship for automation.

