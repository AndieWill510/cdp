# RFC-CDP-004 — Test Protocol

Author: Kevin “Andie” Williams  
Status: Draft v0.3  
Series: Constitutional Decision Plane (CDP)  
Date: March 17, 2026

## Abstract
Defines validation of Decisions through evidence, simulation, precedent, verification, and empirical evaluation.

## 1. Purpose
The Test Protocol answers:
- what evidence supports or refutes a Decision;
- how a Decision is validated before adjudication;
- what outputs of testing are valid.

## 2. Authority
Actors invoking this protocol MUST possess `TEST` authority. Test authority MAY be specialized.

## 3. Preconditions
- Decision MUST exist;
- Decision MUST be in `UNDER_DELIBERATION` or `UNDER_TEST`;
- Envelope, identity, and attestation MUST validate.

## 4. Test Types
- `simulation`
- `empirical`
- `policy`
- `precedent`
- `verification`

## 5. State Transitions
- `UNDER_DELIBERATION → UNDER_TEST`
- `UNDER_TEST → UNDER_DELIBERATION`

Testing MAY be iterative.

## 6. Semantics
A Test is a structured attempt to validate or invalidate claims within a Decision.

A Test MUST:
- produce observable output;
- be attributable;
- state its method;
- include reproducibility material or explain limitations.

A Test MUST NOT:
- grant authority;
- bypass challenge;
- directly authorize execution.

## 7. Recommended Payload
```json
{
  "test_type": "simulation | empirical | policy | precedent | verification",
  "claim": "string",
  "method": "string",
  "inputs": ["string"],
  "artifacts": ["uri"],
  "result": {
    "status": "pass | fail | mixed | inconclusive",
    "summary": "string"
  },
  "confidence": {
    "level": "low | medium | high",
    "notes": "string"
  },
  "limitations": ["string"],
  "metadata": {}
}
```

## 8. Effects
Accepted Test results are attached to the Decision and become available to adjudicators.

## 9. Principle
Propose introduces intent. Challenge introduces tension. Test introduces reality.
