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
| 027 | `session-027-identity-and-attestation` (PR #41) | Identity and Attestation vertical slice (`db/ddl/010-identity-and-attestation.sql`, Actor Registry, Identity Claim, Attestation Record, `attest_and_create_decision` proof path via `POST /attested-decisions`). Explicitly out of scope: Authority, Standing, Legitimize, Repair, real cryptographic verification, OAuth/SSO/password storage. v0.2 corrected two review findings: attestor/subject conflation, and unbounded identity-claim recognition. | [docs/session-027-identity-and-attestation.md](session-027-identity-and-attestation.md) | v0.2 CI passing (run `30704929899`); open, not yet reviewed/merged |

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
