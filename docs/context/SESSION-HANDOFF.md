# SESSION-HANDOFF — CDP Session Handoff

Status: Draft v0.1 alias  
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
2. `docs/context/SESSION-HANDOFF.md`
3. `docs/context/AI-MEMORY-BRIEF.md`
4. `collab/COUNCIL_ROLES.md`
5. `collab/PROMOTION_PROTOCOL.md`
6. `collab/INDEX.md`
7. `rfc/RFC-CDP-000-Series-Index.md`
8. active session file under `collab/sessions/`, if one exists

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
DATE:
MODERATOR:
CURRENT STATUS:

CANONICAL FILES CHANGED:
-

SESSION FILES CHANGED:
-

DECISIONS MADE:
-

OPEN QUESTIONS:
-

DEFERRED WORK:
-

KNOWN DISSENT:
-

NEXT RECOMMENDED MOVE:
-

DO NOT ASSUME:
-
```

## 5. Current Handoff Snapshot

As of 2026-05-27, recent promoted work includes:

- RFC-CDP-022 Draft v0.5 — APC gate result payload defined.
- RFC-CDP-023 Draft v0.5 — proposal admission references added to Decision Lifecycle Envelope.
- RFC-CDP-024 Draft v0.1 — Proposal Sufficiency Gate created.
- RFC-CDP-025 Draft v0.2 — Persistence Model with standing enforcement projection.
- RFC-CDP-033 Draft v0.4 — Standing persistence reference added.
- RFC-CDP-041 Draft v0.4 — Propose wired to Proposal Sufficiency.
- RFC-CDP-042 Draft v0.4 — Formation Challenge distinguished from ordinary Challenge.
- RFC-CDP-045 Draft v0.5 — Legitimize wired to APC and necessary-not-sufficient axioms, including hierarchy.
- RFC-CDP-070 Draft v0.1 — Appeals and Contestability Model created.

## 6. Current Queue

Current likely queue:

1. Record Hash Propagation to governed record RFCs in the `040–048` band.
2. Reference implementation / DDL profile for RFC-CDP-025.
3. Series Index repair if RFC-CDP-000 is stale relative to recent sessions.
4. Review whether `proposal_sufficiency_record` and `formation_challenge_record` should be registered in RFC-CDP-022.

## 7. Rules for Model Handoff

A receiving model should:

- state what files it has read;
- state any files it could not access;
- distinguish repo state from chat memory;
- avoid promoting unverified assumptions;
- ask for or search the relevant active session file before drafting canon;
- preserve dissent and deferred work rather than smoothing it away.

A receiving model should not:

- infer canon from chat alone;
- treat `collab/` content as canonical before promotion;
- treat hierarchy, confidence, fluency, or recency as legitimacy;
- collapse open questions for momentum.

## 8. Relationship to CDP Itself

This file is not an RFC.

It is a context-plane artifact that supports CDP collaboration hygiene.

If its contents become normative, they should be promoted through `collab/PROMOTION_PROTOCOL.md` into an RFC or RFC update.
