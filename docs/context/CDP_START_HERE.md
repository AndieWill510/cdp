# CDP_START_HERE — Single-File Context Bundle

Status: Draft v0.1  
Date: 2026-05-27  
Purpose: One-file orientation bundle for CDP collaborators when multi-file fetching is unreliable.

## 1. Why This File Exists

Some collaborators and model fetch tools intermittently fail to read individual repository files even when those files exist.

This file provides a single durable entry point so a collaborator can begin work without depending on a chain of many successful fetches.

Failure mode:

> Context fetch fragility — when important context exists in the repository but a collaborator cannot reliably access every referenced file, creating false 404s, stale state, or context-plane drift.

If another context file 404s, read this file first.

---

## 2. What CDP Is

CDP is the Constitutional Decision Plane.

It is a constitutional control plane for consequential decisions in human-AI systems.

It is not governance theater, a checklist, a vibes document, or a generic agent orchestration pattern.

It is a protocol architecture for forcing consequential proposals to earn authority through governed formation, challenge, test, adjudication, legitimacy, execution, record, repair, and learning.

Short form:

> CDP is anti-fatalism in protocol form.

---

## 3. Core Lifecycle

Canonical lifecycle verbs:

```text
Nemawashi / Framing
Propose
Challenge
Test
Adjudicate
Legitimize
Execute
Record
Learn
Repair / Appeal when triggered
```

Important distinctions:

- Proposal is not Decision.
- Decision is not Execution.
- Sufficiency is not Legitimacy.
- Legitimacy is not Correctness.
- Hierarchy is not Legitimacy.

---

## 4. Load-Bearing Axioms

```text
Plausibility is not legitimacy.

Integrity is necessary but not sufficient for sufficiency.

Sufficiency is necessary but not sufficient for legitimacy.

Legitimacy is necessary but not sufficient for correctness.

Hierarchy is neither necessary nor sufficient for legitimacy.
```

These are not slogans. They are architectural constraints.

---

## 5. Living Covenant

This CDP collaboration has three active participants: Andie, G, and C.

The repository is the shared project record.

Chat is temporary working context.

No participant should have to carry all continuity alone.

Shared rules:

- preserve context;
- name uncertainty;
- keep changes small;
- protect CDP vocabulary;
- repair drift when found.

---

## 6. Council Role Model

CDP collaboration operates as a council, not a hierarchy.

Current role tendencies:

- Andie convenes, stewards, witnesses, and adjudicates when not recused.
- G synthesizes, drafts, patches, promotes canon, and tracks corpus state.
- C challenges, detects coherence gaps, and sharpens failure modes.

These are rotating council functions, not permanent hierarchy.

A participant may originate in one moment, challenge in another, review coherence in another, and promote only after adjudication.

Council does not mean consensus.

Consensus may be evidence of alignment, but it is neither necessary nor sufficient for canon promotion.

A dissent may be overruled, but it must not be erased.

---

## 7. Canon and Collaboration Rules

Conversation is not canon.

Eloquence is not canon.

Consensus is not canon.

Hierarchy is not canon.

Canon is promoted, recorded, verified, and repairable.

Standard promotion path:

```text
conversation
  -> challenge memo
  -> moderator / council adjudication
  -> decision record
  -> RFC / schema / index patch
  -> verification
  -> session closure
```

Nothing in `collab/` is canonical merely because it exists.

A collaboration artifact becomes canonical only when it is promoted into the relevant RFC, schema, index, or durable artifact and verified.

---

## 8. Current Context State

As of 2026-05-27:

- Sessions 001–015 are closed-promoted.
- No active session is recorded in `collab/INDEX.md`.
- Recent promoted work includes:
  - RFC-CDP-022 Draft v0.5 — APC gate result payload defined.
  - RFC-CDP-023 Draft v0.5 — proposal admission references added to Decision Lifecycle Envelope.
  - RFC-CDP-024 Draft v0.1 — Proposal Sufficiency Gate created.
  - RFC-CDP-025 Draft v0.2 — Persistence Model with standing enforcement projection.
  - RFC-CDP-033 Draft v0.4 — Standing persistence reference added.
  - RFC-CDP-041 Draft v0.4 — Propose wired to Proposal Sufficiency.
  - RFC-CDP-042 Draft v0.4 — Formation Challenge distinguished from ordinary Challenge.
  - RFC-CDP-045 Draft v0.5 — Legitimize wired to APC and necessary-not-sufficient axioms, including hierarchy.
  - RFC-CDP-070 Draft v0.1 — Appeals and Contestability Model created.

Current likely queue:

1. Record Hash Propagation to governed record RFCs in the `040–048` band.
2. Reference implementation / DDL profile for RFC-CDP-025.
3. Series Index repair if RFC-CDP-000 is stale relative to recent sessions.
4. Decide whether `proposal_sufficiency_record` and `formation_challenge_record` become RFC-CDP-022 payload types.
5. Continue lifecycle protocol updates only when upstream objects are stable.

---

## 9. Required Orientation Files

When fetches are reliable, read these in order:

1. `docs/context/README.md`
2. `docs/context/LIVING_COVENANT.md`
3. `docs/context/SESSION_HANDOFF.md`
4. `docs/context/AI_MEMORY_BRIEF.md`
5. `collab/COUNCIL_ROLES.md`
6. `collab/PROMOTION_PROTOCOL.md`
7. `collab/INDEX.md`
8. `rfc/RFC-CDP-000-Series-Index.md`

If any of these fail, continue from this file and name the missing file as context-plane debt.

`docs/context/C_ORIENTATION.md` is a deprecated compatibility redirect, not the primary source.

Do not rely on `skills/CDP_CONTEXT_FOR_CLAUDE.md` or older primer text for current state unless refreshed and verified.

---

## 10. Before Drafting Canon

Before drafting canon:

- state what files you read;
- state what files you could not access;
- distinguish repo state from chat memory;
- name the failure mode precisely;
- preserve dissent and uncertainty;
- challenge schema drift;
- recommend the narrowest canonical next move.

If a claim is not yet canon, preserve it as draft.

If a process hides power, challenge it.

If uncertain, say so.

---

## 11. Common Failure Modes to Watch

- Schema drift between prose and machine-readable artifacts.
- Context seam failure between sessions or models.
- Context fetch fragility.
- Legitimacy theater.
- Hierarchy masquerading as meritocracy.
- Council role ambiguity.
- Proposal admission without sufficiency.
- Challenge surface confusion.
- Closure without repair resolution.
- Standing as unenforceable record.
- Downstream schema drift from reserved payloads.
- Governed path severance.

---

## 12. Current Safe Starting Question

After reading this file, ask:

```text
What is the live edge for this session: record-hash propagation, implementation DDL, series-index repair, or another named repair?
```

Do not assume the next move from stale context.
