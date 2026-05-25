# RFC-CDP-042 — Challenge Protocol

Author: Kevin “Andie” Williams  
Status: Draft v0.4  
Series: Constitutional Decision Plane (CDP)  
Date: May 24, 2026  
Updates: RFC-CDP-042 v0.3  
Depends On: RFC-CDP-021, RFC-CDP-023, RFC-CDP-024, RFC-CDP-025, RFC-CDP-030, RFC-CDP-031, RFC-CDP-033, RFC-CDP-041  
Related: RFC-CDP-002, RFC-CDP-022, RFC-CDP-043, RFC-CDP-044, RFC-CDP-045, RFC-CDP-047, RFC-CDP-048, RFC-CDP-070

## Abstract

Defines structured dissent, critique, and adversarial pressure for admitted CDP proposals.

Draft v0.4 defines the boundary between ordinary Challenge and Formation Challenge.

Formation Challenge is an upstream act governed by `RFC-CDP-024-Proposal-Sufficiency-Gate.md`. It contests whether something has earned admission as a proposal.

Ordinary Challenge is governed by this RFC. It contests an admitted proposal on its merits, evidence, risks, policy, ethics, operations, assumptions, or consequences.

---

## 1. Purpose

The Challenge Protocol MUST:

- introduce structured dissent;
- expose weaknesses in an admitted proposal;
- require clarification, amendment, evidence, test, rejection, or repair;
- enforce deliberation prior to adjudication;
- preserve material dissent in the governed path.

Challenge is not optional.

Silence MUST NOT be interpreted as agreement.

---

## 2. Failure Mode: Challenge Surface Confusion

The failure mode this RFC addresses is **challenge surface confusion**.

Challenge surface confusion occurs when upstream formation defects and downstream proposal-merit objections are treated as the same kind of challenge.

This causes at least three governance failures:

1. **Admission defects are laundered into deliberation.** A malformed proposal is treated as admitted and challengers are forced to repair formation defects during ordinary Challenge.
2. **Standing rules drift.** Formation challengers and ordinary challengers may have different standing surfaces, but a merged challenge model hides that distinction.
3. **Outcome options blur.** Formation Challenge may return a proposal to formation; ordinary Challenge may clarify, amend, test, block, reject, or escalate.

RFC-CDP-024 owns Formation Challenge.

RFC-CDP-042 owns ordinary Challenge.

---

## 3. Boundary with Formation Challenge

Formation Challenge and ordinary Challenge are distinct.

### 3.1 Formation Challenge

Formation Challenge asks:

> Has this earned admission as a proposal?

It is raised before or during proposal admission.

It targets proposal sufficiency, proposer standing, missing evidence, missing uncertainty, affected-party impact, reversibility, APC gate defects, or invalid exception authority.

It may result in:

- return to formation;
- request missing evidence;
- require uncertainty disclosure;
- require stakeholder impact analysis;
- require APC gate result;
- block admission;
- allow exception with controls.

Formation Challenge is governed by RFC-CDP-024.

### 3.2 Ordinary Challenge

Ordinary Challenge asks:

> Should this admitted proposal survive adversarial scrutiny?

It is raised after proposal admission.

It targets the admitted proposal's logic, evidence, policy fit, ethics, operational viability, risk, testability, authority, consequences, or repair implications.

It may result in:

- clarification;
- amendment;
- additional evidence;
- test requirement;
- blocking challenge;
- counterproposal;
- rejection recommendation;
- repair or appeal trigger.

Ordinary Challenge is governed by this RFC.

### 3.3 Non-Substitution Rule

A Formation Challenge MUST NOT be used as a substitute for ordinary Challenge.

An ordinary Challenge MUST NOT be used to paper over a missing or unresolved Proposal Sufficiency Gate.

If a proposal has not been admitted under RFC-CDP-024 and RFC-CDP-023, ordinary Challenge MUST NOT proceed except to record that admission is invalid or blocked.

---

## 4. Authority and Standing

Actors invoking ordinary Challenge MUST possess Challenge authority or recognized Challenge standing.

The system MUST ensure that Challenge authority is not artificially restricted.

Challenge standing MUST be evaluated in relation to the admitted proposal, affected parties, evidence custody, domain expertise, governance authority, repair rights, or other recognized standing bases under RFC-CDP-033.

Affected-party standing MUST be protected.

No actor may deny affected-party Challenge standing merely because impact has not yet been proven.

---

## 5. Preconditions

Before ordinary Challenge may proceed:

- a Decision MUST exist;
- the proposal MUST be admitted under RFC-CDP-024;
- the Decision Lifecycle Envelope MUST include `proposal_sufficiency_ref` under RFC-CDP-023;
- the referenced `proposal_sufficiency_record` MUST have `sufficiency_status: sufficient` or `sufficiency_status: excepted`;
- unresolved formation challenges MUST be resolved, sustained and remediated, rejected by a valid authority, or explicitly deferred with compensating controls;
- Envelope, identity, standing, and attestation MUST validate;
- any relevant APC gate result required by RFC-CDP-024 MUST be present, passed, or properly exceptioned.

---

## 6. Mandatory Deliberation Gate

A Decision MUST NOT proceed to Adjudication unless:

- at least one ordinary Challenge has been recorded; or
- a formal `no challenge` condition has been explicitly attested under policy.

Silence MUST NOT be interpreted as agreement.

A `no challenge` attestation MUST NOT be used when:

- affected-party standing has been denied or unresolved;
- material dissent exists but has not been recorded;
- proposal sufficiency is unresolved;
- a blocking Formation Challenge remains active;
- a required APC gate result is failed, missing, or exceptioned without valid authority.

---

## 7. State Transitions

Ordinary Challenge state transitions:

```text
admitted -> under_challenge
under_challenge -> under_challenge
under_challenge -> challenge_resolved
under_challenge -> challenge_blocked
```

Challenge MUST NOT advance the lifecycle to Adjudication by itself.

It deepens, blocks, or conditions progression.

---

## 8. Payload Schema

Content-Type:

```text
application/cdp.challenge+json
```

```json
{
  "challenge_type": "logical | evidentiary | policy | ethical | operational | authority | standing | repair | apc | other",
  "severity": "low | medium | high | blocking",
  "target": {
    "field": "string",
    "reference": "optional pointer"
  },
  "argument": "string",
  "requested_action": "clarify | amend | provide_evidence | run_test | reject | block | repair | escalate",
  "proposal_sufficiency_ref": "ref",
  "formation_challenge_refs": ["ref"],
  "apc_gate_result_refs": ["ref"],
  "requested_tests": [
    {
      "test_type": "simulation | empirical | policy | precedent",
      "description": "string"
    }
  ],
  "counterproposal": {
    "description": "optional",
    "rationale": "optional"
  },
  "evidence_refs": ["string"],
  "impact_assessment": {
    "risk": "low | medium | high | critical",
    "scope": "local | domain | systemic"
  },
  "metadata": {}
}
```

---

## 9. Challenge Types

Draft v0.4 recognizes the following ordinary Challenge types:

| Type | Meaning |
|---|---|
| `logical` | Challenges reasoning, inference, or internal consistency. |
| `evidentiary` | Challenges evidence sufficiency, quality, provenance, or interpretation. |
| `policy` | Challenges alignment with policy, rule, authority, or constraint. |
| `ethical` | Challenges harm, fairness, dignity, equity, erasure, or relational consequences. |
| `operational` | Challenges feasibility, implementation, resilience, or operational risk. |
| `authority` | Challenges whether claimed authority is valid. |
| `standing` | Challenges whether an actor has valid standing or whether recusal applies. |
| `repair` | Challenges whether appeal, repair, breach, or affected-party review is required. |
| `apc` | Challenges premature certainty, failed APC criteria, waivers, exceptions, or sufficiency performance that survived admission. |
| `other` | Reserved for extension or implementation-profile use. |

Formation Challenge is not listed as an ordinary Challenge type because it is owned by RFC-CDP-024.

---

## 10. Severity Enforcement

If a Challenge is marked `blocking`, the Decision MUST NOT advance to Adjudication until:

- the Challenge is resolved; or
- the Challenge is explicitly adjudicated as non-blocking by an actor with valid standing and authority.

A blocking Challenge MUST be referenced in the Decision Lifecycle Envelope and covered by governed path hash manifest rules.

---

## 11. APC Relationship

Ordinary Challenge MAY include `challenge_type: apc` when a challenger contests premature certainty after proposal admission.

An APC Challenge may contest:

- failed or waived APC criteria;
- missing evidence;
- inadequate uncertainty disclosure;
- inadequate alternatives analysis;
- collapsed dissent;
- inadequate stakeholder impact analysis;
- inadequate reversibility path;
- improper threshold definition;
- invalid APC exception authority;
- sufficiency performance that passed the Proposal Sufficiency Gate cosmetically.

If an APC Challenge is sustained, the relevant APC gate result SHOULD be updated, superseded, or linked to a new governed record.

---

## 12. Formation Challenge Reference Rule

Ordinary Challenge payloads SHOULD carry `formation_challenge_refs` when relevant.

These references preserve the admission history that shaped the admitted proposal.

If a formation challenge was sustained and remediated, the ordinary Challenge record SHOULD reference the remediation when relevant.

If a formation challenge was deferred under exception, ordinary Challenge MAY challenge the validity or sufficiency of that deferral.

---

## 13. Determinism Guarantee

CDP does not enforce deterministic outcomes.

CDP MUST enforce deterministic process:

- all valid Challenges are processed;
- all blocking Challenges are resolved or adjudicated as non-blocking;
- all decisions pass through adversarial scrutiny unless a formal no-challenge condition is validly attested;
- all material dissent is preserved;
- all unresolved blocking conditions are visible in the governed path.

---

## 14. Persistence Requirements

Challenge records SHOULD be stored as governed records under RFC-CDP-025.

The Decision Lifecycle Envelope SHOULD reference ordinary Challenge records through `stage_record_refs.challenge_refs`.

Challenge records SHOULD reference relevant:

- `proposal_sufficiency_ref`;
- `formation_challenge_refs`;
- `apc_gate_result_refs`;
- evidence records;
- standing records;
- repair or appeal records when applicable.

---

## 15. Security and Governance Considerations

Challenge records may contain sensitive dissent, affected-party claims, evidence disputes, ethical objections, authority disputes, and repair triggers.

Implementations SHOULD protect challengers from retaliation, preserve affected-party review rights, support redaction where necessary, and avoid suppressing material dissent through summary substitution.

Challenge suppression, artificial restriction of Challenge authority, or failure to process valid blocking Challenges may constitute a governance breach.

---

## 16. Status of This Draft

Promoted into Draft v0.4:

- corrected canonical heading from legacy RFC-CDP-003 to RFC-CDP-042;
- updated dependencies to current RFC numbering;
- challenge surface confusion as failure mode;
- clear boundary between Formation Challenge and ordinary Challenge;
- non-substitution rule;
- proposal admission preconditions before ordinary Challenge;
- APC Challenge type for post-admission premature-certainty objections;
- formation challenge reference rule;
- updated persistence requirements.

Deferred:

- detailed standing rules for ordinary challengers;
- formal no-challenge attestation schema;
- downstream Adjudicate Protocol handling of blocking challenges;
- record_hash propagation for challenge records;
- challenge state machine alignment.

---

## 17. Principle

The universe may be probabilistic.

The court is not.

Challenge does not create legitimacy.

Challenge prevents legitimacy theater.
