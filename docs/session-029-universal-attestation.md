# Session 029 — Universal Attestation

Status: merged. Implementation complete, verified locally against a live
Docker Compose stack (fresh migration apply, live `uvicorn`, live
Postgres), and confirmed passing in CI (run `30729249209` on head commit
`2c9d5fb`, see §5). PR #43 (session 028) merged to main first; PR #44 was
rebased cleanly onto it, then merged as `7311c8c`. This file documents
what already exists on `main`, not a plan for future work.

Scope: **Universal Attestation** (RFC-CDP-031 §2: "All mutating acts MUST
be attested"), extending the attest+authority proof path sessions 027/028
built for decision creation to the other mutating governed acts this
repository's canonical implementation already has service functions for.
Requested directly as the second of the five follow-up items named in
review of PR #41's evidence layer.

## 1. Scope note (read this first)

"Universal" here is bounded, not literal. It means: every mutating act
this repository's canonical implementation path (`cdp/`) already has a
governed service function for. Concretely, four acts gain an attested
proof path in this session, alongside the one (decision creation) that
already had one:

- raising a challenge (RFC-CDP-042)
- adjudicating a challenge (challenge-level, not the full RFC-CDP-044)
- authorizing execution
- recording an execution attempt (RFC-CDP-047)

It explicitly does **not** reach:

- **Test, Legitimize, Learn** (RFC-CDP-043/045/048) — no service function
  exists for these yet, so there is nothing to attest.
- **The Identity/Attestation/Authority slices' own mutations**
  (`register_actor`, `submit_identity_claim`,
  `recognize_identity_claim`/`deny_identity_claim`/`contest_identity_claim`,
  `grant_authority`, `revoke_authority`). Attesting these would be
  circular: they are the foundation this session's attestation depends
  on, not acts attestation can be layered on top of. An identity claim
  cannot itself be recognized by presenting a recognized identity claim
  for the recognizing act — the regress has to stop somewhere, and it
  stops at the seeded bounded actors (`cdp_identity_recognition_authority`,
  `cdp_authority_grant_issuer`) sessions 027/028 already established.

## 2. What this slice does

One additive migration, a refactor (behavior-preserving) of the four
pre-existing mutating service functions to extract cursor-based bodies,
five new shared helper functions in `cdp/core/services.py`, four new
`attest_and_*` proof-path functions, and four new additive API routes.

### 2.1 The refactor: extracting `_..._in_transaction` helpers

`raise_challenge_for_decision`, `adjudicate_challenge`,
`authorize_execution`, and `record_execution_attempt` each previously
opened their own `with db.transaction() as cursor:` block inline. Each is
now a thin wrapper (`with db.transaction() as cursor: return
_X_in_transaction(cursor, input)`), with the actual body extracted into a
cursor-based `_X_in_transaction` function — the exact pattern
`_create_decision_with_workflow_in_transaction` established in session
027, applied to the other four mutating functions so this session's
`attest_and_*` wrappers can reuse them without nesting a second
`db.transaction()` connection. Each extracted function's result dict also
now includes the `decision` row it fetched, which the new `attest_and_*`
wrappers use to read `decision_class_id` for the authority-scope check
without a second query. **Behavior-preserving**: verified by re-running
the full pre-existing suite (213 tests) after the refactor, before adding
any new code, with zero regressions.

### 2.2 Shared helpers

Five new functions in `cdp/core/services.py`, generalizing what
`attest_and_create_decision` (session 028) did inline for decision
creation only:

- `_check_actor_active(cursor, actor_id)` — actor existence/activeness,
  shared by every `attest_and_*` function.
- `_check_claim_recognized_and_scoped(cursor, *, claim_id, actor_id,
  required_purpose_scope)` — identity-claim ownership/recognition/scope,
  parameterized by the required `purpose_scope` string so each act type
  can require its own (see §2.3).
- `_evaluate_authority(cursor, *, actor_id, authority, ...)` — renamed
  from session 028's `_evaluate_propose_authority`, now parameterized by
  `authority` instead of hardcoding `PROPOSE`.
- `_persist_attestation_and_authority(cursor, *, ..., governed_act_ref_id,
  ...)` — the attestation-record-insert + audit-event +
  authority-evaluation-insert + audit-event block session 028 wrote
  inline for decision creation, now shared and extended with
  `governed_act_ref_id` (see §2.4).

`attest_and_create_decision` itself was refactored to call these shared
helpers instead of its own inline logic — verified behavior-preserving
the same way as §2.1, before any new `attest_and_*` function was added.

### 2.3 Per-act purpose_scope and authority type

| Act | `purpose_scope` required | `authority` required |
|---|---|---|
| Decision creation (session 028, unchanged) | `decision_creation` | `PROPOSE` |
| Challenge raised | `challenge_raising` | `CHALLENGE` |
| Challenge adjudicated | `challenge_adjudication` | `ADJUDICATE` |
| Execution authorized | `execution_authorization` | `AUTHORIZE_EXECUTION` |
| Execution recorded | `execution_recording` | `RECORD` |

The four new authority types were already seeded in the full RFC-CDP-032
§5 vocabulary session 028 wrote (only `PROPOSE` was evaluated by any code
path before this session) — no new authority-type vocabulary was needed,
only new evaluation call sites.

### 2.4 `governed_act_ref_id`: disambiguating multiple sub-records

`attestation_record` and `authority_evaluation_result`'s existing
`governed_act_registry_name`/`governed_act_decision_id` pair uniquely
identifies a *decision* — sufficient for decision creation, where the
decision is the governed act. It is not sufficient for the four new act
types: a decision can have many challenges, and a challenge can be
adjudicated more than once while non-terminal (007's own header notes
this). `db/ddl/012-universal-attestation.sql` adds a nullable
`governed_act_ref_id UUID` column to both tables — `NULL` for
`decision_created` (every existing row from 010/011, unchanged), and the
challenge/adjudication/authorization/execution ID for the four new types.
This is a deliberately un-FK-enforced polymorphic reference (its target
table depends on `governed_act_type`); see the DDL header for why four
mutually-exclusive nullable FK columns were judged not worth the added
complexity at this scope.

### 2.5 The four new proof paths

Each follows the identical shape `attest_and_create_decision` established:
fetch the decision (to read `decision_class_id` for the authority-scope
check — the decision already exists for these four acts, unlike decision
creation), check actor, check claim, evaluate authority, perform the
underlying governed act via the extracted `_..._in_transaction` helper,
persist attestation + authority evaluation. Each is additive: the
underlying unattested function/route (`raise_challenge_for_decision` /
`POST .../challenges`, `adjudicate_challenge` / `POST .../adjudications`,
`authorize_execution` / `POST .../execution-authorizations`,
`record_execution_attempt` / `POST .../execution-records`) is completely
untouched, exactly as `POST /decisions` remained untouched by
`attest_and_create_decision`.

## 3. Objects added

No new tables. `db/ddl/012-universal-attestation.sql` is purely additive
`ALTER TABLE ... ADD COLUMN IF NOT EXISTS` plus four new
`governed_act_type` controlled-vocabulary rows.

## 4. Routes added (`cdp/api/decisions.py`)

- `POST /decisions/{registry_name}/{decision_id}/attested-challenges`
- `POST /decisions/{registry_name}/{decision_id}/challenges/{challenge_id}/attested-adjudications`
- `POST /decisions/{registry_name}/{decision_id}/attested-execution-authorizations`
- `POST /decisions/{registry_name}/{decision_id}/attested-execution-records`

Each accepts the underlying act's own fields plus the five attestation
fields (`submitted_by_actor_id`, `identity_claim_id`,
`attestation_method`, `credential_reference`, `issued_at`) — the same flat
request shape `POST /attested-decisions` established. `AuthorityNotGranted`
maps to `403`, matching sessions 027/028's convention.

## 5. Tests run

All of the following were run against a live Docker Compose stack (fresh
`docker compose build cdp-api`, fresh `up -d`, live Postgres, live
`uvicorn`):

- **Refactor regression check**: full pre-existing suite (213 tests) run
  immediately after §2.1's extraction refactor and again after §2.2's
  `attest_and_create_decision` refactor, both times before any new code
  was added — zero regressions at either checkpoint.
- **Static** (no DB): `tests/migration/test_migration_012_universal_attestation.py::Migration012StaticTests` — 7/7 pass.
- **Postgres/service**: `Migration012PostgresSmokeTests` (1) +
  `tests/universal_attestation/test_universal_attestation_service.py` (14
  cases: 6 for challenge including a forced-failure rollback test, 3 for
  adjudication, 2 for execution authorization, 3 for execution record) —
  15/15 pass, all on the first run.
- **API round-trip**: `tests/universal_attestation/test_universal_attestation_api.py`
  (5 cases: one round trip per act type plus a missing-authority 403) —
  5/5 pass, all on the first run.
- **Full combined suite, unchanged**: every test from sessions 020–028
  (240 static/Postgres/service tests, 43 API tests, both including this
  session's new tests) passes with no regression.
- `ruff check cdp` — passes with no findings.

Combined total this session verified locally: **283 tests pass** (240
static/Postgres/service including the 15 new ones, 43 API including the 5
new ones).

**GitHub Actions:** confirmed. PR #44 was originally opened stacked on
unmerged PR #43 (`session-028-authority-and-delegation`); its base was
changed to `main` after opening, and since a base-branch edit does not
itself fire `synchronize`/`opened`, CI was first triggered via `gh
workflow run cdp-ci.yml --ref session-029-universal-attestation`
(`workflow_dispatch`) — run `30729045854` on commit `4d0e7b8`,
2026-08-02T02:32:40Z, conclusion `success`. PR #43 was then merged to
main (`c508c6d`) and PR #44 was rebased cleanly (no conflicts) onto the
updated main, producing new commit SHAs `c229cc6`/`2c9d5fb`. The
force-push triggered a genuine `pull_request` CI run on the rebased,
now-unstacked branch: run `30729249209` on commit `2c9d5fb` (this
branch's actual head), 2026-08-02T02:39:41Z, conclusion `success`. Both
jobs (`pr-guard`, `full-cdp-slice-tests`) passed on both runs.

## 6. Evidence level reached

**Integration Tested (E4)**, per `evidence/000-current-state.md`, cited
to CI run `30729249209` on commit `2c9d5fb` (PR #44's current, unstacked
head) — the same discipline sessions 026–028 followed: E4 specifically
means CI-confirmed, not locally-confirmed.

## 7. Known limitations (see `evidence/003-known-gaps.md` for the full list)

- Does not reach Test, Legitimize, or Learn — no service function exists
  for those acts yet.
- Does not reach the Identity/Attestation/Authority slices' own
  mutations — deliberately circular-avoidant, see §1.
- `governed_act_ref_id` is an un-FK-enforced polymorphic reference —
  integrity across the four possible target tables is a service-layer
  guarantee (each `attest_and_*` function passes the correct ID from its
  own governed act's result), not a database-enforced one.
- Every limitation already named for the Identity/Attestation (session
  027) and Authority (session 028) slices applies identically here, since
  this session reuses their objects and checks unchanged: claim-based not
  cryptographic verification, no caller authentication, a single
  hardcoded seeded actor for recognition/grant-issuance, no delegation/
  quorum/separation-of-duties.

## 8. Explicit non-goals (all held to)

Not implemented by this slice: Test/Legitimize/Learn attestation (no
underlying service function exists), attestation of the
Identity/Attestation/Authority slices' own mutations, delegation, quorum,
separation-of-duties, real caller authentication, RFC-CDP-030/031 spec
edits, production deployment.

## 9. Context-plane note

This file follows the pattern set by `docs/session-028-authority-and-delegation.md`:
written before staging/committing, so the working tree's actual state is
recorded before it potentially changes. See `docs/SESSION-INDEX.md` for
where this fits in the implementation-session sequence.
