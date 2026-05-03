# RFC-CDP-003 — Challenge Protocol

Author: Kevin “Andie” Williams  
Status: Draft v0.3  
Series: Constitutional Decision Plane (CDP)  
Date: March 17, 2026

## Abstract
Defines structured dissent, critique, and adversarial pressure for CDP.

## 1. Purpose
The Challenge Protocol MUST:
- introduce structured dissent;
- expose weaknesses in a Decision;
- require clarification, amendment, or validation;
- enforce deliberation prior to adjudication.

Challenge is not optional.

## 2. Authority
Actors invoking this protocol MUST possess `CHALLENGE` authority. The system MUST ensure that Challenge authority is not artificially restricted.

## 3. Preconditions
- a Decision MUST exist;
- the Decision MUST be in `PROPOSED` or `UNDER_DELIBERATION`;
- Envelope, identity, and attestation MUST validate.

## 4. Mandatory Deliberation Gate
A Decision MUST NOT proceed to Adjudication unless:
- at least one Challenge has been recorded; or
- a formal `no challenge` condition has been explicitly attested under policy.

Silence MUST NOT be interpreted as agreement.

## 5. State Transitions
- `PROPOSED → UNDER_DELIBERATION`
- `UNDER_DELIBERATION → UNDER_DELIBERATION`

Challenge MUST NOT advance the lifecycle. It deepens or blocks progression.

## 6. Payload Schema
Content-Type: `application/cdp.challenge+json`

```json
{
  "challenge_type": "logical | evidentiary | policy | ethical | operational",
  "severity": "low | medium | high | blocking",
  "target": {
    "field": "string",
    "reference": "optional pointer"
  },
  "argument": "string",
  "requested_action": "clarify | amend | provide_evidence | run_test | reject",
  "requested_tests": [
    {
      "test_type": "simulation | empirical | policy | precedent",
      "description": "string"
    }
  ],
  "counterproposal": {
    "description": "optional",
    "rationale": "optional"
  },
  "evidence_refs": ["string"],
  "impact_assessment": {
    "risk": "low | medium | high",
    "scope": "local | domain | systemic"
  },
  "metadata": {}
}
```

## 7. Severity Enforcement
If a Challenge is marked `blocking`, the Decision MUST NOT advance to Adjudication until:
- the Challenge is resolved; or
- the Challenge is explicitly adjudicated as non-blocking.

## 8. Determinism Guarantee
CDP does not enforce deterministic outcomes.
CDP MUST enforce deterministic process:
- all valid Challenges are processed;
- all blocking Challenges are resolved;
- all decisions pass through adversarial scrutiny.

## 9. Principle
The universe may be probabilistic. The court is not.
