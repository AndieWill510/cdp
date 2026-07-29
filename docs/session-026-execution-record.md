# Session 026 — Execution Record

Status: implementation drafted, uncommitted on branch `session-026-execution`.
Not yet staged, committed, tested in CI, or reviewed. This file documents
what already exists in the working tree, not a plan for future work.

Scope: **Execution Attempt → Execution Record.**

Explicitly out of scope for this session:
- repair implementation
- repair workflow
- repair verification
- learning
- workflow closure

This matches the "Explicitly still out of scope" note in
`docs/session-024-architecture-checkpoint.md` §5, which named this slice as
the recommended next step after execution authorization (session 025).

## 1. What this slice does

`record_execution_attempt` (`cdp/core/services.py`) is the fifth
transactional vertical slice: record one already-concluded execution
attempt (`succeeded`, `failed`, or `partial`) against a decision that has
an `execution_authorization_record`, via
`POST /decisions/{registry_name}/{decision_id}/execution-records`.

This records an external act after the fact. There is no adapter, no
external call, no async job, and no in-flight/pending status — by the time
CDP is told about an execution attempt, it has already concluded.

Steps inside one transaction (`cdp/core/services.py:record_execution_attempt`):

1. fetch the decision — 404 if missing (`DecisionNotFound`)
2. fetch the `execution_authorization_record` for the decision — 409 if
   absent (`DecisionNotAuthorizedForExecution`)
3. fetch the workflow instance — 409 if absent, or if
   `workflow_status` is `blocked`, `closed`, or `cancelled`
   (`ExecutionNotPermitted`) — authorization eligibility is not assumed to
   still hold just because an authorization row exists (e.g. a new
   challenge raised after authorization re-blocks the workflow)
4. reject `completed_at < attempted_at` (`ValueError` → 422)
5. if `execution_status == "succeeded"`, reject if this authorization
   already has a succeeded record (`ExecutionAlreadySucceeded` → 409),
   backed by a DB-level partial unique index so a concurrent race can't
   create two
6. insert `cdp_core.execution_record`
7. append an `execution.recorded` audit event, correlated by
   `registry_name`/`decision_id` per the session-024 §2 invariant
8. commit

Retries are expected: multiple `execution_record` rows may exist per
authorization (a failed or partial attempt doesn't block another attempt).
At most one may be `succeeded`.

## 2. New/changed files (uncommitted)

- `db/ddl/009-execution-record.sql` (new) — `cdp_core.execution_record`
  table, `execution_status` controlled vocabulary
  (`succeeded`/`failed`/`partial`), partial unique index enforcing at most
  one succeeded record per authorization.
- `cdp/core/repositories/execution_records.py` (new) — insert, fetch-by-
  authorization, fetch-succeeded-for-authorization.
- `cdp/core/services.py` (modified) — `record_execution_attempt`,
  `ExecutionRecordInput`, and the exception types listed above.
- `cdp/api/decisions.py` (modified) — `POST
  /decisions/{registry_name}/{decision_id}/execution-records` and its
  error-to-status-code mapping.
- `.github/workflows/cdp-ci.yml` (modified) — wires the new migration and
  service/API tests into the existing static and Postgres-backed CI jobs.
- `tests/test_migration_009_execution_record.py`,
  `tests/test_execution_record_service.py`,
  `tests/test_execution_record_api.py` (new).

## 3. Boundary verification against declared scope

Checked directly against the working tree during this session (not
assumed from the docstrings):

- No statement in `db/ddl/009-execution-record.sql` writes to
  `cdp_core.workflow_instance`. Asserted by
  `tests/test_migration_009_execution_record.py`, which fails the build if
  an `UPDATE cdp_core.workflow_instance` string appears in the migration's
  executable SQL.
- `record_execution_attempt` only *reads* `workflow_instance` (to check
  eligibility and to link `workflow_instance_id`); it contains no call
  that updates workflow status, closes the workflow, or completes a task.
- No repair table, repair repository, repair service function, or repair
  API route is added. The only appearances of the word "repair" in the
  diff are: (a) explanatory comments/docstrings stating *why* this slice
  deliberately does not touch repair, and (b) the pre-existing
  `referred_to_repair` challenge-adjudication outcome vocabulary from
  session 022, unchanged here.
- No workflow-closure logic is added; `workflow_status`/`closed_at` are
  read only, to assert in tests that they remain untouched by an execution
  record write.

Conclusion: the uncommitted implementation stays inside the declared
Execution Attempt → Execution Record boundary. Repair, repair workflow,
repair verification, learning, and workflow closure remain unimplemented,
as intended.

## 4. What remains before this can close

- Staging, running the full test suite (including the Postgres-backed
  migration/service/API tiers) locally, and committing.
- Normal PR review path (per `docs/session-024-architecture-checkpoint.md`
  §5 recommendation, and consistent with sessions 020/022/025's PR-based
  merge pattern).
- The demo/manual-test decision rows created against
  `sample_attorney_demo` during API exercising were cleaned up out-of-band
  (decision ids `demo-exec-record-1785127279`,
  `demo-exec-record-noauth-1785127474`); confirmed zero residual rows
  across `decision_registry`, `workflow_instance`, `workflow_task`,
  `challenge_record`, `challenge_adjudication_record`,
  `execution_authorization_record`, `execution_record`, and
  `cdp_audit.event_log`.

## 5. Context-plane note

This file exists because Session 026 had an implementation started in the
working tree before any handoff record was written for it — a gap between
"repository as authoritative for repository state" and "working
conversation as authoritative for design intent until promoted." See
`docs/SESSION-INDEX.md` for how this fits alongside sessions 020–025, three
of which (022, 023, 025) were merged without ever getting a dedicated
`docs/session-0NN-*.md` file.
