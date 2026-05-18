# RFC-CDP-023 — Decision Lifecycle Envelope

Author: Kevin “Andie” Williams  
Status: Draft v0.2  
Series: Constitutional Decision Plane (CDP)  
Date: May 17, 2026  
Depends On: RFC-CDP-001, RFC-CDP-021, RFC-CDP-022, RFC-CDP-030, RFC-CDP-031, RFC-CDP-032, RFC-CDP-033  
Related: RFC-CDP-040, RFC-CDP-041, RFC-CDP-042, RFC-CDP-043, RFC-CDP-044, RFC-CDP-045, RFC-CDP-046, RFC-CDP-047, RFC-CDP-048, RFC-CDP-050, RFC-CDP-052, RFC-CDP-070, RFC-CDP-071, RFC-CDP-072, RFC-CDP-073, RFC-CDP-074, RFC-CDP-075, RFC-CDP-090

## Abstract

This RFC defines the **Decision Lifecycle Envelope**: the governed path index for a complete CDP decision across lifecycle stages.

The Decision Lifecycle Envelope is not a wire message and is not a warehouse for every artifact produced by a decision.

It is a persistent, updatable, human-readable and machine-readable index that identifies the decision, exposes its current lifecycle state, references the governed artifacts produced at each stage, preserves standing and recusal control surfaces, and supports audit, appeal, repair, execution control, and learning.

The Wire Message Envelope is defined separately in `RFC-CDP-021-Wire-Message-Envelope-Schema`.

---

## 1. Purpose and Failure Mode

### 1.1 Purpose

The Decision Lifecycle Envelope answers:

- what decision is being governed;
- what lifecycle stage it is in;
- what its current status is;
- what human-readable summary represents the governed record;
- what standing and recusal status applies;
- what governed records exist for framing, proposal, challenge, evidence, testing, adjudication, legitimacy, execution, appeal, repair, and learning;
- what lineage and integrity markers allow reconstruction of the governed path.

### 1.2 Failure Mode: Governed Path Severance

The failure mode this RFC addresses is **governed path severance**.

Governed path severance occurs when a decision record exists, but the governed path that makes the decision legitimate or illegitimate has been lost, scattered, loosely linked, or replaced by summary.

A decision may have standing records, challenge memos, test results, adjudication records, legitimacy records, execution constraints, dissent, repair claims, and learning artifacts. If those artifacts are stored separately and are not authoritatively indexed, later reviewers cannot reconstruct:

- which standing records governed which stage;
- whether a challenge was resolved or merely noted;
- what authority basis legitimization used;
- whether execution constraints derived from adjudication or were added afterward;
- whether dissent was preserved or collapsed;
- what appeal or repair path remains available.

A governance receipt is not a governed path.

The Decision Lifecycle Envelope exists to preserve the governed path without collapsing the path into an unreadable pile.

---

## 2. Design Rule: Governed Path Index, Not Warehouse

The Decision Lifecycle Envelope is a **governed path index**, not a warehouse.

It carries references to governed artifacts, not the artifacts themselves.

The envelope SHOULD include:

- identity;
- lifecycle state;
- human-readable summary with record pointer;
- standing and recusal control surface;
- required governed stage references;
- lineage;
- integrity markers.

The envelope SHOULD NOT embed full artifacts that have their own governed lifecycle.

Full artifacts SHOULD be stored as governed records and referenced by ID or URI.

---

## 3. Secondary Failure Mode: Summary Substitution

The Decision Lifecycle Envelope must also prevent **summary substitution**.

Summary substitution occurs when a human-readable summary is treated as equivalent to the governed record.

A summary may say:

```text
The proposal was challenged and approved.
```

The governed record may show:

```text
The challenge was filed but not adjudicated. Approval was granted by the proposer's delegated authority under a scope that may not cover this decision type.
```

These are structurally different.

Therefore, every human-readable summary in a Decision Lifecycle Envelope MUST point to the governed record it summarizes.

A summary without a governed record pointer is not CDP-compliant.

---

## 4. Relationship to Wire Message Envelope

The Wire Message Envelope is per-message and is defined in `RFC-CDP-021-Wire-Message-Envelope-Schema`.

The Decision Lifecycle Envelope is per-decision.

A decision lifecycle may contain many wire messages.

The Decision Lifecycle Envelope indexes the governed path across those messages and the governed artifacts they produce.

Implementations SHOULD connect Wire Message Envelopes and Decision Lifecycle Envelopes through:

- `decision_id`;
- `correlation_id`;
- lineage references;
- governed record references;
- integrity hashes.

These two envelope types MUST NOT be conflated.

---

## 5. Minimum Viable Schema

The following schema is the Draft v0.2 minimum viable Decision Lifecycle Envelope.

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
  # Allowed: nemawashi|propose|challenge|
  #   test|adjudicate|legitimize|execute|
  #   record|learn|repair|appeal
  status: <enum>
  # Allowed: draft|under_challenge|
  #   under_test|adjudicated|legitimized|
  #   execution_queued|executed|recorded|
  #   appealed|repair_required|closed

  # Human-readable surface
  human_summary:
    summary_text: <string>
    plain_language_status: <string>
    known_uncertainties: [<string>]
    material_dissent_refs: [<ref>]
    summary_governed_by_ref: <ref>

  # Standing control surface
  standing_status: <enum>
  # Allowed: unreviewed|valid|contested|
  #   recusal_active|blocked|emergency
  standing_record_refs: [<ref>]
  recusal_record_refs: [<ref>]
  affected_party_claim_refs: [<ref>]

  # Governed stage references
  stage_record_refs:
    framing_ref: <ref|null>
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
    supersedes_envelope_id: <uuid|null>
    superseded_by_envelope_id: <uuid|null>
```

---

## 6. Required Field Rules

The following fields are REQUIRED:

- `envelope_id`
- `envelope_schema_version`
- `decision_id`
- `decision_type`
- `created_at`
- `updated_at`
- `created_by`
- `lifecycle_stage`
- `status`
- `human_summary`
- `human_summary.summary_text`
- `human_summary.plain_language_status`
- `human_summary.known_uncertainties`
- `human_summary.material_dissent_refs`
- `human_summary.summary_governed_by_ref`
- `standing_status`
- `standing_record_refs`
- `recusal_record_refs`
- `affected_party_claim_refs`
- `stage_record_refs`
- all fields under `stage_record_refs`
- `integrity`
- `integrity.lineage_refs`
- `integrity.governed_path_hash`
- `integrity.governed_path_hash_algorithm`

Reference list fields are REQUIRED even when empty.

An empty list `[]` is informative.

An absent reference list is ambiguous and non-compliant.

---

## 7. Embedded Payload Rule

Embedded payloads are NOT permitted in the base Decision Lifecycle Envelope schema.

The base envelope carries governed references.

Portability, air-gapped operation, sealed legal bundles, or tamper-resistant embedding MAY be defined by Implementation Profile RFCs in the `120–149` band.

Those profiles MUST NOT silently alter the base Decision Lifecycle Envelope semantics.

---

## 8. Standing and Recusal Binding

The Decision Lifecycle Envelope connects to `RFC-CDP-033-Standing-and-Recusal-Model.md` through three mechanisms.

### 8.1 Standing Status

The envelope MUST include top-level `standing_status`.

Allowed values:

```text
unreviewed | valid | contested | recusal_active | blocked | emergency
```

This field is the control-surface warning light for human and machine reviewers.

### 8.2 Standing and Recusal References

The envelope MUST include:

- `standing_record_refs`
- `recusal_record_refs`
- `affected_party_claim_refs`

These records MUST NOT be embedded in the base envelope.

They are governed records with their own identity, lifecycle, and contestability.

### 8.3 Stage-Specific Interpretation

Each stage record reference MUST be interpretable against the standing and recusal records that governed that stage.

For example, an adjudication record must be readable alongside standing records to verify that the adjudicator had valid standing and was not improperly recused or conflicted.

The envelope carries the references.

The lifecycle protocol RFCs enforce the rules.

---

## 9. Human-Readable Surface Requirements

A Decision Lifecycle Envelope MUST include a human-readable surface.

Minimum fields:

```yaml
human_summary:
  summary_text: <string>
  plain_language_status: <string>
  known_uncertainties: [<string>]
  material_dissent_refs: [<ref>]
  summary_governed_by_ref: <ref>
```

The summary MUST NOT claim to be the governed record.

The summary MUST point to the governed record it represents.

The summary MUST NOT suppress material dissent.

The summary MUST NOT describe the decision as more resolved than the governed records show.

If `known_uncertainties` is empty, that is a positive claim that no material uncertainty is currently known. Implementations SHOULD support attestation of that claim.

---

## 10. Governed Path Hash

The `governed_path_hash` prevents **integrity theater**.

Integrity theater occurs when a system presents a hash as proof of governance integrity, but the hash covers only a superficial shell, receipt, or summary rather than the governed path that matters.

A compliant `governed_path_hash` MUST be computed over a canonicalized **Governed Path Manifest**, not over raw artifacts directly and not over the envelope shell alone.

### 10.1 Governed Path Manifest

The Governed Path Manifest is a deterministic object derived from the Decision Lifecycle Envelope.

It contains stable references, stage order, declared record hashes, standing and recusal references, summary pointers, dissent references, lineage, and supersession links.

It does not contain full governed artifacts.

The manifest MUST include:

```yaml
governed_path_manifest:
  manifest_schema_version: <semver>
  envelope_id: <uuid>
  envelope_schema_version: <semver>
  decision_id: <uuid>
  decision_type: <string>
  lifecycle_stage: <enum>
  status: <enum>
  standing_status: <enum>

  human_summary_refs:
    summary_governed_by_ref: <ref>
    material_dissent_refs: [<ref>]

  standing_refs:
    standing_record_refs: [<ref>]
    recusal_record_refs: [<ref>]
    affected_party_claim_refs: [<ref>]

  ordered_stage_refs:
    - stage: nemawashi
      refs: [<ref_with_record_hash>]
    - stage: propose
      refs: [<ref_with_record_hash>]
    - stage: challenge
      refs: [<ref_with_record_hash>]
    - stage: test
      refs: [<ref_with_record_hash>]
    - stage: adjudicate
      refs: [<ref_with_record_hash>]
    - stage: legitimize
      refs: [<ref_with_record_hash>]
    - stage: execute
      refs: [<ref_with_record_hash>]
    - stage: record
      refs: [<ref_with_record_hash>]
    - stage: learn
      refs: [<ref_with_record_hash>]
    - stage: appeal
      refs: [<ref_with_record_hash>]
    - stage: repair
      refs: [<ref_with_record_hash>]

  lineage_refs: [<ref>]
  supersedes_envelope_id: <uuid|null>
  superseded_by_envelope_id: <uuid|null>
```

Each `ref_with_record_hash` MUST include at least:

```yaml
ref_with_record_hash:
  ref_id: <string>
  ref_type: <string>
  record_hash: <hash>
  record_hash_algorithm: <string>
```

### 10.2 Hash Construction

To compute `governed_path_hash`, implementations MUST:

1. Build the Governed Path Manifest from the Decision Lifecycle Envelope.
2. Normalize all timestamps, identifiers, enum values, references, and hash strings according to the canonicalization rules in this RFC.
3. Sort unordered reference lists lexicographically by `ref_id` unless an explicit lifecycle order is defined.
4. Preserve lifecycle stage order exactly as defined in `ordered_stage_refs`.
5. Serialize the manifest as canonical JSON.
6. Hash the canonical JSON byte sequence using the declared `governed_path_hash_algorithm`.

The default algorithm for Draft v0.2 is:

```text
SHA-256
```

The resulting digest MUST be stored in:

```yaml
integrity.governed_path_hash
```

The algorithm identifier MUST be stored in:

```yaml
integrity.governed_path_hash_algorithm
```

Recommended identifier:

```text
sha256
```

### 10.3 What MUST Be Hashed

The Governed Path Manifest MUST cover:

- `envelope_id`
- `envelope_schema_version`
- `decision_id`
- `decision_type`
- `lifecycle_stage`
- `status`
- `standing_status`
- `human_summary.summary_governed_by_ref`
- `human_summary.material_dissent_refs`
- `standing_record_refs`
- `recusal_record_refs`
- `affected_party_claim_refs`
- all fields under `stage_record_refs`, represented as ordered stage references;
- each referenced record's `record_hash` and `record_hash_algorithm` when available;
- `integrity.lineage_refs`
- `integrity.supersedes_envelope_id`
- `integrity.superseded_by_envelope_id`

### 10.4 What MUST NOT Be Hashed Directly

The Governed Path Manifest MUST NOT directly hash or embed:

- full evidence files;
- full challenge memos;
- full test outputs;
- full adjudication records;
- full legitimacy records;
- full execution logs;
- full appeal records;
- full repair records;
- full learning artifacts;
- model outputs;
- mutable display summaries;
- access-control metadata that can change without altering governance content.

Those artifacts MUST expose or be associated with their own `record_hash` values.

The `governed_path_hash` hashes the path manifest and declared record hashes, not the entire universe of governed content.

### 10.5 Referenced Record Hashes

Every governed record referenced by a Decision Lifecycle Envelope SHOULD expose:

```yaml
record_hash: <hash>
record_hash_algorithm: <string>
record_schema_version: <semver>
```

If a referenced record does not yet expose a `record_hash`, the manifest MUST still include the reference with:

```yaml
record_hash: null
record_hash_algorithm: null
```

Such a manifest is valid but integrity-incomplete.

An integrity-incomplete envelope MUST NOT be represented as fully integrity-verified.

### 10.6 Canonicalization Rules

Draft v0.2 canonicalization rules:

- Serialize the Governed Path Manifest as canonical JSON.
- Object keys MUST be sorted lexicographically.
- Arrays that represent unordered reference sets MUST be sorted lexicographically by `ref_id`.
- Arrays that represent lifecycle order MUST preserve canonical lifecycle order.
- Empty reference lists MUST be serialized as empty arrays `[]`.
- `null` values MUST be serialized explicitly.
- Timestamps MUST use UTC ISO-8601 format with `Z` suffix.
- Enum values MUST be lowercase.
- Hash algorithm identifiers MUST be lowercase.
- Whitespace outside string values MUST NOT affect the hash.

If future drafts adopt an external canonicalization standard, this RFC MUST name it explicitly and define migration behavior.

### 10.7 Supersession and Updates

A new envelope version that changes the governed path MUST produce a new `governed_path_hash`.

A superseding envelope MUST set:

```yaml
integrity.supersedes_envelope_id: <prior_envelope_id>
```

The superseded envelope SHOULD set:

```yaml
integrity.superseded_by_envelope_id: <new_envelope_id>
```

If the superseded envelope cannot be updated, the superseding envelope's lineage MUST preserve the prior envelope reference.

A change to display formatting alone SHOULD NOT produce a new governed path hash unless it changes the human summary fields covered by the manifest.

A change to any referenced record hash, standing status, lifecycle stage, status, summary governed-by reference, material dissent reference, stage reference, lineage reference, or supersession link MUST produce a new governed path hash.

---

## 11. Security and Governance Considerations

Decision Lifecycle Envelopes are governance-sensitive.

They may expose:

- affected-party claims;
- standing and recusal state;
- challenge existence;
- dissent references;
- evidence references;
- appeal or repair hooks;
- execution constraints;
- learning artifacts.

Implementations SHOULD consider:

- access control;
- redaction;
- culturally appropriate handling;
- evidence custody;
- affected-party review;
- appeal rights;
- repair-plane triggers;
- retention and deletion policy;
- audit logging;
- integrity verification.

A valid `governed_path_hash` proves only that the canonicalized governed path manifest matches the stored hash. It does not prove that the underlying decision was correct, legitimate, sufficient, unbiased, or harmless.

Hash integrity is evidence, not legitimacy.

---

## 12. Status of This Draft

This RFC was created from Session 003 of the CDP collaboration process and updated in Session 004.

Promoted into this draft:

- Decision Lifecycle Envelope as separate from Wire Message Envelope;
- governed path severance as the primary failure mode;
- summary substitution as a secondary failure mode;
- governed path index, not warehouse;
- required human-readable surface with governed record pointer;
- required standing status and standing/recusal references;
- no embedded payloads in the base schema;
- required reference lists even when empty;
- governed path hash construction through a canonicalized Governed Path Manifest;
- referenced record hashes as the bridge between path integrity and artifact integrity;
- canonicalization and supersession rules.

Not yet resolved:

- whether lifecycle-stage enum belongs here or in `RFC-CDP-022-Protocol-Payload-Schema-Registry.md`;
- how each lifecycle protocol will enforce stage-specific binding to standing records;
- implementation profiles for embedded or sealed payloads;
- whether this schema should later move from Draft to Candidate after implementation testing;
- whether referenced record hash requirements should be promoted into a shared Common Building Blocks or Record Schema RFC.

---

## 13. Summary

The Decision Lifecycle Envelope is the governed path index for a CDP decision.

It prevents governed path severance and summary substitution.

It carries the control surface and references the governed record.

It is not a warehouse.

It is not a wire message.

Its `governed_path_hash` is computed over a canonicalized Governed Path Manifest that includes stage references, standing references, summary pointers, lineage, supersession links, and referenced record hashes.

It is the object that lets a decision remain legible, legitimate, auditable, contestable, executable only under authority, recordable, repairable, and learnable across time.
