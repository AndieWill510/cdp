# Test Matrix

Status: Draft v0.1 — as of 2026-08-03, post-merge state reflecting main `199c934` (sessions 020-032 merged; 027-032 closed as the Identity/Attestation/Authority/Authentication sequence -- see docs/session-027-032-identity-authority-closure.md)

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
- `tests/authority/`
- `tests/execution/`
- `tests/identify_attest_standing/`
- `tests/migration/`
- `tests/nemawashi/`
- `tests/misc/`
- `tests/standing/`
- `tests/universal_attestation/`

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
| Identify (Actor Registry / Identity Claim) | `tests/migration/test_migration_010_identity_and_attestation.py::Migration010StaticTests` | `tests/identify_attest_standing/test_actor_service.py`; `tests/identify_attest_standing/test_identity_claim_service.py`; `tests/migration/test_migration_010_identity_and_attestation.py::Migration010PostgresSmokeTests` | `tests/identify_attest_standing/test_identity_attestation_api.py` (actor/claim portions) | CI job `full-cdp-slice-tests`, run `30704929899` on commit `f8ae3d0` (v0.2-corrected code), re-confirmed unchanged by run `30705068165` on PR #41's actual merged head `46afc46` | Healthy | `db/ddl/010-identity-and-attestation.sql` | Includes the anti-delete trigger actually firing (a real `DELETE` attempt raising, not just DDL text inspection), full supersession/denial-preservation coverage, and (v0.2) that an arbitrary registered actor or a self-recognizing claimant is rejected with `RecognitionAuthorityRequired`/`SelfRecognitionForbidden`. |
| Attest (Attestation Record) | `tests/migration/test_migration_010_identity_and_attestation.py::Migration010StaticTests` | `tests/identify_attest_standing/test_attestation_service.py`; `tests/migration/test_migration_010_identity_and_attestation.py::Migration010PostgresSmokeTests` | `tests/identify_attest_standing/test_identity_attestation_api.py` (attested-decision portions) | Same CI run as the Identify row above, success | Healthy | `db/ddl/010-identity-and-attestation.sql` | Covers the fail-closed proof path against decision creation: unknown actor, inactive actor, unrecognized claim, wrong-scope claim, claim-belongs-to-different-actor, and forced-failure rollback, each asserting zero rows persisted; plus (v0.2) that the attestor and the decision's subject may independently differ and both remain correctly, separately attributed. |
| Standing -- Constitutional Affected-Party, Challenge stage (RFC-CDP-033) | `tests/migration/test_migration_015_standing_and_recusal.py::Migration015StaticTests` | `tests/standing/test_standing_claim_service.py`; `tests/migration/test_migration_015_standing_and_recusal.py::Migration015PostgresSmokeTests` | `tests/standing/test_standing_claim_api.py` | CI job `full-cdp-slice-tests`, run `31183454972`, PR #53 head commit `44d3b6c` (post narrowed-deferral correction), success | Healthy | `db/ddl/015-standing-and-recusal.sql` | Session 035. Includes both forbid-delete-and-forbid-update triggers on `standing_claim`/`standing_recognition_determination` actually firing (real `DELETE`/`UPDATE` attempts, not DDL text inspection), the DB-level minimal-sufficiency `CHECK` rejecting a claim missing all basis fields, self-determination and non-authority-determination both rejected, a second determination on the same claim rejected, and the load-bearing proof that a pending, minimally sufficient claim (no determination yet) permits raising a Challenge. Pre-merge review correction: `narrow_standing_claim` and its route were removed (this table has no `outcome_scope` column, so a `narrowed` determination would have been enforcement-indistinguishable from `recognized`); only `recognized`/`denied` are reachable now, and tests were added confirming the function's absence, the database's own rejection of a direct `narrowed` insert, and the `/narrow` route's 404 -- see `docs/session-035-affected-party-standing-challenge.md` §2.1. |
| Standing -- every other type; Recusal (RFC-CDP-033) | | | | | N/A | | No code, no tests. Evidence-Custodian, Record-Keeper, Delegated, Emergency, Repair, Appeal, and AI Functional Standing, and Recusal in its entirety (§7, §10), remain unimplemented after session 035 -- see that session's doc for the explicit non-goals list. |
| Authority and Delegation (RFC-CDP-032), SS19 Minimal Compliance | `tests/migration/test_migration_011_authority_and_delegation.py::Migration011StaticTests` | `tests/authority/test_authority_grant_service.py`; `tests/migration/test_migration_011_authority_and_delegation.py::Migration011PostgresSmokeTests`; 6 authority-gate cases added to `tests/identify_attest_standing/test_attestation_service.py` | `tests/authority/test_authority_grant_api.py`; 3 authority-gate cases added to `tests/identify_attest_standing/test_identity_attestation_api.py` | CI job `full-cdp-slice-tests`, run `30707515976`, PR #43 head commit `b29e75a`, success | Healthy | `db/ddl/011-authority-and-delegation.sql` | Includes the anti-delete trigger on `authority_grant` actually firing, wildcard-vs-exact scope matching, and expired/revoked grants both failing closed. |
| Universal Attestation (RFC-CDP-031 §2) — challenge/adjudication/execution-authorization/execution-record | `tests/migration/test_migration_012_universal_attestation.py::Migration012StaticTests` | `tests/universal_attestation/test_universal_attestation_service.py`; `tests/migration/test_migration_012_universal_attestation.py::Migration012PostgresSmokeTests` | `tests/universal_attestation/test_universal_attestation_api.py` | CI job `full-cdp-slice-tests`, run `30729249209`, commit `2c9d5fb` (PR #44's current head, after rebase onto main post-PR#43-merge; superseding an earlier run `30729045854` on pre-rebase commit `4d0e7b8`), success | Healthy | `db/ddl/012-universal-attestation.sql` | Reuses the shared actor/claim/authority-check helpers `attest_and_create_decision` was refactored onto (session 027/028's own rows). Includes a forced-failure rollback case for challenge-raising, matching the pattern in the other attested proof paths. |
| Identity Claim Scope (richer purpose/scope semantics) | `tests/migration/test_migration_013_identity_claim_scope.py::Migration013StaticTests` | `tests/migration/test_migration_013_identity_claim_scope.py::Migration013PostgresSmokeTests`; 4 new cases in `tests/identify_attest_standing/test_identity_claim_service.py`; 3 new cases in `test_attestation_service.py`; 2 new cases in `tests/universal_attestation/test_universal_attestation_service.py` | 2 new cases in `tests/identify_attest_standing/test_identity_attestation_api.py` | CI job `full-cdp-slice-tests`, run `30730450515`, commit `77f29c9`, success | Healthy | `db/ddl/013-identity-claim-scope.sql` | Mirrors `authority_grant`'s two-level scope model; enforced once in the shared `_check_claim_recognized_and_scoped` helper, so all five `attest_and_*` proof paths gained the check simultaneously — covered here by testing it against both `attest_and_create_decision` and `attest_and_raise_challenge`, not all five individually (the helper is shared code, not five independent implementations). |
| Caller Authentication (bearer-token binding) | `tests/migration/test_migration_014_caller_authentication.py::Migration014StaticTests`; `tests/migration/test_dev_seed_caller_authentication_tokens.py::DevSeedCallerAuthenticationTokensStaticTests` | `tests/migration/test_migration_014_caller_authentication.py::Migration014PostgresSmokeTests`; `tests/migration/test_migration_014_caller_authentication.py::Migration014IsolatedDatabaseTests`; `tests/migration/test_dev_seed_caller_authentication_tokens.py::DevSeedCallerAuthenticationTokensPostgresSmokeTests`; 8 cases in `tests/identify_attest_standing/test_actor_service.py::CallerAuthenticationTests` | every existing case in `test_identity_attestation_api.py`, `test_authority_grant_api.py`, `test_universal_attestation_api.py` now presents a token; new cases across those three files covering missing/mismatched tokens and token_hash redaction | CI job `full-cdp-slice-tests`, run `30779064311` on merge commit `199c934` (main, push-triggered) -- superseding the PR-head citation `30778872564`/`7766879` now that PR #49 is merged | Healthy | `db/ddl/014-caller-authentication.sql`; `db/seed/dev-caller-authentication-tokens.sql` | `verify_bearer_token` is a standalone check, never called from inside any other service function, so it required updating every existing API test that hits a now-protected route (not a new-tests-only addition) rather than just adding coverage alongside untouched tests. Pre-merge review (PR #48) moved privileged token seeding out of the canonical migration path into `db/seed/` and required a redaction fix to the revoke response. Post-merge review added `Migration014IsolatedDatabaseTests`, which proves the zero-privileged-tokens invariant against a genuinely isolated scratch database in CI, closing the gap where that invariant was previously only manually verified -- see `evidence/003-known-gaps.md`'s Caller Authentication section. |
| Appeals / Repair (RFC-CDP-070 series) | | | | | N/A | | No code, no tests. |
| Worker / queue consumption | | | | | N/A | `cdp/worker/main.py` | Process runs (no-op loop, per its own docstring) but there is nothing for a test to exercise. |
| Self-canonicalizing ingestion | `tests/misc/test_self_canonicalizing_ingestion.py` (all classes; no live dependency required) | | | | Known gaps | | The tested code is a reference implementation embedded in the test file itself, not a `cdp/` module — see [`000-current-state.md`](000-current-state.md#execution-substrate). A passing suite here provides zero coverage of any production ingestion path, because none exists. Its fixture-lookup path was also broken by the 2026-07-31 reorg and fixed the same day (commit `7b6efae`). |
| Postgres init contract | `tests/db/test_postgres_init_contract.py::test_postgres_init_files_have_single_ordered_owner`; `::test_bootstrap_sql_enforces_idempotent_smoke_marker` | `tests/db/test_postgres_init_contract.py::test_postgres_bootstrap_runtime_marker_is_unique` | | CI job `full-cdp-slice-tests` runs the Runtime Test listed | Healthy | `docker/postgres/init/01-init-cdp.sql` | Infra contract test, not a governance step. Repo-root path computation broken and fixed alongside the other migration tests on 2026-07-31 (commit `7b6efae`). |
| Docker build/runtime verification | | | | | Not exercised in CI | `tests/build_verification/test_build_verification.py` | 11 real checks against a running Docker stack (API health, Postgres extensions, Redis, Qdrant, LocalStack S3/SQS/EventBridge/DynamoDB/SSM/Secrets). No CI job invokes `test_build_verification.py` — it can only be run manually against a local stack, so a regression here would go undetected until someone happens to run it by hand. |
| RFC index/manifest integrity | | `scripts/verify_rfc_index.py` via `make verify-rfc-index` | | CI workflow `rfc-index-integrity.yml` | Known gaps | | Not a `pytest` test; a standalone verification script. Running it directly on 2026-07-31 (`python3 scripts/verify_rfc_index.py`) shows it emits roughly two dozen `WARN`-level lines — manifest/header status drift (e.g. `RFC-CDP-053` manifest says "Draft", header says "Draft v0.1") and canonical files entirely absent from the manifest (e.g. `RFC-CDP-063` through `RFC-CDP-066`, `RFC-CDP-076`, `RFC-CDP-077`) — yet still exits with "RFC index verification passed." The check is real and does run in CI, but its warnings are non-fatal, so this class of drift can accumulate indefinitely without failing the build. |
