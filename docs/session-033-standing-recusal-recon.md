# Session 033 — Standing and Recusal Reconnaissance

Status: docs-only reconnaissance. No code, DDL, repositories, services,
routes, migrations, or tests were added or modified in this session.
Standing and Recusal (RFC-CDP-033) remain **Not Implemented (E0)** in
`evidence/000-current-state.md` after this session — this document makes
no evidence-level claim of any kind.

## 1. Purpose

Decide what must be clarified in `RFC-CDP-033-Standing-and-Recusal-Model.md`
(Draft v0.6) before a bounded Standing and Recusal implementation slice can
be safely attempted, without inventing schema, policy, or architecture in
the process. This is the recommended next constitutional gate per
`docs/session-027-032-identity-authority-closure.md`'s closing
recommendation.

## 2. Files read

- `rfc/RFC-CDP-033-Standing-and-Recusal-Model.md` (Draft v0.6, in full)
- `docs/session-027-032-identity-authority-closure.md` (in full)
- `evidence/000-current-state.md` (in full)
- `evidence/003-known-gaps.md` (in full)
- `architecture/001-canonical-governance-workflow.md` (in full)

All five filenames matched exactly; no substitution was needed.

## 3. Files not read but probably relevant

Named here, not read this session, per the reconnaissance's bounded scope:

- `rfc/RFC-CDP-001-Vision-Scope-Principles.md` §5.1 (the answerability
  root RFC-033 cites directly)
- `rfc/RFC-CDP-025-CDP-Persistence-Model.md` (governs `cdp_governed_record`
  / `cdp_standing_record`, which RFC-033 §12 references but does not itself
  define)
- `rfc/RFC-CDP-030-Identify-Protocol.md`, `RFC-CDP-031-Attest-Protocol.md`,
  `RFC-CDP-032-Authority-and-Delegation-Model.md` (the three RFCs whose
  bounded-seeded-actor recognition/grant pattern is the closest existing
  precedent for how RFC-033 might name a Standing recognition authority)
- `rfc/RFC-CDP-070` through `074` (the Repair/Appeal band RFC-033 depends
  on for Repair Standing, Appeal Standing, and the automatic Breach Record
  rule)
- `rfc/RFC-CDP-078-Relationship-Taxonomy-and-Recognition-Model.md` (the
  non-suspension rule the architecture doc cites as governing how
  Relationship Type must never gate Standing — RFC-033 itself does not
  cite RFC-078 at all)
- `docs/session-027-identity-and-attestation.md` (cited by
  `evidence/003-known-gaps.md` as the source of the Standing non-goal
  scoping decision)
- `docs/SESSION-INDEX.md`

## 4. Findings

### 4.1 What RFC-CDP-033 already defines well enough to implement

- **Definitions (§4)** cleanly separate Standing, Recusal, and Functional
  Standing from Identity, Attestation, and Authority, and §3 explicitly
  cross-references those three RFCs to say why. This is one of the
  strongest-drafted sections in the RFC.
- **Existence / Recognition / Scope (§11.2)** is a precise three-way split,
  with an explicit rule that non-recognition must not be read as proof of
  non-existence and recognition must not be read as CDP having created the
  relationship. This directly satisfies the architecture doc's citation of
  RFC-033 §11 as the answerability gateway.
- **The Answerability Test (§11.3)**, a concrete five-question method for
  resolving contested Standing claims, with an explicit statement that a
  Standing determination "MUST be able to show its work" against it.
- **Standing Type Taxonomy (§11.4)** and the **Recognition Authority table
  (§11.5)** are conceptually complete: Constitutional (with three named
  subtypes), Delegated, Emergency, Repair, and Appeal Standing are each
  defined and distinguished by how they are recognized vs. granted.
- **Contestability Boundaries (§11.7)** correctly tiers Constitutional vs.
  Delegated Standing contestability and sets a contest window (before/during
  the relevant stage; post-execution belongs to Appeal/Repair).
- **Proposer recusal (§7)**, tiered by risk class (low-risk/reversible vs.
  high-risk/irreversible vs. emergency), gives implementable defaults.
- The persistence direction in §12 (canonical governed artifact vs.
  queryable enforcement projection, non-revocation of Constitutional
  Standing enforced "where possible" at the storage layer) is consistent
  with the architecture doc's persistence cross-reference (§10) and with
  the pattern already used for `cdp_governed_record` elsewhere in this
  repository.

### 4.2 What remains ambiguous or contradictory

**(a) No named recognition mechanism — the single largest gap.**
§11.1 states a *binding* recognition "requires valid procedural authority,
competence, independence, and record, exercised by an actor or process
authorized under this RFC to make that determination," and §11.5's table
says Constitutional Standing is "Recognized by the CDP framework." Neither
names who or what that is. Sessions 027 and 028 resolved the structurally
identical problem for Identity and Authority by seeding a single, bounded,
named actor (`cdp_identity_recognition_authority`,
`cdp_authority_grant_issuer`) directly in DDL and documenting it as a
narrow interpretation, not a general authorization system. RFC-033 does
not adopt, reject, or even mention that pattern. Without an explicit
answer, an implementer is left to invent one — which is exactly what this
reconnaissance is supposed to prevent, and one of the stop conditions
named for this session.

**(b) The Standing Record Seed (§9) conflates several distinct acts in one
mutable row.** The seed schema has `standing_basis` (a claim),
`standing_recognized_by`/`standing_recognized_at` (a recognition act),
`conflicts_declared`/`conflict_description`/`recusal_required`/
`recusal_scope`/`recusal_basis` (a recusal determination), and
`contested`/`contest_record_id` (a contest disposition) all as fields on
one record, with no version, lineage, or append-only structure. §9 itself
says this is "a seed for discussion... remains Draft until separately
stabilized," so the RFC does not claim this is final — but as drafted, it
reads as a single row meant to be updated in place, which risks exactly
the "giant mutable row that overwrites history" failure mode named in this
session's brief. Session 027/028's actual implementations (identity_claim,
authority_grant) did not do this — they kept claim and decision as
separate, append-only-per-decision structures.

**(c) The automatic Breach Record rule (§11.6) is underspecified for
implementation.** "Denial of Constitutional Standing MUST automatically
generate a Breach Record" does not define:
- what counts as "denial" versus a narrowing, deferral, or provisional
  evidentiary rejection under Answerability Test Question 5 (§11.3), which
  the RFC itself says can "confirm, narrow, defer, or reject" a claim —
  four outcomes, only one of which (reject) plausibly maps to "denial,"
  and even that is ambiguous between a good-faith mistaken determination
  and intentional suppression;
- who creates the Breach Record (an actor? the recognition process itself,
  as a side effect?);
- how circularity is avoided when the party denied standing lacks
  recognized standing, at that moment, to invoke the Repair plane that is
  supposed to protect them — RFC-033 asserts the breach entry "MUST NOT
  require action by the affected party," which is the right instinct, but
  doesn't say what triggers it if not the affected party's own act;
- whether this is automatic, presumptive, or contingent on later
  adjudication of whether the denial was correct.

This is a corpus-wide design intent, not an RFC-033 invention — the
architecture doc (§4.13) independently states "denial of standing is
itself a trigger event and an automatic breach" as an RFC-070 entry
condition — but RFC-072's schema and trigger mechanics were not read this
session, and RFC-033 does not itself resolve the "what counts as denial"
question needed to implement this without converting every unsuccessful
preliminary claim into a constitutional violation.

**(d) RFC-033 never cites RFC-078**, even though the architecture doc
treats RFC-078's non-suspension rule (Relationship Type must never gate
Standing) as load-bearing corpus-wide. This is silence, not a violation —
RFC-033 doesn't do anything that contradicts RFC-078 — but a reader of
RFC-033 alone would not know this constraint exists. Worth a citation, not
a rewrite.

**(e) A stale forward reference.** RFC-033's header lists `RFC-CDP-075` as
a hard `Depends On`. `architecture/001-canonical-governance-workflow.md`
Gap 5 states RFC-CDP-075 "does not exist as a file" and is listed
`Reserved` in the manifest. Confirmed directly: `rfc/` contains
`RFC-CDP-070` through `RFC-CDP-074` but no `RFC-CDP-075` file. This is a
small, real inconsistency — but fixing it requires an editorial choice
(drop the dependency vs. annotate it as reserved) rather than a pure typo
correction, so it is reported here rather than fixed in this session.

**(f) No anti-flooding/anti-retaliation safeguard on preliminary
Affected-Party Standing.** §11.4 correctly forbids denying affected-party
standing on the grounds that impact hasn't been proven yet, and the
architecture doc (§4.2) repeats this for the Proposal Sufficiency Gate.
Neither document specifies any bound on how many such claims may be filed,
by whom, or with what consequence for bad-faith or retaliatory claims. This
may be intentional (a scope decision for a later, narrower RFC or risk
profile) but it is not stated as such anywhere read this session.

### 4.3 Direct answers to the ten review questions

1. **Identity / Authority / Standing / Recusal separated?** Yes — §3 and
   §4 do this cleanly and explicitly.
2. **Existence / recognition / scope of Standing separated?** Yes — §11.2
   is precise and internally consistent; §11.7 reinforces it.
3. **Who or what may bind CDP to a Standing recognition?** Not answered
   concretely. §11.1/§11.5 state the *properties* required (procedural
   authority, competence, independence, record) but name no actor or
   process, unlike the precedent set for Identity and Authority. This is
   the central open question.
4. **Relationship Type avoided as a Standing prerequisite?** Yes in effect
   — RFC-033 never mentions Relationship Type at all, and the
   corpus-level ordering (architecture doc §2) keeps it downstream and
   explanatory-only. RFC-033 would benefit from an explicit citation to
   RFC-078 §8.2, but nothing currently violates the rule.
5. **Does the automatic Breach Record rule need clarification before
   implementation?** Yes — see 4.2(c). "Denial" needs an operational
   definition distinguishing it from narrowing/deferral/good-faith
   rejection before this rule can be implemented without over-triggering.
6. **Is the seed Standing Record schema safe?** Not as drafted — see
   4.2(b). It mixes a claim, a recognition act, a recusal determination,
   and a contest disposition into one mutable row with no lineage. The RFC
   itself already marks it non-final ("remains Draft until separately
   stabilized"), which this reconnaissance treats as license to recommend
   a split rather than as evidence the RFC is wrong.
7. **Smallest honest implementation slice for the next session?** See §5
   below.
8. **What should remain explicitly out of scope?** See §6 below.

## 5. Proposed minimum implementation slice for Session 034

This is a proposal for the next session's scoping conversation, not a
commitment made by this session.

- **Standing type:** Affected-Party Standing only (a Constitutional
  Standing subtype). This is the narrowest type with an already-precise
  rule in the RFC ("claim of potential impact is sufficient for
  preliminary standing... no actor may deny... on the grounds that impact
  has not yet been proven," §11.4), and it is the type the architecture
  doc's Proposal Sufficiency Gate section already assumes exists.
- **Provisional Standing vs. binding recognition:** the slice must keep
  these two acts distinct, not sequential-and-blocking. Submission of a
  minimally sufficient affected-party standing claim creates **provisional
  Standing** to raise the initial Challenge. Separately, a **binding
  Standing recognition** determination — made by whatever recognition
  mechanism is resolved below — may later confirm, narrow, reject, or
  contest that claim. Pending recognition MUST NOT block the initial
  Challenge unless the claim fails a minimal sufficiency check (identifies
  no possible consequence or answerability relationship) or a separately
  specified abuse threshold applies (not defined in this slice — see
  finding 4.2(f)). This follows directly from §11.4's rule that a claim of
  potential impact is sufficient for preliminary standing: the first
  protected act cannot depend on prior institutional recognition without
  contradicting that rule.
- **Lifecycle stage:** Challenge (RFC-CDP-042), which is already
  Integration Tested (E4) and already has an attested proof path
  (`attest_and_raise_challenge`, session 029). Standing would gate whether
  a given actor may raise a challenge as an affected party, mirroring how
  the PROPOSE authority gate (session 028) was added to
  `attest_and_create_decision` without changing that function's existing
  contract for callers who don't claim the new status.
- **Recognition mechanism:** blocked pending RFC clarification (see stop
  condition below) — the two live options are (a) the RFC names a
  Standing recognition pattern explicitly (most likely a bounded seeded
  actor, mirroring `cdp_identity_recognition_authority` /
  `cdp_authority_grant_issuer`), or (b) Session 034 adopts that pattern on
  its own initiative and documents it as an interpretation the way
  sessions 027/028 did, subject to review. Recommendation: resolve this in
  RFC text first, since inventing it silently in code is exactly what this
  reconnaissance was asked to prevent.
- **Minimum recusal rule:** none enforced in this slice. Affected-party
  standing to raise a challenge does not implicate proposer recusal (no
  Legitimize stage exists yet to recuse from), so Recusal enforcement
  should be deferred entirely rather than partially implemented.
- **Persistence objects:** at minimum two separate, append-only records —
  a Standing Claim record (actor, decision, stage, basis, submitted_at) and
  a Standing Recognition Determination record (claim reference, outcome,
  recognized/denied/narrowed, decided_by, decided_at) — explicitly not the
  single mutable seed row in §9. No enforcement-projection table should be
  attempted in the same session that first defines the canonical shape.
- **API operations:** submit an affected-party standing claim; recognize,
  deny, or narrow that claim (mirroring `submit_identity_claim` /
  `recognize_identity_claim` / `deny_identity_claim`'s existing shape).
- **Enforcement point:** a Standing gate added to
  `attest_and_raise_challenge`, analogous to the Authority gate already
  added to `attest_and_create_decision`. The gate checks for a minimally
  sufficient pending or recognized standing claim, not for a completed
  binding recognition — consistent with the provisional-Standing rule
  above.
- **Negative cases:**
  - challenge attempted with no Standing claim on file at all → reject;
  - challenge attempted with a minimally sufficient, still-pending
    affected-party claim → permit provisionally, pending later binding
    recognition;
  - claim submitted for a nonexistent actor or decision → reject;
  - an actor attempting to recognize their own claim → reject;
  - recognition attempted by an actor other than the bounded recognition
    actor → reject;
  - a materially incomplete claim that identifies no possible consequence
    or answerability relationship → reject as failing minimal
    sufficiency, not as "denial of Constitutional Standing" (§11.6's
    automatic-breach rule attaches to denial of an already-sufficient
    claim, not to a claim that never cleared the sufficiency floor);
  - a later narrowing or rejection of a previously provisional claim →
    preserved as its own governed determination record, linked to the
    original claim and contestable under §10/§11.7, never an in-place
    overwrite of the claim record.
- **Non-goals for this slice:** listed in §6.
- **What remains E0 after this slice:** Recusal in its entirety; every
  Standing type other than Affected-Party (Evidence-Custodian,
  Record-Keeper, Delegated, Emergency, Repair, Appeal, AI Functional);
  automatic Breach Record generation on denial (both because RFC-072 is
  itself E0 and because "denial" is not yet operationally defined); the
  full two-layer canonical-artifact-plus-enforcement-projection model
  (only the canonical shape would exist); database-level non-revocation
  enforcement for Constitutional Standing.

## 6. Explicit non-goals (for this session and the proposed next one)

For this session (033):
- No DDL, repository, service, route, or test code.
- No rewrite of RFC-CDP-033 beyond what a future session decides once the
  ambiguities above are resolved.
- No evidence-level change of any kind — Standing and Recusal remain E0.

For the proposed Session 034 slice:
- Recusal (proposer, adjudicator, legitimizer independence, capture risk,
  emergency role compression) — entirely deferred.
- Delegated, Emergency, Repair, Appeal, and AI Functional Standing.
- Automatic Breach Record generation.
- The enforcement-projection half of the two-layer persistence model.
- Any change to Identity, Attestation, or Authority code paths beyond
  adding one new gate call site.
- Test, Legitimize, or Learn (RFC-CDP-043/045/048) — none of these exist
  yet and the proposed slice does not require them.

## 7. Risks of implementing before these questions are settled

- **Silent invention of a recognition authority.** If Session 034 (or any
  future session) adds a Standing recognition mechanism without the RFC
  naming one, that code becomes the de facto constitutional answer by
  default, which is precisely the "centralized standing-granter becomes
  the origin of rights CDP claims only to recognize" failure mode RFC-033
  §11.1 warns against in prose.
- **Erasure of disagreement.** Implementing the §9 seed schema literally,
  as a single mutable row, would let a later recognition or recusal
  determination silently overwrite an earlier claim or contest, losing the
  history a contestable Standing model depends on.
- **Over-triggering or under-triggering Repair.** Implementing the
  automatic Breach Record rule without an operational definition of
  "denial" risks either flooding the Repair plane with every narrowed or
  deferred claim, or under-protecting affected parties if "denial" is
  defined too narrowly to catch real suppression.
- **Compounding on an unstable base.** RFC-033 v0.6 itself documents five
  unresolved items in §14 (schema location, risk-class-to-recusal-depth
  mapping, lifecycle protocol updates, Functional Standing/HITL-AIITL
  relationship, projection atomicity). Building code against a draft that
  already names its own open questions, without first closing at least the
  recognition-authority question, risks a second implementation-then-
  correction cycle like the one session 032 already went through for
  caller authentication.

## 8. Stop conditions encountered

Per this session's brief, one stop condition applies directly:

> The RFC does not identify a legitimate recognition authority or
> process.

This is confirmed true for Constitutional Standing generally (§11.1,
§11.5) — the RFC states the *properties* recognition must have, not the
actor or process that has them. This session does not silently invent
one; it is reported here as the primary blocking question for Session 034
to resolve, either through an RFC update or an explicitly reviewed
implementation-session interpretation following the session 027/028
precedent.

No other stop condition applies: the seed schema issue is a drafting
looseness the RFC itself flags as non-final, not a conflation that erases
disagreement in already-adopted text; the Breach Record rule needs
clarification but is not in material conflict with RFC-072 (RFC-072 was
not read this session, so this cannot be fully confirmed — flagged as an
open item for whichever session next reads both); AI Functional Standing
was reviewed only at the level present in RFC-033 §8 and did not surface a
conflict with RFC-034 or the current Authority model, but RFC-034 was not
read this session either, so this is a partial answer, not a clearance.
