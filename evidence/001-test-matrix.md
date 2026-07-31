# Test Matrix

Status: Draft v0.1 — as of 2026-07-31

This matrix lists, for each governance step or capability, which categories
of test actually exist in the repository. A cell is left blank when no
corresponding test file/artifact was found — blank means "unknown value
requiring no inference," not "assumed absent." Do not fill a blank cell from
an RFC or architecture document; fill it only when a corresponding test
artifact is found.

Column definitions:

- **Static Tests** — run without a live dependency (no DB, no server). Typically named `*StaticTests` in this repo.
- **Runtime Tests** — run against a live local dependency (e.g. Postgres) but not through the API. Typically named `*PostgresSmokeTests` or a bare service test requiring `CDP_TEST_DATABASE_URL`.
- **API Tests** — HTTP round-trip tests against a running server, gated by `CDP_TEST_API_URL`.
- **Integration Tests** — the specific CI job that runs Static/Runtime/API tests together against a fresh checkout, fresh Postgres, and fresh `uvicorn` process.

## Test folder structure

The repository now organizes Python test artifacts into per-topic folders
directly under `tests/`. Folders containing test files:

- `tests/build_verification/`
- `tests/challenge/`
- `tests/db/`
- `tests/decision/`
- `tests/execution/`
- `tests/migration/`
- `tests/nemawashi/`
- `tests/misc/`

Folders that exist as placeholders (containing only `.gitkeep`, no test files
yet) for governance steps with no code or coverage:

- `tests/adjudicate/`
- `tests/appeals_repair/`
- `tests/docker_build_verification/`
- `tests/execute_authorization/`
- `tests/execute_record/`
- `tests/identify_attest_standing/`
- `tests/learn/`
- `tests/legitimize/`
- `tests/postgres_init_contract/`
- `tests/propose/`
- `tests/record/`
- `tests/rfc_index_manifest_integrity/`
- `tests/self_canonicalizing_ingestion/`
- `tests/test/`
- `tests/worker_queue/`

These placeholder folders are intentionally present even though no test
Python scripts exist in them yet, so the matrix can explicitly record which
governance steps lack coverage rather than omitting them.

| Governance Step | Static Tests | Runtime Tests | API Tests | Integration Tests | Evidence | Notes |
|---|---|---|---|---|---|---|
| Nemawashi / workflow rules | `tests/nemawashi/test_nemawashi_workflow_rules_ddl.py::NemawashiWorkflowRulesDDLStaticTests`; `tests/migration/test_migration_004_decision_class_workflow_seed.py::Migration004StaticTests` | `tests/nemawashi/test_nemawashi_workflow_rules_ddl.py::NemawashiWorkflowRulesDDLPostgresSmokeTests`; `tests/migration/test_migration_004_decision_class_workflow_seed.py::Migration004PostgresSmokeTests` | | CI job `full-cdp-slice-tests` runs the Runtime Tests listed | `.github/workflows/cdp-ci.yml` | No dedicated API surface for this step; exercised as a precondition of decision creation. |
| Propose (decision creation) | `tests/migration/test_migration_004_decision_class_workflow_seed.py::Migration004StaticTests` | `tests/decision/test_decision_service.py` (requires `CDP_TEST_DATABASE_URL`) | `tests/decision/test_decision_api.py` (requires `CDP_TEST_API_URL`) | CI job `full-cdp-slice-tests`, run `30542840497`, success | `cdp/api/decisions.py`, `cdp/core/services.py` | |
| Challenge | `tests/migration/test_migration_005_challenge_transition.py::Migration005StaticTests` | `tests/challenge/test_challenge_service.py`; `tests/migration/test_migration_005_challenge_transition.py::Migration005PostgresSmokeTests` | `tests/challenge/test_challenge_api.py` | CI job `full-cdp-slice-tests`, run `30542840497`, success | `db/ddl/005-challenge-transition.sql` | |
| Test (protocol step) | | | | | | No test artifacts exist for this governance step; no code implements it. |
| Adjudicate | `tests/migration/test_migration_007_challenge_adjudication.py::Migration007StaticTests` | `tests/challenge/test_challenge_adjudication_service.py`; `tests/migration/test_migration_007_challenge_adjudication.py::Migration007PostgresSmokeTests` | `tests/challenge/test_challenge_adjudication_api.py` | CI job `full-cdp-slice-tests`, run `30542840497`, success | `db/ddl/007-challenge-adjudication.sql` | |
| Legitimize | | | | | | No code, no tests. |
| Execute (authorization) | `tests/migration/test_migration_008_execution_authorization.py::Migration008StaticTests` | `tests/execution/test_execution_authorization_service.py`; `tests/migration/test_migration_008_execution_authorization.py::Migration008PostgresSmokeTests` | `tests/execution/test_execution_authorization_api.py` | CI job `full-cdp-slice-tests`, run `30542840497`, success | `db/ddl/008-execution-authorization.sql` | |
| Execute (record) | `tests/migration/test_migration_009_execution_record.py::Migration009StaticTests` | `tests/execution/test_execution_record_service.py`; `tests/migration/test_migration_009_execution_record.py::Migration009PostgresSmokeTests` | `tests/execution/test_execution_record_api.py` | CI job `full-cdp-slice-tests`, run `30542840497`, success | `db/ddl/009-execution-record.sql` | A local ad hoc `pytest` run on 2026-07-31 against a stale, long-running local `cdp-api` container showed 2 failures here; CI (fresh build) passes. See [`000-current-state.md`](000-current-state.md#local-vs-ci-discrepancy-documented-not-resolved-here). |
| Record (audit trail) | | `tests/migration/test_migration_006_audit_event_ordering.py::Migration006PostgresSmokeTests`; audit assertions embedded in `tests/decision/test_decision_service.py::test_happy_path_creates_decision_workflow_task_and_three_audit_events` | | CI job `full-cdp-slice-tests` runs the Runtime Tests listed | `db/ddl/006-audit-event-ordering.sql`, `cdp/core/repositories/audit.py` | No dedicated static test class found; no route exposes the audit trail for read, so no API Tests entry. |
| Learn | | | | | | No code, no tests. |
| Identify / Attest / Standing | | | | | | No code, no tests. |
| Appeals / Repair (RFC-CDP-070 series) | | | | | | No code, no tests. |
| Worker / queue consumption | | | | | `cdp/worker/main.py` | Process runs (no-op loop, per its own docstring) but there is nothing for a test to exercise. |
| Self-canonicalizing ingestion | `tests/misc/test_self_canonicalizing_ingestion.py` (all classes; no live dependency required) | | | | | The tested code is a reference implementation embedded in the test file itself, not a `cdp/` module — see [`000-current-state.md`](000-current-state.md#execution-substrate). |
| Postgres init contract | `tests/db/test_postgres_init_contract.py::test_postgres_init_files_have_single_ordered_owner`; `::test_bootstrap_sql_enforces_idempotent_smoke_marker` | `tests/db/test_postgres_init_contract.py::test_postgres_bootstrap_runtime_marker_is_unique` | | CI job `full-cdp-slice-tests` runs the Runtime Test listed | `docker/postgres/init/01-init-cdp.sql` | Infra contract test, not a governance step. |
| Docker build/runtime verification | | | | | `tests/build_verification/test_build_verification.py` | 11 checks against a running Docker stack (API health, Postgres extensions, Redis, Qdrant, LocalStack S3/SQS/EventBridge/DynamoDB/SSM/Secrets). Not run by either CI workflow — no CI job invokes `test_build_verification.py`; it appears to be a local/manual smoke test only. |
| RFC index/manifest integrity | | `scripts/verify_rfc_index.py` via `make verify-rfc-index` | | CI workflow `rfc-index-integrity.yml` | | Not a `pytest` test; a standalone verification script. Included here because it is a genuine, executing check with CI evidence, even though it is repository tooling rather than a CDP governance step. |
