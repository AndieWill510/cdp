# Demonstrated Capabilities

Status: Draft v0.1 — as of 2026-07-31

This document describes only capabilities that have cleared at least E2
(Structurally Tested) per [`README.md`](README.md). It contains no roadmap,
no aspirational content, and no RFC summary — for what is expected but not
yet demonstrated, see [`003-known-gaps.md`](003-known-gaps.md).

## Decision creation

A decision can be created through a live HTTP API (`POST /decisions`,
`cdp/api/decisions.py`) backed by a real Postgres database, and the
transaction that creates it also creates a workflow instance, a task, and
three audit events in the same commit. This is demonstrated by
`tests/test_decision_service.py::test_happy_path_creates_decision_workflow_task_and_three_audit_events`
and `tests/test_decision_api.py`, both confirmed passing against a live
`uvicorn` process and live Postgres service container in CI run `30542840497`
(`full-cdp-slice-tests` job, push to `main`, 2026-07-30T12:30:41Z).

## Challenge transitions

A decision can be challenged (`POST
/decisions/{registry_name}/{decision_id}/challenges`), enforcing the
transition rules encoded in `db/ddl/005-challenge-transition.sql`. Demonstrated
by `tests/test_challenge_service.py` and `tests/test_challenge_api.py`,
confirmed passing in the same CI run as above.

## Challenge adjudication

A challenge can be adjudicated (`POST
.../challenges/{challenge_id}/adjudications`), enforcing the constraints in
`db/ddl/007-challenge-adjudication.sql`. Demonstrated by
`tests/test_challenge_adjudication_service.py` and
`tests/test_challenge_adjudication_api.py`, confirmed passing in the same CI
run.

## Execution authorization and execution recording

A decision can be authorized for execution (`POST
.../execution-authorizations`) and the resulting execution can be recorded
(`POST .../execution-records`), including the constraint that an execution
record cannot be created without a prior authorization
(`db/ddl/008-execution-authorization.sql`, `db/ddl/009-execution-record.sql`).
Demonstrated by `tests/test_execution_authorization_service.py`,
`tests/test_execution_authorization_api.py`,
`tests/test_execution_record_service.py`, and
`tests/test_execution_record_api.py`, all confirmed passing against a fresh
checkout in CI run `30542840497`.

## Audit trail

Every one of the above operations writes to an append-only audit trail
(`cdp/core/repositories/audit.py`) inside the same database transaction as
the operation itself, and the ordering of those events is constrained by
`db/ddl/006-audit-event-ordering.sql`. This is demonstrated both structurally
(`tests/test_migration_006_audit_event_ordering.py`) and by direct assertion
in the decision-creation test named above.

## Workflow-rule enforcement (Nemawashi)

A decision cannot be created without an active workflow definition matching
its decision class — attempting otherwise raises `NoActiveWorkflowError`
(`cdp/core/services.py`). The underlying schema
(`db/ddl/003-nemawashi-workflow-rules.sql`,
`db/ddl/004-decision-class-workflow-seed.sql`) is demonstrated against a live
Postgres instance by
`tests/test_nemawashi_workflow_rules_ddl.py::NemawashiWorkflowRulesDDLPostgresSmokeTests`
and `tests/test_migration_004_decision_class_workflow_seed.py`, confirmed
passing in CI.

## Continuous integration itself

The repository's two-tier CI setup (`.github/workflows/cdp-ci.yml`) has been
observed to actually execute, not merely exist: `pr-guard` runs lint and
static tests on every PR push; `full-cdp-slice-tests` provisions a real
`pgvector/pgvector:pg16` Postgres service container, applies all DDL under
`db/ddl/`, starts a real `uvicorn cdp.api.main:app` process, and runs the API
round-trip suite against it. Run `30542840497` (push to `main`,
2026-07-30T12:30:41Z) shows both jobs completed with conclusion `success`.

## RFC index/manifest verification

A second, independent CI workflow (`.github/workflows/rfc-index-integrity.yml`)
executes `scripts/verify_rfc_index.py` against the contents of `rfc/` on
every push or PR touching that directory. This is a genuinely executing
consistency check over the RFC layer, distinct from the RFC content itself.

## Local Docker stack

A local multi-service stack (`docker/docker-compose.yml`: `cdp-api`,
`cdp-worker`, `cdp-redis`, `cdp-localstack`, `cdp-postgres` with `pgvector`,
`cdp-qdrant`) can be brought up and remain healthy over an extended period.
Directly observed via `docker ps` on 2026-07-31: `cdp-postgres`, `cdp-redis`,
and `cdp-localstack` reporting `healthy` after 12 days of uptime, `cdp-api`
`healthy` after 45 hours. This demonstrates the infrastructure composition
runs; it does not by itself demonstrate any governance-step logic (see the
per-step entries above and in [`000-current-state.md`](000-current-state.md)
for that).
