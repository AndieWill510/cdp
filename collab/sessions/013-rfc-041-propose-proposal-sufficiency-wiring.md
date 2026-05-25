# Session 013 Shared Chat: RFC-CDP-041 Propose Protocol Proposal Sufficiency Wiring

```text
SESSION: 013-rfc-041-propose-proposal-sufficiency-wiring
DATE_OPENED: 2026-05-24
MODERATOR: Andie
STATUS: promotion-applied
MODE: shared-chat-file
CANON_TARGET: RFC-CDP-041-Propose-Protocol.md
PURPOSE: Wire the Propose Protocol to the Proposal Sufficiency Gate and Decision Lifecycle Envelope admission rule.
```

## Why This Session Exists

Session 010 created:

```text
RFC-CDP-024 — Proposal Sufficiency Gate
```

Session 011 defined:

```text
anti_premature_certainty_gate_result
```

in:

```text
RFC-CDP-022 — Protocol Payload Schema Registry
```

Session 012 patched:

```text
RFC-CDP-023 — Decision Lifecycle Envelope
```

to include:

```text
proposal_sufficiency_ref
formation_challenge_refs
apc_gate_result_refs
```

and an admission rule requiring sufficient or excepted proposal sufficiency before an envelope may represent a proposal as admitted.

Now the Propose Protocol must consume those envelope fields.

---

## Failure Mode

The failure mode is **proposal bypass into Challenge**.

Proposal bypass into Challenge occurs when a proposed decision enters the ordinary Challenge lifecycle even though the Decision Lifecycle Envelope does not show that the proposal earned admission through the Proposal Sufficiency Gate.

RFC-CDP-024 defines the gate.

RFC-CDP-023 indexes the gate artifacts.

RFC-CDP-041 enforces that Propose cannot proceed without them.

---

## Turn 001 — 2026-05-24 — G / Andie — Propose Wiring Promotion

```text
DATE: 2026-05-24
AUTHOR: ChatGPT / G, approved by Andie
ROLE: canon promotion / protocol wiring
STATUS: adjudicated-and-promoted
PURPOSE: Patch RFC-CDP-041 so Propose respects Proposal Sufficiency admission.
```

### G Position

Envelope first. Propose second.

Session 012 gave the envelope the references it needs.

Session 013 teaches Propose to consume them.

### Action Taken

Patched:

```text
rfc/RFC-CDP-041-Propose-Protocol.md
```

Advanced to:

```text
Draft v0.4
```

Commit:

```text
c9d785958031f1616b2853a841a83e30df8fd3f2
```

### Changes Promoted

Promoted into RFC-CDP-041 Draft v0.4:

- corrected canonical heading from legacy RFC-CDP-002 to RFC-CDP-041;
- updated dependencies to current RFC numbering;
- failure mode: proposal bypass into Challenge;
- Proposal Sufficiency Gate admission rule;
- proposer standing check requirement;
- formation challenge relationship;
- APC gate relationship;
- persistence relationship to RFC-CDP-025;
- idempotency protection against duplicate or conflicting sufficiency references.

### Core Rule

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

---

## Promotion Decision

```text
PROMOTE TO CANON:
- RFC-CDP-041 Draft v0.4 Proposal Sufficiency wiring

DEFER:
- RFC-CDP-042 Challenge Protocol formation challenge relationship
- RFC-CDP-045 Legitimize Protocol APC wiring
- lifecycle state machine alignment
- risk classification mechanism
```
