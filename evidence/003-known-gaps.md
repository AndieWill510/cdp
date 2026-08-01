# Known Gaps

Status: Draft v0.1 — as of 2026-07-31

This document describes capabilities the constitutional layer (RFCs) or the
architecture layer expects, for which implementation, runtime-test,
integration-test, or evidence artifacts do not currently exist. It describes
the current state faithfully; it does not propose how to close any gap.

## Missing implementation

No code exists under a canonical implementation path (`cdp/`) for these:

- **Standing and Recusal** (RFC-CDP-033) — no standing/recusal code.
  Deliberately out of scope for the Identity and Attestation slice — see
  Non-Goals in `docs/session-027-identity-and-attestation.md`. Identity
  Claim recognition (RFC-CDP-030/033 §11.2) is not Standing: a recognized
  claim establishes who an actor is for a governed purpose, not whether
  that actor has the right to participate in a specific decision stage.
- **Authority and Delegation** (RFC-CDP-032) — no authority-grant,
  delegation, or authority-evaluation code. `attest_and_create_decision`
  checks actor existence/activeness and identity-claim recognition/scope,
  not authority in RFC-CDP-032's sense (no `Authority Grant` object, no
  separation-of-duties, no quorum, no delegation chain).
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

## Identity and Attestation slice -- specific limitations

These are named here rather than left implicit, per this document's own
discipline:

- **RFC-CDP-030 and RFC-CDP-031 are thin.** Both are Draft v0.3, roughly 40
  lines each, and specify no persistence schema. The `cdp_core.actor`,
  `cdp_core.identity_claim`, and `cdp_core.attestation_record` schemas in
  `db/ddl/010-identity-and-attestation.sql` are a documented interpretation
  composing those RFCs' minimal required-properties lists with
  RFC-CDP-033 §11.2's existence/recognition/scope distinction and §11.6's
  non-erasure rule -- not a direct implementation of a schema either RFC
  actually specifies. See the DDL file's header and
  `docs/session-027-identity-and-attestation.md` for the full reasoning.
- **"Verified" is not cryptographic.** `attest_and_create_decision`'s
  verification means the actor is active and holds a recognized, in-scope
  identity claim -- it does not check a cryptographic signature, and
  `attestation_method`/`credential_reference` record a claimed, opaque
  evidence reference, not proof. `attestation_verification_result`'s
  `failed` value is schema-supported but not written by this slice's
  synchronous service path, which fails closed via exception instead (see
  `cdp/core/repositories/attestations.py`'s docstring).
- **The proof path covers exactly one governed act.** `governed_act_type`
  is seeded with only `decision_created`. Attesting any other mutating act
  (a challenge, an adjudication, an execution authorization) is not
  implemented.
- **A separate `cdp_actor_type` registry, not a retrofit of the legacy
  `actor_type` registry `decision_registry` already uses.** A compatibility
  mapping in `cdp/core/repositories/actors.py`
  (`_LEGACY_ACTOR_TYPE_MAP`) tags each governed actor's underlying
  `identifier_registry` row with a compatible legacy `actor_type` value
  (`synthetic` → `agent`, `collective` → `institution`) so it can still be
  used as `decision_registry.subject_actor_id`, which predates this slice
  and was out of bounds to modify. This is a bridge, not a claim that the
  two vocabularies are equivalent.
- **Recognition authority is a single hardcoded actor, not a delegable
  grant.** `decided_by_actor_id` must equal the one seeded
  `cdp_identity_recognition_authority` actor (v0.2 review correction,
  `cdp/core/services.py`'s `_decide_identity_claim`) -- an arbitrary
  registered actor, or the claimant itself, cannot decide a claim. This
  closes the ambient-recognition gap the RFC-CDP-033 §11.1 constitutional
  root explicitly warns against, but it is still not RFC-CDP-032 Authority:
  there is no grant, scope, expiry, or delegation chain, and widening who
  may hold this role requires a code change, not a governed act.
- **The attestor and the decision's subject are independently recorded,
  never required to be the same actor** (v0.2 review correction).
  `attest_and_create_decision` no longer requires
  `attestation_input.actor_id` to equal `decision_input.subject_actor_id`
  -- a clinician (attestor) may attest a decision about a patient
  (subject). The subject is not required to be a governed `cdp_core.actor`
  at all, only a legacy-registered identifier, per
  `decision_registry`'s pre-existing rules.

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
