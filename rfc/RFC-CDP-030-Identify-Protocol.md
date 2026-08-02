# RFC-CDP-030 — Identify Protocol

Author: Kevin "Andie" Williams  
Status: Draft v0.4  
Series: Constitutional Decision Plane (CDP)  
Date: March 17, 2026  
Updates: RFC-CDP-030 v0.3  
Related: RFC-CDP-031, RFC-CDP-032, RFC-CDP-033

## Abstract
Defines how humans, institutions, and synthetic actors are identified in CDP.

Draft v0.4 corrects the canonical heading (the file previously carried a
stale RFC-CDP-012 header from before this protocol was renumbered into
the 030-039 identity band) and adds §6, documenting the schema and
behavior a real implementation has since built against this RFC's
minimal requirements. §§1-5 below are unchanged from Draft v0.3 and
remain the forward-looking specification; §6 is new and describes what
exists today, honestly distinguished from what the spec still leaves
open.

## 1. Purpose
The Identify Protocol answers:
- how humans, institutions, and synthetic actors are identified;
- how delegation and scope are represented;
- how identity links to authority.

## 2. Actor Types
At minimum:
- `human`
- `institution`
- `synthetic`

## 3. Required Properties
An identity SHOULD include:
- stable actor identifier;
- actor type;
- display label;
- trust source;
- authority grants;
- delegation relationships;
- revocation status.

## 4. Delegation
If authority may be delegated, policy MUST define:
- who may delegate;
- to whom;
- for what scope;
- until when;
- how revocation behaves.

## 5. Principle
No anonymous authority. Anonymous participation MAY exist only under explicit policy and without silent escalation into unverified power.

## 6. Implementation Status (added in Draft v0.4)

This section documents what a real, running implementation
(`cdp/core/services.py`, `db/ddl/010-identity-and-attestation.sql`,
`db/ddl/013-identity-claim-scope.sql`) has built against this RFC's
minimal requirements, across four development sessions
(`docs/session-027-identity-and-attestation.md` through
`docs/session-030-identity-claim-scope.md`). This RFC itself specifies no
persistence schema in §§1-5 above; the schema described here is a
documented interpretation composing this RFC's minimal
required-properties list (§3) with RFC-CDP-033 §11.2's
existence/recognition/scope distinction and §11.6's non-erasure rule --
not a claim that this RFC itself mandates this exact shape.

### 6.1 Actor Registry (§2, §3 partially satisfied)

A governed `cdp_core.actor` table exists, one row per identity,
FK'd to the pre-existing `cdp_core.identifier_registry` row it
elaborates. It carries:

- `actor_type` -- `human`, `institution`, `synthetic` (§2's three
  minimum types), plus `collective` (added for community/collective
  actors, beyond §2's list);
- a `display_mode` capability (`public`, `protected`, `pseudonymous`) --
  not named in §3, added so an actor's public-facing label and its
  accountable identity can differ without conflating "identifiable" with
  "publicly named";
- `actor_status` (`active`, `suspended`, `revoked`, `superseded`) --
  satisfies §3's "revocation status" requirement;
- `identity_continuity_key`, an immutable-once-set UUID (enforced by a
  database trigger) -- the stable anchor §3's "stable actor identifier"
  requirement calls for, kept accountable even if display or status
  change later.

§3's "trust source" is not a separate stored field; the closest
analogue is which actor performed a claim's recognition (§6.2 below).

### 6.2 Identity Claim (RFC-CDP-033 §11.2 composition, not directly specified by this RFC)

A governed `cdp_core.identity_claim` table records a claim of identity
for a stated purpose, going through a recognition state machine
(`pending` -> `recognized`/`denied`/`contested`/`superseded`/`withdrawn`)
that never deletes a row -- denial or contest is recorded as a status
transition, never erasure (RFC-CDP-033 §11.6). Recognizing, denying, or
contesting a claim is restricted to a single seeded, bounded
`cdp_identity_recognition_authority` actor; an arbitrary registered
actor, or the claimant deciding its own claim, is rejected.

As of Draft v0.4 (session 030,
`db/ddl/013-identity-claim-scope.sql`), a claim's coverage is governed
by two independent, optional axes: a `purpose_scope` string (unchanged
since Draft v0.3's original implementation) and an optional two-level
`scope_registry_name`/`scope_decision_class_id` pair mirroring
RFC-CDP-032's authority-grant scope model. A claim that sets neither of
the two new fields behaves exactly as every claim did before session
030.

### 6.3 What is deliberately not implemented

- **§4 Delegation is entirely unimplemented for identity itself.**
  There is no delegator/delegate/scope/validity/revocation model for
  *who may claim to be whom*. (RFC-CDP-032 implements a scoped grant/
  revoke model for *authority to perform governed acts*, which is a
  related but distinct question -- see §6.4.)
- **"How identity links to authority" (§1) is answered by a separate
  RFC, not by this one.** RFC-CDP-032's Authority Grant is issued to an
  `actor_id` independently of any Identity Claim; the two objects are
  connected only through the shared proof path (RFC-CDP-031 §6.3),
  which checks both a recognized Identity Claim and a matching Authority
  Grant before admitting a governed act. Identity Claim recognition
  itself does not grant authority -- see RFC-CDP-032's own header for
  its core principle ("no authority without scope, no authority without
  record").
- **No real authentication.** The API accepts a submitted `actor_id` at
  face value; nothing proves the HTTP caller controls the actor_id it
  asserts. This is a distinct question from claim recognition (which
  governs whether an *actor* is recognized for a purpose, not whether
  the *caller* making the request is who it says it is) and remains
  unaddressed as of this draft.
- **Trust source, per §3, is not a first-class stored field** -- see
  §6.1.

### 6.4 Cross-reference

See RFC-CDP-032 (Authority and Delegation Model) for the authority
question this RFC's §1 raises but does not itself answer, and
RFC-CDP-031 (Attest Protocol) §6 for how Identify's recognized claims
are consumed by the attestation proof path.
