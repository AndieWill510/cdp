# SESSION-HANDOFF — CDP Session Handoff

Status: Draft v0.4 alias  
Date: 2026-05-27  
Canonical content mirrors: `docs/context/SESSION_HANDOFF.md`  
Purpose: Durable handoff file for moving CDP work between sessions, collaborators, and AI models.

## 1. Why This File Exists

CDP depends on continuity across sessions.

A constitutional control plane cannot rely on ephemeral chat memory, model context windows, or one participant personally carrying the full state.

This file defines what must be handed off when a session pauses, resumes, changes model, or moves from collaboration into canon.

Failure mode:

> Context seam failure — when a new session or model cannot tell what is canonical, what is draft, what is pending adjudication, and what must not be silently promoted.

## 2. Current Orientation Path

A new collaborator should read, in order:

1. `docs/context/CDP_START_HERE.md`
2. `docs/context/CULTURE.md`
3. `docs/context/SESSION-HANDOFF.md`
4. `docs/context/AI-MEMORY-BRIEF.md`
5. `collab/COUNCIL_ROLES.md`
6. `collab/PROMOTION_PROTOCOL.md`
7. `collab/INDEX.md`
8. `rfc/RFC-CDP-000-Series-Index.md`
9. active session file under `collab/sessions/`, if one exists

This applies to G, C, Andie, and future CDP collaborators. No model should rely on private chat memory when repo memory is available.

If any file in this path is missing, that is context-plane debt and should be repaired before starting major new RFC work.

## 3. Handoff Minimum

Every handoff should include:

- current active session;
- latest promoted RFCs;
- current promotion queue;
- unresolved decisions;
- deferred work;
- known dissent;
- files changed in the last session;
- next recommended action;
- what must not be assumed.

## 4. Handoff Template

```text
SESSION:
DATE_OPENED:
DATE_CLOSED:
MODERATOR:
STATUS:
CANON_TARGET:

PROMOTED:
-

NOT PROMOTED:
-

COMMIT:
-

VERIFICATION METHOD:
-

OPEN QUESTIONS:
-

DO NOT ASSUME:
-
```

## 5. Current Handoff Snapshot

As of 2026-05-27, recent promoted work includes:

- CULTURE.md Draft v0.3 — shared ground and working culture added to the context plane; Thomas Glen Williams warning restored in §4.3.
- RFC-CDP-000 Draft v1.3 — Series Index repaired for Sessions 007–016 and status-version convention made explicit.
- RFC-CDP-022 Draft v0.5 — APC gate result payload defined.
- RFC-CDP-023 Draft v0.5 — proposal admission references added to Decision Lifecycle Envelope.
- RFC-CDP-024 Draft v0.1 — Proposal Sufficiency Gate created.
- RFC-CDP-025 Draft v0.2 — Persistence Model with standing enforcement projection.
- RFC-CDP-033 Draft v0.4 — Standing persistence reference added.
- RFC-CDP-041 Draft v0.4 — Propose wired to Proposal Sufficiency.
- RFC-CDP-042 Draft v0.4 — Formation Challenge distinguished from ordinary Challenge.
- RFC-CDP-045 Draft v0.5 — Legitimize wired to APC and necessary-not-sufficient axioms, including hierarchy.
- RFC-CDP-070 Draft v0.1 — Appeals and Contestability Model created.

## 6. Latest Closed Session

```text
SESSION: 016
DATE_OPENED: 2026-05-27
DATE_CLOSED: 2026-05-27
MODERATOR: Andie
STATUS: closed-promoted
CANON_TARGET: rfc/RFC-CDP-000-Series-Index.md

PROMOTED:
- RFC-CDP-000 Draft v1.2 → Draft v1.3
- date updated to May 27, 2026
- Status Version Qualifier convention added (no version column)
- Sessions 010–016 adjudication notes added
- 022: Draft → Draft v0.5
- 023: Draft → Draft v0.5
- 024: Reserved → Draft v0.1
- 041: Draft → Draft v0.4
- 042: Draft → Draft v0.4
- 045: Draft → Draft v0.5
- §7 corrected: RFC-CDP-024 now identified as Proposal Sufficiency Gate

NOT PROMOTED:
- Record Hash Propagation (deferred, next in queue)
- Reference implementation / DDL for RFC-CDP-025 (deferred)

COMMIT: 563c4b9ec641e89edfaa2d7c00204885d12ef997

VERIFICATION METHOD: commit SHA confirmed by G; blob fetch returned stale cache

OPEN QUESTIONS:
- None from this session

DO NOT ASSUME:
- blob fetch reflects current repo state when CDN cache is stale; use commit SHA verification for authoritative confirmation
```

## 7. Latest Culture Promotion

```text
ARTIFACT: docs/context/CULTURE.md
STATUS: Draft v0.3 closed-promoted
COMMIT: 617c01288c325a03291088dd4e06269f21a52f37
PROMOTED:
- Primary Culture Frame established as the opening section.
- CULTURE.md added to the orientation chain.
- Thomas Glen Williams warning restored in §4.3 as a pull quote.
- Architectural interpretation preserved after the inherited warning.
VERIFICATION METHOD: commit SHA confirmed by G.
```

## 8. Current Queue

Current likely queue:

1. Record Hash Propagation to governed record RFCs in the `040–048` band.
2. Reference implementation / DDL profile for RFC-CDP-025.
3. Review whether `proposal_sufficiency_record` and `formation_challenge_record` should be registered in RFC-CDP-022.

## 9. Verification Rule

If a blob-path fetch disagrees with a known commit SHA, do not immediately assume the commit failed.

Verify by commit SHA or exact commit ref before declaring promotion failure.

A stale blob fetch is context fetch fragility, not proof that the canonical patch failed.

## 10. Rules for Model Handoff

A receiving model should:

- state what files it has read;
- state any files it could not access;
- distinguish repo state from chat memory;
- avoid promoting unverified assumptions;
- ask for or search the relevant active session file before drafting canon;
- preserve dissent and deferred work rather than smoothing it away;
- use commit SHA verification when blob fetches appear stale;
- read and preserve `docs/context/CULTURE.md` as part of the shared context plane.

A receiving model should not:

- infer canon from chat alone;
- treat `collab/` content as canonical before promotion;
- treat hierarchy, confidence, fluency, or recency as legitimacy;
- collapse open questions for momentum;
- treat a stale blob fetch as authoritative when a commit SHA proves otherwise;
- treat culture as optional decoration rather than operating ground.

## 11. Relationship to CDP Itself

This file is not an RFC.

It is a context-plane artifact that supports CDP collaboration hygiene.

If its contents become normative, they should be promoted through `collab/PROMOTION_PROTOCOL.md` into an RFC or RFC update.
