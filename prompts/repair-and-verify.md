# Repair and Verify

Use this workflow when asked to diagnose and repair a defect in the local CDP system.

## Load

1. Read `AGENTS.md`.
2. Follow `skills/engineering/investigate-bug.md`.
3. If the defect touches PostgreSQL schema or initialization, also follow `skills/database/db-migration.md`.
4. Complete verification with `skills/testing/docker-test.md`.

## Instruction

Diagnose the reported behavior from evidence before editing. Make the smallest coherent repair, add or strengthen a regression test, and run the canonical Docker verification loop.

Do not delete Docker volumes, discard unrelated work, commit, or push unless explicitly instructed.

Do not declare completion while relevant tests or health checks fail.

## Required Final Report

Return:

- branch inspected
- files read
- files changed
- diagnosis and supporting evidence
- commands run
- tests and health checks
- PostgreSQL verification when relevant
- unresolved uncertainty
