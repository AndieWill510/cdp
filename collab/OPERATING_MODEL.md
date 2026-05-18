# CDP Collaboration Operating Model

This document defines how human and AI collaborators should use the `collab/` folder.

The goal is to support many future conversations without turning the repository into a pile of disconnected notes.

## Core Principle

CDP collaboration must keep humans **in the loop**, not **in the pile**.

A human should be able to open one conversation file and quickly answer:

- What conversation is active?
- Who said what?
- What was decided?
- What remains contested?
- What should move into canonical RFCs or schemas?
- What is only working material?

## Preferred Structure

Use **one Markdown file per collaboration session**.

Recommended structure:

```text
collab/
  README.md
  OPERATING_MODEL.md
  INDEX.md
  sessions/
    001-rfc-completeness-coherency-readability.md
    002-topic-slug.md
    003-topic-slug.md
```

Do not create a folder full of separate prompt, response, adjudication, and promotion files unless the moderator explicitly decides a session needs extraction.

Default is one shared chat file.

## Why One File

A single shared file is easier to moderate.

It preserves sequence.

It reduces schema drift.

It lets Andie treat the file like a shared room rather than a document management problem.

The file may contain:

- session frame
- prompts
- model responses
- challenges
- moderator notes
- adjudication
- promotion decision

## Collaboration Loop

Use this rhythm inside the shared file:

```text
1. Frame the session.
2. Invite critique.
3. Preserve dissent.
4. Human adjudicates.
5. Promote accepted material into canon.
6. Record what remains open.
```

## Turn Format

Each new contribution should use a turn heading:

```text
## Turn 002 — Claude / Sonnet — RFC Review

DATE:
AUTHOR:
ROLE:
STATUS:
PURPOSE:

Content here.
```

Suggested status values:

- draft
- under-review
- challenged
- adjudicated
- promoted
- rejected
- superseded

## Canon Boundary

The `collab/` folder is provisional.

Canonical material belongs in:

- RFCs
- schemas
- architecture documents
- implementation files
- formal decision records

Do not let `collab/` become the hidden constitution.

If something matters, promote it.

## Naming Rules

Use numbered session files:

```text
sessions/001-topic-slug.md
sessions/002-topic-slug.md
sessions/003-topic-slug.md
```

Use dates inside files when useful, but keep file ordering numeric.

## Human Moderator Role

Andie moderates.

The moderator should decide:

- what question is being asked;
- what counts as enough evidence;
- what gets promoted;
- what remains dissent;
- what is deferred;
- what is rejected.

The moderator is not required to resolve every disagreement immediately.

Preserved dissent is a feature, not a failure.

## Model Roles

### ChatGPT

Default role: synthesizer, architect, continuity keeper, protocol drafter.

### Claude / Sonnet

Default role: challenger, coherence reviewer, human-readability critic, schema-drift detector.

### Other Models

Other models may contribute when their role is explicit.

Do not add model output without naming the model, date, prompt, and purpose.

## Promotion Rule

Every significant collaboration should end with one of these outcomes:

```text
PROMOTE TO CANON:
PROMOTE WITH CHANGES:
DO NOT PROMOTE:
DEFER:
```

This is how CDP avoids becoming human-in-the-pile governance theater.

## Extraction Rule

If a shared chat file grows too large, extract stable material into a canonical artifact or a dated appendix.

Do not split too early.

Premature foldering is schema drift wearing a little hat.

## Closing Note

The point is not to make every conversation permanent.

The point is to make important reasoning retrievable, contestable, and promotable.
