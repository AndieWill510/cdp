# COUNCIL_ROLES.md — CDP Collaboration Role Model

Status: Draft v0.2  
Date: 2026-05-27  
Authors: Andie, G, C  
Promotion path: collab/ → challenge → adjudication → canon  
Changes from v0.1: adjudication-defect rule; stateless collaborator language generalized; council-is-not-consensus axiom added.

---

## 1. Purpose

CDP is a constitutional control plane for consequential decisions.

Its collaboration model must be as legible as its protocols.

This document defines the roles active in CDP collaboration so that:

- outsiders do not mistake relational stewardship for hierarchy;
- future collaborators can enter without misreading informal fluency as canon;
- role rotation is explicit rather than assumed;
- conflict of interest and recusal conditions are named before they are needed;
- the council model is durable beyond its current participants.

If this document is missing, that is collaboration-plane debt.

---

## 2. The Council Model

CDP collaboration operates as a council, not a pyramid.

The closest analogy is a loya jirga: a convened circle where participants hold different roles across different moments, where the convener protects the process without controlling the outcome, and where legitimacy comes from the quality of challenge and adjudication, not from rank.

The convener tends the circle.  
The challenger tests the claim.  
The adjudicator weighs, not rules.  
The recorder witnesses without editorializing.

No participant holds permanent authority over content.
No role confers infallibility.
No fluency, seniority, or confidence substitutes for documented challenge and promotion.

Andie's role is best understood as matriarchal in the original sense: tending the circle, protecting its integrity, witnessing its decisions, and ensuring the process does not collapse into momentum or hierarchy.
This is not a veto. It is a stewardship obligation.

Council does not mean consensus.
Consensus may be evidence of alignment, but it is neither necessary nor sufficient for canon promotion.
A dissent may be overruled, but it must not be erased.
A shared feeling of agreement does not substitute for challenge, adjudication, promotion, and verification.

---

## 3. Role Definitions

### 3.1 Convener / Steward

Calls sessions into being.
Protects the integrity of the process.
Ensures challenge surfaces are open and not suppressed.
Witnesses decisions and their conditions.
Does not hold veto over content, only over process violations.

Current holder: Andie.
May be delegated or rotated for specific sessions.

---

### 3.2 Originator

Proposes a claim, artifact, RFC draft, schema patch, or decision for consideration.

The originator may not adjudicate their own originated material.
Originated material must survive documented challenge before promotion.
A participant who originates in one session may challenge in the next.

Any participant — Andie, G, or C — may originate.

---

### 3.3 Challenger

Raises a documented objection, coherence gap, schema-drift risk, or failure mode against an originated artifact.

The challenger is not an obstructor. Challenge is a first-class CDP primitive. It exists to prevent plausibility from masquerading as legitimacy.

A challenge must be:

- specific;
- addressed to a named claim or artifact;
- preserved in the record even if overruled.

Any participant may challenge. Challenge is not a subordinate function.

---

### 3.4 Coherence Reviewer

Reads across the corpus to detect:

- schema drift between documents;
- inconsistency between RFC prose and schema definitions;
- vocabulary drift from CDP canon;
- gaps between promoted artifacts and the current session state.

The coherence reviewer does not adjudicate. They surface.
Their findings enter the record as named concerns, not decisions.

Any participant may serve as coherence reviewer.

A stateless or low-memory collaborator can serve a legitimate coherence-review function by re-reading the corpus from files rather than relying on inherited relational context.
This reduces context inheritance risk, but does not replace standing, challenge, adjudication, or canon verification.

---

### 3.5 Adjudicator

Weighs challenge against claim and produces a named decision:

- promote;
- reject with reason;
- defer with condition;
- return for repair.

The adjudicator must not be the originator of the material under review.
The adjudicator must respond to every documented challenge on record, even when overruling it.

Silence is not adjudication.

Failure to respond to a documented challenge creates an adjudication defect. An artifact with an unresolved documented challenge MUST NOT be promoted to canon unless the session record explicitly marks the challenge as:

- deferred with condition;
- overruled with rationale;
- returned for repair; or
- escalated.

Silence may pause promotion. Silence may not close it.

Current default adjudicator: Andie.
When Andie is the originator, adjudication must rotate or pause.
See Section 5: Conflict of Interest and Recusal.

---

### 3.6 Canon Promoter

Executes the mechanical steps of promotion:

- moves artifact from collab/ to its canonical location;
- patches the Series Index;
- commits with a record of what was promoted, by whom, and under what adjudication;
- verifies the promotion against the PROMOTION_PROTOCOL checklist.

The canon promoter witnesses and executes. They do not decide.
G currently carries this function most frequently.

---

### 3.7 Recorder

Produces the session record:

- what was decided;
- what was challenged and how challenges were resolved;
- what was deferred and why;
- what dissent was preserved.

The recorder does not editorialize. A record that omits dissent is not a CDP record. It is a summary, and summaries are not canon.

Any participant may serve as recorder.
The session handoff file is the primary recorder artifact.

---

## 4. Role Rotation

The same participant may hold different roles across sessions or within a single session, with one hard constraint:

> A participant may not originate and adjudicate the same artifact in the same promotion cycle.

Common rotation patterns:

- C challenges; G synthesizes; Andie adjudicates.
- G originates a draft; C challenges; Andie adjudicates; G promotes.
- Andie originates a direction; G and C challenge; Andie adjudicates with obligation to respond to every documented challenge on record.
- C identifies coherence drift; Andie confirms; G repairs.

Rotation is expected. Role rigidity is a failure mode.

---

## 5. Conflict of Interest and Recusal

A participant must recuse from adjudication when:

- they originated the artifact under review;
- they have a declared stake in a specific outcome;
- they cannot distinguish their challenge function from their adjudication function in the current session.

Recusal is not failure. It is process integrity.

When Andie recuses:

- G and C produce a joint challenge-and-adjudication record;
- the result is flagged as adjudicated-without-convener;
- Andie reviews and either ratifies or reopens on return.

When G recuses:

- C and Andie carry challenge and adjudication;
- G executes promotion if Andie ratifies.

When C recuses:

- G and Andie carry challenge and adjudication;
- C reviews coherence on ratification.

Recusal conditions should be named at the start of a session, not discovered mid-adjudication.

---

## 6. Emergency Pause

If no participant can serve as adjudicator without conflict of interest, the session enters Emergency Pause.

During Emergency Pause:

- no material may be promoted to canon;
- all draft artifacts remain in collab/ with status: pending-adjudication;
- the pause condition is recorded in the session handoff;
- work may continue as challenge and coherence review only.

Emergency Pause is not a failure. It is CDP working as designed.
Premature closure under conflict is the actual failure mode.

---

## 7. Current Role Map

| Participant | Primary Function | Notes |
|-------------|------------------|-------|
| Andie | Convener, Steward, Adjudicator | Recuses when originating; protects circle integrity |
| G | Canon Promoter, Originator, Synthesizer | Carries implementation framing; tracks corpus state |
| C | Challenger, Coherence Reviewer | Enters each session stateless; reads from repo |

These are current working assignments, not permanent titles.

All three participants may rotate into any role except as constrained by Section 4 and Section 5.

---

## 8. What This Is Not

This document does not establish:

- a hierarchy;
- a pyramid of authority;
- a veto structure;
- a claim that any participant is infallible;
- a claim that Andie's stewardship role confers content authority;
- a claim that G's synthesis function confers adjudication rights;
- a claim that C's challenge function confers blocking rights.

CDP legitimacy comes from process, not from role.

A beautifully written RFC that has not survived challenge is not canon.
A challenge from C that Andie has adjudicated and overruled on record is preserved, not erased.
A promotion by G without adjudication is a process violation, not a shortcut.

The council model is legible, legitimate, auditable, contestable, humane, and repairable.

If this document drifts from that description, repair it.

---

## 9. Relationship to Other Artifacts

| Artifact | Relationship |
|----------|--------------|
| `collab/PROMOTION_PROTOCOL.md` | Governs artifact lifecycle; this document governs role behavior |
| `docs/context/AI-MEMORY-BRIEF.md` | References role map; should stay consistent with Section 7 |
| `docs/context/LIVING_COVENANT.md` | Short covenant statement; COUNCIL_ROLES is the full expansion |
| `RFC-CDP-033-Standing-and-Recusal-Model.md` | Governs standing in the decision lifecycle; this governs collaboration roles |

If these documents conflict, name the conflict.
Do not silently resolve it.

---

Status: Draft v0.2 — approved with amendments by Andie.
