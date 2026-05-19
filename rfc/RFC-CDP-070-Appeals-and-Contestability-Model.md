# RFC-CDP-070 — Appeals and Contestability Model

Author: Kevin “Andie” Williams  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: May 19, 2026  
Depends On: RFC-CDP-001, RFC-CDP-023, RFC-CDP-033, RFC-CDP-072  
Related: RFC-CDP-071, RFC-CDP-073, RFC-CDP-074, RFC-CDP-075, RFC-CDP-092

## Abstract

This RFC defines the Appeals and Contestability Model for CDP.

It establishes the constitutional right of affected parties to initiate appeal or contestability review, independent of institutional permission.

It defines who may initiate, what events trigger review, the minimum appeal record, closure-blocking conditions, institutional response requirements, and handoff to the Repair plane.

---

## 1. Failure Mode

The failure mode this RFC addresses is **repair without standing to initiate**.

A system that recognizes repair as important but requires institutional permission to trigger review collapses Repair into discretion.

CDP must prevent this.

A related failure mode is **structural repair amnesia**: a governance system iterates through technical correctness while the constitutional claims of affected parties, peoples, or sovereign authorities recede into referenced but procedurally unreachable documents.

A perfectly governed, fully auditable decision that erases a sovereignty claim is still erasure.

---

## 2. Constitutional Right of Entry

Initiation of appeal or contestability review is a constitutional right arising from affected-party standing as defined in `RFC-CDP-033-Standing-and-Recusal-Model.md`.

It is not a procedural permission granted by the institution.

The institution cannot block appeal initiation by denying that harm occurred.

The claim of harm is sufficient to initiate review.

Denial of appeal initiation is itself a breach subject to repair.

---

## 3. Who May Initiate

Any actor with affected-party standing under RFC-CDP-033 MAY initiate appeal or contestability review.

No institutional permission is required.

Standing MAY be challenged during review.

Standing MUST NOT be challenged as a condition of initiation.

---

## 4. Trigger Events

The following events MUST trigger availability of appeal or contestability review:

- denial of constitutional standing;
- challenge filed but not adjudicated before legitimization;
- affected-party claim submitted and not resolved before closure;
- sovereignty claim raised and not addressed before legitimization;
- governed path hash verification failure after execution;
- institutional non-response within a defined response window.

This list is normative for Draft v0.1.

Future drafts MAY add trigger events, but MUST NOT remove these triggers without a superseding RFC or explicit deprecation record.

---

## 5. Minimum Appeal Record

```yaml
appeal_record:
  appeal_id: <uuid>
  decision_id: <uuid>
  initiator_id: <actor_id>
  initiator_standing_basis: <string>
  claim_of_harm: <string>
  trigger_event: <enum>
  appeal_status: <enum>
  # Allowed: initiated|under_review|
  #   responded|unresolved|resolved|
  #   withdrawn|escalated
  institutional_response: <string|null>
  institutional_response_status: <enum>
  # Allowed: unanswered|acknowledged|
  #   accepted|rejected|deferred|
  #   contested|in_repair|completed|
  #   failed
  resolution_record_ref: <ref|null>
  created_at: <timestamp>
  updated_at: <timestamp>
```

The appeal record is a minimum viable schema.

Implementation profiles or later RFCs MAY extend it, but MUST preserve the fields above unless superseded.

---

## 6. Closure-Blocking Rule

A Decision Lifecycle Envelope MUST NOT advance to `status: closed` while:

- an appeal record has `appeal_status` other than `resolved` or `withdrawn`;
- an affected-party claim has no recorded resolution.

This rule is normative.

Implementations MUST enforce it.

Closure of a decision record without resolving active appeal or affected-party claims is a governance breach.

---

## 7. Institutional Response Requirements

The institution MUST respond to each appeal point within a defined response window.

The response window MAY be defined by implementation profile, policy scope, regulation, contract, or governance agreement.

Non-response MUST be recorded as:

```yaml
institutional_response_status: unanswered
```

Silence does not close an appeal.

Delay does not extinguish standing.

---

## 8. Handoff to Repair Plane

RFC-CDP-070 defines entry.

What happens inside the repair process is governed by:

- `RFC-CDP-071-Twenty-Points-Repair-Protocol.md`
- `RFC-CDP-072-Breach-Record-and-Repair-Agenda-Schema.md`
- `RFC-CDP-073-Affected-Party-Review-and-Anti-Erasure.md`
- `RFC-CDP-074-Sovereignty-Claims-and-Authority-Pluralism.md`
- `RFC-CDP-075-Rematriation-and-Land-Resource-Return-Protocol.md`
- `RFC-CDP-092-Repair-State-Machine.md`

An initiated appeal MUST generate a Breach Record under RFC-CDP-072 unless the appeal is withdrawn before review begins.

---

## 9. Relationship to Standing and Recusal

Affected-party standing is sufficient to initiate appeal or contestability review.

Standing may be challenged during review, but not before initiation.

Denial of constitutional standing is itself a trigger event and a breach.

Denial of constitutional standing MUST automatically generate a Breach Record under RFC-CDP-072. This MUST NOT require action by the affected party.

---

## 10. Relationship to Decision Lifecycle Envelope

Appeal and repair activity SHOULD be referenced in the Decision Lifecycle Envelope defined by `RFC-CDP-023-Decision-Lifecycle-Envelope.md`.

At minimum:

- active appeals SHOULD appear in `appeal_refs`;
- repair activity SHOULD appear in `repair_refs`;
- unresolved appeals or affected-party claims MUST block closure under this RFC;
- governed path hash verification failure after execution MUST trigger availability of appeal or contestability review.

Future revisions MAY define stronger RFC-CDP-023 repair-trigger integration once this entry model stabilizes.

---

## 11. Status of This Draft

This RFC was created from Session 005 of the CDP collaboration process.

Promoted into this draft:

- repair without standing to initiate as the primary failure mode;
- structural repair amnesia as a related failure mode;
- appeal initiation as a constitutional right of entry;
- affected-party standing as sufficient for initiation;
- normative trigger events;
- minimum appeal record schema;
- closure-blocking rule;
- institutional response requirements;
- handoff to Repair plane RFCs;
- automatic Breach Record generation for denial of constitutional standing.

Not yet resolved:

- exact response window defaults;
- whether trigger events should become a shared registry;
- how appeal records acquire `record_hash` under future Record Hash Propagation work;
- how the Repair State Machine in RFC-CDP-092 should consume appeal records;
- whether RFC-CDP-023 should later add stronger repair-trigger fields after RFC-CDP-070 stabilizes.

---

## 12. Summary

Repair needs an entry door.

CDP must not require institutional permission before an affected party can initiate appeal or contestability review.

Affected-party standing is sufficient to enter.

Silence does not close an appeal.

Unresolved appeal blocks closure.

Denial of constitutional standing is not merely noted. It generates a breach record and enters the Repair plane.
