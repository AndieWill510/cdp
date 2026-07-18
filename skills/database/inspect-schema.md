---
name: inspect-schema
description: Inspect the live CDP PostgreSQL schema and its initialization evidence without modifying data or structure.
inputs:
  - running local Docker stack or reachable CDP PostgreSQL database
  - repository branch and current database configuration
outputs:
  - identified database, user, search path, schemas, tables, extensions, and schema version
  - comparison between runtime state and repository initialization sources
  - evidence-backed diagnosis of missing or unexpected relations
---

# Goal

Determine what PostgreSQL database and schema state actually exist at runtime before proposing any migration, reset, or repair.

This skill is read-only. It exists to prevent guesses such as “the tables were not loaded” when the real issue may be the wrong database, schema, search path, initialization lifecycle, or stale Docker volume.

## Preconditions

1. Read and follow `AGENTS.md`.
2. Confirm the current branch and preserve unrelated work.
3. Read:
   - `docker/docker-compose.yml`
   - `docker/postgres/init/001_initialize.sh`
   - `docker/postgres/init/ddl/01-init-cdp.sql`
   - relevant files under `db/ddl/` and `db/seed/`
   - `skills/database/db-migration.md` when inspection may lead to a schema change
4. Do not delete volumes, rerun initialization manually, or change DDL during inspection.

## Procedure

### 1. Establish repository and container context

Run:

```bash
git branch --show-current
git status --short
docker compose -f docker/docker-compose.yml config --quiet
docker compose -f docker/docker-compose.yml ps
```

Record whether the `postgres` service is running and healthy.

### 2. Confirm the configured database target

Inspect the Compose configuration and record:

- `POSTGRES_DB`
- `POSTGRES_USER`
- the application `DATABASE_URL`
- the PostgreSQL container name
- mounted initialization paths
- the named volume used for `/var/lib/postgresql/data`

For the current local stack, the expected target is:

- database: `cdp`
- user: `cdp`
- service: `postgres`

Do not assume these values if the repository configuration has changed.

### 3. Confirm the live connection identity

Run:

```bash
docker compose -f docker/docker-compose.yml exec -T postgres \
  psql -U cdp -d cdp -X -v ON_ERROR_STOP=1 -c \
  "SELECT current_database(), current_user, session_user, current_schema(), current_setting('search_path');"
```

If this command fails, report the connection failure before doing anything else.

### 4. Inspect extensions

Run:

```bash
docker compose -f docker/docker-compose.yml exec -T postgres \
  psql -U cdp -d cdp -X -v ON_ERROR_STOP=1 -c \
  "SELECT extname, extversion FROM pg_extension ORDER BY extname;"
```

Verify that required extensions include:

- `pgcrypto`
- `vector`

### 5. Inspect schemas

Run:

```bash
docker compose -f docker/docker-compose.yml exec -T postgres \
  psql -U cdp -d cdp -X -v ON_ERROR_STOP=1 -c \
  "SELECT schema_name FROM information_schema.schemata ORDER BY schema_name;"
```

Verify whether the expected CDP schemas exist:

- `cdp_core`
- `cdp_audit`
- `cdp_repair`
- `cdp_projection`

### 6. Inspect relations by schema

Run:

```bash
docker compose -f docker/docker-compose.yml exec -T postgres \
  psql -U cdp -d cdp -X -v ON_ERROR_STOP=1 -c \
  "SELECT schemaname, tablename FROM pg_catalog.pg_tables WHERE schemaname NOT IN ('pg_catalog', 'information_schema') ORDER BY schemaname, tablename;"
```

Also inspect views and materialized views:

```bash
docker compose -f docker/docker-compose.yml exec -T postgres \
  psql -U cdp -d cdp -X -v ON_ERROR_STOP=1 -c \
  "SELECT table_schema, table_name, table_type FROM information_schema.tables WHERE table_schema NOT IN ('pg_catalog', 'information_schema') ORDER BY table_schema, table_name;"
```

Do not treat `\dt` returning no relations as proof that the database is empty until the active schema and search path have been confirmed. Prefer fully qualified inspection across all non-system schemas.

### 7. Inspect bootstrap evidence

Run:

```bash
docker compose -f docker/docker-compose.yml exec -T postgres \
  psql -U cdp -d cdp -X -v ON_ERROR_STOP=1 -c \
  "SELECT component, version, initialized_at FROM cdp_core.schema_version ORDER BY component;"
```

Then verify the bootstrap smoke row:

```bash
docker compose -f docker/docker-compose.yml exec -T postgres \
  psql -U cdp -d cdp -X -v ON_ERROR_STOP=1 -c \
  "SELECT label, embedding FROM cdp_projection.vector_smoke_test WHERE label = 'bootstrap';"
```

Expected initialization evidence currently includes:

- `cdp_core.schema_version`
- component `local-postgres-bootstrap`
- version `0.1.0`
- a `bootstrap` row in `cdp_projection.vector_smoke_test`

### 8. Inspect initialization logs

Run:

```bash
docker compose -f docker/docker-compose.yml logs --no-color postgres | \
  grep -E "Initializing CDP database|Executing .*\.sql|CDP database initialization complete|Skipping .*decision_registry" || true
```

Remember: `/docker-entrypoint-initdb.d` initialization runs only when PostgreSQL starts with an empty data directory. A healthy container with a persistent existing volume may correctly skip all initialization scripts.

### 9. Compare runtime state with repository sources

Compare the runtime schemas and relations against:

- `docker/postgres/init/ddl/01-init-cdp.sql`
- `db/ddl/*.sql`
- `db/seed/*.sql`
- the execution order in `docker/postgres/init/001_initialize.sh`

Classify discrepancies as one of:

- wrong database or user
- wrong schema or search path
- initialization did not run
- initialization ran against an earlier repository version
- persistent volume contains stale state
- DDL failed partway through
- source DDL and runtime schema have drifted
- expected relation is not actually part of the current initialization path

### 10. Stop before repair

Report findings before changing files or database state.

If repair is needed, route next to the appropriate skill:

- `skills/database/db-migration.md` for a schema change
- `skills/engineering/investigate-bug.md` for initialization or runtime failure
- `skills/testing/docker-test.md` for full-stack verification
- future `skills/database/reset-local-db.md` only when destructive reset is explicitly approved

## Success Criteria

- The active database, user, schema, and search path are known.
- Runtime extensions, schemas, relations, and bootstrap evidence are recorded.
- Initialization logs and mounted source paths are inspected.
- Any discrepancy is classified with evidence.
- No data, schema, volume, or repository file is changed.
- The next repair workflow, if any, is named explicitly.

## Never

- Never infer that no tables exist from an unqualified `\dt` alone.
- Never run `docker compose down -v` during inspection.
- Never drop schemas, databases, tables, or volumes.
- Never manually create missing relations as a diagnostic shortcut.
- Never claim initialization failed without checking logs and persistent-volume behavior.
- Never change the database target merely to make expected relations appear.

## Report

Return:

- branch and worktree state
- configured database target
- live database, user, current schema, and search path
- extensions found and missing
- schemas found and missing
- relations grouped by schema
- bootstrap version and smoke evidence
- initialization log evidence
- repository files inspected
- discrepancy classification
- recommended next skill
- unresolved uncertainty
