# RFC-CDP-023 — Decision Lifecycle Envelope

Author: Kevin “Andie” Williams  
Status: Draft v0.4  
Series: Constitutional Decision Plane (CDP)  
Date: May 19, 2026  
Depends On: RFC-CDP-001, RFC-CDP-021, RFC-CDP-022, RFC-CDP-030, RFC-CDP-031, RFC-CDP-032, RFC-CDP-033, RFC-CDP-070  
Related: RFC-CDP-040, RFC-CDP-041, RFC-CDP-042, RFC-CDP-043, RFC-CDP-044, RFC-CDP-045, RFC-CDP-046, RFC-CDP-047, RFC-CDP-048, RFC-CDP-050, RFC-CDP-052, RFC-CDP-071, RFC-CDP-072, RFC-CDP-073, RFC-CDP-074, RFC-CDP-075, RFC-CDP-090, RFC-CDP-092

## Abstract

This RFC defines the **Decision Lifecycle Envelope**: the governed path index for a complete CDP decision across lifecycle stages.

The Decision Lifecycle Envelope is not a wire message and is not a warehouse for every artifact produced by a decision.

It is a persistent, updatable, human-readable and machine-readable index that identifies the decision, exposes its current lifecycle state, references the governed artifacts produced at each stage, preserves standing and recusal control surfaces, preserves appeal and repair control surfaces, and supports audit, appeal, repair, execution control, and learning.

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
- what appeal and repair status applies;
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

### 1.3 Integrity Failure Mode: Silent Reference Mutation

The specific integrity failure mode addressed by `governed_path_hash` is **silent reference mutation**.

Silent reference mutation occurs when a referenced governed record changes after the envelope registered it, while the envelope continues to point to the same reference identifier.

Example:

```text
The envelope references challenge record cr-abc.
cr-abc is later edited to remove a blocking objection.
The reference ID remains cr-abc.
A hash over reference IDs alone does not change.
The governed path appears clean, but the record was mutated.
```

The `governed_path_hash` MUST make this detectable by hashing a canonicalized manifest that includes registration-time hashes of referenced records, not merely their reference IDs.

A secondary integrity failure mode is **path reordering**, in which the order of governed records is changed to make a decision appear more linear, complete, or deliberate than it was.

The Governed Path Manifest therefore MUST preserve sequence position for ordered references.

### 1.4 Repair Failure Mode: Closure Without Repair Resolution

The repair failure mode this RFC addresses is **closure without repair resolution**.

Closure without repair resolution occurs when a decision advances to `status: closed` while appeal, repair, breach, or affected-party claim conditions exist and are recorded but not enforced.

Passive repair indexing is the mechanism.

Closure without repair resolution is the harm.

A Decision Lifecycle Envelope MUST expose repair status and MUST block closure when active appeal, unresolved repair, or unresolved affected-party claim conditions exist.

---

## 2. Design Rule: Governed Path Index, Not Warehouse

The Decision Lifecycle Envelope is a **governed path index**, not a warehouse.

It carries references to governed artifacts, not the artifacts themselves.

The envelope SHOULD include:

- identity;
- lifecycle state;
- human-readable summary with record pointer;
- standing and recusal control surface;
- repair control surface;
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

The following schema is the Draft v0.4 minimum viable Decision Lifecycle Envelope.

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

  # Repair control surface
  repair_control:
    repair_status: <enum>
    # Allowed: none|available|triggered|
    #   active|blocked|resolved
    closure_blocked: <boolean>
    closure_blocking_reason: <string|null>
    closure_blocking_refs: [<ref>]

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
    governed_path_hash_constructed_at: <timestamp>
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
- `repair_control`
- `repair_control.repair_status`
- `repair_control.closure_blocked`
- `repair_control.closure_blocking_reason`
- `repair_control.closure_blocking_refs`
- `stage_record_refs`
- all fields under `stage_record_refs`
- `integrity`
- `integrity.lineage_refs`
- `integrity.governed_path_hash`
- `integrity.governed_path_hash_algorithm`
- `integrity.governed_path_hash_constructed_at`

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

## 9. Repair Control Surface

The Decision Lifecycle Envelope connects to `RFC-CDP-070-Appeals-and-Contestability-Model.md` through a repair control surface.

The envelope reflects appeal and repair state.

It does not own or manage the appeal process, repair process, or repair state machine.

Those are governed by RFC-CDP-070 and RFC-CDP-092.

### 9.1 Repair Status

The envelope MUST include:

```yaml
repair_control:
  repair_status: <none|available|triggered|active|blocked|resolved>
  closure_blocked: <boolean>
  closure_blocking_reason: <string|null>
  closure_blocking_refs: [<ref>]
```

Allowed `repair_status` values:

| Value | Meaning |
|---|---|
| `none` | No appeal, repair, breach, or unresolved affected-party condition is known. |
| `available` | Appeal or contestability review is available under RFC-CDP-070, but not yet triggered. |
| `triggered` | An RFC-CDP-070 trigger event has been recorded. |
| `active` | Appeal, repair, breach review, or affected-party review is active. |
| `blocked` | Closure or progression is blocked by unresolved appeal, repair, breach, or affected-party claim conditions. |
| `resolved` | Prior appeal, repair, breach, or affected-party claim conditions have recorded resolution. |

### 9.2 No Duplicate Reference Lists

The repair control surface MUST NOT duplicate reference lists already carried elsewhere in the envelope.

The following remain the authoritative reference lists:

- `stage_record_refs.appeal_refs`
- `stage_record_refs.repair_refs`
- `affected_party_claim_refs`

`repair_control.closure_blocking_refs` exists only to identify which referenced records currently block closure.

It MUST NOT become a second source of truth for all appeal, repair, or affected-party claim references.

### 9.3 RFC-CDP-070 Trigger Binding

When any RFC-CDP-070 trigger event is recorded against a decision, the Decision Lifecycle Envelope MUST set:

```yaml
repair_control.repair_status: triggered
repair_control.closure_blocked: true
```

unless a later governed record shows that the trigger has been resolved, withdrawn, or superseded.

RFC-CDP-070 owns the trigger definitions.

RFC-CDP-023 reflects trigger state and enforces closure blocking.

### 9.4 Closure-Blocking Rule

A Decision Lifecycle Envelope MUST NOT advance to:

```yaml
status: closed
```

when any of the following are true:

- `repair_control.closure_blocked` is `true`;
- `stage_record_refs.appeal_refs` contains a reference with unresolved status under RFC-CDP-070;
- `affected_party_claim_refs` contains an unresolved claim;
- `stage_record_refs.repair_refs` contains an unresolved repair record under the Repair plane;
- a denial of constitutional standing has generated a Breach Record under RFC-CDP-033 and RFC-CDP-072 that has not been resolved.

This rule is normative.

Implementations MUST enforce it.

### 9.5 Unresolved Affected-Party Claims

An unresolved affected-party claim blocks closure regardless of whether a formal appeal record exists.

Requiring formal appeal as a condition of closure blocking would reintroduce the institutional permission failure that RFC-CDP-070 exists to prevent.

### 9.6 Human-Readable Repair Warning

When `repair_control.closure_blocked` is true, the human-readable surface SHOULD make the repair or appeal condition visible in plain language.

The summary MUST NOT represent a decision as closed or fully resolved while closure is blocked by active appeal, repair, breach, or affected-party claim conditions.

---

## 10. Human-Readable Surface Requirements

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

## 11. Governed Path Hash

The `governed_path_hash` prevents **silent reference mutation** and reduces **integrity theater**.

A compliant `governed_path_hash` MUST be computed over a canonicalized **Governed Path Manifest**, not over raw artifacts directly and not over the envelope shell alone.

Integrity theater occurs when a system presents a hash as proof of governance integrity, but the hash covers only a superficial shell, receipt, or summary rather than the governed path that matters.

Silent reference mutation occurs when a reference remains stable while the referenced governed record changes after registration.

The Governed Path Manifest MUST capture the reference and the content hash attested at the moment the record is registered into the envelope.

### 11.1 Governed Path Manifest

The Governed Path Manifest is a deterministic object derived from the Decision Lifecycle Envelope.

It contains stable references, stage order, registration-time content hashes, standing and recusal references, summary pointers, dissent references, lineage, and supersession links.

It does not contain full governed artifacts.

The manifest MUST include:

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

Each `ref_with_registration_hash` MUST include at least:

```yaml
ref_with_registration_hash:
  sequence_position: <integer>
  ref_id: <string>
  ref_type: <string>
  content_hash_at_registration: <hash|null>
  content_hash_algorithm: <string|null>
  record_schema_version: <semver|null>
  registered_at: <timestamp>
```

`content_hash_at_registration` is the hash captured by the envelope at the moment the reference is registered into the governed path.

It is authoritative for envelope integrity verification.

A hash declared by the referenced record at query time is not authoritative for verifying the envelope's governed path integrity unless it matches the registered hash or is otherwise reconciled by a superseding envelope.

### 11.2 Hash Construction

To compute `governed_path_hash`, implementations MUST:

1. Build the Governed Path Manifest from the Decision Lifecycle Envelope.
2. Include `governed_path_hash_algorithm` inside the manifest.
3. Include `governed_path_hash_constructed_at` inside the manifest.
4. Normalize all timestamps, identifiers, enum values, references, and hash strings according to the canonicalization rules in this RFC.
5. Assign `sequence_position` to every entry in ordered lists.
6. Sort unordered reference lists lexicographically by `ref_id` unless an explicit lifecycle order is defined.
7. Preserve lifecycle stage order exactly as defined in `ordered_stage_refs`.
8. Serialize the manifest as canonical JSON.
9. Hash the canonical JSON byte sequence using the declared `governed_path_hash_algorithm`.

The default algorithm for Draft v0.4 is:

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

### 11.3 Sequence Position and Tiebreakers

For any ordered reference list, each entry MUST include `sequence_position`.

Sequence positions MUST be assigned by ascending `registered_at` timestamp.

When two records have the same `registered_at` timestamp, ties MUST be broken by lexicographic ordering of `ref_id`.

If both `registered_at` and `ref_id` are identical, the envelope is invalid because two distinct governed references cannot be deterministically ordered.

Implementations MUST NOT rely on array insertion order alone unless that order has been produced by these canonical rules.

### 11.4 What MUST Be Hashed

The Governed Path Manifest MUST cover:

- `manifest_schema_version`
- `governed_path_hash_algorithm`
- `governed_path_hash_constructed_at`
- `envelope_id`
- `envelope_schema_version`
- `decision_id`
- `decision_type`
- `lifecycle_stage`
- `status`
- `standing_status`
- `repair_control.repair_status`
- `repair_control.closure_blocked`
- `repair_control.closure_blocking_refs`, including registration-time hashes where available;
- `human_summary.summary_governed_by_ref`
- `human_summary.material_dissent_refs`, including registration-time hashes where available;
- `standing_record_refs`, including registration-time hashes where available;
- `recusal_record_refs`, including registration-time hashes where available;
- `affected_party_claim_refs`, including registration-time hashes where available;
- all fields under `stage_record_refs`, represented as ordered stage references;
- each referenced record's `content_hash_at_registration` and `content_hash_algorithm` when available;
- `integrity.lineage_refs`, including registration-time hashes where available;
- `integrity.supersedes_envelope_id`
- `integrity.superseded_by_envelope_id`

### 11.5 What MUST NOT Be Hashed Directly

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

Those artifacts MUST expose or be associated with their own content hash values.

The `governed_path_hash` hashes the path manifest and registration-time content hashes, not the entire universe of governed content.

### 11.6 Referenced Record Hashes

Every governed record type referenced by a Decision Lifecycle Envelope MUST define, in its governing RFC or schema, how its content hash is computed.

Until that requirement is propagated across all referenced record types, implementations MUST document their local record-hash computation rule.

Every governed record referenced by a Decision Lifecycle Envelope SHOULD expose:

```yaml
record_hash: <hash>
record_hash_algorithm: <string>
record_schema_version: <semver>
```

At registration time, the envelope MUST capture the referenced record's current content hash into:

```yaml
content_hash_at_registration: <hash|null>
content_hash_algorithm: <string|null>
record_schema_version: <semver|null>
registered_at: <timestamp>
```

If a referenced record does not yet expose a content hash, the manifest MUST still include the reference with:

```yaml
content_hash_at_registration: null
content_hash_algorithm: null
```

Such a manifest is valid but integrity-incomplete.

An integrity-incomplete envelope MUST NOT be represented as fully integrity-verified.

### 11.7 Canonicalization Rules

Draft v0.4 canonicalization rules:

- Serialize the Governed Path Manifest as canonical JSON.
- UTF-8 encoding MUST be used.
- Object keys MUST be sorted lexicographically at every nesting level.
- Whitespace outside string values MUST NOT be emitted.
- Arrays that represent unordered reference sets MUST be sorted lexicographically by `ref_id`.
- Arrays that represent lifecycle order MUST preserve canonical lifecycle order.
- Ordered reference entries MUST include `sequence_position`.
- Sequence positions MUST be assigned by ascending `registered_at`, then lexicographic `ref_id`.
- Empty reference lists MUST be serialized as empty arrays `[]`.
- `null` values MUST be serialized explicitly.
- Timestamps MUST use UTC ISO-8601 format with `Z` suffix.
- Enum values MUST be lowercase.
- Hash algorithm identifiers MUST be lowercase.
- The hash algorithm identifier MUST appear inside the manifest itself.

If future drafts adopt an external canonicalization standard, this RFC MUST name it explicitly and define migration behavior.

Canonicalization rules are interoperability requirements. Implementations MUST NOT substitute local canonicalization behavior while claiming cross-implementation hash compatibility.

### 11.8 Supersession and Updates

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

A change to any referenced registration-time content hash, standing status, repair status, closure-blocking state, lifecycle stage, status, summary governed-by reference, material dissent reference, stage reference, lineage reference, sequence position, or supersession link MUST produce a new governed path hash.

---

## 12. Security and Governance Considerations

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
- closure-blocking enforcement;
- retention and deletion policy;
- audit logging;
- integrity verification.

A valid `governed_path_hash` proves only that the canonicalized governed path manifest matches the stored hash. It does not prove that the underlying decision was correct, legitimate, sufficient, unbiased, or harmless.

Hash integrity is evidence, not legitimacy.

Legitimacy is governed by the lifecycle protocols, especially `RFC-CDP-045-Legitimize-Protocol.md`, and by authority, standing, and recusal constraints in `RFC-CDP-033-Standing-and-Recusal-Model.md`.

A valid hash may preserve an illegitimate path with perfect fidelity.

That is useful evidence, not approval.

---

## 13. Status of This Draft

This RFC was created from Session 003 of the CDP collaboration process and updated in Sessions 004 and 006.

Promoted into this draft:

- Decision Lifecycle Envelope as separate from Wire Message Envelope;
- governed path severance as the primary failure mode;
- summary substitution as a secondary failure mode;
- silent reference mutation as the integrity failure mode;
- closure without repair resolution as the repair failure mode;
- governed path index, not warehouse;
- required human-readable surface with governed record pointer;
- required standing status and standing/recusal references;
- repair control surface with closure blocking;
- no embedded payloads in the base schema;
- required reference lists even when empty;
- governed path hash construction through a canonicalized Governed Path Manifest;
- registration-time content hashes as the bridge between path integrity and artifact integrity;
- sequence position and tiebreaker rules for ordered references;
- canonicalization and supersession rules;
- distinction between hash integrity and legitimacy.

Not yet resolved:

- whether lifecycle-stage enum belongs here or in `RFC-CDP-022-Protocol-Payload-Schema-Registry.md`;
- how each lifecycle protocol will enforce stage-specific binding to standing records;
- implementation profiles for embedded or sealed payloads;
- whether this schema should later move from Draft to Candidate after implementation testing;
- whether referenced record hash requirements should be promoted into a shared Common Building Blocks or Record Schema RFC;
- how implementation models will populate `repair_control` consistently from RFC-CDP-070 and RFC-CDP-092.

---

## 14. Summary

The Decision Lifecycle Envelope is the governed path index for a CDP decision.

It prevents governed path severance, summary substitution, silent reference mutation, and closure without repair resolution.

It carries the control surface and references the governed record.

It is not a warehouse.

It is not a wire message.

Its `repair_control` surface makes appeal and repair state visible without duplicating the authoritative appeal, repair, and affected-party reference lists.

Its `governed_path_hash` is computed over a canonicalized Governed Path Manifest that includes stage references, standing references, repair status, closure-blocking state, summary pointers, lineage, supersession links, sequence positions, and registration-time content hashes for referenced records.

It is the object that lets a decision remain legible, legitimate, auditable, contestable, executable only under authority, recordable, repairable, and learnable across time.
