# RFC-CDP-022 — Protocol Payload Schema Registry

Author: Kevin “Andie” Williams  
Status: Draft v0.6  
Series: Constitutional Decision Plane (CDP)  
Date: June 25, 2026  
Updates: RFC-CDP-022 v0.5; RFC-CDP-015 legacy numbering  
Depends On: RFC-CDP-002, RFC-CDP-024, RFC-CDP-025  
Related: RFC-CDP-021, RFC-CDP-023, RFC-CDP-041, RFC-CDP-042, RFC-CDP-045, RFC-CDP-047, RFC-CDP-048

## Abstract

This RFC defines the Protocol Payload Schema Registry for CDP.

The registry names payload families and cross-cutting governed record payloads used by Wire Message Envelopes, lifecycle protocols, persistence records, and downstream governance gates.

Draft v0.6 registers the proposal-admission governed record payloads that were defined by RFC-CDP-024 and indexed by RFC-CDP-023:

```text
proposal_sufficiency_record
formation_challenge_record
```

This prevents proposal sufficiency and formation challenge records from existing as unregistered shapes while downstream lifecycle RFCs already depend on them.

---

## 1. Purpose

The Protocol Payload Schema Registry answers:

- what payload families are recognized by CDP;
- which payload names may be carried in the Wire Message Envelope `payload_type` field;
- which governed record payloads are shared across protocol stages;
- which RFC owns the semantics of a registered payload;
- how downstream protocols may reference Draft-compatible payloads without inventing new shapes.

A registered payload name does not by itself make a decision valid, sufficient, legitimate, executable, or correct.

Registration creates a stable name and boundary for a governed artifact.

---

## 2. Boundary with Envelope, Lifecycle, and Persistence

This registry does not define the Wire Message Envelope.

The Wire Message Envelope is defined by RFC-CDP-021 and carries `payload_type` plus `payload` for a single protocol act.

This registry does not define the Decision Lifecycle Envelope.

The Decision Lifecycle Envelope is defined by RFC-CDP-023 and indexes governed records across a decision lifecycle.

This registry does not define persistence tables.

The CDP Persistence Model is defined by RFC-CDP-025.

A registered payload may be:

1. carried directly in a Wire Message Envelope;
2. persisted as a governed record under RFC-CDP-025;
3. referenced by the Decision Lifecycle Envelope under RFC-CDP-023;
4. consumed by lifecycle protocols such as Propose, Challenge, Legitimize, Record, or Learn.

These are related uses. They MUST NOT be conflated.

---

## 3. Registry Guidance

Each payload schema SHOULD:

- define required fields;
- include `metadata` or an equivalent extension space when appropriate;
- reference artifacts by stable identifier;
- avoid duplicating universal Wire Message Envelope fields;
- identify its semantic owner RFC;
- identify persistence and envelope relationships when known.

Payload schemas MUST NOT silently redefine universal envelope semantics.

A payload registry entry MAY point to another RFC for the normative schema when that RFC owns the governed act or gate semantics.

---

## 4. Payload Families

### 4.1 Propose

Baseline payload fields:

```text
proposal_type, title, description, objective, policy_scope, required_authorities
```

### 4.2 Challenge

Baseline payload fields:

```text
challenge_type, severity, argument, requested_action
```

### 4.3 Test

Baseline payload fields:

```text
test_type, claim, method, result
```

### 4.4 Adjudicate

Baseline payload fields:

```text
disposition, rationale, considered_refs
```

### 4.5 Legitimize

Baseline payload fields:

```text
status, basis, scope, expiry
```

### 4.6 Execute

Baseline payload fields:

```text
target, authorization_ref, idempotency_key
```

### 4.7 Record

Baseline payload fields:

```text
record_ref, artifact_refs, summary
```

### 4.8 Learn

Baseline payload fields:

```text
observed_outcome, lessons, recommended_changes
```

### 4.9 Nemawashi

Baseline payload fields:

```text
stakeholders, positions, alignment_status, open_issues
```

---

## 5. Cross-Cutting Gate and Record Payloads

### 5.1 Anti-Premature-Certainty Gate Result

Payload name:

```text
anti_premature_certainty_gate_result
```

Status:

```text
Defined — Draft v0.6
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

Indexed by:

```text
RFC-CDP-023-Decision-Lifecycle-Envelope.md
```

Purpose:

Records the result of evaluating whether a decision, proposal, or gate has prematurely collapsed uncertainty, alternatives, dissent, stakeholder impact, reversibility, or acceptance threshold before required sufficiency conditions have been met.

This payload exists so Propose, Proposal Sufficiency, Challenge, Legitimize, Record, and Learn can reference the same gate-result object rather than inventing separate shapes.

#### 5.1.1 Failure Modes

This payload supports detection and recording of two related failure modes defined by RFC-CDP-002 and RFC-CDP-024:

1. **Procedural bypass** — required sufficiency checks were skipped, rushed, or bypassed.
2. **Certainty performance** — sufficiency fields exist but perform inquiry without representing genuine inquiry.

The payload can record field presence and evaluator findings.

It cannot by itself prove that inquiry was genuine.

That requires adversarial review, formation challenge, ordinary Challenge, Learn-stage review, or other CDP governance mechanisms.

#### 5.1.2 Canonical Draft Schema

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

#### 5.1.3 Required Fields

The following fields are required in Draft v0.6:

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

`record_hash` is nullable in Draft v0.6 because record-hash propagation to governed record RFCs remains a separate open work item.

#### 5.1.4 Criterion Status Values

Allowed criterion status values:

```text
pass | fail | waived | not_applicable | unknown
```

A criterion marked `waived` MUST have a corresponding waiver entry.

A criterion marked `unknown` MUST NOT be treated as passed.

#### 5.1.5 Pass Rule

`passed` MUST be `false` if `unwaived_failures` is non-empty.

`passed` MUST be `false` if any required criterion has status `fail` or `unknown` and no valid waiver exists.

A payload with `passed: true` means the APC gate passed for the stated `gate_context` and risk tier.

It does not mean the decision is legitimate.

Legitimacy is governed by applicable lifecycle protocols, especially Legitimize, Standing, Decision Lifecycle Envelope, and Repair/Appeal mechanisms.

#### 5.1.6 Waiver and Exception Constraints

Waivers MUST identify the criterion waived, authority, reason, expiration when applicable, and whether the proposer was recused.

The proposer MUST NOT authorize their own APC waiver or exception.

Every APC exception MUST set:

```text
learn_review_required: true
```

This preserves the RFC-CDP-002 requirement that exceptions are reviewed at Learn stage.

#### 5.1.7 Persistence Requirements

When persisted, this payload SHOULD be stored as a governed record in `cdp_governed_record` under RFC-CDP-025 with:

```text
record_type: anti_premature_certainty_gate_result
```

The payload SHOULD be referenced by the Decision Lifecycle Envelope when used for proposal admission, challenge closure, legitimization, execution, record, or learning.

#### 5.1.8 Downstream Use

Downstream RFCs MAY reference this Draft-compatible payload before it is Accepted.

However, any downstream RFC requiring this payload as a blocking precondition MUST state:

- which `gate_context` is required;
- which risk tiers require it;
- whether exceptions are allowed;
- which standing checks apply to the evaluator and waiver authority;
- how failures block lifecycle advancement.

---

### 5.2 Proposal Sufficiency Record

Payload name:

```text
proposal_sufficiency_record
```

Status:

```text
Defined — Draft v0.6
```

Defined by:

```text
RFC-CDP-024-Proposal-Sufficiency-Gate.md
```

Persisted by:

```text
RFC-CDP-025-CDP-Persistence-Model.md
```

Indexed by:

```text
RFC-CDP-023-Decision-Lifecycle-Envelope.md
```

Consumed by:

```text
RFC-CDP-041-Propose-Protocol.md
RFC-CDP-042-Challenge-Protocol.md
RFC-CDP-045-Legitimize-Protocol.md
```

Purpose:

Records whether a proposed decision has met the minimum formation requirements necessary to enter the governed proposal and challenge lifecycle.

The normative gate semantics and minimum viable schema are owned by RFC-CDP-024.

#### 5.2.1 Registration Rule

A `proposal_sufficiency_record` MAY be carried as a Wire Message Envelope payload when submitting, amending, attesting, or transmitting the governed sufficiency record.

When persisted, it SHOULD be stored as a governed record under RFC-CDP-025 with:

```text
record_type: proposal_sufficiency_record
```

When a proposal is admitted, the Decision Lifecycle Envelope MUST reference the governed record through:

```text
stage_record_refs.proposal_sufficiency_ref
```

#### 5.2.2 Minimum Required Fields

The registered payload MUST preserve at least the required fields defined by RFC-CDP-024, including:

- `record_id`
- `decision_id`
- `proposer_id`
- `proposer_standing_record_ref`
- `submitted_at`
- `risk_tier`
- `sufficiency_status`
- `claim`
- `evidence_refs` or `evidence_waiver_ref`
- `uncertainty_summary`
- `reversibility_path`
- `exception_invoked`
- `governed_record_ref`
- `lineage_refs`

A `proposal_sufficiency_record` with `sufficiency_status: sufficient` or `sufficiency_status: excepted` is evidence of admission sufficiency.

It is not evidence of legitimacy by itself.

#### 5.2.3 Non-Substitution Rule

A proposal summary, rationale, or ordinary Propose payload MUST NOT substitute for a governed `proposal_sufficiency_record` when RFC-CDP-023, RFC-CDP-041, RFC-CDP-042, or RFC-CDP-045 requires sufficiency evidence.

---

### 5.3 Formation Challenge Record

Payload name:

```text
formation_challenge_record
```

Status:

```text
Defined — Draft v0.6
```

Defined by:

```text
RFC-CDP-024-Proposal-Sufficiency-Gate.md
```

Persisted by:

```text
RFC-CDP-025-CDP-Persistence-Model.md
```

Indexed by:

```text
RFC-CDP-023-Decision-Lifecycle-Envelope.md
```

Related to:

```text
RFC-CDP-042-Challenge-Protocol.md
```

Purpose:

Records an upstream challenge to whether a proposed decision has earned admission as a proposal.

A Formation Challenge contests proposal formation, sufficiency, proposer standing, missing evidence, uncertainty, stakeholder impact, reversibility, APC requirements, or exception authority before ordinary Challenge begins.

The normative semantics and minimum viable schema are owned by RFC-CDP-024.

#### 5.3.1 Registration Rule

A `formation_challenge_record` MAY be carried as a Wire Message Envelope payload when raising, amending, attesting, resolving, or transmitting a governed formation challenge.

When persisted, it SHOULD be stored as a governed record under RFC-CDP-025 with:

```text
record_type: formation_challenge_record
```

The Decision Lifecycle Envelope MUST preserve formation challenge history through:

```text
stage_record_refs.formation_challenge_refs
```

The list MAY be empty. An absent list is ambiguous and non-compliant with RFC-CDP-023.

#### 5.3.2 Minimum Required Fields

The registered payload MUST preserve at least the required fields defined by RFC-CDP-024, including:

- `record_id`
- `decision_id`
- `challenger_id`
- `target_sufficiency_record_ref`
- `challenged_criteria`
- `challenge_summary`
- `requested_outcome`
- `submitted_at`
- `status`
- `governed_record_ref`
- `lineage_refs`

#### 5.3.3 Boundary Rule

A `formation_challenge_record` MUST NOT be treated as an ordinary Challenge record.

Formation Challenge is upstream of proposal admission and is governed by RFC-CDP-024.

Ordinary Challenge is downstream of proposal admission and is governed by RFC-CDP-042.

---

## 6. Content Types

Default encodings SHOULD use structured syntax suffixes:

- `application/cdp.propose+json`
- `application/cdp.challenge+json`
- `application/cdp.test+json`
- `application/cdp.apc-gate-result+json`
- `application/cdp.proposal-sufficiency-record+json`
- `application/cdp.formation-challenge-record+json`

Alternate encodings MAY be supported if schema semantics are preserved.

---

## 7. Open Questions

1. Should `record_hash` be made mandatory after record-hash propagation is complete?
2. Should APC criteria be represented as a list rather than a fixed object to allow domain-specific extensions?
3. Should `gate_context` values be moved into `cdp_controlled_vocabulary` under RFC-CDP-025?
4. Should registered payload entries be promoted into standalone machine-readable JSON Schema artifacts?
5. Should `SUBMIT_SUFFICIENCY_RECORD` and `RAISE_FORMATION_CHALLENGE` be added to the Wire Message Envelope act enum in RFC-CDP-021?

---

## 8. Status of This Draft

Promoted into Draft v0.4:

- canonical heading updated to match the filename and Series Index entry.

Promoted into Draft v0.5:

- `anti_premature_certainty_gate_result` promoted from Reserved to Defined Draft payload.

Promoted into Draft v0.6:

- `proposal_sufficiency_record` registered as a Defined Draft payload and governed record type;
- `formation_challenge_record` registered as a Defined Draft payload and governed record type;
- registry boundary clarified against Wire Message Envelope, Decision Lifecycle Envelope, and Persistence Model;
- stale open questions about whether proposal sufficiency and formation challenge should be registered were resolved by registration;
- content types added for proposal sufficiency and formation challenge records.

Deferred:

- record-hash propagation;
- controlled vocabulary ownership for `gate_context`;
- machine-readable schema artifact generation;
- Wire Message Envelope act enum updates.

---

## 9. Principle

Envelope fields are universal.

Lifecycle envelopes are indexes.

Persistence records are storage artifacts.

Payload fields are act-specific, gate-specific, or record-specific.

A registered payload is not legitimacy.

Payload schemas MUST NOT silently redefine universal envelope semantics.