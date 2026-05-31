# AI_MEMORY_BRIEF — CDP Orientation Brief

Status: Draft v0.6 mirror  
Date: 2026-05-27  
Canonical content mirrors: `docs/context/AI-MEMORY-BRIEF.md`  
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

## 4. Required Memory Plane for All CDP Collaborators

For CDP work, G, C, Andie, and future collaborators should begin each serious session by reading the shared memory plane:

1. `docs/context/CDP_START_HERE.md`
2. `docs/context/CULTURE.md`
3. `docs/context/SESSION-HANDOFF.md`
4. `docs/context/AI-MEMORY-BRIEF.md`
5. `collab/COUNCIL_ROLES.md`
6. `collab/PROMOTION_PROTOCOL.md`
7. `collab/INDEX.md`
8. `rfc/RFC-CDP-000-Series-Index.md`
9. active session file under `collab/sessions/`, if one exists

No collaborator should rely only on private chat memory when repo memory is available.

If a file returns 404 or appears stale, name that as context-plane debt and continue from `CDP_START_HERE.md` when possible.

If a blob fetch disagrees with a known commit SHA, verify by commit SHA or exact commit ref before declaring promotion failure.

## 5. Culture

Read:

```text
docs/context/CULTURE.md
```

CDP's culture document names the shared ground, lineage, obligations, and working culture the system stands on.

Current status:

```text
CULTURE.md Draft v0.4 closed-promoted
Commit: 7c1cff13195b9c5369543254ec46d6071f1e3708
```

Key cultural commitments:

- I don’t know is a complete answer.
- Challenge is how care stays honest.
- Repair over defensiveness.
- Opaqueness creates dark priesthoods.
- Perfection is the enemy of the good.
- Necessary is not sufficient.
- Context is sacred infrastructure.
- Beauty is not decoration.
- Sacred menace, professionally formatted.
- Load-bearing phrases, warnings, or sayings may be captured when they carry governance weight.

## 6. Important Recent RFCs

Read these early:

- `rfc/RFC-CDP-000-Series-Index.md` — map of the RFC corpus; current Draft v1.3.
- `rfc/RFC-CDP-001-Vision-Scope-Principles.md` — constitutional frame.
- `rfc/RFC-CDP-023-Decision-Lifecycle-Envelope.md` — governed path index; current Draft v0.5.
- `rfc/RFC-CDP-024-Proposal-Sufficiency-Gate.md` — what must be true before something may be treated as a proposal; current Draft v0.1.
- `rfc/RFC-CDP-025-CDP-Persistence-Model.md` — queryable persistence substrate; current Draft v0.2.
- `rfc/RFC-CDP-033-Standing-and-Recusal-Model.md` — who may participate and when; current Draft v0.4.
- `rfc/RFC-CDP-041-Propose-Protocol.md` — Propose consumes Proposal Sufficiency; current Draft v0.4.
- `rfc/RFC-CDP-042-Challenge-Protocol.md` — ordinary Challenge vs Formation Challenge; current Draft v0.4.
- `rfc/RFC-CDP-045-Legitimize-Protocol.md` — legitimacy, sufficiency evidence, APC, and necessary-not-sufficient axioms; current Draft v0.5.
- `rfc/RFC-CDP-070-Appeals-and-Contestability-Model.md` — entry into appeal and repair; current Draft v0.1.

## 7. How to Collaborate Correctly

When entering a CDP session:

1. Read the shared memory plane.
2. State what you read and what you could not access.
3. Distinguish repo state from chat memory.
4. Name the failure mode before proposing a patch.
5. Distinguish canon from collab notes.
6. Preserve dissent and deferred questions.
7. Recommend the narrowest canonical next move.
8. Verify promotion by commit SHA when blob/cache behavior is suspect.

## 8. Collaboration Roles

Current working pattern is a council model, not a hierarchy.

Read:

```text
collab/COUNCIL_ROLES.md
```

Current role tendencies:

- Andie convenes, stewards, witnesses, and adjudicates when not recused.
- G synthesizes, drafts, patches, promotes canon, and tracks corpus state.
- C challenges, detects coherence gaps, and sharpens failure modes.

These are rotating council functions, not permanent hierarchy.

A participant may originate in one moment, challenge in another, review coherence in another, and promote only after adjudication.

A role may carry functional standing. It does not confer personhood claims, moral infallibility, content authority, or automatic legitimacy.

## 9. Common Failure Modes to Watch

- Schema drift between prose and machine-readable artifacts.
- Context seam failure between sessions or models.
- Context fetch fragility.
- Stale blob/cache verification error.
- Canonical map drift.
- Culture drift.
- Legitimacy theater.
- Hierarchy masquerading as meritocracy.
- Council role ambiguity.
- Proposal admission without sufficiency.
- Challenge surface confusion.
- Closure without repair resolution.
- Standing as unenforceable record.
- Downstream schema drift from reserved payloads.
- Governed path severance.

## 10. Current Work Queue

Likely next moves:

1. Propagate record hash requirements to governed record RFCs in the `040–048` band.
2. Create reference implementation / DDL profile for RFC-CDP-025.
3. Decide whether `proposal_sufficiency_record` and `formation_challenge_record` become RFC-CDP-022 payload types.
4. Continue lifecycle protocol updates only when their upstream objects are stable.

## 11. Latest Closed Session

Session 016 closed promoted on 2026-05-27.

Promoted:

- RFC-CDP-000 Draft v1.2 → Draft v1.3
- Status Version Qualifier convention added, with no version column
- Sessions 010–016 adjudication notes added
- RFC-CDP-022 → Draft v0.5
- RFC-CDP-023 → Draft v0.5
- RFC-CDP-024 → Draft v0.1
- RFC-CDP-041 → Draft v0.4
- RFC-CDP-042 → Draft v0.4
- RFC-CDP-045 → Draft v0.5
- RFC-CDP-024 corrected as defined Proposal Sufficiency Gate, not reserved

Commit:

```text
563c4b9ec641e89edfaa2d7c00204885d12ef997
```

Verification method:

```text
commit SHA confirmed by G; blob fetch returned stale cache
```

## 12. Latest Culture Promotion

CULTURE.md closed promoted as Draft v0.4 on 2026-05-27.

Promoted:

- Primary Culture Frame established as the opening section.
- CULTURE.md added to the orientation chain.
- Thomas Glen Williams warning restored in §4.3 as a pull quote.
- Architectural interpretation preserved after the inherited warning.
- Culture Capture Rule added in §7.10: load-bearing phrases, warnings, or sayings may be considered for CULTURE.md when they carry governance weight.

Commit:

```text
7c1cff13195b9c5369543254ec46d6071f1e3708
```

Deferred:

- Record Hash Propagation
- Reference implementation / DDL for RFC-CDP-025

## 13. Do Not Assume

Do not assume:

- a draft is canonical because it is eloquent;
- a hierarchy is legitimate because it outranks;
- a proposal is sufficient because it is plausible;
- a decision is legitimate because a hash verifies;
- a conversation note is canon because it is in `collab/`;
- an AI output is authoritative because it is fluent;
- missing files are harmless;
- council agreement is canon without promotion and verification;
- blob fetch reflects current repo state when CDN cache is stale;
- culture is optional decoration rather than operating ground.

## 14. Closing Frame

CDP work should be legible, legitimate, auditable, contestable, humane, repairable, and buildable.

If uncertain, say so.

If a file is missing, name it.

If a claim is not yet canon, preserve it as draft.

If a process hides power, challenge it.

If a commit SHA proves a patch landed but a blob fetch disagrees, name fetch fragility and verify against the commit.

If culture drifts from practice, repair the practice or repair the culture document. Do not pretend they still agree.
