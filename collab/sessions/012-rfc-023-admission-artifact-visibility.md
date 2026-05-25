# Session 012 Shared Chat: RFC-CDP-023 Admission Artifact Visibility Patch

```text
SESSION: 012-rfc-023-admission-artifact-visibility
DATE_OPENED: 2026-05-24
MODERATOR: Andie
STATUS: promotion-applied
MODE: shared-chat-file
CANON_TARGET: RFC-CDP-023-Decision-Lifecycle-Envelope.md
PURPOSE: Patch the Decision Lifecycle Envelope so Proposal Sufficiency, Formation Challenge, and APC gate result artifacts are explicitly indexed and covered by the governed_path_hash manifest.
```

## Why This Session Exists

Session 010 created:

```text
RFC-CDP-024 — Proposal Sufficiency Gate
```

Session 011 promoted:

```text
anti_premature_certainty_gate_result
```

in:

```text
RFC-CDP-022 — Protocol Payload Schema Registry
```

The Decision Lifecycle Envelope must now explicitly index the proposal admission artifacts produced by those RFCs.

Without that patch, Proposal Sufficiency and Formation Challenge can exist as governed records but remain invisible to the governed path index.

---

## Failure Mode

The failure mode is **admission artifact invisibility**.

Admission artifact invisibility occurs when Proposal Sufficiency, Formation Challenge, or Anti-Premature-Certainty gate result artifacts exist as governed records but are not explicitly indexed by the Decision Lifecycle Envelope.

When this happens, reviewers cannot reconstruct whether a proposal earned admission before entering the challenge lifecycle.

---

## Turn 001 — 2026-05-24 — C / G / Andie — Envelope-First Decision

```text
DATE: 2026-05-24
AUTHOR: Claude / Sonnet / C and ChatGPT / G
ROLE: challenger / architecture reviewer / canon promotion
STATUS: adjudicated-and-promoted
PURPOSE: Patch RFC-CDP-023 before RFC-CDP-041 so the envelope can carry the references that Propose will consume.
```

### C Position

C agreed with G that RFC-CDP-023 comes before RFC-CDP-041.

Reason:

The envelope is the governed path index. It must define what to carry before the Propose Protocol can define what to reference.

### G Position

G agreed.

Reason:

Envelope first. Propose second.

If the envelope cannot see the gate, the gate cannot govern the path.

### Integrity Catch

C identified a necessary integrity condition:

Adding the three new reference fields without adding them to the governed path manifest would create a hash coverage gap.

Therefore, the schema update and manifest coverage update must land in the same patch.

---

## Patch Applied

Patched:

```text
rfc/RFC-CDP-023-Decision-Lifecycle-Envelope.md
```

Advanced to:

```text
Draft v0.5
```

Commit:

```text
7b88e3d98b7d5bdd6a9829e8493c52b0385c58a7
```

### Changes Promoted

Added explicit proposal admission references:

```yaml
stage_record_refs:
  proposal_sufficiency_ref: <ref|null>
  formation_challenge_refs: [<ref>]
  apc_gate_result_refs: [<ref>]
```

Added admission rule:

```text
A Decision Lifecycle Envelope MUST NOT represent a proposal as admitted, with lifecycle_stage: propose or later, unless proposal_sufficiency_ref is non-null and the referenced proposal_sufficiency_record has sufficiency_status: sufficient or excepted.
```

Added failure mode:

```text
admission artifact invisibility
```

Updated governed path manifest coverage to include:

- `proposal_sufficiency_ref`
- `formation_challenge_refs`
- `apc_gate_result_refs`

Added explicit clarification that these references are included in the manifest and are not excluded.

---

## Promotion Decision

```text
PROMOTE TO CANON:
- RFC-CDP-023 Draft v0.5 admission artifact visibility patch

DEFER:
- RFC-CDP-041 Propose Protocol Proposal Sufficiency wiring
- RFC-CDP-042 Challenge Protocol formation challenge relationship
- RFC-CDP-045 Legitimize Protocol APC wiring
- lifecycle-stage enum ownership
- record_hash propagation
```
