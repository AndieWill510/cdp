---
name: investigate-bug
description: Diagnose a CDP defect from evidence, patch the smallest root cause, and prove the repair without disturbing unrelated work.
inputs:
  - observed failure, error, or unexpected behavior
outputs:
  - evidence-backed diagnosis
  - minimal repair when authorized
  - regression test and verification evidence
---

# Goal

Turn an observed failure into a reproducible, explained, and tested repair rather than a speculative patch.

## Preconditions

1. Read and follow `AGENTS.md`.
2. Preserve unrelated working-tree changes.
3. Capture the exact observed behavior, expected behavior, and environment.
4. Identify the narrowest command that reproduces the failure.

## Procedure

1. Inspect relevant code, tests, configuration, recent changes, and logs.
2. Reproduce the failure before editing when practical.
3. Separate evidence from hypotheses.
4. State the most likely root cause and meaningful alternatives.
5. Make the smallest coherent patch that addresses the root cause.
6. Add or strengthen a regression test that fails before the repair and passes after it.
7. Run the narrow test first.
8. Use `skills/testing/docker-test.md` when the behavior crosses process, database, network, container, or service boundaries.
9. Review the final diff for unrelated changes and accidental schema drift.

## Success Criteria

- The failure is reproducible or the inability to reproduce is clearly stated.
- The diagnosis is supported by observed evidence.
- A regression test protects the repaired behavior.
- Relevant tests pass.
- No unrelated behavior or governance control is weakened.

## Never

- Never patch solely from an error message without inspecting the surrounding system.
- Never suppress an exception, warning, or failing test without explaining why suppression is correct.
- Never broaden scope merely because adjacent cleanup is tempting.
- Never report certainty greater than the evidence supports.

## Report

Return:

- observed and expected behavior
- reproduction command and result
- evidence gathered
- root cause and alternatives considered
- files changed
- regression test added or updated
- verification performed
- remaining uncertainty
