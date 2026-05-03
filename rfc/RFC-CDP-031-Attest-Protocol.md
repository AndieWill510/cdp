# RFC-CDP-011 — Attest Protocol

Author: Kevin “Andie” Williams  
Status: Draft v0.3  
Series: Constitutional Decision Plane (CDP)  
Date: March 17, 2026

## Abstract
Defines how actors sign, attest, and bind authority to acts.

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
