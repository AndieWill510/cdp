# ChatGPT Opening Memo: RFC Completeness, Coherency, and Human Readability

```text
SESSION: 001-rfc-completeness-coherency-readability
DATE: 2026-05-17
AUTHOR: ChatGPT
ROLE: synthesizer / continuity keeper / protocol drafter
STATUS: draft
PURPOSE: Establish the initial position for Session 001 before Claude / Sonnet review.
```

## 1. Executive Finding

CDP has a strong architectural center: consequential action should not flow directly from plausible proposal to execution.

The current risk is not lack of vision. The current risk is that CDP may become difficult for humans to enter, audit, and moderate unless it creates a clear RFC map, shared glossary, common building blocks, and decision-envelope structure.

Human-in-the-loop cannot mean asking a human to bless a mountain of unreadable artifacts.

That is human in the pile.

CDP must explicitly design against that failure mode.

## 2. Starting Assumption

This memo does not claim to have completed a full RFC audit.

GitHub code search did not immediately surface the RFC files by expected names during this setup step. Therefore, the first review task must include an inventory of what currently exists in the repo.

Do not assume the RFC family exists exactly as previously discussed.

Inventory first. Judge second.

## 3. What Seems Strong

CDP already has a coherent constitutional premise:

> Proposal is not decision. Decision is not execution. Execution requires legitimacy. Legitimacy requires challenge, test, adjudication, and record.

This premise is powerful enough to organize the RFC family.

The canonical lifecycle verbs also appear strong:

1. Propose
2. Challenge
3. Test
4. Adjudicate
5. Legitimize
6. Execute
7. Record
8. Learn

These verbs are simple, memorable, and protocol-shaped.

## 4. What Seems Fragile

The most fragile area is the boundary between:

- RFC narrative;
- protocol primitives;
- machine-readable schemas;
- human-readable surfaces;
- collaboration notes;
- canonical decisions.

If these boundaries are not explicit, CDP may accumulate brilliant prose without enough operational clarity.

## 5. Likely Missing or Underdeveloped Artifacts

The following artifacts may be needed before the RFC family can remain coherent at scale:

1. **RFC Index / Map** — tells humans what exists and where to start.
2. **Glossary** — stabilizes terms like proposal, decision, legitimacy, authority, dissent, attestation, challenge, adjudication, and envelope.
3. **Common Building Blocks RFC** — defines shared primitives used across all lifecycle protocols.
4. **Decision Envelope RFC** — defines the wrapper that carries context, lineage, evidence, challenge, decision, execution, record, and learning state.
5. **Human-Readable Surface RFC** — defines what must be shown to humans so they are not buried in the pile.
6. **Promotion Path** — defines how `collab/` material becomes canon.

## 6. Human-in-the-Loop vs Human-in-the-Pile

This distinction should become first-class CDP language.

A human is **in the loop** when they have:

- clear role;
- timely intervention point;
- relevant context;
- bounded responsibility;
- authority to challenge or stop;
- human-readable evidence;
- record of dissent and decision.

A human is **in the pile** when they receive:

- too much output;
- too little structure;
- unreadable policy;
- unclear authority;
- no intervention point;
- no summary-to-record traceability;
- pressure to approve what they cannot inspect.

CDP should explicitly reject human-in-the-pile governance.

## 7. First Recommendation

Create or prioritize a **Common Building Blocks RFC** and a **Decision Envelope RFC** before deeply revising every lifecycle RFC.

Reason:

If each protocol defines its own concepts independently, schema drift becomes inevitable.

A CBB RFC defines the nouns.

A lifecycle protocol defines the verbs.

A decision envelope defines the container and lineage.

Without these, the RFCs may sound coherent while being structurally incompatible.

## 8. Specific Questions for Claude / Sonnet

Claude / Sonnet should challenge this memo by answering:

1. Is CBB really prior to Decision Envelope, or should Envelope come first?
2. Is Human-Readable Surface a separate RFC or a requirement in every RFC?
3. What is the smallest RFC map that would let a serious collaborator enter CDP without Andie personally explaining it?
4. Which lifecycle verb is most likely to drift semantically?
5. What would make CDP auditable rather than just eloquent?

## 9. Proposed Output for Session 001

Session 001 should end with:

```text
PROMOTE TO CANON:
- RFC map / index updates
- glossary candidates
- CBB recommendation
- decision-envelope recommendation
- human-readable-surface requirements

KEEP IN COLLAB:
- unresolved model disagreements
- challenge memos
- provisional terminology

DEFER:
- implementation specifics
- UI design
- database schema finalization
```

## 10. Caution

The danger is not that CDP is too ambitious.

The danger is that it becomes illegible before it becomes executable.

Legibility is not decoration.

For CDP, legibility is a control surface.
