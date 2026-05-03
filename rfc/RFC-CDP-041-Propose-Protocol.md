# RFC-CDP-002 — Propose Protocol

Author: Kevin “Andie” Williams  
Status: Draft v0.3  
Series: Constitutional Decision Plane (CDP)  
Date: March 17, 2026

## Abstract
Defines the canonical mechanism by which a Decision is introduced, amended, or resubmitted into CDP.

## 1. Purpose
The Propose Protocol:
- creates a new Decision or amends an existing one;
- defines initial intent, scope, and constraints;
- establishes the baseline object for all subsequent acts.

## 2. Authority
Actors invoking this protocol MUST possess `PROPOSE` authority. Authority MUST be verifiable via Identify and Attest.

## 3. Preconditions
- actor identity MUST be established;
- Envelope MUST conform to RFC-CDP-014;
- Decision MUST conform to RFC-CDP-013;
- for new Decisions, `decision_id` MUST be unique;
- for amendments, the Decision MUST exist.

## 4. State Transitions
- `NULL → PROPOSED`
- `{ALLOWED_STATE} → PROPOSED` for revision or resubmission

## 5. Semantics
A Propose act is an offer into governance.
It does not assert truth.
It does not confer legitimacy.
It introduces structured intent.

## 6. Effects
Upon successful processing:
- Decision enters `PROPOSED`;
- Decision becomes eligible for Challenge;
- lineage is established or extended;
- authority history is updated.

## 7. Payload Schema
Content-Type: `application/cdp.propose+json`

```json
{
  "proposal_type": "create | amend | resubmit",
  "title": "string",
  "description": "string",
  "objective": "string",
  "rationale": "string",
  "policy_scope": "string",
  "constraints": ["string"],
  "assumptions": ["string"],
  "expected_outcomes": ["string"],
  "risk_profile": {
    "level": "low | medium | high | critical",
    "factors": ["string"]
  },
  "required_authorities": ["PROPOSE","CHALLENGE","TEST","ADJUDICATE","LEGITIMIZE","EXECUTE","RECORD"],
  "requested_tests": [
    {
      "test_type": "simulation | policy | empirical | precedent",
      "description": "string"
    }
  ],
  "references": ["string"],
  "attachments": ["uri"],
  "metadata": {}
}
```

## 8. Validation Rules
A valid Propose payload MUST:
- include title, description, and objective;
- define a policy scope;
- specify at least one required authority;
- include sufficient information for Challenge and Test.

## 9. Idempotency
Repeated Propose messages with identical `message_id` SHOULD be treated as idempotent.

## 10. Principle
Propose defines the world. Learn later corrects the world.
