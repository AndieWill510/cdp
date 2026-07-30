# RFC-CDP-092 — Repair State Machine

Author: Kevin “Andie” Williams  
Status: Draft v0.3  
Series: Constitutional Decision Plane (CDP)  
Date: July 30, 2026  
Depends On: RFC-CDP-001, RFC-CDP-010, RFC-CDP-032, RFC-CDP-033, RFC-CDP-045, RFC-CDP-047, RFC-CDP-048, RFC-CDP-061, RFC-CDP-070, RFC-CDP-071, RFC-CDP-072, RFC-CDP-073, RFC-CDP-074  
Updates: RFC-CDP-071, RFC-CDP-072, RFC-CDP-073, RFC-CDP-074

## Abstract

Repair exists because governance exercises power over relationships.

Procedure determines whether power was exercised according to constitutional process. Constitutional legitimacy, under `RFC-CDP-045-Legitimize-Protocol.md`, determines whether the answerability created by that exercise of power was preserved rather than erased, ignored, or institutionally denied. Repair determines whether the relationships affected by that exercise of power remain capable of continuing.

These are distinct constitutional questions. A procedurally flawless, constitutionally legitimate decision may nevertheless leave trust damaged, dignity diminished, grief unanswered, cooperation impaired, or answerability incomplete. Repair exists because governance concerns relationships, not merely decisions.

This RFC defines the Repair State Machine for the Constitutional Decision Plane (CDP): the lifecycle of Breach Records, Repair Agendas, Repair Points, Institutional Responses, Repair Commitments, Completion Evidence, Affected-Party Review, Dissent, and Sovereignty Claims.

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

A repair process MUST preserve breach, claim, response, commitment, evidence, affected-party review, dissent, authority conflict, relationship disposition, and learning state.

Repair MUST NOT be marked complete merely because a responding institution says it is complete.

The state of the Repair process and the resulting state of the affected relationship are distinct determinations. Section 13 defines the latter as a Relationship Disposition, recorded separately from `current_state`.

### 2.1 Repair Follows Relationship, Not Error

Repair is not triggered solely by procedural failure, under the constitutional principle established in `RFC-CDP-001-Vision-Scope-Principles.md` Section 5.13.

Repair is required whenever the exercise of governed power leaves a material answerability relationship unresolved, impaired, denied, or incapable of healthy continuation. That relationship may be strained by a decision that broke no rule at all: a correctly authorized, fully legitimate act can still leave the parties to it unable to continue in right relationship.

Procedural correctness neither guarantees nor eliminates the need for Repair. A decision MAY be procedurally correct, constitutionally legitimate, and still require Repair.

### 2.2 The Governing Question of Repair

Each stage of the CDP lifecycle answers a distinct constitutional question. Propose asks what should we do. Challenge asks what might be wrong. Test asks whether it holds. Adjudicate asks what the decision is. Legitimize asks whether we may act. Execute asks whether we acted. Record asks what happened.

Repair asks a different question: what remains between us?

Repair is not primarily asking who was right, who won, or who is at fault. Those questions may be answered along the way, as evidence within a breach record or a factor in an institutional response. But they are not what Repair exists to resolve. Repair asks what remains between the parties after power has been exercised, and whether that remainder can be carried forward, restored, or honestly closed.

### 2.3 Relationship to Procedural and Constitutional Legitimacy

`RFC-CDP-045-Legitimize-Protocol.md` distinguishes procedural legitimacy from constitutional legitimacy. This RFC adds a third, independent constitutional question:

- **Procedural legitimacy** asks: was governance conducted correctly?
- **Constitutional legitimacy** asks: was answerability preserved?
- **Repair** asks: have the affected relationships been restored, renewed, or responsibly transformed after the exercise of power? Section 13 records this answer as a Relationship Disposition, distinct from the process states defined in Sections 5 through 11.

These questions are sequential in that Repair ordinarily follows Legitimize and Execute in time. They are independent in that none of them answers the others. A decision MAY be procedurally correct. A decision MAY be constitutionally legitimate. Repair MAY nevertheless still be required.

Implementations MUST NOT infer that successful completion of Legitimize or Execute implies completion of Repair. `constitutional_legitimacy_status: preserved` under RFC-CDP-045 means material answerability claims were not erased, ignored, or institutionally denied during governance; it does not certify that the relationships those claims arose from are now capable of continuing. That determination belongs to Repair alone, and only the states and closure rules defined later in this RFC may make it.

### 2.4 Constitutional Purpose of Repair

The purpose of Repair is not to erase disagreement, manufacture reconciliation, or require continued relationship.

Its purpose is to ensure that answerability remains possible after power has been exercised, and that relationships are given a governed opportunity either to continue with restored integrity or to conclude with truthfulness, dignity, and an accurate record.

Governance succeeds not merely when every decision is procedurally correct, but when every exercise of power leaves relationships capable of continuing.

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

### 3.5 RFC-CDP-033 Standing and Recusal Model

RFC-CDP-033 defines Standing as the procedural recognition of an answerability relationship that CDP does not create.

This RFC governs what happens when that relationship is left unresolved, impaired, denied, or incapable of healthy continuation after governed power has been exercised. Standing determines who may participate in that process; it does not determine whether the process is owed in the first place. Section 2.1 does.

### 3.6 RFC-CDP-045 Legitimize Protocol

RFC-CDP-045 distinguishes procedural legitimacy from constitutional legitimacy and defines the Answerability Gate that evaluates the latter.

This RFC does not re-adjudicate that determination. It picks up where RFC-CDP-045 leaves off: `constitutional_legitimacy_status: preserved` or `blocked` describes whether governance addressed answerability during the decision. It does not describe whether the relationships affected by the decision are now capable of continuing. Section 2.3 defines that boundary precisely.

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
```

However, repair is non-linear. It may enter contested, blocked, failed, unresolved, reopened, or superseded states.

Learning is recorded against whichever terminal or durable state the repair item reaches; it is not a further stage in this lifecycle. Section 16 defines learning as an event recorded on the repair object, not a transition of `current_state`. Section 13 similarly records the disposition of the affected relationship without changing `current_state`.

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

Learning is not a canonical repair state. Producing learning artifacts does not transition `current_state`; it sets `learning_recorded` and `learning_refs` on the Repair State object defined in Section 12, and is triggered under Section 16.

---

## 6. Terminal and Non-Terminal States

### 6.1 Terminal States

The following MAY be terminal for a specific repair object:

```text
CLOSED
CLOSED_WITH_RESERVATIONS
SUPERSEDED
WITHDRAWN
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
| `CLOSED` | `REOPENED` | New evidence, review, dissent, or authority conflict reopens. |
| `CLOSED_WITH_RESERVATIONS` | `REOPENED` | Reservations mature into new contestation. |
| `REOPENED` | `UNDER_REVIEW` | Review resumes. |

`CLOSED`, `CLOSED_WITH_RESERVATIONS`, `FAILED`, and `UNRESOLVED` each MAY produce learning artifacts. Doing so sets `learning_recorded` and `learning_refs` under Section 12; it is not a transition to a further state, and `current_state` remains whichever of these four values applied.

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
- Relationship Disposition recorded under Section 13;
- learning path defined.

Closure MUST NOT erase dissent, reservations, unresolved authority claims, breach history, or repair history.

Closure MUST NOT be read as establishing a `RESTORED` or `RENEWED` Relationship Disposition. The two are recorded and required independently.

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
  "relationship_disposition_ref": "ref|null",
  "learning_recorded": false,
  "learning_refs": [],
  "updated_by": "actor_or_system_ref",
  "updated_at": "timestamp"
}
```

`relationship_disposition_ref` MAY be null before a disposition is determined. When non-null, it MUST point to a valid Relationship Disposition object as defined in Section 13.

`learning_recorded` MUST be `false` until learning artifacts have been produced for the current terminal or durable state. Setting it `true` MUST NOT change `current_state`.

`learning_refs` MAY be empty. When non-empty, each reference MUST point to a learning artifact produced under Section 16.

---

## 13. Relationship Disposition

Repair closure and relationship restoration are distinct determinations. Implementations MUST NOT infer reconciliation, renewed consent, restored trust, or continued relationship from `CLOSED` or `CLOSED_WITH_RESERVATIONS`.

The Repair State Machine defined in Sections 5 through 11 tracks the state of the Repair *process*: whether it is closed, closed with reservations, failed, unresolved, or otherwise procedurally situated. It does not, by itself, describe what happened to the relationship that made Repair necessary. This section defines that as a separate, required determination.

### 13.1 Relationship Disposition Values

A Relationship Disposition MUST be one of:

| Disposition | Meaning |
|---|---|
| `RESTORED` | The relationship continues on substantially its original terms; trust, consent, and cooperation are reestablished. |
| `RENEWED` | The relationship continues, refreshed by explicit agreement, after a lapse or breach. |
| `TRANSFORMED` | The relationship continues, but on materially changed terms, roles, or conditions. |
| `CONCLUDED` | The relationship ends by mutual or authorized agreement, truthfully and with dignity, without implying restored trust. |
| `CONTINUING_WITH_RESERVATIONS` | The relationship continues, but material reservations, dissent, or unresolved concerns remain on record. |
| `SEPARATED_WITH_OBLIGATIONS` | The relationship ends, but outstanding answerability, remedy, or accountability obligations survive the separation. |
| `UNRESOLVED` | Neither continuation nor conclusion has been determined; the disposition remains open. |
| `NOT_DETERMINED` | No disposition has yet been assessed. |

Implementation profiles MAY refine these values but MUST NOT collapse them into a single "resolved" or "closed" flag.

### 13.2 Normative Rules

The following distinctions MUST be preserved:

- Repair MAY complete without reconciliation.
- A relationship MAY continue in a changed form.
- A relationship MAY conclude truthfully and with dignity without implying fault, defeat, or restored trust.
- Separation MUST NOT be treated as discharging outstanding answerability obligations arising from the same conduct.
- An affected party MAY decline renewed relationship without thereby causing Repair to fail.
- Process closure MUST NOT be treated as proof that trust, consent, or relationship has been restored.

### 13.3 Withdrawal Does Not Discharge Answerability

`WITHDRAWN` describes the claim, not the underlying relationship or its obligations.

Withdrawal of a claim by an authorized claimant does not automatically extinguish institutional, constitutional, public, or independently held answerability obligations arising from the same conduct. A Relationship Disposition MUST still be recorded for a withdrawn repair item where such obligations remain material. `WITHDRAWN` process state and `SEPARATED_WITH_OBLIGATIONS` or `UNRESOLVED` disposition MAY coexist.

### 13.4 Relationship Disposition Object

A Relationship Disposition SHOULD be represented as a governed object associated with, but distinct from, the Repair State object:

```json
{
  "relationship_disposition_id": "rd_20260503_001",
  "repair_state_id": "rs_20260503_001",
  "relationship_disposition": "TRANSFORMED",
  "disposition_rationale": "string",
  "continuing_obligations": [],
  "affected_party_position_refs": [],
  "determined_by": "authority_or_process_ref",
  "recorded_at": "timestamp"
}
```

`relationship_disposition` MUST be one of the values in Section 13.1.

`continuing_obligations` MAY be empty. An empty list is a positive claim that no continuing obligation survives the disposition; it MUST be attested, not assumed.

`affected_party_position_refs` SHOULD reference the affected party's own recorded position on the disposition, including a position of continued disagreement, non-consent, or refusal. Recording a Relationship Disposition MUST NOT require affected-party agreement with that disposition; it MUST require that the affected party's position, if recorded, is not silently overwritten by it.

`determined_by` MUST reference the authority or process responsible for the determination. A responding institution MUST NOT be the sole determiner of a `RESTORED` or `RENEWED` disposition where affected-party review is required under Section 9 or `RFC-CDP-073-Affected-Party-Review-and-Anti-Erasure.md`.

### 13.5 Relationship to Closure

A Relationship Disposition SHOULD be recorded no later than the repair item's transition to a terminal state under Section 6.1.

Closure under Section 9 MUST NOT require a `RESTORED` or `RENEWED` disposition. Closure MAY occur with any disposition value, including `CONCLUDED`, `SEPARATED_WITH_OBLIGATIONS`, or `UNRESOLVED`, provided the applicable closure requirements in Section 9 are otherwise met.

---

## 14. State Transition Record

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

## 15. AIITL Repair State Duties

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
- likely need to reopen;
- a recorded Relationship Disposition inconsistent with the affected party's recorded position or with the underlying evidence.

AIITL MUST NOT:

- close repair;
- simulate affected-party review;
- waive sovereignty claims;
- determine final repair sufficiency;
- erase dissent;
- treat institutional response as completion;
- determine or assert a Relationship Disposition;
- treat process closure as evidence of a `RESTORED` or `RENEWED` disposition.

---

## 16. Learning Hooks

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

Triggering Learn sets `learning_recorded: true` and appends to `learning_refs` on the Repair State object defined in Section 12. It MUST NOT change `current_state`. A repair item that closed, failed, or remained unresolved continues to expose that same `current_state` after learning artifacts are produced; the object does not become harder to query for its disposition merely because it has also been learned from.

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

## 17. Minimal Compliance

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
- learning hook that does not overwrite `current_state`;
- Relationship Disposition, recorded separately from `current_state`;
- forbidden transition checks.

A minimal implementation MUST NOT allow repair to close solely because an institution has responded.

A minimal implementation MUST NOT infer a Relationship Disposition from `current_state` or from the presence of learning artifacts.

---

## 18. Summary

Repair has state.

Repair may be submitted, preserved, reviewed, contested, blocked, committed, evidenced, reviewed again, closed, reopened, unresolved, failed, or superseded. It may also be learned from, without that learning changing which of these states it is in.

A repair state machine prevents institutions from treating repair as a comment, a checkbox, a public-relations response, or an internal closure decision.

Unresolved is not closed. Deferred is not repaired. Failed is not forgotten.

Closed is not restored. A Repair process may reach its most final process state while the relationship it concerns remains transformed, concluded, separated with obligations outstanding, or simply unresolved. That is not a defect in the process. It is the reason Section 13 records the relationship's disposition as its own determination, never inferred from `current_state`, never discharged by withdrawal, and never owed to the responding institution alone to decide.

Repair does not exist because procedure failed. It exists because governance exercises power over relationships, and a procedurally correct, constitutionally legitimate exercise of power can still leave a relationship unable to continue. Repair asks what remains between the parties, and gives that remainder a governed path to restoration or to a truthful, dignified close.
