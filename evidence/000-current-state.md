# Current State

Status: Draft v0.1 — as of 2026-08-01, session 029 (Universal Attestation) working tree, building on PR #43 head `b29e75a`

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

Every row below is assigned exactly one of these six labels — the same E0–E5
scale defined in `README.md`, so "Not Implemented" and "E0" are the same
rating, not two different systems:

- **Not Implemented (E0)** — no code in a canonical path (`cdp/`) provides
  evidence of the capability itself. Two rows below (`Worker / queue
  consumption`, `Self-canonicalizing spreadsheet ingestion`) have some
  incidental code — a no-op stub, a reference implementation embedded in a
  test file — but neither is evidence of the capability working, so both
  are rated E0 with a note explaining what the incidental code is.
- **Implemented (E1)** — code exists in `cdp/`, no test exercises it.
- **Structurally Tested (E2)** — tested without a live dependency.
- **Runtime Tested (E3)** — tested against a live local dependency (e.g. Postgres), not through the full API.
- **Integration Tested (E4)** — tested through the live API against a live database, confirmed passing in CI.
- **Production Demonstrated (E5)** — observed operating in production.

## Identity and Standing (RFC-CDP-030 series)

| Step | Classification | Evidence |
|---|---|---|
| Identify (RFC-CDP-030) | Integration Tested (E4) | DDL: `db/ddl/010-identity-and-attestation.sql` (`cdp_core.actor`, `cdp_core.identity_claim`, plus the seeded `cdp_identity_recognition_authority` bounded recognition authority added in the v0.2 review correction). Repositories: `cdp/core/repositories/actors.py`, `identity_claims.py`. Service: `register_actor`, `submit_identity_claim`, `recognize_identity_claim`, `deny_identity_claim`, `contest_identity_claim` (`cdp/core/services.py`). Routes: `POST /actors`, `GET /actors/{actor_id}`, `POST /identity-claims`, `GET /identity-claims/{claim_id}`, `POST /identity-claims/{claim_id}/{recognize,deny,contest}` (`cdp/api/identity.py`). Tests: `tests/identify_attest_standing/test_actor_service.py`, `test_identity_claim_service.py`, `test_identity_attestation_api.py`, including coverage that an arbitrary registered actor or a claimant cannot self-recognize. Confirmed passing in CI job `full-cdp-slice-tests`: run `30704929899` on commit `f8ae3d0` (the v0.2-corrected code), 2026-08-01T14:59:19Z, conclusion `success`, re-confirmed unchanged by run `30705068165` on `46afc46` (PR #41's actual merged head -- only evidence-doc text differed between the two commits, not the code this row describes). This is not authentication/authorization/personhood -- see `db/ddl/010-identity-and-attestation.sql`'s header for the constitutional scope note. |
| Attest (RFC-CDP-031) | Integration Tested (E4) | DDL: `db/ddl/010-identity-and-attestation.sql` (`cdp_core.attestation_record`). Repository: `cdp/core/repositories/attestations.py`. Service: `attest_and_create_decision` (`cdp/core/services.py`), the proof-path integration with decision creation -- as of the v0.2 review correction, the attesting actor is no longer required to equal the decision's subject_actor_id (see the docstring). Routes: `POST /attested-decisions`, `GET /attestations/{attestation_id}` (`cdp/api/identity.py`), `GET /decisions/{registry_name}/{decision_id}/attestations` (`cdp/api/decisions.py`, added in v0.2). Tests: `tests/identify_attest_standing/test_attestation_service.py` (grown to 20 cases as of session 028, including a distinct-attestor-and-subject proof and 6 Authority-gate cases -- see the Authority row below), exercised through the live API by `tests/identify_attest_standing/test_identity_attestation_api.py`. Confirmed passing in the same CI runs as Identify above: `30704929899` on `f8ae3d0`, re-confirmed unchanged by `30705068165` on PR #41's actual merged head `46afc46`; this E4 rating predates session 028's Authority extension to the same function -- see the Authority row for that citation. "Verified" in this slice means the actor is active and holds a recognized, in-scope identity claim, not cryptographic proof -- see the DDL header for the honest scope statement. |
| Standing and Recusal (RFC-CDP-033) | Not Implemented (E0) | No evidence currently available. This slice deliberately does not implement Standing -- see Non-Goals in `docs/session-027-identity-and-attestation.md`. |

## Authority (RFC-CDP-032)

| Step | Classification | Evidence |
|---|---|---|
| Authority and Delegation (RFC-CDP-032), scoped to SS19 Minimal Compliance | Integration Tested (E4) | DDL: `db/ddl/011-authority-and-delegation.sql` (`cdp_core.authority_grant`, `cdp_core.authority_evaluation_result`, seeded bounded `cdp_authority_grant_issuer` actor). Repository: `cdp/core/repositories/authority.py`. Service: `grant_authority`, `revoke_authority`, and an Authority gate added to `attest_and_create_decision` (`cdp/core/services.py`). Routes: `POST /authority-grants`, `GET /authority-grants/{grant_id}`, `POST /authority-grants/{grant_id}/revoke` (`cdp/api/authority.py`), `GET /decisions/{registry_name}/{decision_id}/authority-evaluations` (`cdp/api/decisions.py`). Tests: `tests/authority/test_authority_grant_service.py` (9 cases, including the anti-delete trigger actually firing), `tests/authority/test_authority_grant_api.py` (8 cases), plus 6 Authority-gate cases added to `tests/identify_attest_standing/test_attestation_service.py` and 3 to `test_identity_attestation_api.py`. Confirmed passing in CI job `full-cdp-slice-tests`: run `30707515976`, PR #43 head commit `b29e75a`, 2026-08-01T16:09:37Z, conclusion `success`. This is not delegation, quorum, presence, emergency/repair/sovereignty authority, or separation-of-duties enforcement -- see the DDL header's constitutional scope note. |

## Universal Attestation (RFC-CDP-031 §2)

| Step | Classification | Evidence |
|---|---|---|
| Attested challenge, adjudication, execution authorization, execution record | Integration Tested (E4) | DDL: `db/ddl/012-universal-attestation.sql` (additive `governed_act_ref_id` column on `cdp_core.attestation_record` and `cdp_core.authority_evaluation_result`, four new `governed_act_type` vocabulary values). Service: `attest_and_raise_challenge`, `attest_and_adjudicate_challenge`, `attest_and_authorize_execution`, `attest_and_record_execution_attempt` (`cdp/core/services.py`), each reusing the shared `_check_actor_active`/`_check_claim_recognized_and_scoped`/`_evaluate_authority`/`_persist_attestation_and_authority` helpers `attest_and_create_decision` was refactored onto. Routes: `POST /decisions/{registry_name}/{decision_id}/attested-challenges`, `.../challenges/{challenge_id}/attested-adjudications`, `.../attested-execution-authorizations`, `.../attested-execution-records` (`cdp/api/decisions.py`). Tests: `tests/migration/test_migration_012_universal_attestation.py` (7 static + 1 Postgres smoke), `tests/universal_attestation/test_universal_attestation_service.py` (14 cases), `tests/universal_attestation/test_universal_attestation_api.py` (5 cases). Initial corrected proof: run `30729045854` on commit `4d0e7b8` (dispatched via `workflow_dispatch` while PR #44 was still stacked on unmerged PR #43), 2026-08-02T02:32:40Z, conclusion `success`. Current PR-head verification, after PR #43 merged to main (`c508c6d`) and PR #44 was rebased onto it: run `30729249209` on commit `2c9d5fb` (this branch's actual head), 2026-08-02T02:39:41Z, conclusion `success`, alongside the full pre-existing suite with no regressions. Does not reach Test, Legitimize, Learn, or the Identity/Attestation/Authority slices' own mutations — see `docs/session-029-universal-attestation.md` §1 for the scope note. |

## Decision Lifecycle (RFC-CDP-040–048)

| Step | Classification | Evidence |
|---|---|---|
| Nemawashi (RFC-CDP-040) — workflow rules | Runtime Tested (E3) | DDL: `db/ddl/003-nemawashi-workflow-rules.sql`, `db/ddl/004-decision-class-workflow-seed.sql`. Repository: `cdp/core/repositories/workflows.py`. Tests: `tests/nemawashi/test_nemawashi_workflow_rules_ddl.py` (`NemawashiWorkflowRulesDDLStaticTests` run in CI job `pr-guard`; `NemawashiWorkflowRulesDDLPostgresSmokeTests` run against a live Postgres service container in CI job `full-cdp-slice-tests`, `.github/workflows/cdp-ci.yml`). No dedicated API route exposes Nemawashi as a standalone protocol step — it is consumed internally when a decision is created (`NoActiveWorkflowError` in `cdp/core/services.py`), so it has not cleared E4 in its own right. |
| Propose (RFC-CDP-041) — decision creation | Integration Tested (E4) | Route: `POST /decisions` (`cdp/api/decisions.py`). Service: `create_decision_with_workflow` (`cdp/core/services.py`, described in its own docstring as "the smallest executable decision vertical"). Tests: `tests/decision/test_decision_service.py`, `tests/decision/test_decision_api.py`. Confirmed passing in CI job `full-cdp-slice-tests` (starts a live `uvicorn cdp.api.main:app` against a live Postgres service container and runs the API round-trip test): run `30637092898`, PR #40 head commit `75c8f5c`, 2026-07-31T14:04:50Z, conclusion `success`. (An earlier run, `30542840497`, passed the same test on `main` before this PR's test-suite reorg; `30637092898` supersedes it as the citation of record for the current file layout.) |
| Challenge (RFC-CDP-042) | Integration Tested (E4) | Route: `POST /decisions/{registry_name}/{decision_id}/challenges`. DDL: `db/ddl/005-challenge-transition.sql`. Tests: `tests/challenge/test_challenge_service.py`, `tests/challenge/test_challenge_api.py`, `tests/migration/test_migration_005_challenge_transition.py`. Same CI run as above. |
| Test (RFC-CDP-043) | Not Implemented (E0) | No code implements a distinct "Test Protocol" evidence-gathering step prior to adjudication. (Not to be confused with this repository's `pytest` suite, which tests the *implementation*, not decisions.) |
| Adjudicate (RFC-CDP-044) | Integration Tested (E4) | Route: `POST /decisions/{registry_name}/{decision_id}/challenges/{challenge_id}/adjudications`. DDL: `db/ddl/007-challenge-adjudication.sql`. Tests: `tests/challenge/test_challenge_adjudication_service.py`, `tests/challenge/test_challenge_adjudication_api.py`, `tests/migration/test_migration_007_challenge_adjudication.py`. Same CI run as above. |
| Legitimize (RFC-CDP-045) | Not Implemented (E0) | No corresponding route, service function, or table found. The live API's `openapi.json` (checked 2026-07-31 against the locally running `cdp-api` container) lists no legitimize-related path. |
| Execute (RFC-CDP-046) / Presence-Bound Execution Authority (RFC-CDP-051) | Integration Tested (E4) | Routes: `POST .../execution-authorizations`, `POST .../execution-records` (`cdp/api/decisions.py`). DDL: `db/ddl/008-execution-authorization.sql`, `db/ddl/009-execution-record.sql`. Tests: `tests/execution/test_execution_authorization_service.py`, `tests/execution/test_execution_authorization_api.py`, `tests/execution/test_execution_record_service.py`, `tests/execution/test_execution_record_api.py`. Confirmed passing in the same CI run (`30637092898`) — this is a fresh checkout, fresh `uvicorn` process, and fresh Postgres container, so the CI result reflects current source. See "Local vs. CI discrepancy" below for a caveat about ad hoc local runs. |
| Record (RFC-CDP-047) — audit trail | Runtime Tested (E3), exercised indirectly at E4 | Every mutating service function in `cdp/core/services.py` writes to the audit trail via `audit_repo.append_event` inside the same transaction (e.g. lines around 223, 234, 249, 358, 371, 384, 517, 525, 537, 685, 692). DDL: `db/ddl/006-audit-event-ordering.sql`. Directly asserted — via `SELECT event_type FROM cdp_audit.event_log` and forced-failure rollback checks, not just presence — by `tests/decision/test_decision_service.py`, `tests/challenge/test_challenge_service.py`, `tests/challenge/test_challenge_adjudication_service.py`, `tests/execution/test_execution_authorization_service.py`, and `tests/execution/test_execution_record_service.py`; exercised structurally/at Postgres level by `tests/migration/test_migration_006_audit_event_ordering.py` and `tests/db/test_db_ddl_runtime.py`. There is no route that exposes the audit trail for external read, so "Record" as an externally-observable API capability has not cleared E4; the write path has. |
| Learn (RFC-CDP-048) | Not Implemented (E0) | No evidence currently available. |

## Appeals and Repair (RFC-CDP-070 series)

| Step | Classification | Evidence |
|---|---|---|
| Appeals and Contestability (RFC-CDP-070) | Not Implemented (E0) | No evidence currently available. |
| Twenty Points Repair Protocol (RFC-CDP-071) | Not Implemented (E0) | No evidence currently available. |
| Breach Record and Repair Agenda (RFC-CDP-072) | Not Implemented (E0) | No evidence currently available. |

## Execution substrate

| Capability | Classification | Evidence |
|---|---|---|
| Worker / queue consumption | Not Implemented (E0, stub present) | `cdp/worker/main.py` docstring states literally: "The worker currently provides a safe no-op loop so the local Docker stack can start cleanly before queue consumers are implemented." The process runs (visible in `docker ps` as `cdp-worker`, "Up 5 days"), but it consumes nothing. |
| Self-canonicalizing spreadsheet ingestion | Not Implemented (E0, as production code) | `tests/misc/test_self_canonicalizing_ingestion.py` contains its own inline reference implementation (CSV/Excel parsing, header derivation, identifier validation) and states in its module docstring: "These tests intentionally keep the ingestion code small and dependency-free. They prove the contract, not a production loader." No corresponding module exists under `cdp/`. This is a proven *contract*, not an implemented capability — see [`003-known-gaps.md`](003-known-gaps.md). |

## Repository tooling (not a CDP governance step, but genuinely evidenced)

| Capability | Classification | Evidence |
|---|---|---|
| RFC index/manifest consistency check | Runtime Tested (E3) | `.github/workflows/rfc-index-integrity.yml` runs `python scripts/verify_rfc_index.py` on every push/PR touching `rfc/**`, and it passed on this PR's head commit. This is a real, executing check, distinct from the RFC content itself. Running it directly (`python3 scripts/verify_rfc_index.py`) on 2026-07-31 confirms the check does detect the drift described in `rfc/index/rfc-manifest.json` being out of date relative to `rfc/` (e.g. `RFC-CDP-063` through `RFC-CDP-066`, `RFC-CDP-076`, `RFC-CDP-077` absent from the manifest; several status mismatches between the manifest and individual RFC headers) — it emits `WARN`-level lines naming each one — but those warnings are non-fatal, so the script still exits "RFC index verification passed." The check runs and is accurate about what it flags; it simply does not fail the build on this class of drift. See [`001-test-matrix.md`](001-test-matrix.md) for the Test Suite Health rating on this row (Known gaps). |

## Local vs. CI discrepancy (documented, not resolved here)

A local ad hoc `pytest` run on 2026-07-31 against a stale, long-running
local `cdp-api` container (built before the `execution-records` route was
added, never rebuilt) produced two false-negative failures in
`tests/execution/test_execution_record_api.py`. A fresh CI environment —
which builds and starts the API from the current checkout on every run —
passed all execution-record tests. This is drift between a long-lived local
Docker container and current source, not a defect in the source, in CI, or
in the tests; it does not affect the Execute (record) row's evidence level
above. The full root-cause detail and its Test Suite Health classification
(Known gaps — nothing in the suite detects a stale API target) live in
[`001-test-matrix.md`](001-test-matrix.md), which is where this class of
finding belongs per [`README.md`](README.md#what-an-evidence-level-does-not-claim).
