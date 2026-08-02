# Session 032 — Real Authentication / Caller Binding

Status: implementation complete, verified locally against a live Docker
Compose stack (fresh migration apply, live `uvicorn`, live Postgres), and
confirmed passing in CI (run `30751140549` on head commit `29c5cdb`, see
§5). Not yet reviewed/merged (PR #48). This file documents what already
exists in the working tree, not a plan for future work.

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
one active token per actor at a time, and `issued_at`/`revoked_at`.

The two bounded system actors that already exist only via direct SQL
seed rows (`cdp_identity_recognition_authority`,
`cdp_authority_grant_issuer` -- sessions 027/028) never went through
`register_actor`, so they had no token from that path. The migration
seeds fixed, **published-in-plaintext** tokens for both, explicitly
documented in the file's header as local/dev/test use only, providing
zero secrecy, and requiring rotation before any deployment that matters
-- a real production system would need a different bootstrapping story
for these two actors' credentials, which this slice does not provide.

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

### 2.4 Revocation: `POST /actors/{actor_id}/tokens/revoke`

Self-service only, like a logout: the route requires the caller to
already present that exact actor's own current active token (checked via
`verify_bearer_token` before calling `revoke_actor_bearer_token`) --
there is no separate revoking-authority role. Raises `NoActiveBearerToken`
(`404`) if the actor has no active token to revoke.

## 3. Objects added

`db/ddl/014-caller-authentication.sql`: one new table,
`cdp_core.actor_bearer_token`, plus its controlled-vocabulary status
registry (`active`, `revoked`).

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
  -- 9/9 pass, including a direct assertion that the two seed tokens'
  published plaintext actually hashes to the value stored in the
  migration (catching transcription drift between the header comment and
  the real `INSERT`).
- **Postgres/service**: `Migration014PostgresSmokeTests` (1, including a
  direct assertion that the partial unique index actually rejects a
  second active token for the same actor, not just DDL text inspection)
  + 8 new cases in
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
  published seed tokens) -- plus 12 new cases across the three files
  covering missing token (401), wrong actor's valid token (403), and the
  revoke-then-reuse round trip. All pass.
- **Full combined suite, unchanged**: every test from sessions 020-031
  continues to pass -- 114 static (pr-guard's exact list) + 118
  Postgres/service (full-cdp-slice-tests' exact list) + 56 API
  (full-cdp-slice-tests' exact list) = 288 tests, zero regressions in any
  test that did not need updating for the new auth requirement.
- `ruff check cdp` -- passes with no findings.

**GitHub Actions:** confirmed. Both jobs (`pr-guard`,
`full-cdp-slice-tests`) passed: run `30751140549`, commit `29c5cdb`
(this branch's head), 2026-08-02T14:00:14Z, conclusion `success`. (The
first attempt failed only on a transient Docker Hub registry timeout
pulling `pgvector/pgvector:pg16` inside GitHub's runner infrastructure,
unrelated to this change; a rerun of the same commit passed cleanly.)
`RFC Index Integrity` also ran (no `rfc/` files touched this session)
and passed.

## 6. Evidence level reached

**Integration Tested (E4)**, per `evidence/000-current-state.md`, cited
to CI run `30751140549` on commit `29c5cdb` -- the same discipline
sessions 026-030 followed: E4 specifically means CI-confirmed, not
locally-confirmed.

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
  plaintext in version control.** See `db/ddl/014-caller-authentication.sql`'s
  header -- explicit, not an oversight, but a real limitation for any
  deployment that matters. There is no rotation mechanism to replace
  them (see the first bullet above).
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
