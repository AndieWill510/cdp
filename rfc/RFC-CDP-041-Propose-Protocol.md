# RFC-CDP-041 — Propose Protocol

Author: Kevin “Andie” Williams  
Status: Draft v0.4  
Series: Constitutional Decision Plane (CDP)  
Date: May 24, 2026  
Updates: RFC-CDP-041 v0.3  
Depends On: RFC-CDP-021, RFC-CDP-023, RFC-CDP-024, RFC-CDP-025, RFC-CDP-030, RFC-CDP-031, RFC-CDP-033  
Related: RFC-CDP-002, RFC-CDP-022, RFC-CDP-042, RFC-CDP-045, RFC-CDP-047, RFC-CDP-090

## Abstract

Defines the canonical mechanism by which a Decision is introduced, amended, or resubmitted into CDP.

Draft v0.4 wires Propose to the Proposal Sufficiency Gate. A proposal MUST NOT advance into the ordinary Challenge lifecycle unless the Decision Lifecycle Envelope shows a valid proposal sufficiency path under RFC-CDP-024 and RFC-CDP-023.

---

## 1. Purpose

The Propose Protocol:

- creates a new Decision or amends an existing one;
- defines initial intent, scope, constraints, assumptions, rationale, and expected outcomes;
- establishes the baseline object for subsequent CDP acts;
- consumes the Proposal Sufficiency Gate result before admitting a proposal into the Challenge lifecycle.

Propose is not the formation gate itself.

Proposal formation and proposal sufficiency are governed by `RFC-CDP-024-Proposal-Sufficiency-Gate.md`.

Propose consumes the result of that gate.

---

## 2. Failure Mode: Proposal Bypass Into Challenge

The failure mode this RFC addresses is **proposal bypass into Challenge**.

Proposal bypass into Challenge occurs when a proposed decision enters the ordinary Challenge lifecycle even though the Decision Lifecycle Envelope does not show that the proposal earned admission through the Proposal Sufficiency Gate.

This is downstream of the failure mode defined in RFC-CDP-024:

```text
proposal admission without sufficiency
```

RFC-CDP-024 defines the gate.

RFC-CDP-023 indexes the gate artifacts.

RFC-CDP-041 enforces that Propose cannot proceed without them.

---

## 3. Authority and Standing

Actors invoking this protocol MUST possess authority to propose.

Authority MUST be verifiable via Identify and Attest.

Actors invoking this protocol MUST also have valid standing to participate at the Propose stage.

Standing MUST be evaluated through `RFC-CDP-033-Standing-and-Recusal-Model.md` and, where implemented, through `cdp_standing_record` as defined by `RFC-CDP-025-CDP-Persistence-Model.md`.

A proposal submitted by an actor with missing, stale, invalid, expired, blocked, or recused Propose-stage standing MUST NOT advance unless an explicit emergency exception path is invoked and recorded.

Affected-party standing MUST be protected under RFC-CDP-033. If a proposer claims affected-party standing, the system MUST NOT require proof of impact before allowing preliminary standing for proposal admission.

---

## 4. Preconditions

Before a Propose act may advance a decision into the ordinary Challenge lifecycle:

- actor identity MUST be established under RFC-CDP-030;
- relevant attestations MUST be available under RFC-CDP-031;
- Wire Message Envelope MUST conform to RFC-CDP-021;
- Decision Lifecycle Envelope MUST conform to RFC-CDP-023;
- Decision object MUST conform to the applicable Decision Object Schema;
- for new Decisions, `decision_id` MUST be unique;
- for amendments, the Decision MUST exist;
- proposer standing MUST be valid for the Propose stage;
- `proposal_sufficiency_ref` MUST be present in the Decision Lifecycle Envelope after admission;
- referenced `proposal_sufficiency_record` MUST have `sufficiency_status: sufficient` or `sufficiency_status: excepted`;
- any active formation challenge MUST be resolved, deferred under explicit authority, or reflected as blocking admission;
- APC gate requirements MUST be satisfied or deferred according to RFC-CDP-024 risk-tier rules.

---

## 5. Proposal Sufficiency Admission Rule

A Propose act MUST NOT move a decision into the ordinary Challenge lifecycle unless the Decision Lifecycle Envelope satisfies the RFC-CDP-023 admission rule:

```text
proposal_sufficiency_ref is non-null
```

and the referenced `proposal_sufficiency_record` has:

```yaml
sufficiency_status: sufficient
```

or:

```yaml
sufficiency_status: excepted
```

If `proposal_sufficiency_ref` is null, missing, stale, integrity-incomplete, insufficient, blocked, or unresolved, the Propose act MUST NOT mark the proposal as admitted.

If the sufficiency record is excepted, the exception MUST satisfy RFC-CDP-024 exception requirements, including proposer recusal from exception authority.

---

## 6. State Transitions

Draft v0.4 recognizes proposal formation and admission states from RFC-CDP-024 and RFC-CDP-023.

Allowed transitions:

```text
NULL -> formation
formation -> admission_pending
admission_pending -> admitted
admitted -> proposed
proposed -> challenge_eligible
```

Amendment or resubmission MAY follow:

```text
{allowed_state} -> formation
formation -> admission_pending
admission_pending -> admitted
admitted -> proposed
```

A proposal MUST NOT move directly from `formation` or `admission_pending` to `challenge_eligible`.

The Proposal Sufficiency Gate mediates admission.

---

## 7. Semantics

A Propose act is an offer into governance.

It does not assert truth.

It does not confer legitimacy.

It does not authorize execution.

It introduces structured intent after proposal sufficiency has been satisfied or exceptioned.

A proposal with sufficient admission may still be challenged, tested, adjudicated against, rejected, appealed, repaired, or learned from.

---

## 8. Effects

Upon successful processing:

- Decision enters `proposed` or equivalent Propose-stage state;
- Decision becomes eligible for ordinary Challenge;
- Decision Lifecycle Envelope preserves `proposal_sufficiency_ref`;
- Decision Lifecycle Envelope preserves any `formation_challenge_refs` and `apc_gate_result_refs`;
- lineage is established or extended;
- authority and standing history are updated;
- relevant governed records are referenced by the envelope and available for governed path hash coverage.

---

## 9. Payload Schema

Content-Type:

```text
application/cdp.propose+json
```

```json
{
  "proposal_type": "create | amend | resubmit",
  "title": "string",
  "description": "string",
  "objective": "string",
  "rationale": "string",
  "policy_scope": "string",
  "constraints": ["string"],
  "assumptions": ["string"],
  "expected_outcomes": ["string"],
  "risk_profile": {
    "level": "low | medium | high | critical | unknown",
    "factors": ["string"]
  },
  "required_authorities": ["PROPOSE", "CHALLENGE", "TEST", "ADJUDICATE", "LEGITIMIZE", "EXECUTE", "RECORD"],
  "proposal_sufficiency_ref": "ref",
  "formation_challenge_refs": ["ref"],
  "apc_gate_result_refs": ["ref"],
  "requested_tests": [
    {
      "test_type": "simulation | policy | empirical | precedent",
      "description": "string"
    }
  ],
  "references": ["string"],
  "attachments": ["uri"],
  "metadata": {}
}
```

---

## 10. Validation Rules

A valid Propose payload MUST:

- include title, description, and objective;
- define a policy scope;
- specify at least one required authority;
- include sufficient information for Challenge and Test;
- include `proposal_sufficiency_ref` once admitted;
- preserve `formation_challenge_refs` as a list, even when empty;
- preserve `apc_gate_result_refs` as a list, even when empty;
- reference a Decision Lifecycle Envelope that satisfies RFC-CDP-023 admission rules.

A Propose payload MUST NOT treat a summary, rationale, or narrative as a substitute for the governed `proposal_sufficiency_record`.

---

## 11. Formation Challenge Relationship

Formation challenge is governed by RFC-CDP-024, not by ordinary Challenge.

Propose MUST respect unresolved formation challenges.

If any `formation_challenge_refs` are active and unresolved, Propose MUST NOT advance the proposal into ordinary Challenge unless the formation challenge has been:

- resolved;
- sustained and remediated;
- rejected by an actor with valid standing;
- deferred under explicit authority with compensating controls;
- exceptioned under RFC-CDP-024 exception rules.

Formation challenge is distinct from ordinary Challenge because it contests admission, not merits.

---

## 12. APC Gate Relationship

APC gate results are defined in RFC-CDP-022 and governed by RFC-CDP-002 and RFC-CDP-024.

Propose MUST preserve any APC gate results relevant to proposal admission.

For high, critical, or unknown risk proposals, Propose SHOULD NOT advance unless an APC gate result required by RFC-CDP-024 is present, passed, or properly exceptioned.

For low and medium risk proposals, APC requirements MAY be staged according to RFC-CDP-024 risk-tier rules, but evidence, uncertainty, and reversibility declarations remain non-negotiable admission requirements.

---

## 13. Persistence Requirements

The Propose Protocol consumes governed artifacts persisted under RFC-CDP-025.

Implementations SHOULD persist:

- proposal records in `cdp_governed_record`;
- proposal sufficiency records in `cdp_governed_record`;
- formation challenge records in `cdp_governed_record`;
- APC gate result records in `cdp_governed_record`;
- standing enforcement projections in `cdp_standing_record`;
- envelope references in `cdp_envelope_ref`.

A Propose act SHOULD NOT be considered fully processed until the Decision Lifecycle Envelope references the relevant governed records.

---

## 14. Idempotency

Repeated Propose messages with identical `message_id` SHOULD be treated as idempotent.

Repeated Propose messages MUST NOT create duplicate proposal sufficiency references or duplicate admission transitions.

If a repeated Propose message refers to different sufficiency, formation challenge, or APC gate records under the same `message_id`, the message MUST be treated as conflicting, not idempotent.

---

## 15. Security and Governance Considerations

Proposal payloads and sufficiency artifacts may contain sensitive evidence, affected-party information, uncertainty analysis, exception rationale, and authority claims.

Implementations SHOULD address:

- proposer standing;
- affected-party standing protection;
- formation challenge visibility;
- APC gate visibility;
- exception abuse;
- stale or invalid standing projections;
- admission bypass attempts;
- summary substitution;
- governed path hash coverage;
- repair and appeal hooks.

---

## 16. Status of This Draft

Promoted into Draft v0.4:

- corrected canonical heading to RFC-CDP-041;
- updated dependencies to current RFC numbering;
- proposal bypass into Challenge as failure mode;
- Proposal Sufficiency Gate admission rule;
- proposer standing check requirement;
- formation challenge relationship;
- APC gate relationship;
- persistence relationship to RFC-CDP-025;
- idempotency protection against duplicate or conflicting sufficiency references.

Deferred:

- detailed formation challenge standing rules;
- full Challenge Protocol patch;
- full Legitimize Protocol APC wiring;
- lifecycle state machine alignment;
- risk classification mechanism.

---

## 17. Principle

Propose defines the world only after formation has earned admission.

Learn later corrects the world.

Challenge tests whether the proposal should survive.

Proposal Sufficiency determines whether the proposal may enter.
