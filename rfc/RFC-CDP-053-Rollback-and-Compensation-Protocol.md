# RFC-CDP-053 — Rollback and Compensation Protocol

Author: Kevin “Andie” Williams  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: May 3, 2026  
Depends On: RFC-CDP-001, RFC-CDP-010, RFC-CDP-032, RFC-CDP-046, RFC-CDP-047, RFC-CDP-048, RFC-CDP-051, RFC-CDP-052, RFC-CDP-061, RFC-CDP-071, RFC-CDP-072, RFC-CDP-073, RFC-CDP-074  
Updates: RFC-CDP-046, RFC-CDP-051, RFC-CDP-052

## Abstract

This RFC defines the Rollback and Compensation Protocol for the Constitutional Decision Plane (CDP).

Rollback attempts to reverse, undo, pause, restore, or revert an executed action. Compensation addresses harm or loss that cannot be fully reversed. Mitigation reduces ongoing or future harm when neither rollback nor full compensation is immediately available.

CDP MUST distinguish successful execution from safe execution, and safe execution from repair. When a governed action causes harm, exceeds authority, violates scope, produces unintended effects, or becomes illegitimate due to new evidence or context, CDP needs a structured way to reverse, compensate, mitigate, record, review, and learn.

---

## 1. Purpose

This RFC answers:

- when rollback is required or recommended;
- when compensation is required or recommended;
- how rollback differs from compensation and mitigation;
- who may request or authorize rollback;
- how rollback interacts with presence, emergency override, repair, and sovereignty claims;
- what must be recorded;
- how affected-party review applies;
- how rollback failure is handled;
- how rollback and compensation produce learning.

---

## 2. Core Principle

Execution is not the end of governance.

If action can cause harm, CDP MUST preserve the ability to pause, reverse, compensate, mitigate, review, repair, and learn.

Rollback is preferred when reversal is possible and safe.

Compensation is required when reversal is impossible, incomplete, harmful, or insufficient.

Mitigation is required when ongoing or future harm must be reduced.

---

## 3. Relationship to Existing RFCs

### 3.1 RFC-CDP-046 Execute Protocol

Execute governs bounded enactment.

This RFC defines how executed or executing actions may be reversed, compensated, mitigated, or repaired.

### 3.2 RFC-CDP-051 Presence-Bound Execution Authority

High-impact rollback or compensation may require its own Presence Grant.

Presence for the original action MUST NOT be assumed sufficient for rollback unless policy explicitly allows it.

### 3.3 RFC-CDP-052 Emergency Override and Kill Switch

Kill Switch may pause or halt action. This RFC defines what happens after pause or halt when reversal, compensation, or mitigation is required.

### 3.4 RFC-CDP-071 through RFC-CDP-074 Repair RFCs

Rollback and compensation may produce repair obligations.

Affected-party review, anti-erasure, and sovereignty claims MUST be preserved when implicated.

### 3.5 RFC-CDP-061 Schema Drift and Context Preservation

Schema drift may reveal that a prior execution was valid under obsolete context but illegitimate or harmful under current context.

This RFC defines rollback and compensation response paths for such cases.

---

## 4. Terminology

### 4.1 Rollback

**Rollback** is an attempt to reverse, undo, restore, revert, or nullify an executed action or its effects.

### 4.2 Compensation

**Compensation** is an action intended to address harm, loss, breach, or burden that cannot be fully reversed.

Compensation MAY include restoration, payment, apology, service correction, policy change, access correction, land/resource return, record correction, operational remedy, or other appropriate repair.

### 4.3 Mitigation

**Mitigation** is an action that reduces ongoing or future harm when rollback or full compensation is not immediately available.

### 4.4 Restoration

**Restoration** is a rollback or compensation action intended to restore a prior state, right, access, record, relationship, or condition.

### 4.5 Irreversible Action

An **Irreversible Action** is an action that cannot be fully undone.

Irreversible actions require heightened execution controls and SHOULD require rollback or compensation planning before execution.

### 4.6 Rollback Plan

A **Rollback Plan** is a structured plan describing how an execution can be reversed, paused, restored, or compensated if it fails or causes harm.

### 4.7 Compensation Plan

A **Compensation Plan** is a structured plan describing how harm will be addressed when rollback is impossible, incomplete, or insufficient.

---

## 5. Rollback Triggers

Rollback SHOULD be considered when:

- execution exceeded scope;
- authority was invalid, stale, revoked, or decayed;
- presence was invalid or missing;
- active challenge was ignored;
- execution caused unintended harm;
- policy was violated;
- target system behavior differed from expectation;
- schema drift invalidated the execution context;
- affected-party review identifies harm;
- sovereignty claim was ignored;
- emergency override was condemned or qualified in post-hoc review;
- completion evidence is contested;
- execution result is materially incorrect;
- legal, regulatory, safety, or ethical requirements demand reversal.

---

## 6. Compensation Triggers

Compensation SHOULD be considered when:

- rollback is impossible;
- rollback is incomplete;
- rollback would cause additional harm;
- delay caused harm;
- exposure, loss, or breach has already occurred;
- affected-party review identifies insufficient restoration;
- repair claim requires remedy beyond reversal;
- institutional action created burden, loss, exclusion, or misclassification;
- sovereignty claim or cultural handling violation cannot be undone;
- emergency action was necessary but harmful;
- execution created irreversible material effects.

---

## 7. Mitigation Triggers

Mitigation SHOULD be considered when:

- harm is ongoing;
- rollback requires time;
- compensation requires review;
- affected systems remain unsafe;
- credentials, agents, models, queues, or tools remain at risk;
- a repair process is unresolved;
- evidence is incomplete but risk is credible;
- sovereignty or affected-party review is pending.

---

## 8. Rollback Plan Object

A Rollback Plan SHOULD be represented as:

```json
{
  "rollback_plan_id": "rbp_20260503_001",
  "decision_id": "decision_123",
  "execution_ref": "execution_456",
  "plan_type": "rollback | restoration | mitigation | compensation | hybrid",
  "created_by": "actor_or_system_ref",
  "authority_ref": "authority_grant_ref",
  "scope": {
    "target_systems": [],
    "affected_records": [],
    "affected_parties": [],
    "repair_agenda_refs": [],
    "sovereignty_claim_refs": []
  },
  "preconditions": [],
  "steps": [
    {
      "step_id": "step_001",
      "action": "string",
      "target": "string",
      "expected_effect": "string",
      "risk": "low | medium | high | critical",
      "requires_presence": false,
      "requires_review": false
    }
  ],
  "verification": {
    "required": true,
    "method": "string",
    "evidence_required": []
  },
  "fallback": {
    "compensation_plan_required": true,
    "mitigation_required": true
  },
  "status": "draft | approved | active | completed | failed | superseded",
  "record_refs": [],
  "metadata": {}
}
```

---

## 9. Compensation Plan Object

A Compensation Plan SHOULD be represented as:

```json
{
  "compensation_plan_id": "cp_20260503_001",
  "decision_id": "decision_123",
  "execution_ref": "execution_456",
  "harm_summary": "string",
  "affected_party_refs": [],
  "repair_point_refs": [],
  "sovereignty_claim_refs": [],
  "compensation_type": "restoration | payment | access_correction | record_correction | apology | service | policy_change | resource | other",
  "proposed_remedy": "string",
  "authority_refs": [],
  "review_required": true,
  "affected_party_review_refs": [],
  "commitment_refs": [],
  "completion_evidence_refs": [],
  "status": "proposed | under_review | committed | in_progress | completed | contested | failed | superseded",
  "record_refs": [],
  "metadata": {}
}
```

---

## 10. Rollback Request Object

A Rollback Request SHOULD be represented as:

```json
{
  "rollback_request_id": "rbr_20260503_001",
  "decision_id": "decision_123",
  "execution_ref": "execution_456",
  "requested_by": "actor_or_party_ref",
  "request_type": "rollback | compensation | mitigation | hybrid",
  "basis": "authority_failure | scope_failure | harm | challenge | affected_party_review | sovereignty_claim | emergency_review | schema_drift | other",
  "description": "string",
  "evidence_refs": [],
  "urgency": "low | medium | high | emergency",
  "requested_action": "string",
  "status": "submitted | acknowledged | under_review | approved | rejected | deferred | in_progress | completed | failed | superseded",
  "record_refs": [],
  "created_at": "timestamp"
}
```

---

## 11. Rollback Execution Object

A Rollback Execution SHOULD be represented as:

```json
{
  "rollback_execution_id": "rbe_20260503_001",
  "rollback_plan_id": "rbp_20260503_001",
  "decision_id": "decision_123",
  "execution_ref": "execution_456",
  "executed_by": "actor_or_system_ref",
  "authority_ref": "authority_grant_ref",
  "presence_ref": "presence_grant_ref_or_null",
  "started_at": "timestamp",
  "completed_at": null,
  "result": "pending | succeeded | partially_succeeded | failed | unsafe | superseded",
  "step_results": [],
  "evidence_refs": [],
  "residual_harm": "string",
  "compensation_required": false,
  "mitigation_required": false,
  "affected_party_review_required": false,
  "record_refs": [],
  "metadata": {}
}
```

---

## 12. Authority Requirements

Rollback, compensation, and mitigation SHOULD require authority appropriate to the action.

CDP implementations SHOULD distinguish:

- authority to request rollback;
- authority to approve rollback;
- authority to execute rollback;
- authority to approve compensation;
- authority to commit resources;
- authority to alter records;
- authority to notify affected parties;
- authority to satisfy repair obligations.

High-impact rollback or compensation SHOULD require Presence Grant, quorum, or affected-party review where policy requires it.

---

## 13. Interaction with Affected-Party Review

Affected-party review SHOULD be required when rollback or compensation affects:

- identity;
- rights;
- eligibility;
- benefits;
- access;
- land;
- jurisdiction;
- cultural material;
- repair obligations;
- sovereignty claims;
- public or private records about affected parties.

Affected parties MAY contest:

- whether rollback was sufficient;
- whether compensation was appropriate;
- whether completion evidence is adequate;
- whether residual harm remains;
- whether repair should remain open.

---

## 14. Interaction with Sovereignty Claims

If rollback or compensation affects a sovereignty claim, CDP SHOULD preserve:

- sovereignty claim refs;
- authority conflict refs;
- affected sovereign or community review;
- restricted evidence controls;
- non-appropriation requirements;
- dissent;
- unresolved status where applicable.

Rollback MUST NOT be used to erase sovereignty claims from the record.

---

## 15. Rollback State Guidance

Rollback status SHOULD use:

```text
not_required
requested
acknowledged
under_review
approved
rejected
deferred
in_progress
succeeded
partially_succeeded
failed
unsafe
compensation_required
mitigation_required
contested
closed
learned
```

`partially_succeeded` SHOULD trigger compensation or mitigation review.

`failed` MUST NOT be treated as closure.

---

## 16. Record Requirements

CDP implementations SHOULD record:

- original execution;
- rollback request;
- authority basis;
- rollback plan;
- compensation plan;
- mitigation actions;
- presence grants;
- affected parties;
- repair refs;
- sovereignty refs;
- execution steps;
- evidence;
- residual harm;
- review outcome;
- dissent;
- learning artifacts.

Rollback records MUST preserve the original action. They MUST NOT rewrite history to make the original execution disappear.

---

## 17. Failure Modes

CDP implementations SHOULD distinguish:

- rollback impossible;
- rollback unsafe;
- rollback partial;
- rollback authority failure;
- rollback presence failure;
- compensation authority failure;
- compensation insufficient;
- mitigation insufficient;
- affected-party review contested;
- sovereignty conflict unresolved;
- evidence insufficient;
- repair obligation still open;
- learning failure.

---

## 18. Learning Hooks

Rollback and compensation SHOULD trigger Learn when:

- rollback is requested;
- rollback succeeds;
- rollback partially succeeds;
- rollback fails;
- compensation is required;
- mitigation is required;
- affected-party review contests outcome;
- sovereignty claim was mishandled;
- emergency override caused harm;
- schema drift caused or revealed the need for rollback;
- execution gate policy was insufficient;
- presence authority was insufficient.

Learning artifacts MAY include:

- execution policy update;
- rollback plan template;
- compensation policy update;
- authority model update;
- presence requirement update;
- repair commitment;
- schema drift rule;
- emergency override rule;
- incident precedent.

Learning MUST NOT erase original execution, harm, dissent, or repair obligations.

---

## 19. Minimal Compliance

A minimal CDP implementation SHOULD support:

- rollback request;
- rollback plan;
- rollback execution result;
- compensation plan;
- mitigation action record;
- authority references;
- affected-party review flag;
- completion evidence;
- residual harm field;
- learning hook.

A minimal implementation MUST NOT treat rollback failure as closure.

---

## 20. Summary

Execution is not the end of governance.

When action has already happened, CDP must still be able to reverse what can be reversed, compensate what cannot be reversed, mitigate what is still dangerous, preserve what happened, and learn without erasure.

Rollback repairs state when possible. Compensation addresses harm when reversal is not enough. Mitigation reduces ongoing danger. Record preserves truth. Learn changes the future.
