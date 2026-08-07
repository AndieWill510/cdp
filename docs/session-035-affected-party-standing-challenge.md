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
- Two outcomes written by this slice's service layer: `recognized`,
  `denied` (§11.8's full five-value vocabulary is seeded at the database
  layer; `narrowed`, `deferred`, and `rejected` are reserved, not yet
  reachable, mirroring `authority_evaluation_result`'s precedent of
  seeding a wider vocabulary than a table CHECK currently admits).
  `narrowed` is withheld specifically, not merely deferred alongside the
  other two: RFC-CDP-033 §9.2's determination schema includes
  `outcome_scope` to record what a narrowing actually narrows to, and
  this table omits that column. A pre-merge review of this PR correctly
  identified that writing `narrowed` without a recorded scope would be
  enforcement-indistinguishable from `recognized` at the Challenge gate
  while still asserting a narrowing the system cannot describe — a truth
  problem, not just a missing feature. `narrow_standing_claim` and the
  `POST /standing-claims/{claim_id}/narrow` route were removed before
  merge; the determination table's `CHECK` constraint now admits only
  `recognized`/`denied`, and `narrowed` remains seeded in the
  vocabulary table only, for a future session that adds `outcome_scope`.
- A single, bounded, seeded actor — `cdp_standing_recognition_authority`
  — is the only actor authorized to recognize or deny a claim, and may
  not determine a claim where it is itself the claimant. This satisfies
  RFC-CDP-033 §11.5 (Draft v0.7)'s four required properties (bounded,
  non-self-interested, procedurally authorized, auditable) without the
  RFC naming a specific actor, mirroring the precedent sessions 027/028
  set for `cdp_identity_recognition_authority` /
  `cdp_authority_grant_issuer`.
- `submit_affected_party_standing_claim`, `recognize_standing_claim`,
  `deny_standing_claim` (`cdp/core/services.py`) and
  `POST /standing-claims`, `GET /standing-claims/{claim_id}`,
  `POST /standing-claims/{claim_id}/{recognize,deny}`
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
  A `recognized` determination also permits it; only a `denied`
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
- The `narrowed` recognition outcome. Seeded in the
  `standing_recognition_outcome` vocabulary; not writable by
  `cdp_core.standing_recognition_determination`'s own `CHECK` constraint,
  not exposed by any service function or route. See §2.1.

### 2.1 Pre-merge review correction: `narrowed` deferred

The version of this slice first opened as PR #53 implemented `narrowed`
as a third writable outcome, alongside `recognized` and `denied`, and
`attest_and_raise_challenge`'s gate treated a `narrowed` determination as
fully sufficient to permit the Challenge — identically to `recognized`.

Review before merge correctly identified this as a genuine defect, not a
style nit: RFC-CDP-033 §9.2's Standing Recognition Determination schema
includes `outcome_scope` specifically to record *what* a narrowing
narrows to, and this table's implementation of that schema omits the
column. Writing a `narrowed` determination with no recorded scope made it
enforcement-indistinguishable from `recognized` — the Challenge gate could
not have behaved any differently for a narrowed claim even if it wanted
to — while the stored record still asserted that a narrowing had
occurred. That is a truth problem: the system would have claimed to know
something (how the claim was narrowed) that it could not actually
express anywhere.

The fix, applied before merge:

- `narrow_standing_claim` (service) and the
  `POST /standing-claims/{claim_id}/narrow` route (API) were removed
  entirely, not merely deprecated.
- `cdp_core.standing_recognition_determination`'s `chk_standing_determination_outcome_value`
  constraint now admits only `'recognized'` and `'denied'`.
- `narrowed` remains seeded in the `standing_recognition_outcome`
  vocabulary table, annotated as reserved until a future session adds an
  `outcome_scope` column and teaches the Challenge gate to honor it.
- Tests updated accordingly: the two removed-outcome service tests are
  replaced by a test pinning `narrow_standing_claim`'s absence and a test
  proving the database itself rejects a direct `narrowed` insert; the API
  suite gained a test proving `POST .../narrow` now 404s as an
  unregistered route; the migration test asserting "three outcomes" was
  replaced with one asserting exactly two, plus a test that `narrowed`
  is still present in the vocabulary seed but absent from the
  determination table's own `CHECK`.

This is deferral, not removal of the concept — RFC-CDP-033 still
describes `narrowed` as a legitimate outcome, and the vocabulary and RFC
text are both untouched. What changed is that this slice no longer
*claims* to support an outcome it cannot honestly enforce.

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
- `tests/migration/test_migration_015_standing_and_recusal.py` — 16 tests
  (15 static, 1 Postgres smoke).
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

`docs/SESSION-INDEX.md`, `evidence/000-current-state.md`,
`evidence/001-test-matrix.md`, `evidence/002-demonstrated-capabilities.md`,
and `evidence/003-known-gaps.md` were updated citing CI run `31146632317`
(commit `868f191`, `full-cdp-slice-tests` and `pr-guard` both `success`)
once that run confirmed passing, following the same discipline every
prior implementation session in this repository used — an evidence-level
claim was not made in those documents until a citable CI run backed it.

### 5.1 Re-verification after the `narrowed` correction (§2.1)

After the `narrowed`-deferral fix described in §2.1, the full local
verification in this section was re-run against a rebuilt `cdp-api`
image and the same live Postgres:

- `ruff check cdp` — passes, zero findings.
- `tests/migration/test_migration_015_standing_and_recusal.py` — 16
  tests, all pass (up from 15: the three-outcome static assertion was
  replaced with a two-outcome assertion plus a new test confirming
  `narrowed` is seeded but not permitted by the `CHECK` constraint).
- `tests/standing/test_standing_claim_service.py` — 21 tests, all pass
  (the removed `test_narrow_happy_path` and
  `test_narrowed_claim_permits_challenge` are replaced by
  `test_narrow_standing_claim_does_not_exist` and
  `test_narrowed_outcome_rejected_by_the_database`).
- `tests/standing/test_standing_claim_api.py` — 15 tests, all pass (up
  from 14: `test_recognize_narrow_deny_each_require_a_fresh_claim` is
  renamed and narrowed to `test_recognize_and_deny_each_require_a_fresh_claim`;
  new `test_narrow_route_does_not_exist` confirms `POST
  .../narrow` now returns FastAPI's own `404` for an unregistered route).
- The full pre-existing service suite (139 tests) and API suite (71
  tests) re-run alongside the above — zero regressions.

This document's evidence citations (§5 above, and the four `evidence/`
files) still point to CI run `31146632317`, the run that confirmed the
implementation *before* this correction. That run remains valid evidence
for everything it actually tested (the schema, the gate mechanics, the
optional-parameter behavior) since none of that changed; it is simply no
longer the complete picture for the outcome vocabulary specifically. A
fresh CI run on the corrected commit will supersede it as the citation of
record once available — see the evidence files for whichever citation is
current.

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
