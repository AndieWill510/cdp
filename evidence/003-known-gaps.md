# Known Gaps

Status: Draft v0.3 -- as of 2026-08-01, session 028 (Authority and Delegation) working tree, building on PR #41 head `46afc46`

This document describes known gaps, limitations, and evidence boundaries:
capabilities the constitutional or architecture layer expects but that are
not yet implemented, not yet tested at the relevant level, or implemented
only within a narrower scope than the RFCs ultimately require. Not every
item below means "nothing exists" -- several describe the honest
boundaries of a capability that has already cleared E4 (see the Identity
and Attestation section). It describes the current state faithfully; it
does not propose how to close any gap.

## Missing implementation

No code exists under a canonical implementation path (`cdp/`) for these:

- **Standing and Recusal** (RFC-CDP-033) — no standing/recusal code.
  Deliberately out of scope for the Identity and Attestation slice — see
  Non-Goals in `docs/session-027-identity-and-attestation.md`. Identity
  Claim recognition (RFC-CDP-030/033 §11.2) is not Standing: a recognized
  claim establishes who an actor is for a governed purpose, not whether
  that actor has the right to participate in a specific decision stage.
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
- **Application authentication and a general policy engine.** No caller
  authentication, session model, or OAuth/OIDC/SAML exists in the
  canonical `cdp/` path. `README-control-plane-v0.1.md` states the same of
  the (dormant) `src/cdp_control_plane` prototype: "No auth. No UI. No
  policy engine. No migration framework." A bounded RFC-CDP-032 Authority
  Grant/evaluation mechanism now exists (session 028 -- see the Authority
  section below), but it is not a general authorization system: it
  evaluates exactly one authority type (`PROPOSE`) for exactly one
  governed act (decision creation), grants can only be issued or revoked
  by a single hardcoded seeded actor, and nothing in it authenticates an
  HTTP caller's identity -- every actor_id in every request is accepted at
  face value. Likewise, the seeded identity-recognition authority added in
  PR #41 (`cdp_identity_recognition_authority`) remains a single hardcoded,
  bounded guardrail against ambient identity-claim recognition, not a
  general authorization system.

## Missing standalone protocol surface

- **Nemawashi / workflow rules** has structural and runtime-level (live
  Postgres) test coverage -- this is not a testing gap. The actual gap is
  that no route exposes it as a standalone protocol step, only as a
  precondition of decision creation, so it cannot be exercised (or its own
  runtime test written) independent of `POST /decisions`.

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

## Identity and Attestation -- known limitations of the E4 slice

Identify and Attest (RFC-CDP-030, RFC-CDP-031) are now **Integration
Tested (E4)** for the bounded decision-creation proof path (see
`000-current-state.md`, cited to CI run `30704929899` on commit `f8ae3d0`,
re-confirmed unchanged by run `30705068165` on `46afc46`, PR #41's actual
merged head): actor registration, identity-claim submission/recognition,
claim preservation under denial/contest, protected/pseudonymous display,
attested decision creation, distinct attestor/subject preservation, and
decision-level attestation lookup are all exercised through the live API
against Postgres and confirmed passing in CI. The items below are the
honest boundaries of that E4 capability, not evidence of an unimplemented
one -- named here rather than left implicit, per this document's own
discipline:

- **RFC-CDP-030 and RFC-CDP-031 remain underspecified relative to the
  implemented schema.** Both are Draft v0.3, roughly 40 lines each, and
  specify no persistence schema. The `cdp_core.actor`,
  `cdp_core.identity_claim`, and `cdp_core.attestation_record` schemas in
  `db/ddl/010-identity-and-attestation.sql` are a documented interpretation
  composing those RFCs' minimal required-properties lists with
  RFC-CDP-033 §11.2's existence/recognition/scope distinction and §11.6's
  non-erasure rule -- not a direct implementation of a schema either RFC
  actually specifies. See the DDL file's header and
  `docs/session-027-identity-and-attestation.md` for the full reasoning.
- **Verification is claim-based, not cryptographic.**
  `attest_and_create_decision`'s verification means the actor is active
  and holds a recognized, in-scope identity claim -- it does not check a
  cryptographic signature, and `attestation_method`/`credential_reference`
  record a claimed, opaque evidence reference, not proof.
  `attestation_verification_result`'s `failed` value is schema-supported
  but not written by this slice's synchronous service path, which fails
  closed via exception instead (see
  `cdp/core/repositories/attestations.py`'s docstring).
- **Caller authentication does not exist.** The API accepts a submitted
  `actor_id` (for registration, claims, decisions, or claim decisions) at
  face value -- there is no session, token, or credential proving the HTTP
  caller actually controls the actor_id it is asserting. This is distinct
  from the claim-based verification point above: that governs whether an
  *actor* is recognized for a purpose; this is about whether the *caller*
  making the HTTP request is who it says it is, which nothing in this
  slice checks.
- **Only decision creation is attested.** `governed_act_type` is seeded
  with only `decision_created`. Attesting any other mutating act (a
  challenge, an adjudication, an execution authorization) is not
  implemented.
- **Recognition authority is a single hardcoded actor, not RFC-CDP-032
  Authority.** `decided_by_actor_id` must equal the one seeded
  `cdp_identity_recognition_authority` actor (v0.2 review correction,
  `cdp/core/services.py`'s `_decide_identity_claim`) -- an arbitrary
  registered actor, or the claimant itself, cannot decide a claim. This
  closes the ambient-recognition gap the RFC-CDP-033 §11.1 constitutional
  root explicitly warns against, but there is no authority-grant,
  delegation, expiry, quorum, or separation-of-duties model, and widening
  who may hold this role requires a code change, not a governed act.
- **Purpose scope is a simple string equality check, not a governed scope
  language.** `attest_and_create_decision` requires an identity claim's
  `purpose_scope` to equal the literal string `"decision_creation"` --
  there is no hierarchy, wildcard, or composable scope grammar, and
  extending coverage to other governed acts (see above) would need either
  more literal scope strings or a real scope language, neither of which
  exists yet.
- **A separate `cdp_actor_type` registry, not a retrofit of the legacy
  `actor_type` registry `decision_registry` already uses.** A compatibility
  mapping in `cdp/core/repositories/actors.py`
  (`_LEGACY_ACTOR_TYPE_MAP`) tags each governed actor's underlying
  `identifier_registry` row with a compatible legacy `actor_type` value
  (`synthetic` → `agent`, `collective` → `institution`) so it can still be
  used as `decision_registry.subject_actor_id`, which predates this slice
  and was out of bounds to modify. This is a bridge, not a claim that the
  two vocabularies are equivalent.
- **The attestor and the decision's subject are independently recorded,
  never required to be the same actor** (v0.2 review correction).
  `attest_and_create_decision` no longer requires
  `attestation_input.actor_id` to equal `decision_input.subject_actor_id`
  -- a clinician (attestor) may attest a decision about a patient
  (subject). Decision subjects are not required to be governed
  `cdp_core.actor` rows at all, only a legacy-registered identifier, per
  `decision_registry`'s pre-existing rules.
- **No production deployment evidence exists for this slice**, consistent
  with every other capability in this repository -- see "Production
  operation" under Missing evidence below.

## Authority (RFC-CDP-032) -- known limitations of the SS19 Minimal Compliance slice

Session 028 rates Authority at E4 (Integration Tested) in
`000-current-state.md`, cited to CI run `30707515976` on PR #43 head
`b29e75a`. The items below are the honest boundaries of that scope, not a
claim that RFC-CDP-032 is implemented in full:

- **No delegation.** RFC-CDP-032 SS8's entire delegation model (a
  delegator, a delegation chain, `may_delegate`, recipient/scope/validity
  propagation) is absent. `grant_type` (SS6:
  `direct | delegated | quorum | presence | emergency | repair |
  sovereignty`) is not even a column -- every grant this slice can issue
  is implicitly "direct."
- **No quorum, presence (beyond a pre-existing, narrower table), or
  emergency/repair/sovereignty grant types** (SS12, SS14, SS15).
  `cdp_core.execution_authorization_record` (session 025) already covers
  a narrower slice of "presence"-shaped ground and predates this session;
  it is not unified with `cdp_core.authority_grant` here.
- **No separation-of-duties enforcement** (SS11) -- nothing prevents the
  same actor from holding conflicting authorities.
- **Only `PROPOSE` is evaluated.** All 23 RFC-CDP-032 SS5 authority types
  are seeded as controlled vocabulary (so a future slice can grant and
  evaluate them without a schema change), but no code path checks any
  authority type except `PROPOSE`, and only for decision creation.
- **Authority decay is a single `expires_at` comparison.** RFC-CDP-032
  SS9 names many decay triggers (policy version change, role change, risk
  reclassification, active-challenge conflict, jurisdiction change...);
  this slice tracks none of them.
- **Scope is a two-level hierarchy, not RFC-CDP-032 SS6's full scope
  object.** `scope_registry_name` + nullable `scope_decision_class_id`
  (with an explicit wildcard rule) is a real hierarchy, a genuine step
  past Identity's flat string-equality `purpose_scope` -- but it has no
  jurisdiction, `risk_level_max`, environment, target-systems,
  affected-parties, or repair-agenda dimensions.
- **The grant issuer is a single hardcoded seeded actor**
  (`cdp_authority_grant_issuer`), not a delegable role -- the same
  documented limitation session 027 v0.2 accepted for the identity
  recognition authority, applied here from the start. Widening it
  requires a code change, not a governed act.
- **Caller authentication does not exist here either** -- the same gap
  named in the Identity and Attestation section above applies identically
  to `POST /authority-grants`: `issued_by_actor_id` and
  `revoked_by_actor_id` are accepted at face value, not proven to be the
  HTTP caller.
- **No production deployment evidence exists for this slice.**

## RFC index/manifest verification -- known limitation of a working check

This is not a missing-evidence item: `scripts/verify_rfc_index.py` runs in
CI on every change to `rfc/**` and has been run directly and confirmed
passing (see `000-current-state.md`'s "RFC index/manifest consistency
check" row and `001-test-matrix.md`'s corresponding entry). The gap is
narrower than "does the check run" -- it is that the check's drift
detection is non-fatal:

- **RFC manifest / disk consistency drift is detected but does not fail
  the build.** `rfc/index/rfc-manifest.json` is dated 2026-07-16. As of
  2026-07-31, several files present in `rfc/` are not listed in it
  (`RFC-CDP-054`, `RFC-CDP-063`, `RFC-CDP-064`, `RFC-CDP-065`,
  `RFC-CDP-066`, `RFC-CDP-076`, `RFC-CDP-077`), and several manifest/header
  status pairs disagree (e.g. `RFC-CDP-053` manifest says "Draft", header
  says "Draft v0.1"). `verify_rfc_index.py` emits `WARN`-level lines naming
  each one, but still exits "RFC index verification passed" -- so this
  class of drift can accumulate indefinitely without ever failing CI. The
  check running and passing is not evidence that the manifest is
  accurate; those are two different claims.

## Missing evidence

- **Production operation** — no governance step in this repository has E5
  (Production Demonstrated) evidence. All E4 evidence is CI-based (a
  provisioned Postgres service container and a freshly started `uvicorn`
  process inside a GitHub Actions run), not a production deployment.
