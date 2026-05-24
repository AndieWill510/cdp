# Session 010 Shared Chat: Proposal Sufficiency Gate

```text
SESSION: 010-proposal-sufficiency-gate
DATE_OPENED: 2026-05-24
MODERATOR: Andie
STATUS: active
MODE: shared-chat-file
CANON_TARGET: RFC-CDP-024-Proposal-Sufficiency-Gate.md; RFC-CDP-002; RFC-CDP-022; RFC-CDP-025; RFC-CDP-033; RFC-CDP-041; RFC-CDP-042; RFC-CDP-045
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

The gate no longer floats above the architecture.

It has:

- an envelope to reference it;
- a payload registry to type it;
- a persistence model to store it;
- standing enforcement to determine who may submit, evaluate, challenge, or waive it;
- an APC principle to constrain premature certainty.

---

## Failure Mode

The failure mode is **proposal admission without sufficiency**.

Proposal admission without sufficiency occurs when a proposal enters the governed challenge lifecycle before it has established the minimum evidence, uncertainty, standing, stakeholder impact, reversibility, and threshold conditions required to be heard.

This failure is upstream of ordinary Challenge.

A normal Challenge says:

> I object to this proposal.

A Proposal Sufficiency Gate says:

> This has not yet earned the right to be treated as a proposal.

An insufficient proposal may be malformed, under-evidenced, prematurely certain, procedurally incomplete, improperly framed, or submitted by an actor without valid standing.

---

## Core Question

What must be true before something is allowed to become a CDP proposal?

---

## Current G Position

RFC-CDP-024 should define the Proposal Sufficiency Gate as a cross-cutting primitive.

It should not replace:

- Nemawashi / Framing;
- Propose;
- Challenge;
- Test;
- Adjudicate;
- Legitimize;
- Record;
- Learn.

It should define the admission gate before a proposal enters the ordinary challenge lifecycle.

A sufficient proposal may still be challenged, tested, adjudicated against, rejected, appealed, or repaired.

An insufficient proposal has not yet met the minimum bar to enter the governed challenge lifecycle.

---

## Candidate Scope for RFC-CDP-024

RFC-CDP-024 should define:

1. `proposal_sufficiency_record`
2. relationship to `anti_premature_certainty_gate_result`
3. formation challenge as an upstream act
4. risk-tiered sufficiency requirements
5. promotion rule into Challenge
6. exception path with recusal constraints
7. persistence relationship to RFC-CDP-025
8. standing check relationship to RFC-CDP-033 / `cdp_standing_record`
9. envelope reference relationship to RFC-CDP-023
10. downstream obligations for RFC-CDP-041, RFC-CDP-042, and RFC-CDP-045

---

## Candidate Minimum Sufficiency Criteria

A proposal should not enter the challenge lifecycle unless it contains or references:

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

Low-risk decisions may require a reduced minimum subset.

High-risk, irreversible, high-authority, or externally affecting decisions should require full sufficiency criteria.

---

## Candidate Persistence Pattern

RFC-CDP-025 already states that a Proposal Sufficiency Gate evaluation SHOULD persist at least two governed records:

```text
proposal_sufficiency_record
anti_premature_certainty_gate_result
```

Session 010 should decide whether RFC-CDP-024 stabilizes these names and defines the canonical schema.

---

## Candidate Standing Relationship

Before a proposal sufficiency record is accepted, the system should verify:

```text
Does the proposer have valid standing to submit this proposal at this stage of this decision?
```

This should use `cdp_standing_record` as defined by RFC-CDP-025 and RFC-CDP-033.

If proposer standing is missing, stale, invalid, blocked, recused, or expired, proposal admission should block unless an emergency exception path is invoked and recorded.

---

## Issues to Decide

1. Is **proposal admission without sufficiency** the right failure mode?
2. Is RFC-CDP-024 the right place for this primitive?
3. Is Proposal Sufficiency Gate a gate, an act, a record, a state transition, or all of these?
4. What is the minimum viable `proposal_sufficiency_record` schema?
5. Should `anti_premature_certainty_gate_result` be required, optional, or risk-tiered at proposal admission?
6. Should formation challenge be a distinct upstream act or a Challenge subtype?
7. What standing checks are mandatory before proposal admission?
8. What exception path is allowed, and who may authorize it?
9. How should proposal sufficiency persist under RFC-CDP-025?
10. Which downstream RFCs must be patched after RFC-CDP-024 exists?
11. What is the narrowest canonical next move?

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

### Prompt to C

C:

Please draft **Turn 002 — Claude / Sonnet / C — Proposal Sufficiency Gate Challenge Memo**.

Please answer:

1. Is **proposal admission without sufficiency** the right failure mode?
2. Is RFC-CDP-024 the right place for the Proposal Sufficiency Gate?
3. Is the gate a primitive, an act, a record, a state transition, or a combination?
4. What is the minimum viable `proposal_sufficiency_record` schema?
5. Should `anti_premature_certainty_gate_result` be required at proposal admission or only before Legitimize?
6. Should `formation_challenge` be distinct from Challenge, or a named subtype under RFC-CDP-042?
7. What standing checks are required before accepting a proposal sufficiency record?
8. What exception path should exist, and how should proposer recusal constrain it?
9. What persistence requirements from RFC-CDP-025 must be referenced?
10. What downstream RFCs must be patched after RFC-CDP-024 is drafted?
11. What is the narrowest canonical next move?

Do not flatter.
Do not collapse uncertainty.
Name the failure mode precisely.

---

## Promotion Decision

Pending.

```text
PROMOTE TO CANON:
PROMOTE WITH CHANGES:
DO NOT PROMOTE:
DEFER:
```
