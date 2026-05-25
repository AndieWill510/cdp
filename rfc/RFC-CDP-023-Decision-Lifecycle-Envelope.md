# RFC-CDP-023 — Decision Lifecycle Envelope

Author: Kevin “Andie” Williams  
Status: Draft v0.5  
Series: Constitutional Decision Plane (CDP)  
Date: May 24, 2026  
Updates: RFC-CDP-023 v0.4  
Depends On: RFC-CDP-001, RFC-CDP-021, RFC-CDP-022, RFC-CDP-024, RFC-CDP-025, RFC-CDP-030, RFC-CDP-031, RFC-CDP-032, RFC-CDP-033, RFC-CDP-070  
Related: RFC-CDP-040, RFC-CDP-041, RFC-CDP-042, RFC-CDP-043, RFC-CDP-044, RFC-CDP-045, RFC-CDP-046, RFC-CDP-047, RFC-CDP-048, RFC-CDP-050, RFC-CDP-052, RFC-CDP-071, RFC-CDP-072, RFC-CDP-073, RFC-CDP-074, RFC-CDP-075, RFC-CDP-090, RFC-CDP-092

## Abstract

This RFC defines the **Decision Lifecycle Envelope**: the governed path index for a complete CDP decision across lifecycle stages.

The Decision Lifecycle Envelope is not a wire message and is not a warehouse for every artifact produced by a decision.

It is a persistent, updatable, human-readable and machine-readable index that identifies the decision, exposes lifecycle state, references governed artifacts, preserves standing and recusal control surfaces, preserves proposal admission artifacts, preserves appeal and repair control surfaces, and supports audit, appeal, repair, execution control, and learning.

Draft v0.5 updates Draft v0.4 by making Proposal Sufficiency, Formation Challenge, and Anti-Premature-Certainty gate result artifacts visible in the envelope and covered by the governed path manifest.

---

## 1. Purpose and Failure Modes

The Decision Lifecycle Envelope answers:

- what decision is being governed;
- what lifecycle stage it is in;
- what its current status is;
- what human-readable summary represents the governed record;
- what standing and recusal status applies;
- whether a proposal earned admission before entering the challenge lifecycle;
- what proposal sufficiency, formation challenge, and APC gate result artifacts exist;
- what appeal and repair status applies;
- what governed records exist across lifecycle stages;
- what lineage and integrity markers allow reconstruction of the governed path.

This RFC addresses five failure modes:

1. **Governed path severance** — the decision record exists, but the governed path is scattered, loosely linked, or replaced by summary.
2. **Summary substitution** — a human-readable summary is treated as equivalent to the governed record it summarizes.
3. **Silent reference mutation** — a referenced governed record changes after registration while the envelope still points to the same reference identifier.
4. **Closure without repair resolution** — a decision is marked closed while appeal, repair, breach, or affected-party claim conditions remain unresolved.
5. **Admission artifact invisibility** — Proposal Sufficiency, Formation Challenge, or APC gate result artifacts exist as governed records but are not explicitly indexed by the envelope.

Admission artifact invisibility creates a governed path gap between formation and proposal/challenge. The envelope therefore carries explicit references for proposal sufficiency, formation challenge, and APC gate result artifacts.

---

## 2. Design Rule: Governed Path Index, Not Warehouse

The Decision Lifecycle Envelope is a **governed path index**, not a warehouse.

It carries references to governed artifacts, not the artifacts themselves.

The envelope includes identity, lifecycle state, human-readable summary with record pointer, standing and recusal control surface, proposal admission references, repair control surface, governed stage references, lineage, and integrity markers.

Full artifacts should be stored as governed records and referenced by ID or URI.

Embedded payloads are not part of the base Decision Lifecycle Envelope schema. Implementation profiles may define sealed, portable, or air-gapped variants without changing base semantics.

---

## 3. Minimum Viable Schema

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
    framing_ref: <ref|null>
    proposal_sufficiency_ref: <ref|null>
    # REQUIRED after admission. Must point to a proposal_sufficiency_record
    # with sufficiency_status: sufficient or excepted.
    # Null only before admission gate is evaluated.
    formation_challenge_refs: [<ref>]
    # Required field. Empty list is valid. Records any formation challenges
    # raised before proposal admission.
    apc_gate_result_refs: [<ref>]
    # Required field. Empty list is valid. Records APC gate evaluations per
    # RFC-CDP-022 and RFC-CDP-024.
    proposal_ref: <ref|null>
    challenge_refs: [<ref>]
    evidence_refs: [<ref>]
    test_refs: [<ref>]
    adjudication_ref: <ref|null>
    legitimacy_ref: <ref|null>
    execution_constraint_ref: <ref|null>
    execution_record_ref: <ref|null>
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

Reference list fields are required even when empty. An empty list is informative. An absent list is ambiguous.

---

## 4. Human-Readable Surface Requirements

Every human-readable summary must point to the governed record it summarizes through `summary_governed_by_ref`.

The summary must not claim to be the governed record, suppress material dissent, or describe the decision as more resolved than the governed records show.

If `known_uncertainties` is empty, that is a positive claim that no material uncertainty is currently known.

---

## 5. Proposal Admission References

The envelope connects to RFC-CDP-024 and RFC-CDP-022 through three explicit references:

```yaml
stage_record_refs:
  proposal_sufficiency_ref: <ref|null>
  formation_challenge_refs: [<ref>]
  apc_gate_result_refs: [<ref>]
```

### 5.1 proposal_sufficiency_ref

`proposal_sufficiency_ref` points to the governed `proposal_sufficiency_record` that establishes whether the proposal earned admission.

After a proposal is admitted, `proposal_sufficiency_ref` is required. Before admission, it may be null only when the proposal is still in formation or no sufficiency record has been submitted.

### 5.2 formation_challenge_refs

`formation_challenge_refs` points to governed records produced by `RAISE_FORMATION_CHALLENGE` under RFC-CDP-024. The list is required and may be empty.

### 5.3 apc_gate_result_refs

`apc_gate_result_refs` points to governed `anti_premature_certainty_gate_result` records defined by RFC-CDP-022. The list is required and may be empty.

### 5.4 Admission Rule

A Decision Lifecycle Envelope MUST NOT represent a proposal as admitted, with `lifecycle_stage: propose` or later, unless:

- `proposal_sufficiency_ref` is non-null; and
- the referenced `proposal_sufficiency_record` has `sufficiency_status: sufficient` or `sufficiency_status: excepted`.

An envelope with a null `proposal_sufficiency_ref` and `lifecycle_stage` at or past `propose` is non-compliant with this RFC.

---

## 6. Standing and Recusal Binding

The envelope connects to RFC-CDP-033 through top-level `standing_status`, `standing_record_refs`, `recusal_record_refs`, and `affected_party_claim_refs`.

These records are referenced, not embedded.

Each stage record reference must be interpretable against the standing and recusal records that governed that stage. The envelope carries references; lifecycle protocol RFCs enforce rules.

---

## 7. Repair Control Surface

The envelope connects to RFC-CDP-070 through `repair_control`.

When any RFC-CDP-070 trigger event is recorded against a decision, the envelope sets `repair_status: triggered` and `closure_blocked: true`, unless a later governed record shows that the trigger has been resolved, withdrawn, or superseded.

A Decision Lifecycle Envelope cannot advance to `status: closed` while unresolved appeal, repair, breach, or affected-party claim conditions remain.

An unresolved affected-party claim blocks closure regardless of whether a formal appeal record exists.

---

## 8. Governed Path Hash

The `governed_path_hash` is computed over a canonicalized Governed Path Manifest.

Hash integrity is evidence, not legitimacy.

A valid hash may preserve an illegitimate path with perfect fidelity. That is useful evidence, not approval.

### 8.1 Governed Path Manifest Structure

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

  proposal_admission_refs:
    proposal_sufficiency:
      ref_id: <ref|null>
      content_hash_at_registration: <hash|null>
    formation_challenges:
      - ref_id: <ref>
        content_hash_at_registration: <hash>
        sequence_position: <integer>
    apc_gate_results:
      - ref_id: <ref>
        content_hash_at_registration: <hash>

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

Each `ref_with_registration_hash` includes sequence position, reference ID, reference type, registration-time content hash, hash algorithm, record schema version, and registration timestamp.

### 8.2 Hash Coverage

The manifest covers:

- envelope identity and schema version;
- `decision_id` and `decision_type`;
- `lifecycle_stage` and `status`;
- `standing_status`;
- `repair_control.repair_status` and `repair_control.closure_blocked`;
- summary governed-by and material dissent references;
- standing, recusal, and affected-party claim references;
- `proposal_sufficiency_ref`;
- `formation_challenge_refs`;
- `apc_gate_result_refs`;
- all other `stage_record_refs`;
- closure-blocking references;
- registration-time content hashes and algorithms when available;
- lineage and supersession links.

Adding proposal sufficiency, formation challenge, and APC gate result references to the envelope without adding them to manifest coverage would create an integrity gap. Therefore the v0.5 schema and manifest changes are inseparable.

### 8.3 Fields Excluded from the Manifest

Full governed artifacts, mutable display formatting, and access-control metadata are not hashed directly by the governed path manifest.

`proposal_sufficiency_ref`, `formation_challenge_refs`, and `apc_gate_result_refs` are included in the manifest. They are not excluded.

### 8.4 Canonicalization Rules

The manifest uses canonical JSON, UTF-8 encoding, lexicographically sorted object keys, explicit nulls, empty arrays rather than omitted lists, lowercase enum values, lowercase hash algorithm identifiers, and UTC ISO-8601 timestamps with `Z` suffix.

Ordered reference entries include `sequence_position`, assigned by ascending `registered_at`, then lexicographic `ref_id`.

The default algorithm for Draft v0.5 is `sha256`.

If a referenced record lacks a content hash, the manifest still includes the reference with null hash fields. Such a manifest is valid but integrity-incomplete and must not be represented as fully integrity-verified.

---

## 9. Security and Governance Considerations

Decision Lifecycle Envelopes may expose affected-party claims, standing and recusal state, proposal sufficiency state, formation challenge existence, APC gate result existence, challenge existence, dissent references, evidence references, appeal or repair hooks, execution constraints, and learning artifacts.

Implementations should address access control, redaction, culturally appropriate handling, evidence custody, affected-party review, appeal rights, repair triggers, closure blocking, admission blocking, retention, audit logging, and integrity verification.

---

## 10. Status of This Draft

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
- downstream Propose, Challenge, and Legitimize protocol consumption.

---

## 11. Summary

The Decision Lifecycle Envelope is the governed path index for a CDP decision.

It prevents governed path severance, summary substitution, silent reference mutation, closure without repair resolution, and admission artifact invisibility.

Its proposal admission references make Proposal Sufficiency, Formation Challenge, and APC gate artifacts visible in the governed path.

Its governed path hash covers those references so admission integrity does not become a blind spot.
