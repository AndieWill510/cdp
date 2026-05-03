# RFC-CDP-018 — Governance State Machine

Author: Kevin “Andie” Williams  
Status: Draft v0.3  
Series: Constitutional Decision Plane (CDP)  
Date: March 17, 2026

## Abstract
Defines the formal states and transitions each protocol may cause.

## 1. Purpose
This RFC answers:
- what the formal states are;
- what transitions each protocol may cause;
- how convergence, escalation, revision, and failure states behave.

## 2. Recommended States
`DRAFT, PROPOSED, UNDER_DELIBERATION, UNDER_TEST, ADJUDICATED, LEGITIMIZED, EXECUTING, EXECUTED, FAILED, ROLLED_BACK, RECORDED, LEARNED, REJECTED, WITHDRAWN, ESCALATED`

## 3. Core Transition Rules
- Propose introduces `PROPOSED`.
- Challenge enters or maintains `UNDER_DELIBERATION`.
- Test enters or maintains `UNDER_TEST`.
- Adjudicate produces `ADJUDICATED`, `REJECTED`, or `ESCALATED`.
- Legitimize produces `LEGITIMIZED`, `REJECTED`, or `ESCALATED`.
- Execute produces `EXECUTING`, then `EXECUTED`, `FAILED`, or `ROLLED_BACK`.
- Record produces `RECORDED`.
- Learn produces `LEARNED`.

## 4. Forbidden Patterns
Implementations MUST prevent:
- `PROPOSED → EXECUTED`;
- execution without legitimacy;
- adjudication without challenge satisfaction under policy;
- loss of prior history.

## 5. Principle
State transitions are where governance becomes enforceable.
