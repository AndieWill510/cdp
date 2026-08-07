# Session 034 — RFC-CDP-033 Standing Recognition Clarification

Status: docs-only. No code, DDL, repositories, services, routes, migrations,
or tests were added or modified in this session. Standing and Recusal
remain **Not Implemented (E0)** in `evidence/000-current-state.md` after
this session — this document makes no evidence-level claim of any kind.

## 1. Purpose

`docs/session-033-standing-recusal-recon.md` (PR #51) identified the
recognition-authority gap as the primary blocker to a bounded Standing and
Recusal implementation slice: RFC-CDP-033 v0.6 stated the *properties* a
binding Standing recognition determination must have, but never named the
actor or process that holds them, unlike the seeded-actor precedent set
for Identity (session 027) and Authority (session 028). It also flagged
the §9 seed schema's single-mutable-row conflation of claim, recognition,
recusal, and contest, and the underspecified "denial" trigger for
§11.6's automatic Breach Record rule.

This session amends `rfc/RFC-CDP-033-Standing-and-Recusal-Model.md` to
close those gaps precisely enough that a future implementation session
does not have to invent policy in code — without implementing anything
itself.

## 2. Scope of this amendment

RFC-CDP-033 is bumped from Draft v0.6 to **Draft v0.7**. Six changes, all
normative or materially clarifying:

1. **Standing recognition role, defined by required properties (§11.5).**
   A binding recognition determination must be made by an actor or process
   that is bounded, non-self-interested, procedurally authorized, and
   auditable. This RFC does not name a specific implementation actor —
   that remains an implementation decision, the same way `RFC-CDP-030`
   and `RFC-CDP-032` each bind their own recognition/grant-issuance role
   to a specific, bounded, seeded actor without this RFC dictating which
   one. What changed is that the properties such an actor must satisfy are
   now explicit and checkable, closing the regress §11.1 already named in
   prose but did not operationalize.
2. **Provisional affected-party Standing, formalized (§11.4).** A
   minimally sufficient claim (one identifying a possible consequence and
   the relationship that grounds answerability) creates provisional
   Standing immediately, sufficient to raise the first protected act (for
   example, a Challenge) without waiting on binding recognition. A claim
   that fails minimal sufficiency does not acquire provisional Standing
   and does not trigger the Breach Record rule if left unrecognized. This
   directly implements the correction requested for PR #51: pending
   recognition must not block the first Challenge when a claim of
   potential impact has been made, consistent with §11.4's existing rule
   that such a claim is sufficient for preliminary standing.
3. **A five-value recognition outcome vocabulary, new §11.8.**
   `recognized | narrowed | deferred | rejected | denied`. `denied` is
   defined precisely and is the only outcome that triggers §11.6's
   automatic Breach Record rule — distinguished from `rejected` (a
   good-faith merits determination against a claim that cleared minimal
   sufficiency), from `narrowed`/`deferred` (both preserve some or all of
   the claimed Standing), and from a claim that never cleared minimal
   sufficiency in the first place (never eligible for denial because it
   was never a sufficient claim to deny).
4. **The §9 seed schema split into four append-only records:** Standing
   Claim, Standing Recognition Determination, Recusal Record, Standing
   Contest Record. Each is its own immutable record referencing the ones
   before it; none is edited in place. This directly addresses the
   session-033 finding that the single-row seed schema risked erasing
   disagreement and history.
5. **RFC-CDP-078 cited directly, new §3.5.** Relationship Type is
   explanatory, not gating, per `RFC-CDP-078` §8.2's non-suspension rule —
   previously true at the corpus level (per
   `architecture/001-canonical-governance-workflow.md`) but not stated in
   RFC-CDP-033's own text.
6. **RFC-CDP-075 removed from `Depends On`.** It does not exist as a
   drafted RFC (confirmed against `rfc/` in session 033); it is now noted
   separately as reserved rather than listed as a hard dependency.

## 3. What this session deliberately does not resolve

Carried forward from §14's "Not yet resolved" list, unchanged by this
session:

- how risk classes determine recusal depth;
- how this model updates lifecycle protocol RFCs;
- how Functional Standing relates to `RFC-CDP-062`;
- how implementation profiles enforce projection atomicity.

Newly named as unresolved by this session (not resolved, precisely
scoped):

- which specific actor(s) will satisfy the four required properties in
  §11.5 for this repository's own implementation — the RFC now states the
  properties, not a name, matching the pattern already used for Identity
  and Authority;
- the abuse or anti-flooding threshold for provisional affected-party
  claims mentioned in session 033's finding 4.2(f) — still not specified
  anywhere in this RFC, and this session does not attempt to specify one.

Neither of these blocks the narrow implementation slice proposed below;
both should be resolved before Standing is extended to other types or to
a public-facing deployment.

## 4. Stop conditions re-checked

Per the standing session discipline: the primary stop condition from
session 033 — "the RFC does not identify a legitimate recognition
authority or process" — is now addressed at the level this RFC can
address: the *properties* a legitimate recognition authority must have
are fully specified and checkable (§11.5). Naming the concrete actor
remains, correctly, an implementation-session decision, not something an
RFC should hardcode. This is not a stop condition remaining open; it is
the RFC doing its job and leaving one narrower, implementation-scoped
decision for the next session, which is expected.

No other stop condition applies. This session did not touch RFC-CDP-072,
so whether §11.6's now-precise `denied` definition fully reconciles with
RFC-072's Breach Record schema is not confirmed here — a future session
implementing the Breach Record generation path should read RFC-072
directly before writing that code.

## 5. Proposed minimum implementation slice (unchanged from Session 033, now unblocked)

The slice proposed in `docs/session-033-standing-recusal-recon.md` §5
remains the recommendation, now with its blocking question answered at
the RFC level:

- **Standing type:** Affected-Party Standing only.
- **Lifecycle stage:** Challenge (RFC-CDP-042), gating
  `attest_and_raise_challenge`.
- **Recognition mechanism:** a bounded seeded actor satisfying RFC-033
  §11.5's four properties (bounded, non-self-interested, procedurally
  authorized, auditable), mirroring `cdp_identity_recognition_authority`
  / `cdp_authority_grant_issuer`. The implementation session must document
  which actor holds this role and how it satisfies each property, per
  §11.5's closing sentence.
- **Provisional Standing rule:** a minimally sufficient affected-party
  claim permits raising the initial Challenge immediately; a pending or
  deferred recognition determination does not block it. Enforcement
  checks for a minimally sufficient claim on file, not a completed
  recognition.
- **Persistence objects:** Standing Claim and Standing Recognition
  Determination (RFC-033 §9.1, §9.2) as two separate, append-only records
  — not the single mutable row the RFC previously seeded.
- **Non-goals:** Recusal in its entirety; every Standing type other than
  Affected-Party; automatic Breach Record generation (RFC-072 not yet
  implemented, and this session did not cross-check §11.6/§11.8 against
  RFC-072's actual schema); the enforcement-projection half of the
  two-layer persistence model; Test, Legitimize, or Learn.
- **What remains E0 after that slice:** everything not listed above,
  exactly as scoped in session 033 §5.

This session does not implement any of this. It is recorded here so the
next implementation session has the updated, RFC-grounded version of the
same slice in one place.

## 6. Validation

- `python3 scripts/verify_rfc_index.py` run after these edits — passes
  with only the same pre-existing, non-fatal WARN-level drift already
  documented in `evidence/003-known-gaps.md`'s "RFC index/manifest
  verification" section; `rfc/index/rfc-manifest.json`'s RFC-CDP-033 entry
  was updated in this session (status bumped to `"Draft v0.7"`) so this
  session does not itself introduce new drift.
