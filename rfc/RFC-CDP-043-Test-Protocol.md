# RFC-CDP-043 — Test Protocol

Author: Kevin “Andie” Williams  
Status: Draft v0.4  
Series: Constitutional Decision Plane (CDP)  
Date: July 16, 2026  
Updates: RFC-CDP-043 v0.3  
Depends On: RFC-CDP-020, RFC-CDP-033, RFC-CDP-034

## Abstract
Defines validation of Decisions through evidence, simulation, precedent, verification, empirical evaluation, and Participation Integrity testing.

## 1. Purpose
The Test Protocol answers:
- what evidence supports or refutes a Decision;
- how a Decision is validated before adjudication;
- what outputs of testing are valid;
- whether constitutionally protected participation remained intact in practice when RFC-CDP-034 applies.

## 2. Authority
Actors invoking this protocol MUST possess `TEST` authority and valid Test-stage Standing. Test authority MAY be specialized.

## 3. Preconditions
- Decision MUST exist;
- Decision MUST be in `UNDER_DELIBERATION` or `UNDER_TEST`;
- Envelope, identity, attestation, and Standing MUST validate;
- known Sovereignty Claims MUST be handled under RFC-CDP-074 before ordinary Participation Integrity testing is applied.

## 4. Test Types
- `simulation`
- `empirical`
- `policy`
- `precedent`
- `verification`
- `participation_integrity`
- `operational_reachability`

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
- include reproducibility material or explain limitations;
- distinguish absence of evidence from evidence of integrity.

A Test MUST NOT:
- grant authority;
- create Standing;
- bypass challenge;
- directly authorize execution;
- convert decision-local credibility findings into generalized trustworthiness scores.

## 7. Participation Integrity testing
When required by RFC-CDP-034, Test MUST support evidence concerning:

- allocation integrity;
- accessible and timely entry;
- accurate representation;
- evaluation and credibility standards;
- materially plausible revision paths;
- review independence and reason preservation;
- immediate and downstream repair;
- operational reachability across materially similar participants;
- authority-downgrading risk.

Permitted methods include:

- sampled decision-record review;
- counterfactual comparison of materially similar cases;
- reversal rates by participant or source type;
- abandonment and delay rates;
- review of actual credibility rationales;
- accessibility effectiveness testing;
- review of whether testimony was understood before rejection;
- review of whether successful challenges repaired downstream records.

A Participation Integrity test result SHOULD reference the corresponding `participation_integrity_attestation` under RFC-CDP-034.

## 8. Recommended Payload
```json
{
  "test_type": "simulation | empirical | policy | precedent | verification | participation_integrity | operational_reachability",
  "claim": "string",
  "method": "string",
  "inputs": ["string"],
  "artifacts": ["uri"],
  "participation_integrity_attestation_ref": "ref|null",
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

## 9. Effects
Accepted Test results are attached to the Decision and become available to adjudicators.

Participation Integrity testing MUST NOT itself declare legitimacy. It produces evidence consumed by Adjudicate and Legitimize.

## 10. Principle
Propose introduces intent. Challenge introduces tension. Test introduces reality.

A participation right that exists only on paper has not yet survived Test.
