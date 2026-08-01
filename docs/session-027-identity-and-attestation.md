# Session 027 — Identity and Attestation

Status: implementation complete, verified locally against a live Docker
Compose stack and confirmed passing in CI on PR #41 (run `30677856180`,
head commit `70ef08b`). Not yet reviewed/merged. This file documents what
already exists in the working tree, not a plan for future work.

Scope: **Identity and Attestation** (RFC-CDP-030 Identify Protocol,
RFC-CDP-031 Attest Protocol), the constitutional goal being: CDP can
establish who performed a governed act, what evidence supports that
attribution, and whether the act was properly attested — without
collapsing identity into personhood, public exposure, standing, authority,
or answerability.

## 1. Constitutional scope note (read this first)

RFC-CDP-030 and RFC-CDP-031 are both thin — Draft v0.3, ~40 lines each,
with no persistence-schema section, and their file headers still carry a
stale internal title ("RFC-CDP-012"/"RFC-CDP-011" respectively) from
before they were renumbered into the 030/031 slots. Neither RFC specifies
an Identity Claim or Attestation Record schema with the richness this
slice's constitutional brief required (recognition status,
contestability, supersession, protected/pseudonymous display).

This implementation composes RFC-CDP-030/031's minimal required-properties
lists with two things: RFC-CDP-033 §11.2's existence/recognition/scope
distinction (an actor exists independently of CDP; a claim states who an
actor claims to be; recognition is a separate CDP act that does not create
the actor or prove everything about it) and RFC-CDP-033 §11.6's non-erasure
rule (denial does not extinguish the underlying claim). This is a
documented interpretation of an underspecified corpus area, filling the
gap with the constitutional constraints supplied directly for this
session, not a silent invention hidden in code. Per the review discipline
this session followed, this gap was surfaced before implementation began,
not discovered after.

## 2. What this slice does

Three new governed objects, one new migration, three new repositories,
six new service functions, nine new API routes, and one new proof-path
integration with existing decision creation.

### 2.1 Actor Registry (`cdp_core.actor`)

Elaborates an existing `cdp_core.identifier_registry` row
(`registry_name='actor'`) — which is how actors already existed in this
codebase before this slice, just without governed richness — with:

- `actor_type`: `human | institution | synthetic | collective`, FK'd to a
  new `cdp_actor_type` registry. RFC-CDP-030 §2's minimum is
  human/institution/synthetic; `collective` is this slice's required
  extension for community/collective actors.
- `display_mode`: `public | protected | pseudonymous` — a capability of
  any actor_type, not a type itself. A human, institution, synthetic, or
  collective actor can each be protected or pseudonymous. This is what
  lets "internal continuity remains accountable" coexist with "public
  display can remain pseudonymous."
- `actor_status`: `active | suspended | revoked | superseded` (lifecycle).
- `identity_continuity_key`: a UUID set once at creation and made
  immutable by a database trigger (`trg_actor_identity_continuity_immutable`)
  — an update that tries to change it raises.
- No legal-name, credential, or secret field. `display_label` (on the
  underlying `identifier_registry` row) is the only human-readable label
  and is never treated as proof of identity.
- No `DELETE` is possible — `trg_actor_forbid_delete` raises
  unconditionally. Retirement is `actor_status`, not erasure.

### 2.2 Identity Claim (`cdp_core.identity_claim`)

Captures actor reference, claimant, a free-text `claimed_identity_descriptor`
(a claim, not a verified fact), a free-text `purpose_scope` (proportionality:
scoped to a governed purpose, not universal — deliberately not a controlled
vocabulary, since scope is inherently contextual), `evidence_refs` (opaque
references, never the evidence itself), and a `recognition_status` state
machine: `pending → recognized | denied | contested | superseded | withdrawn`.

Denial and contest do not delete or blank the row — `recognized_by_actor_id`,
`recognition_rationale`, and `decided_at` are recorded for every non-pending
terminal state (enforced by a CHECK constraint), and the row itself is
protected from `DELETE` by `trg_identity_claim_forbid_delete`, which raises
unconditionally, verified in this session by an actual `DELETE` attempt in
the Postgres smoke test (not just a check that the trigger's SQL text
exists). Supersession links two claims (`supersedes_claim_id` /
`superseded_by_claim_id`) instead of replacing one in place.

### 2.3 Attestation Record (`cdp_core.attestation_record`)

Binds an actor and a recognized, in-scope identity claim to one governed
act (this slice: `decision_created` only — `governed_act_type` is seeded
with a single value, extensible later, not implemented further now).
Records `attestation_method` (`shared_secret_reference | cryptographic_signature
| delegated_trust_reference`), `credential_reference` (an opaque,
non-secret handle — a CHECK constraint backstops against a caller pasting
a literal "password"/"passwd" value in as a lazy guardrail, not a
substitute for the "reference, not the secret" contract), `issued_at`,
`verification_result`, and `verifier_actor_id` (seeded system actor
`cdp_attestation_service`). No `DELETE` is possible here either.

**Honest scope of "verified":** this slice's verification means the actor
is active and holds a recognized, in-scope identity claim. It is not
cryptographic proof. `verification_result: failed` is schema-supported
(for a future asynchronous/out-of-band verification flow) but not written
by this slice's synchronous service path, which fails closed via a raised
exception before anything is persisted instead.

### 2.4 The proof path: `POST /attested-decisions`

`attest_and_create_decision` (`cdp/core/services.py`) is the integration
demonstration. Inside one transaction:

1. actor existence + `actor_status == 'active'` check (404 / 409)
2. identity claim ownership + `recognition_status == 'recognized'` check
   (409)
3. identity claim `purpose_scope == 'decision_creation'` check (409)
4. attesting actor must equal the decision's `subject_actor_id` (409,
   checked before the transaction even opens — the cheapest failure first)
5. decision creation, reusing `_create_decision_with_workflow_in_transaction`
   — the body of `create_decision_with_workflow`, extracted so this path
   is not a second, nested `db.transaction()` connection
6. attestation record insert
7. `attestation.recorded` audit event

`POST /decisions` (`create_decision_with_workflow`, `cdp/api/decisions.py`)
is untouched — same signature, same behavior, same tests passing unchanged.
This is additive, not a retrofit: every existing caller of `POST /decisions`
continues to create unattested decisions exactly as before. Only the new
route requires attestation.

## 3. Objects added

| Object | Table | Repository | Service functions |
|---|---|---|---|
| Actor | `cdp_core.actor` | `cdp/core/repositories/actors.py` | `register_actor` |
| Identity Claim | `cdp_core.identity_claim` | `cdp/core/repositories/identity_claims.py` | `submit_identity_claim`, `recognize_identity_claim`, `deny_identity_claim`, `contest_identity_claim` |
| Attestation Record | `cdp_core.attestation_record` | `cdp/core/repositories/attestations.py` | `attest_and_create_decision` |

## 4. Routes added (`cdp/api/identity.py`)

- `POST /actors`, `GET /actors/{actor_id}`
- `POST /identity-claims`, `GET /identity-claims/{claim_id}`
- `POST /identity-claims/{claim_id}/recognize`
- `POST /identity-claims/{claim_id}/deny`
- `POST /identity-claims/{claim_id}/contest`
- `POST /attested-decisions`
- `GET /attestations/{attestation_id}`

`GET /actors/{actor_id}` never exposes `identity_continuity_key`.
`GET /identity-claims/{claim_id}` redacts `claimed_identity_descriptor` and
`evidence_refs` to `"[protected]"` whenever the actor's `display_mode` is
not `public` — verified by
`test_protected_actor_identity_claim_response_redacts_descriptor_and_evidence`.

## 5. Tests run

All of the following were run against a live Docker Compose stack
(`docker/docker-compose.yml`: fresh `docker compose build cdp-api`, fresh
`up -d`, live Postgres, live `uvicorn`) on 2026-07-31:

- **Static** (no DB): `tests/migration/test_migration_010_identity_and_attestation.py::Migration010StaticTests` — 13/13 pass.
- **Postgres/service**: `Migration010PostgresSmokeTests` (1) +
  `tests/identify_attest_standing/{test_actor_service,test_identity_claim_service,test_attestation_service}.py`
  (5 + 8 + 8 = 21) — 22/22 pass.
- **API round-trip**: `tests/identify_attest_standing/test_identity_attestation_api.py` — 11/11 pass.
- **Full pre-existing suite, unchanged**: 131 migration/service tests + 24
  API tests (including all of `tests/decision`, `tests/challenge`,
  `tests/execution`, `tests/nemawashi`, `tests/db`) — all still pass, no
  regression from the `create_decision_with_workflow` refactor or the new
  routes.
- `ruff check cdp` — passes with no findings.

**GitHub Actions:** PR #41 (branch `session-027-identity-and-attestation`),
labeled `run-full-ci`. CI run `30677856180` on head commit `70ef08b`
(2026-08-01T01:24:52Z) — both `PR guard (static, no DB)` and
`Full CDP slice tests (Postgres/service/API)` completed with conclusion
`success`, exercising the same static/Postgres/API tiers wired into
`.github/workflows/cdp-ci.yml` above, against a fresh Postgres service
container and a freshly started `uvicorn` process.

## 6. Evidence level reached

Identify and Attest are rated **Integration Tested (E4)** in
`evidence/000-current-state.md`, cited to CI run `30677856180` on PR #41's
head commit `70ef08b`.

## 7. A real gap found along the way, and how it was resolved

`decision_registry`'s `validate_decision_registry_identifiers` trigger
(001-decision-registry-kernel.sql, pre-existing) hard-checks that
`subject_actor_id` is typed under the legacy `actor_type` registry
(`agent|human|system|institution|unknown`). A governed actor registered
through this slice's `cdp_actor_type` registry
(`human|institution|synthetic|collective`) would fail that check the
moment it was used as a decision's `subject_actor_id` — discovered by
actually running the happy-path test, not by inspection.

Resolved with a compatibility bridge, not a retrofit of
`decision_registry` (out of bounds for this slice): `actors_repo.insert_actor`
tags the underlying `identifier_registry` row with a mapped legacy
`actor_type` (`synthetic → agent`, `collective → institution`, `human` and
`institution` unchanged) purely for `decision_registry`'s benefit, while
`cdp_core.actor.actor_type` — the actor's real, RFC-CDP-030 type — is
unaffected and separately FK'd to `cdp_actor_type`. Documented in
`cdp/core/repositories/actors.py` and `evidence/003-known-gaps.md`.

## 8. Known limitations (see `evidence/003-known-gaps.md` for the full list)

- "Verified" is claim-based, not cryptographic.
- The proof path covers exactly one governed act (`decision_created`).
- Deciding a claim (recognize/deny/contest) requires the decider to be a
  registered actor, nothing more — no Authority or Standing check gates
  who may decide.
- `recognized_by`/deny/contest actors are validated against the legacy
  `identifier_registry`, not required to hold their own `cdp_core.actor`
  governance row.

## 9. Explicit non-goals (all held to)

Not implemented by this slice, verified by what the migration and service
layer do *not* contain (`test_migration_does_not_write_out_of_scope_governance_tables`,
and the header comment in `db/ddl/010-identity-and-attestation.sql`):
full authentication product, OAuth, OIDC, SAML, enterprise SSO, password
storage, biometric identity, universal civil-name verification, Standing
adjudication, Authority grants, recusal, complex delegation, identity
federation, Repair, Learning, closure, production deployment.

## 10. Context-plane note

This file follows the pattern set by `docs/session-026-execution-record.md`:
written before staging/committing, so the working tree's actual state is
recorded before it potentially changes. See `docs/SESSION-INDEX.md` for
where this fits in the implementation-session sequence.
