# CDP Engineering Instructions

## Project

CDP is the Constitutional Decision Plane.

The core decision lifecycle is:

Propose → Challenge → Test → Adjudicate → Legitimize → Execute → Record → Improve

Preserve auditability, contestability, explicit state transitions, and human oversight. Do not bypass governance controls merely to make tests pass.

## Repository Safety

- Work only within this repository.
- Never commit directly to `main`.
- Never force-push.
- Do not delete Docker volumes unless explicitly instructed.
- Do not run destructive database commands unless explicitly instructed.
- Do not modify secrets or commit `.env` files.
- Before changing architecture, identify the relevant RFCs and explain any conflict or schema drift.
- Prefer small, reviewable patches over broad rewrites.
- Do not overwrite unrelated uncommitted work.

## Before Editing

Run:

```bash
git status --short
git branch --show-current
```

If the current branch is `main`, stop and ask for a feature branch. If unrelated changes are present, preserve them and limit the patch to the requested scope.

## Docker

The canonical Compose file is:

```bash
docker/docker-compose.yml
```

Use repository-level commands where possible:

```bash
make up-build
make ps
make logs
make down
```

`make down` preserves volumes. Never run `make down-volumes`, `make reset-local`, `docker compose down -v`, or equivalent destructive commands unless explicitly instructed.

The local services are:

- `cdp-api`
- `cdp-worker`
- `postgres`
- `qdrant`
- `redis`
- `localstack`

## Canonical Codex Test Loop

For implementation and repair work, run:

```bash
bash scripts/codex_test_loop.sh
```

Pass pytest arguments after `--` when narrowing the test scope:

```bash
bash scripts/codex_test_loop.sh -- tests/test_db_ddl_runtime.py -q
```

The test loop must:

1. confirm Git and branch context;
2. validate Docker Compose configuration;
3. build and start the local stack headlessly;
4. wait for the API and PostgreSQL health checks;
5. run `scripts/test_suite.sh`;
6. verify that the `cdp` database contains user tables;
7. capture service logs whether tests pass or fail;
8. preserve Docker volumes and leave the stack running for inspection.

A task is not complete merely because code was written. Relevant tests must pass, services must remain healthy, and database state must be verified.

## Database

The local PostgreSQL database is:

- host inside Compose: `postgres`
- database: `cdp`
- user: `cdp`
- schema: `public`, unless a migration explicitly establishes another schema

Before assuming migrations failed:

1. confirm the target database and active schema;
2. inspect `docker/docker-compose.yml`;
3. inspect `docker/postgres/init/`;
4. inspect container logs;
5. verify that application and initialization code use the same database URL;
6. remember that `/docker-entrypoint-initdb.d` runs only when the Postgres data directory is first initialized.

Do not manually create application tables merely to make a test pass. Repair the migration or initialization path instead.

## Testing Strategy

- Run the narrowest relevant tests first.
- Run the broader suite after the narrow tests pass.
- Treat lint findings as evidence; do not silence them without understanding the cause.
- Inspect logs for hidden startup, migration, or dependency failures.
- Prefer deterministic tests over timing-based sleeps.
- Do not weaken assertions simply to obtain a green result.

## Git and Reporting

Do not commit or push unless explicitly requested.

After editing, report:

```bash
git diff --stat
git diff
```

The final report must state:

- files read;
- files changed;
- commands run;
- tests passed and failed;
- Docker service health;
- database verification;
- unresolved uncertainty.

## Definition of Done

A change is complete only when:

- the implementation is present;
- relevant tests pass;
- Docker services remain healthy;
- migrations and database initialization are consistent;
- no secrets are introduced;
- documentation changes accompany behavior changes;
- verification evidence is reported truthfully.
