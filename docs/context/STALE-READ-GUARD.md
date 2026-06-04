# STALE-READ-GUARD — Context Fetch and Repeated-Diagnosis Guard

Status: Draft v0.1  
Date: 2026-06-04  
Purpose: Prevent stateless collaborators from rediscovering repaired context-plane issues as fresh debt.

## 1. Why This File Exists

Some collaborators enter CDP sessions without durable conversational memory. That is useful for fresh challenge, but it can create a repeated-diagnosis failure mode: the same old context-plane issue is rediscovered and reported as new work.

This file exists to convert repeated diagnosis into verification and repair.

Failure mode:

> Groundhog Day context drift — when a stateless or stale-fetch collaborator repeatedly reports a repaired or bounded context-plane issue as if it were still active.

## 2. Verification Rule

Before reporting context-plane debt involving orientation paths, old filenames, missing session records, or deprecated primers, first verify the current repository state through the preferred entry path:

1. `docs/context/CDP_START_HERE.md`
2. `docs/context/CULTURE.md`
3. `docs/context/README.md`
4. `docs/context/SESSION-HANDOFF.md`
5. `docs/context/AI-MEMORY-BRIEF.md`
6. `collab/INDEX.md`
7. `rfc/RFC-CDP-000-Series-Index.md`

If the current repo still shows the problem, name it as context-plane debt and recommend the narrowest repair.

If only an old local cache, stale fetch, old primer, or prior chat excerpt shows the problem, do not re-litigate it as active repo debt. Name it as stale-read or context-fetch fragility and move to the live edge.

## 3. Known Repaired or Bounded Items

The following items should not be repeatedly rediscovered as new defects without fresh verification:

- `docs/context/README.md` is the current context-folder entry point.
- `C_ORIENTATION.md` has been replaced by `CDP_START_HERE.md`, `AI-MEMORY-BRIEF.md`, `CULTURE.md`, `COUNCIL_ROLES.md`, and `C_CDP_PREFERENCES.md`.
- Hyphenated filenames are preferred for collaborator fetching: `SESSION-HANDOFF.md` and `AI-MEMORY-BRIEF.md`.
- Underscore versions may exist as compatibility aliases, not preferred fetch paths.
- Session 016 has a collaboration record at `collab/sessions/016-rfc-series-index-repair-and-status-version-convention.md`.
- `collab/INDEX.md` is the current collaboration-session index.

## 4. Collaborator Instruction

When entering a CDP session, a collaborator should state:

```text
I checked STALE-READ-GUARD before naming context-plane debt.
```

If a reported defect appears in this guard, the collaborator should verify current repo state before continuing the critique.

## 5. Repair Rule

Do not make Andie, G, C, or any future collaborator carry the same context repair in memory alone.

If a repeated issue is real, repair the file.

If a repeated issue is stale, route future collaborators through this guard.

If a repeated issue is ambiguous, record the ambiguity here with the current best verification path.
