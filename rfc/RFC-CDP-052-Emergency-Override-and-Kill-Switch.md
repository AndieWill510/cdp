# RFC-CDP-052 — Emergency Override and Kill Switch

Author: Kevin “Andie” Williams  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: May 3, 2026  
Depends On: RFC-CDP-001, RFC-CDP-010, RFC-CDP-032, RFC-CDP-046, RFC-CDP-047, RFC-CDP-048, RFC-CDP-050, RFC-CDP-051, RFC-CDP-061  
Updates: RFC-CDP-046, RFC-CDP-050, RFC-CDP-051

## Abstract

This RFC defines Emergency Override and Kill Switch controls for the Constitutional Decision Plane (CDP).

Emergency Override allows a CDP implementation to temporarily bypass, defer, or accelerate one or more ordinary governance steps only under explicit, scoped, time-bounded, recorded, and reviewable emergency conditions.

Kill Switch controls allow a CDP implementation to pause, halt, revoke, quarantine, or terminate execution when continuing action would be unsafe, unauthorized, illegitimate, harmful, out of scope, contested, or inconsistent with policy.

Emergency power is not an escape from governance. Emergency power is governed power under exceptional conditions.

---

## 1. Purpose

This RFC answers:

- when emergency override may be invoked;
- who may invoke emergency override;
- what emergency authority must include;
- how emergency action is scoped and time-bounded;
- how kill switches pause, halt, revoke, quarantine, or terminate execution;
- how override and kill-switch events are recorded;
- when post-hoc review is required;
- how abuse of emergency authority is detected;
- how emergency action produces learning without normalizing bypass.

---

## 2. Core Principle

Emergency action may be necessary.

Emergency action MUST NOT become ambient authority.

Every emergency override MUST be scoped, time-bounded, attributable, recorded, challenge-aware, and subject to post-hoc review.

Every kill-switch action MUST preserve enough record to reconstruct why action was stopped, by whom, under what authority, and with what downstream effects.

---

## 3. Relationship to Existing RFCs

### 3.1 RFC-CDP-046 Execute Protocol

Execute governs bounded enactment.

This RFC defines emergency paths that may pause, block, accelerate, or terminate execution.

### 3.2 RFC-CDP-050 Decision-Type Maturity and Queued Execution Gates

Execution gates route immature or risky decision types to review.

This RFC defines when emergency conditions may override queue routing or force a kill-switch intervention.

### 3.3 RFC-CDP-051 Presence-Bound Execution Authority

Presence-Bound Execution Authority defines Presence Grants and time-bounded execution authority.

This RFC defines emergency presence requirements, emergency presence expiry, and post-hoc review of emergency grants.

### 3.4 RFC-CDP-032 Authority and Delegation Model

Emergency authority is a special authority type.

This RFC defines scope, decay, revocation, and record requirements for emergency authority.

### 3.5 RFC-CDP-061 Schema Drift and Context Preservation

Schema drift may make execution unsafe even when prior records are valid.

This RFC defines schema drift as a possible kill-switch trigger.

---

## 4. Terminology

### 4.1 Emergency Override

An **Emergency Override** is a time-bounded, policy-scoped authorization to bypass, defer, accelerate, or alter ordinary governance steps under emergency conditions.

Emergency Override MUST NOT erase skipped steps. It creates a duty for post-hoc record, review, and learning.

### 4.2 Kill Switch

A **Kill Switch** is a governed mechanism that halts, pauses, quarantines, revokes, disables, or terminates a decision, execution, agent, tool, credential, queue, workflow, or target-system action.

### 4.3 Pause

A **Pause** temporarily stops progress while preserving state for possible continuation.

### 4.4 Halt

A **Halt** stops execution and requires explicit reauthorization before continuation.

### 4.5 Quarantine

**Quarantine** isolates a decision, actor, artifact, queue item, tool, model, credential, or execution target to prevent propagation or further action.

### 4.6 Termination

**Termination** ends an execution path and prevents continuation under the same authorization.

### 4.7 Emergency Authority

**Emergency Authority** is scoped authority to invoke an Emergency Override or Kill Switch under defined policy conditions.

Emergency Authority MUST be shorter-lived and more tightly scoped than ordinary authority.

### 4.8 Post-Hoc Review

**Post-Hoc Review** is mandatory review after an emergency action to determine whether the action was justified, correctly scoped, adequately recorded, and whether repair, rollback, policy update, or learning is required.

---

## 5. Emergency Conditions

Emergency Override MAY be permitted when delay would create unacceptable risk of:

- imminent harm to people;
- irreversible rights-affecting action;
- safety-critical failure;
- legal or regulatory breach;
- security incident;
- production outage with material impact;
- unauthorized data exposure;
- destructive execution;
- model or agent runaway behavior;
- credential compromise;
- active exploitation;
- blocked humanitarian, safety, or protective action;
- failure to act that would itself cause serious harm.

Emergency Override MUST NOT be used merely for convenience, deadline pressure, institutional embarrassment, public relations, avoidance of challenge, avoidance of affected-party review, or bypassing dissent.

---

## 6. Emergency Override Modes

CDP implementations SHOULD distinguish the following modes.

| Mode | Meaning |
|---|---|
| `bypass` | Temporarily skip one or more ordinary gates. |
| `defer` | Defer one or more required reviews until after action. |
| `accelerate` | Shorten review or queue timing while preserving required checks. |
| `escalate` | Route immediately to higher authority or quorum. |
| `authorize_once` | Permit a single bounded action. |
| `limited_window` | Permit bounded actions for a short emergency window. |
| `pause` | Temporarily stop execution. |
| `halt` | Stop execution pending reauthorization. |
| `quarantine` | Isolate affected object or capability. |
| `terminate` | End execution and prevent continuation. |

---

## 7. Emergency Override Object

An Emergency Override SHOULD be represented as:

```json
{
  "emergency_override_id": "eo_20260503_001",
  "decision_id": "decision_123",
  "mode": "bypass | defer | accelerate | escalate | authorize_once | limited_window",
  "emergency_type": "safety | security | legal | regulatory | operational | humanitarian | data_exposure | runaway_agent | other",
  "invoked_by": "actor_ref",
  "authority_ref": "authority_grant_or_presence_ref",
  "basis": "string",
  "skipped_or_deferred_controls": [],
  "scope": {
    "target_systems": [],
    "actions_allowed": [],
    "actions_disallowed": [],
    "data_domains": [],
    "environment": "dev | test | prod | regulated | public",
    "maximum_operations": 1
  },
  "validity": {
    "issued_at": "timestamp",
    "expires_at": "timestamp",
    "single_use": true
  },
  "challenge_state": {
    "active_challenges": [],
    "emergency_challenge_allowed": true,
    "post_hoc_challenge_required": true
  },
  "post_hoc_review": {
    "required": true,
    "due_at": "timestamp",
    "review_authority_refs": []
  },
  "record_refs": [],
  "status": "active | expired | used | revoked | rejected | under_review | ratified | condemned",
  "metadata": {}
}
```

---

## 8. Kill Switch Object

A Kill Switch action SHOULD be represented as:

```json
{
  "kill_switch_id": "ks_20260503_001",
  "decision_id": "decision_123",
  "target_type": "decision | execution | queue | agent | model | tool | credential | workflow | target_system | dataset | other",
  "target_ref": "target_id",
  "action": "pause | halt | quarantine | revoke | disable | terminate",
  "trigger": "manual | policy | anomaly | challenge | authority_failure | presence_failure | schema_drift | security | safety | repair | other",
  "invoked_by": "actor_or_system_ref",
  "authority_ref": "authority_grant_ref",
  "reason": "string",
  "scope": {
    "environment": "dev | test | prod | regulated | public",
    "affected_systems": [],
    "affected_actions": [],
    "blast_radius": "local | domain | systemic"
  },
  "effects": {
    "queues_paused": [],
    "tokens_revoked": [],
    "agents_disabled": [],
    "executions_halted": [],
    "artifacts_quarantined": []
  },
  "review": {
    "review_required": true,
    "due_at": "timestamp",
    "review_authority_refs": []
  },
  "status": "active | lifted | partially_lifted | superseded | expired | under_review",
  "record_refs": [],
  "created_at": "timestamp"
}
```

---

## 9. Required Checks Before Emergency Override

Before allowing Emergency Override, CDP SHOULD evaluate:

1. Is there a credible emergency condition?
2. Who is invoking emergency authority?
3. Is emergency authority valid and in scope?
4. What ordinary controls are being bypassed, deferred, or accelerated?
5. What is the least intrusive emergency action?
6. What is the time window?
7. What is the maximum allowed scope?
8. What active challenges exist?
9. What affected-party or repair claims are implicated?
10. What post-hoc review is required?
11. What record will be produced?

Emergency Override MUST fail closed if emergency authority cannot be established, unless the kill-switch path is needed to prevent imminent harm.

---

## 10. Kill Switch Triggers

A Kill Switch SHOULD be available for:

- authority failure;
- presence failure;
- active blocking challenge;
- schema drift that makes execution unsafe;
- execution outside scope;
- unexpected blast radius;
- runaway agent behavior;
- model or tool malfunction;
- credential compromise;
- unauthorized data access;
- repair or sovereignty claim conflict;
- affected-party review requirement discovered late;
- policy violation;
- legal or regulatory risk;
- safety risk;
- human override;
- quorum withdrawal.

Kill Switch activation SHOULD be easier than Emergency Override.

Stopping harm should have lower friction than expanding power.

---

## 11. Post-Hoc Review Requirements

Every Emergency Override SHOULD produce Post-Hoc Review.

Post-Hoc Review SHOULD determine:

- whether emergency condition was valid;
- whether invoked authority was valid;
- whether scope was respected;
- whether skipped controls were justified;
- whether affected parties were harmed;
- whether repair is required;
- whether rollback or compensation is required;
- whether policy must change;
- whether the emergency path was abused;
- whether learning artifacts are required.

Post-Hoc Review status SHOULD use:

```text
pending
under_review
ratified
ratified_with_reservations
condemned
repair_required
policy_update_required
insufficient_record
```

---

## 12. Abuse and Anti-Pattern Detection

CDP implementations SHOULD detect emergency abuse patterns.

Anti-patterns include:

- repeated emergency overrides for ordinary workflow;
- emergency override used to bypass dissent;
- emergency override used to bypass affected-party review;
- emergency override used to avoid embarrassment or delay;
- broad emergency authority with no expiration;
- emergency action without record;
- emergency action without post-hoc review;
- kill switch lifted without review;
- emergency path used to normalize permanent authority expansion.

Emergency abuse SHOULD trigger Challenge, Record, Learn, and possibly Repair.

---

## 13. Interaction with Queues

Emergency Override MAY alter queue behavior only within scope.

Permitted queue actions MAY include:

- priority escalation;
- immediate review routing;
- temporary pause;
- quarantine;
- dead-letter routing;
- single-use bypass;
- limited-window processing.

Emergency Override MUST NOT silently convert a gated decision type into autonomous execution.

---

## 14. Interaction with Presence

High-risk emergency execution SHOULD require emergency presence unless delay would itself create imminent harm.

Emergency presence SHOULD be:

- explicit;
- time-bounded;
- scoped;
- recorded;
- non-replayable;
- subject to post-hoc review.

Emergency presence MUST NOT become standing authority.

---

## 15. Interaction with Repair and Sovereignty

Emergency Override MUST NOT erase repair or sovereignty claims.

If emergency action affects a repair agenda, affected party, sovereignty claim, restricted knowledge, or breach record, the override record SHOULD include:

- affected repair refs;
- affected sovereignty claim refs;
- why delay was unsafe;
- how review will occur;
- what repair or compensation may be required;
- what was done to minimize harm.

Emergency Override MUST NOT be used to avoid repair obligations.

---

## 16. Record Requirements

CDP implementations SHOULD record:

- emergency condition;
- invoking actor;
- authority basis;
- skipped or deferred controls;
- scope;
- start and expiration time;
- actions taken;
- active challenges;
- kill-switch events;
- queue changes;
- presence grants;
- affected parties;
- repair or sovereignty implications;
- post-hoc review outcome;
- learning artifacts.

Emergency records SHOULD be tamper-evident where feasible.

---

## 17. Learning Hooks

Emergency Override and Kill Switch events SHOULD trigger Learn when:

- override is invoked;
- kill switch is activated;
- post-hoc review condemns or qualifies emergency action;
- emergency abuse pattern is detected;
- repair is required;
- rollback or compensation is required;
- repeated emergency action indicates bad policy, bad design, or inadequate staffing;
- schema drift or authority decay caused the emergency.

Learning artifacts MAY include:

- policy update;
- queue rule update;
- authority model update;
- presence requirement update;
- kill-switch trigger update;
- repair obligation;
- training guidance;
- incident precedent.

Learning MUST NOT normalize emergency bypass as ordinary governance.

---

## 18. Minimal Compliance

A minimal CDP implementation SHOULD support:

- emergency override record;
- kill-switch record;
- emergency authority reference;
- scope;
- expiration;
- skipped-control list;
- post-hoc review requirement;
- pause or halt action;
- record of lifted or terminated kill switch;
- learning hook.

A minimal implementation MUST NOT allow emergency override without record.

---

## 19. Summary

Emergency power is governed power under exceptional conditions.

Emergency Override allows temporary, scoped, time-bounded deviation from ordinary governance only when delay would create unacceptable risk.

Kill Switch controls allow CDP to stop harm quickly when authority, presence, policy, safety, repair, or schema conditions fail.

Stopping harm should have lower friction than expanding power.

Emergency does not erase governance. Emergency creates a debt to record, review, repair, and learn.
