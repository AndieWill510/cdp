# CDP Implementation Session Index

This indexes the **implementation / vertical-slice track**: sessions that
add or checkpoint executable CDP code (`cdp/`, `db/ddl/`, `tests/`,
`.github/workflows/`), numbered `docs/session-0NN-*.md`.

This is a distinct track from `collab/sessions/001`–`019`, which indexes
RFC design, deliberation, and adjudication sessions. The two tracks
happen to share one continuous number sequence across the repo's history,
but they are not the same kind of session and are not interchangeable —
see the cross-reference note in `collab/INDEX.md`.

Facts below are taken directly from `git log --merges` (PR numbers, branch
names, merged file lists), not reconstructed from memory or chat.

## Sessions

| Session | Branch(es) / PR(s) | Topic | Doc file | Status |
|---|---|---|---|---|
| 020 | `session-020-challenge-transition` (PR #21); `session-020-challenge-transition-impl` (PR #22) | Challenge transition — design note, then executable implementation (`db/ddl/005-challenge-transition.sql`, challenge service/API) | [docs/session-020-challenge-transition.md](session-020-challenge-transition.md) | merged; doc covers the design note, not the separate impl PR |
| 021 | `session-021-challenge-policy-followups` (PR #23) | Challenge policy follow-ups | [docs/session-021-challenge-policy-followups.md](session-021-challenge-policy-followups.md) | merged |
| 022 | `session-022-challenge-adjudication` (PR #24) | Challenge adjudication vertical slice (`db/ddl/006-audit-event-ordering.sql`, `007-challenge-adjudication.sql`, adjudication service/API) | — | merged; **no dedicated session doc was written** — context-plane gap, not reconstructed here |
| 023 | `session-023-ci-for-cdp-slices` (PR #25) | Cost-controlled CDP slice CI (`.github/workflows/cdp-ci.yml`) | — | merged; **no dedicated session doc was written** — context-plane gap, not reconstructed here |
| 024 | `session-024-architecture-checkpoint` (PR #26) | Architecture checkpoint summarizing sessions 019–023; no implementation in this session | [docs/session-024-architecture-checkpoint.md](session-024-architecture-checkpoint.md) | merged |
| 025 | `session-025-execution-authorization` (PR #27) | Execution authorization vertical slice (`db/ddl/008-execution-authorization.sql`, execution-authorization service/API) | — | merged; **no dedicated session doc was written** — context-plane gap, not reconstructed here |
| 026 | `session-026-execution` | Execution Attempt → Execution Record vertical slice (`db/ddl/009-execution-record.sql`, `record_execution_attempt`, execution-record API). Explicitly out of scope: repair implementation, repair workflow, repair verification, learning, workflow closure. | [docs/session-026-execution-record.md](session-026-execution-record.md) | merged (PR #28) |
| 027 | `session-027-identity-and-attestation` (PR #41) | Identity and Attestation vertical slice (`db/ddl/010-identity-and-attestation.sql`, Actor Registry, Identity Claim, Attestation Record, `attest_and_create_decision` proof path via `POST /attested-decisions`). Explicitly out of scope: Authority, Standing, Legitimize, Repair, real cryptographic verification, OAuth/SSO/password storage. v0.2 corrected two review findings: attestor/subject conflation, and unbounded identity-claim recognition. | [docs/session-027-identity-and-attestation.md](session-027-identity-and-attestation.md) | merged (PR #41, merge commit `2b2cc5c`) |
| 028 | `session-028-authority-and-delegation` (PR #43) | Authority and Delegation vertical slice (`db/ddl/011-authority-and-delegation.sql`, Authority Grant, Authority Evaluation Result, bounded grant issuer, `attest_and_create_decision` extended with a PROPOSE-authority gate), scoped to RFC-CDP-032 §19 Minimal Compliance. Explicitly out of scope: delegation, quorum, separation-of-duties enforcement, emergency/repair/sovereignty authority. | [docs/session-028-authority-and-delegation.md](session-028-authority-and-delegation.md) | merged (PR #43, merge commit `c508c6d`) |
| 029 | `session-029-universal-attestation` (PR #44) | Universal Attestation vertical slice (`db/ddl/012-universal-attestation.sql`, additive `governed_act_ref_id` on `attestation_record`/`authority_evaluation_result`; four new `attest_and_*` proof paths — challenge raising, challenge adjudication, execution authorization, execution recording). Explicitly out of scope: Test/Legitimize/Learn attestation, attestation of the Identity/Attestation/Authority slices' own mutations. | [docs/session-029-universal-attestation.md](session-029-universal-attestation.md) | merged (PR #44, merge commit `7311c8c`) |
| 030 | `session-030-identity-claim-scope` (PR #46) | Richer scope semantics for Identity Claims (`db/ddl/013-identity-claim-scope.sql`, optional `scope_registry_name`/`scope_decision_class_id` on `cdp_core.identity_claim`, mirroring `authority_grant`'s two-level scope model), enforced in `_check_claim_recognized_and_scoped` across all five `attest_and_*` proof paths. Explicitly out of scope: RFC-CDP-032 Authority changes, real caller authentication, RFC-CDP-030/031 spec edits, a general/composable scope grammar. | [docs/session-030-identity-claim-scope.md](session-030-identity-claim-scope.md) | merged (PR #46, merge commit `53d292d`) |
| 031 | `session-031-rfc-spec-updates` (PR #47) | RFC-CDP-030/031 spec updates (documentation-only): fixes both files' stale internal header (RFC-CDP-012/RFC-CDP-011 from before renumbering), bumps both to Draft v0.4, and adds an Implementation Status section to each documenting the schema/behavior sessions 027-030 actually built, including an explicit statement that RFC-CDP-031 §4's cryptographic verification requirements are not implemented. No code changed. | [docs/session-031-rfc-spec-updates.md](session-031-rfc-spec-updates.md) | merged (PR #47, merge commit `82ad056`) |
| 032 | `session-032-caller-authentication` (PR #48; post-merge review fixes PR #49) | Real authentication / caller binding (`db/ddl/014-caller-authentication.sql`, `cdp_core.actor_bearer_token`; `register_actor` issues a one-time bearer token; `verify_bearer_token` gates nine actor-asserting mutating routes; self-service `POST /actors/{actor_id}/tokens/revoke`). Explicitly out of scope: OAuth2/OIDC/SSO, cryptographic request signing, token rotation, TLS. Closes the last of the five follow-up items from the PR #41 evidence-layer review. Reviewed twice: pre-merge (PR #48 -- privileged seed credentials moved out of the canonical migration path into `db/seed/`, revoke response redacted, transaction-boundary check/use gap recorded in known gaps) and post-merge (PR #49 -- stale docstring/evidence-header fixes, `Migration014IsolatedDatabaseTests` added to prove the zero-privileged-tokens invariant in CI rather than only manually). | [docs/session-032-caller-authentication.md](session-032-caller-authentication.md) | merged (PR #48, merge commit `660e744`; PR #49, merge commit `199c934`) |

### Sessions 027-032: Identity, Attestation, Authority, and Caller Authentication -- closed sequence

Sessions 027 through 032 form one continuous implementation arc and are
now **closed** as of main `199c934`: the bounded scope this sequence set
out to cover -- governed actor identity, claim-based attestation,
RFC-CDP-032 §19 Minimal Compliance authority, and real bearer-token
caller-to-actor binding -- is implemented, tested, reviewed (including
one post-merge review pass), corrected, and merged, all at Integration
Tested (E4). See
[docs/session-027-032-identity-authority-closure.md](session-027-032-identity-authority-closure.md)
for the full closure statement: what was built, the evidence level
reached, what remains explicitly out of scope, and the recommended next
constitutional gap (Standing and Recusal, RFC-CDP-033).

## Known gaps

- Sessions 022, 023, and 025 were merged to `main` with real, verifiable
  implementation (see PR file lists above via `git show --stat`) but have
  no corresponding `docs/session-0NN-*.md` handoff file. This is
  documented context-plane debt, per the same principle as the Session 016
  repair note in `collab/INDEX.md` §"Context-Plane Repair Note." It is
  **not** backfilled here — only 020, 021, 024, and now 026 have narrative
  doc files, and that asymmetry is recorded rather than papered over.
- This index itself did not exist before Session 026. Prior to this file,
  the implementation track had no index at all; a reader had to already
  know to look for `docs/session-0NN-*.md` files by convention.
