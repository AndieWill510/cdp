# RFC-CDP-024 — Proposal Sufficiency Gate

Author: Kevin “Andie” Williams  
Status: Draft v0.2  
Series: Constitutional Decision Plane (CDP)  
Date: June 25, 2026  
Updates: RFC-CDP-024 v0.1  
Depends On: RFC-CDP-002, RFC-CDP-022, RFC-CDP-023, RFC-CDP-025, RFC-CDP-033  
Related: RFC-CDP-041, RFC-CDP-042, RFC-CDP-045, RFC-CDP-047, RFC-CDP-048, RFC-CDP-090

## Abstract

This RFC defines the Proposal Sufficiency Gate for CDP.

The Proposal Sufficiency Gate determines whether a proposed decision has met the minimum formation requirements necessary to enter the CDP challenge lifecycle.

It does not decide whether the proposal is correct, legitimate, accepted, or executable.

It answers a narrower upstream question:

> Has this proposal earned the right to be heard?

A sufficient proposal may still be challenged, tested, adjudicated against, rejected, appealed, or repaired.

An insufficient proposal has not yet met the minimum bar to enter the governed challenge lifecycle.

Draft v0.2 aligns this gate with downstream integration now present in RFC-CDP-022, RFC-CDP-023, RFC-CDP-041, RFC-CDP-042, and RFC-CDP-045.

---

## 1. Purpose

CDP separates proposal formation from proposal challenge.

A governance system that allows under-formed proposals to enter the challenge lifecycle forces challengers, adjudicators, and affected parties to repair formation defects downstream.

This produces unnecessary burden, schema drift, premature certainty, and illegitimate framing power.

The Proposal Sufficiency Gate defines the minimum requirements for proposal admission.

It exists before ordinary Challenge.

It protects the Challenge lifecycle from becoming a cleanup layer for malformed proposals.

---

## 2. Failure Mode: Proposal Admission Without Sufficiency

The failure mode this RFC addresses is **proposal admission without sufficiency**.

Proposal admission without sufficiency occurs when a proposal enters the governed challenge lifecycle before it has established the minimum evidence, uncertainty, standing, stakeholder impact, reversibility, and threshold conditions required to be heard.

This failure has two mechanisms.

### 2.1 Premature Admission

Premature admission occurs when a proposal enters the challenge lifecycle before meeting minimum formation requirements.

The system accepts it because no gate exists, the gate is advisory, or the gate has no blocking enforcement.

Premature admission is prevented by a blocking Proposal Sufficiency Gate.

### 2.2 Sufficiency Performance

Sufficiency performance occurs when a proposal satisfies the gate schema on paper, but the content performs sufficiency without achieving it.

Examples include:

- evidence fields containing assertions rather than references;
- uncertainty fields containing boilerplate rather than actual uncertainty;
- alternatives listed only to dismiss them without analysis;
- stakeholder impact fields that name affected parties without assessing harm;
- reversibility paths that exist nominally but cannot be executed;
- APC self-checks completed cosmetically.

Sufficiency performance is only partially addressed by this RFC.

The Proposal Sufficiency Gate can block missing structure.

Formation Challenge contests whether the structure represents genuine inquiry.

---

## 3. Architectural Role

The Proposal Sufficiency Gate is:

1. a cross-cutting primitive;
2. a record-producing gate;
3. an upstream adversarial surface;
4. a state transition guard.

It is not a lifecycle stage.

It is not a replacement for Propose.

It is not a replacement for Challenge.

It is a precondition for proposal admission.

### 3.1 Core Distinction

Ordinary Challenge asks:

> Is this proposal acceptable, valid, safe, legitimate, or correct?

Proposal Sufficiency asks:

> Is this ready to be treated as a proposal?

### 3.2 Admission Flow

Recommended conceptual flow:

```text
formation
  -> submit_sufficiency_record
  -> admission_pending
  -> sufficient | insufficient | excepted
  -> admitted | returned_to_formation | blocked
  -> Propose / Challenge lifecycle
```

---

## 4. Normative Acts

This RFC defines two named upstream acts.

### 4.1 SUBMIT_SUFFICIENCY_RECORD

`SUBMIT_SUFFICIENCY_RECORD` is the act of submitting a proposal sufficiency record for gate evaluation.

It may be performed by a proposer, delegated proposal author, or authorized formation actor with valid standing.

### 4.2 RAISE_FORMATION_CHALLENGE

`RAISE_FORMATION_CHALLENGE` is the act of challenging whether a proposal has met the minimum formation requirements required for admission.

Formation Challenge is distinct from ordinary Challenge under RFC-CDP-042.

It occurs before the proposal enters the challenge lifecycle.

It contests formation sufficiency, not the ultimate merits of the proposal.

### 4.3 Formation Challenge Outcomes

A Formation Challenge MAY result in:

```text
return_to_formation
request_missing_evidence
require_uncertainty_disclosure
require_stakeholder_impact
require_APC_gate
block_admission
allow_exception_with_controls
```

---

## 5. Proposal Sufficiency States

```text
forming
admission_pending
sufficient
insufficient
excepted
admitted
returned_to_formation
blocked
```

| State | Meaning |
|---|---|
| `forming` | Proposal is under formation and has not submitted sufficiency record. |
| `admission_pending` | Sufficiency record submitted and awaiting gate evaluation. |
| `sufficient` | Gate criteria met for applicable risk tier. |
| `insufficient` | Gate criteria not met and no valid exception exists. |
| `excepted` | Insufficient proposal admitted under explicit, auditable exception. |
| `admitted` | Proposal may enter Propose / Challenge lifecycle. |
| `returned_to_formation` | Proposal must be revised before resubmission. |
| `blocked` | Proposal cannot proceed under current conditions. |

---

## 6. Minimum Sufficiency Criteria

A proposal SHOULD NOT enter the challenge lifecycle unless it contains or references:

1. proposal identity and proposer standing;
2. claim or requested decision;
3. evidence references or evidence-waiver rationale;
4. uncertainty summary;
5. alternatives considered or alternatives-waiver rationale;
6. affected-party / stakeholder impact statement;
7. reversibility, appeal, repair, or compensation path;
8. decision threshold or acceptance criteria;
9. APC self-check or APC gate result;
10. record references sufficient to preserve lineage.

Risk-tiering remains an open dependency.

Until a canonical risk classification mechanism exists, implementations MUST document their local risk classification rule.

---

## 7. Minimum Viable proposal_sufficiency_record Schema

```yaml
proposal_sufficiency_record:
  record_id: <uuid>
  decision_id: <uuid>
  proposer_id: <actor_id>
  proposer_standing_record_ref: <ref>
  submitted_at: <timestamp>
  risk_tier: <low|medium|high|critical|unknown>
  sufficiency_status: <pending|sufficient|insufficient|excepted>

  # Required for all risk tiers
  claim: <string>
  evidence_refs: [<ref>]
  evidence_waiver_ref: <ref|null>
  uncertainty_summary: <string>
  reversibility_path: <string>

  # Required for medium, high, critical unless waived
  alternatives_refs: [<ref>]
  alternatives_waiver_ref: <ref|null>
  stakeholder_impact_ref: <ref|null>

  # Required for high and critical unless exceptioned
  decision_threshold: <string|null>
  apc_gate_result_ref: <ref|null>

  # Exception path
  exception_invoked: <boolean>
  exception_authority_ref: <ref|null>
  exception_reason: <string|null>
  exception_proposer_recused: <boolean>

  # Integrity
  governed_record_ref: <ref>
  record_hash: <hash|null>
  lineage_refs: [<ref>]
```

`record_hash` is nullable in Draft v0.2 because record-hash propagation to governed record RFCs remains a separate open work item.

A null `record_hash` means the record may be referenceable, but it must not be represented as fully integrity-verified.

### 7.1 Non-Negotiable Admission Fields

Every proposal, regardless of risk tier, MUST include:

- `claim`;
- `proposer_id`;
- `proposer_standing_record_ref`;
- evidence references or evidence waiver;
- `uncertainty_summary`;
- `reversibility_path`.

These fields are minimum admission requirements.

They are not optional for low-risk proposals.

### 7.2 Registry and Envelope Binding

`proposal_sufficiency_record` is registered by RFC-CDP-022.

When persisted, it SHOULD be stored under RFC-CDP-025 with:

```text
record_type: proposal_sufficiency_record
```

When a proposal is admitted, it MUST be indexed by RFC-CDP-023 through:

```text
stage_record_refs.proposal_sufficiency_ref
```

A Propose payload, summary, rationale, or narrative statement MUST NOT substitute for the governed `proposal_sufficiency_record`.

---

## 8. APC Gate Relationship

The Proposal Sufficiency Gate is related to, but distinct from, the Anti-Premature-Certainty Gate.

The Proposal Sufficiency Gate asks whether a proposal is sufficiently formed to enter the challenge lifecycle.

The Anti-Premature-Certainty Gate asks whether a decision has collapsed uncertainty too early before finalization or execution eligibility.

### 8.1 Risk-Tiered APC Requirement

Draft v0.2 recommends:

| Risk tier | APC requirement at admission |
|---|---|
| `low` | APC self-check required; full gate result required before Legitimize. |
| `medium` | APC self-check required; full gate result required before Challenge closes. |
| `high` | Full APC gate result required at admission. |
| `critical` | Full APC gate result required at admission. |
| `unknown` | Treat as high until classified. |

This table is provisional until a canonical risk classification mechanism exists.

### 8.2 Non-Tiered APC Minimum

Every proposal MUST declare evidence, uncertainty, and reversibility at admission.

This minimum is not risk-tiered.

### 8.3 APC Payload Binding

`anti_premature_certainty_gate_result` is registered by RFC-CDP-022.

When used for proposal admission, the APC gate result SHOULD use:

```yaml
gate_context: proposal_admission
```

and SHOULD be indexed by RFC-CDP-023 through:

```text
stage_record_refs.apc_gate_result_refs
```

---

## 9. Standing Checks

Before accepting a proposal sufficiency record, the system MUST verify proposer standing.

### 9.1 Proposer Standing Check

The system MUST query `cdp_standing_record` or implementation-profile equivalent to determine whether the proposer has valid standing at the Propose stage.

If no valid standing record exists, admission MUST block unless an explicit emergency exception path is invoked and recorded.

If recusal is required, admission MUST block unless the recusal scope explicitly permits participation at Propose.

### 9.2 Constitutional Standing Protection

If the proposer claims affected-party standing as their basis, the system MUST NOT require proof of impact before admission.

The claim of potential impact is sufficient for preliminary standing under RFC-CDP-033.

Requiring proof of impact before admission is a violation of constitutional standing and MUST be treated as a governance breach.

---

## 10. Formation Challenge

Formation Challenge is a distinct upstream act owned by this RFC.

It is not a subtype of ordinary Challenge.

### 10.1 Distinction from Challenge

Ordinary Challenge contests the proposal after admission.

Formation Challenge contests admission itself.

Formation Challenge may be raised when:

- required sufficiency fields are missing;
- sufficiency fields are cosmetic or non-substantive;
- proposer standing is invalid or stale;
- affected-party standing is improperly denied;
- APC self-check or gate result is missing when required;
- evidence, alternatives, uncertainty, impact, reversibility, or threshold content is inadequate;
- exception authority is invalid or conflicted.

### 10.2 Formation Challenge Record

A Formation Challenge SHOULD produce a governed record.

Minimum seed schema:

```yaml
formation_challenge_record:
  record_id: <uuid>
  decision_id: <uuid>
  challenger_id: <actor_id>
  target_sufficiency_record_ref: <ref>
  challenged_criteria:
    - <evidence|uncertainty|alternatives|stakeholder_impact|reversibility|threshold|standing|apc|exception_authority>
  challenge_summary: <string>
  requested_outcome: <return_to_formation|request_missing_evidence|require_uncertainty_disclosure|require_stakeholder_impact|require_APC_gate|block_admission|allow_exception_with_controls>
  submitted_at: <timestamp>
  status: <pending|sustained|rejected|resolved|deferred>
  governed_record_ref: <ref>
  record_hash: <hash|null>
  lineage_refs: [<ref>]
```

`record_hash` is nullable in Draft v0.2 because record-hash propagation to governed record RFCs remains a separate open work item.

### 10.3 Registry and Envelope Binding

`formation_challenge_record` is registered by RFC-CDP-022.

When persisted, it SHOULD be stored under RFC-CDP-025 with:

```text
record_type: formation_challenge_record
```

Formation Challenge records MUST be indexed by RFC-CDP-023 through:

```text
stage_record_refs.formation_challenge_refs
```

The list may be empty.

An absent list is ambiguous.

### 10.4 Standing for Formation Challenge

Standing requirements for Formation Challenge are not identical to ordinary Challenge.

Formation Challenge standing SHOULD be broad enough to allow affected parties, evidence custodians, record keepers, and authorized governance reviewers to contest proposal formation before admission.

Detailed standing rules remain open and SHOULD be aligned with RFC-CDP-033 and future lifecycle protocol updates.

---

## 11. Exception Path

A proposal with incomplete sufficiency criteria MAY enter the challenge lifecycle only under explicit, auditable exception.

An exception MUST include missing criteria, reason, exception authority, compensating controls, expiration or review condition, and Learn-stage review requirement.

The proposer MUST NOT authorize their own exception.

Proposer recusal on exception authority is absolute.

Emergency exceptions MAY use compressed authority only under explicit emergency conditions and MUST include post-hoc justification and review.

---

## 12. Persistence Requirements

Proposal Sufficiency Gate artifacts MUST be persisted according to RFC-CDP-025.

Every Proposal Sufficiency Gate evaluation MUST persist:

1. `proposal_sufficiency_record` in `cdp_governed_record` as the canonical artifact;
2. `anti_premature_certainty_gate_result` in `cdp_governed_record`, when required by risk tier or downstream state;
3. `formation_challenge_record` in `cdp_governed_record`, when Formation Challenge is raised.

If a previously computed APC gate result is reused, the sufficiency record MUST reference it and preserve the reuse rationale.

### 12.1 Envelope References

Proposal sufficiency records, Formation Challenge records, and APC gate result records are indexed by the Decision Lifecycle Envelope through explicit RFC-CDP-023 fields:

```yaml
stage_record_refs:
  proposal_sufficiency_ref: <ref|null>
  formation_challenge_refs: [<ref>]
  apc_gate_result_refs: [<ref>]
```

A proposal MUST NOT be represented as admitted unless `proposal_sufficiency_ref` points to a governed `proposal_sufficiency_record` with `sufficiency_status: sufficient` or `sufficiency_status: excepted`.

Formation Challenge references MUST remain visible even if the challenge was resolved, rejected, sustained, remediated, or deferred with controls.

### 12.2 Standing Check Record

The result of the proposer standing check MUST be recorded.

The record SHOULD include timestamp, standing record reference, standing status, recusal flag and scope, projection status, and admission decision based on the check.

---

## 13. Downstream Integration Status

Draft v0.1 identified downstream RFC obligations.

As of Draft v0.2, the following have landed:

| RFC | Integration status |
|---|---|
| RFC-CDP-022 | Registers `anti_premature_certainty_gate_result`, `proposal_sufficiency_record`, and `formation_challenge_record`. |
| RFC-CDP-023 | Indexes `proposal_sufficiency_ref`, `formation_challenge_refs`, and `apc_gate_result_refs`. |
| RFC-CDP-041 | Requires valid proposal sufficiency before Propose advances into ordinary Challenge. |
| RFC-CDP-042 | Distinguishes Formation Challenge from ordinary Challenge. |
| RFC-CDP-045 | Requires proposal sufficiency and APC evidence before Legitimize proceeds. |

Still pending or partially open:

| Area | Remaining work |
|---|---|
| RFC-CDP-021 | Decide whether to add `SUBMIT_SUFFICIENCY_RECORD` and `RAISE_FORMATION_CHALLENGE` to the act enum. |
| RFC-CDP-047 | Define how Record preserves proposal admission artifacts and record hashes. |
| RFC-CDP-048 | Define Learn-stage review of sufficiency failures, APC exceptions, and repeated admission defects. |
| Risk classification | Define canonical risk-tier ownership and vocabulary. |
| Formation Challenge standing | Define detailed standing rules for formation challengers. |

---

## 14. Security and Governance Considerations

Proposal sufficiency records may contain sensitive evidence, affected-party information, uncertainty assessments, standing records, exception rationale, and challenge history.

Implementations SHOULD address access control, redaction, affected-party review, evidence handling, standing enforcement, exception abuse, emergency exception normalization, sufficiency performance, Formation Challenge suppression, repair, and appeal paths.

Repeated sufficiency failures SHOULD be treated as governance learning signals.

Repeated exceptions SHOULD trigger Learn-stage review and possible governance escalation.

---

## 15. Open Questions

1. What canonical mechanism classifies decision risk tier?
2. What is the required emergency exception review window?
3. What standing rules apply to Formation Challenge challengers?
4. Should `SUBMIT_SUFFICIENCY_RECORD` and `RAISE_FORMATION_CHALLENGE` be added to the Wire Message Envelope act enum in RFC-CDP-021?
5. Should Formation Challenge have a dedicated persistence table if query pressure grows?
6. How should Record and Learn consume admission artifacts after record-hash propagation lands?

---

## 16. Status of This Draft

Promoted into Draft v0.1:

- proposal admission without sufficiency as the failure mode;
- premature admission and sufficiency performance as distinct mechanisms;
- Proposal Sufficiency Gate as primitive, act, record, and state transition guard;
- `SUBMIT_SUFFICIENCY_RECORD` and `RAISE_FORMATION_CHALLENGE` as upstream acts;
- minimum viable `proposal_sufficiency_record` schema;
- risk-tiered APC relationship;
- proposer standing check through `cdp_standing_record`;
- affected-party constitutional standing protection;
- Formation Challenge as distinct from ordinary Challenge;
- exception path with absolute proposer recusal;
- persistence requirements from RFC-CDP-025;
- downstream RFC obligations.

Promoted into Draft v0.2:

- stale future-patch language removed after RFC-CDP-022, RFC-CDP-023, RFC-CDP-041, RFC-CDP-042, and RFC-CDP-045 integration landed;
- `proposal_sufficiency_record` binding to RFC-CDP-022 and RFC-CDP-023 clarified;
- `formation_challenge_record` binding to RFC-CDP-022 and RFC-CDP-023 clarified;
- APC gate result binding to RFC-CDP-022 and RFC-CDP-023 clarified;
- nullable `record_hash` aligned with deferred record-hash propagation;
- downstream integration status table added;
- open questions narrowed to remaining unresolved work.

Deferred:

- canonical risk classification mechanism;
- emergency exception review window;
- Formation Challenge standing rules;
- Wire Message Envelope act enum updates;
- Record and Learn integration;
- record-hash propagation;
- possible dedicated persistence table for Formation Challenge.

---

## 17. Summary

The Proposal Sufficiency Gate protects the CDP lifecycle from malformed proposal admission.

It does not decide whether a proposal is correct.

It decides whether a proposal is ready to be heard.

Challenge asks whether the proposal should survive.

Proposal Sufficiency asks whether the proposal may enter.

A constitutional decision system must not force affected parties, challengers, adjudicators, or repair processes to compensate for formation failures that should have been caught at the gate.