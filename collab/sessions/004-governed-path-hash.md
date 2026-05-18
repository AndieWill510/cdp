# Session 004 Shared Chat: Governed Path Hash

```text
SESSION: 004-governed-path-hash
DATE_OPENED: 2026-05-17
MODERATOR: Andie
STATUS: active
MODE: shared-chat-file
CANON_TARGET: RFC-CDP-023-Decision-Lifecycle-Envelope.md
PURPOSE: Define how governed_path_hash should be constructed so the Decision Lifecycle Envelope can preserve integrity without embedding every governed artifact.
```

## How to Use This File

This is a shared chat transcript and working record for Session 004.

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

How should `governed_path_hash` be computed for `RFC-CDP-023-Decision-Lifecycle-Envelope.md`?

---

## Background

Session 003 created `RFC-CDP-023-Decision-Lifecycle-Envelope.md` as the governed path index for a complete CDP decision.

RFC-CDP-023 requires `governed_path_hash`, but leaves exact construction undefined.

The open question is whether the hash covers:

- the ordered list of governed reference IDs;
- canonicalized metadata for each referenced record;
- content hashes of referenced records;
- lifecycle-stage order and status values;
- summary pointers and dissent references;
- standing and recusal references;
- repair and appeal references.

---

## Relevant Canonical Files

Read these first:

1. `https://github.com/AndieWill510/cdp/blob/main/skills/CDP_CONTEXT_FOR_CLAUDE.md`
2. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-000-Series-Index.md`
3. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-021-Envelope-Schema.md`
4. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-023-Decision-Lifecycle-Envelope.md`
5. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-033-Standing-and-Recusal-Model.md`
6. `https://github.com/AndieWill510/cdp/blob/main/collab/sessions/004-governed-path-hash.md`

---

## Initial Hash Hypothesis

The governed path hash should probably not hash every full artifact directly.

It should hash a canonicalized **governed path manifest** that includes:

- envelope identity fields;
- lifecycle stage and status;
- ordered governed stage reference IDs;
- each referenced record's declared content hash;
- standing and recusal reference IDs;
- summary governed-by reference;
- material dissent references;
- lineage references;
- supersession links.

This would make the envelope tamper-evident without making the envelope a warehouse.

This is a hypothesis, not final schema.

---

## Core Risk

The hash can fail in two opposite ways:

1. **Too shallow:** hashes only reference IDs, allowing referenced content to mutate without detection.
2. **Too deep:** hashes every byte of every artifact directly, making the envelope brittle, huge, and impossible to update safely.

The design problem is:

> What must be canonicalized and hashed so the governed path is tamper-evident while referenced records remain separately governed?

---

## Issues to Decide

Candidate decisions:

1. Should `governed_path_hash` hash a governed path manifest rather than raw artifacts?
2. What fields belong in the governed path manifest?
3. Should referenced records each expose their own `record_hash`?
4. Should the path hash include lifecycle order?
5. Should the path hash include standing and recusal status?
6. Should the path hash include human summary pointers?
7. What canonicalization rules are required?
8. What is the narrowest RFC-CDP-023 update?

---

## Turn 001 — 2026-05-17 — Andie / ChatGPT — Session Opening

```text
DATE: 2026-05-17
AUTHOR: Andie, recorded by ChatGPT
ROLE: moderator / session opener
STATUS: active
PURPOSE: Record Decision 014 approval and open Session 004 on governed_path_hash.
```

### Decision 014

Approved: Open Session 004 on **Governed Path Hash**.

### Scope

This session is about defining `governed_path_hash` for `RFC-CDP-023-Decision-Lifecycle-Envelope.md`.

This session is not yet a decision to rewrite all lifecycle RFCs or define every governed record schema.

### ChatGPT Position

My position: `governed_path_hash` should hash a canonicalized **governed path manifest**, not raw artifacts directly.

The manifest should include stable references plus the content hashes declared by those referenced records.

That gives CDP tamper evidence without turning the envelope into a warehouse or making every envelope update recursively hash the universe.

### Failure Mode

The failure mode is **integrity theater**.

Integrity theater occurs when a system presents a hash as proof of governance integrity, but the hash only covers a superficial receipt rather than the governed path that matters.

A hash that covers only the envelope shell is not enough.

A hash that requires embedding everything defeats the envelope design.

The governed path hash must prove that the path index and its referenced record hashes have not been silently changed.

---

## Turn 002 — Pending — Claude / Sonnet — Governed Path Hash Challenge Memo

Claude / Sonnet:

Read:

1. `https://github.com/AndieWill510/cdp/blob/main/skills/CDP_CONTEXT_FOR_CLAUDE.md`
2. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-000-Series-Index.md`
3. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-021-Envelope-Schema.md`
4. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-023-Decision-Lifecycle-Envelope.md`
5. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-033-Standing-and-Recusal-Model.md`
6. `https://github.com/AndieWill510/cdp/blob/main/collab/sessions/004-governed-path-hash.md`

Then draft **Turn 002 — Claude / Sonnet — Governed Path Hash Challenge Memo**.

Please answer:

1. What failure mode should governed_path_hash prevent?
2. Is ChatGPT's governed path manifest approach correct, too shallow, or too complex?
3. What exactly should be hashed?
4. What should not be hashed?
5. Should referenced records expose their own hashes?
6. What canonicalization rules are required?
7. How should supersession and updates work?
8. What should be added to RFC-CDP-023?
9. What is the narrowest RFC update you recommend?

Do not flatter.

Do not collapse uncertainty.

Name the failure mode precisely.

Also include a proposed patch section for:

`https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-023-Decision-Lifecycle-Envelope.md`

---

## Promotion Decision

Pending.

```text
PROMOTE TO CANON:
PROMOTE WITH CHANGES:
DO NOT PROMOTE:
DEFER:
```
