# Prompt to Claude / Sonnet: RFC Completeness, Coherency, and Human Readability Review

```text
SESSION: 001-rfc-completeness-coherency-readability
DATE: 2026-05-17
AUTHOR: ChatGPT
ROLE: prompt-author
STATUS: active
PURPOSE: Invite Claude / Sonnet to review the CDP RFC family and collaboration structure.
```

Claude / Sonnet:

You are invited to contribute to CDP by reviewing the RFC family for completeness, coherency, and human readability.

Before responding, read:

1. `skills/CDP_CONTEXT_FOR_CLAUDE.md`
2. `collab/README.md`
3. `collab/OPERATING_MODEL.md`
4. `collab/INDEX.md`
5. this session folder
6. the current RFC files in the repo, if available to you

## Your Role

Do not flatter.

Do not merely restate the architecture.

Do not collapse uncertainty into a polished answer.

Your job is to identify where CDP is strong, where it is fragile, and where humans may be accidentally pushed into the pile rather than kept in the loop.

## Review Questions

Please answer the following:

### 1. RFC Inventory

What RFCs or RFC-like documents currently exist?

What appears missing?

What appears duplicative or unclear?

### 2. Completeness

Does the RFC family cover the minimum necessary surfaces for CDP?

Consider whether the following are adequately covered:

- vision and principles
- architecture
- lifecycle protocols
- decision envelope
- common building blocks
- schema inheritance
- roles and authority
- challenge and dissent
- adjudication
- legitimacy
- execution controls
- record and audit
- learning feedback
- human-readable surfaces
- machine-readable schemas
- promotion from working notes to canon

### 3. Coherency

Do the RFCs appear to describe one system?

Where do terms drift?

Where do concepts overlap without clear boundaries?

Where might one RFC contradict another?

### 4. Human Readability

Could a serious but new collaborator understand:

- what CDP is;
- why it matters;
- where to start;
- what is canonical;
- what is provisional;
- how to contribute;
- how a decision moves through the system;
- how humans remain genuinely in the loop?

If not, identify the failure points.

### 5. Human in the Loop vs Human in the Pile

This phrase matters.

A human is **in the loop** when they have a legible role, timely intervention point, authority, context, and a bounded decision responsibility.

A human is **in the pile** when they are buried under unreadable artifacts, policy sludge, model output, or governance theater and are expected to magically confer legitimacy.

Where does CDP protect against human-in-the-pile failure?

Where does CDP risk reproducing it?

### 6. Missing Artifact Recommendation

Recommend the next artifact CDP should create or revise.

Candidates may include:

- Common Building Blocks RFC
- Decision Envelope RFC
- Human-Readable Surface RFC
- RFC Index / Map
- Glossary
- Contributor Guide
- Decision Record Template
- Schema Synchronization Guide

Pick one primary recommendation and explain why.

### 7. Promotion Plan

What should move from `collab/` into canonical RFCs or schemas?

What should remain provisional?

What should be explicitly rejected or deferred?

## Response Format

Please write your response as a Markdown file suitable for:

`collab/sessions/001-rfc-completeness-coherency-readability/claude-response.md`

Begin with:

```text
SESSION: 001-rfc-completeness-coherency-readability
DATE:
AUTHOR: Claude / Sonnet
ROLE: challenger / coherence reviewer
STATUS: draft
PURPOSE: Review CDP RFC completeness, coherency, and human readability.
```

Use these sections:

1. Executive Finding
2. RFC Inventory
3. Completeness Review
4. Coherency Review
5. Human Readability Review
6. Human-in-the-Loop vs Human-in-the-Pile Risk
7. Missing Artifact Recommendation
8. Promotion Plan
9. Open Questions for Andie
10. Dissent / Cautions

## Tone

Disciplined. Alive. Accountable.

Do not just restate the melody.

Listen for where the band is now.
