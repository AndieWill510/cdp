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
- **Test Suite Health** — a separate axis from the four columns above. Those
  columns answer "does a test of this kind exist" (a capability claim);
  this column answers "is that test suite itself trustworthy" (see
  [`README.md`](README.md#what-an-evidence-level-does-not-claim)). One of:
  - **Healthy** — tests exist, run in CI, and no specific blind spot is
    currently known.
  - **Known gaps** — tests exist but have a specific, named blind spot
    (cited in the Notes column).
  - **Not exercised in CI** — a real test file exists with real assertions,
    but no CI job invokes it, so it can silently rot without anyone
    noticing.
  - **N/A** — no code and/or no tests exist for this row, so there is
    nothing to assess health of.

A row being fully populated across the first four columns is a capability
claim, not a thoroughness claim — a row can have every column filled and
still land on "Known gaps" in the health column. Do not infer Test Suite
Health from the presence of a citation; it is assessed and cited
independently in the Notes column.

## Test folder structure

The repository now organizes Python test artifacts into per-topic folders
directly under `tests/`. Folders containing test files:

- `tests/build_verification/`
- `tests/challenge/`
- `tests/db/`
- `tests/decision/`
- `tests/execution/`
- `tests/identify_attest_standing/`
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

| Governance Step | Static Tests | Runtime Tests | API Tests | Integration Tests | Test Suite Health | Evidence | Notes |
|---|---|---|---|---|---|---|---|
| Nemawashi / workflow rules | `tests/nemawashi/test_nemawashi_workflow_rules_ddl.py::NemawashiWorkflowRulesDDLStaticTests`; `tests/migration/test_migration_004_decision_class_workflow_seed.py::Migration004StaticTests` | `tests/nemawashi/test_nemawashi_workflow_rules_ddl.py::NemawashiWorkflowRulesDDLPostgresSmokeTests`; `tests/migration/test_migration_004_decision_class_workflow_seed.py::Migration004PostgresSmokeTests` | | CI job `full-cdp-slice-tests` runs the Runtime Tests listed | Healthy | `.github/workflows/cdp-ci.yml` | No dedicated API surface for this step; exercised as a precondition of decision creation. This file's repo-root path computation was broken by the 2026-07-31 test-folder reorg and fixed the same day (commit `7b6efae`); currently passing. |
| Propose (decision creation) | `tests/migration/test_migration_004_decision_class_workflow_seed.py::Migration004StaticTests` | `tests/decision/test_decision_service.py` (requires `CDP_TEST_DATABASE_URL`) | `tests/decision/test_decision_api.py` (requires `CDP_TEST_API_URL`) | CI job `full-cdp-slice-tests`, run `30637092898`, success | Healthy | `cdp/api/decisions.py`, `cdp/core/services.py` | |
| Challenge | `tests/migration/test_migration_005_challenge_transition.py::Migration005StaticTests` | `tests/challenge/test_challenge_service.py`; `tests/migration/test_migration_005_challenge_transition.py::Migration005PostgresSmokeTests` | `tests/challenge/test_challenge_api.py` | CI job `full-cdp-slice-tests`, run `30637092898`, success | Healthy | `db/ddl/005-challenge-transition.sql` | Includes a forced-failure test asserting the audit event is rolled back with the rest of the transaction, not just the happy path. |
| Test (protocol step) | | | | | N/A | | No test artifacts exist for this governance step; no code implements it. |
| Adjudicate | `tests/migration/test_migration_007_challenge_adjudication.py::Migration007StaticTests` | `tests/challenge/test_challenge_adjudication_service.py`; `tests/migration/test_migration_007_challenge_adjudication.py::Migration007PostgresSmokeTests` | `tests/challenge/test_challenge_adjudication_api.py` | CI job `full-cdp-slice-tests`, run `30637092898`, success | Healthy | `db/ddl/007-challenge-adjudication.sql` | Same rollback-on-failure coverage pattern as Challenge. |
| Legitimize | | | | | N/A | | No code, no tests. |
| Execute (authorization) | `tests/migration/test_migration_008_execution_authorization.py::Migration008StaticTests` | `tests/execution/test_execution_authorization_service.py`; `tests/migration/test_migration_008_execution_authorization.py::Migration008PostgresSmokeTests` | `tests/execution/test_execution_authorization_api.py` | CI job `full-cdp-slice-tests`, run `30637092898`, success | Healthy | `db/ddl/008-execution-authorization.sql` | `test_happy_path_completes_review_task_advances_workflow_and_orders_audit_events` asserts audit-event ordering explicitly, not just presence. |
| Execute (record) | `tests/migration/test_migration_009_execution_record.py::Migration009StaticTests` | `tests/execution/test_execution_record_service.py`; `tests/migration/test_migration_009_execution_record.py::Migration009PostgresSmokeTests` | `tests/execution/test_execution_record_api.py` | CI job `full-cdp-slice-tests`, run `30637092898`, success | Known gaps | `db/ddl/009-execution-record.sql` | A local ad hoc `pytest` run on 2026-07-31 against a stale, long-running local `cdp-api` container showed 2 failures here; CI (fresh build) passes. See [`000-current-state.md`](000-current-state.md#local-vs-ci-discrepancy-documented-not-resolved-here). The gap: nothing in the suite itself detects or warns that `CDP_TEST_API_URL` may be pointing at a stale container — a developer has to notice the discrepancy independently, as happened here. |
| Record (audit trail) | | `tests/migration/test_migration_006_audit_event_ordering.py::Migration006PostgresSmokeTests`; audit-event content and rollback assertions embedded directly in `tests/decision/test_decision_service.py`, `tests/challenge/test_challenge_service.py`, `tests/challenge/test_challenge_adjudication_service.py`, `tests/execution/test_execution_authorization_service.py`, and `tests/execution/test_execution_record_service.py` (each queries `cdp_audit.event_log` directly and/or forces an audit-write failure to assert the rest of the transaction rolls back) | | CI job `full-cdp-slice-tests` runs the Runtime Tests listed | Healthy | `db/ddl/006-audit-event-ordering.sql`, `cdp/core/repositories/audit.py` | Corrected 2026-07-31: an earlier version of this row understated coverage as "only asserted by the decision-creation test." All five mutating service tests assert on `cdp_audit.event_log` directly. No route exposes the audit trail for external read, so there is still no API Tests entry. |
| Learn | | | | | N/A | | No code, no tests. |
| Identify (Actor Registry / Identity Claim) | `tests/migration/test_migration_010_identity_and_attestation.py::Migration010StaticTests` | `tests/identify_attest_standing/test_actor_service.py`; `tests/identify_attest_standing/test_identity_claim_service.py`; `tests/migration/test_migration_010_identity_and_attestation.py::Migration010PostgresSmokeTests` | `tests/identify_attest_standing/test_identity_attestation_api.py` (actor/claim portions) | Passing locally as of 2026-08-01 on the v0.2-corrected commit; fresh CI run pending (prior run `30677856180` validated pre-correction behavior only) -- see Notes | Healthy | `db/ddl/010-identity-and-attestation.sql` | Includes the anti-delete trigger actually firing (a real `DELETE` attempt raising, not just DDL text inspection), full supersession/denial-preservation coverage, and (v0.2) that an arbitrary registered actor or a self-recognizing claimant is rejected with `RecognitionAuthorityRequired`/`SelfRecognitionForbidden`. |
| Attest (Attestation Record) | `tests/migration/test_migration_010_identity_and_attestation.py::Migration010StaticTests` | `tests/identify_attest_standing/test_attestation_service.py`; `tests/migration/test_migration_010_identity_and_attestation.py::Migration010PostgresSmokeTests` | `tests/identify_attest_standing/test_identity_attestation_api.py` (attested-decision portions) | Same status as the Identify row above -- passing locally, fresh CI run pending | Healthy | `db/ddl/010-identity-and-attestation.sql` | Covers the fail-closed proof path against decision creation: unknown actor, inactive actor, unrecognized claim, wrong-scope claim, claim-belongs-to-different-actor, and forced-failure rollback, each asserting zero rows persisted; plus (v0.2) that the attestor and the decision's subject may independently differ and both remain correctly, separately attributed. |
| Standing and Recusal (RFC-CDP-033) | | | | | N/A | | No code, no tests. Not implemented by the Identity and Attestation slice -- see Non-Goals in `docs/session-027-identity-and-attestation.md`. |
| Appeals / Repair (RFC-CDP-070 series) | | | | | N/A | | No code, no tests. |
| Worker / queue consumption | | | | | N/A | `cdp/worker/main.py` | Process runs (no-op loop, per its own docstring) but there is nothing for a test to exercise. |
| Self-canonicalizing ingestion | `tests/misc/test_self_canonicalizing_ingestion.py` (all classes; no live dependency required) | | | | Known gaps | | The tested code is a reference implementation embedded in the test file itself, not a `cdp/` module — see [`000-current-state.md`](000-current-state.md#execution-substrate). A passing suite here provides zero coverage of any production ingestion path, because none exists. Its fixture-lookup path was also broken by the 2026-07-31 reorg and fixed the same day (commit `7b6efae`). |
| Postgres init contract | `tests/db/test_postgres_init_contract.py::test_postgres_init_files_have_single_ordered_owner`; `::test_bootstrap_sql_enforces_idempotent_smoke_marker` | `tests/db/test_postgres_init_contract.py::test_postgres_bootstrap_runtime_marker_is_unique` | | CI job `full-cdp-slice-tests` runs the Runtime Test listed | Healthy | `docker/postgres/init/01-init-cdp.sql` | Infra contract test, not a governance step. Repo-root path computation broken and fixed alongside the other migration tests on 2026-07-31 (commit `7b6efae`). |
| Docker build/runtime verification | | | | | Not exercised in CI | `tests/build_verification/test_build_verification.py` | 11 real checks against a running Docker stack (API health, Postgres extensions, Redis, Qdrant, LocalStack S3/SQS/EventBridge/DynamoDB/SSM/Secrets). No CI job invokes `test_build_verification.py` — it can only be run manually against a local stack, so a regression here would go undetected until someone happens to run it by hand. |
| RFC index/manifest integrity | | `scripts/verify_rfc_index.py` via `make verify-rfc-index` | | CI workflow `rfc-index-integrity.yml` | Known gaps | | Not a `pytest` test; a standalone verification script. Running it directly on 2026-07-31 (`python3 scripts/verify_rfc_index.py`) shows it emits roughly two dozen `WARN`-level lines — manifest/header status drift (e.g. `RFC-CDP-053` manifest says "Draft", header says "Draft v0.1") and canonical files entirely absent from the manifest (e.g. `RFC-CDP-063` through `RFC-CDP-066`, `RFC-CDP-076`, `RFC-CDP-077`) — yet still exits with "RFC index verification passed." The check is real and does run in CI, but its warnings are non-fatal, so this class of drift can accumulate indefinitely without failing the build. |
