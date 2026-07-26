# Session 021 — Challenge Policy Follow-ups (Note)

Status: not started — planning note only, no implementation yet.
Depends on: session-020-challenge-transition-impl (PR #22, merged
2026-07-26), specifically `raise_challenge_for_decision` in
`cdp/core/services.py` and `cdp_core.challenge_record` in
`db/ddl/005-challenge-transition.sql`.

## Why this note exists

PR #22 shipped challenge admission gated only by
`workflow_instance.workflow_status` being non-terminal (see
`_TERMINAL_WORKFLOW_STATUSES` in `cdp/core/services.py` and the
"Workflow-awareness note" in `005-challenge-transition.sql`). That was an
explicit, accepted tradeoff for that slice: no `workflow_stage` or
`rule_definition` yet gates challenges through an explicit challenge
stage/transition, so the non-terminal-status check was used as a
transitional workflow-status gate rather than a full challenge-policy
model.

**This is the key follow-up**: that transitional gate should not become
the final policy. A future slice needs to replace or refine it with real
configured gating (explicit challenge stage, and/or a `rule_definition` row
wiring the already-registered `raise_challenge` action_type to a workflow).

## Candidate next slices

None of these are scoped or implemented yet. Listed in roughly the order
they'd naturally need to happen (later items depend on earlier ones
existing), not in priority order.

1. **Explicit configured challenge-stage/rule gating.**
   Replace the transitional workflow-status gate with a real config check:
   either a `workflow_stage` row with `lifecycle_stage = 'challenge'` on
   the relevant workflow, a `rule_definition` row using the existing
   `raise_challenge` action_type, or both. Should not hardcode which
   workflows/classes allow challenges — same discipline as
   `workflow_definition.applies_to_*` in session-019.

2. **Challenge resolution / dismissal / withdrawal.**
   `challenge_status` currently never advances past `raised`
   (`under_review` / `resolved` / `dismissed` / `withdrawn` are seeded but
   unused). Needs its own transactional service and endpoint(s), plus
   deciding whether resolving a challenge should also unblock the
   `workflow_instance` (and whether that unblock is automatic or requires
   an explicit adjudication outcome first).

3. **Adjudication of a raised challenge.**
   The `adjudicate_challenge` workflow_task this slice creates is currently
   inert -- nothing ever marks it `completed`. This slice would need an
   adjudication decision/outcome model, standing/authority checks for who
   may adjudicate, and would likely produce the actual state transition
   that resolution (#2) depends on.

4. **Repair path if a challenge is sustained.**
   If adjudication sustains a challenge, what happens to the original
   decision? This connects to `cdp_repair` (per RFC material on repair
   plane reanchoring) and is likely its own multi-step vertical slice, not
   an extension of the challenge-transition service itself.

## Open questions carried forward

- Should challenge admission differ by `challenge_type` (e.g. an `apc`
  challenge_type having different preconditions than `policy`)? Not
  addressed by the transitional gate.
- Should a second challenge against an already-blocked workflow_instance
  behave differently (reject, merge into the existing adjudication task)
  rather than opening a new `adjudicate_challenge` task each time? Current
  behavior (session-020): each challenge opens its own task, untested.
