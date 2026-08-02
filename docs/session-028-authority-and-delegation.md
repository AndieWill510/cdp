# Session 028 — Authority and Delegation

Status: implementation complete, verified locally against a live Docker
Compose stack and confirmed passing in CI on PR #43 (run `30707515976`,
head commit `b29e75a`). Not yet reviewed/merged. This file documents what
already exists in the working tree, not a plan for future work.

Scope: **Authority** (RFC-CDP-032 Authority and Delegation Model), scoped
to that RFC's §19 Minimal Compliance profile. Requested directly by the
user's own review of PR #41's evidence layer, which named RFC-CDP-032 as
"the next constitutional work," and confirmed via `AskUserQuestion` as the
one item (of five candidates) to build now.

## 1. Constitutional scope note (read this first)

RFC-CDP-032's abstract states the principle this session implements
narrowly: "Authority in CDP is not ambient access. Authority is a scoped,
attributable, time-bounded, policy-governed, revocable, and recordable
capacity to perform or authorize a governed act." §3's core principle is
even more direct: "No anonymous authority. No ambient authority. No
authority without scope. No authority without record."

This session implements exactly §19's Minimal Compliance list and nothing
past it:

- actor identity references (reuses the Identity slice's governed Actor)
- explicit authority grants (`cdp_core.authority_grant`)
- authority scope (a real two-level hierarchy with a wildcard rule, not a
  bare string — see §2.1 below)
- attested mutating acts (already existed; unchanged)
- authority evaluation result (`cdp_core.authority_evaluation_result`)
- revocation status (`authority_grant.status`)
- basic separation-of-duty checks — **explicitly not implemented**; §19
  says a minimal implementation "MAY defer advanced quorum, sovereignty,
  and repair authority features," and separation-of-duties is grouped with
  those deferrals in this session's reading, since none of quorum,
  sovereignty, or repair authority exist yet for it to separate
- record of authority pass/fail (the evaluation result, plus
  `authority.evaluated` audit events)
- execution authority distinct from legitimacy authority — already true
  in this codebase; `cdp_core.execution_authorization_record` (session
  025) predates this slice and is untouched by it

Deliberately **not** implemented, named here rather than left implicit:
delegation (§8 — no delegator, no delegation chain, no `may_delegate`
flag), quorum authority (§12), presence authority (§15 — a different,
pre-existing table already covers a narrower slice of this ground),
emergency/repair/sovereignty grant types (§14), separation-of-duties
enforcement (§11), and authority decay beyond a simple `expires_at`
comparison (§9 names many decay triggers — policy version change, role
change, risk reclassification — none of which this slice tracks).
`grant_type` (§6: `direct | delegated | quorum | presence | emergency |
repair | sovereignty`) is not modeled as a column at all — every grant
this slice can issue is implicitly `direct`.

## 2. What this slice does

Two new governed objects, one new migration, one new repository, four new
service functions (plus one extended), four new API routes (plus one
extended), and a real scope grammar upgrade over the Identity slice's flat
string-equality check.

### 2.1 Scope model — the "richer purpose/scope semantics" upgrade

RFC-CDP-030/031's `identity_claim.purpose_scope` (session 027) is a flat
string compared for exact equality. This slice's `authority_grant` scope
is a genuine two-level hierarchy: `scope_registry_name` (required) and
`scope_decision_class_id` (nullable). `NULL` means "every decision class
in that registry" — an explicit wildcard, not "no scope"; a grant can
never have a `NULL` `scope_registry_name`. This is still far short of
RFC-CDP-032 §6's full scope object (jurisdiction, `risk_level_max`,
environment, target systems, affected parties, repair agenda IDs), but it
is a real hierarchy with a documented wildcard rule, exercised by
`cdp/core/repositories/authority.py`'s `fetch_active_grants_for_actor`,
which orders exact-class matches before wildcard matches so a caller
taking the first result prefers the more specific grant.

### 2.2 Authority Grant (`cdp_core.authority_grant`)

One authority per row (not RFC-CDP-032 §6's array — a deliberate
normalization choice matching this repo's existing "one atomic fact per
column, not key1/value1" discipline). Captures the subject actor, the
`authority` (FK'd to a new `authority_type` registry seeded with the full
23-value RFC-CDP-032 §5 vocabulary, though only `PROPOSE` is evaluated
anywhere in this slice), the two-level scope above, `issued_at` /
`effective_at` / **mandatory** `expires_at`, the issuing actor, and a
`basis` (FK'd to a `policy | role | consent | treaty | law |
community_authority | emergency` registry).

`expires_at` is `NOT NULL` by deliberate constitutional choice, not an
oversight: RFC-CDP-032 §9 states "CDP assumes authority decays unless
policy states otherwise." A nullable `expires_at` would silently mean
"forever," which is exactly the ambient-authority failure mode §3
forbids — so every grant must declare its own expiry.

`status` only ever takes `active` or `revoked` from this slice's service
layer (enforced by a CHECK constraint tighter than the 5-value vocabulary
seeded for future use) — `expired` is computed at evaluation time by
comparing `expires_at` to the evaluation clock, never stored or flipped by
a background job; `suspended`/`superseded` are reserved, unwritten.

No `DELETE` is possible — `trg_authority_grant_forbid_delete` raises
unconditionally, verified in this session by an actual `DELETE` attempt in
the Postgres smoke test. Revocation is a status transition
(`revoked_at`/`revoked_by_actor_id`/`revocation_reason`, all-or-nothing
paired with `status='revoked'` via a CHECK constraint), never erasure.

**Bounded issuer, from the start, not as a follow-up fix.** Only the
single seeded `cdp_authority_grant_issuer` actor may issue or revoke a
grant (`AuthorityGrantIssuerRequired` otherwise) — this applies the exact
discipline the Identity and Attestation slice's v0.2 review correction
established for `cdp_identity_recognition_authority`, but built in here
from the first commit rather than discovered as a gap after the fact.

### 2.3 Authority Evaluation Result (`cdp_core.authority_evaluation_result`)

The governed, permanent (no-`DELETE`, same trigger pattern) record of
whether an actor held matching authority for one governed act, and which
grant (if any) satisfied it. Only `pass`/`fail` are written synchronously
by this slice — `conditional`/`escalated` are schema-seeded for a future
asynchronous or multi-party evaluation flow, matching the same
honest-scope pattern `attestation_verification_result` established in
session 027 (`failed` seeded, never written by the synchronous path).

### 2.4 The proof path: extending `attest_and_create_decision`, not replacing it

`architecture/001-canonical-governance-workflow.md` §4.0 prescribes the
order `Identify + Attest (RFC-030, RFC-031) → Authority Check (RFC-032) →
Nemawashi → ...`. Before this session, `attest_and_create_decision`
(session 027) implemented only the first half. This session completes the
ordering for the one proof path this project has been building across two
sessions, rather than introducing a second, competing "fullest"
decision-creation route — see the extensive docstring update in
`cdp/core/services.py` for the reasoning recorded at the point of change.

Concretely: between the identity/claim checks and decision creation,
`attest_and_create_decision` now evaluates whether the attesting actor
holds an active, unexpired `PROPOSE` grant scoped to the decision's
`registry_name`/`decision_class_id` (exact match, or a registry-wide
wildcard grant). Failure raises `AuthorityNotGranted` before anything is
persisted — fail closed, same pattern as every other check in this
function. On success, the decision is created, then (mirroring
`attestation_record`'s existing timing, since both FK to the decision)
the evaluation result and attestation record are both persisted, then two
audit events in causal order: `attestation.recorded`,
`authority.evaluated`.

**This is a deliberate, documented behavior change**, not a bug: every
existing test and caller of `POST /attested-decisions` from session 027
must now also hold a matching grant, or the call fails closed with `403`.
`POST /decisions` (`create_decision_with_workflow`) remains completely
untouched — it still accepts unattested, unauthorized decisions exactly
as before, for every existing caller and test.

`GET /decisions/{registry_name}/{decision_id}/authority-evaluations`
(`cdp/api/decisions.py`) mirrors session 027's
`GET .../attestations` route — durable, discoverable "was authority
checked for this act, and how" directly from the decision, without
needing to already know an evaluation ID.

## 3. Objects added

| Object | Table | Repository | Service functions |
|---|---|---|---|
| Authority Grant | `cdp_core.authority_grant` | `cdp/core/repositories/authority.py` | `grant_authority`, `revoke_authority` |
| Authority Evaluation Result | `cdp_core.authority_evaluation_result` | `cdp/core/repositories/authority.py` | (written internally by `attest_and_create_decision`, no standalone service function) |

## 4. Routes added

In `cdp/api/authority.py`:

- `POST /authority-grants`, `GET /authority-grants/{grant_id}`
- `POST /authority-grants/{grant_id}/revoke`

In `cdp/api/decisions.py`:

- `GET /decisions/{registry_name}/{decision_id}/authority-evaluations`

Extended (not a new route): `POST /attested-decisions` now also requires
and evaluates authority — see §2.4. Its request schema is unchanged; no
new field was needed, since the evaluated actor is already
`submitted_by_actor_id` and the scope is already the decision's own
`registry_name`/`decision_class_id`.

## 5. Tests run

All of the following were run against a live Docker Compose stack (fresh
`docker compose build cdp-api`, fresh `up -d`, live Postgres, live
`uvicorn`):

- **Static** (no DB): `tests/migration/test_migration_011_authority_and_delegation.py::Migration011StaticTests` — 16/16 pass.
- **Postgres/service**: `Migration011PostgresSmokeTests` (1) +
  `tests/authority/test_authority_grant_service.py` (9) — 10/10 pass,
  including the anti-delete trigger actually firing (a real `DELETE`
  attempt raising, not just DDL text inspection).
- **Extended proof-path service tests**:
  `tests/identify_attest_standing/test_attestation_service.py` grew from
  14 to 20 cases: 3 existing happy-path tests updated to grant `PROPOSE`
  authority as setup, 6 new authority-specific cases (missing grant,
  wrong registry scope, wrong decision-class scope, wildcard-scope
  success, expired grant, revoked grant).
- **API round-trip**: `tests/authority/test_authority_grant_api.py` (8
  cases: grant/get/revoke round trip, wildcard scope, unauthorized
  issuer/revoker, unknown actor, already-revoked, unknown grant, missing
  grant) — 8/8 pass.
  `tests/identify_attest_standing/test_identity_attestation_api.py` grew
  from 15 to 18 cases: 2 existing tests updated to grant authority as
  setup, 3 new cases (missing-authority 403, authority-evaluations list
  round trip, authority-evaluations-list-against-missing-decision 404).
- **Full pre-existing suite, unchanged**: every test from sessions
  020–027 (213 static/Postgres/service tests, 30 non-authority API
  tests) still passes, no regression from the `attest_and_create_decision`
  extension.
- `ruff check cdp` — passes with no findings.

Combined total this session verified locally: **251 tests pass** (213
static/Postgres/service including the 10 new authority ones, 38 API
including the 8 new authority-grant ones).

**GitHub Actions:** PR #43 (branch `session-028-authority-and-delegation`),
labeled `run-full-ci`. CI run `30707515976` on head commit `b29e75a`
(2026-08-01T16:09:37Z) — both `PR guard (static, no DB)` and
`Full CDP slice tests (Postgres/service/API)` completed with conclusion
`success` on the first push, exercising the same static/Postgres/API
tiers wired into `.github/workflows/cdp-ci.yml` above, against a fresh
Postgres service container and a freshly started `uvicorn` process.

## 6. Evidence level reached

Authority is rated **Integration Tested (E4)** in
`evidence/000-current-state.md`, cited to CI run `30707515976` on PR #43's
head commit `b29e75a`.

## 7. Known limitations (see `evidence/003-known-gaps.md` for the full list)

- No delegation, quorum, presence (beyond the pre-existing, narrower
  `execution_authorization_record`), emergency/repair/sovereignty grant
  types, or separation-of-duties enforcement.
- The grant issuer is a single hardcoded seeded actor, not a delegable
  role — widening it requires a code change, not a governed act (the same
  documented limitation session 027 v0.2 accepted for the
  recognition authority).
- Only `PROPOSE` authority is evaluated anywhere; the other 22 seeded
  `authority_type` values exist in the controlled vocabulary but are not
  checked by any code path yet.
- Authority decay (RFC-CDP-032 §9) is a single `expires_at` comparison,
  not the richer multi-trigger decay model the RFC describes.
- Scope is a two-level hierarchy (registry + decision class), not
  RFC-CDP-032 §6's full scope object (jurisdiction, risk level,
  environment, target systems, affected parties, repair agenda).

## 8. Explicit non-goals (all held to)

Not implemented by this slice, verified by what the migration and service
layer do *not* contain
(`test_migration_does_not_write_out_of_scope_governance_tables`, and the
header comment in `db/ddl/011-authority-and-delegation.sql`): delegation,
quorum, separation-of-duties enforcement, emergency/repair/sovereignty
authority, Standing, Legitimize, Repair, real authentication/caller
binding, universal attestation for acts other than decision creation,
RFC-CDP-030/031 spec edits, and production deployment.

## 9. Context-plane note

This file follows the pattern set by `docs/session-027-identity-and-attestation.md`:
written before staging/committing, so the working tree's actual state is
recorded before it potentially changes. See `docs/SESSION-INDEX.md` for
where this fits in the implementation-session sequence.
