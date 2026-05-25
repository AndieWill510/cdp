# Session 014 Shared Chat: RFC-CDP-042 Challenge Protocol Formation Challenge Boundary

```text
SESSION: 014-rfc-042-challenge-formation-challenge-boundary
DATE_OPENED: 2026-05-24
MODERATOR: Andie
STATUS: promotion-applied
MODE: shared-chat-file
CANON_TARGET: RFC-CDP-042-Challenge-Protocol.md
PURPOSE: Patch Challenge Protocol to distinguish ordinary Challenge from Formation Challenge and wire Challenge to Proposal Sufficiency admission artifacts.
```

## Why This Session Exists

Session 010 created:

```text
RFC-CDP-024 — Proposal Sufficiency Gate
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

Session 013 patched:

```text
RFC-CDP-041 — Propose Protocol
```

so Propose cannot bypass Proposal Sufficiency into Challenge.

Now Challenge must define its boundary with Formation Challenge.

---

## Failure Mode

The failure mode is **challenge surface confusion**.

Challenge surface confusion occurs when upstream formation defects and downstream proposal-merit objections are treated as the same kind of challenge.

This causes governance failures:

- admission defects are laundered into deliberation;
- standing rules drift;
- outcome options blur.

---

## Turn 001 — 2026-05-24 — G / Andie — Challenge Boundary Promotion

```text
DATE: 2026-05-24
AUTHOR: ChatGPT / G, approved by Andie
ROLE: canon promotion / protocol boundary definition
STATUS: adjudicated-and-promoted
PURPOSE: Patch RFC-CDP-042 so Challenge respects the Formation Challenge boundary.
```

### G Position

Formation Challenge contests admission.

Ordinary Challenge contests an admitted proposal.

These are different challenge surfaces and must not be collapsed.

### Action Taken

Patched:

```text
rfc/RFC-CDP-042-Challenge-Protocol.md
```

Advanced to:

```text
Draft v0.4
```

Commit:

```text
e4617417050fa256b65a9684cee3a98a8d63024f
```

### Changes Promoted

Promoted into RFC-CDP-042 Draft v0.4:

- corrected canonical heading from legacy RFC-CDP-003 to RFC-CDP-042;
- updated dependencies to current RFC numbering;
- failure mode: challenge surface confusion;
- clear boundary between Formation Challenge and ordinary Challenge;
- non-substitution rule;
- proposal admission preconditions before ordinary Challenge;
- APC Challenge type for post-admission premature-certainty objections;
- formation challenge reference rule;
- updated persistence requirements.

### Core Rule

Formation Challenge is governed by RFC-CDP-024.

Ordinary Challenge is governed by RFC-CDP-042.

Formation Challenge asks:

```text
Has this earned admission as a proposal?
```

Ordinary Challenge asks:

```text
Should this admitted proposal survive adversarial scrutiny?
```

---

## Promotion Decision

```text
PROMOTE TO CANON:
- RFC-CDP-042 Draft v0.4 formation challenge boundary

DEFER:
- detailed standing rules for ordinary challengers
- formal no-challenge attestation schema
- Adjudicate handling of blocking challenges
- record_hash propagation for challenge records
- challenge state machine alignment
```
