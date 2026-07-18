---
name: propose-skill-change
description: Propose a bounded, reviewable change to a CDP skill based on observed evidence.
inputs:
  - completed review from skills/governance/review-skill.md
  - target skill path
outputs:
  - proposed patch
  - rationale, risks, and validation plan
---

# Goal

Turn observed process friction into a small, contestable, testable improvement without allowing silent self-modification.

## Preconditions

- Read `AGENTS.md`, `skills/README.md`, and `skills/governance/review-skill.md`.
- Complete or obtain an evidence-backed review of the target skill.
- Confirm the work is on a non-default branch.
- Preserve unrelated work.

## Procedure

1. Restate the problem using observed evidence.
2. Identify the target skill and any scripts or prompts it coordinates.
3. State why the problem belongs in the skill rather than in code, tests, tooling, or environment configuration.
4. Draft the smallest coherent change.
5. Explain how the change affects:
   - safety
   - human oversight
   - contestability
   - evidence requirements
   - portability across contributors and agents
6. Define validation before applying the patch:
   - a task that previously exposed the friction
   - expected observable improvement
   - regression checks
   - stop conditions
7. Apply the patch only when the requested scope authorizes repository changes.
8. Run the validation task using the revised skill.
9. Compare results before and after when prior evidence exists.
10. Report the proposal and evidence; do not self-approve consequential governance reductions.

## Success Criteria

- The change traces directly to observed evidence.
- The patch is bounded and reviewable.
- Validation demonstrates whether the change improved the workflow.
- Any safety reduction requires explicit human approval.
- The original rationale and dissent remain visible in version history or the task report.

## Never

- Do not modify `AGENTS.md` through this skill.
- Do not make a process change solely to suppress a failure or inconvenient warning.
- Do not broaden permissions or destructive operations by default.
- Do not claim the revised skill is better without running its validation plan.
- Do not recursively revise the same skill more than once in a single task without stopping for review.

## Report

Report:

- evidence motivating the change
- target files
- why this is a skill change
- patch summary
- safety and governance impact
- validation performed
- before-and-after result
- unresolved uncertainty
- approval still required
