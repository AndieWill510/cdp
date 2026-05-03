# RFC-CDP-019 — Execution State Machine

Author: Kevin “Andie” Williams  
Status: Draft v0.3  
Series: Constitutional Decision Plane (CDP)  
Date: March 17, 2026

## Abstract
Defines what happens after legitimacy.

## 1. Purpose
This RFC answers:
- how authorization, execution, rollback, retry, and record transitions work;
- how termination is guaranteed.

## 2. Recommended States
`AUTHORIZED, DISPATCHED, IN_PROGRESS, PAUSED, RETRYING, COMPLETED, FAILED, ROLLED_BACK, TERMINATED`

## 3. Entry Condition
Execution state machine entry MUST require a valid legitimacy artifact and all execution preconditions required by policy.

## 4. Transition Guidance
- `AUTHORIZED → DISPATCHED`
- `DISPATCHED → IN_PROGRESS`
- `IN_PROGRESS → COMPLETED`
- `IN_PROGRESS → PAUSED`
- `IN_PROGRESS → FAILED`
- `FAILED → RETRYING`
- `FAILED → ROLLED_BACK`
- `PAUSED → IN_PROGRESS`
- terminal failure paths MAY become `TERMINATED`

## 5. Required Controls
Implementations SHOULD support:
- idempotency keys;
- retry caps;
- rollback references;
- pause or kill switch;
- execution telemetry;
- final outcome summary.

## 6. Principle
Authorization is not the same thing as safe enactment.
