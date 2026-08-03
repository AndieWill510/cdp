# Session 032 — Real Authentication / Caller Binding

Status: merged (PR #48, merge commit `660e744`). Reviewed before merge --
two corrections applied (§2.1, §2.5) and one gap recorded rather than
fixed (§7's transaction-boundary bullet). Reviewed a second time after
merge, at `660e744` -- three more corrections applied: stale docstring
text in `cdp/api/authority.py` (§2.3), this file's and the evidence
docs' stale pre-merge header metadata, and a new isolated CI test for
the zero-privileged-tokens invariant (§5). This file documents what
exists on `main`, not a plan for future work.

Scope: binds an HTTP caller to the actor_id it asserts on every mutating
route that accepts one, closing the gap every prior session (027-031)
explicitly named as unaddressed: RFC-CDP-030 §6 and RFC-CDP-031 §7 (both
added in session 031) state plainly that the API accepts a submitted
`actor_id` at face value. Requested directly as the first of the five
follow-up items named in review of PR #41's evidence layer ("real
authentication / caller binding") -- the last of the five to be
implemented, and the only one that reverses a non-goal every prior
session explicitly declared ("no real crypto/OAuth"). The user confirmed
the specific mechanism (bearer token per actor, over HMAC-signed requests
or OAuth2/OIDC) before this session began.

## 1. Scope note (read this first)

This proves the HTTP caller controls a token issued to the actor_id it
asserts. It is real in the sense that a request asserting an actor_id it
does not hold a valid token for is rejected (401/403) by the HTTP layer
itself, not merely logged or checked after the fact. It is **not**:

- **OAuth2/OIDC/SSO.** There is no external identity provider, no
  session model, no JWT, no token expiry beyond manual revocation.
- **Cryptographic signing.** RFC-CDP-031 §4's signature-validity
  requirement remains unmet -- a bearer token is *presented* over TLS (in
  a real deployment), not signed over per-request. This is the same gap
  session 031 already documented in RFC-CDP-031 §7.1; this session does
  not close it.
- **Token rotation.** A revoked token's actor cannot obtain a
  replacement in this slice, and a lost token is unrecoverable. See §7.

## 2. What this slice does

### 2.1 Migration: `db/ddl/014-caller-authentication.sql`

Adds one new table, `cdp_core.actor_bearer_token`: `token_hash` (SHA-256
hex digest -- the plaintext is never stored), `status` (`active` /
`revoked`, mirroring `identity_claim`/`authority_grant`'s anti-erasure
discipline -- a revoked token's row is preserved, never deleted, enforced
by a `BEFORE DELETE` trigger), a partial unique index enforcing at most
one active token per actor at a time, and `issued_at`/`revoked_at`. **This
migration seeds no tokens.**

**Review correction before merging PR #48:** the two bounded system
actors that already exist only via direct SQL seed rows
(`cdp_identity_recognition_authority`, `cdp_authority_grant_issuer` --
sessions 027/028) never went through `register_actor`, so they have no
token from that path. An earlier version of this migration seeded fixed,
published-in-plaintext tokens for both directly inside `db/ddl/014`,
documented as local/dev/test use only -- but review correctly identified
that this meant any deployment applying the canonical migration path
unmodified was born with known, active, privileged credentials for two
system actors that can recognize any Identity Claim and issue/revoke any
Authority Grant. A comment saying "provide zero secrecy" does not turn
that into a safe default. The seed INSERT now lives in a new file,
`db/seed/dev-caller-authentication-tokens.sql`, which is deliberately
**not** part of the `db/ddl/` migration path -- it is applied only by the
local Docker Compose init hook
(`docker/postgres/init/02_initialize_repository.sh`'s existing `db/seed`
step, previously unused) and by CI's `full-cdp-slice-tests` job's own
dedicated seeding step, never by a path a real deployment would run. A
real deployment must provision credentials for these two actors through
its own out-of-band mechanism, which this slice still does not provide.

### 2.2 Token issuance: `register_actor` (additive)

`register_actor` (`cdp/core/services.py`) now also generates a bearer
token (`secrets.token_urlsafe(32)`), inserts its SHA-256 hash into
`actor_bearer_token`, and returns the **plaintext** token once, in the
response's new `bearer_token` key. This is the only time the plaintext
is ever available anywhere in this system -- it is not logged, not
recoverable, and a caller that loses it can only revoke-and-re-register
under session 032's rules (see §7). Every other existing field and key
in `register_actor`'s response is unchanged.

### 2.3 The boundary check: `verify_bearer_token`

A standalone function in `cdp/core/services.py`, deliberately **not**
called from inside any other service function (`register_actor`,
`submit_identity_claim`, `recognize/deny/contest_identity_claim`,
`grant_authority`, `revoke_authority`, or any `attest_and_*` function) --
so none of their existing signatures, behavior, or ~150 existing
service-layer tests change. It parses an `Authorization: Bearer <token>`
header, hashes the token, looks up its row, and raises
`BearerTokenMissing` (no/malformed header), `BearerTokenInvalid` (hash
matches no active row), or `BearerTokenActorMismatch` (matches a
different actor) -- or returns `None` on success.

The API layer (`cdp/api/identity.py`, `authority.py`, `decisions.py`)
calls `verify_bearer_token` first, before the underlying mutating
service function, on every route that accepts an actor-asserting field:

| Route | Field checked |
|---|---|
| `POST /identity-claims` | `claimant_actor_id` |
| `POST /identity-claims/{id}/{recognize,deny,contest}` | `decided_by_actor_id` |
| `POST /attested-decisions` | `submitted_by_actor_id` |
| `POST /authority-grants` | `issued_by_actor_id` |
| `POST /authority-grants/{id}/revoke` | `revoked_by_actor_id` |
| `POST .../attested-challenges` | `submitted_by_actor_id` |
| `POST .../challenges/{id}/attested-adjudications` | `submitted_by_actor_id` |
| `POST .../attested-execution-authorizations` | `submitted_by_actor_id` |
| `POST .../attested-execution-records` | `submitted_by_actor_id` |

`BearerTokenMissing`/`BearerTokenInvalid` map to `401`;
`BearerTokenActorMismatch` maps to `403`.

**Not covered, deliberately** (matching every prior session's "additive,
not retrofit" doctrine): `POST /actors` itself (registration -- no token
exists yet, before an actor has ever been granted one), and every plain/
unattested route (`POST /decisions`, `POST .../challenges`,
`POST .../adjudications`, `POST .../execution-authorizations`,
`POST .../execution-records` without the `attested-` prefix) -- these
remain exactly as unauthenticated as they were in every prior session.

**Post-merge review correction:** `cdp/api/authority.py`'s module
docstring described `cdp_authority_grant_issuer`'s bearer token as
"seeded by that migration for local/dev/test use" -- true when written,
false after the pre-merge fix in §2.1 moved that seeding out of
`db/ddl/014` into `db/seed/`. Corrected to name the actual source
(`db/seed/dev-caller-authentication-tokens.sql`) and state plainly that
the canonical migration provisions no credentials for this actor.

### 2.4 Revocation: `POST /actors/{actor_id}/tokens/revoke`

Self-service only, like a logout: the route requires the caller to
already present that exact actor's own current active token (checked via
`verify_bearer_token` before calling `revoke_actor_bearer_token`) --
there is no separate revoking-authority role. Raises `NoActiveBearerToken`
(`404`) if the actor has no active token to revoke.

**Review correction before merging PR #48:** the route originally
returned the service layer's full `actor_bearer_token` row, including
`token_hash`. Review correctly flagged that a credential verifier --
even a one-way hash -- has no reason to cross the API boundary. The
route now redacts the response to `{actor_id, token_id, status,
revoked_at}`; the service function `revoke_actor_bearer_token` itself is
unchanged and still returns the full row (used internally and by the
service-layer tests in §5).

## 3. Objects added

`db/ddl/014-caller-authentication.sql`: one new table,
`cdp_core.actor_bearer_token`, plus its controlled-vocabulary status
registry (`active`, `revoked`). No rows are seeded by this migration --
see §2.1. `db/seed/dev-caller-authentication-tokens.sql` (new, not part
of the migration path): the two bounded system actors' local/dev/test
tokens, applied separately (§2.1).

## 4. Routes added or changed

- New: `POST /actors/{actor_id}/tokens/revoke`.
- Changed (additive request/response fields, new required header): `POST
  /actors` (response gains `bearer_token`), and the nine routes listed in
  §2.3's table (all now require `Authorization: Bearer <token>`).

## 5. Tests run

All of the following were run against a live Docker Compose stack (fresh
migration apply, live Postgres, live `uvicorn`):

- **Static** (no DB):
  `tests/migration/test_migration_014_caller_authentication.py::Migration014StaticTests`
  (9/9, now including `test_migration_does_not_seed_any_tokens`, added in
  the pre-merge review pass, in place of the removed
  `test_seeded_tokens_match_the_published_plaintext`) and the new
  `tests/migration/test_dev_seed_caller_authentication_tokens.py::DevSeedCallerAuthenticationTokensStaticTests`
  (4/4, including the seed-token-plaintext-matches-hash assertion moved
  from 014, and a direct assertion that the file lives outside `db/ddl/`
  and its header warns unmistakably against deployment use) -- all pass.
- **Postgres/service**: `Migration014PostgresSmokeTests` (1, asserting
  rerunning 014 never changes the bounded actors' token count, whatever
  it already was -- see §5's design note above for why this doesn't
  assert an exact zero) + `Migration014IsolatedDatabaseTests` (1, added
  in the post-merge review pass: creates and drops its own scratch
  database on the same Postgres server, applies the full canonical
  migration path -- `docker/postgres/init/01-init-cdp.sql` then every
  `db/ddl/*.sql` file present on disk, not a hardcoded list -- and
  asserts the exact zero-token property directly, automatically, in CI,
  rather than only by the one-time manual check this session originally
  relied on; verified to actually catch a regression by deliberately
  injecting a token-seeding statement into 014 and confirming the test
  fails, then reverting) + `DevSeedCallerAuthenticationTokensPostgresSmokeTests`
  (1, asserting the seed file actually activates both bounded actors'
  tokens and is rerun-safe) + 8 new cases in
  `tests/identify_attest_standing/test_actor_service.py`'s new
  `CallerAuthenticationTests` class (token issued as hash-only, `verify_bearer_token`
  success/missing/invalid/mismatch, revoke-then-verify-fails,
  revoke-with-nothing-to-revoke, anti-delete trigger firing) -- all pass.
- **API round-trip**: every existing test in
  `tests/identify_attest_standing/test_identity_attestation_api.py`,
  `tests/authority/test_authority_grant_api.py`, and
  `tests/universal_attestation/test_universal_attestation_api.py` was
  updated to present the correct actor's token (`_register_actor` now
  returns `(actor_id, token)`; the two bounded system actors use their
  published seed tokens, now sourced from `db/seed/`) -- plus 12 new
  cases across the three files covering missing token (401), wrong
  actor's valid token (403), and the revoke-then-reuse round trip, plus
  a direct assertion (added in the pre-merge review pass) that the
  revoke response never contains `token_hash`. All pass.
- **Full combined suite, unchanged**: every test from sessions 020-031
  continues to pass -- 118 static (pr-guard's exact list) + 120
  Postgres/service (full-cdp-slice-tests' exact list, +1 for
  `Migration014IsolatedDatabaseTests`, added in the post-merge review
  pass) + 56 API (full-cdp-slice-tests' exact list) = 294 tests, zero
  regressions in any test that did not need updating for the new auth
  requirement.
  **Design note, discovered mid-review:** an earlier version of
  `test_apply_001_through_013_then_014_twice_is_idempotent` asserted the
  two bounded actors have *exactly zero* tokens after applying 001-014 --
  true against an isolated database, but false in both this developer's
  persistent local Docker Postgres and in CI itself, since CI's own
  "Seed dev/test-only data" step (added by this same fix, for the
  benefit of every *other* test in the run) commits `db/seed/`'s tokens
  into the one shared test database before any pytest file runs. The
  assertion now checks that rerunning 014 leaves the count *unchanged*
  (true regardless of what already seeded the table), while the static
  `test_migration_does_not_seed_any_tokens` -- SQL text inspection, no
  database dependency -- carries the actual "014 seeds nothing" claim.
  Confirmed working both ways: manually verified against a throwaway
  `CREATE DATABASE` with only 001-014 applied (zero tokens, as expected)
  and against the normal shared local/CI database (already-seeded,
  count-unchanged assertion holds).
- `ruff check cdp` -- passes with no findings.

**GitHub Actions:** confirmed on the reviewed, final commit. Both jobs
(`pr-guard`, `full-cdp-slice-tests`) passed: run `30770996059`, commit
`ba8f5a9`, 2026-08-02T22:50:53Z, conclusion `success`. `RFC Index
Integrity` also ran (no `rfc/` files touched this session) and passed.

Earlier runs, kept here for the record: the pre-review implementation
passed as run `30751140549` on commit `29c5cdb`, 2026-08-02T14:00:14Z
(the first attempt at that commit failed only on a transient Docker Hub
registry timeout pulling `pgvector/pgvector:pg16` inside GitHub's runner
infrastructure, unrelated to this change; a rerun of the same commit
passed cleanly). The first review-correction commit, `8333801`,
correctly caught a test-design bug in CI (run `30770796503` failed --
`test_apply_001_through_013_then_014_twice_is_idempotent` wrongly
assumed database isolation the shared CI test database doesn't provide,
fixed in the next commit; see §5's design note). `ba8f5a9` above is the
commit that actually merges.

## 6. Evidence level reached

**Integration Tested (E4)**, per `evidence/000-current-state.md`, cited
to CI run `30770996059` on commit `ba8f5a9` -- the reviewed and
corrected, final commit -- the same discipline sessions 026-030
followed: E4 specifically means CI-confirmed, not locally-confirmed.

## 7. Known limitations

- **No token rotation.** A revoked token's actor cannot obtain a
  replacement through this system; the only path back is registering a
  new actor. A lost (never revoked, but no longer known to its holder)
  token remains valid until manually revoked by whoever still holds it --
  there is no "forgot my token" recovery flow.
- **Not cryptographic signing.** RFC-CDP-031 §4 remains unmet -- see §1.
- **Bearer tokens travel in the `Authorization` header on every request,
  with no mention of transport security.** This system's Docker Compose
  stack runs over plain HTTP locally; nothing in this slice adds or
  enforces TLS. A bearer token intercepted in transit is fully usable by
  whoever intercepts it (the standard bearer-token risk) -- a production
  deployment would need to terminate TLS in front of this API, which is
  outside this repository's current scope.
- **The two bounded system actors' seed tokens are published in
  plaintext in version control.** See
  `db/seed/dev-caller-authentication-tokens.sql`'s header -- explicit,
  not an oversight, but a real limitation for any deployment that
  matters. There is no rotation mechanism to replace them (see the first
  bullet above). As of the pre-merge review pass, this seed data no
  longer lives in the canonical `db/ddl/` migration path -- see §2.1.
- **Caller-binding verification runs in a separate transaction from the
  governed mutation it authorizes -- a check/use gap, flagged in review
  before merging PR #48 and recorded here rather than fixed.**
  `verify_bearer_token` opens and completes its own transaction; the
  route then calls the underlying mutating service function, which opens
  its own, separate transaction. A token valid at the moment
  `verify_bearer_token` checks it could be revoked by a concurrent
  request before the governed mutation actually commits -- in principle,
  the audit record could show an authenticated actor performing an act
  using a credential no longer active at the mutation's real transaction
  boundary. Closing this would mean threading a token/cursor through
  every one of the nine protected routes' underlying service functions,
  reversing the deliberate design choice (§2.3) that kept
  `verify_bearer_token` standalone specifically so none of their ~150
  existing service-layer tests needed to change. Not fixed in this
  session, deliberately -- see `evidence/003-known-gaps.md`'s Caller
  Authentication section for the fuller statement.
- **`ActorNotFound` is no longer directly reachable through the HTTP
  surface on caller-bound routes for an actor that was never
  registered** -- since no token could ever exist for such an actor,
  caller-binding (checked first) always intercepts with 401/403 before
  the service-layer `ActorNotFound` check is reached. `ActorNotFound`
  remains directly exercised at the service layer (unaffected by this
  session, since `verify_bearer_token` is never called from inside any
  other service function) -- see
  `test_attested_decision_with_unknown_actor_returns_403_via_caller_binding`
  in `tests/identify_attest_standing/test_identity_attestation_api.py`,
  which documents this consequence directly.
- **Caller-binding covers actor-asserting mutating routes only, not
  every mutating route.** `POST /actors` (registration) and every plain/
  unattested route remain unauthenticated -- see §2.3's "Not covered,
  deliberately" note.
- **No production deployment evidence exists for this slice.**

## 8. Explicit non-goals (all held to)

Not implemented by this slice: OAuth2/OIDC/SSO, cryptographic request
signing (RFC-CDP-031 §4), token rotation/refresh, TLS termination or any
transport-security guarantee, session/cookie-based auth, rate limiting,
authentication of GET routes (all remain open reads, unchanged),
authentication of `POST /actors` itself or any plain/unattested route.

## 9. Context-plane note

This file follows the pattern set by `docs/session-031-rfc-spec-updates.md`:
written before staging/committing, so the working tree's actual state is
recorded before it potentially changes. See `docs/SESSION-INDEX.md` for
where this fits in the implementation-session sequence. This closes out
the five-item follow-up list from the PR #41 evidence-layer review:
Authority (session 028), Universal Attestation (session 029), Identity
Claim Scope (session 030), RFC spec updates (session 031), and this
session.
