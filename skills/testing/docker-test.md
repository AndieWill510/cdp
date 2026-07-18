---
name: docker-test
description: Build the local CDP stack, run its canonical test suite, verify PostgreSQL relations, and preserve diagnostic evidence.
inputs:
  - a non-main working branch
  - Docker Desktop running
outputs:
  - test results
  - container health and database verification
  - captured logs and unresolved failures
---

# Goal

Verify that a proposed CDP change works in the real local Docker Compose environment rather than only appearing correct in source code.

## Preconditions

1. Read and follow `AGENTS.md`.
2. Work from the repository root.
3. Confirm the active branch is not `main`.
4. Confirm Docker is available.
5. Do not discard unrelated working-tree changes.

## Procedure

1. Inspect repository state:

   ```bash
   git status --short
   git branch --show-current
   ```

2. Run the canonical test loop:

   ```bash
   make codex-test
   ```

3. If it fails, inspect the emitted test output and Docker logs.
4. Identify the root cause before editing.
5. Make the smallest coherent patch.
6. Rerun `make codex-test`.
7. Repeat only while each patch is evidence-based and remains within scope.

## Success Criteria

- Docker Compose configuration is valid.
- Required containers start and become healthy.
- The canonical test suite exits successfully.
- PostgreSQL contains the expected CDP relations.
- No secrets are introduced.
- Docker volumes remain intact.

## Never

- Never run `docker compose down -v` or `make down-volumes` unless explicitly instructed.
- Never force-push.
- Never commit or push unless explicitly instructed.
- Never bypass a failing test, health check, migration, or governance control merely to report success.
- Never declare completion when the canonical test loop still fails.

## Report

Return:

- branch inspected
- files read
- files changed
- commands run
- tests passed and failed
- database verification
- log locations or relevant excerpts
- remaining uncertainty
