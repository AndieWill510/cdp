# Identity and Authority Slice Closure — Sessions 027–032

Status: closed. Main `199c934`. This is not a new implementation session
and adds no code -- it is a summary document tying off one continuous
six-session arc so future readers can understand it without
reconstructing it from PR history. See the per-session docs
(`docs/session-027-identity-and-attestation.md` through
`docs/session-032-caller-authentication.md`) for full implementation
detail; this file is the durable, one-page entry point.

## What was built

Sessions 027 through 032 implemented, in order:

| Session | Slice | What it added |
|---|---|---|
| 027 | Identity and Attestation | `cdp_core.actor` (Actor Registry), `cdp_core.identity_claim` (recognition/denial/contest, protected/pseudonymous display, non-erasure), `cdp_core.attestation_record`, and the first `attest_and_*` proof path (`attest_and_create_decision`). |
| 028 | Authority and Delegation | `cdp_core.authority_grant`, `cdp_core.authority_evaluation_result`, scoped to RFC-CDP-032 §19 Minimal Compliance; `attest_and_create_decision` extended with a PROPOSE-authority gate. |
| 029 | Universal Attestation | Four more `attest_and_*` proof paths (challenge raising, challenge adjudication, execution authorization, execution recording) -- every governed act this repository's canonical path had a service function for at the time. |
| 030 | Identity Claim Scope | Optional two-level (registry + decision-class wildcard) scope on Identity Claims, mirroring `authority_grant`'s model; enforced once, in the shared claim-check helper all five `attest_and_*` functions use. |
| 031 | RFC-CDP-030/031 spec updates | Documentation-only: fixed both RFCs' stale internal header, bumped to Draft v0.4, added an Implementation Status section to each stating plainly what the code does and does not prove (most importantly: no cryptographic signature verification). |
| 032 | Caller Authentication | `cdp_core.actor_bearer_token`; `register_actor` issues a one-time bearer token; `verify_bearer_token` gates nine actor-asserting mutating routes; self-service revocation. Reviewed twice (PR #48 pre-merge, PR #49 post-merge) before this closure. |

## What this arc provides (Integration Tested, E4, confirmed in CI)

- Governed actor registration, independent of legal-name/personhood.
- Identity claims: submission, recognition, denial, contest -- all
  preserved, never erased -- plus protected/pseudonymous display that
  redacts claim content but not actor-level identity.
- Purpose-scope, plus an optional registry/decision-class scope, on
  identity claims.
- Attestation across the five governed-act proof paths this repository
  implements: decision creation, challenge raising, challenge
  adjudication, execution authorization, execution recording.
- Scoped Authority Grants for the currently implemented authority model
  (RFC-CDP-032 §19 Minimal Compliance): five authority types evaluated
  (`PROPOSE`, `CHALLENGE`, `ADJUDICATE`, `AUTHORIZE_EXECUTION`,
  `RECORD`), a real two-level scope (registry + decision-class,
  wildcard-capable), mandatory expiry.
- Real HTTP-caller-to-actor possession binding through bearer tokens on
  nine actor-asserting mutating routes -- a request asserting an
  actor_id it does not hold a valid token for is rejected before
  anything is persisted.
- Self-service token revocation, with the HTTP response redacted to
  `{actor_id, token_id, status, revoked_at}` -- the credential verifier
  itself never crosses the API boundary.
- A canonical migration path (`db/ddl/`) that provisions **no**
  privileged credentials: the two bounded system actors
  (`cdp_identity_recognition_authority`, `cdp_authority_grant_issuer`)
  are unreachable through the HTTP API until an operator provisions
  their credentials out of band. Local/dev/test bootstrapping of those
  two credentials lives outside the migration path entirely
  (`db/seed/dev-caller-authentication-tokens.sql`), applied only by
  local Docker init and CI's own test job. This CI-enforced invariant
  (not just manually checked) is `Migration014IsolatedDatabaseTests`.

All of the above is exercised through the live API against live
Postgres and confirmed passing in CI as of merge commit `199c934` (run
`30779064311`, push-triggered, conclusion `success`) -- see
`evidence/000-current-state.md`'s Identity and Standing, Authority,
Universal Attestation, Identity Claim Scope, and Caller Authentication
rows for the per-capability citations.

## What this arc deliberately does not provide

Named boundaries, not hidden defects -- each is documented in detail in
`evidence/003-known-gaps.md`'s per-slice sections:

- **OAuth2/OIDC/SAML, sessions, or account recovery.** Bearer tokens
  only; a lost token has no "forgot my credential" recovery path.
- **Token rotation.** A revoked token's actor cannot obtain a
  replacement through this system.
- **Cryptographic request signing.** RFC-CDP-031 §4's signature-validity
  requirement remains unmet -- a bearer token is presented, not signed
  over per-request.
- **Production secrets provisioning.** The two bounded system actors'
  credentials, once an operator provisions them, have no rotation
  mechanism either; this repository does not specify how a real
  deployment should manage them.
- **Full RFC-CDP-032.** No delegation, quorum, presence,
  emergency/repair/sovereignty grant types, separation-of-duties
  enforcement, or the fuller authority-decay model SS9 names.
- **A transaction-boundary check/use gap.** `verify_bearer_token` opens
  and completes its own transaction, separate from the governed
  mutation it authorizes -- a token could in principle be revoked
  between the check and the mutation's own commit. Recorded, not fixed
  -- fixing it would mean threading a token/cursor through every
  protected route's underlying service function, reversing the design
  choice that kept the check standalone.
- **Standing and Recusal (RFC-CDP-033).** Still **Not Implemented
  (E0)**. See "What comes next" below -- this is the load-bearing gap.
- **Production Demonstrated (E5) evidence for anything in this
  repository.** All E4 evidence is CI-based (a provisioned Postgres
  service container and a freshly started API process inside a GitHub
  Actions run), not observed production operation.

## What comes next

Identity, Attestation, Authority, and Caller Authentication together can
now answer:

- Who is this actor?
- Does the HTTP caller actually control that actor identity?
- Is the actor's identity claim recognized and in scope for this act?
- Does the actor currently hold the authority this act requires?
- Is the act attested and recorded?

They cannot yet answer:

- May this particular actor properly participate in this particular
  matter?
- Are they conflicted, disqualified, recused, or an affected party with
  standing to challenge?
- Who has standing to propose, test, adjudicate, or appeal this specific
  decision?

That is RFC-CDP-033, Standing and Recusal -- still rated Not Implemented
(E0) in `evidence/000-current-state.md`. It is not a small missing
feature layered on top of what exists; it is the next constitutional
gate. Identity without Standing establishes who is speaking, not
whether they should exercise power in this matter. Authority without
Recusal can still let a legitimately credentialed actor participate in
a matter where they have a disqualifying conflict.

**Recommendation:** begin a bounded Standing and Recusal slice next,
following the same review discipline this arc used (read the RFC and
existing code first, report gaps, implement the narrowest safe version,
verify through CI, invite review before and after merge). Do not extend
authentication/authorization further first -- OAuth/OIDC, cryptographic
signing, and token rotation are each real gaps, but none of them is the
next *constitutional* gap; Standing is. Test, Legitimize, and Learn
(RFC-CDP-043/045/048) remain open after that, but Standing should
precede them, since participation legitimacy belongs upstream of
adjudication and legitimation.

## Context-plane note

This document does not replace any per-session doc or evidence file --
it is a pointer and summary, written once, at closure, so a future
reader has one place to start. See `docs/SESSION-INDEX.md` for where
this fits in the implementation-session sequence, and
`evidence/000-current-state.md`'s closure note (same content,
evidence-layer framing) for the corresponding entry there.
