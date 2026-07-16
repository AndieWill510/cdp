# RFC-CDP-044 — Adjudicate Protocol

Author: Kevin “Andie” Williams  
Status: Draft v0.4  
Series: Constitutional Decision Plane (CDP)  
Date: July 16, 2026  
Updates: RFC-CDP-044 v0.3  
Depends On: RFC-CDP-020, RFC-CDP-033, RFC-CDP-034, RFC-CDP-043

## Abstract
Defines the formal judgment mechanism for CDP, including explicit treatment of Participation Integrity where applicable.

## 1. Purpose
Adjudicate produces a structured judgment over the current deliberative posture of a Decision.

It must distinguish whether a participant had valid Standing from whether that participation retained integrity in practice.

## 2. Authority
Actors invoking this protocol MUST possess `ADJUDICATE` authority and valid Adjudicate-stage Standing.

## 3. Preconditions
- Decision MUST exist;
- Challenge requirements MUST be satisfied under policy;
- blocking challenges MUST be resolved or explicitly overruled with basis;
- relevant tests MUST be attached or explicitly waived by policy;
- required Participation Integrity tests or attestations MUST be attached, pending with explicit basis, or validly excepted;
- Sovereignty Claims or Authority Conflicts MUST be handled under RFC-CDP-032 and RFC-CDP-074.

## 4. Dispositions
Adjudication MAY yield:
- `approve_for_legitimacy_review`
- `reject`
- `revise_and_resubmit`
- `escalate`
- `defer_pending_test`
- `defer_pending_participation_integrity_review`
- `refer_to_repair`
- `refer_to_sovereignty_process`

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
- whether legitimacy review may proceed;
- Standing and Authority distinctions relevant to the judgment;
- Participation Integrity status when RFC-CDP-034 applies;
- any Sovereignty Claim or Authority Conflict disposition;
- any required Review or Repair path.

Where Participation Integrity is material, the adjudication SHOULD record:

- what contribution domains were recognized;
- whether entry and representation remained intact;
- what evaluation or credibility standards were applied;
- what materially sufficient contribution could have changed the result;
- whether rejection or discount was independently reviewable;
- whether immediate and downstream repair is required;
- unresolved uncertainty.

An adjudicator MUST NOT treat a valid Participation Integrity Attestation as proof that the decision is correct.

An adjudicator MUST NOT treat a failed or compromised attestation as a credibility judgment about the participant. It is a judgment about the process.

## 7. Principle
Judgment must be explicit, reviewable, and grounded in the record.

Adjudication must not confuse the participant’s Standing, the process’s Participation Integrity, the evidence’s quality, and the decision’s correctness.
