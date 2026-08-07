# Known Gaps

Status: Draft v0.4 -- as of 2026-08-03, post-merge state reflecting main `199c934` (sessions 020-032 merged; 027-032 closed as the Identity/Attestation/Authority/Authentication sequence -- see docs/session-027-032-identity-authority-closure.md)

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
  Session 034 (`docs/session-034-rfc-033-standing-recognition-clarification.md`)
  clarified RFC-CDP-033 to Draft v0.7 -- naming the required properties of
  a legitimate Standing recognition role, formalizing provisional
  affected-party Standing, defining a five-value recognition outcome
  vocabulary, and splitting the seed schema into four append-only records
  -- but this is a specification change only; no code exists under `cdp/`
  for any of it.
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
- **A general policy engine, session model, and OAuth/OIDC/SAML do not
  exist.** `README-control-plane-v0.1.md` states the same of the
  (dormant) `src/cdp_control_plane` prototype: "No auth. No UI. No
  policy engine. No migration framework." A bounded RFC-CDP-032 Authority
  Grant/evaluation mechanism now exists (session 028 -- see the Authority
  section below), but it is not a general authorization system: it
  evaluates only the specific authority type each Universal Attestation
  proof path names, grants can only be issued or revoked by a single
  hardcoded seeded actor. As of session 032, an HTTP caller asserting an
  actor_id on the nine mutating routes that accept one is no longer
  simply believed -- a matching bearer token is required (see the Caller
  Authentication section below) -- but this remains a bearer-token check,
  not OAuth/OIDC/SAML, has no rotation mechanism, and every plain/
  unattested route (`POST /decisions`, `POST /actors` itself, and every
  non-`attested-` challenge/adjudication/execution route) remains
  unauthenticated exactly as before. Likewise, the seeded
  identity-recognition authority added in PR #41
  (`cdp_identity_recognition_authority`) remains a single hardcoded,
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

- **RFC-CDP-030 and RFC-CDP-031 still specify no persistence schema in
  their original requirement sections.** As of session 031, both are
  Draft v0.4 (~40 lines of original §§1-5/1-6 spec text, unchanged, plus
  a new Implementation Status section each) and their previously stale
  internal headers (`RFC-CDP-012`/`RFC-CDP-011`, left over from before
  the identity band was renumbered) are corrected -- but the original
  spec sections still specify no persistence schema, by design; session
  031 documented an interpretation in a new section, it did not add a
  schema to the RFCs' own normative text. The `cdp_core.actor`,
  `cdp_core.identity_claim`, and `cdp_core.attestation_record` schemas in
  `db/ddl/010-identity-and-attestation.sql` remain a documented
  interpretation composing those RFCs' minimal required-properties lists
  with RFC-CDP-033 §11.2's existence/recognition/scope distinction and
  §11.6's non-erasure rule -- not a direct implementation of a schema
  either RFC's original text actually specifies. See the DDL file's
  header, `docs/session-027-identity-and-attestation.md`, and
  `docs/session-031-rfc-spec-updates.md` for the full reasoning.
  RFC-CDP-031 §7 (added in session 031) also states plainly that §4's
  cryptographic verification requirements are not implemented by this
  slice -- see the next bullet, which now duplicates less and cites the
  RFC directly.
- **Verification is claim-based, not cryptographic.**
  `attest_and_create_decision`'s verification means the actor is active
  and holds a recognized, in-scope identity claim -- it does not check a
  cryptographic signature, and `attestation_method`/`credential_reference`
  record a claimed, opaque evidence reference, not proof.
  `attestation_verification_result`'s `failed` value is schema-supported
  but not written by this slice's synchronous service path, which fails
  closed via exception instead (see
  `cdp/core/repositories/attestations.py`'s docstring).
- **Caller authentication is now bearer-token based (session 032), not
  absent, but still narrower than a session/credential system.** Claim
  submission, claim decisions, and attested-decision creation all
  require an `Authorization: Bearer` header matching the asserted
  actor_id's active token (`verify_bearer_token`,
  `db/ddl/014-caller-authentication.sql`) -- see the Caller
  Authentication section below for the full boundary. `POST /actors`
  itself remains unauthenticated (no token exists before registration).
  This is distinct from the claim-based verification point above: that
  governs whether an *actor* is recognized for a purpose; caller
  authentication is about whether the *caller* making the HTTP request
  controls the actor_id it asserts.
- **Only decision creation, challenge-raising, challenge-adjudication,
  execution authorization, and execution recording are attested** (the
  last four added in session 029 -- see the Universal Attestation section
  below). `governed_act_type` still does not cover Test, Legitimize, or
  Learn (no service function exists for those acts to attest), or the
  Identity/Attestation/Authority slices' own mutations (deliberately, to
  avoid circularity -- see the Universal Attestation section).
- **Recognition authority is a single hardcoded actor, not RFC-CDP-032
  Authority.** `decided_by_actor_id` must equal the one seeded
  `cdp_identity_recognition_authority` actor (v0.2 review correction,
  `cdp/core/services.py`'s `_decide_identity_claim`) -- an arbitrary
  registered actor, or the claimant itself, cannot decide a claim. This
  closes the ambient-recognition gap the RFC-CDP-033 §11.1 constitutional
  root explicitly warns against, but there is no authority-grant,
  delegation, expiry, quorum, or separation-of-duties model, and widening
  who may hold this role requires a code change, not a governed act.
- **Purpose scope is a simple string equality check.** Every
  `attest_and_*` proof path still requires an identity claim's
  `purpose_scope` to equal one specific literal string per act type
  (`"decision_creation"`, `"challenge_raising"`, etc.) -- there is no
  hierarchy, wildcard, or composable grammar on this axis, and it remains
  unchanged by session 030 below. Session 030 adds a genuinely richer,
  independent second axis (registry + decision-class scope, optional),
  not a replacement for this one -- see the Identity Claim Scope section
  below.
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
- **Caller authentication is bearer-token based as of session 032.**
  `POST /authority-grants` and `.../revoke` both require the caller to
  present `cdp_authority_grant_issuer`'s own token, not merely assert
  that actor_id in the request body. The canonical migration
  (`db/ddl/014-caller-authentication.sql`) provisions no credential for
  this actor; the local/dev/test-only token this repository's own tests
  and Docker stack use comes from
  `db/seed/dev-caller-authentication-tokens.sql`, published in plaintext
  there and never applied to a real deployment -- see the Caller
  Authentication section below.
- **No production deployment evidence exists for this slice.**

## Universal Attestation (RFC-CDP-031 §2) -- known limitations of the session 029 slice

Session 029 rates the four new attested proof paths at Integration Tested
(E4) in `000-current-state.md`, cited to CI run `30729249209` on this
branch's current head commit `2c9d5fb` (after rebasing PR #44 onto main
following PR #43's merge). The items below are the honest boundaries
of that scope, not a claim that RFC-CDP-031 §2 is implemented in full:

- **Does not reach Test, Legitimize, or Learn.** No service function
  exists for RFC-CDP-043/045/048 yet, so there is nothing for this slice
  to attest.
- **Does not attest the Identity/Attestation/Authority slices' own
  mutations.** Registering an actor, submitting or deciding an identity
  claim, and granting or revoking authority remain unattested,
  deliberately -- they are the foundation this slice's attestation checks
  depend on (an identity claim cannot be recognized by presenting a
  recognized identity claim for the recognizing act), not acts
  attestation can be layered on top of.
- **`governed_act_ref_id` is an un-FK-enforced polymorphic reference.**
  It disambiguates which challenge/adjudication/authorization/execution
  an attestation or authority-evaluation row refers to, but its target
  table depends on `governed_act_type` and nothing in the database
  enforces that correspondence -- it is a service-layer guarantee (each
  `attest_and_*` function passes the ID from its own governed act's
  result), not a database-enforced one. See
  `db/ddl/012-universal-attestation.sql`'s header for the reasoning.
- **Every limitation already named for Identity/Attestation and Authority
  above applies identically here**, since this slice reuses those slices'
  objects and checks unchanged: claim-based not cryptographic
  verification, single hardcoded seeded actors for recognition/grant-
  issuance, no delegation/quorum/separation-of-duties, purpose scope as
  flat string equality (extended here to four new literal strings --
  `challenge_raising`, `challenge_adjudication`, `execution_authorization`,
  `execution_recording` -- not a scope language). As of session 032, all
  four attested proof paths here also require bearer-token caller
  binding on `submitted_by_actor_id` -- see the Caller Authentication
  section below.
- **No production deployment evidence exists for this slice.**

## Identity Claim Scope -- known limitations of the session 030 slice

Session 030 rates the optional registry/decision-class scope on Identity
Claims at Integration Tested (E4) in `000-current-state.md`, cited to CI
run `30730450515` on commit `77f29c9`. The items below are the honest
boundaries of that scope, not a claim of anything broader:

- **Optional, not mandatory.** A claim can still be submitted with
  neither `scope_registry_name` nor `scope_decision_class_id` set, in
  which case `purpose_scope` alone governs coverage exactly as it did
  before this session. This is a deliberate backward-compatibility
  choice, not an oversight -- see
  `db/ddl/013-identity-claim-scope.sql`'s header -- but it does mean the
  richer scope is opt-in per claim, not enforced claim-wide.
- **Still two fixed dimensions, not a general scope grammar.** The same
  limitation already named for `authority_grant`'s scope model above:
  no jurisdiction, risk-level, environment, or affected-parties
  dimension -- `scope_registry_name`/`scope_decision_class_id` only.
- **Does not touch `authority_grant` or RFC-CDP-032 Authority at all.**
  Identity Claim's scope and Authority Grant's scope are two
  independent, unlinked columns on two different tables, each with its
  own two-level model -- there is no shared scope object between them.
- **No production deployment evidence exists for this slice.**

## Caller Authentication -- known limitations of the session 032 slice

Session 032 rates bearer-token caller binding at Integration Tested (E4)
in `000-current-state.md`, cited to CI run `30770996059` on commit
`ba8f5a9` -- the reviewed and corrected commit, after a pre-merge review
pass (PR #48) identified a deployment-blocking issue and two hardening
issues, fixed or recorded below. The items below are the honest
boundaries of that scope, not a claim that this reaches OAuth/OIDC or
cryptographic signing; see `docs/session-032-caller-authentication.md`
§1 and §7 for the full statement:

- **Not OAuth/OIDC/SSO, not cryptographic signing.** A bearer token is
  presented, not signed over per-request -- RFC-CDP-031 §4's signature-
  validity requirement remains unmet, exactly as session 031 already
  documented.
- **No token rotation.** A revoked token's actor cannot obtain a
  replacement in this system; the only path back is registering a new
  actor. There is no "forgot my token" recovery flow.
- **No transport-security guarantee.** This slice adds nothing about
  TLS; a bearer token intercepted in transit is fully usable by whoever
  intercepts it, the standard bearer-token risk. This repository's local
  Docker Compose stack runs over plain HTTP.
- **The two bounded system actors' seed tokens are published in
  plaintext in version control** (`db/seed/dev-caller-authentication-tokens.sql`'s
  header) -- explicit, not an oversight, but zero secrecy for any
  deployment that matters, and there is no rotation mechanism (see
  above) to replace them. **Review correction before merging PR #48:**
  an earlier version of this slice seeded these same two tokens directly
  inside `db/ddl/014-caller-authentication.sql`, the canonical migration
  path -- meaning any deployment applying the normal migrations
  unmodified was born with known, active, privileged credentials for
  `cdp_identity_recognition_authority` and `cdp_authority_grant_issuer`.
  A "provide zero secrecy" warning in a comment does not make that a
  safe default. The seed INSERT now lives only in `db/seed/`, applied
  solely by the local Docker Compose init hook and by CI's test job --
  never by `db/ddl/`. `db/ddl/014`'s SQL text contains no `INSERT INTO
  cdp_core.actor_bearer_token` at all (see
  `tests/migration/test_migration_014_caller_authentication.py`'s
  `test_migration_does_not_seed_any_tokens`, a static, database-state-
  independent assertion; the accompanying Postgres smoke test asserts
  the weaker but portable claim that rerunning 014 never changes the
  bounded actors' token count, since the shared test database it runs
  against may already have `db/seed/` applied for other tests in the
  same CI/local run). A real deployment must still provision credentials
  for these two actors through its own out-of-band mechanism, which this
  repository does not provide.
- **Caller-binding verification runs in a separate transaction from the
  governed mutation it authorizes -- a check/use gap.**
  `verify_bearer_token` opens and completes its own `db.transaction()`
  (see `cdp/core/services.py`); the route then calls the underlying
  mutating service function, which opens its own, separate transaction.
  A token that is valid at the moment `verify_bearer_token` checks it
  could be revoked by a concurrent request before the governed mutation
  actually commits, so in principle the audit record could show an
  authenticated actor performing an act using a credential that was no
  longer active at the mutation's real transaction boundary. This is a
  narrow window (a revocation racing a mutation for the same actor,
  within the gap between two transactions on the same request) and is
  not fixed in this session -- deliberately: closing it would mean
  threading a token/cursor through every one of the nine protected
  routes' underlying service functions (`submit_identity_claim`,
  `recognize/deny/contest_identity_claim`, `attest_and_create_decision`,
  `grant_authority`, `revoke_authority`, and all four Universal
  Attestation `attest_and_*` functions), reversing the deliberate design
  choice that kept `verify_bearer_token` standalone specifically so none
  of their ~150 existing service-layer tests needed to change (see
  `docs/session-032-caller-authentication.md` §2.3). Recorded here
  rather than fixed, per review before merging PR #48.
- **Not every mutating route is covered.** `POST /actors` itself
  (registration) and every plain/unattested route (`POST /decisions`,
  and every challenge/adjudication/execution-authorization/execution-
  record route without the `attested-` prefix) remain unauthenticated,
  exactly as in every prior session -- see
  `docs/session-032-caller-authentication.md` §2.3's "Not covered,
  deliberately" note.
- **`ActorNotFound` is no longer directly reachable through the HTTP
  surface on caller-bound routes for an actor that was never
  registered** -- a documented, deliberate consequence, not a defect:
  since no token could ever exist for an unregistered actor, caller-
  binding (checked first) always intercepts with 401/403 before the
  service-layer `ActorNotFound` check would be reached. `ActorNotFound`
  remains directly exercised at the service layer, which this session
  does not change (`verify_bearer_token` is never called from inside any
  other service function).
- **No rate limiting, no session/cookie model, no authentication of GET
  routes** (all reads remain open, unchanged).
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
