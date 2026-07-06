# RFC-CDP-023 — Decision Lifecycle Envelope

Author: Kevin “Andie” Williams  
Status: Draft v0.7  
Series: Constitutional Decision Plane (CDP)  
Date: July 6, 2026  
Updates: RFC-CDP-023 v0.6  
Depends On: RFC-CDP-001, RFC-CDP-021, RFC-CDP-022, RFC-CDP-024, RFC-CDP-025, RFC-CDP-030, RFC-CDP-031, RFC-CDP-032, RFC-CDP-033, RFC-CDP-070  
Related: RFC-CDP-040, RFC-CDP-041, RFC-CDP-042, RFC-CDP-043, RFC-CDP-044, RFC-CDP-045, RFC-CDP-046, RFC-CDP-047, RFC-CDP-048, RFC-CDP-050, RFC-CDP-052, RFC-CDP-071, RFC-CDP-072, RFC-CDP-073, RFC-CDP-074, RFC-CDP-075, RFC-CDP-090, RFC-CDP-092

## Abstract

This RFC defines the **Decision Lifecycle Envelope**: the governed path index for a complete CDP decision across lifecycle stages.

The Decision Lifecycle Envelope is not a wire message and is not a warehouse for every artifact produced by a decision.

It is a persistent, updatable, human-readable and machine-readable index that identifies the decision, exposes lifecycle state, references governed artifacts, preserves standing and recusal control surfaces, preserves Nemawashi and proposal admission artifacts, preserves appeal and repair control surfaces, exposes execution-control hooks, exposes covenant/boundary hooks, and supports audit, appeal, repair, execution control, and learning.

Draft v0.7 adds first-class Nemawashi reference families and lightweight cross-plane hooks for Execution and Covenant surfaces. This aligns the envelope more tightly with the README lifecycle and four-plane model without turning the envelope into a warehouse.

Draft v0.6 aligned proposal admission references with the registered payload and governed record types in RFC-CDP-022:

```text
proposal_sufficiency_record
formation_challenge_record
anti_premature_certainty_gate_result
```

The envelope indexes these records. It does not embed, redefine, or legitimize them.

---

## 1. Purpose and Failure Modes

The Decision Lifecycle Envelope answers:

- what decision is being governed;
- what lifecycle stage it is in;
- what its current status is;
- what human-readable summary represents the governed record;
- what standing and recusal status applies;
- what Nemawashi, stakeholder, early dissent, boundary, and unresolved-question artifacts exist before proposal admission;
- whether a proposal earned admission before entering the challenge lifecycle;
- what proposal sufficiency, formation challenge, and APC gate result artifacts exist;
- what challenge, evidence, test, adjudication, legitimacy, execution, appeal, repair, and learning artifacts exist;
- what execution-control hooks apply before legitimacy becomes action;
- what covenant/boundary hooks apply where relationship, witness, clarification, or boundary-holding records are required;
- what appeal and repair status applies;
- what governed records exist across lifecycle stages;
- what lineage and integrity markers allow reconstruction of the governed path.

This RFC addresses seven failure modes:

1. **Governed path severance** — the decision record exists, but the governed path is scattered, loosely linked, or replaced by summary.
2. **Summary substitution** — a human-readable summary is treated as equivalent to the governed record it summarizes.
3. **Silent reference mutation** — a referenced governed record changes after registration while the envelope still points to the same reference identifier.
4. **Closure without repair resolution** — a decision is marked closed while appeal, repair, breach, or affected-party claim conditions remain unresolved.
5. **Admission artifact invisibility** — Proposal Sufficiency, Formation Challenge, or APC gate result artifacts exist as governed records but are not explicitly indexed by the envelope.
6. **Nemawashi invisibility** — stakeholder mapping, pre-proposal consultation, early dissent, boundary conditions, or unresolved questions exist before proposal admission but are not indexed as part of the governed path.
7. **Cross-plane hook ambiguity** — Execution Plane and Covenant Plane records exist, but the Decision Lifecycle Envelope lacks explicit hooks to show whether execution, witness, clarification, boundary-holding, appeal, or repair surfaces constrain the decision.

Admission artifact invisibility creates a governed path gap between formation and proposal/challenge.

Nemawashi invisibility creates a governed path gap before formation and proposal admission. It can make a proposal appear procedurally mature even when affected parties, dissent, boundary conditions, or unresolved questions were never surfaced.

Cross-plane hook ambiguity allows a decision to appear complete in the Decision Plane while execution, covenant, appeal, or repair conditions remain unresolved elsewhere.

The envelope therefore carries explicit references for Nemawashi artifacts, proposal sufficiency, formation challenge, APC gate result artifacts, execution-control hooks, and covenant/boundary hooks.

---

## 2. Design Rule: Governed Path Index, Not Warehouse

The Decision Lifecycle Envelope is a **governed path index**, not a warehouse.

It carries references to governed artifacts, not the artifacts themselves.

The envelope includes identity, lifecycle state, human-readable summary with record pointer, standing and recusal control surface, Nemawashi references, proposal admission references, repair control surface, governed stage references, execution-control hooks, covenant/boundary hooks, lineage, and integrity markers.

Full artifacts should be stored as governed records and referenced by ID or URI.

Embedded payloads are not part of the base Decision Lifecycle Envelope schema.

Implementation profiles may define sealed, portable, or air-gapped variants without changing base semantics.

---

## 3. Relationship to Wire Message Envelope and Payload Registry

The Wire Message Envelope is per-message and is defined by RFC-CDP-021.

The Protocol Payload Schema Registry is defined by RFC-CDP-022.

The Decision Lifecycle Envelope is per-decision.

Wire messages may carry payloads such as `proposal_sufficiency_record`, `formation_challenge_record`, or `anti_premature_certainty_gate_result`.

The Decision Lifecycle Envelope indexes the governed records produced or referenced by those messages.

A wire payload is not automatically a governed lifecycle reference.

A governed lifecycle reference is not automatically a valid payload.

Implementations SHOULD connect these surfaces through `decision_id`, `correlation_id`, governed record identifiers, payload type, record type, registration-time content hash, and lineage fields.

---

## 4. Minimum Viable Schema

```yaml
decision_envelope:
  # Identity
  envelope_id: <uuid>
  envelope_schema_version: <semver>
  decision_id: <uuid>
  decision_type: <string>
  created_at: <timestamp>
  updated_at: <timestamp>
  created_by: <actor_id>

  # Lifecycle state
  lifecycle_stage: <enum>
  # Allowed: nemawashi|propose|challenge|test|adjudicate|legitimize|execute|record|learn|repair|appeal
  status: <enum>
  # Allowed: draft|formation|admission_pending|admitted|under_challenge|under_test|adjudicated|legitimized|execution_queued|executed|recorded|appealed|repair_required|closed

  # Human-readable surface
  human_summary:
    summary_text: <string>
    plain_language_status: <string>
    known_uncertainties: [<string>]
    material_dissent_refs: [<ref>]
    summary_governed_by_ref: <ref>

  # Standing control surface
  standing_status: <unreviewed|valid|contested|recusal_active|blocked|emergency>
  standing_record_refs: [<ref>]
  recusal_record_refs: [<ref>]
  affected_party_claim_refs: [<ref>]

  # Repair control surface
  repair_control:
    repair_status: <none|available|triggered|active|blocked|resolved>
    closure_blocked: <boolean>
    closure_blocking_reason: <string|null>
    closure_blocking_refs: [<ref>]

  # Governed stage references
  stage_record_refs:
    # Nemawashi / pre-proposal alignment and dissent discovery.
    nemawashi_refs: [<ref>]
    # Required field. Empty list is valid.
    stakeholder_map_ref: <ref|null>
    pre_proposal_consultation_refs: [<ref>]
    early_dissent_refs: [<ref>]
    boundary_condition_refs: [<ref>]
    unresolved_question_refs: [<ref>]

    framing_ref: <ref|null>
    proposal_sufficiency_ref: <ref|null>
    # REQUIRED after admission.
    # Must point to a governed record with:
    #   record_type: proposal_sufficiency_record
    #   sufficiency_status: sufficient|excepted
    # Null only before admission gate is evaluated.
    formation_challenge_refs: [<ref>]
    # Required field. Empty list is valid.
    # Each non-empty reference points to record_type: formation_challenge_record.
    apc_gate_result_refs: [<ref>]
    # Required field. Empty list is valid.
    # Each non-empty reference points to record_type: anti_premature_certainty_gate_result.
    proposal_ref: <ref|null>
    challenge_refs: [<ref>]
    evidence_refs: [<ref>]
    test_refs: [<ref>]
    adjudication_ref: <ref|null>
    legitimacy_ref: <ref|null>

    # Execution Plane hooks.
    maturity_gate_ref: <ref|null>
    execution_queue_ref: <ref|null>
    review_queue_ref: <ref|null>
    presence_grant_ref: <ref|null>
    execution_constraint_ref: <ref|null>
    execution_record_ref: <ref|null>

    # Covenant Plane hooks.
    witness_record_refs: [<ref>]
    clarification_record_refs: [<ref>]
    boundary_hold_refs: [<ref>]

    appeal_refs: [<ref>]
    repair_refs: [<ref>]
    learning_refs: [<ref>]

  # Integrity and lineage
  integrity:
    lineage_refs: [<ref>]
    governed_path_manifest_ref: <ref|null>
    governed_path_hash: <hash>
    governed_path_hash_algorithm: <string>
    governed_path_hash_constructed_at: <timestamp>
    supersedes_envelope_id: <uuid|null>
    superseded_by_envelope_id: <uuid|null>
```

Reference list fields are required even when empty.

An empty list is informative.

An absent list is ambiguous.

Null singleton references are allowed where this RFC explicitly defines a nullable reference.

---

## 5. Human-Readable Surface Requirements

Every human-readable summary must point to the governed record it summarizes through `summary_governed_by_ref`.

The summary must not claim to be the governed record, suppress material dissent, or describe the decision as more resolved than the governed records show.

If `known_uncertainties` is empty, that is a positive claim that no material uncertainty is currently known.

A visualization, dashboard, or plain-language summary is not an adjudication, legitimacy basis, execution approval, or closure record.

Understanding is not legitimacy.

---

## 6. Nemawashi References

Nemawashi is the pre-proposal alignment, surfacing, consultation, and dissent-discovery stage.

It does not admit a proposal.

It does not legitimate a decision.

It prepares a proposal for admission by identifying affected parties, standing questions, known objections, early dissent, missing evidence, boundary conditions, and unresolved questions.

The envelope connects Nemawashi artifacts through these reference families:

```yaml
stage_record_refs:
  nemawashi_refs: [<ref>]
  stakeholder_map_ref: <ref|null>
  pre_proposal_consultation_refs: [<ref>]
  early_dissent_refs: [<ref>]
  boundary_condition_refs: [<ref>]
  unresolved_question_refs: [<ref>]
```

### 6.1 nemawashi_refs

`nemawashi_refs` points to governed records that document the pre-proposal formation work for the decision.

The list is required and may be empty.

An empty list means no Nemawashi records are currently indexed in the envelope.

An absent list is ambiguous and non-compliant with this RFC.

### 6.2 stakeholder_map_ref

`stakeholder_map_ref` points to a governed artifact identifying known affected parties, accountable owners, standing candidates, reviewers, and participation boundaries.

It may be null when stakeholder mapping has not yet been performed or is not applicable.

If a proposal relies on a claim that affected parties were identified, `stakeholder_map_ref` SHOULD be non-null.

### 6.3 pre_proposal_consultation_refs

`pre_proposal_consultation_refs` points to governed records of consultation, alignment, or pre-proposal review.

These records are evidence that participation was sought or attempted.

They are not proof that participation was sufficient.

### 6.4 early_dissent_refs

`early_dissent_refs` points to objections, warnings, counter-frames, or material disagreement raised before proposal admission.

Early dissent must not be hidden inside a plain-language summary.

It must be independently referenceable.

### 6.5 boundary_condition_refs

`boundary_condition_refs` points to governed records describing constraints, limits, cultural or institutional boundaries, explicit non-consent, jurisdictional boundaries, or review conditions discovered before proposal admission.

### 6.6 unresolved_question_refs

`unresolved_question_refs` points to open questions that remain material to proposal sufficiency, standing, challenge, adjudication, legitimacy, execution, appeal, or repair.

An unresolved question may be acceptable, blocking, or informational depending on downstream protocol rules.

The envelope indexes the question.

Lifecycle protocol RFCs decide the effect.

### 6.7 Nemawashi Rule

A Decision Lifecycle Envelope MAY advance beyond `lifecycle_stage: nemawashi` with empty Nemawashi references only when lifecycle protocol rules allow direct proposal formation, exception, emergency handling, or not-applicable classification.

Such advancement does not mean Nemawashi occurred.

It means the envelope records that no governed Nemawashi artifacts were indexed.

---

## 7. Proposal Admission References

The envelope connects to RFC-CDP-024 and RFC-CDP-022 through three explicit proposal-admission reference families:

```yaml
stage_record_refs:
  proposal_sufficiency_ref: <ref|null>
  formation_challenge_refs: [<ref>]
  apc_gate_result_refs: [<ref>]
```

### 7.1 proposal_sufficiency_ref

`proposal_sufficiency_ref` points to the governed `proposal_sufficiency_record` that establishes whether the proposal earned admission.

After a proposal is admitted, `proposal_sufficiency_ref` is required.

Before admission, it may be null only when the proposal is still in formation or no sufficiency record has been submitted.

### 7.2 formation_challenge_refs

`formation_challenge_refs` points to governed `formation_challenge_record` artifacts produced by `RAISE_FORMATION_CHALLENGE` under RFC-CDP-024.

The list is required and may be empty.

An empty list means no formation challenges are currently recorded in the envelope.

An absent list does not mean no formation challenges exist.

### 7.3 apc_gate_result_refs

`apc_gate_result_refs` points to governed `anti_premature_certainty_gate_result` records defined by RFC-CDP-022.

The list is required and may be empty.

### 7.4 Admission Rule

A Decision Lifecycle Envelope MUST NOT represent a proposal as admitted, with `lifecycle_stage: propose` or later, unless:

- `proposal_sufficiency_ref` is non-null; and
- the referenced `proposal_sufficiency_record` has `sufficiency_status: sufficient` or `sufficiency_status: excepted`.

An envelope with a null `proposal_sufficiency_ref` and `lifecycle_stage` at or past `propose` is non-compliant with this RFC.

Nemawashi references may support proposal sufficiency.

They do not themselves satisfy the admission rule unless a lifecycle protocol explicitly defines an exception or the sufficiency record incorporates them.

### 7.5 Record-Type Rule

When implementation profiles expose record typing, the referenced admission records SHOULD use the following `record_type` values:

| Envelope field | Required record type |
|---|---|
| `proposal_sufficiency_ref` | `proposal_sufficiency_record` |
| `formation_challenge_refs` | `formation_challenge_record` |
| `apc_gate_result_refs` | `anti_premature_certainty_gate_result` |

A reference with the right identifier shape but the wrong record type MUST NOT satisfy the admission rule.

---

## 8. Standing and Recusal Binding

The envelope connects to RFC-CDP-033 through top-level `standing_status`, `standing_record_refs`, `recusal_record_refs`, and `affected_party_claim_refs`.

These records are referenced, not embedded.

Each stage record reference must be interpretable against the standing and recusal records that governed that stage.

The envelope carries references.

Lifecycle protocol RFCs enforce rules.

---

## 9. Execution Plane Hooks

The README defines an Execution Plane distinct from the Decision Plane.

The Decision Lifecycle Envelope therefore exposes lightweight execution-control hooks without embedding the Execution Plane record schemas.

```yaml
stage_record_refs:
  maturity_gate_ref: <ref|null>
  execution_queue_ref: <ref|null>
  review_queue_ref: <ref|null>
  presence_grant_ref: <ref|null>
  execution_constraint_ref: <ref|null>
  execution_record_ref: <ref|null>
```

These references answer whether legitimacy has become action, whether execution is queued, whether review is required, whether a presence grant exists, and whether execution is constrained or complete.

A legitimized decision is not automatically executable.

Execution Plane protocols decide whether execution is queued, blocked, granted, constrained, or completed.

---

## 10. Covenant Plane Hooks

The README defines a Covenant Plane for witness, challenge, clarification, boundary holding, record, and repair.

The Decision Lifecycle Envelope exposes covenant/boundary hooks so that relationship and participation constraints are not lost when a decision is reviewed through the Decision Plane.

```yaml
stage_record_refs:
  witness_record_refs: [<ref>]
  clarification_record_refs: [<ref>]
  boundary_hold_refs: [<ref>]
```

These references are required lists and may be empty.

An empty list is informative.

An absent list is ambiguous.

Covenant hooks do not replace standing, recusal, affected-party claim, appeal, or repair records.

They index governed artifacts that show whether the decision was witnessed, clarified, bounded, or held under relationship constraints.

---

## 11. Repair Control Surface

The envelope connects to RFC-CDP-070 through `repair_control`.

When any RFC-CDP-070 trigger event is recorded against a decision, the envelope sets `repair_status: triggered` and `closure_blocked: true`, unless a later governed record shows that the trigger has been resolved, withdrawn, or superseded.

A Decision Lifecycle Envelope cannot advance to `status: closed` while unresolved appeal, repair, breach, or affected-party claim conditions remain.

An unresolved affected-party claim blocks closure regardless of whether a formal appeal record exists.

---

## 12. Governed Path Hash

The `governed_path_hash` is computed over a canonicalized Governed Path Manifest.

Hash integrity is evidence, not legitimacy.

A valid hash may preserve an illegitimate path with perfect fidelity.

That is useful evidence, not approval.

### 12.1 Governed Path Manifest Structure

```yaml
governed_path_manifest:
  manifest_schema_version: <semver>
  governed_path_hash_algorithm: <string>
  governed_path_hash_constructed_at: <timestamp>
  envelope_id: <uuid>
  envelope_schema_version: <semver>
  decision_id: <uuid>
  decision_type: <string>
  lifecycle_stage: <enum>
  status: <enum>
  standing_status: <enum>
  repair_status: <enum>
  closure_blocked: <boolean>

  human_summary_refs:
    summary_governed_by_ref: <ref>
    material_dissent_refs: [<ref_with_registration_hash>]

  standing_refs:
    standing_record_refs: [<ref_with_registration_hash>]
    recusal_record_refs: [<ref_with_registration_hash>]
    affected_party_claim_refs: [<ref_with_registration_hash>]

  nemawashi_refs:
    nemawashi_refs: [<ref_with_registration_hash>]
    stakeholder_map:
      ref_id: <ref|null>
      record_type: <stakeholder_map_record|null>
      content_hash_at_registration: <hash|null>
    pre_proposal_consultations: [<ref_with_registration_hash>]
    early_dissent_refs: [<ref_with_registration_hash>]
    boundary_condition_refs: [<ref_with_registration_hash>]
    unresolved_question_refs: [<ref_with_registration_hash>]

  proposal_admission_refs:
    proposal_sufficiency:
      ref_id: <ref|null>
      record_type: <proposal_sufficiency_record|null>
      content_hash_at_registration: <hash|null>
    formation_challenges:
      - ref_id: <ref>
        record_type: <formation_challenge_record>
        content_hash_at_registration: <hash>
        sequence_position: <integer>
    apc_gate_results:
      - ref_id: <ref>
        record_type: <anti_premature_certainty_gate_result>
        content_hash_at_registration: <hash>
        sequence_position: <integer>

  execution_control_refs:
    maturity_gate_ref: <ref_with_registration_hash|null>
    execution_queue_ref: <ref_with_registration_hash|null>
    review_queue_ref: <ref_with_registration_hash|null>
    presence_grant_ref: <ref_with_registration_hash|null>
    execution_constraint_ref: <ref_with_registration_hash|null>
    execution_record_ref: <ref_with_registration_hash|null>

  covenant_refs:
    witness_record_refs: [<ref_with_registration_hash>]
    clarification_record_refs: [<ref_with_registration_hash>]
    boundary_hold_refs: [<ref_with_registration_hash>]

  repair_control_refs:
    closure_blocking_refs: [<ref_with_registration_hash>]

  ordered_stage_refs:
    - stage: nemawashi
      refs: [<ref_with_registration_hash>]
    - stage: propose
      refs: [<ref_with_registration_hash>]
    - stage: challenge
      refs: [<ref_with_registration_hash>]
    - stage: test
      refs: [<ref_with_registration_hash>]
    - stage: adjudicate
      refs: [<ref_with_registration_hash>]
    - stage: legitimize
      refs: [<ref_with_registration_hash>]
    - stage: execute
      refs: [<ref_with_registration_hash>]
    - stage: record
      refs: [<ref_with_registration_hash>]
    - stage: learn
      refs: [<ref_with_registration_hash>]
    - stage: appeal
      refs: [<ref_with_registration_hash>]
    - stage: repair
      refs: [<ref_with_registration_hash>]

  lineage_refs: [<ref_with_registration_hash>]
  supersedes_envelope_id: <uuid|null>
  superseded_by_envelope_id: <uuid|null>
```

Each `ref_with_registration_hash` includes sequence position, reference ID, reference type, record type when available, registration-time content hash, hash algorithm, record schema version, and registration timestamp.

### 12.2 Hash Coverage

The manifest covers:

- envelope identity and schema version;
- `decision_id` and `decision_type`;
- `lifecycle_stage` and `status`;
- `standing_status`;
- `repair_control.repair_status` and `repair_control.closure_blocked`;
- summary governed-by and material dissent references;
- standing, recusal, and affected-party claim references;
- Nemawashi references, stakeholder map reference, pre-proposal consultation references, early dissent references, boundary-condition references, and unresolved-question references;
- `proposal_sufficiency_ref` and its record type when available;
- `formation_challenge_refs` and their record types when available;
- `apc_gate_result_refs` and their record types when available;
- execution-control references when available;
- covenant/boundary references when available;
- all other `stage_record_refs`;
- closure-blocking references;
- registration-time content hashes and algorithms when available;
- lineage and supersession links.

Adding Nemawashi, proposal sufficiency, formation challenge, APC gate result, execution-control, or covenant/boundary references to the envelope without adding them to manifest coverage would create an integrity gap.

Therefore the schema and manifest coverage for these reference families are inseparable.

### 12.3 Fields Excluded from the Manifest

Full governed artifacts, mutable display formatting, and access-control metadata are not hashed directly by the governed path manifest.

`nemawashi_refs`, `stakeholder_map_ref`, `pre_proposal_consultation_refs`, `early_dissent_refs`, `boundary_condition_refs`, `unresolved_question_refs`, `proposal_sufficiency_ref`, `formation_challenge_refs`, `apc_gate_result_refs`, execution-control refs, and covenant refs are included in the manifest.

They are not excluded.

### 12.4 Canonicalization

The manifest uses canonical JSON, UTF-8 encoding, lexicographically sorted object keys, explicit nulls, empty arrays rather than omitted lists, lowercase enum values, lowercase hash algorithm identifiers, and UTC ISO-8601 timestamps with `Z` suffix.

Ordered reference entries include `sequence_position`, assigned by ascending `registered_at`, then lexicographic `ref_id`.

The default algorithm for Draft v0.7 is `sha256`.

If a referenced record lacks a content hash, the manifest still includes the reference with null hash fields.

Such a manifest is valid but integrity-incomplete and must not be represented as fully integrity-verified.

---

## 13. Security and Governance Considerations

Decision Lifecycle Envelopes may expose affected-party claims, standing and recusal state, Nemawashi participation surfaces, stakeholder maps, early dissent, boundary conditions, unresolved questions, proposal sufficiency state, formation challenge existence, APC gate result existence, challenge existence, dissent references, evidence references, appeal or repair hooks, execution constraints, execution queue state, presence grants, witness records, clarification records, boundary-holding records, and learning artifacts.

Implementations should address access control, redaction, culturally appropriate handling, evidence custody, affected-party review, appeal rights, repair triggers, closure blocking, admission blocking, execution blocking, retention, audit logging, record-type validation, integrity verification, and the possibility that participation records themselves may be sensitive.

---

## 14. Status of This Draft

Promoted into Draft v0.7:

- first-class Nemawashi reference families;
- explicit `stakeholder_map_ref`;
- explicit `pre_proposal_consultation_refs`;
- explicit `early_dissent_refs`;
- explicit `boundary_condition_refs`;
- explicit `unresolved_question_refs`;
- explicit statement that Nemawashi does not admit or legitimate a proposal;
- explicit boundary that visualization and understanding are not adjudication or legitimacy;
- lightweight Execution Plane hooks for maturity gate, queues, review, presence grant, constraints, and execution record;
- lightweight Covenant Plane hooks for witness, clarification, and boundary holding;
- governed path manifest coverage for Nemawashi, execution-control, and covenant/boundary references.

Promoted into Draft v0.6:

- alignment with RFC-CDP-022 registered payload and governed record types;
- explicit boundary between wire payloads, governed records, and lifecycle envelope references;
- record-type validation rule for proposal admission references;
- governed path manifest fields for proposal admission record types;
- hash coverage clarified to include proposal-admission record types when available.

Promoted into Draft v0.5:

- admission artifact invisibility as a proposal-admission failure mode;
- explicit `proposal_sufficiency_ref`;
- explicit `formation_challenge_refs`;
- explicit `apc_gate_result_refs`;
- admission rule requiring `proposal_sufficiency_ref` before propose-or-later lifecycle state;
- governed path manifest coverage for proposal sufficiency, formation challenge, and APC gate result references;
- clarity that those three reference families are not excluded from the manifest.

Preserved from Draft v0.4:

- governed path severance;
- summary substitution;
- silent reference mutation;
- closure without repair resolution;
- governed path index, not warehouse;
- human-readable surface with governed record pointer;
- standing and recusal references;
- repair control surface with closure blocking;
- no embedded payloads in the base schema;
- reference lists required even when empty;
- governed path hash construction through a canonicalized manifest;
- registration-time content hashes;
- hash integrity is evidence, not legitimacy.

Not yet resolved:

- lifecycle-stage enum ownership;
- stage-specific standing enforcement by lifecycle protocols;
- referenced record hash propagation;
- canonical risk-tier vocabulary ownership;
- implementation-profile handling for sealed or air-gapped embedded bundles;
- detailed record schemas for Nemawashi, Execution Plane, and Covenant Plane hook records;
- whether Nemawashi sufficiency should be a separate gate or only an input to proposal sufficiency.

---

## 15. Summary

The Decision Lifecycle Envelope is the governed path index for a CDP decision.

It prevents governed path severance, summary substitution, silent reference mutation, closure without repair resolution, admission artifact invisibility, Nemawashi invisibility, and cross-plane hook ambiguity.

Its Nemawashi references make stakeholder mapping, pre-proposal consultation, early dissent, boundary conditions, and unresolved questions visible before proposal admission.

Its proposal admission references make Proposal Sufficiency, Formation Challenge, and APC artifacts visible in the governed path.

Its execution-control and covenant hooks preserve the boundary between a valid decision, executable action, and relationship-aware governance.

Its governed path hash covers those references so admission, participation, execution, and covenant integrity do not become blind spots.

It indexes governed records.

It does not replace them.
