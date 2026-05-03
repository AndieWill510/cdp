# RFC-CDP-007A: Decision-Type Maturity and Queued Execution Gates

**Status:** Draft  
**Category:** Standards Track  
**Extends:** RFC-CDP-007 Execute Protocol; RFC-CDP-008 Record Protocol; RFC-CDP-009 Learn Protocol  
**Author:** CDP Project  
**Created:** 2026-04-27  
**Recovered / Reconstructed:** 2026-05-03  
**Filename:** `RFC-CDP-007A-Decision-Type-Maturity-and-Queued-Execution-Gates.md`

---

## Abstract

This RFC defines a CDP extension for **Decision-Type Maturity** and **Queued Execution Gates**.

The purpose of this extension is to prevent new, unproven, or risky classes of decisions from being automatically executed without supervised review. Instead of treating automation as a binary state, CDP SHALL treat each `decision_type` as a governable object that can mature through evidence, review, successful execution, and recorded outcomes.

This RFC introduces a vendor-neutral queue-based execution pattern in which decisions may be routed to review, challenge, approval, rejection, execution, or dead-letter queues according to policy. Cloud implementations MAY use AWS SQS, Azure Service Bus, Google Pub/Sub, Kafka, RabbitMQ, NATS, PostgreSQL-backed queues, Redis streams, or other durable mechanisms. No vendor-specific implementation is required.

> Agentic systems MUST NOT be trusted all at once.  
> Decision types SHOULD mature through governed experience.

---

## 1. Motivation

Agentic AI systems can produce decisions, recommendations, or executable actions at scale. Without gating, a new class of automated decision may move directly from proposal to execution before humans understand its failure modes, boundary conditions, or policy implications.

Traditional human-in-the-loop patterns often focus on individual actions. That is useful but incomplete. CDP also requires governance over the **type of decision being automated**.

When a system encounters a new or insufficiently proven `decision_type`, execution SHOULD be delayed, queued, reviewed, and recorded until that decision type earns greater autonomy.

This is canary deployment for decisions.

---

## 2. Relationship to Existing CDP RFCs

### 2.1 RFC-CDP-007 Execute Protocol

This RFC extends Execute by adding an **Execution Gate Policy** evaluation before an approved decision may execute.

An execution gate determines whether a decision:

- MAY execute automatically;
- MUST be queued for human review;
- MUST be challenged;
- MUST receive quorum approval;
- MUST be blocked;
- MUST be routed to exception/dead-letter handling.

### 2.2 RFC-CDP-008 Record Protocol

This RFC extends Record by requiring durable evidence of:

- gate evaluation;
- queue routing;
- reviewer identity or role;
- approval, rejection, escalation, challenge, or deferral outcome;
- maturity level at time of decision;
- graduation or demotion events;
- policy version used for gate evaluation.

### 2.3 RFC-CDP-009 Learn Protocol

This RFC extends Learn by allowing CDP to update decision-type maturity based on recorded outcomes, human reviews, defects, reversals, appeals, and drift signals.

Learning MUST NOT silently increase autonomy without recordable policy support.

---

## 3. Terminology

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

Maturity is not model confidence alone. It is a governance state based on policy, evidence, review history, failure history, and risk.

### 3.3 Execution Gate

An execution gate is a policy-controlled checkpoint between a legitimate decision and an executable action.

A decision may be validly proposed, challenged, tested, adjudicated, and legitimated, yet still be prevented from execution if its decision type is immature, risky, disputed, or outside policy bounds.

### 3.4 Durable Queue

A durable queue is a reliable routing mechanism that preserves a decision or execution request until it is processed, reviewed, retried, rejected, expired, or escalated.

### 3.5 Graduation

Graduation is a policy-authorized maturity increase that permits a decision type to move to lower-friction execution.

### 3.6 Demotion

Demotion is a maturity decrease caused by policy changes, adverse outcomes, drift, failed review, appeal, defect detection, or other governance signals.

---

## 4. Maturity Levels

CDP implementations SHOULD support the following maturity levels.

| Level | Meaning | Default execution behavior |
|---|---|---|
| `experimental` | New or unproven decision type | Queue every decision for review |
| `supervised` | Early governed use | Require review for first N decisions or until threshold is met |
| `sampled` | Mostly trusted within bounds | Auto-execute most decisions; sample or route risky cases for review |
| `autonomous` | Trusted within defined policy limits | Auto-execute if all policy checks pass |
| `restricted` | Sensitive, high-risk, disputed, or legally constrained | Always require human approval, quorum, or presence-bound authorization |
| `blocked` | Not permitted to execute | Reject or route to exception process |

---

## 5. Execution Gate Policy

An Execution Gate Policy SHOULD include:

- `decision_type`
- `maturity_level`
- first-N review requirements
- success thresholds for graduation
- failure thresholds for demotion
- sampling rules after graduation
- reviewer role requirements
- quorum requirements
- presence-bound authorization requirements
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

Reference flow:

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

Logical queues MAY include:

```text
cdp.decisions.pending_review
cdp.decisions.approved_execution
cdp.decisions.rejected
cdp.decisions.challenge_required
cdp.decisions.deferred
cdp.decisions.dead_letter
cdp.decisions.maturity_events
```

---

## 7. First-N Review

A CDP implementation SHOULD support first-N review for new or newly modified decision types.

First-N review means that the first `N` decisions of a given `decision_type` MUST be manually reviewed before execution.

Graduation MUST be recorded as a governance event.

---

## 8. Risk-Weighted Review

Even after graduation, individual decisions SHOULD be routed to review when risk indicators exceed policy thresholds.

Risk indicators MAY include:

- high monetary value;
- legal or regulatory impact;
- benefits, access, eligibility, employment, housing, healthcare, credit, or liberty impact;
- low model confidence;
- missing or conflicting evidence;
- prior appeal or reversal patterns;
- unusual input distribution;
- policy drift;
- reviewer disagreement;
- affected-party contestation.

---

## 9. Graduation Rules

A decision type MUST NOT graduate solely because a model reports high confidence.

Graduation SHOULD require:

- completed first-N review;
- sufficient successful reviewed decisions;
- no unresolved critical defects;
- no unresolved policy violations;
- acceptable reversal or appeal rate;
- acceptable reviewer disagreement rate;
- evidence completeness above policy threshold;
- record completeness above policy threshold;
- explicit graduation event recorded by CDP.

---

## 10. Demotion Rules

A decision type SHOULD be demoted when evidence indicates that its current maturity level is no longer justified.

Demotion triggers MAY include:

- successful appeal;
- policy violation;
- material defect;
- harmful outcome;
- new legal or regulatory requirement;
- evidence drift;
- model change;
- data distribution shift;
- missing record evidence;
- reviewer disagreement above threshold.

Demotion MUST be recorded.

---

## 11. Compatibility

This RFC is backward-compatible with the CDP lifecycle. It does not replace RFC-CDP-007. It adds a maturity-aware gate between legitimate decision approval and executable action.

---

## 12. Summary

Automation is not a switch. Automation is a governed maturity state.

A decision type earns autonomy through policy, evidence, review, record, and continued accountability.