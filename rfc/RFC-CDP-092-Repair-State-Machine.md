# RFC-CDP-092 — Repair State Machine

Author: Kevin “Andie” Williams  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: May 3, 2026  
Depends On: RFC-CDP-001, RFC-CDP-010, RFC-CDP-032, RFC-CDP-047, RFC-CDP-048, RFC-CDP-061, RFC-CDP-071, RFC-CDP-072, RFC-CDP-073, RFC-CDP-074  
Updates: RFC-CDP-071, RFC-CDP-072, RFC-CDP-073, RFC-CDP-074

## Abstract

This RFC defines the Repair State Machine for the Constitutional Decision Plane (CDP).

The Repair State Machine governs the lifecycle of Breach Records, Repair Agendas, Repair Points, Institutional Responses, Repair Commitments, Completion Evidence, Affected-Party Review, Dissent, and Sovereignty Claims.

Repair is not an ordinary decision lifecycle. It may begin before a Decision, interrupt a Decision, block execution, reopen closure, preserve unresolved authority conflict, and require learning even when no final agreement is reached.

---

## 1. Purpose

This RFC answers:

- what states a repair process may occupy;
- what transitions are allowed;
- what conditions block closure;
- how affected-party review affects state;
- how sovereignty claims affect state;
- how institutional response and non-response are represented;
- how repair commitments move through execution and evidence;
- how repair may fail, reopen, or remain unresolved;
- how repair produces learning without erasing breach history.

---

## 2. Core Principle

Repair is a lifecycle, not a note field.

A repair process MUST preserve breach, claim, response, commitment, evidence, affected-party review, dissent, authority conflict, and learning state.

Repair MUST NOT be marked complete merely because a responding institution says it is complete.

---

## 3. Relationship to Existing RFCs

### 3.1 RFC-CDP-071 Twenty Points Repair Protocol

RFC-CDP-071 defines the repair protocol and anti-flattening requirements.

This RFC defines the state machine used to govern that protocol.

### 3.2 RFC-CDP-072 Breach Record and Repair Agenda Schema

RFC-CDP-072 defines the objects that move through repair states.

This RFC defines allowed state transitions for those objects.

### 3.3 RFC-CDP-073 Affected-Party Review and Anti-Erasure

RFC-CDP-073 defines review rights, anti-erasure violations, and closure blocking.

This RFC defines how review and anti-erasure outcomes affect repair state.

### 3.4 RFC-CDP-074 Sovereignty Claims and Authority Pluralism

RFC-CDP-074 defines sovereignty claims, authority conflicts, and closure/execution blocking.

This RFC defines state transitions when sovereignty claims are asserted, contested, unresolved, or superseded.

---

## 4. Repair Lifecycle Overview

The typical repair lifecycle is:

```text
DISCOVERED
  → SUBMITTED
  → ACKNOWLEDGED
  → UNDER_REVIEW
  → RESPONDED
  → COMMITTED
  → IN_REPAIR
  → EVIDENCE_SUBMITTED
  → AFFECTED_PARTY_REVIEW
  → CLOSED
  → LEARNED
```

However, repair is non-linear. It may enter contested, blocked, failed, unresolved, reopened, or superseded states.

---

## 5. Canonical Repair States

Repair implementations SHOULD support the following states.

| State | Meaning |
|---|---|
| `DISCOVERED` | A possible breach, repair claim, or repair need has been identified. |
| `SUBMITTED` | A Breach Record, Repair Agenda, or Repair Point has been submitted. |
| `ACKNOWLEDGED` | The receiving institution or CDP process acknowledges receipt. |
| `PRESERVED` | Original claim shape, numbering, language, provenance, and authority are preserved. |
| `UNDER_REVIEW` | The claim is being reviewed for scope, authority, evidence, and response requirements. |
| `CONTESTED` | Accuracy, authority, evidence, classification, response, or closure is disputed. |
| `AUTHORITY_CONFLICT` | One or more unresolved authority claims materially affect the process. |
| `RESPONSE_REQUIRED` | Institutional or accountable response is required. |
| `RESPONDED` | A response has been recorded. |
| `COMMITMENT_REQUIRED` | The response requires a concrete repair commitment. |
| `COMMITTED` | A repair commitment has been recorded. |
| `IN_REPAIR` | A repair commitment is being executed or implemented. |
| `EVIDENCE_REQUIRED` | Completion evidence is required before closure. |
| `EVIDENCE_SUBMITTED` | Completion evidence has been submitted. |
| `AFFECTED_PARTY_REVIEW` | Affected-party or sovereign-party review is required or active. |
| `BLOCKED` | Progress is blocked by missing review, authority conflict, evidence failure, or anti-erasure violation. |
| `DEFERRED` | Action is deferred with recorded reason and review date. |
| `FAILED` | Repair commitment or process has failed. |
| `UNRESOLVED` | Repair cannot presently be resolved but remains material and open in the record. |
| `CLOSED_WITH_RESERVATIONS` | Closure is allowed but reservations or dissent remain recorded. |
| `CLOSED` | Repair is closed under applicable authority, evidence, and review requirements. |
| `REOPENED` | A closed or deferred repair item has been reopened. |
| `SUPERSEDED` | A later agreement, agenda, record, or process supersedes this repair item. |
| `WITHDRAWN` | An authorized claimant withdraws the claim or point. |
| `LEARNED` | Learning artifacts have been produced. |

---

## 6. Terminal and Non-Terminal States

### 6.1 Terminal States

The following MAY be terminal for a specific repair object:

```text
CLOSED
CLOSED_WITH_RESERVATIONS
SUPERSEDED
WITHDRAWN
LEARNED
```

### 6.2 Non-Terminal Durable States

The following are non-terminal but may persist indefinitely:

```text
CONTESTED
AUTHORITY_CONFLICT
BLOCKED
DEFERRED
FAILED
UNRESOLVED
```

A non-terminal durable state MUST remain discoverable.

Unresolved is not closed.

Deferred is not repaired.

Failed is not forgotten.

---

## 7. Allowed Transitions

Implementations SHOULD enforce the following transition guidance.

| From | To | Condition |
|---|---|---|
| `DISCOVERED` | `SUBMITTED` | Claim or breach is formally submitted. |
| `SUBMITTED` | `ACKNOWLEDGED` | Receipt is recorded. |
| `SUBMITTED` | `PRESERVED` | Original claim structure is preserved. |
| `ACKNOWLEDGED` | `PRESERVED` | Original claim structure is preserved after acknowledgment. |
| `PRESERVED` | `UNDER_REVIEW` | Review begins. |
| `UNDER_REVIEW` | `CONTESTED` | Accuracy, authority, classification, or evidence is challenged. |
| `UNDER_REVIEW` | `AUTHORITY_CONFLICT` | Material authority conflict is detected. |
| `UNDER_REVIEW` | `RESPONSE_REQUIRED` | Institution or accountable party must respond. |
| `RESPONSE_REQUIRED` | `RESPONDED` | Response is recorded. |
| `RESPONDED` | `COMMITMENT_REQUIRED` | Response requires concrete repair commitment. |
| `RESPONDED` | `CONTESTED` | Response is disputed. |
| `COMMITMENT_REQUIRED` | `COMMITTED` | Repair commitment is recorded. |
| `COMMITTED` | `IN_REPAIR` | Repair execution begins. |
| `IN_REPAIR` | `EVIDENCE_REQUIRED` | Completion evidence is required. |
| `EVIDENCE_REQUIRED` | `EVIDENCE_SUBMITTED` | Evidence is submitted. |
| `EVIDENCE_SUBMITTED` | `AFFECTED_PARTY_REVIEW` | Review is required or requested. |
| `AFFECTED_PARTY_REVIEW` | `CONTESTED` | Review contests target. |
| `AFFECTED_PARTY_REVIEW` | `CLOSED_WITH_RESERVATIONS` | Review permits closure with reservations. |
| `AFFECTED_PARTY_REVIEW` | `CLOSED` | Review supports closure or policy permits closure. |
| `CLOSED` | `LEARNED` | Learning artifacts are generated. |
| `CLOSED_WITH_RESERVATIONS` | `LEARNED` | Learning artifacts preserve reservations. |
| `FAILED` | `LEARNED` | Failure produces learning. |
| `UNRESOLVED` | `LEARNED` | Unresolved status produces learning without closure. |
| `CLOSED` | `REOPENED` | New evidence, review, dissent, or authority conflict reopens. |
| `CLOSED_WITH_RESERVATIONS` | `REOPENED` | Reservations mature into new contestation. |
| `REOPENED` | `UNDER_REVIEW` | Review resumes. |

---

## 8. Forbidden Transitions

Implementations MUST prevent or explicitly flag the following patterns:

| Forbidden Pattern | Reason |
|---|---|
| `SUBMITTED → CLOSED` | Claim cannot close without preservation, review, and response checks. |
| `RESPONDED → CLOSED` without evidence when evidence is required | Institutional response is not repair completion. |
| `COMMITTED → CLOSED` without Completion Evidence | Commitment is not completion. |
| `EVIDENCE_SUBMITTED → CLOSED` without required affected-party review | Evidence must be reviewable when review is required. |
| `CONTESTED → CLOSED` without disposition | Contestation must be resolved, preserved, or explicitly carried as reservation. |
| `AUTHORITY_CONFLICT → CLOSED` without authority disposition | Authority conflict cannot disappear silently. |
| `BLOCKED → CLOSED` without unblock rationale | Block must be resolved or superseded. |
| `DEFERRED → CLOSED` without renewed review | Deferral is not closure. |
| `FAILED → CLOSED` without repair path or supersession | Failure cannot become completion. |
| `UNRESOLVED → CLOSED` without new authority or evidence | Unresolved is not closed. |

---

## 9. Closure Rules

Closure SHOULD require:

- original claim preserved;
- authority claims recorded;
- institutional response recorded when required;
- repair commitment recorded when required;
- completion evidence recorded when required;
- affected-party review completed when required;
- sovereignty claim disposition recorded when applicable;
- dissent preserved;
- anti-erasure violations resolved or carried as reservations;
- learning path defined.

Closure MUST NOT erase dissent, reservations, unresolved authority claims, breach history, or repair history.

---

## 10. Blocking Conditions

A repair process SHOULD enter `BLOCKED` when:

- affected-party review is required but absent;
- sovereignty claim is material and unresolved;
- authority conflict prevents closure or execution;
- original repair point was not preserved;
- institutional response is missing where required;
- completion evidence is missing or insufficient;
- summary is materially contested;
- restricted or culturally sensitive material is mishandled;
- anti-erasure violation is material;
- responding institution is sole evaluator where independent review is required.

A blocked process SHOULD include reason, responsible parties, unblock conditions, review date, and record references.

---

## 11. Reopening Rules

A closed repair item SHOULD be reopenable when:

- new evidence emerges;
- affected-party review contests closure;
- completion evidence is found insufficient;
- sovereignty claim becomes material;
- authority conflict was not preserved;
- erasure event is detected;
- repair commitment fails after closure;
- learning reveals recurring harm;
- closure was based on invalid authority or stale schema.

Reopening MUST preserve prior closure record. It MUST NOT rewrite history.

---

## 12. Repair State Object

A Repair State object SHOULD be represented as:

```json
{
  "repair_state_id": "rs_20260503_001",
  "target_type": "breach_record | repair_agenda | repair_point | institutional_response | repair_commitment | completion_evidence | authority_conflict | sovereignty_claim",
  "target_ref": "target_id",
  "current_state": "UNDER_REVIEW",
  "previous_state": "PRESERVED",
  "transition_reason": "string",
  "required_next_actions": [],
  "blocking_conditions": [],
  "authority_claim_refs": [],
  "affected_party_review_refs": [],
  "sovereignty_claim_refs": [],
  "dissent_refs": [],
  "evidence_refs": [],
  "record_refs": [],
  "updated_by": "actor_or_system_ref",
  "updated_at": "timestamp"
}
```

---

## 13. State Transition Record

Every material state transition SHOULD produce a transition record.

```json
{
  "transition_id": "rst_20260503_001",
  "repair_state_id": "rs_20260503_001",
  "target_ref": "target_id",
  "from_state": "UNDER_REVIEW",
  "to_state": "CONTESTED",
  "trigger": "affected_party_review | institutional_response | evidence | authority_conflict | erasure_event | policy | AIITL_signal | other",
  "actor_ref": "actor_or_system_ref",
  "authority_ref": "authority_or_claim_ref",
  "rationale": "string",
  "record_refs": [],
  "created_at": "timestamp"
}
```

---

## 14. AIITL Repair State Duties

AIITL MAY surface possible state errors.

AIITL MAY identify:

- closure without evidence;
- repair point not preserved;
- affected-party review missing;
- dissent hidden;
- sovereignty claim downgraded;
- unresolved authority conflict;
- anti-erasure violation;
- stale closure;
- likely need to reopen.

AIITL MUST NOT:

- close repair;
- simulate affected-party review;
- waive sovereignty claims;
- determine final repair sufficiency;
- erase dissent;
- treat institutional response as completion.

---

## 15. Learning Hooks

The Repair State Machine SHOULD trigger Learn when:

- repair closes;
- repair closes with reservations;
- repair fails;
- repair remains unresolved beyond policy threshold;
- repair is reopened;
- authority conflict recurs;
- anti-erasure violation occurs;
- affected-party review contests closure;
- completion evidence is repeatedly insufficient.

Learning artifacts MAY include:

- policy revision;
- schema revision;
- authority model revision;
- anti-erasure validation rule;
- affected-party review requirement;
- repair precedent;
- training guidance;
- escalation pattern;
- new state or transition rule.

Learning MUST NOT erase the repair record.

---

## 16. Minimal Compliance

A minimal CDP implementation SHOULD support:

- canonical repair states;
- current state per repair target;
- state transition record;
- blocked state and reason;
- contested state;
- affected-party review state;
- authority-conflict state;
- closure and closure-with-reservations;
- reopening;
- learning hook;
- forbidden transition checks.

A minimal implementation MUST NOT allow repair to close solely because an institution has responded.

---

## 17. Summary

Repair has state.

Repair may be submitted, preserved, reviewed, contested, blocked, committed, evidenced, reviewed again, closed, reopened, unresolved, failed, superseded, or learned from.

A repair state machine prevents institutions from treating repair as a comment, a checkbox, a public-relations response, or an internal closure decision.

Unresolved is not closed. Deferred is not repaired. Failed is not forgotten.
