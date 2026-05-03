# RFC-CDP-012: Presence-Bound Execution Authority

**Status:** Draft 0.1  
**Category:** Standards Track  
**Author:** Andie Williams / CDP Contributors  
**Created:** 2026-04-27  
**Recovered / Reconstructed:** 2026-05-03  
**Original recovered title:** `RFC-CDP-011-Presence-Bound-Execution-Authority.md`  
**Renumbering note:** Renumbered to RFC-CDP-012 to avoid collision with RFC-CDP-011 Covenant AIITL.  
**Updates:** RFC-CDP-007 Execute Protocol; RFC-CDP-008 Record Protocol  
**Depends on:** RFC-CDP-001, RFC-CDP-002, RFC-CDP-003, RFC-CDP-004, RFC-CDP-005, RFC-CDP-006, RFC-CDP-008  

---

## 1. Abstract

This RFC defines **Presence-Bound Execution Authority** for the Constitutional Decision Plane (CDP). Presence-Bound Execution Authority ensures that consequential decisions are not merely approved in the abstract, but are executed only under verified, time-bounded, policy-scoped human or institutional authority.

This module introduces a formal execution-control primitive: the **Presence Grant**. A Presence Grant binds a proposed execution to one or more authorized actors, a legitimacy record, a time window, an execution scope, and a non-replayable authority token.

CDP determines whether a decision is legitimate. Presence-Bound Execution Authority determines whether the system is presently authorized to act on that decision.

---

## 2. Motivation

Agentic AI systems increasingly possess the ability to recommend, initiate, modify, trigger, or complete actions across software, financial, operational, administrative, legal, healthcare, and government systems.

Traditional access control models often rely on static or reusable authority mechanisms:

- API keys
- service accounts
- long-lived OAuth sessions
- stored credentials
- role-based permissions
- standing approvals
- queue-based automation
- unattended execution runners

These mechanisms answer:

> Does this principal have access?

They do not sufficiently answer:

> Is this specific action presently authorized, legitimate, scoped, contested if necessary, and bound to accountable authority?

Presence-Bound Execution Authority closes this gap.

---

## 3. Design Principle

CDP separates **decision legitimacy** from **execution authority**.

Execution requires both:

1. **Legitimacy:** the decision has passed the required CDP governance path.
2. **Presence:** the execution is authorized by live, time-bounded, policy-scoped authority.

A decision may be legitimate but not executable. A present actor may be authorized but not allowed to execute an illegitimate decision.

---

## 4. Relationship to Existing CDP RFCs

### 4.1 RFC-CDP-007 Execute Protocol

This RFC extends Execute by requiring authority checks for controlled, consequential, privileged, irreversible, externally visible, or materially impactful actions.

The Execute Protocol MUST NOT complete a controlled action unless it can reference a valid Presence Grant.

### 4.2 RFC-CDP-008 Record Protocol

Every Presence Grant, Presence Challenge, authority token, quorum result, exception, failure, override, and execution attempt MUST be recorded.

The record MUST preserve enough detail to reconstruct who authorized execution, under which policy, during what window, for which decision, for which target, under which constraints, and with what outcome.

### 4.3 RFC-CDP-006 Legitimize Protocol

The Legitimize Protocol establishes that a decision may proceed. Presence-Bound Execution Authority establishes that a specific execution instance may occur now.

Legitimacy is durable within policy limits. Presence is ephemeral by design.

---

## 5. Terminology

### 5.1 Presence

**Presence** is a verified condition indicating that an authorized human, group, institution, process, or accountable control node is actively participating in, supervising, or authorizing a specific execution.

Presence MAY include interactive confirmation, cryptographic proof, device-bound confirmation, quorum approval, privileged session activation, institutional attestation, or other policy-approved signals.

Presence MUST be time-bounded.

### 5.2 Presence Grant

A **Presence Grant** is a signed, non-replayable, policy-scoped authorization object that permits a specific execution action or class of actions for a limited time.

A Presence Grant does not create legitimacy. It permits execution of an already-legitimized decision.

### 5.3 Presence Token

A **Presence Token** is an ephemeral credential derived from a Presence Grant and passed to the execution substrate.

Presence Tokens MUST be non-replayable and SHOULD be single-use for high-risk actions.

### 5.4 Quorum Presence

**Quorum Presence** requires multiple distinct authorized actors or roles to approve or participate in an execution.

Quorum Presence SHOULD be required for high-impact, irreversible, privileged, regulated, or contested actions.

### 5.5 Authority Decay

**Authority Decay** means that execution authority loses validity over time, after context changes, after policy changes, after decision state changes, or after failed execution attempts.

CDP assumes authority decays unless explicitly renewed.

---

## 6. Normative Requirements

A CDP-compliant execution system:

1. MUST verify that the underlying decision has a valid legitimacy record.
2. MUST classify execution risk before execution.
3. MUST require a Presence Grant for controlled actions.
4. MUST bind the Presence Grant to a specific decision or decision family.
5. MUST bind the Presence Grant to an execution scope.
6. MUST bind the Presence Grant to an expiration time.
7. MUST record the Presence Grant and execution outcome.
8. MUST reject stale, replayed, malformed, or scope-incompatible Presence Tokens.
9. MUST support policy-defined quorum rules.
10. MUST provide an auditable reason when execution is denied.

### 6.1 Controlled Action Requirement

A Presence Grant is REQUIRED when an action is classified as privileged, irreversible, externally visible, financially material, legally material, safety-critical, production-impacting, identity-impacting, data-destructive, policy-changing, model-changing, rights-affecting, contested, escalated, or regulated.

### 6.2 Non-Replay Requirement

Presence Tokens MUST NOT be reusable outside their original scope.

For high-risk actions, Presence Tokens MUST be single-use.

### 6.3 Scope Requirement

A Presence Grant MUST declare its execution scope.

At minimum, the scope SHOULD include:

- action type
- target system
- target resource
- data domain
- environment
- actor or agent permitted to execute
- maximum duration
- maximum number of operations
- rollback or compensation expectation
- allowed and disallowed tools or APIs

Execution MUST fail closed if the requested action exceeds the grant scope.

### 6.4 Expiration Requirement

Every Presence Grant MUST expire.

Expiration MAY be based on wall-clock time, session termination, completion of action, quorum withdrawal, policy change, decision state change, failed challenge, failed execution, risk score change, or environmental change.

High-risk grants SHOULD expire within minutes unless policy explicitly permits a longer window.

### 6.5 Challenge Preservation Requirement

A Presence Grant MUST NOT override an active Challenge unless policy explicitly permits emergency override.

If a Challenge exists, execution MUST verify that the challenge was resolved, adjudicated, withdrawn, or emergency override was invoked and recorded.

---

## 7. Presence Grant Object

A Presence Grant SHOULD be represented as a signed structured object.

Required fields SHOULD include:

- `presence_grant_id`
- `decision_id`
- `legitimacy_record_id`
- `grant_type`
- `risk_level`
- `authorized_subjects`
- `execution_scope`
- `issued_at`
- `expires_at`
- `policy_ref`
- `nonce`
- `signature`

---

## 8. Emergency Override

Emergency override MAY be permitted by policy, but MUST be recorded as an exceptional execution path.

Emergency override records MUST include:

- invoking actor
- asserted emergency condition
- skipped or deferred governance steps
- expiration time
- affected decision
- affected execution target
- post-execution review requirement

Emergency override MUST NOT erase the requirement for later Record, Review, and Learn stages.

---

## 9. Agentic AI Considerations

Agentic AI systems MUST NOT be treated as inherently authorized merely because they possess a tool, credential, instruction, memory, or delegated task.

An agent MAY request execution, prepare execution context, recommend a required Presence Grant, and execute after receiving a valid Presence Token.

An agent MUST NOT mint its own Presence Grant for a controlled action unless it is acting as a policy-governed control node whose authority is independently authorized, recorded, and bounded.

---

## 10. Constitutional Interpretation

Presence-Bound Execution Authority is the CDP equivalent of requiring a warrant, countersignature, quorum, or live commission before power is exercised.

This module does not decide guilt, truth, validity, policy, or legitimacy. Those questions are handled by prior CDP stages.

It asks:

> Even if this decision is legitimate, who is presently authorized to execute it, under what limits, and with what record?

---

## 11. Implementation Guidance

A minimal implementation MAY include:

- a risk classifier;
- a Presence Grant issuer;
- a token minting service;
- a policy evaluator;
- an execution gateway;
- a record writer;
- a replay cache;
- an expiration scheduler.

A mature implementation SHOULD include quorum workflows, cryptographic signatures, tamper-evident records, policy version pinning, challenge-state integration, emergency override paths, post-execution review, anomaly detection, role-separation enforcement, and integration with enterprise IAM/PAM systems.

---

## 12. Open Questions

1. Should Presence Grants be represented as JWTs, SDS-style envelopes, W3C Verifiable Credentials, or a CDP-native signed object?
2. Should emergency override require later adjudication by default?
3. How should human coercion or approval fatigue be detected?
4. How should quorum rules differ across legal, medical, financial, defense, and enterprise domains?
5. Should Presence Tokens be visible to agents, or only to execution gateways?
6. Should some Presence Grants be revocable by challengers after issuance?
7. How should policy handle long-running executions that outlive the original Presence window?

---

## 13. Summary

Presence-Bound Execution Authority prevents agentic AI systems from converting ambient access into action.

It makes execution authority explicit, scoped, temporary, policy-bound, challenge-aware, quorum-capable, non-replayable, and auditable.

CDP governs the decision. Presence-Bound Execution governs the moment of action.
