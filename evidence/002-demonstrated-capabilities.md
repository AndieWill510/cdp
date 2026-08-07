# Demonstrated Capabilities

Status: Draft v0.1 — as of 2026-08-03, post-merge state reflecting main `199c934` (sessions 020-032 merged; 027-032 closed as the Identity/Attestation/Authority/Authentication sequence -- see docs/session-027-032-identity-authority-closure.md)

This document describes only capabilities that have cleared at least E2
(Structurally Tested) per [`README.md`](README.md). It contains no roadmap,
no aspirational content, and no RFC summary — for what is expected but not
yet demonstrated, see [`003-known-gaps.md`](003-known-gaps.md).

## Decision creation

A decision can be created through a live HTTP API (`POST /decisions`,
`cdp/api/decisions.py`) backed by a real Postgres database, and the
transaction that creates it also creates a workflow instance, a task, and
three audit events in the same commit. This is demonstrated by
`tests/decision/test_decision_service.py::test_happy_path_creates_decision_workflow_task_and_three_audit_events`
and `tests/decision/test_decision_api.py`, both confirmed passing against a live
`uvicorn` process and live Postgres service container in CI run `30637092898`
(`full-cdp-slice-tests` job, PR #40 head commit `75c8f5c`, 2026-07-31T14:04:50Z).
An earlier run, `30542840497`, passed the same test on `main` before this PR's
test-suite reorganization; `30637092898` is the current citation of record
since it validates the post-reorg file layout.

## Challenge transitions

A decision can be challenged (`POST
/decisions/{registry_name}/{decision_id}/challenges`), enforcing the
transition rules encoded in `db/ddl/005-challenge-transition.sql`. Demonstrated
by `tests/challenge/test_challenge_service.py` and `tests/challenge/test_challenge_api.py`,
confirmed passing in the same CI run as above.

## Challenge adjudication

A challenge can be adjudicated (`POST
.../challenges/{challenge_id}/adjudications`), enforcing the constraints in
`db/ddl/007-challenge-adjudication.sql`. Demonstrated by
`tests/challenge/test_challenge_adjudication_service.py` and
`tests/challenge/test_challenge_adjudication_api.py`, confirmed passing in the same CI
run.

## Execution authorization and execution recording

A decision can be authorized for execution (`POST
.../execution-authorizations`) and the resulting execution can be recorded
(`POST .../execution-records`), including the constraint that an execution
record cannot be created without a prior authorization
(`db/ddl/008-execution-authorization.sql`, `db/ddl/009-execution-record.sql`).
Demonstrated by `tests/execution/test_execution_authorization_service.py`,
`tests/execution/test_execution_authorization_api.py`,
`tests/execution/test_execution_record_service.py`, and
`tests/execution/test_execution_record_api.py`, all confirmed passing against a fresh
checkout in CI run `30637092898`.

## Identity and Attestation

An actor can be registered (`POST /actors`), submit an identity claim
(`POST /identity-claims`), and have that claim recognized, denied, or
contested (`POST /identity-claims/{claim_id}/{recognize,deny,contest}`) --
enforcing that a denied or contested claim's row is preserved, never
deleted, both at the service layer and at the database level
(`cdp_core.identity_claim`'s `trg_identity_claim_forbid_delete` trigger,
`db/ddl/010-identity-and-attestation.sql`). Only a single seeded, bounded
recognition authority (`cdp_identity_recognition_authority`) may recognize,
deny, or contest a claim -- an arbitrary registered actor, or a claimant
deciding its own claim, is rejected with `403` (v0.2 review correction; see
`docs/session-027-identity-and-attestation.md` §2.5).

A decision-creation act can be attested to a registered, active actor
holding a recognized, in-scope identity claim (`POST /attested-decisions`,
`attest_and_create_decision` in `cdp/core/services.py`), and rejected
closed -- with nothing persisted -- when the actor is unknown, inactive, or
the claim is missing, unrecognized, out of scope, or belongs to a different
actor. The attesting actor (who performed the act) and the decision's
subject (who/what it concerns) are independently recorded and never
required to be the same actor (v0.2 review correction): a clinician may
attest a decision about a patient, an adjuster a decision about a claimant.
`GET /decisions/{registry_name}/{decision_id}/attestations` makes who
attested a decision discoverable directly from the decision.

Demonstrated by `tests/identify_attest_standing/test_actor_service.py`,
`test_identity_claim_service.py`, and `test_attestation_service.py` (24
cases total, including a direct assertion that `DELETE FROM
cdp_core.identity_claim` itself raises, not just that the trigger's SQL
text exists, and that self-recognition and unauthorized recognition are
independently rejected), and by
`tests/identify_attest_standing/test_identity_attestation_api.py` (15
cases, including a full actor/claim/attestation/decision round trip, a
protected-actor redaction check, and the Alice-attests/Bob-is-the-subject
proof) exercised through a live `uvicorn` process and Postgres. Confirmed
passing in CI job `full-cdp-slice-tests`, run `30704929899` on commit
`f8ae3d0` (2026-08-01T14:59:19Z, conclusion `success`, the v0.2-corrected
code), re-confirmed unchanged by run `30705068165` on `46afc46` (PR #41's
actual merged head -- only evidence-doc text differed between the two
commits), alongside the full pre-existing suite with no regressions.

This is not authentication or personhood: no password, token, or key
material is stored; "verified" means the actor is active and holds a
recognized, in-scope claim, not cryptographic proof. No Standing,
Legitimize, or Repair object is written by any function in this slice --
including the recognition-authority check, which is a single hardcoded
seeded actor, not a grant/delegation model. (As of session 028, described
below, `attest_and_create_decision` does additionally evaluate and write
a bounded Authority record -- that extension belongs to the Authority
slice, not this one, and does not change anything stated above about
Identity/Attestation's own scope.) See
`db/ddl/010-identity-and-attestation.sql`'s header and
`docs/session-027-identity-and-attestation.md` for the full scope
statement.

## Authority

`attest_and_create_decision` (`cdp/core/services.py`) additionally
evaluates whether the attesting actor holds an active, unexpired
`PROPOSE` Authority Grant scoped to the decision's registry_name/
decision_class_id (exact match, or a registry-wide wildcard grant) before
creating the decision -- completing the ordering
`architecture/001-canonical-governance-workflow.md` SS4.0 prescribes
(Identify + Attest -> Authority -> ... -> Propose) for this one proof
path. A grant is issued via `POST /authority-grants` and revoked via
`POST /authority-grants/{grant_id}/revoke`, both restricted to a single
seeded bounded actor (`cdp_authority_grant_issuer`) -- an arbitrary
registered actor cannot issue or revoke authority, the same discipline
the Identity and Attestation slice's v0.2 review correction established
for identity-claim recognition, applied here from the start.
`GET /decisions/{registry_name}/{decision_id}/authority-evaluations`
makes whether (and how) authority was evaluated for a decision
discoverable directly from the decision.

Scope is a real two-level hierarchy (registry + decision class, with an
explicit `NULL`-means-wildcard rule for decision class), not a flat
string-equality check -- see `db/ddl/011-authority-and-delegation.sql`'s
"Scope model" note. `expires_at` is mandatory on every grant: RFC-CDP-032
SS9 states "CDP assumes authority decays unless policy states otherwise,"
so nothing can be granted "forever" by omission.

Demonstrated by `tests/authority/test_authority_grant_service.py` (9
cases, including a direct assertion that `DELETE FROM
cdp_core.authority_grant` itself raises) and
`tests/authority/test_authority_grant_api.py` (8 cases), plus 6
authority-gate cases added to
`tests/identify_attest_standing/test_attestation_service.py` (missing
grant, wrong registry scope, wrong decision-class scope, wildcard-scope
success, expired grant, revoked grant) and 3 to
`test_identity_attestation_api.py`. Confirmed passing in CI job
`full-cdp-slice-tests`, run `30707515976` (PR #43 head commit `b29e75a`,
2026-08-01T16:09:37Z, conclusion `success`), alongside the full
pre-existing suite with no regressions.

This is not delegation, quorum, presence, emergency/repair/sovereignty
authority, or separation-of-duties enforcement, and the grant issuer is a
single hardcoded actor, not a delegable role. See
`db/ddl/011-authority-and-delegation.sql`'s header and
`docs/session-028-authority-and-delegation.md` for the full scope
statement.

## Universal Attestation

The same attest-then-authorize proof path `attest_and_create_decision`
established for decision creation now also covers four more mutating
acts: raising a challenge (`POST .../attested-challenges`), adjudicating
one (`POST .../challenges/{challenge_id}/attested-adjudications`),
authorizing execution (`POST .../attested-execution-authorizations`), and
recording an execution attempt (`POST .../attested-execution-records`).
Each requires the same shape of proof decision creation already required
-- a registered, active actor holding a recognized, in-scope identity
claim, plus an active, unexpired, correctly-scoped Authority Grant for
that specific act (`CHALLENGE`, `ADJUDICATE`, `AUTHORIZE_EXECUTION`, or
`RECORD` respectively, each evaluated against its own `purpose_scope`
string) -- and each writes its own `attestation_record` and
`authority_evaluation_result` row, disambiguated from any other
challenge/adjudication/authorization/execution on the same decision by
the new `governed_act_ref_id` column
(`db/ddl/012-universal-attestation.sql`).

The four underlying unattested routes (`POST .../challenges`, `POST
.../adjudications`, `POST .../execution-authorizations`, `POST
.../execution-records`) remain untouched and fully functional on their
own -- attestation is additive here exactly as it was for decision
creation, not a replacement.

Demonstrated by `tests/universal_attestation/test_universal_attestation_service.py`
(14 cases: actor/claim/authority fail-closed coverage per act type, plus
a forced-failure rollback test for challenge-raising asserting zero rows
persisted) and `tests/universal_attestation/test_universal_attestation_api.py`
(5 cases: one full round trip per act type, plus a missing-authority
`403`), exercised through a live `uvicorn` process and Postgres, alongside
`tests/migration/test_migration_012_universal_attestation.py` (7 static +
1 Postgres smoke test proving 001 through 012 apply cleanly and 012 is
rerun-safe). All 283 tests in the combined suite (this session's new
tests plus every test from sessions 020-028) pass locally against a live
Docker Compose stack with zero regressions, and are confirmed passing in
CI job `full-cdp-slice-tests`. Initial corrected proof: run `30729045854`
on commit `4d0e7b8` (2026-08-02T02:32:40Z, conclusion `success`). Current
PR-head verification, after PR #44 was rebased onto main following PR
#43's merge: run `30729249209` on commit `2c9d5fb` (this branch's actual
head), 2026-08-02T02:39:41Z, conclusion `success`.

This does not reach Test, Legitimize, or Learn (RFC-CDP-043/045/048) --
no service function exists for those acts yet -- and it deliberately does
not attest the Identity/Attestation/Authority slices' own mutations
(registering an actor, submitting or deciding an identity claim, granting
or revoking authority): those are the foundation this capability depends
on, not acts it can be layered on top of. See
`docs/session-029-universal-attestation.md` §1 for the full scope
statement.

## Identity Claim Scope

An Identity Claim may optionally declare a two-level scope --
`scope_registry_name` (exact-match) plus a nullable
`scope_decision_class_id` (wildcard within that registry) -- the same
shape `authority_grant` already has (session 028). `POST
/identity-claims` accepts the two new fields
(`db/ddl/013-identity-claim-scope.sql`), and the shared
`_check_claim_recognized_and_scoped` helper every `attest_and_*` proof
path calls now also enforces them when a claim sets
`scope_registry_name`: exact registry match required, exact-or-wildcard
decision-class match required. A claim that omits both fields (every
claim submitted before this migration) is unaffected -- `purpose_scope`
alone continues to govern its coverage, exactly as before.

Demonstrated by `tests/migration/test_migration_013_identity_claim_scope.py`
(7 static + 1 Postgres smoke test, including a direct assertion that the
CHECK constraint forbidding a decision-class scope without a registry
scope fires on an actual `INSERT`, not just DDL text inspection), 4 new
cases in `tests/identify_attest_standing/test_identity_claim_service.py`
(persist both fields, registry-only wildcard, both omitted leaves both
`NULL`, class-without-registry rejected by the database), 3 new cases in
`test_attestation_service.py` (wrong registry, wrong decision class,
matching registry with wildcard class -- against
`attest_and_create_decision`), 2 new cases in
`tests/universal_attestation/test_universal_attestation_service.py`
(wrong registry, matching registry with wildcard class -- against
`attest_and_raise_challenge`, proving the shared helper's check applies
beyond decision creation), and 2 new cases in
`test_identity_attestation_api.py` (matching-scope claim succeeds with
`201`, wrong-registry claim returns `409`). All 259 tests in the combined
suite (this session's new tests plus every test from sessions 020-029)
pass locally against a live Docker Compose stack with zero regressions,
and are confirmed passing in CI job `full-cdp-slice-tests`, run
`30730450515` on this branch's head commit `77f29c9`,
2026-08-02T03:20:23Z, conclusion `success`.

This is still not RFC-CDP-032 Authority's model or a general governed
scope grammar -- it composes the same two fixed dimensions (registry,
decision class) `authority_grant` already does. See
`docs/session-030-identity-claim-scope.md` for the full scope statement.

## Caller Authentication

Registering an actor (`POST /actors`) now also returns a one-time bearer
token (`register_actor` in `cdp/core/services.py`) -- the only time its
plaintext is ever available; only its SHA-256 hash is stored
(`cdp_core.actor_bearer_token`, `db/ddl/014-caller-authentication.sql`).
Nine mutating routes that accept an actor-asserting field now require an
`Authorization: Bearer <token>` header matching that actor's active
token, checked by `verify_bearer_token` before the underlying governed
act runs: identity-claim submission and recognition/denial/contest,
attested-decision creation, authority-grant issuance and revocation, and
all four Universal Attestation proof paths (attested challenge,
adjudication, execution authorization, execution record). A request
presenting no token, an unknown token, or a different actor's valid
token is rejected (401/403) before the underlying act is ever attempted
-- nothing is persisted. `POST /actors/{actor_id}/tokens/revoke` lets an
actor revoke its own token, self-service, by presenting that same
current token; the response is redacted to `{actor_id, token_id, status,
revoked_at}` (a review correction before merging PR #48 -- the full row,
including `token_hash`, previously crossed the API boundary
unnecessarily). The revoked row itself is preserved, never deleted
(`cdp_core.actor_bearer_token`'s anti-delete trigger).

This is real in the sense that closes RFC-CDP-030 §6 and RFC-CDP-031
§7's named gap: a caller can no longer simply assert an actor_id it does
not control and have every downstream check (claim recognition, scope,
authority) proceed as if it did. It is not OAuth/OIDC, not cryptographic
request signing (RFC-CDP-031 §4 remains unmet), and has no token
rotation -- see `docs/session-032-caller-authentication.md` for the full
scope statement.

**Review correction before merging PR #48:** an earlier version of this
capability seeded the two bounded system actors'
(`cdp_identity_recognition_authority`, `cdp_authority_grant_issuer`)
local/dev/test tokens directly inside `db/ddl/014-caller-authentication.sql`
-- the canonical migration path -- meaning any deployment applying the
normal migrations unmodified was born with known, active, privileged
credentials. That seeding now lives only in
`db/seed/dev-caller-authentication-tokens.sql`, applied solely by the
local Docker Compose init hook and by CI's test job, never by `db/ddl/`.
Applying only `db/ddl/001` through `014` to an otherwise-empty database
now leaves both bounded actors with zero tokens (confirmed manually
against a throwaway database); against the shared local/CI database,
where `db/seed/` is intentionally applied before the test suite runs for
the benefit of other tests, the equivalent, database-state-independent
claim is proven at the static-analysis level instead -- `014`'s own SQL
text contains no `INSERT INTO cdp_core.actor_bearer_token` at all. Review
also flagged that `verify_bearer_token` opens and
completes its own transaction, separate from the governed mutation it
authorizes -- a check/use gap recorded in
`evidence/003-known-gaps.md`'s Caller Authentication section rather than
fixed in this session; see that section for the full reasoning.

Demonstrated by `tests/migration/test_migration_014_caller_authentication.py`
(a static test asserting the migration's SQL text seeds *no* tokens; a
Postgres smoke test asserting rerunning the migration never changes the
bounded actors' token count, whatever it already was; and, added in a
post-merge review pass, `Migration014IsolatedDatabaseTests`, which
creates and drops its own scratch database on the same Postgres server,
applies the full canonical migration path -- every `db/ddl/*.sql` file
present on disk, not a hardcoded list -- and asserts the exact
zero-privileged-tokens property automatically in CI, closing the gap
where that property was previously proven only by a one-time manual
check; verified to actually catch a regression by deliberately injecting
a token-seeding statement into 014 and confirming the test fails, then
reverting) and the new
`tests/migration/test_dev_seed_caller_authentication_tokens.py` (static
+ Postgres smoke, including a direct assertion that the published
seed-token plaintext actually hashes to the value stored in that file,
and that applying it activates both bounded actors' tokens), 8 new cases
in `tests/identify_attest_standing/test_actor_service.py`'s
`CallerAuthenticationTests` (token issued as hash-only,
`verify_bearer_token` success/missing/invalid/mismatch,
revoke-then-verify-fails, revoke-with-nothing-to-revoke, anti-delete
trigger firing), and every existing API test across
`test_identity_attestation_api.py`, `test_authority_grant_api.py`, and
`test_universal_attestation_api.py` -- updated to present the correct
actor's token rather than added alongside untouched tests, since
`verify_bearer_token` now gates the routes those tests already
exercised -- plus new cases covering missing/mismatched tokens, the
revoke round trip, and (added in the pre-merge review pass) a direct
assertion that the revoke response never contains `token_hash`. The full
combined suite (this session's new and updated tests plus every
unaffected test from sessions 020-031) passes locally against a live
Docker Compose stack with zero unexplained regressions, and is confirmed
passing in CI job `full-cdp-slice-tests`, run `30779064311` on merge
commit `199c934` (main, push-triggered), 2026-08-03T02:20:39Z,
conclusion `success` -- the closure-state citation, superseding the two
earlier PR-head citations (`30770996059`/`ba8f5a9` for the pre-merge
review fixes, `30778872564`/`7766879` for the post-merge review fixes)
now that both PRs (#48, #49) are merged.

## Standing (Constitutional Affected-Party, Challenge stage)

An actor can submit a Constitutional Affected-Party Standing Claim
against an existing decision (`POST /standing-claims`,
`submit_affected_party_standing_claim` in `cdp/core/services.py`), and
that claim can be separately recognized or denied by a single seeded,
bounded recognition authority (`cdp_standing_recognition_authority`,
`POST /standing-claims/{claim_id}/{recognize,deny}`) -- never determined
by the claimant itself or by any other actor
(`db/ddl/015-standing-and-recusal.sql`). The claim and its determination
are two separate, immutable database rows -- both forbid-delete *and*
forbid-update triggers fire on real `DELETE`/`UPDATE` attempts against
either table, not just on DDL text inspection -- and this slice permits
exactly one determination per claim, rejecting a second attempt.

Minimal sufficiency (RFC-CDP-033 §11.4: "identifies a possible
consequence and the relationship that makes the actor answerable to it")
is enforced by the database itself, not application code: a claim insert
fails closed unless `claimed_impact` is non-blank and at least one of
`standing_basis_role`/`standing_basis_accountability`/
`standing_basis_contextual_relationship` is also non-blank.

Only two of RFC-CDP-033 §11.8's five recognition outcomes are reachable
-- `recognized` and `denied`. A pre-merge review of PR #53 found that the
first version of this slice also implemented `narrowed` as a writable
outcome, with the Challenge gate treating it identically to `recognized`
-- but the determination table has no `outcome_scope` column (RFC-CDP-033
§9.2) to record what a narrowing actually narrows to, so a `narrowed`
determination would have been enforcement-indistinguishable from
`recognized` while still asserting a narrowing the system could not
describe. `narrow_standing_claim` and its route were removed before
merge; `narrowed` remains seeded in the outcome vocabulary only, reserved
for a future session that adds `outcome_scope`. See
`docs/session-035-affected-party-standing-challenge.md` §2.1.

The load-bearing capability this slice exists to prove: `POST
/decisions/{registry_name}/{decision_id}/attested-challenges` accepts an
**optional** `standing_claim_id`. When supplied, a minimally sufficient
claim with **no recognition determination yet** -- still provisional --
is sufficient to raise the Challenge; a `recognized` determination also
permits it; only a `denied` determination blocks it (`403`). This is the
exact correction requested during review of the session-033
reconnaissance doc, now implemented and proven end to end, not merely
documented as an intention. When `standing_claim_id` is omitted,
challenge-raising is completely unaffected -- this is additive to the
existing attested-challenge path, not a new blanket requirement, because
RFC-CDP-033 §6 names several distinct bases for Challenge standing
(affected party, domain expert, governance authority) and this slice
implements only one of them; a mandatory gate would functionally deny
standing to every legitimate challenger this slice does not model.

Demonstrated by `tests/standing/test_standing_claim_service.py` (21
cases, split into claim/determination coverage and a dedicated
`ProvisionalStandingChallengeGateTests` class proving the pending-claim,
recognized-claim, and denied-claim outcomes against a real
`attest_and_raise_challenge` call, plus that omitting `standing_claim_id`
is unaffected, that `narrow_standing_claim` does not exist, and that a
direct `narrowed` insert is rejected by the database's own CHECK
constraint) and `tests/standing/test_standing_claim_api.py` (15 cases:
full submit/recognize/deny round trips, self-determination and
unauthorized-determination both returning `403`, a second determination
returning `409`, the same provisional/recognized/denied Challenge-gating
proof exercised through the live HTTP API, and a direct assertion that
`POST .../narrow` returns `404` as an unregistered route), alongside
`tests/migration/test_migration_015_standing_and_recusal.py` (16 cases:
15 static + 1 Postgres smoke, including an assertion that `narrowed` is
seeded in the vocabulary but excluded from the determination table's own
CHECK constraint). The full combined suite (this session's new tests plus
every test from sessions 020-034) passes locally against a live Docker
Compose stack with zero regressions.

CI job `full-cdp-slice-tests` run `31146632317` (commit `868f191`,
2026-08-07T04:11:29Z, conclusion `success`) confirmed the implementation
*before* the `narrowed`-deferral correction above -- the schema, gate
mechanics, and optional-parameter behavior it verified are unchanged by
that correction, but it does not itself cover the corrected outcome
vocabulary. See `evidence/000-current-state.md` and
`docs/SESSION-INDEX.md` for whichever CI citation is current as of the
commit actually merged.

This is not Recusal, which has no code at all; not any Standing type
other than Constitutional Affected-Party; not automatic Breach Record
generation on a `denied` outcome (RFC-CDP-072 itself remains E0, so there
is nothing to generate a Breach Record into); and not the
enforcement-projection half of RFC-CDP-033 §12's two-layer persistence
model. See `docs/session-035-affected-party-standing-challenge.md` for
the full scope statement.

## Audit trail

Every one of the above operations writes to an append-only audit trail
(`cdp/core/repositories/audit.py`) inside the same database transaction as
the operation itself, and the ordering of those events is constrained by
`db/ddl/006-audit-event-ordering.sql`. This is demonstrated both structurally
(`tests/migration/test_migration_006_audit_event_ordering.py`) and by direct
assertion — querying `cdp_audit.event_log` and forcing an audit-write
failure to confirm the rest of the transaction rolls back with it — in each
of `tests/decision/test_decision_service.py`,
`tests/challenge/test_challenge_service.py`,
`tests/challenge/test_challenge_adjudication_service.py`,
`tests/execution/test_execution_authorization_service.py`, and
`tests/execution/test_execution_record_service.py`.

## Workflow-rule enforcement (Nemawashi)

A decision cannot be created without an active workflow definition matching
its decision class — attempting otherwise raises `NoActiveWorkflowError`
(`cdp/core/services.py`). The underlying schema
(`db/ddl/003-nemawashi-workflow-rules.sql`,
`db/ddl/004-decision-class-workflow-seed.sql`) is demonstrated against a live
Postgres instance by
`tests/nemawashi/test_nemawashi_workflow_rules_ddl.py::NemawashiWorkflowRulesDDLPostgresSmokeTests`
and `tests/migration/test_migration_004_decision_class_workflow_seed.py`, confirmed
passing in CI.

## Continuous integration itself

The repository's two-tier CI setup (`.github/workflows/cdp-ci.yml`) has been
observed to actually execute, not merely exist: `pr-guard` runs lint and
static tests on every PR push; `full-cdp-slice-tests` provisions a real
`pgvector/pgvector:pg16` Postgres service container, applies all DDL under
`db/ddl/`, starts a real `uvicorn cdp.api.main:app` process, and runs the API
round-trip suite against it. Run `30637092898` (PR #40 head commit `75c8f5c`,
2026-07-31T14:04:50Z) shows both jobs completed with conclusion `success`.

## RFC index/manifest verification

A second, independent CI workflow (`.github/workflows/rfc-index-integrity.yml`)
executes `scripts/verify_rfc_index.py` against the contents of `rfc/` on
every push or PR touching that directory. This is a genuinely executing
consistency check over the RFC layer, distinct from the RFC content itself.

## Local Docker stack

A local multi-service stack (`docker/docker-compose.yml`: `cdp-api`,
`cdp-worker`, `cdp-redis`, `cdp-localstack`, `cdp-postgres` with `pgvector`,
`cdp-qdrant`) can be brought up and remain healthy over an extended period.
Directly observed via `docker ps` on 2026-07-31: `cdp-postgres`, `cdp-redis`,
and `cdp-localstack` reporting `healthy` after 12 days of uptime, `cdp-api`
`healthy` after 45 hours. This demonstrates the infrastructure composition
runs; it does not by itself demonstrate any governance-step logic (see the
per-step entries above and in [`000-current-state.md`](000-current-state.md)
for that).
