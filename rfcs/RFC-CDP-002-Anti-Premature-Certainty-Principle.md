# RFC-CDP-002 — Anti-Premature-Certainty Principle

Author: Kevin “Andie” Williams / ChatGPT
Status: Draft
Series: Constitutional Decision Plane (CDP)
Date: 2026-05-23
Intended Band: `000–009` — Series / Constitutional Frame
Canonical Target: `rfc/RFC-CDP-002-Anti-Premature-Certainty-Principle.md`
Current Location: `rfcs/` staging lane pending canonical RFC migration
Updates: `RFC-CDP-001-Vision-Scope-Principles` once promoted
Depends On: `RFC-CDP-041-Propose-Protocol`, `RFC-CDP-042-Challenge-Protocol`, `RFC-CDP-043-Test-Protocol`, `RFC-CDP-044-Adjudicate-Protocol`, `RFC-CDP-045-Legitimize-Protocol`, `RFC-CDP-047-Record-Protocol`

---

## Abstract

This RFC defines the Anti-Premature-Certainty Principle for CDP.

A CDP-governed system MUST NOT collapse ambiguity, uncertainty, dissent, or unresolved stakeholder impact into a final or executable decision before the system has passed explicit sufficiency checks.

Informally:

> Premature certainty is a control-plane defect.

The principle is falsifiable. A decision can be tested for premature certainty by inspecting whether evidence, alternatives, dissent, uncertainty, reversibility, stakeholder impact, and decision thresholds were recorded before legitimation or execution.

---

## 1. Motivation

Governance systems often fail by resolving ambiguity too early.

This failure is not merely rhetorical. It creates operational, ethical, legal, and architectural risk. A system that treats an under-tested conclusion as settled can:

- erase dissent;
- hide uncertainty;
- bypass affected parties;
- overfit to institutional convenience;
- execute actions without sufficient authority;
- produce audit trails that explain decisions without legitimizing them.

CDP exists to make decisions contestable, auditable, accountable, replayable, and legitimate. Premature certainty undermines each of these properties.

The Anti-Premature-Certainty Principle therefore converts a cultural warning into an enforceable decision-control requirement.

---

## 2. Principle

A CDP-governed system MUST NOT treat a decision as legitimate until the system can prove that:

1. supporting evidence was recorded;
2. viable alternatives were considered or explicitly waived;
3. challenge, dissent, or adversarial review occurred or was explicitly waived;
4. uncertainty was surfaced in bounded, inspectable form;
5. stakeholder impact was identified;
6. reversibility, appeal, rollback, or compensation paths were defined;
7. the decision threshold was defined before the conclusion was finalized.

A decision that cannot satisfy these conditions MUST remain in a non-final state unless an explicit, auditable exception is recorded.

---

## 3. Normative Language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are to be interpreted as normative requirements for CDP-conformant implementations.

---

## 4. Definition: Premature Certainty

A decision exhibits premature certainty when it asserts finality, legitimacy, confidence, authority, or executability before the required decision record can demonstrate procedural sufficiency.

A decision is prematurely certain if one or more of the following conditions is true:

| Test | Failure condition |
|---|---|
| Evidence test | No evidence, source lineage, precedent, or policy basis is recorded. |
| Alternatives test | No viable alternatives are recorded, compared, or waived. |
| Challenge test | No dissent, objection, counterargument, or adversarial review is recorded. |
| Uncertainty test | Confidence is asserted without uncertainty bounds or unresolved-question tracking. |
| Stakeholder-impact test | Affected parties, downstream risks, or externalized harms are not identified. |
| Reversibility test | No appeal, rollback, compensation, or repair path is stated. |
| Threshold test | Decision criteria or approval thresholds were defined after the conclusion or not at all. |

---

## 5. Decision Gate

A CDP implementation MUST evaluate the Anti-Premature-Certainty Gate before a decision can transition into `legitimated`, `execution_eligible`, or equivalent finalizing states.

The gate MUST return:

```yaml
anti_premature_certainty_gate:
  passed: true | false
  failures: []
  waivers: []
  evaluated_at: timestamp
  evaluator: actor_ref
  record_ref: record_ref
```

If `passed` is `false`, the decision MUST NOT be promoted unless an exception path is invoked.

---

## 6. Required Decision Record Fields

A CDP decision record SHOULD include at least the following fields:

```yaml
decision_id: string
decision_state: proposed | challenged | tested | adjudicated | legitimated | execution_eligible | executed | recorded | appealed | repaired
claim: string
confidence_level: low | medium | high | unknown
uncertainty_summary: string
unresolved_questions:
  - question: string
    owner: actor_ref | null
    disposition: open | accepted_risk | resolved | deferred

evidence_refs:
  - ref: string
    type: policy | data | precedent | testimony | test_result | analysis | other
    lineage: string | null

alternatives_considered:
  - alternative: string
    disposition: accepted | rejected | deferred | waived
    rationale: string

objections_recorded:
  - objection_id: string
    raised_by: actor_ref | role_ref | null
    summary: string
    disposition: sustained | rejected | mitigated | deferred | unresolved

stakeholders_affected:
  - stakeholder: actor_ref | group_ref | system_ref
    impact_summary: string
    risk_level: low | medium | high | unknown

reversibility_plan:
  rollback_available: true | false
  appeal_path: string | null
  compensation_path: string | null
  repair_path: string | null

decision_threshold:
  threshold_defined_at: timestamp
  threshold_type: quorum | confidence | risk | authority | policy | custom
  threshold_value: string
  met: true | false

anti_premature_certainty_gate:
  passed: true | false
  failures: []
  waivers: []
```

---

## 7. Waivers and Exceptions

Some operational contexts require action under incomplete certainty.

CDP MAY allow an explicit exception path, but the exception MUST be recorded. An exception MUST NOT silently convert an under-supported decision into a legitimate decision.

An exception record MUST include:

```yaml
exception_requested: true
exception_reason: string
exception_scope: string
exception_authority: actor_ref | role_ref
exception_expires_at: timestamp | null
accepted_risks:
  - string
required_follow_up:
  - action: string
    due_at: timestamp | null
```

Exceptions SHOULD be temporary, scoped, reviewable, and reversible wherever possible.

---

## 8. State-Machine Requirement

A CDP implementation MUST prevent direct transition from `proposed` to `legitimated` or `execution_eligible` unless the Anti-Premature-Certainty Gate passes or an exception record is present.

Recommended transition constraint:

```text
proposed
  -> challenged
  -> tested
  -> adjudicated
  -> anti_premature_certainty_gate
  -> legitimated
  -> execution_eligible
```

Emergency paths MAY bypass intermediate states only if the exception record is preserved and later review is mandatory.

---

## 9. Falsifiability

This RFC is falsifiable because an implementation can be tested against observable records.

A conformant test suite can assert:

1. A decision without evidence cannot pass the gate.
2. A decision without alternatives cannot pass unless alternatives are explicitly waived.
3. A decision without challenge cannot pass unless challenge is explicitly waived.
4. A decision without uncertainty tracking cannot pass.
5. A decision without stakeholder impact cannot pass.
6. A decision without reversibility, appeal, compensation, or repair cannot pass.
7. A decision without a pre-defined threshold cannot pass.
8. A waiver must be recorded as a waiver, not as ordinary legitimacy.
9. Execution must be blocked when the gate fails.
10. The record must remain replayable after the decision is finalized.

---

## 10. Reference Implementation Sketch

```python
def anti_premature_certainty_gate(decision: dict) -> dict:
    failures = []

    if not decision.get("evidence_refs"):
        failures.append("missing_evidence_lineage")

    if not decision.get("alternatives_considered"):
        failures.append("missing_alternatives")

    if not decision.get("objections_recorded"):
        failures.append("missing_challenge_or_dissent")

    if not decision.get("uncertainty_summary"):
        failures.append("missing_uncertainty_summary")

    if not decision.get("stakeholders_affected"):
        failures.append("missing_stakeholder_impact")

    reversibility = decision.get("reversibility_plan") or {}
    if not any([
        reversibility.get("rollback_available"),
        reversibility.get("appeal_path"),
        reversibility.get("compensation_path"),
        reversibility.get("repair_path"),
    ]):
        failures.append("missing_reversibility_or_repair_path")

    threshold = decision.get("decision_threshold") or {}
    if not threshold.get("threshold_defined_at") or not threshold.get("threshold_type"):
        failures.append("missing_predefined_decision_threshold")

    waivers = decision.get("waivers") or []
    unwaived_failures = [
        failure for failure in failures
        if failure not in {waiver.get("failure") for waiver in waivers}
    ]

    return {
        "passed": len(unwaived_failures) == 0,
        "failures": failures,
        "unwaived_failures": unwaived_failures,
        "waivers": waivers,
    }
```

---

## 11. Conformance Levels

### Level 0 — Non-conformant

The system may assert final decisions without evidence, challenge, uncertainty, stakeholder impact, or reversibility.

### Level 1 — Advisory

The system reports missing sufficiency fields but does not block promotion or execution.

### Level 2 — Gated

The system blocks promotion to legitimation or execution eligibility unless the gate passes or an explicit waiver is recorded.

### Level 3 — Auditable and Replayable

The system preserves all gate inputs, failures, waivers, thresholds, and reviewer actions in a replayable decision record.

### Level 4 — Adaptive

The system learns from premature-certainty failures, updates templates, improves prompts, tunes review thresholds, and reports recurring institutional failure modes.

---

## 12. Security and Governance Considerations

Premature certainty can be exploited.

An attacker, rushed operator, poorly governed agent, or institutionally incentivized actor may try to force a decision into finality before objections, affected parties, or contradictory evidence are visible.

CDP implementations SHOULD treat repeated premature-certainty failures as control-plane risk signals.

Examples include:

- repeated omission of dissent;
- recurring waiver of stakeholder impact;
- confidence inflation without test evidence;
- emergency exceptions becoming normal workflow;
- thresholds being defined after conclusions.

These patterns SHOULD trigger review, audit, or governance escalation.

---

## 13. Relationship to CDP Planes

### Decision Plane

The principle gates ordinary decision lifecycle promotion.

### Execution Plane

The principle prevents legitimation from becoming automatic action when sufficiency has not been demonstrated.

### Covenant Plane

The principle protects context, dissent, boundaries, and relationship-specific obligations from being flattened into administrative certainty.

### Repair Plane

The principle preserves appeal, compensation, and repair pathways when decisions affect parties who may later contest the legitimacy of the decision.

---

## 14. Design Note

The phrase “premature certainty is violence in a blazer” is preserved here as design shorthand, not as normative protocol language.

Its engineering translation is:

> Certainty must be earned through protocol.

A CDP system SHOULD make premature certainty visible, testable, blockable, reviewable, and repairable.

---

## 15. Open Questions

1. Should this RFC remain in the constitutional frame band as `002`, or move to the covenant band as a schema-drift/context-preservation control?
2. Should the gate be mandatory for all decisions, or only decisions above a risk, impact, autonomy, or authority threshold?
3. Should “alternatives considered” be waived for routine low-risk operational decisions?
4. Should the gate be represented as a standalone protocol payload type in the Protocol Payload Schema Registry?
5. Should premature-certainty failures become first-class learning events in the Learn Protocol?

---

## 16. Review Instructions for C

Reviewer should read:

1. the CDP README and RFC numbering bands;
2. the Covenant / AIITL material, especially bounded human-AI collaboration, schema drift, context preservation, and role boundaries;
3. this RFC as a proposed constitutional-frame principle.

Reviewer should specifically assess:

- whether `002` is the correct future canonical number;
- whether this belongs in the `000–009` constitutional band or the `060–069` covenant band;
- whether the gate criteria are too strict for low-risk decisions;
- whether waiver semantics are sufficiently auditable;
- whether this should update the Legitimize Protocol, Record Protocol, or Governance State Machine.
