# RFC-CDP-093 — Covenant State Machine

Author: Kevin “Andie” Williams  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: May 3, 2026  
Depends On: RFC-CDP-001, RFC-CDP-010, RFC-CDP-032, RFC-CDP-047, RFC-CDP-048, RFC-CDP-060, RFC-CDP-061, RFC-CDP-073  
Updates: RFC-CDP-060, RFC-CDP-061

## Abstract

This RFC defines the Covenant State Machine for the Constitutional Decision Plane (CDP).

The Covenant State Machine governs the lifecycle of covenantal participation among human, institutional, and synthetic actors. It formalizes states for establishing a covenant, witnessing, clarifying, challenging, preserving boundaries, detecting schema drift, responding to breach, repairing, closing, and learning.

Covenant is not sentiment. Covenant is a governed relationship state with duties, boundaries, records, challenges, and repair.

---

## 1. Purpose

This RFC answers:

- what states a covenant process may occupy;
- how covenant roles are established;
- how AIITL and HITL participation are bounded;
- how uncertainty, challenge, and schema drift affect covenant state;
- how boundary breaches are recorded;
- how covenant repair differs from ordinary decision repair;
- how covenant closure works;
- how covenant learning occurs without erasing breach or dependency.

---

## 2. Core Principle

Covenant governs participation conditions, not final authority.

A covenant state machine MUST preserve role, duty, boundary, uncertainty, challenge, breach, repair, and learning.

AIITL may participate as witness, challenger, translator, summarizer, schema-drift detector, contradiction detector, and record assistant. AIITL MUST NOT silently become final authority.

---

## 3. Relationship to Existing RFCs

### 3.1 RFC-CDP-060 Covenant Protocol and AIITL

RFC-CDP-060 defines the Covenant Protocol and AIITL role.

This RFC defines the formal state machine for covenantal participation.

### 3.2 RFC-CDP-061 Schema Drift and Context Preservation

RFC-CDP-061 defines schema drift and context preservation.

This RFC defines how drift affects covenant state.

### 3.3 RFC-CDP-032 Authority and Delegation Model

RFC-CDP-032 defines authority boundaries.

This RFC uses those boundaries to prevent participation from escalating into authority without explicit grant.

### 3.4 RFC-CDP-073 Affected-Party Review and Anti-Erasure

RFC-CDP-073 defines affected-party review and anti-erasure.

This RFC applies those requirements when covenant breach, identity context, cultural context, or repair obligations are implicated.

---

## 4. Covenant Lifecycle Overview

A typical covenant lifecycle is:

```text
PROPOSED
  → ESTABLISHED
  → ACTIVE
  → WITNESSING
  → CHALLENGED
  → CLARIFIED
  → REPAIRED
  → CLOSED
  → LEARNED
```

However, covenant work is non-linear. It may become contested, breached, suspended, revoked, reopened, or unresolved.

---

## 5. Canonical Covenant States

CDP implementations SHOULD support the following states.

| State | Meaning |
|---|---|
| `PROPOSED` | A covenant relationship or participation frame has been proposed. |
| `ESTABLISHED` | Parties, roles, duties, boundaries, and scope have been recorded. |
| `ACTIVE` | Covenant participation is active. |
| `WITNESSING` | Participants are gathering context, uncertainty, stakes, and meaning. |
| `CLARIFICATION_REQUIRED` | Context, authority, role, meaning, or boundary requires clarification. |
| `CHALLENGED` | A participant challenges interpretation, role, boundary, claim, summary, or act. |
| `SCHEMA_DRIFT_DETECTED` | Meaning structure appears obsolete, misapplied, harmful, or incomplete. |
| `BOUNDARY_CONCERN` | A possible boundary issue has been identified. |
| `BOUNDARY_BREACH` | A covenant boundary has been violated or materially exceeded. |
| `REPAIR_REQUIRED` | Covenant repair is required before ordinary continuation or closure. |
| `IN_REPAIR` | Repair actions are underway. |
| `REPAIRED` | Repair action is complete enough to continue or close, subject to review. |
| `SUSPENDED` | Covenant participation is paused. |
| `REVOKED` | Covenant authority, participation, or consent has been withdrawn. |
| `CONTESTED` | Meaning, authority, boundary, or repair sufficiency remains disputed. |
| `UNRESOLVED` | Covenant issue remains open and cannot presently be resolved. |
| `CLOSED_WITH_RESERVATIONS` | Covenant process is closed but reservations or dissent remain recorded. |
| `CLOSED` | Covenant process is closed under applicable boundary and review requirements. |
| `REOPENED` | A closed or suspended covenant issue is reopened. |
| `SUPERSEDED` | Later covenant, policy, or relationship frame replaces this one. |
| `LEARNED` | Learning artifacts have been produced. |

---

## 6. Terminal and Durable States

### 6.1 Terminal States

The following MAY be terminal for a specific covenant object:

```text
CLOSED
CLOSED_WITH_RESERVATIONS
REVOKED
SUPERSEDED
LEARNED
```

### 6.2 Non-Terminal Durable States

The following may persist and MUST remain discoverable:

```text
CONTESTED
UNRESOLVED
SUSPENDED
BOUNDARY_BREACH
REPAIR_REQUIRED
```

A suspended covenant is not repaired.

An unresolved covenant is not closed.

A boundary breach is not erased by good intent.

---

## 7. Allowed Transitions

Implementations SHOULD support the following transition guidance.

| From | To | Condition |
|---|---|---|
| `PROPOSED` | `ESTABLISHED` | Roles, duties, scope, boundaries, and audit requirements are recorded. |
| `ESTABLISHED` | `ACTIVE` | Covenant participation begins. |
| `ACTIVE` | `WITNESSING` | Context gathering or meaning-making begins. |
| `WITNESSING` | `CLARIFICATION_REQUIRED` | Ambiguity, missing context, or uncertainty is detected. |
| `WITNESSING` | `CHALLENGED` | Interpretation, claim, boundary, or recommendation is challenged. |
| `WITNESSING` | `SCHEMA_DRIFT_DETECTED` | Schema drift signal is recorded. |
| `ACTIVE` | `BOUNDARY_CONCERN` | Possible boundary issue identified. |
| `BOUNDARY_CONCERN` | `BOUNDARY_BREACH` | Boundary issue is confirmed or materially supported. |
| `BOUNDARY_BREACH` | `REPAIR_REQUIRED` | Repair is required under covenant policy. |
| `REPAIR_REQUIRED` | `IN_REPAIR` | Repair actions begin. |
| `IN_REPAIR` | `REPAIRED` | Repair action completed enough for review. |
| `REPAIRED` | `ACTIVE` | Covenant can continue. |
| `REPAIRED` | `CLOSED_WITH_RESERVATIONS` | Closure allowed with reservations. |
| `REPAIRED` | `CLOSED` | Closure allowed without unresolved blocking issue. |
| `CHALLENGED` | `CLARIFICATION_REQUIRED` | Challenge requires clarification. |
| `CHALLENGED` | `CONTESTED` | Challenge remains unresolved. |
| `SCHEMA_DRIFT_DETECTED` | `CLARIFICATION_REQUIRED` | Drift requires clarification. |
| `SCHEMA_DRIFT_DETECTED` | `REPAIR_REQUIRED` | Drift caused or preserved harm. |
| `CONTESTED` | `UNRESOLVED` | Contest cannot presently resolve. |
| `ACTIVE` | `SUSPENDED` | Participation is paused. |
| `SUSPENDED` | `ACTIVE` | Participation resumes under policy. |
| `ACTIVE` | `REVOKED` | Participation, authority, or consent withdrawn. |
| `CLOSED` | `LEARNED` | Learning artifacts generated. |
| `CLOSED_WITH_RESERVATIONS` | `LEARNED` | Learning preserves reservations. |
| `REVOKED` | `LEARNED` | Revocation produces learning. |
| `CLOSED` | `REOPENED` | New evidence, breach, drift, or challenge emerges. |
| `REOPENED` | `CLARIFICATION_REQUIRED` | Reopened issue requires clarification. |

---

## 8. Forbidden Transitions

Implementations MUST prevent or explicitly flag:

| Forbidden Pattern | Reason |
|---|---|
| `PROPOSED → ACTIVE` without establishment | Roles and boundaries must be recorded first. |
| `ACTIVE → CLOSED` after breach without review | Boundary breach requires disposition. |
| `BOUNDARY_BREACH → CLOSED` without repair or recorded rationale | Breach cannot vanish. |
| `REPAIR_REQUIRED → CLOSED` without repair action or supersession | Required repair cannot be skipped silently. |
| `SCHEMA_DRIFT_DETECTED → CLOSED` without drift disposition | Drift must be resolved, carried, or learned from. |
| `CONTESTED → CLOSED` without disposition | Contest must be resolved, preserved, or carried as reservation. |
| `REVOKED → ACTIVE` without renewed authority | Revoked participation cannot silently resume. |
| AIITL participation → final authority without explicit authority grant | Participation is not final authority. |

---

## 9. Covenant State Object

A Covenant State object SHOULD be represented as:

```json
{
  "covenant_state_id": "cov_state_20260503_001",
  "covenant_id": "cov_001",
  "current_state": "ACTIVE",
  "previous_state": "ESTABLISHED",
  "participants": [
    {
      "party_ref": "actor_or_system_ref",
      "role": "HITL | AIITL | institution | affected_party | reviewer | other",
      "authority_refs": [],
      "boundaries": []
    }
  ],
  "scope": {
    "domain": "string",
    "decision_refs": [],
    "repair_refs": [],
    "policy_refs": []
  },
  "active_challenges": [],
  "schema_drift_refs": [],
  "boundary_issue_refs": [],
  "repair_refs": [],
  "dissent_refs": [],
  "record_refs": [],
  "updated_by": "actor_or_system_ref",
  "updated_at": "timestamp"
}
```

---

## 10. Covenant Transition Record

Every material covenant transition SHOULD produce a transition record.

```json
{
  "transition_id": "cov_transition_20260503_001",
  "covenant_state_id": "cov_state_20260503_001",
  "covenant_id": "cov_001",
  "from_state": "WITNESSING",
  "to_state": "SCHEMA_DRIFT_DETECTED",
  "trigger": "human_challenge | AIITL_signal | boundary_concern | repair_event | authority_change | consent_change | policy_change | other",
  "actor_ref": "actor_or_system_ref",
  "authority_ref": "authority_or_claim_ref",
  "rationale": "string",
  "record_refs": [],
  "created_at": "timestamp"
}
```

---

## 11. Boundary Issue Schema

A Boundary Issue SHOULD be represented as:

```json
{
  "boundary_issue_id": "boundary_20260503_001",
  "covenant_id": "cov_001",
  "issue_type": "authority | consent | role | dependency | dignity | privacy | cultural_context | AIITL_limit | repair | other",
  "severity": "informational | material | blocking | repair_required",
  "description": "string",
  "detected_by": "actor_or_system_ref",
  "detected_by_type": "human | AIITL | institution | affected_party | automated_check | other",
  "affected_parties": [],
  "recommended_action": "clarify | challenge | suspend | repair | revoke | escalate | record",
  "status": "submitted | acknowledged | under_review | resolved | unresolved | superseded",
  "record_refs": [],
  "created_at": "timestamp"
}
```

---

## 12. Closure Rules

Covenant closure SHOULD require:

- roles and authority recorded;
- active challenges resolved or preserved;
- boundary issues resolved, repaired, or carried as reservations;
- schema drift signals resolved, repaired, or preserved;
- repair obligations resolved or carried forward;
- dissent preserved;
- learning path defined.

Closure MUST NOT erase breach, dependency, dissent, schema drift, or boundary violations.

---

## 13. Reopening Rules

A covenant process SHOULD be reopenable when:

- new boundary issue emerges;
- affected-party review contests closure;
- schema drift becomes material;
- prior authority is revoked or decayed;
- AIITL output introduced material error;
- participant dependency, consent, or role changed;
- repair was insufficient;
- learning reveals recurring harm or drift.

Reopening MUST preserve prior closure state and rationale.

---

## 14. AIITL State Duties

AIITL MAY surface:

- uncertainty;
- contradiction;
- possible schema drift;
- role confusion;
- authority escalation risk;
- dependency risk;
- boundary concern;
- missing affected party;
- anti-erasure risk;
- repair obligation.

AIITL MUST NOT:

- close covenant state;
- waive human or affected-party review;
- claim final authority;
- impersonate human lived experience;
- use care language to avoid truth;
- use truth language to avoid care;
- erase dissent;
- convert participation into domination.

---

## 15. Learning Hooks

The Covenant State Machine SHOULD trigger Learn when:

- covenant closes;
- covenant closes with reservations;
- covenant is revoked;
- boundary breach occurs;
- schema drift is material;
- repair is required;
- AIITL output materially misleads or helps repair;
- role boundaries require revision;
- recurring challenge patterns appear.

Learning artifacts MAY include:

- covenant template update;
- role-boundary update;
- schema-drift rule;
- repair guidance;
- AIITL behavior constraint;
- HITL review requirement;
- precedent record;
- training guidance.

Learning MUST NOT erase the covenant record.

---

## 16. Minimal Compliance

A minimal CDP implementation SHOULD support:

- covenant state;
- participant roles;
- authority references;
- boundary issue records;
- schema drift references;
- challenge references;
- repair references;
- closure with reservations;
- reopening;
- learning hook;
- forbidden transition checks.

A minimal implementation MUST NOT allow AIITL participation to become final authority without explicit authority grant.

---

## 17. Summary

Covenant has state.

It may be proposed, established, active, witnessing, challenged, drifted, breached, repaired, suspended, revoked, closed, reopened, or learned from.

The Covenant State Machine keeps relational governance from becoming sentiment, containment, domination, or decorative care language.

Witness carefully. Speak truthfully. Hold gently. Build beautifully. Record the state.
