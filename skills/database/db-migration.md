---
name: db-migration
description: Change the CDP PostgreSQL schema safely, preserving migration history, runtime reproducibility, and auditability.
inputs:
  - requested schema change
  - relevant data model and RFC context
outputs:
  - additive migration or initialization change
  - runtime database verification
  - regression evidence
---

# Goal

Make a PostgreSQL schema change without creating drift between source DDL, container initialization, application expectations, and the actual `cdp` database.

## Preconditions

1. Read and follow `AGENTS.md`.
2. Inspect the relevant RFCs, database DDL, initialization scripts, tests, and application models.
3. Confirm which database, schema, and migration mechanism are authoritative.
4. Confirm whether the change affects only new local databases or must upgrade existing databases.

## Procedure

1. Inspect the current schema sources and initialization order.
2. Inspect the running database when available:

   ```bash
   docker compose -f docker/docker-compose.yml exec -T postgres \
     psql -U cdp -d cdp -c '\dn' \
     -c '\dt *.*'
   ```

3. State the intended schema change and any compatibility risk before editing.
4. Prefer an additive, reviewable migration. Do not rewrite an already-applied migration unless the repository explicitly treats initialization DDL as disposable and the task is limited to fresh local databases.
5. Update tests that prove the required tables, columns, constraints, indexes, and extensions exist.
6. Run the narrowest relevant database tests first.
7. Run `make codex-test` for full Docker verification.
8. Compare the resulting runtime schema with the intended source definition.

## Success Criteria

- The intended schema exists in the `cdp` database.
- Initialization and upgrade behavior are explicit.
- Relevant constraints and indexes are tested.
- Application code and schema agree.
- `make codex-test` passes.
- No unrelated data is destroyed.

## Never

- Never manually create runtime tables as a substitute for repairing migrations or initialization.
- Never silently change the target database or schema.
- Never delete Docker volumes to hide an upgrade failure.
- Never weaken constraints merely to make fixtures pass.
- Never claim backward compatibility without testing it.

## Report

Return:

- authoritative schema files read
- migration or initialization files changed
- database and schema inspected
- SQL verification commands and results
- tests run
- compatibility assumptions
- unresolved uncertainty
