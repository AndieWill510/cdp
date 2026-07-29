# RFC-CDP-003 — Answerability Principle

Author: Kevin “Andie” Williams / ChatGPT  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: July 29, 2026  
Updates: RFC-CDP-001, RFC-CDP-033, RFC-CDP-045  
Related: RFC-CDP-002, RFC-CDP-032, RFC-CDP-042, RFC-CDP-070, RFC-CDP-074

---

## Abstract

This RFC establishes **answerability** as a constitutional principle of the Constitutional Decision Plane.

Answerability is not created by procedure. It arises when the exercise of power may materially affect another actor, community, authority, record, right, resource, relationship, or future.

CDP recognizes, protects, tests, and operationalizes answerability through standing, challenge, adjudication, legitimacy, record, appeal, remedy, and repair.

A decision MUST NOT be treated as constitutionally legitimate merely because required procedure was completed. The governed path MUST also preserve and address applicable answerability claims.

---

## 1. Purpose

This RFC answers:

- what makes power answerable;
- how answerability differs from procedural compliance;
- why constitutional standing is recognized rather than institutionally manufactured;
- how unresolved answerability claims affect legitimacy;
- how answerability is represented without creating a new lifecycle stage;
- how CDP avoids institutional self-exemption and false closure.

---

## 2. Core Principle

Power is constitutionally answerable when its exercise may materially affect another actor, community, authority, record, right, resource, relationship, or future.

Answerability arises from the consequence-bearing relationship. It does not depend on recognition, permission, legibility, procedural admission, or institutional approval by the actor or institution being challenged.

CDP does not create the underlying obligation. CDP recognizes, preserves, tests, and operationalizes it.

No actor may extinguish an answerability relationship solely by:

- denying standing;
- withholding recognition;
- controlling the record;
- completing internal procedure;
- rejecting the claim without a contestable determination;
- declaring closure;
- treating institutional self-approval as resolution.

---

## 3. Answerability and Procedure

CDP distinguishes procedural validity from constitutional legitimacy.

A process may be fully recorded, internally compliant, institutionally approved, and procedurally complete while remaining unanswerable to those whose rights, interests, evidence, authority, communities, or futures it affects.

Procedure can preserve, demonstrate, test, or defeat a claim to legitimacy.

Procedure does not create the relationships that make power answerable.

Therefore:

> Procedural completion does not by itself establish constitutional legitimacy.

And:

> Procedure may establish procedural validity. It does not extinguish answerability.

---

## 4. Constitutional Standing

Constitutional standing is the procedural recognition and protection of an underlying answerability relationship.

Some actors have standing because their relationship to a decision makes the exercise of power answerable to them, not because another actor grants permission.

At minimum, CDP recognizes constitutional standing for:

- affected parties;
- evidence custodians;
- record-keepers.

CDP recognizes and protects this standing. It does not create the consequence-bearing relationship from which the standing arises.

No actor may revoke constitutional standing. Its scope, stage, or application may be challenged under RFC-CDP-033, but its existence MUST NOT depend on approval by the actor, institution, or system being challenged.

Denial, suppression, artificial narrowing, or procedural laundering of constitutional standing is a governance breach and MUST be recordable, contestable, appealable, and repairable.

### 4.1 Constitutional Root

Standing ordinarily appears to require recognition: a system records who may participate, at what stage, in what role, and under what constraints.

That procedural fact creates a deeper question:

> What makes the system answerable to a participant before the system has recognized that participant?

Some relationships make the exercise of power answerable to another actor. A decision may affect a person, community, right, resource, record, body of evidence, jurisdiction, repair claim, or future. That consequence-bearing relationship exists before the institution records it and may persist even when the institution denies it.

Constitutional standing is CDP’s procedural recognition and protection of that prior answerability relationship.

Therefore:

- CDP does not manufacture affected-party standing;
- CDP does not grant itself moral authority by declaring an axiom;
- CDP recognizes that certain relationships create claims the governed process must hear, preserve, and answer;
- institutional denial cannot extinguish the underlying relationship;
- procedural recognition makes the claim actionable, contestable, auditable, and repairable within CDP.

Affected-party, evidence-custodian, and record-keeper standing are constitutional because CDP cannot make a legitimate claim to govern while excluding the actors to whom the exercise of governance is answerable.

The constitutional regress does not stop because CDP appoints itself the ultimate granter. It stops because the obligation is grounded in the relationship between power and consequence.

### 4.2 Standing Representation

Constitutional standing is not institutionally granted; it is recognized and protected by CDP.

Where a standing schema requires a granter, constitutional standing SHOULD be represented as:

```yaml
standing_granted_by: null
standing_recognition_basis: constitutional_answerability
```

or an equivalent explicit representation that does not falsely identify an institutional granter.

### 4.3 Answerability Test

A claim to constitutional standing SHOULD be evaluated by asking:

1. What governed act, decision, omission, record, or execution is at issue?
2. What material consequence may follow or has followed?
3. What relationship connects the claimant to that consequence?
4. What form of answer is owed: notice, participation, evidence preservation, challenge, review, appeal, remedy, repair, or closure contestation?
5. What evidence or counterexample would narrow or defeat the claimed scope of standing?

The claimant need not prove final harm before preliminary affected-party standing is recognized. Scope may be challenged. Existence MUST NOT be denied solely because the responding institution disputes the consequence.

---

## 5. Legitimacy

CDP distinguishes:

- **Integrity**: the governed path record has not been silently mutated.
- **Sufficiency**: the proposal earned admission into the governed lifecycle.
- **Procedural legitimacy**: the decision was made through a valid CDP process by actors with valid standing and authority, with required challenge, sufficiency, repair, dissent, and record conditions addressed.
- **Constitutional legitimacy**: the governed decision remains answerable to those materially affected and to implicated authority systems, and applicable answerability claims have been recognized, preserved, and addressed without erasure, false closure, or institutional self-exemption.
- **Correctness**: the decision is factually, technically, ethically, legally, culturally, or operationally right in the relevant domain.
- **Hierarchy**: a role, rank, office, organizational position, or chain-of-command relationship that may confer delegated authority in some institutional contexts.

These are distinct.

Integrity is necessary but not sufficient for sufficiency.

Sufficiency is necessary but not sufficient for procedural legitimacy.

Procedural legitimacy is necessary but not sufficient for constitutional legitimacy when material answerability claims remain applicable.

Constitutional legitimacy is necessary but not sufficient for correctness.

Hierarchy is neither necessary nor sufficient for legitimacy.

A decision can have:

- integrity without sufficiency;
- sufficiency without procedural legitimacy;
- procedural legitimacy without constitutional legitimacy;
- constitutional legitimacy without correctness;
- hierarchy without legitimacy;
- legitimacy without hierarchy;
- a valid hash preserving an illegitimate process;
- a sufficient proposal adjudicated by actors without valid standing;
- completed internal procedure that remains unanswerable to affected parties;
- hierarchical approval that bypassed affected-party standing, challenge, repair, dissent, or sovereignty authority.

Therefore:

> A decision MUST NOT be treated as constitutionally legitimate while material answerability claims are erased, excluded, falsely resolved, or denied a governed path.

---

## 6. Legitimation Requirements

Before a decision may be constitutionally legitimized:

- applicable answerability relationships and claims MUST be identified;
- affected-party, evidence-custodian, record-keeper, repair, and sovereignty standing MUST be preserved where applicable;
- the governed path MUST show how material answerability claims were answered, deferred with valid controls, or preserved as unresolved;
- institutional self-approval MUST NOT be treated as resolution of an answerability claim.

Legitimation MUST block when:

1. A material answerability claim has been erased, denied without a contestable determination, or excluded from the governed path.
2. The legitimacy record relies on procedural completion to declare an affected-party, repair, or sovereignty claim resolved without required review.
3. The decision’s claimed legitimacy would depend on the responding institution being the sole judge of whether it owes an answer.

These conditions are hard stops unless a valid emergency path expressly preserves the unresolved claim and creates time-bounded post-hoc review, appeal, record, and repair obligations.

---

## 7. Record Requirements

A legitimacy record SHOULD include:

```yaml
answerability_claim_refs: [<ref>]
answerability_disposition_refs: [<ref>]
unresolved_answerability_refs: [<ref>]
constitutional_legitimacy_status: <satisfied|conditionally_satisfied|blocked|unresolved>
```

`answerability_claim_refs` MAY be empty only when the legitimizer positively attests that no material answerability relationship applies.

`unresolved_answerability_refs` MUST preserve material unresolved claims. An unresolved claim MUST NOT be omitted merely because an institution has rejected or declined to recognize it.

`constitutional_legitimacy_status: satisfied` MUST NOT be asserted when a material answerability claim remains erased, unrecorded, or falsely closed.

---

## 8. Relationship to Existing RFCs

### 8.1 RFC-CDP-001

RFC-CDP-001 MUST be read as including answerability as a constitutional condition of legitimate power.

Its references to constitutional standing mean standing recognized and protected as the procedural expression of consequence-bearing relationships, not standing manufactured by institutional grant.

### 8.2 RFC-CDP-033

This RFC supersedes RFC-CDP-033 Section 11.1 to the extent that Section 11.1 describes constitutional standing as granted axiomatically by the CDP framework.

Constitutional standing is instead recognized and protected by CDP because of an underlying answerability relationship.

In RFC-CDP-033’s Standing Grant Authority table, the `Granted By` value for constitutional standing MUST be interpreted as:

```text
Not institutionally granted; recognized and protected by CDP
```

### 8.3 RFC-CDP-045

RFC-CDP-045 MUST distinguish procedural legitimacy from constitutional legitimacy as defined here.

Legitimize does not make power answerable. It tests whether answerability has been honored sufficiently for governed enactment.

Where RFC-CDP-045 uses the unqualified term `legitimacy`, implementations MUST determine from context whether procedural legitimacy, constitutional legitimacy, or both are required. High-risk, rights-affecting, repair-sensitive, sovereignty-sensitive, irreversible, or externally affecting decisions MUST require constitutional legitimacy.

---

## 9. Invariants

The following MUST hold:

- power remains answerable to materially affected parties and implicated authorities;
- procedural completion does not by itself establish constitutional legitimacy;
- constitutional standing is recognized and protected rather than institutionally manufactured;
- unresolved answerability claims remain visible and contestable;
- institutional self-approval does not resolve answerability;
- answerability claims remain subject to evidence, scope, authority, contestability, and recusal requirements;
- answerability does not authorize CDP to determine sovereignty it does not hold.

---

## 10. Non-Effects

This RFC does not:

- create a new lifecycle stage;
- create an unbounded right to participate in every stage;
- eliminate standing scope challenges or recusal;
- make correctness equivalent to legitimacy;
- authorize CDP to determine sovereignty it does not hold;
- permit an affected-party claim to bypass evidence, scope, authority, or contestability requirements.

---

## 11. Foundational Statement

CDP does not create the relationships that make power answerable. It recognizes and protects them.

CDP preserves standing, dissent, authority, memory, harm, remedy, return obligations, sovereignty claims, and repair so that power can be made legible, answerable, legitimate, contestable, accountable, correctable, and capable of returning what should not have been taken.
