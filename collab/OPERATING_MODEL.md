# CDP Collaboration Operating Model

This document defines how human and AI collaborators should use the `collab/` folder.

The goal is to support many future conversations without turning the repository into a pile of disconnected notes.

## Core Principle

CDP collaboration must keep humans **in the loop**, not **in the pile**.

A human should be able to open this folder and quickly answer:

- What conversation is active?
- What was decided?
- What remains contested?
- What should move into canonical RFCs or schemas?
- What is only working material?

## Folder Structure

Recommended structure:

```text
collab/
  README.md
  OPERATING_MODEL.md
  INDEX.md
  sessions/
    001-rfc-completeness-coherency-readability/
      README.md
      prompt-to-claude.md
      chatgpt-opening-memo.md
      claude-response.md
      adjudication.md
      promotion-plan.md
  templates/
    session-readme-template.md
    challenge-memo-template.md
    adjudication-template.md
    promotion-plan-template.md
```

## Artifact Types

### Session README

Defines the purpose, scope, participants, and active question for a collaboration session.

### Prompt to Claude / Sonnet

A direct prompt that can be pasted into Claude or used by Claude when writing into the repo.

### Opening Memo

The initiating model's structured position.

### Response Memo

The responding model's structured critique, extension, or alternative framing.

### Adjudication

The human moderator's decision, synthesis, or instruction.

### Promotion Plan

The path from working material to canonical repo content.

A session is not finished until it has either:

1. a promotion plan; or
2. an explicit decision not to promote the work.

## Collaboration Loop

Use this rhythm:

```text
1. Frame the session.
2. Invite critique.
3. Preserve dissent.
4. Human adjudicates.
5. Promote accepted material into canon.
6. Record what remains open.
```

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

Use numbered sessions:

```text
sessions/001-topic-slug/
sessions/002-topic-slug/
sessions/003-topic-slug/
```

Use dates inside files when useful, but keep folder ordering numeric.

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

## Required Header for Session Files

Each working file should begin with:

```text
SESSION:
DATE:
AUTHOR:
ROLE:
STATUS:
PURPOSE:
```

Suggested status values:

- draft
- under-review
- challenged
- adjudicated
- promoted
- rejected
- superseded

## Promotion Rule

Every significant collaboration should end with one of these outcomes:

```text
PROMOTE TO CANON:
PROMOTE WITH CHANGES:
DO NOT PROMOTE:
DEFER:
```

This is how CDP avoids becoming human-in-the-pile governance theater.

## Closing Note

The point is not to make every conversation permanent.

The point is to make important reasoning retrievable, contestable, and promotable.
