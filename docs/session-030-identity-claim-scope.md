# Session 030 — Richer Scope Semantics for Identity Claims

Status: implementation complete, verified locally against a live Docker
Compose stack (fresh migration apply, live `uvicorn`, live Postgres), and
confirmed passing in CI (run `30730450515` on head commit `77f29c9`, see
§5). Not yet reviewed/merged (PR #46). This file documents what already
exists in the working tree, not a plan for future work.

Scope: extends Identity Claim's coverage model from a flat `purpose_scope`
string-equality check to an optional two-level (registry + decision-class
wildcard) scope, mirroring the model session 028 already built for
Authority Grants. Requested directly as the third of the five follow-up
items named in review of PR #41's evidence layer ("richer purpose/scope
semantics"); session 028 partially addressed this for Authority Grants
only, leaving Identity Claim's own scope untouched until now.

## 1. Scope note (read this first)

This is additive and optional, not a replacement for `purpose_scope`.
Every Identity Claim still declares a `purpose_scope` (e.g.
`decision_creation`, `challenge_raising`) exactly as before, and that
check is unchanged. What's new is a second, independent, optional axis:
a claim may also declare `scope_registry_name` (exact-match) and
`scope_decision_class_id` (nullable wildcard within that registry) --
the same two-level shape `authority_grant` already has. A claim that
omits both new fields (every claim submitted before this migration, and
any claim submitted after it that doesn't set them) behaves identically
to how every claim behaved before this session: `purpose_scope` alone
governs which governed acts it covers. Nothing about the pre-existing E4
proof paths' behavior changes for claims that don't opt into the new
fields.

This is still not RFC-CDP-032 Authority's model or a general governed
scope grammar -- it composes the same two fixed dimensions
(registry, decision class) `authority_grant` already does, not a
jurisdiction/risk-level/environment/affected-parties model.

## 2. What this slice does

One additive migration, a repository/service/API plumbing change to
accept the two new optional fields, and an extension of the shared
`_check_claim_recognized_and_scoped` helper (used by all five attest_and_*
proof paths) to also enforce them when a claim sets `scope_registry_name`.

### 2.1 Migration: `db/ddl/013-identity-claim-scope.sql`

Adds two nullable columns to `cdp_core.identity_claim`:
`scope_registry_name TEXT` and `scope_decision_class_id TEXT`, plus a
CHECK constraint (added idempotently via a `DO $$ ... IF NOT EXISTS`
guard, matching `006-audit-event-ordering.sql`'s pattern for
`uq_event_log_event_sequence`) that forbids `scope_decision_class_id`
being set without `scope_registry_name` also being set --
`scope_decision_class_id` alone would be ambiguous (which registry?).

Unlike `authority_grant.scope_registry_name` (mandatory there),
`identity_claim`'s new columns are nullable. `authority_grant` was a new
table introduced with this scope model from the start; `identity_claim`
already has rows and an E4-tested purpose_scope-only proof path across
sessions 027-029 that this migration must not retroactively invalidate.
NULL `scope_registry_name` means "not scoped to a particular registry" --
the backward-compatible default.

### 2.2 The matching rule

Mirrors `authority_grant`'s wildcard rule exactly (see
`011-authority-and-delegation.sql`'s "Scope model" note):

- `scope_registry_name IS NULL` -- claim is not registry-scoped; only
  `purpose_scope` governs coverage (unchanged pre-session-030 behavior).
- `scope_registry_name` set, `scope_decision_class_id IS NULL` -- claim
  covers every decision class in that registry (wildcard).
- Both set -- claim covers exactly that registry and decision class.

Implemented in Python inside `_check_claim_recognized_and_scoped`
(`cdp/core/services.py`), not as a SQL query, since the claim row is
already fetched by that point and the governed act's
registry_name/decision_class_id are already available at every call
site (the same values each site already passes to `_evaluate_authority`
for the Authority check).

### 2.3 Where it's enforced

All five `attest_and_*` proof paths reuse the same
`_check_claim_recognized_and_scoped` helper, so all five gained this
check simultaneously: `attest_and_create_decision`,
`attest_and_raise_challenge`, `attest_and_adjudicate_challenge`,
`attest_and_authorize_execution`, `attest_and_record_execution_attempt`.
A claim scoped to the wrong registry or decision class raises
`IdentityClaimScopeInsufficient` (the same exception `purpose_scope`
mismatches already raised, reused rather than adding a new exception
type -- both are "this claim's scope does not cover the governed act").

### 2.4 Plumbing

- `cdp/core/repositories/identity_claims.py`: `insert_claim` accepts
  optional `scope_registry_name`/`scope_decision_class_id`.
- `cdp/core/services.py`: `IdentityClaimInput` gains the same two
  optional fields (default `None`), passed through by
  `submit_identity_claim`.
- `cdp/api/identity.py`: `IdentityClaimCreateRequest` gains the same two
  optional fields -- they flow to `IdentityClaimInput` automatically via
  the route's existing `**request.model_dump()` construction, no route
  code change needed.

## 3. Objects added

No new tables. `db/ddl/013-identity-claim-scope.sql` is purely additive:
two nullable columns plus one CHECK constraint on
`cdp_core.identity_claim`.

## 4. Routes changed

None added; `POST /identity-claims` accepts two new optional request
fields.

## 5. Tests run

All of the following were run against a live Docker Compose stack (fresh
migration apply, live Postgres, live `uvicorn`):

- **Static** (no DB): `tests/migration/test_migration_013_identity_claim_scope.py::Migration013StaticTests` -- 7/7 pass.
- **Postgres/service**: `Migration013PostgresSmokeTests` (1, including a
  direct assertion that the CHECK constraint fires on an actual INSERT,
  not just DDL text inspection) + 4 new cases in
  `tests/identify_attest_standing/test_identity_claim_service.py`
  (persist both fields, registry-only wildcard, both fields omitted
  leaves both NULL, class-without-registry rejected by the DB) + 3 new
  cases in `tests/identify_attest_standing/test_attestation_service.py`
  (wrong registry, wrong decision class, matching registry with wildcard
  class) + 2 new cases in
  `tests/universal_attestation/test_universal_attestation_service.py`
  (wrong registry, matching registry with wildcard class, proving the
  same helper's new check applies to a non-decision-creation proof path
  too) -- all pass.
- **API round-trip**: 2 new cases in
  `tests/identify_attest_standing/test_identity_attestation_api.py`
  (matching registry-scoped claim succeeds with 201, wrong-registry
  claim returns 409) -- pass.
- **Full combined suite, unchanged**: every pre-existing test from
  sessions 020-029 continues to pass -- 105 static (pr-guard's exact
  list) + 109 Postgres/service (full-cdp-slice-tests' exact list) + 45
  API (full-cdp-slice-tests' exact list) = 259 tests, zero regressions.
- `ruff check cdp` -- passes with no findings.

**GitHub Actions:** confirmed. Both jobs (`pr-guard`,
`full-cdp-slice-tests`) passed on the first run: run `30730450515`,
commit `77f29c9` (this branch's head), 2026-08-02T03:20:23Z, conclusion
`success`.

## 6. Evidence level reached

**Integration Tested (E4)**, per `evidence/000-current-state.md`, cited
to CI run `30730450515` on commit `77f29c9` -- the same discipline
sessions 026-029 followed: E4 specifically means CI-confirmed, not
locally-confirmed.

## 7. Known limitations

- **Still two fixed dimensions, not a general scope grammar.** Same
  limitation session 028 documented for `authority_grant`'s scope: no
  jurisdiction, risk-level, environment, or affected-parties dimension.
- **Nullable, not mandatory.** A claim can still be submitted without any
  registry/decision-class scope, relying on `purpose_scope` alone -- this
  is a deliberate backward-compatibility choice (see SS1), not an
  oversight, but it does mean the richer scope is opt-in, not enforced
  claim-wide.
- **No production deployment evidence exists for this slice.**

## 8. Explicit non-goals (all held to)

Not implemented by this slice: RFC-CDP-032 Authority changes (session 028
already has its own, separate scope model; this slice does not touch
`authority_grant`), real caller authentication, RFC-CDP-030/031 spec
edits, a general/composable scope grammar, production deployment.

## 9. Context-plane note

This file follows the pattern set by `docs/session-029-universal-attestation.md`:
written before staging/committing, so the working tree's actual state is
recorded before it potentially changes. See `docs/SESSION-INDEX.md` for
where this fits in the implementation-session sequence.
