# RFC-CDP-022 — Protocol Payload Schema Registry

Author: Kevin “Andie” Williams  
Status: Draft v0.5  
Series: Constitutional Decision Plane (CDP)  
Date: May 24, 2026  
Updates: RFC-CDP-015 legacy numbering  
Depends On: RFC-CDP-002, RFC-CDP-024, RFC-CDP-025

## Abstract

Defines payload schemas and registered payload families for Propose, Challenge, Test, Adjudicate, Legitimize, Execute, Record, Learn, Nemawashi, and cross-cutting governance gates.

This RFC also defines the Anti-Premature-Certainty gate result payload used by proposal sufficiency, challenge, legitimization, record, and learning flows.

## 1. Purpose

This RFC answers what each protocol payload contains and standardizes the act-specific body inside the common Envelope.

It also registers named cross-cutting payload types used by multiple protocols.

## 2. Guidance

Each payload schema SHOULD:

- define required fields;
- include `metadata` as extension space;
- reference artifacts by stable identifier;
- avoid duplicating universal Envelope fields.

Payload schemas MUST NOT silently redefine universal envelope semantics.

## 3. Payload Families

### Propose

`proposal_type, title, description, objective, policy_scope, required_authorities`

### Challenge

`challenge_type, severity, argument, requested_action`

### Test

`test_type, claim, method, result`

### Adjudicate

`disposition, rationale, considered_refs`

### Legitimize

`status, basis, scope, expiry`

### Execute

`target, authorization_ref, idempotency_key`

### Record

`record_ref, artifact_refs, summary`

### Learn

`observed_outcome, lessons, recommended_changes`

### Nemawashi

`stakeholders, positions, alignment_status, open_issues`

## 4. Cross-Cutting Gate Payloads

### 4.1 Anti-Premature-Certainty Gate Result

Payload name:

```text
anti_premature_certainty_gate_result
```

Status:

```text
Defined — Draft v0.5
```

Defined by:

```text
RFC-CDP-002-Anti-Premature-Certainty-Principle.md
RFC-CDP-024-Proposal-Sufficiency-Gate.md
```

Persisted by:

```text
RFC-CDP-025-CDP-Persistence-Model.md
```

Purpose:

Records the result of evaluating whether a decision, proposal, or gate has prematurely collapsed uncertainty, alternatives, dissent, stakeholder impact, reversibility, or acceptance threshold before the required sufficiency conditions have been met.

This payload exists so Propose, Proposal Sufficiency, Challenge, Legitimize, Record, and Learn can reference the same gate-result object rather than inventing separate shapes.

### 4.1.1 Failure Modes

This payload supports detection and recording of two related failure modes defined by RFC-CDP-002 and RFC-CDP-024:

1. **Procedural bypass** — required sufficiency checks were skipped, rushed, or bypassed.
2. **Certainty performance** — sufficiency fields exist but perform inquiry without representing genuine inquiry.

The payload can record field presence and evaluator findings.

It cannot by itself prove that inquiry was genuine.

That requires adversarial review, formation challenge, Challenge, Learn-stage review, or other CDP governance mechanisms.

### 4.1.2 Canonical Draft Schema

```yaml
anti_premature_certainty_gate_result:
  gate_id: <uuid>
  decision_id: <uuid>
  evaluated_at: <timestamp>
  evaluator: <actor_ref>
  evaluator_standing_record_ref: <ref|null>
  risk_tier: <low|medium|high|critical|unknown>
  gate_context: <proposal_admission|challenge_closure|legitimize|execute|learn|other>
  passed: <boolean>

  criteria:
    evidence:
      status: <pass|fail|waived|not_applicable|unknown>
      record_refs: [<ref>]
      notes: <string|null>
    uncertainty:
      status: <pass|fail|waived|not_applicable|unknown>
      record_refs: [<ref>]
      notes: <string|null>
    alternatives:
      status: <pass|fail|waived|not_applicable|unknown>
      record_refs: [<ref>]
      notes: <string|null>
    dissent:
      status: <pass|fail|waived|not_applicable|unknown>
      record_refs: [<ref>]
      notes: <string|null>
    stakeholder_impact:
      status: <pass|fail|waived|not_applicable|unknown>
      record_refs: [<ref>]
      notes: <string|null>
    reversibility:
      status: <pass|fail|waived|not_applicable|unknown>
      record_refs: [<ref>]
      notes: <string|null>
    threshold:
      status: <pass|fail|waived|not_applicable|unknown>
      record_refs: [<ref>]
      notes: <string|null>

  failures: [<string>]
  unwaived_failures: [<string>]

  waivers:
    - criterion: <evidence|uncertainty|alternatives|dissent|stakeholder_impact|reversibility|threshold>
      authority: <actor_ref>
      authority_standing_record_ref: <ref|null>
      reason: <string>
      expires_at: <timestamp|null>
      proposer_recused: <boolean>

  exception_invoked: <boolean>
  exception_ref: <ref|null>
  learn_review_required: <boolean>
  proposal_sufficiency_record_ref: <ref|null>
  formation_challenge_refs: [<ref>]
  record_ref: <ref>
  record_hash: <hash|null>
  lineage_refs: [<ref>]
```

### 4.1.3 Required Fields

The following fields are required in Draft v0.5:

- `gate_id`
- `decision_id`
- `evaluated_at`
- `evaluator`
- `risk_tier`
- `gate_context`
- `passed`
- `criteria`
- `failures`
- `unwaived_failures`
- `waivers`
- `exception_invoked`
- `learn_review_required`
- `record_ref`
- `lineage_refs`

`record_hash` is nullable in Draft v0.5 because record-hash propagation to governed record RFCs remains a separate open work item.

### 4.1.4 Criterion Status Values

Allowed criterion status values:

```text
pass | fail | waived | not_applicable | unknown
```

A criterion marked `waived` MUST have a corresponding waiver entry.

A criterion marked `unknown` MUST NOT be treated as passed.

### 4.1.5 Pass Rule

`passed` MUST be `false` if `unwaived_failures` is non-empty.

`passed` MUST be `false` if any required criterion has status `fail` or `unknown` and no valid waiver exists.

A payload with `passed: true` means the APC gate passed for the stated `gate_context` and risk tier.

It does not mean the decision is legitimate.

Legitimacy is governed by the applicable lifecycle protocols, especially Legitimize, Standing, Decision Lifecycle Envelope, and Repair/Appeal mechanisms.

### 4.1.6 Waiver and Exception Constraints

Waivers MUST identify the criterion waived, authority, reason, expiration when applicable, and whether the proposer was recused.

The proposer MUST NOT authorize their own APC waiver or exception.

Every APC exception MUST set:

```text
learn_review_required: true
```

This preserves the RFC-CDP-002 requirement that exceptions are reviewed at Learn stage.

### 4.1.7 Persistence Requirements

When persisted, this payload SHOULD be stored as a governed record in `cdp_governed_record` under `RFC-CDP-025` with:

```text
record_type: anti_premature_certainty_gate_result
```

The payload SHOULD be referenced by the Decision Lifecycle Envelope when used for proposal admission, challenge closure, legitimization, execution, record, or learning.

### 4.1.8 Downstream Use

Downstream RFCs MAY reference this Draft-compatible payload before it is Accepted.

However, any downstream RFC requiring this payload as a blocking precondition MUST state:

- which `gate_context` is required;
- which risk tiers require it;
- whether exceptions are allowed;
- which standing checks apply to the evaluator and waiver authority;
- how failures block lifecycle advancement.

## 5. Content Types

Default encodings SHOULD use structured syntax suffixes:

- `application/cdp.propose+json`
- `application/cdp.challenge+json`
- `application/cdp.test+json`
- `application/cdp.apc-gate-result+json`

Alternate encodings MAY be supported if schema semantics are preserved.

## 6. Principle

Envelope fields are universal.

Payload fields are act-specific or gate-specific.

Payload schemas MUST NOT silently redefine universal envelope semantics.

## 7. Open Questions

1. Should `proposal_sufficiency_record` be registered as its own payload type?
2. Should `formation_challenge_record` be registered as its own payload type?
3. Should `record_hash` be made mandatory after record-hash propagation is complete?
4. Should APC criteria be represented as a list rather than a fixed object to allow domain-specific extensions?
5. Should `gate_context` values be moved into `cdp_controlled_vocabulary` under RFC-CDP-025?

## 8. Legacy Note

This file previously carried the title `RFC-CDP-015 — Protocol Payload Schemas` after renumbering.

Draft v0.4 updated the heading to match the canonical filename and Series Index entry.

Draft v0.5 promotes `anti_premature_certainty_gate_result` from Reserved to Defined Draft payload.
