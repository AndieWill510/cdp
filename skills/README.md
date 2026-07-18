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
