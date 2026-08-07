# Session 035 — Affected-Party Standing for Challenge-Raising

Status: implementation session. Follows the sequence
[docs/session-033-standing-recusal-recon.md](session-033-standing-recusal-recon.md)
(PR #51, reconnaissance) →
[docs/session-034-rfc-033-standing-recognition-clarification.md](session-034-rfc-033-standing-recognition-clarification.md)
(PR #52, RFC-CDP-033 clarified to Draft v0.7) → this session (the
implementation slice both of those sessions explicitly deferred).

## 1. Purpose

Implement the narrowest bounded slice of RFC-CDP-033 (Standing and
Recusal) that can reach Integration Tested (E4): Constitutional
Affected-Party Standing, gating Challenge-raising only. This is the
"minimum implementation slice" both prior sessions proposed and refined,
now built, tested, and verified against a live database and a live API,
following the same discipline sessions 027–032 used for Identity,
Attestation, and Authority.

## 2. Scope

**Implemented:**

- `cdp_core.standing_claim` — a Standing Claim (RFC-CDP-033 §9.1),
  immutable once inserted (forbid-delete and forbid-update triggers).
  Minimal sufficiency (§11.4: "identifies a possible consequence and the
  relationship that makes the actor answerable to it") is enforced at the
  database layer — `claimed_impact` must be non-blank, and at least one of
  `standing_basis_role` / `standing_basis_accountability` /
  `standing_basis_contextual_relationship` must be non-blank.
- `cdp_core.standing_recognition_determination` — a Standing Recognition
  Determination (§9.2), a *separate*, also-immutable record referencing
  the claim it determines, never an edit to the claim itself. This slice
  permits exactly one determination per claim (`UNIQUE(claim_id)`);
  chained/corrected determinations are named future work, not silently
  allowed or forbidden.
- Three outcomes written by this slice's service layer: `recognized`,
  `narrowed`, `denied` (§11.8's full five-value vocabulary is seeded at
  the database layer; `deferred` and `rejected` are reserved, not yet
  reachable, mirroring `authority_evaluation_result`'s precedent of
  seeding a wider vocabulary than a table CHECK currently admits).
- A single, bounded, seeded actor — `cdp_standing_recognition_authority`
  — is the only actor authorized to recognize, narrow, or deny a claim,
  and may not determine a claim where it is itself the claimant. This
  satisfies RFC-CDP-033 §11.5 (Draft v0.7)'s four required properties
  (bounded, non-self-interested, procedurally authorized, auditable)
  without the RFC naming a specific actor, mirroring the precedent
  sessions 027/028 set for `cdp_identity_recognition_authority` /
  `cdp_authority_grant_issuer`.
- `submit_affected_party_standing_claim`, `recognize_standing_claim`,
  `narrow_standing_claim`, `deny_standing_claim`
  (`cdp/core/services.py`) and `POST /standing-claims`,
  `GET /standing-claims/{claim_id}`,
  `POST /standing-claims/{claim_id}/{recognize,narrow,deny}`
  (`cdp/api/standing.py`).
- An **optional** Standing gate on `attest_and_raise_challenge`: a new
  `standing_claim_id` field on `AttestedChallengeInput` /
  `AttestedChallengeCreateRequest`. When supplied, the referenced claim is
  verified (belongs to the attesting actor, matches this decision and the
  `challenge` stage, has no `denied` determination) before the challenge
  is raised. **When omitted, challenge-raising is completely unaffected**
  — this is additive, not a new blanket requirement.
- Provisional Standing, proven end to end: a minimally sufficient claim
  with **no determination yet** is sufficient to raise the challenge.
  `recognized` and `narrowed` determinations also permit; only a `denied`
  determination blocks. This is the specific correction requested and
  applied to PR #51's reconnaissance doc, now actually implemented and
  tested — see §5 below for the exact test that proves it.

**Not implemented, deliberately (named, not hidden):**

- Recusal, in its entirety. No table, no check, no route. RFC-CDP-033
  §7/§10 remain unenforced code.
- Every Standing type other than Constitutional Affected-Party
  (Evidence-Custodian, Record-Keeper, Delegated, Emergency, Repair,
  Appeal, AI Functional). The `standing_type` vocabulary seeds all seven;
  the service layer accepts exactly one.
- Automatic Breach Record generation on a `denied` outcome (RFC-CDP-033
  §11.6). RFC-CDP-072 (Breach Record and Repair Agenda Schema) itself
  remains E0 in this repository — there is nothing to generate a Breach
  Record *in*. `deny_standing_claim`'s docstring names this explicitly.
- The enforcement-projection half of RFC-CDP-033 §12's two-layer
  persistence model. Only the canonical claim/determination shape exists.
- Standing for any lifecycle stage other than Challenge.
- Database-level non-revocation enforcement for Constitutional Standing
  (§12) — not applicable yet since nothing here is ever revoked, only
  determined once.
- Any change to the plain, unattested `POST /decisions/{registry}/
  {decision}/challenges` route, or to `attest_and_create_decision`. Only
  `attest_and_raise_challenge` gained the new optional parameter.

## 3. Why the Standing gate is optional, not mandatory

RFC-CDP-033 §6's stage-specific Standing matrix names several distinct
bases for Challenge standing — affected party, domain expert, governance
authority — and this slice implements only one of them (Affected-Party).
Making `standing_claim_id` mandatory for every attested-challenge caller
would therefore functionally deny standing to every legitimate
non-affected-party challenger this slice does not model, which is exactly
what RFC-CDP-033 §11.2 forbids: non-recognition must never be read as
non-existence. The gate only runs when a caller supplies
`standing_claim_id`; every existing caller and test that doesn't is
completely unaffected — confirmed by
`test_challenge_without_standing_claim_id_is_unaffected` (service) and
`test_attested_challenge_without_standing_claim_id_is_unaffected` (API),
and by the full pre-existing test suite passing unchanged (§5).

## 4. Files

- `db/ddl/015-standing-and-recusal.sql` — new migration: two tables, three
  controlled-vocabulary registries (`standing_stage`, `standing_type`,
  `standing_recognition_outcome`), one seeded bounded actor.
- `cdp/core/repositories/standing.py` — new repository (insert/fetch for
  both tables, no update, no delete).
- `cdp/core/services.py` — new Standing section (exceptions, dataclasses,
  `submit_affected_party_standing_claim`, `_determine_standing_claim` plus
  its three named wrappers); `AttestedChallengeInput` gains
  `standing_claim_id`; `attest_and_raise_challenge` gains the optional
  gate, described fully in its own docstring.
- `cdp/api/standing.py` — new route module (four routes).
- `cdp/api/decisions.py` — `AttestedChallengeCreateRequest` gains
  `standing_claim_id`; the route passes it through and adds three new
  exception-to-HTTP-status mappings
  (`StandingClaimActorMismatch`/`StandingClaimDecisionMismatch` → 409,
  `StandingClaimNotSufficient` → 403).
- `cdp/api/main.py` — registers the new router.
- `db/seed/dev-caller-authentication-tokens.sql` — adds a third bounded
  actor's local/dev/test token (`cdp_standing_recognition_authority`),
  published in plaintext there per that file's existing, explicit
  discipline — never in the canonical `db/ddl/` migration path (confirmed
  by `test_migration_does_not_seed_any_tokens` and by
  `Migration014IsolatedDatabaseTests`, which globs every `db/ddl/*.sql`
  file and asserts zero privileged tokens in a genuinely fresh, isolated
  database — this session's 015 migration is automatically covered by
  that existing regression test without any change to it).
- `tests/migration/test_migration_015_standing_and_recusal.py` — 15 tests
  (13 static, 2 Postgres smoke).
- `tests/standing/test_standing_claim_service.py` — 21 tests, split into
  `StandingClaimTests` (submission, determination, authorization,
  immutability) and `ProvisionalStandingChallengeGateTests` (the gate
  itself, including the provisional-standing proof).
- `tests/standing/test_standing_claim_api.py` — 14 API round-trip tests.
- `.github/workflows/cdp-ci.yml` — registers all three new test files at
  their correct CI stage (static / Postgres smoke / service / API).

## 5. Verification performed this session

No CI run had completed at the time this document was first written in
this session — verification below was run locally against this
repository's own Docker Compose stack (`cdp-postgres`, rebuilt `cdp-api`),
using the exact same commands `.github/workflows/cdp-ci.yml` runs, before
pushing:

- `ruff check cdp` — passes, zero findings.
- The full `pr-guard` static test list (132 tests, including all 13 new
  015-migration static tests) — all pass.
- The full `full-cdp-slice-tests` migration/service test list (142 tests,
  including the new 015 Postgres smoke tests and all 21 new Standing
  service tests) — all pass, with **zero regressions** in any
  pre-existing test (decision, challenge, adjudication, execution,
  identity, attestation, authority, universal attestation).
- The full API round-trip test list (70 tests, including all 14 new
  Standing API tests) — all pass, zero regressions.
- `Migration014IsolatedDatabaseTests` (creates a genuinely fresh, isolated
  database, applies every `db/ddl/*.sql` file present on disk, asserts
  zero privileged tokens for the bounded actors) — passes, automatically
  covering the new `cdp_standing_recognition_authority` actor without any
  change to that test.
- An end-to-end manual smoke script (service layer, then repeated at the
  HTTP API layer) proving the exact claim this slice exists to prove:
  register an actor, recognize its identity claim, grant it `CHALLENGE`
  authority, submit a minimally sufficient affected-party standing claim,
  **raise a challenge referencing that claim before any determination
  exists** (succeeds), attempt self-determination (rejected), attempt
  determination by a non-authority actor (rejected), deny the claim,
  attempt a second determination on the same claim (rejected, 409),
  attempt a further challenge referencing the now-denied claim (rejected,
  403).

`docs/SESSION-INDEX.md` and `evidence/000-current-state.md` /
`evidence/003-known-gaps.md` will be updated with the actual CI run ID
once this branch's PR has a confirmed passing `full-cdp-slice-tests` run,
following the same discipline every prior implementation session in this
repository used — an evidence-level claim is not made in this document
until a citable CI run backs it.

## 6. What remains E0 after this session

Recusal in its entirety; every Standing type other than Affected-Party;
automatic Breach Record generation; the enforcement-projection half of
the persistence model; Standing for Propose, Test, Adjudicate, Legitimize,
Execute, Record, or Learn; Test, Legitimize, Learn, and the entire
RFC-CDP-070 Repair/Appeals band remain unimplemented, unaffected by this
session.

## 7. Recommended next steps

- Extend the Standing gate to Adjudicate or Legitimize once those stages'
  proof paths exist and RFC-CDP-033's recusal sections are ready to be
  implemented alongside them — Standing without Recusal at those stages
  is exactly the "authority capture through participation" failure mode
  RFC-CDP-033 §2 names.
- Implement RFC-CDP-072 (Breach Record and Repair Agenda Schema) before
  attempting automatic Breach Record generation on `denied` outcomes —
  do not invent a Breach Record shape as a side effect of a future
  Standing session.
- Revisit the anti-flooding/anti-retaliation gap named in session 033's
  recon (finding 4.2(f)) before Standing claims are exposed to any
  untrusted or adversarial population — nothing in this slice bounds how
  many claims a given actor may submit.
