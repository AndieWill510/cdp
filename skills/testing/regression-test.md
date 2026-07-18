---
name: regression-test
description: Prove that a code or process change fixes its target without breaking previously valid behavior.
inputs:
  - changed files or proposed patch
  - original failure or friction evidence
outputs:
  - focused regression evidence
  - broader verification result
---

# Goal

Verify that a change resolves the observed problem and preserves relevant existing behavior.

## Preconditions

- Read `AGENTS.md`.
- Identify the original failing behavior or process friction.
- Identify the narrowest test that can reproduce it.
- Preserve Docker volumes unless explicitly instructed otherwise.

## Procedure

1. Record the original reproduction command and observed failure.
2. Add or identify a focused test that fails for the original reason.
3. Run the focused test before the patch when practical and safe.
4. Apply or inspect the smallest coherent patch.
5. Run the focused test again.
6. Run adjacent tests covering the same component, schema, or workflow.
7. Run the repository's canonical verification command:

   ```bash
   make codex-test
   ```

8. Inspect Docker service status and captured logs for hidden failures.
9. When the change affects PostgreSQL, verify expected relations and representative queries.
10. Distinguish:
    - verified pass
    - unrelated failure
    - environmental blocker
    - untested assumption

## Success Criteria

- The original failure is reproducible or its absence is honestly explained.
- A focused test demonstrates the fix.
- Broader verification passes or failures are clearly bounded.
- Hidden service or database failures are not ignored.
- Remaining uncertainty is explicit.

## Never

- Do not weaken assertions merely to obtain a green test.
- Do not delete or skip a valid failing test without explaining why it is obsolete.
- Do not describe an environmental blocker as a product defect.
- Do not declare regression coverage when only syntax or lint checks ran.

## Report

Report:

- original failure
- reproduction command
- focused regression test
- adjacent tests
- canonical verification result
- Docker status
- database verification when applicable
- unrelated failures
- untested assumptions
- conclusion
