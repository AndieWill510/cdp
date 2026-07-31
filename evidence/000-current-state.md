# Current State

Status: Draft v0.1 — as of 2026-07-31

This document classifies each governance step against the evidence levels
defined in [`README.md`](README.md). Classification follows the *strongest
artifact currently available*, not the intent expressed in the corresponding
RFC or architecture document. Where no artifact exists, this document says so
explicitly rather than inferring capability from specification.

Governance-step names follow the RFC-CDP-04x protocol band
(`rfc/RFC-CDP-040-*` through `RFC-CDP-048-*`), plus the RFC-CDP-03x identity
band and RFC-CDP-07x appeals band, since those are the bands that name
discrete lifecycle steps. This is a naming convenience for this document, not
a claim that the code implements those RFCs' contents.

## Legend

- **Not Implemented** — no code in a canonical path (`cdp/`).
- **Implemented (E1)** — code exists in `cdp/`, no test exercises it.
- **Structurally Tested (E2)** — tested without a live dependency.
- **Runtime Tested (E3)** — tested against a live local dependency (e.g. Postgres), not through the full API.
- **Integration Tested (E4)** — tested through the live API against a live database, confirmed passing in CI.
- **Production Demonstrated (E5)** — observed operating in production.

## Identity and Standing (RFC-CDP-030 series)

| Step | Classification | Evidence |
|---|---|---|
| Identify (RFC-CDP-030) | Not Implemented | No authentication/identity code found under `cdp/`. `README-control-plane-v0.1.md` states the dormant `src/cdp_control_plane` prototype has "No auth." |
| Attest (RFC-CDP-031) | Not Implemented | No evidence currently available. |
| Standing and Recusal (RFC-CDP-033) | Not Implemented | No evidence currently available. |

## Decision Lifecycle (RFC-CDP-040–048)

| Step | Classification | Evidence |
|---|---|---|
| Nemawashi (RFC-CDP-040) — workflow rules | Runtime Tested (E3) | DDL: `db/ddl/003-nemawashi-workflow-rules.sql`, `db/ddl/004-decision-class-workflow-seed.sql`. Repository: `cdp/core/repositories/workflows.py`. Tests: `tests/nemawashi/test_nemawashi_workflow_rules_ddl.py` (`NemawashiWorkflowRulesDDLStaticTests` run in CI job `pr-guard`; `NemawashiWorkflowRulesDDLPostgresSmokeTests` run against a live Postgres service container in CI job `full-cdp-slice-tests`, `.github/workflows/cdp-ci.yml`). No dedicated API route exposes Nemawashi as a standalone protocol step — it is consumed internally when a decision is created (`NoActiveWorkflowError` in `cdp/core/services.py`), so it has not cleared E4 in its own right. |
| Propose (RFC-CDP-041) — decision creation | Integration Tested (E4) | Route: `POST /decisions` (`cdp/api/decisions.py`). Service: `create_decision_with_workflow` (`cdp/core/services.py`, described in its own docstring as "the smallest executable decision vertical"). Tests: `tests/decision/test_decision_service.py`, `tests/decision/test_decision_api.py`. Confirmed passing in CI job `full-cdp-slice-tests` (starts a live `uvicorn cdp.api.main:app` against a live Postgres service container and runs the API round-trip test): run `30542840497`, push to `main`, 2026-07-30T12:30:41Z, conclusion `success`. |
| Challenge (RFC-CDP-042) | Integration Tested (E4) | Route: `POST /decisions/{registry_name}/{decision_id}/challenges`. DDL: `db/ddl/005-challenge-transition.sql`. Tests: `tests/challenge/test_challenge_service.py`, `tests/challenge/test_challenge_api.py`, `tests/migration/test_migration_005_challenge_transition.py`. Same CI run as above. |
| Test (RFC-CDP-043) | Not Implemented | No code implements a distinct "Test Protocol" evidence-gathering step prior to adjudication. (Not to be confused with this repository's `pytest` suite, which tests the *implementation*, not decisions.) |
| Adjudicate (RFC-CDP-044) | Integration Tested (E4) | Route: `POST /decisions/{registry_name}/{decision_id}/challenges/{challenge_id}/adjudications`. DDL: `db/ddl/007-challenge-adjudication.sql`. Tests: `tests/challenge/test_challenge_adjudication_service.py`, `tests/challenge/test_challenge_adjudication_api.py`, `tests/migration/test_migration_007_challenge_adjudication.py`. Same CI run as above. |
| Legitimize (RFC-CDP-045) | Not Implemented | No corresponding route, service function, or table found. The live API's `openapi.json` (checked 2026-07-31 against the locally running `cdp-api` container) lists no legitimize-related path. |
| Execute (RFC-CDP-046) / Presence-Bound Execution Authority (RFC-CDP-051) | Integration Tested (E4) | Routes: `POST .../execution-authorizations`, `POST .../execution-records` (`cdp/api/decisions.py`). DDL: `db/ddl/008-execution-authorization.sql`, `db/ddl/009-execution-record.sql`. Tests: `tests/execution/test_execution_authorization_service.py`, `tests/execution/test_execution_authorization_api.py`, `tests/execution/test_execution_record_service.py`, `tests/execution/test_execution_record_api.py`. Confirmed passing in the same CI run (`30542840497`) — this is a fresh checkout, fresh `uvicorn` process, and fresh Postgres container, so the CI result reflects current source. See "Local vs. CI discrepancy" below for a caveat about ad hoc local runs. |
| Record (RFC-CDP-047) — audit trail | Runtime Tested (E3), exercised indirectly at E4 | Every mutating service function in `cdp/core/services.py` writes to the audit trail via `audit_repo.append_event` inside the same transaction (e.g. lines around 223, 234, 249, 358, 371, 384, 517, 525, 537, 685, 692). DDL: `db/ddl/006-audit-event-ordering.sql`. Directly asserted by `tests/decision/test_decision_service.py::test_happy_path_creates_decision_workflow_task_and_three_audit_events` and exercised structurally/at Postgres level by `tests/migration/test_migration_006_audit_event_ordering.py` and `tests/db/test_db_ddl_runtime.py`. There is no route that exposes the audit trail for external read, so "Record" as an externally-observable API capability has not cleared E4; the write path has. |
| Learn (RFC-CDP-048) | Not Implemented | No evidence currently available. |

## Appeals and Repair (RFC-CDP-070 series)

| Step | Classification | Evidence |
|---|---|---|
| Appeals and Contestability (RFC-CDP-070) | Not Implemented | No evidence currently available. |
| Twenty Points Repair Protocol (RFC-CDP-071) | Not Implemented | No evidence currently available. |
| Breach Record and Repair Agenda (RFC-CDP-072) | Not Implemented | No evidence currently available. |

## Execution substrate

| Capability | Classification | Evidence |
|---|---|---|
| Worker / queue consumption | Not Implemented (stub present) | `cdp/worker/main.py` docstring states literally: "The worker currently provides a safe no-op loop so the local Docker stack can start cleanly before queue consumers are implemented." The process runs (visible in `docker ps` as `cdp-worker`, "Up 5 days"), but it consumes nothing. |
| Self-canonicalizing spreadsheet ingestion | Not Implemented as production code | `tests/misc/test_self_canonicalizing_ingestion.py` contains its own inline reference implementation (CSV/Excel parsing, header derivation, identifier validation) and states in its module docstring: "These tests intentionally keep the ingestion code small and dependency-free. They prove the contract, not a production loader." No corresponding module exists under `cdp/`. This is a proven *contract*, not an implemented capability — see [`003-known-gaps.md`](003-known-gaps.md). |

## Repository tooling (not a CDP governance step, but genuinely evidenced)

| Capability | Classification | Evidence |
|---|---|---|
| RFC index/manifest consistency check | Runtime Tested (E3) | `.github/workflows/rfc-index-integrity.yml` runs `python scripts/verify_rfc_index.py` on every push/PR touching `rfc/**`. This is a real, executing check, distinct from the RFC content itself. As of 2026-07-31, `rfc/index/rfc-manifest.json` (generated 2026-07-16) does not list several files present in `rfc/` (e.g. `RFC-CDP-054`, `RFC-CDP-063`, `RFC-CDP-064`, `RFC-CDP-065`, `RFC-CDP-066`, `RFC-CDP-076`, `RFC-CDP-077`) — whether the current script flags this drift was not re-verified by running it as part of this document's preparation. |

## Local vs. CI discrepancy (documented, not resolved here)

On 2026-07-31, running `python3 -m pytest -q` from a clean shell against a
**locally running Docker stack** (`cdp-api` container, up 45 hours at the
time) produced `2 failed, 93 passed, 41 skipped`. Both failures were in
`tests/execution/test_execution_record_api.py`, each failing with `404 Not Found` on
`POST /decisions/{registry_name}/{decision_id}/execution-records`.

Root cause, confirmed directly: the running `cdp-api` container's live
`/openapi.json` does not list an `execution-records` path, even though the
route exists in the current source at `cdp/api/decisions.py:199`. The
container was built before that route was added and has not been rebuilt —
this is drift between a long-running local container and current source, not
a defect in the source or in CI. The CI job `full-cdp-slice-tests` builds and
starts the API fresh from the checkout on every run, so the CI result
(`30542840497`, success) reflects current source; the ad hoc local run does
not. This is recorded here as a caveat on how to interpret local `pytest`
runs against a stale Docker stack, not as a gap in the execution-record
capability itself.
