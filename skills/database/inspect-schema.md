---
name: inspect-schema
description: Inspect the live CDP PostgreSQL schema and its initialization evidence without modifying data or structure.
inputs:
  - running local Docker stack or reachable CDP PostgreSQL database
  - repository branch and current database configuration
outputs:
  - identified database, user, search path, schemas, relations, extensions, and schema version
  - comparison between runtime state and repository initialization sources
  - evidence-backed diagnosis of missing, duplicated, or unexpected relations
---

# Goal

Determine what PostgreSQL database and schema state actually exist at runtime before proposing any migration, reset, or repair.

This skill is read-only. It exists to prevent guesses such as “the tables were not loaded” when the real issue may be the wrong database, schema, search path, initialization lifecycle, duplicate initialization ownership, or a persistent Docker volume created from an earlier repository state.

## Preconditions

1. Read and follow `AGENTS.md`.
2. Confirm the current branch and preserve unrelated work.
3. Read:
   - `docker/docker-compose.yml`
   - `docker/postgres/init/001_initialize.sh`
   - `docker/postgres/init/01-init-cdp.sql`
4. Enumerate initialization sources before deciding which repository DDL or seed files are relevant.
5. Do not delete volumes, rerun initialization manually, modify DDL, or change database state during inspection.
6. Load `skills/database/db-migration.md` only after this inspection classifies a discrepancy as requiring a schema change.

## Procedure

Run all commands from the repository root. Preserve command failures; do not append `|| true` to Docker, Compose, or PostgreSQL commands.

### 1. Establish repository and container context

Run:

```bash
git branch --show-current
git status --short

COMPOSE_FILE="docker/docker-compose.yml"
docker compose -f "${COMPOSE_FILE}" config --quiet
docker compose -f "${COMPOSE_FILE}" ps
```

Record whether the `postgres` service exists, is running, and is healthy. A blank `git status --short` means the worktree is clean; state that explicitly in the report.

### 2. Resolve and record the configured database target

Emit the resolved Compose configuration as JSON:

```bash
COMPOSE_CONFIG_JSON="$(docker compose -f "${COMPOSE_FILE}" config --format json)"
printf '%s\n' "${COMPOSE_CONFIG_JSON}" | python3 -m json.tool
```

Extract the PostgreSQL database, user, container name, data mount, initialization mounts, and every configured application `DATABASE_URL`:

```bash
CONFIG_FILE="$(mktemp -t cdp-compose-config.XXXXXX.json)"
printf '%s\n' "${COMPOSE_CONFIG_JSON}" > "${CONFIG_FILE}"

python3 - "${CONFIG_FILE}" <<'PY'
import json
import sys

config = json.load(open(sys.argv[1], encoding="utf-8"))
services = config.get("services", {})
postgres = services.get("postgres")
if postgres is None:
    raise SystemExit("ERROR: resolved Compose configuration has no postgres service")

environment = postgres.get("environment", {}) or {}
print(f"POSTGRES_DB={environment.get('POSTGRES_DB', '')}")
print(f"POSTGRES_USER={environment.get('POSTGRES_USER', '')}")
print(f"POSTGRES_CONTAINER={postgres.get('container_name', '')}")

for mount in postgres.get("volumes", []) or []:
    source = mount.get("source", "") if isinstance(mount, dict) else str(mount)
    target = mount.get("target", "") if isinstance(mount, dict) else ""
    print(f"POSTGRES_MOUNT={source} -> {target}")

for service_name, service in sorted(services.items()):
    service_environment = service.get("environment", {}) or {}
    database_url = service_environment.get("DATABASE_URL")
    if database_url:
        print(f"DATABASE_URL[{service_name}]={database_url}")
PY

read -r POSTGRES_DB POSTGRES_USER < <(
  python3 - "${CONFIG_FILE}" <<'PY'
import json
import sys

config = json.load(open(sys.argv[1], encoding="utf-8"))
environment = config["services"]["postgres"].get("environment", {}) or {}
print(environment.get("POSTGRES_DB", ""), environment.get("POSTGRES_USER", ""))
PY
)

if [[ -z "${POSTGRES_DB}" || -z "${POSTGRES_USER}" ]]; then
  echo "ERROR: POSTGRES_DB or POSTGRES_USER is absent from the resolved Compose configuration." >&2
  exit 1
fi
```

Do not continue with hardcoded credentials after discovering different configured values.

For the current local stack, the expected values are `cdp` and `cdp`, but the resolved configuration is authoritative.

### 3. Define one parameterized read-only PostgreSQL command

Use the discovered values for all subsequent SQL:

```bash
psql_cdp() {
  docker compose -f "${COMPOSE_FILE}" exec -T postgres \
    psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" \
    -X -v ON_ERROR_STOP=1 "$@"
}
```

### 4. Confirm the live connection identity

Run:

```bash
psql_cdp -c \
  "SELECT current_database(), current_user, session_user, current_schema(), current_setting('search_path');"
```

Confirm that the live database and user match the resolved configuration. If they do not match, stop and classify the discrepancy before inspecting expected relations.

### 5. Inspect extensions

Run:

```bash
psql_cdp -c \
  "SELECT extname, extversion FROM pg_extension ORDER BY extname;"
```

Verify whether required extensions are present:

- `pgcrypto`
- `vector`

Record versions as evidence.

### 6. Inspect schemas

Run:

```bash
psql_cdp -c \
  "SELECT schema_name FROM information_schema.schemata ORDER BY schema_name;"
```

Verify whether the expected CDP schemas exist:

- `cdp_core`
- `cdp_audit`
- `cdp_repair`
- `cdp_projection`

An expected schema may legitimately contain no relations; report that separately from a missing schema.

### 7. Inspect all relation types with one catalog query

Run:

```bash
psql_cdp -c "
SELECT
    n.nspname AS schema_name,
    c.relname AS relation_name,
    CASE c.relkind
        WHEN 'r' THEN 'table'
        WHEN 'p' THEN 'partitioned table'
        WHEN 'v' THEN 'view'
        WHEN 'm' THEN 'materialized view'
        WHEN 'f' THEN 'foreign table'
        ELSE c.relkind::text
    END AS relation_type
FROM pg_catalog.pg_class AS c
JOIN pg_catalog.pg_namespace AS n
  ON n.oid = c.relnamespace
WHERE c.relkind IN ('r', 'p', 'v', 'm', 'f')
  AND n.nspname NOT IN ('pg_catalog', 'information_schema')
  AND n.nspname !~ '^pg_toast'
ORDER BY n.nspname, relation_type, c.relname;
"
```

Do not treat an unqualified `\dt` returning no relations as proof that the database is empty. Record the active `search_path` and inspect all non-system schemas.

### 8. Inspect bootstrap evidence and its cardinality

Inspect schema-version evidence:

```bash
psql_cdp -c \
  "SELECT component, version, initialized_at FROM cdp_core.schema_version ORDER BY component;"
```

Inspect the bootstrap smoke row count before reading the rows:

```bash
psql_cdp -c \
  "SELECT count(*) AS bootstrap_row_count FROM cdp_projection.vector_smoke_test WHERE label = 'bootstrap';"

psql_cdp -c \
  "SELECT id, label, embedding, created_at FROM cdp_projection.vector_smoke_test WHERE label = 'bootstrap' ORDER BY created_at, id;"
```

Interpret cardinality explicitly:

- zero rows: bootstrap evidence is missing;
- one row: expected current evidence;
- more than one row: duplicate execution or missing uniqueness may exist and must be investigated.

Expected initialization evidence currently includes:

- `cdp_core.schema_version`;
- component `local-postgres-bootstrap`;
- version `0.1.0`;
- exactly one `bootstrap` row in `cdp_projection.vector_smoke_test`.

### 9. Inspect initialization logs without masking Docker failures

Capture logs first so a Docker or permission failure remains nonzero:

```bash
POSTGRES_LOG_FILE="$(mktemp -t cdp-postgres-logs.XXXXXX.log)"
docker compose -f "${COMPOSE_FILE}" logs --no-color postgres > "${POSTGRES_LOG_FILE}"
```

Then inspect both CDP wrapper execution and native PostgreSQL entrypoint execution:

```bash
if ! grep -E \
  "Initializing CDP database|Executing .*\.sql|running /docker-entrypoint-initdb\.d/.*\.sql|CDP database initialization complete|Skipping .*decision_registry" \
  "${POSTGRES_LOG_FILE}"; then
  echo "No matching PostgreSQL initialization evidence was found in the captured logs."
fi
```

“No matching evidence” is not the same as command failure. Preserve the complete captured log path in the report.

Remember: `/docker-entrypoint-initdb.d` initialization runs only when PostgreSQL starts with an empty data directory. A healthy container with an existing volume may correctly contain no initialization messages from its latest restart.

### 10. Record persistent-volume and container lifecycle evidence

Resolve the running container and inspect its data mount:

```bash
POSTGRES_CONTAINER_ID="$(docker compose -f "${COMPOSE_FILE}" ps -q postgres)"

if [[ -z "${POSTGRES_CONTAINER_ID}" ]]; then
  echo "ERROR: No running container ID was resolved for the postgres service." >&2
  exit 1
fi

docker inspect "${POSTGRES_CONTAINER_ID}" --format \
  'container_id={{.Id}} container_created={{.Created}} restart_count={{.RestartCount}} status={{.State.Status}} started_at={{.State.StartedAt}}'

docker inspect "${POSTGRES_CONTAINER_ID}" --format '{{json .Mounts}}' | python3 -m json.tool

POSTGRES_DATA_VOLUME="$(
  docker inspect "${POSTGRES_CONTAINER_ID}" --format \
    '{{range .Mounts}}{{if eq .Destination "/var/lib/postgresql/data"}}{{.Name}}{{end}}{{end}}'
)"

if [[ -n "${POSTGRES_DATA_VOLUME}" ]]; then
  docker volume inspect "${POSTGRES_DATA_VOLUME}"
else
  echo "No named volume was found at /var/lib/postgresql/data; inspect the mount listing for a bind or anonymous mount."
fi
```

Use volume creation metadata, container timing, bootstrap timestamps, source revisions, and logs together. Do not label state “stale” from age alone.

### 11. Enumerate the actual initialization sources

Build the source-directory list explicitly and record absent optional directories:

```bash
SOURCE_DIRS=(docker/postgres/init db/ddl)

if [[ -d db/seed ]]; then
  SOURCE_DIRS+=(db/seed)
else
  echo "ABSENT OPTIONAL SOURCE DIRECTORY: db/seed"
fi

find "${SOURCE_DIRS[@]}" -type f \
  \( -name '*.sql' -o -name '*.sh' \) -print | sort
```

Record checksums to reveal identical SQL files at different paths:

```bash
find "${SOURCE_DIRS[@]}" -type f -name '*.sql' -print0 | \
  sort -z | xargs -0 shasum
```

Create a source-definition index:

```bash
rg -n -i --glob '*.sql' \
  '^[[:space:]]*CREATE[[:space:]]+(EXTENSION|SCHEMA|TABLE|VIEW|MATERIALIZED[[:space:]]+VIEW|FOREIGN[[:space:]]+TABLE)' \
  "${SOURCE_DIRS[@]}"
```

This index helps locate definitions; it is not proof of execution. Logs and initialization control flow determine which files actually ran.

### 12. Compare runtime state with repository sources deterministically

1. Use the catalog query from Step 7 as the runtime relation inventory.
2. Use the source enumeration, checksums, and definition index from Step 11 as the source inventory.
3. Use `docker/postgres/init/001_initialize.sh`, the resolved Compose mounts, and initialization logs to establish execution order and ownership.
4. For each missing or unexpected runtime object, locate its exact source references:

   ```bash
   OBJECT_NAME='<relation-or-schema-name>'
   rg -n -i --glob '*.sql' --fixed-strings "${OBJECT_NAME}" "${SOURCE_DIRS[@]}"
   ```

5. Open only files shown by execution evidence or object lookup. Do not require contributors to read every large DDL file when no discrepancy points to it.
6. If two source files are identical, report both paths and determine from control flow and logs whether one, both, or neither executes.

Classify each discrepancy as one of:

- wrong database or user;
- wrong schema or search path;
- initialization did not run;
- initialization ran more than once through overlapping mechanisms;
- initialization ran against an earlier repository version;
- persistent volume contains state from an earlier source revision;
- DDL failed partway through;
- source DDL and runtime schema have drifted;
- expected relation is not actually part of the current initialization path;
- no discrepancy found.

Do not classify persistent state as stale without lifecycle evidence. Do not classify initialization as failed merely because the latest restart did not rerun entrypoint scripts.

### 13. Stop before repair

Report findings before changing files or database state.

If repair is needed, route next to the appropriate skill:

- `skills/database/db-migration.md` only for an actual schema change;
- `skills/engineering/investigate-bug.md` for duplicate initialization, initialization ordering, or runtime failure;
- `skills/testing/docker-test.md` for full-stack verification;
- future `skills/database/reset-local-db.md` only when destructive reset is explicitly approved.

## Success Criteria

- The configured and live database targets are both recorded and compared.
- The active database, user, schema, and search path are known.
- Runtime extensions, schemas, and every supported relation type are recorded.
- Bootstrap evidence is evaluated for both presence and cardinality.
- Initialization logs include both wrapper and native-entrypoint execution evidence.
- Docker or permission failures cannot be mistaken for successful evidence collection.
- Initialization source paths, duplicate files, execution ownership, and optional absent directories are explicit.
- Persistent-volume and container lifecycle evidence are recorded before claiming stale state.
- Any discrepancy is classified with evidence.
- No data, schema, volume, or repository file is changed.
- The next repair workflow, if any, is named explicitly.

## Never

- Never infer that no tables exist from an unqualified `\dt` alone.
- Never append `|| true` to Docker, Compose, or PostgreSQL evidence commands.
- Never run `docker compose down -v` during inspection.
- Never drop schemas, databases, tables, or volumes.
- Never manually create missing relations as a diagnostic shortcut.
- Never claim initialization failed without checking logs, execution ownership, and persistent-volume behavior.
- Never claim a volume is stale from age alone.
- Never change the database target merely to make expected relations appear.
- Never load a repair skill until inspection identifies the owning defect layer.

## Report

Return:

- branch and explicit worktree state;
- resolved Compose configuration evidence;
- configured database target and application database URLs;
- live database, user, current schema, and search path;
- extensions found, versions, and missing requirements;
- schemas found, missing, and intentionally empty;
- relations grouped by schema and relation type;
- bootstrap version, smoke-row count, and smoke rows;
- initialization log evidence, including each observed execution path;
- PostgreSQL container and data-volume lifecycle evidence;
- initialization source files, checksums, and absent optional directories;
- runtime/source comparison;
- discrepancy classification;
- recommended next skill;
- unresolved uncertainty.
