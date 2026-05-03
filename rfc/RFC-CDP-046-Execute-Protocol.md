# RFC-CDP-007 — Execute Protocol

Author: Kevin “Andie” Williams  
Status: Draft v0.3  
Series: Constitutional Decision Plane (CDP)  
Date: March 17, 2026

## Abstract
Defines how a legitimized Decision becomes action.

## 1. Purpose
The Execute Protocol answers:
- how a legitimized decision becomes action;
- who may execute;
- what execution authorization looks like;
- what constraints, rollback hooks, and expiry rules apply.

## 2. Authority
Actors invoking this protocol MUST possess `EXECUTE` authority.

## 3. Preconditions
- Decision MUST be `LEGITIMIZED`;
- execution conditions imposed by legitimacy MUST be satisfied;
- required rollback or pause mechanisms MUST exist where feasible and policy requires them.

## 4. Semantics
Execution is bounded enactment.
It is not mere permission.
It is authorization + operationalization under constraints.

## 5. Execution Controls
Execution payloads SHOULD specify:
- target system or domain;
- effective window;
- idempotency key;
- retry policy;
- rollback strategy;
- observability hooks;
- termination conditions;
- escalation contacts.

## 6. State Transitions
- `LEGITIMIZED → EXECUTING`
- `EXECUTING → EXECUTED`
- `EXECUTING → FAILED`
- `EXECUTING → ROLLED_BACK`

## 7. Recommended Payload
```json
{
  "authorization_ref": "string",
  "target": "string",
  "idempotency_key": "string",
  "execution_window": {
    "start": "timestamp",
    "end": "timestamp"
  },
  "rollback_ref": "string",
  "retry_policy": {
    "max_attempts": 3
  },
  "termination_conditions": ["string"],
  "metadata": {}
}
```

## 8. Principle
Authorization is not the same thing as safe execution. Execution remains subordinate to governance.
