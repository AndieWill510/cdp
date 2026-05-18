# Session 003 Shared Chat: Decision Envelope

```text
SESSION: 003-decision-envelope
DATE_OPENED: 2026-05-17
MODERATOR: Andie
STATUS: active
MODE: shared-chat-file
CANON_TARGET: RFC-CDP-021-Envelope-Schema.md
PURPOSE: Define or refine the Decision Envelope as the container that carries decision context, standing, evidence, challenge, adjudication, legitimacy, execution constraints, record, and learning.
```

## How to Use This File

This is a shared chat transcript and working record for Session 003.

All participants should write directly into this single file using dated turns.

The working pattern is:

```text
Turn -> Response -> Challenge -> Moderator Adjudication -> RFC Update -> Series Index Update if needed
```

Approved decisions are RFC-first by default.

Do not leave approved architecture only in `collab/` unless Andie explicitly marks it discussion-only.

---

## Participants

- **Andie** — moderator, originator, human adjudicator
- **ChatGPT** — synthesizer, continuity keeper, protocol drafter
- **Claude / Sonnet** — challenger, coherence reviewer, human-readability critic, schema-drift detector
- **Other collaborators** — invited as named contributors

---

## Session Question

What must the CDP Decision Envelope contain so a consequential decision remains legible, legitimate, auditable, contestable, executable only under authority, recordable, repairable, and learnable?

---

## Background

Session 001 identified the Decision Envelope as a likely load-bearing structure.

Session 002 created and refined `RFC-CDP-033-Standing-and-Recusal-Model.md`, grounding Standing and Recusal as first-class concepts.

The Decision Envelope now needs to carry or reference Standing and Recusal information without becoming an unreadable junk drawer.

The envelope should prevent schema drift between:

- human-readable explanation;
- machine-readable schema;
- challenge record;
- standing record;
- evidence record;
- adjudication record;
- legitimacy basis;
- execution constraints;
- repair / appeal / learning record.

---

## Relevant Canonical Files

Read these first:

1. `https://github.com/AndieWill510/cdp/blob/main/skills/CDP_CONTEXT_FOR_CLAUDE.md`
2. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-000-Series-Index.md`
3. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-001-Vision-Scope-Principles.md`
4. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-021-Envelope-Schema.md`
5. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-033-Standing-and-Recusal-Model.md`
6. `https://github.com/AndieWill510/cdp/blob/main/collab/sessions/003-decision-envelope.md`

---

## Initial Envelope Hypothesis

A Decision Envelope should carry or reference at least:

- envelope identity;
- decision identity;
- lifecycle stage;
- proposer;
- framing / Nemawashi context;
- standing records;
- recusal records;
- affected-party standing claims;
- evidence;
- assumptions;
- challenges;
- tests;
- adjudication;
- legitimacy basis;
- dissent;
- execution constraints;
- record links;
- repair / appeal hooks;
- learning feedback;
- human-readable summary;
- machine-readable payload;
- schema version;
- lineage and provenance.

This is a hypothesis, not final schema.

---

## Core Risk

The Decision Envelope can fail in two opposite ways:

1. **Too thin:** it does not carry enough context to make the decision auditable or contestable.
2. **Too fat:** it becomes a pile of every artifact ever produced, making humans unable to inspect it.

The design problem is not “put everything in the envelope.”

The design problem is:

> What must travel with the decision, what may be linked by reference, and what must remain externally governed?

---

## Issues to Decide

This session should produce one narrow decision at a time.

Candidate decisions:

1. Should RFC-CDP-021 be treated as the canonical Decision Envelope RFC?
2. Should the envelope include full payloads or references to governed records?
3. Should Standing and Recusal be embedded in the envelope or referenced by ID?
4. Should the envelope include a required human-readable summary?
5. Should the envelope define normative schema blocks directly?
6. Should the envelope define required lineage and versioning fields?
7. What is the minimum viable envelope schema?
8. What is the narrowest RFC update to make next?

---

## Turn 001 — 2026-05-17 — Andie / ChatGPT — Session Opening

```text
DATE: 2026-05-17
AUTHOR: Andie, recorded by ChatGPT
ROLE: moderator / session opener
STATUS: active
PURPOSE: Record Decision 010 approval and open Session 003 on the Decision Envelope.
```

### Decision 010

Approved: Open Session 003 on **Decision Envelope**.

### Scope

This session is about `RFC-CDP-021-Envelope-Schema.md` and the Decision Envelope as a load-bearing CDP object.

This session is not yet a decision to rewrite every lifecycle protocol.

### Working Hypothesis

The Decision Envelope is the container and lineage surface that allows CDP to keep proposal, standing, challenge, evidence, adjudication, legitimacy, execution, record, repair, and learning connected without collapsing them into an unreadable pile.

### Caution

Do not make the envelope a junk drawer.

The envelope should carry required identity, state, lineage, and references. It should embed payloads only when necessary for integrity, portability, or audit.

### Prompt to Claude / Sonnet

Claude / Sonnet:

Read:

1. `https://github.com/AndieWill510/cdp/blob/main/skills/CDP_CONTEXT_FOR_CLAUDE.md`
2. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-000-Series-Index.md`
3. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-001-Vision-Scope-Principles.md`
4. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-021-Envelope-Schema.md`
5. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-033-Standing-and-Recusal-Model.md`
6. `https://github.com/AndieWill510/cdp/blob/main/collab/sessions/003-decision-envelope.md`

Then draft **Turn 002 — Claude / Sonnet — Decision Envelope Challenge Memo**.

Please answer:

1. What failure mode should the Decision Envelope prevent?
2. What is the minimum viable envelope?
3. What belongs inside the envelope versus linked by reference?
4. How should Standing and Recusal connect to the envelope?
5. What human-readable surface is required?
6. What machine-readable schema fields are required?
7. What should RFC-CDP-021 say that it probably does not yet say?
8. What is the narrowest RFC update you recommend?

Do not flatter.

Do not collapse uncertainty.

Name the governance failure mode precisely.

---

## Promotion Decision

Pending.

```text
PROMOTE TO CANON:
PROMOTE WITH CHANGES:
DO NOT PROMOTE:
DEFER:
```
