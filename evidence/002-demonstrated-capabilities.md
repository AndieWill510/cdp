# Demonstrated Capabilities

Status: Draft v0.1 — as of 2026-07-31

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
