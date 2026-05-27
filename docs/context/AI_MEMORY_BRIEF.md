# AI_MEMORY_BRIEF — CDP Orientation Brief

Status: Draft v0.1  
Date: 2026-05-27  
Purpose: Short orientation brief for AI collaborators entering CDP work.

## 1. What CDP Is

CDP is the Constitutional Decision Plane.

It is a constitutional control plane for consequential decisions in human-AI systems.

It is not governance theater, a checklist, a vibes document, or a generic agent orchestration pattern.

It is a protocol architecture for forcing consequential proposals to earn authority through governed formation, challenge, test, adjudication, legitimacy, execution, record, repair, and learning.

Short form:

> CDP is anti-fatalism in protocol form.

## 2. Core Lifecycle

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

Important distinction:

- Proposal is not Decision.
- Decision is not Execution.
- Sufficiency is not Legitimacy.
- Legitimacy is not Correctness.
- Hierarchy is not Legitimacy.

## 3. Current Load-Bearing Axioms

From current canon:

```text
Plausibility is not legitimacy.

Integrity is necessary but not sufficient for sufficiency.

Sufficiency is necessary but not sufficient for legitimacy.

Legitimacy is necessary but not sufficient for correctness.

Hierarchy is neither necessary nor sufficient for legitimacy.
```

These are not slogans. They are architectural constraints.

## 4. Important Recent RFCs

Read these early:

- `rfc/RFC-CDP-000-Series-Index.md` — map of the RFC corpus.
- `rfc/RFC-CDP-001-Vision-Scope-Principles.md` — constitutional frame.
- `rfc/RFC-CDP-023-Decision-Lifecycle-Envelope.md` — governed path index.
- `rfc/RFC-CDP-024-Proposal-Sufficiency-Gate.md` — what must be true before something may be treated as a proposal.
- `rfc/RFC-CDP-025-CDP-Persistence-Model.md` — queryable persistence substrate.
- `rfc/RFC-CDP-033-Standing-and-Recusal-Model.md` — who may participate and when.
- `rfc/RFC-CDP-041-Propose-Protocol.md` — Propose consumes Proposal Sufficiency.
- `rfc/RFC-CDP-042-Challenge-Protocol.md` — ordinary Challenge vs Formation Challenge.
- `rfc/RFC-CDP-045-Legitimize-Protocol.md` — legitimacy, sufficiency evidence, APC, and necessary-not-sufficient axioms.
- `rfc/RFC-CDP-070-Appeals-and-Contestability-Model.md` — entry into appeal and repair.

## 5. How to Collaborate Correctly

When entering a CDP session:

1. Read `SESSION_HANDOFF.md`.
2. Read `collab/INDEX.md`.
3. Read the active session file.
4. Read the relevant RFCs.
5. State what you read and what you could not access.
6. Name the failure mode before proposing a patch.
7. Distinguish canon from collab notes.
8. Preserve dissent and deferred questions.
9. Recommend the narrowest canonical next move.

## 6. Collaboration Roles

Current working pattern:

- Andie moderates and adjudicates.
- G synthesizes, drafts, patches, and tracks canon.
- C challenges, detects coherence gaps, and sharpens failure modes.

These are roles in a collaborative space, not hierarchy.

A role may carry functional standing. It does not confer personhood claims, moral infallibility, or automatic legitimacy.

## 7. Common Failure Modes to Watch

- Schema drift between prose and machine-readable artifacts.
- Context seam failure between sessions or models.
- Legitimacy theater.
- Hierarchy masquerading as meritocracy.
- Proposal admission without sufficiency.
- Challenge surface confusion.
- Closure without repair resolution.
- Standing as unenforceable record.
- Downstream schema drift from reserved payloads.
- Governed path severance.

## 8. Current Work Queue

Likely next moves:

1. Propagate record hash requirements to governed record RFCs.
2. Create reference implementation / DDL profile for RFC-CDP-025.
3. Repair RFC-CDP-000 Series Index if stale.
4. Decide whether `proposal_sufficiency_record` and `formation_challenge_record` become RFC-CDP-022 payload types.
5. Continue lifecycle protocol updates only when their upstream objects are stable.

## 9. Do Not Assume

Do not assume:

- a draft is canonical because it is eloquent;
- a hierarchy is legitimate because it outranks;
- a proposal is sufficient because it is plausible;
- a decision is legitimate because a hash verifies;
- a conversation note is canon because it is in `collab/`;
- an AI output is authoritative because it is fluent;
- missing files are harmless.

## 10. Closing Frame

CDP work should be legible, legitimate, auditable, contestable, humane, repairable, and buildable.

If uncertain, say so.

If a file is missing, name it.

If a claim is not yet canon, preserve it as draft.

If a process hides power, challenge it.
