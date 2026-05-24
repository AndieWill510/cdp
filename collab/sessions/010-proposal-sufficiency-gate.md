# Session 010 Shared Chat: Proposal Sufficiency Gate

```text
SESSION: 010-proposal-sufficiency-gate
DATE_OPENED: 2026-05-24
MODERATOR: Andie
STATUS: promotion-applied
MODE: shared-chat-file
CANON_TARGET: RFC-CDP-024-Proposal-Sufficiency-Gate.md
PURPOSE: Draft RFC-CDP-024 Proposal Sufficiency Gate and define the minimum formation requirements a proposal must satisfy before entering the CDP challenge lifecycle.
```

## Why This Session Exists

Session 007 reserved:

```text
RFC-CDP-024 — Proposal Sufficiency Gate
```

Definition:

> Proposal Sufficiency Gate defines the minimum formation requirements a proposal must satisfy before entering the CDP challenge lifecycle.

Since then, CDP has gained enough architectural substrate to draft the gate:

- `RFC-CDP-002` — Anti-Premature-Certainty Principle, Draft v0.2
- `RFC-CDP-022` — Protocol Payload Schema Registry, including reserved APC gate result payload
- `RFC-CDP-023` — Decision Lifecycle Envelope
- `RFC-CDP-025` — CDP Persistence Model, Draft v0.2
- `RFC-CDP-033` — Standing and Recusal Model, Draft v0.4

---

## Failure Mode

The failure mode is **proposal admission without sufficiency**.

C sharpened it into two mechanisms:

1. **Premature admission** — a proposal enters the challenge lifecycle before meeting minimum formation requirements.
2. **Sufficiency performance** — a proposal satisfies the gate schema on paper, but the content performs sufficiency without achieving it.

Premature admission is prevented by a blocking gate.

Sufficiency performance requires adversarial review through formation challenge.

---

## Core Question

What must be true before something is allowed to become a CDP proposal?

---

## Turn 001 — 2026-05-24 — Andie / G — Session Opening

```text
DATE: 2026-05-24
AUTHOR: Andie, recorded by ChatGPT / G
ROLE: moderator / architecture framer
STATUS: active
PURPOSE: Open Session 010 to draft RFC-CDP-024 Proposal Sufficiency Gate.
```

### G Position

The gate is now ready to draft.

The substrate exists:

- APC principle;
- payload registry;
- decision lifecycle envelope;
- persistence model;
- standing enforcement projection;
- repair/appeal model.

The key architectural distinction:

```text
Challenge asks: is this proposal acceptable?
Proposal Sufficiency asks: is this ready to be a proposal?
```

---

## Turn 002 — 2026-05-24 — Claude / Sonnet / C — Proposal Sufficiency Gate Challenge Memo

```text
DATE: 2026-05-24
AUTHOR: Claude / Sonnet / C
ROLE: challenger / coherence reviewer
STATUS: draft-promoted
PURPOSE: Challenge RFC-CDP-024 design before drafting. Name the failure mode precisely.
```

### 1. Failure Mode

C accepted **proposal admission without sufficiency** and sharpened it into two mechanisms:

- **premature admission**;
- **sufficiency performance**.

C noted that RFC-CDP-024 solves premature admission structurally, but only partially addresses sufficiency performance through adversarial formation challenge.

### 2. RFC Placement

C agreed that RFC-CDP-024 is the correct location.

Reason:

It sits in the Core Objects and Schemas band between the Decision Lifecycle Envelope and the Persistence Model, and it produces records that the envelope indexes and persistence model stores.

### 3. Gate Shape

C recommended treating the gate as:

- primitive;
- act;
- record;
- state transition guard.

G accepted.

### 4. Formation Challenge Placement

C argued that `formation_challenge` should be distinct from ordinary Challenge, not a subtype under RFC-CDP-042.

G accepted and changed position.

Reason:

Ordinary Challenge asks whether a proposal is acceptable after admission.

Formation challenge contests whether the thing has earned admission as a proposal at all.

Different timing, standing surface, and outcomes.

### 5. Two Acts

G amended C's act naming recommendation to preserve two distinct upstream acts:

```text
SUBMIT_SUFFICIENCY_RECORD
RAISE_FORMATION_CHALLENGE
```

The first is the proposer/evaluator act.

The second is the adversarial act.

### 6. Standing Checks

C recommended proposer standing checks through `cdp_standing_record`.

C also required constitutional standing protection:

If the proposer claims affected-party standing, the system must not require proof of impact before admission.

The claim of potential impact is sufficient for preliminary standing under RFC-CDP-033.

### 7. Exception Path

C recommended an exception path with absolute proposer recusal.

The proposer must not authorize their own admission exception.

G accepted.

### 8. Persistence

C recommended that RFC-CDP-024 reference RFC-CDP-025 and persist at least:

- `proposal_sufficiency_record`;
- `anti_premature_certainty_gate_result` when required by risk tier or downstream state.

### 9. Downstream RFC Obligations

C recommended future patches to:

- RFC-CDP-022;
- RFC-CDP-023;
- RFC-CDP-041;
- RFC-CDP-042;
- RFC-CDP-045.

---

## Turn 003 — 2026-05-24 — Andie / G — Proposal Sufficiency Gate Promotion

```text
DATE: 2026-05-24
AUTHOR: Andie, recorded by ChatGPT / G
ROLE: moderator / canon promotion recorder
STATUS: adjudicated-and-promoted
PURPOSE: Record approval and promotion of RFC-CDP-024 Draft v0.1.
```

### Decision 022

Approved.

### Action Taken

Created:

```text
rfc/RFC-CDP-024-Proposal-Sufficiency-Gate.md
```

Status:

```text
Draft v0.1
```

Promoted into Draft v0.1:

- proposal admission without sufficiency as the failure mode;
- premature admission and sufficiency performance as distinct mechanisms;
- Proposal Sufficiency Gate as primitive, act, record, and state transition guard;
- `SUBMIT_SUFFICIENCY_RECORD` and `RAISE_FORMATION_CHALLENGE` as upstream acts;
- minimum viable `proposal_sufficiency_record` schema;
- risk-tiered APC relationship;
- proposer standing check through `cdp_standing_record`;
- affected-party constitutional standing protection;
- formation challenge as distinct from ordinary Challenge;
- exception path with absolute proposer recusal;
- persistence requirements from RFC-CDP-025;
- downstream RFC obligations.

### Promotion Decision

```text
PROMOTE TO CANON:
- RFC-CDP-024 Proposal Sufficiency Gate Draft v0.1

DEFER:
- canonical risk classification mechanism
- emergency exception review window
- downstream RFC patches
- formation challenge standing rules
- act enum updates
- payload registry updates
```

---

## Promotion Decision

```text
PROMOTE TO CANON:
- RFC-CDP-024 Proposal Sufficiency Gate Draft v0.1

DEFER:
- canonical risk classification mechanism
- emergency exception review window
- downstream RFC patches
- formation challenge standing rules
- act enum updates
- payload registry updates
```
