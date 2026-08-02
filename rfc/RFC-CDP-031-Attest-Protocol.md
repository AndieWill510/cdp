# RFC-CDP-031 — Attest Protocol

Author: Kevin "Andie" Williams  
Status: Draft v0.4  
Series: Constitutional Decision Plane (CDP)  
Date: March 17, 2026  
Updates: RFC-CDP-031 v0.3  
Related: RFC-CDP-030, RFC-CDP-032

## Abstract
Defines how actors sign, attest, and bind authority to acts.

Draft v0.4 corrects the canonical heading (the file previously carried a
stale RFC-CDP-011 header from before this protocol was renumbered into
the 030-039 identity band) and adds §7, documenting the schema and
behavior a real implementation has since built against this RFC's
minimal requirements. §§1-6 below are unchanged from Draft v0.3 and
remain the forward-looking specification; §7 is new and describes what
exists today, honestly distinguished from what the spec still leaves
open -- most importantly, §4's cryptographic verification requirements,
which the current implementation does not meet.

## 1. Purpose
The Attest Protocol answers:
- how actors sign and bind acts;
- what proof is required;
- how non-repudiation and provenance are represented.

## 2. Scope
All mutating acts MUST be attested.

## 3. Required Elements
An attestation MUST include:
- signing method;
- signer identity reference;
- signature material;
- issuance time;
- optional certificate or trust-chain reference.

## 4. Verification
Implementations MUST verify:
- signature validity;
- signer binding to actor identity;
- authority scope at signing time;
- revocation status where supported.

## 5. Recommended Object
```json
{
  "method": "ed25519",
  "signer": "actor-123",
  "signature": "base64...",
  "cert_ref": "id-456",
  "issued_at": "timestamp"
}
```

## 6. Principle
Authority without proof is assertion. Attestation converts assertion into governed claim.

## 7. Implementation Status (added in Draft v0.4)

This section documents what a real, running implementation
(`cdp/core/services.py`, `db/ddl/010-identity-and-attestation.sql`,
`db/ddl/012-universal-attestation.sql`) has built against this RFC's
minimal requirements, across sessions 027-029
(`docs/session-027-identity-and-attestation.md`,
`docs/session-028-authority-and-delegation.md`,
`docs/session-029-universal-attestation.md`). This RFC specifies no
persistence schema in §§1-6 above; the schema described here is a
documented interpretation, not a claim that this RFC itself mandates
this exact shape.

### 7.1 Attestation Record (§3 partially satisfied, §4 not met)

A governed `cdp_core.attestation_record` table exists. Mapping against
§3's required elements:

| §3 element | Implementation |
|---|---|
| signing method | `attestation_method` -- controlled vocabulary: `shared_secret_reference`, `cryptographic_signature`, `delegated_trust_reference` |
| signer identity reference | `actor_id`, FK'd to a governed `cdp_core.actor` row |
| signature material | `credential_reference` -- an opaque reference/digest, never the secret or key material itself |
| issuance time | `issued_at` |
| certificate/trust-chain reference | not separately modeled; folded into `credential_reference` |

§4's verification requirements are **not met** by this implementation.
"Verification" here means: the attesting actor is registered and
active, and holds a recognized, in-scope Identity Claim
(RFC-CDP-030 §6.2) -- it does not check a cryptographic signature,
regardless of what `attestation_method` a caller declares.
`attestation_method: cryptographic_signature` is accepted as a value but
triggers no different verification path than
`shared_secret_reference`. `attestation_verification_result`'s `failed`
value is schema-supported but unused by the synchronous service path,
which fails closed via a raised exception instead of persisting a
failed-verification row. Signer binding to actor identity (§4's second
bullet) is checked in the sense that the claim must belong to the
attesting actor; revocation status (§4's fourth bullet) is checked via
the actor's `actor_status` and the claim's `recognition_status`, not via
a certificate-revocation mechanism.

### 7.2 Scope (§2: "All mutating acts MUST be attested")

As of Draft v0.4, five governed act types carry an attested proof path,
each requiring the same shape of proof (registered active actor,
recognized in-scope Identity Claim, correctly-scoped RFC-CDP-032
Authority Grant) before the underlying act is performed:

| `governed_act_type` | Introduced | Proof-path function |
|---|---|---|
| `decision_created` | session 027 | `attest_and_create_decision` |
| `challenge_raised` | session 029 | `attest_and_raise_challenge` |
| `challenge_adjudicated` | session 029 | `attest_and_adjudicate_challenge` |
| `execution_authorized` | session 029 | `attest_and_authorize_execution` |
| `execution_recorded` | session 029 | `attest_and_record_execution_attempt` |

§2's "all" is not yet reached: RFC-CDP-043 (Test), RFC-CDP-045
(Legitimize), and RFC-CDP-048 (Learn) have no governed service function
in the canonical implementation path to attest, and the Identity/
Attestation/Authority slices' own mutations (registering an actor,
submitting or deciding an Identity Claim, granting or revoking
authority) are deliberately excluded -- attesting them would be
circular, since they are the foundation this attestation mechanism
depends on, not acts it can be layered on top of.

Each attested act writes its own `attestation_record` row, disambiguated
from other sub-records on the same decision (e.g. which of several
challenges) by a `governed_act_ref_id` column
(`db/ddl/012-universal-attestation.sql`) -- an intentionally
un-FK-enforced polymorphic reference, since its target table depends on
`governed_act_type`.

### 7.3 Authority (a related but distinct check, not this RFC's own scope)

Since session 028, every attest_and_* proof path also evaluates an
RFC-CDP-032 Authority Grant matching the actor, the specific authority
type for that act (`PROPOSE`, `CHALLENGE`, `ADJUDICATE`,
`AUTHORIZE_EXECUTION`, `RECORD`), and the governed act's registry/
decision-class scope, and records the result as a
`cdp_core.authority_evaluation_result` row alongside the attestation
record. This satisfies §4's "authority scope at signing time" bullet,
but the mechanism belongs to RFC-CDP-032, not this RFC -- see that RFC
for its own scope statement.

### 7.4 What is deliberately not implemented

- **§4's cryptographic verification is not implemented at all** -- see
  §7.1. This is the largest gap between this RFC's text and the current
  implementation.
- **No caller authentication.** The API accepts a submitted `actor_id`
  at face value for who is attesting; nothing proves the HTTP caller
  controls that actor_id.
- **§2's "all mutating acts"** -- see §7.2 for the honest current
  coverage boundary.

### 7.5 Cross-reference

See RFC-CDP-030 §6 for the Identity Claim recognition mechanism this
RFC's proof path depends on, and RFC-CDP-032 for the Authority Grant
mechanism §7.3 describes.
