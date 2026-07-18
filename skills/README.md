# CDP Skills

Skills are reusable, version-controlled procedures for recurring engineering work in CDP.

They are not tool-specific prompts. A human engineer, Codex, Claude Code, or another capable agent should be able to follow the same skill and produce comparable evidence.

## Relationship to Other Repository Guidance

- `AGENTS.md` defines standing behavioral and safety constraints.
- `skills/` defines how a recurring capability is performed.
- `prompts/` composes one or more skills into a complete task workflow.
- `scripts/` contains executable automation invoked by skills.

## Skill Format

Each skill should contain:

```yaml
---
name: skill-name
description: One sentence describing when to use the skill.
inputs:
  - required information or artifacts
outputs:
  - evidence the skill must produce
---
```

Then use these sections:

1. `# Goal`
2. `## Preconditions`
3. `## Procedure`
4. `## Success Criteria`
5. `## Never`
6. `## Report`

## Design Rules

- Keep skills small and composable.
- Prefer executable repository commands over prose-only instructions.
- Name uncertainty rather than hiding it.
- Do not weaken governance or safety checks merely to make a task pass.
- Require evidence: commands run, files changed, tests passed, failures, and unresolved uncertainty.
- Do not duplicate standing rules from `AGENTS.md`; reference them.

## Current Skills

- `engineering/investigate-bug.md` — diagnose failures before patching.
- `database/inspect-schema.md` — inspect the live PostgreSQL schema and initialization evidence without changing state.
- `database/db-migration.md` — change PostgreSQL structure safely.
- `testing/docker-test.md` — run the canonical local Docker verification loop.
- `testing/regression-test.md` — prove a fix without hiding adjacent breakage.
- `governance/review-skill.md` — review a skill using observed evidence.
- `governance/propose-skill-change.md` — propose and validate a bounded procedural improvement.

## Governed Evolution

Skills may evolve from evidence gathered while they are used. They may not silently rewrite themselves.

Use `prompts/improve-the-process.md` when a completed task exposes repeated procedural friction. That workflow requires review, a bounded proposal, regression validation, preserved dissent, and a stop for human approval when safety, permissions, evidence requirements, data retention, or contestability would change.

A single run may perform at most one revision cycle. This prevents recursive optimization from outrunning understanding or oversight.
