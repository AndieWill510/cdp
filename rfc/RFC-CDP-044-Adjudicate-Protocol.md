# RFC-CDP-005 — Adjudicate Protocol

Author: Kevin “Andie” Williams  
Status: Draft v0.3  
Series: Constitutional Decision Plane (CDP)  
Date: March 17, 2026

## Abstract
Defines the formal judgment mechanism for CDP.

## 1. Purpose
Adjudicate produces a structured judgment over the current deliberative posture of a Decision.

## 2. Authority
Actors invoking this protocol MUST possess `ADJUDICATE` authority.

## 3. Preconditions
- Decision MUST exist;
- Challenge requirements MUST be satisfied under policy;
- blocking challenges MUST be resolved or explicitly overruled with basis;
- relevant tests MUST be attached or explicitly waived by policy.

## 4. Dispositions
Adjudication MAY yield:
- `approve_for_legitimacy_review`
- `reject`
- `revise_and_resubmit`
- `escalate`
- `defer_pending_test`

## 5. State Transitions
- `UNDER_DELIBERATION → ADJUDICATED`
- `UNDER_TEST → ADJUDICATED`
- `ADJUDICATED → PROPOSED` for revision, where allowed
- `ADJUDICATED → ESCALATED`

## 6. Required Output
An adjudication MUST include:
- disposition;
- rationale;
- challenges considered;
- tests considered;
- unresolved risks;
- whether legitimacy review may proceed.

## 7. Principle
Judgment must be explicit, reviewable, and grounded in the record.
