# Session 024 — Architecture Checkpoint

Status: checkpoint/summary only. No implementation in this session.
Covers: session-019 through session-023 (PRs #20, #22, #24, #25), merged
into `main`.

This note exists so the next session (or the next person) can orient
against the current executable CDP spine without re-deriving it from git
history and four sessions of chat.

## 1. Current executable lifecycle

Four transactional slices, all live on `main`, all exercised end-to-end
against the running local stack and in CI:

1. **Decision creation** (`create_decision_with_workflow`,
   `POST /decisions`) — inserts a decision, resolves its configured
   workflow and first stage, opens an initial blocking review task, and
   commits with a `decision.created` / `workflow.started` / `task.created`
   audit trail.
2. **Challenge raising** (`raise_challenge_for_decision`,
   `POST /decisions/{registry_name}/{decision_id}/challenges`) — inserts a
   durable `challenge_record`, blocks the decision's workflow instance,
   opens an `adjudicate_challenge` task, and commits with a
   `challenge.raised` / `workflow.transitioned` / `task.created` audit
   trail.
3. **Challenge adjudication** (`adjudicate_challenge`,
   `POST /decisions/{registry_name}/{decision_id}/challenges/{challenge_id}/adjudications`)
   — records a `challenge_adjudication_record` (outcome + rationale +
   actor), updates `challenge_status`, completes the adjudication task for
   terminal outcomes, unblocks the workflow instance only if no other
   challenge on the same decision is still open, and commits with a
   `challenge.adjudicated` / `workflow.transitioned` / `task.completed`
   audit trail (only `challenge.adjudicated` for a `deferred` outcome).
4. **Deterministic audit ordering** — `cdp_audit.event_log.event_sequence`
   (a monotonic identity column, added in `006-audit-event-ordering.sql`)
   orders every audit trail above. This was a foundational fix, not part
   of the original plan: `created_at` alone cannot order same-transaction
   events because Postgres's `now()` is transaction-stable, so multiple
   events written in one service call previously shared an identical
   timestamp with no reliable ordering.
5. **Cost-controlled CI** (`.github/workflows/cdp-ci.yml`) — a cheap
   `pr-guard` job (ruff + static migration/DDL tests, no DB) runs on every
   PR; the full Postgres-backed `full-cdp-slice-tests` job (DB-required
   migration tests, all three service tiers, API round-trip tests) runs
   only on push to `main`, manual dispatch, or a PR labeled `run-full-ci`.
   Verified working end-to-end on a real push to `main` (both jobs green).

## 2. Current architectural invariants

These are the rules every slice above was built to, and the next slice
should be held to the same standard:

- **Configured workflow resolution, not hardcoded workflow selection.**
  Which workflow applies to a decision is resolved through
  `workflow_definition.applies_to_registry_name` /
  `applies_to_decision_class_id`, never a hardcoded `workflow_code`.
- **Governed artifacts, not loose text fields.** A challenge is
  `cdp_core.challenge_record`, not a text column on the decision. A
  challenge adjudication is `cdp_core.challenge_adjudication_record` —
  durable identity, raising/adjudicating actor, controlled-vocabulary
  outcome, rationale, timestamps, relationship to the decision and to the
  task it affects — not a bare status flip.
- **Transactional writes.** Every slice is one connection, one
  transaction, one commit; any failure rolls back all of it (decision +
  workflow + task + audit events, or challenge + workflow unblock + task
  completion + audit events). Proven by dedicated atomicity/rollback tests
  in every slice, not just asserted.
- **Audit events correlated by `registry_name`/`decision_id`.** Every audit
  payload carries both, learned the hard way after session-019's first
  draft filtered by `aggregate_id` and silently missed two of three events
  per transaction (their aggregate is the workflow_instance/task UUID, not
  the decision).
- **Audit order by `event_sequence`, not `created_at`.** See item 4 above.
  Any new audit-ordering test or query must use `event_sequence`.
- **Dormant stacks remain untouched.** `prototype/`, `src/cdp_control_plane/`,
  and `scripts/init_db.sql` have had zero changes across all of
  sessions 019–023, verified explicitly before every commit.

## 3. What remains out of scope

Explicitly not implemented, not partially implemented, not stubbed:

- Full RFC-CDP-044 decision-level adjudication (dispositions like
  `approve_for_legitimacy_review` / `escalate` / `defer_pending_test` /
  `refer_to_sovereignty_process`, Participation Integrity treatment). What
  exists is challenge-level adjudication only — deliberately named
  `challenge_adjudication_record` to keep that broader name free.
- Legitimation as a final/declarative "this decision is legitimate" concept.
  (The narrower *execution authorization gate* recommended in section 5 is
  not this — see that section for the distinction.)
- Execution (the act of carrying a decision out).
- Repair (including the `referred_to_repair` adjudication outcome, which
  exists as vocabulary only — no repair-plane wiring).
- Appeal.
- Standing/authority/recusal checks. `adjudicated_by_actor_id`,
  `raised_by_actor_id`, etc. are validated only for identifier-registry
  registration, not for `ADJUDICATE` authority, standing, or recusal.
- Participation integrity.
- Sovereignty process.
- Full Docker Compose CI (Qdrant/Redis/LocalStack) — `test_build_verification.py`
  and `test_codex_test_loop.py` remain local-only/stage-2 CI candidates.

## 4. Recommended next slice options

- **Execution authorization after challenge adjudication** (the
  lifecycle's legitimation gate, framed as an authorization to proceed
  rather than a declaration of final legitimacy — see section 5).
- **Repair path for sustained/referred challenges.**
- **Execution transition.**
- **Authority/standing checks** (across decision creation, challenge
  raising, and adjudication).
- **Configured challenge-stage/rule gating** — replacing the transitional
  non-terminal-workflow-status gate flagged in sessions 020/021 as
  provisional, not final policy.
- **Full-stack CI hardening** (bring Qdrant/Redis/LocalStack into CI).

## 5. Recommendation

**`execution_authorization` after challenge adjudication** — session name
`session-025-execution-authorization`, not `session-025-legitimation-transition`.

### Naming: why not "legitimation"

The lifecycle vocabulary already seeded in 003 calls this stage
`legitimize`, and the underlying conceptual primitive is the same gate.
But "legitimation" as an operational artifact name risks sounding like CDP
is declaring a decision fully, finally, procedurally legitimate — a much
bigger claim than what this slice actually does, and one that invites a
short-circuit reading:

```
proposal created → authorized → execute
```

with no check that blocking challenge work is actually resolved. That is
explicitly not what this slice means. What it means is narrower and
operational:

> This decision is authorized to proceed to execution under the current
> workflow conditions.

Not:

> This decision is morally/procedurally/finally legitimate forever.

So the artifact is named `cdp_core.execution_authorization_record`, and
API/event language should stay centered on "authorized to proceed," not
"declared legitimate." The lifecycle's `legitimize` stage/vocabulary can
still be the underlying alignment point at the DDL level if inspection at
implementation time shows that's the cleaner fit — but the operational
naming (table, service, events, API) should be `execution_authorization`
throughout, per Andie's preference, because it is clearer and less
philosophically overloaded.

### The gate must not bypass unresolved challenges

This is the load-bearing rule, not a footnote: **a decision may receive
execution authorization only when no blocking challenge work remains
open.**

- Blocking `challenge_status` values: `raised`, `under_review`.
- Non-blocking for authorization eligibility: `resolved`, `dismissed`, `withdrawn`.

The future slice should fail with 409 if any blocking challenge remains —
same discipline as every prior slice's fail-closed error mapping, not a
soft warning.

### Expected shape of the future slice (not implemented yet)

```
existing decision
→ verify workflow exists
→ verify no open blocking challenges
→ verify no open adjudicate_challenge task remains
→ create execution_authorization_record
→ update workflow/task state if appropriate
→ append audit event(s)
→ commit atomically
```

It should **not** implement execution itself. Execution authorization says
"this may proceed"; execution says "this was carried out." Those are
separate governed acts, and conflating them would repeat the exact
short-circuit risk this renaming is trying to avoid.

### Why this over the other candidates

- It's the next stage the lifecycle vocabulary already commits to, and
  closes the larger structural hole: right now a decision with no
  challenge, or a challenge that resolves `not_sustained`/`dismissed`,
  has **no defined next step at all**. That's a bigger gap than the
  technical-debt items (transitional gating, missing authority checks),
  because it affects the common path, not an edge case.
- It reuses every invariant in section 2 with no new infrastructure:
  transactional service, governed artifact, controlled vocabulary,
  workflow/task interaction, `event_sequence`-ordered audit trail.
- **Repair remains important but is downstream or parallel, not blocking.**
  When a challenge is sustained or `referred_to_repair`, that decision
  does not receive execution authorization at all (blocked by the gate
  above) — repair becomes the relevant next step for *that* decision, on
  its own track. Repair and execution-as-an-act are both real future
  slices; this one only decides whether a decision is clear to move
  forward, not what happens on either branch after that.
- Configured challenge-stage/rule gating and authority/standing checks are
  legitimate hardening work, but they harden *existing* endpoints rather
  than closing the missing-next-step gap above. Worth doing, but I'd
  sequence them after execution authorization exists, not before.

### Explicitly still out of scope

Full RFC-CDP-044 decision-level adjudication, repair execution,
standing/authority/recusal checks, participation integrity, and
sovereignty process all remain out of scope for this slice, same as
section 3.

Not implementing yet — this is the recommendation, pending your decision.
