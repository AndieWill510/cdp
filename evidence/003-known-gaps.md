# Known Gaps

Status: Draft v0.1 — as of 2026-07-31

This document describes capabilities the constitutional layer (RFCs) or the
architecture layer expects, for which implementation, runtime-test,
integration-test, or evidence artifacts do not currently exist. It describes
the current state faithfully; it does not propose how to close any gap.

## Missing implementation

No code exists under a canonical implementation path (`cdp/`) for these:

- **Identify** (RFC-CDP-030) — no actor identity code.
- **Attest** (RFC-CDP-031) — no attestation code.
- **Standing and Recusal** (RFC-CDP-033) — no standing/recusal code.
- **Test Protocol** (RFC-CDP-043) — no code implements this as a discrete
  evidence-gathering step distinct from adjudication.
- **Legitimize** (RFC-CDP-045) — no corresponding route, service function,
  or table.
- **Learn** (RFC-CDP-048) — no code.
- **Appeals and Contestability** (RFC-CDP-070), **Twenty Points Repair
  Protocol** (RFC-CDP-071), **Breach Record and Repair Agenda**
  (RFC-CDP-072) — no code for any protocol in the RFC-CDP-070 band.
- **Queue consumers** — `cdp/worker/main.py` states in its own docstring
  that it "currently provides a safe no-op loop... before queue consumers are
  implemented." The process runs; it consumes nothing.
- **Self-canonicalizing spreadsheet ingestion as production code** — the
  only implementation of this capability lives inside
  `tests/misc/test_self_canonicalizing_ingestion.py` itself. That file's docstring
  states the embedded code is meant to "prove the contract, not a production
  loader." No module under `cdp/` implements ingestion.
- **Authentication, authorization, and a policy engine** — `README-control-plane-v0.1.md`
  states of the (dormant) `src/cdp_control_plane` prototype: "No auth. No UI.
  No policy engine. No migration framework." No equivalent capability exists
  in the canonical `cdp/` path either.

## Missing runtime tests

- **Nemawashi / workflow rules** has structural and runtime-level (live
  Postgres) test coverage, but no route exposes it as a standalone protocol
  step, so there is no way to write a runtime test of it independent of
  decision creation.

## Missing integration tests

- **Docker build/runtime verification** — `tests/build_verification/test_build_verification.py`
  contains 11 real checks against a running Docker stack (API health,
  Postgres extensions, Redis, Qdrant, LocalStack S3/SQS/EventBridge/DynamoDB/SSM/Secrets),
  but neither `.github/workflows/cdp-ci.yml` nor
  `.github/workflows/rfc-index-integrity.yml` invokes it. It currently runs
  only if a developer runs it manually against a local stack — there is no
  CI evidence of it passing.
- **Audit trail as a read path** — the audit trail is written inside every
  mutating transaction and its ordering is tested at the Postgres level, but
  no route exposes it for external read, so there is no integration test of
  audit-trail retrieval.

## Missing evidence

- **RFC manifest / disk consistency** — `rfc/index/rfc-manifest.json` is
  dated 2026-07-16. As of 2026-07-31, several files present in `rfc/` are not
  listed in it (`RFC-CDP-054`, `RFC-CDP-063`, `RFC-CDP-064`, `RFC-CDP-065`,
  `RFC-CDP-066`, `RFC-CDP-076`, `RFC-CDP-077`). `scripts/verify_rfc_index.py`
  runs in CI on changes to `rfc/**`, but this document's preparation did not
  include re-running that script against current `main`, so whether it
  currently passes or fails given this drift is not established here.
- **Production operation** — no governance step in this repository has E5
  (Production Demonstrated) evidence. All E4 evidence is CI-based (a
  provisioned Postgres service container and a freshly started `uvicorn`
  process inside a GitHub Actions run), not a production deployment.
