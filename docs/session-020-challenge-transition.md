# Session 020 — Challenge Transition (Follow-up Note)

Status: not started — planning note only, no implementation yet.
Depends on: session-019-executable-decision-slice (PR #20), specifically
`create_decision_with_workflow` in `cdp/core/services.py` as the pattern to
follow for transactional writes with an audit trail.

This note exists so the next vertical slice has a starting scope without
re-deriving it from chat history. It intentionally does not implement
anything — no challenge/adjudication/repair code should land on
session-019's branch.

## Scope

Accept a challenge against an existing decision and record it atomically:

1. Verify the decision exists (`cdp_core.decision_registry`, by
   `registry_name` + `decision_id`). Missing decision is a clean
   application-level error, not a partial write.
2. Verify the decision's configured workflow allows a challenge transition
   at its current stage/status. Resolve this from configuration
   (`workflow_definition` / `workflow_stage` / `workflow_instance`), the same
   way session-019 resolves the active workflow — do not hardcode which
   workflows or stages accept challenges.
3. Create the appropriate challenge/deliberation artifact. This likely needs
   a new `cdp_core` table (challenge is not yet modeled in 001/003) —
   confirm whether one exists before assuming a new DDL migration
   (`005-...sql`) is required.
4. Update `workflow_instance` / `workflow_task` state if the challenge
   blocks or redirects the workflow (e.g. `blocked = true`,
   `blocked_reason`, or a new blocking task).
5. Append audit event(s) to `cdp_audit.event_log` (e.g.
   `challenge.raised`, and `workflow.blocked` if applicable).
6. Commit all of the above in exactly one transaction, same as
   `create_decision_with_workflow` — one connection, one commit, rollback on
   any failure.
7. Expose an API endpoint (likely `POST
   /decisions/{registry_name}/{decision_id}/challenges`), with the same
   discipline as session-019: no leaked SQL/exception text, intentional
   status-code mapping (404 missing decision, 409/422 for
   configuration/transition-not-allowed, 500 fallback).
8. Tests: happy path (challenge artifact + state update + audit events),
   rollback safety (forced failure after partial inserts leaves no trace),
   missing decision, and transition-not-allowed by configuration.

## Explicitly out of scope for this slice

Adjudication, legitimation, execution, repair, and appeal. Each of those
should be its own follow-up slice, not bundled into challenge handling.

## Open questions to resolve before implementing

- Is there already a challenge/deliberation table anywhere in `db/ddl/` or
  is this genuinely new schema? (As of session-019, 001 and 003 have no
  challenge table — only `rule_evaluation_result.created_challenge_id TEXT`,
  which is a bare pointer, not a modeled table.)
- Which `workflow_status` / `lifecycle_stage` values legitimately admit a
  challenge? This should come from existing seeded identifiers where
  possible rather than inventing new controlled vocabulary ad hoc.
- Does a challenge always create a blocking task, or only when the
  configured workflow says so?
