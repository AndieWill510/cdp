# Improve the Process

Use this workflow only after a real task has exposed repeated friction, ambiguity, omission, or unsafe behavior in an existing skill or prompt.

## Load

Read:

- `AGENTS.md`
- `skills/README.md`
- `skills/governance/review-skill.md`
- `skills/governance/propose-skill-change.md`
- `skills/testing/regression-test.md`
- the skill or prompt under review
- the completed task report and relevant logs or diffs

## Workflow

1. Describe the observed friction using concrete evidence.
2. Determine whether the defect belongs in:
   - application code
   - tests
   - scripts or tooling
   - environment configuration
   - a skill
   - a composing prompt
3. If the defect is not procedural, stop and route it to the appropriate engineering workflow.
4. Follow `skills/governance/review-skill.md`.
5. Preserve dissent and uncertainty; do not force a change merely to complete the loop.
6. When revision is justified, follow `skills/governance/propose-skill-change.md`.
7. Validate the revised procedure by repeating the relevant task and following `skills/testing/regression-test.md`.
8. Permit at most one revision cycle in this run.
9. Stop for human review when the proposal changes:
   - destructive permissions
   - data retention
   - security boundaries
   - required evidence
   - human approval or contestability
   - `AGENTS.md`
10. Report whether the process should be adopted, revised later, or rejected.

## Governing Principle

The repository may learn from how work actually happens, but it may not silently redefine what counts as safe, truthful, or complete.

## Final Report

Report:

- task that exposed the friction
- evidence reviewed
- layer where the defect belongs
- skill or prompt reviewed
- review disposition
- files changed
- validation run
- before-and-after result
- safety or governance impact
- dissent and unresolved uncertainty
- human approval required
