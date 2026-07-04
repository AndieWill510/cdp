# RFC-CDP-076 — Repair Efficacy and Verification

Author: Kevin “Andie” Williams  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: July 3, 2026  
Updates: RFC-CDP-070, RFC-CDP-071, RFC-CDP-072, RFC-CDP-073, RFC-CDP-092  
Depends On: RFC-CDP-000, RFC-CDP-001, RFC-CDP-002, RFC-CDP-033, RFC-CDP-070, RFC-CDP-071, RFC-CDP-072, RFC-CDP-073

## Abstract

This RFC defines the Repair Efficacy and Verification extension for the CDP Repair plane.

It establishes a required distinction between **repair completion** and **repair efficacy** so a completed repair workflow, closed repair record, fulfilled commitment, or submitted completion evidence cannot silently imply that repair actually occurred.

This RFC introduces a minimal repair efficacy record surface that allows CDP implementations to say, explicitly and queryably:

- the repair process completed, but efficacy was not assessed;
- efficacy was claimed and evidence was supplied;
- efficacy was disputed;
- efficacy was impossible or unsafe to assess;
- efficacy requires later review.

The purpose is not to add another checklist. The purpose is to prevent procedural completion from masquerading as repair.

---

## 1. Failure Mode

The failure mode this RFC addresses is **repair completion masquerading as repair efficacy**.

A repair process may execute every required step and still leave the harmed party unrepaired.

Examples:

- an appeal is filed, reviewed, responded to, and closed, while the affected party remains unheard;
- a breach record is logged, but the governing vocabulary cannot name the harm;
- a repair commitment is marked completed because the institution performed an action, but the conditions that produced the harm remain unchanged;
- completion evidence exists, but it only proves institutional activity, not repair efficacy;
- affected-party silence is treated as consent, satisfaction, waiver, or closure;
- the repair-efficacy review itself becomes a scored checklist that certifies process rather than weighing reality.

CDP already prevents many repair erasures through standing, appeal initiation, breach records, completion evidence, affected-party review, dissent preservation, and closure blocking.

This RFC adds the missing control:

> A completed repair process is not yet proof of repair.

---

## 2. Source Culture and Routing

This RFC is promoted from ConstantC repair culture work.

The ConstantC culture note `repair-completion-vs-repair-efficacy.md` names the underlying distinction:

- repair completion asks whether the repair process ran;
- repair efficacy asks whether the harm was actually reduced, corrected, witnessed, prevented from recurring, or made more truthfully contestable.

The ConstantC liberty/freedom aperture model also informs this RFC: formal recognition or procedural completion may sit at the top of a funnel while actual freedom, repair, or capability remains narrowed by the conditions of access.

CDP absorbs the principle as a repair-plane control, not as citation theater.

---

## 3. Core Distinction

### 3.1 Repair Completion

**Repair completion** is a process state.

It asks whether a required repair action, commitment, workflow, response, review, or record update has reached its procedural endpoint.

Repair completion may be supported by:

- completed appeal handling;
- institutional response;
- fulfilled commitment;
- submitted completion evidence;
- affected-party review opportunity;
- closure decision;
- learning artifact.

### 3.2 Repair Efficacy

**Repair efficacy** is a legitimacy and outcome question.

It asks whether the repair actually addressed the harm in a way that is evidenced, contestable, authority-aware, and not solely self-certified by the responding institution.

Repair efficacy may require consideration of:

- whether the harmed party had meaningful epistemic standing;
- whether the process had the concepts needed to understand the harm;
- whether the repair changed the conditions that produced or preserved the breach;
- whether completion evidence proves more than institutional activity;
- whether affected-party review, dissent, reservations, or silence affect closure;
- whether structural domination remains intact despite formal inclusion or response.

---

## 4. Non-Certification Rule

CDP MUST NOT treat repair completion as evidence of repair efficacy unless a separate repair-efficacy claim is made, grounded, contestable, and preserved in the record.

Completion evidence MAY support an efficacy claim.

Completion evidence MUST NOT silently become an efficacy claim.

A repair point, repair commitment, breach record, repair agenda, affected-party review process, or repair state machine transition MAY reach a completed procedural state while repair efficacy remains:

- unassessed;
- claimed;
- disputed;
- not assessable;
- requiring future review.

A repair record MAY close procedurally only if the record preserves the efficacy status and any limitations, dissent, or unresolved review conditions.

---

## 5. The Checklist Can Eat Itself

Repair-efficacy prompts are discernment prompts, not a compliance checklist.

A CDP implementation MUST NOT treat the presence of all required repair-efficacy fields as proof that efficacy has been established.

The fields defined in this RFC make the distinction queryable. They do not make the judgment automatic.

The failure mode to avoid is meta-procedural closure:

```text
We asked every efficacy question; therefore repair happened.
```

That is the same error this RFC exists to prevent.

A repair-efficacy record MAY support adjudication, review, closure, reopening, learning, or escalation.

It MUST NOT replace adjudication, affected-party review, authority analysis, or human/community judgment where those are required.

---

## 6. Silence Is Not Consent

Affected-party silence MUST NOT be interpreted as evidence of repair efficacy.

Silence may mean safety, exhaustion, coercion, lack of access, lack of trust, lack of shared language, lack of standing, incapacity, refusal, or an affirmative choice not to participate.

Silence MAY pause repair efficacy assessment.

Silence MUST NOT close repair efficacy assessment.

Where a harmed or affected party is silent, absent, unsafe, constrained, or unavailable, the repair-efficacy record MUST preserve that condition explicitly rather than converting it into consent, satisfaction, waiver, forgiveness, or proof.

---

## 7. Minimal Repair Efficacy Record

A Repair Efficacy Record SHOULD be represented as:

```json
{
  "repair_efficacy_record_id": "re_001",
  "record_type": "repair_efficacy_record",
  "target_type": "repair_point | repair_commitment | breach_record | repair_agenda | completion_evidence | closure | repair_process",
  "target_ref": "target_id",
  "completion_status": "pending | completed | failed | withdrawn | superseded",
  "efficacy_status": "unassessed | claimed | disputed | not_assessable | requires_future_review",
  "efficacy_claim": "string_or_null",
  "efficacy_evidence_refs": [],
  "affected_party_standing": "unknown | present | absent | constrained | disputed",
  "affected_party_review_refs": [],
  "dissent_refs": [],
  "limitations": [],
  "silence_policy": "silence_may_pause_but_must_not_close",
  "verification_refs": [],
  "review_due_at": "timestamp_or_null",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### 7.1 Required Fields

A Repair Efficacy Record MUST include:

- `repair_efficacy_record_id`;
- `record_type`;
- `target_type`;
- `target_ref`;
- `completion_status`;
- `efficacy_status`;
- `affected_party_standing`;
- `silence_policy`;
- `created_at`;
- `updated_at`.

### 7.2 Field Semantics

`completion_status` records procedural state.

`efficacy_status` records the current claim about whether repair actually repaired.

`efficacy_claim` states what changed, if efficacy is claimed.

`efficacy_evidence_refs` point to evidence supporting or contesting that claim.

`affected_party_standing` records whether the affected party had meaningful standing in the efficacy assessment.

`limitations` preserve caveats, constraints, incomplete access, unsafe conditions, contested authority, or assessment boundaries.

`silence_policy` MUST preserve the invariant that silence may pause but must not close repair efficacy assessment.

---

## 8. Efficacy Status Enumeration

Repair efficacy status SHOULD use:

```text
unassessed
claimed
disputed
not_assessable
requires_future_review
```

### 8.1 `unassessed`

No repair efficacy claim has been made or evaluated.

This is the default state when a repair process completes but no separate efficacy assessment exists.

### 8.2 `claimed`

A party or process claims repair efficacy and supplies an efficacy claim.

A `claimed` status MUST NOT be treated as verified by default.

### 8.3 `disputed`

An affected party, reviewer, challenger, institution, AIITL surface, or other authorized actor contests the efficacy claim.

A disputed efficacy status MUST remain discoverable.

### 8.4 `not_assessable`

Repair efficacy cannot currently be assessed without unsafe disclosure, unavailable evidence, absent authority, unavailable affected-party process, or other named constraint.

This status MUST preserve the reason in `limitations`.

### 8.5 `requires_future_review`

The record requires later review because the effects of repair cannot yet be known, the repair requires monitoring over time, or an affected-party/community process has not yet completed.

---

## 9. Standing and Epistemic Requirements

Repair efficacy requires epistemic standing.

The harmed or affected party MUST NOT be treated merely as a data source for the system that harmed them.

A repair-efficacy assessment SHOULD ask:

- Was the affected party believed with appropriate weight?
- Did the process have the concepts needed to name the harm?
- Did the process distinguish institutional activity from repair?
- Did the repair change the conditions that produced or preserved the breach?
- Was there evidence beyond institutional self-attestation?
- Could dissent remain in the record without being treated as failure, noise, or disloyalty?
- What would count as evidence that repair did not merely perform itself?

These prompts MUST NOT be implemented as a scored rubric that automatically certifies efficacy.

---

## 10. Relationship to RFC-CDP-070

RFC-CDP-070 defines appeal and contestability entry.

This RFC adds that appeal resolution, institutional response, or procedural closure MUST NOT imply repair efficacy unless a separate Repair Efficacy Record supports that claim.

An appeal may be resolved while repair efficacy is unassessed, disputed, not assessable, or requiring future review.

---

## 11. Relationship to RFC-CDP-071

RFC-CDP-071 requires that repair claims be preserved without flattening and that repair not be treated as completed without recorded evidence.

This RFC adds that recorded evidence of completion does not automatically prove repair efficacy.

The Twenty Points pattern preserves repair points distinctly. Repair efficacy records preserve whether each point's alleged repair actually addressed the harm, without turning the list into a minimization checklist.

---

## 12. Relationship to RFC-CDP-072

RFC-CDP-072 defines breach records, repair agendas, repair points, institutional responses, repair commitments, completion evidence, affected-party review, and dissent.

This RFC updates RFC-CDP-072 by adding Repair Efficacy Record as an adjacent governed repair object.

Minimal implementations that support RFC-CDP-072 SHOULD support Repair Efficacy Record when:

- a Repair Commitment is marked completed;
- Completion Evidence is submitted;
- closure is proposed;
- affected-party review contests completion;
- institutional self-attestation is the primary evidence of completion;
- future review is required to know whether repair actually changed conditions.

---

## 13. Relationship to RFC-CDP-073

RFC-CDP-073 prevents affected-party review from being replaced by institutional approval.

This RFC adds that affected-party silence, absence, unavailability, constrained participation, or refusal MUST NOT be converted into repair efficacy.

Where affected-party review is required but absent, efficacy should normally remain `unassessed`, `not_assessable`, or `requires_future_review`, unless a governing policy and record basis explicitly support a different status while preserving limitations and dissent.

---

## 14. Relationship to RFC-CDP-092

RFC-CDP-092 defines or will define the Repair State Machine.

This RFC requires the Repair State Machine to distinguish procedural closure from repair efficacy.

A repair state machine MAY transition a repair process to a procedural terminal state while leaving repair efficacy in a non-terminal state.

Repair state machine implementations SHOULD expose efficacy state separately from repair process state.

---

## 15. Minimal Implementation Hook

The minimum non-vapor implementation hook is this:

```yaml
repair:
  completion_status: pending | completed | failed | withdrawn | superseded
  efficacy_status: unassessed | claimed | disputed | not_assessable | requires_future_review
  efficacy_claim: string | null
  efficacy_evidence_refs: []
  affected_party_standing: unknown | present | absent | constrained | disputed
  silence_policy: silence_may_pause_but_must_not_close
```

Any CDP repair record that exposes `completion_status: completed` SHOULD also expose `efficacy_status`.

If no efficacy assessment has occurred, the correct value is:

```yaml
efficacy_status: unassessed
```

The absence of `efficacy_status` MUST NOT be interpreted as `claimed`, `verified`, `accepted`, or `not_needed`.

---

## 16. Closure Rule

A repair process MAY close procedurally while repair efficacy remains unresolved only if the record explicitly preserves:

- the procedural closure basis;
- the repair efficacy status;
- known limitations;
- affected-party standing state;
- dissent or reservations;
- future review obligations, if any.

A repair process MUST NOT close in a way that implies repair efficacy when efficacy is unassessed, disputed, not assessable, or awaiting future review.

---

## 17. Security, Privacy, and Cultural Handling

Repair efficacy assessment may involve sensitive cultural, familial, legal, medical, political, identity, safety, or community-held information.

Implementations MUST NOT require unsafe disclosure merely to prove repair efficacy.

A `not_assessable` or `requires_future_review` status may be the correct result when the only way to assess efficacy would expose affected parties to harm, violate cultural protocol, or force disclosure of restricted knowledge.

---

## 18. Learning Requirements

Repair efficacy outcomes SHOULD generate learning when:

- repair completion repeatedly fails to produce efficacy;
- completion evidence repeatedly proves activity but not repair;
- affected-party silence is repeatedly misread as closure;
- efficacy assessments become compliance checklists;
- repair commitments do not change the conditions that produced breach;
- affected-party review identifies missing concepts, evidence, or authority context.

Learning MUST NOT erase breach history, dissent, limitations, or unresolved repair obligations.

---

## 19. Minimal Compliance

A minimal implementation of this RFC SHOULD support:

- Repair Efficacy Record;
- `completion_status` distinct from `efficacy_status`;
- explicit `unassessed` default when efficacy has not been evaluated;
- affected-party standing state;
- silence policy invariant;
- evidence references for efficacy claims;
- dissent references;
- limitations;
- future review state.

A minimal implementation MUST NOT treat repair completion as proof of repair efficacy.

---

## 20. Open Questions

This draft intentionally does not resolve:

- what counts as sufficient evidence of repair efficacy across domains;
- who may verify repair efficacy when affected parties are unavailable, unsafe, constrained, or absent;
- how to distinguish repair incomplete, repair refused, repair impossible, and harm irreversible;
- how the Repair State Machine should model separate procedural and efficacy states;
- whether Repair Efficacy Record should be registered as a payload type in RFC-CDP-022;
- how persistence projections in RFC-CDP-025 should query efficacy state.

These are not defects in the RFC. They are the reason the distinction needs to be made before mechanism hardens around completion.

---

## 21. Summary

Repair completion is a process state.

Repair efficacy is a legitimacy and outcome question.

CDP MUST NOT let the first pretend to answer the second.

A completed repair process is not yet proof of repair.
