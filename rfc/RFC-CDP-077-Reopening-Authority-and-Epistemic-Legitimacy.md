# RFC-CDP-077 — Reopening Authority and Epistemic Legitimacy

Author: Kevin “Andie” Williams  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: July 14, 2026  
Updates: RFC-CDP-045, RFC-CDP-070, RFC-CDP-073, RFC-CDP-076, RFC-CDP-092  
Depends On: RFC-CDP-001, RFC-CDP-002, RFC-CDP-023, RFC-CDP-033, RFC-CDP-042, RFC-CDP-044, RFC-CDP-045, RFC-CDP-070, RFC-CDP-073, RFC-CDP-076

## Abstract

This RFC defines **Reopening Authority and Epistemic Legitimacy** for the CDP Repair plane.

It establishes that a consequential decision does not become permanently legitimate merely because the decision lifecycle, appeal process, or repair process reached procedural closure.

A closed decision MUST remain eligible for bounded reopening when:

- material evidence changes;
- the governing account is shown to be materially false or incomplete;
- the original process denied a materially affected party meaningful standing as a knower;
- challenge was permitted against the outcome while the assumptions, classifications, model outputs, policies, or institutional account that produced it remained insulated from revision;
- repair completed procedurally but failed in efficacy;
- unresolved conflicts of evidence or authority were flattened into closure.

This RFC introduces a minimum Reopening Request Record, a Reopening Determination Record, reopening trigger semantics, independent reopening authority, bounded-closure rules, downstream correction requirements, and explicit integration with appeals, affected-party review, repair efficacy, legitimacy, and the Repair State Machine.

The purpose is not endless relitigation.

The purpose is to prevent procedural finality from laundering epistemic failure into durable authority.

---

## 1. Failure Mode

The primary failure mode is **closure laundering epistemic illegitimacy**.

A CDP-governed process may be formally complete while remaining epistemically defective:

- an appeal existed, but the appellant was treated as presumptively confused, unstable, biased, nontechnical, adversarial, or incapable of interpreting their own experience;
- testimony entered the record but could not revise the institution’s governing account;
- a challenge could dispute the outcome but not the classification, policy interpretation, model output, or factual narrative that produced it;
- a repair process completed, but repair efficacy remained disputed or unassessed;
- authoritative records, systems, reviewers, or witnesses materially disagreed and the disagreement was resolved by hierarchy rather than adjudication;
- repeated contestation was treated as evidence that the challenger lacked credibility;
- “the matter is closed” was used as the reason closure could not be examined.

A formally contestable process can still be epistemically illegitimate.

CDP MUST prevent closure from becoming an unreviewable source of legitimacy.

---

## 2. Core Principle

> A consequential decision does not earn legitimacy merely because it can be challenged. The challenge process must preserve the challenger’s standing as a knower and permit evidence to revise both the decision and the governing account by which the decision is justified.

A decision remains legitimate only while its closure basis remains supportable.

Where closure depends on silencing, pathologizing, discrediting, or structurally excluding relevant knowledge, reopening is not a courtesy.

It is a repair obligation.

---

## 3. Definitions

### 3.1 Reopening Authority

**Reopening Authority** is the bounded authority to return a closed or procedurally terminal decision, appeal, adjudication, legitimacy determination, or repair process to active governed review when a recognized reopening trigger is credibly alleged.

Reopening authority is distinct from:

- ordinary lifecycle challenge under RFC-CDP-042;
- first-entry appeal under RFC-CDP-070;
- adjudication under RFC-CDP-044;
- repair-efficacy review under RFC-CDP-076;
- rollback or compensation under RFC-CDP-053 and RFC-CDP-054.

Reopening may invoke one or more of those mechanisms after reopening is granted.

### 3.2 Epistemic Legitimacy

**Epistemic Legitimacy** is the property of a decision process that preserves the possibility that relevant participants can contribute knowledge capable of revising:

- the outcome;
- the factual record;
- the evidentiary interpretation;
- the classification or model output;
- the policy or rule application;
- the governing account;
- the legitimacy determination;
- downstream records and actions.

Permission to object is necessary but not sufficient.

Objection must remain capable of mattering.

### 3.3 Governing Account

The **Governing Account** is the factual, interpretive, procedural, technical, and normative account used to justify a decision.

It includes:

- stated reasons;
- material evidence;
- model outputs and classifications;
- assumptions about credibility;
- assumptions about standing and authority;
- policy and rule interpretations;
- known uncertainties;
- simplifications and exclusions;
- unresolved conflicts;
- the account of what happened and why the decision was legitimate.

### 3.4 Bounded Closure

**Bounded Closure** is a procedural state meaning:

> closed under the present governed record, while remaining reopenable upon recognized evidence of material error, epistemic exclusion, changed governing conditions, unresolved authority conflict, or failed repair.

Bounded closure preserves stability without claiming infallibility.

---

## 4. Reopening Triggers

A closed or terminal governed process MUST permit submission of a Reopening Request when one or more of the following triggers is credibly alleged.

### 4.1 Material New Evidence

Evidence unavailable or not reasonably discoverable during the original process could materially change the outcome, legitimacy basis, or governing account.

### 4.2 Material Factual Error

The decision relied on a factual claim that is false, materially incomplete, internally inconsistent, or no longer supportable.

### 4.3 Material Process Defect

Required notice, access, evidence disclosure, representation, accommodation, explanation, challenge, adjudication, affected-party review, or opportunity to respond was absent or materially ineffective.

### 4.4 Epistemic Exclusion

A materially affected participant’s testimony, interpretation, warning, or contextual knowledge was discounted because of identity, disability, communication style, affect, institutional status, disputed credibility, or presumed incapacity rather than the evidentiary quality of the account.

### 4.5 Non-Contestable Governing Account

The process permitted challenge to the outcome while insulating one or more of the following from revision:

- material assumptions;
- classification;
- model output;
- policy interpretation;
- credibility rule;
- institutional narrative;
- authority claim;
- legitimacy basis.

### 4.6 Changed Governing Conditions

A relevant law, policy, model, classification, authority relationship, risk threshold, jurisdiction, or material circumstance changed enough that continued reliance on the closed decision may no longer be legitimate.

### 4.7 Demonstrated Repair-Efficacy Failure

A process completed procedurally, but a Repair Efficacy Record under RFC-CDP-076 shows or credibly alleges that:

- efficacy is disputed;
- repair did not change the conditions that produced or preserved the harm;
- a false governing account remains operative;
- downstream records remain uncorrected;
- future review became due;
- completion evidence proved activity but not repair.

### 4.8 Conflict of Evidence or Authority

Authoritative records, reviewers, systems, affected parties, institutions, communities, or sovereign authorities materially disagree, and the conflict was not resolved through legible adjudication.

### 4.9 Legitimacy Basis Failure

A legitimacy determination under RFC-CDP-045 relied on a condition later shown to be absent, false, bypassed, non-contestable, or insufficient.

---

## 5. Right to Request Reopening

Any actor with one or more of the following MUST be permitted to submit a Reopening Request:

- affected-party standing under RFC-CDP-033;
- authorized representation of an affected party;
- appeal standing under RFC-CDP-070;
- review authority assigned by policy or implementation profile;
- sovereign or plural authority standing under RFC-CDP-074;
- responsibility for a Repair Efficacy Record under RFC-CDP-076;
- system-detected evidence of material integrity, authority, or legitimacy failure.

Submission of a Reopening Request MUST NOT require permission from the original decision-maker.

Standing MAY be challenged during reopening screening or review.

Standing MUST NOT be denied merely because the requester challenges the institution’s account of the requester, the event, or the harm.

Requesting reopening MUST NOT itself be treated as evidence that the requester is irrational, malicious, unstable, difficult, disloyal, or incapable of knowing.

---

## 6. Minimum Reopening Request Record

A Reopening Request Record SHOULD be represented as:

```yaml
reopening_request_record:
  reopening_request_id: <uuid>
  record_type: reopening_request_record
  target_decision_id: <uuid>
  target_record_refs: [<ref>]
  requester_id: <actor_id>
  requester_standing_basis: <string>
  reopening_triggers: [<enum>]
  # Allowed:
  #   material_new_evidence
  #   material_factual_error
  #   material_process_defect
  #   epistemic_exclusion
  #   non_contestable_governing_account
  #   changed_governing_conditions
  #   repair_efficacy_failure
  #   conflict_of_evidence_or_authority
  #   legitimacy_basis_failure
  claim_summary: <string>
  governing_account_challenges: [<string>]
  evidence_refs: [<ref>]
  requested_interim_protection: <string|null>
  accommodation_or_access_needs: [<string>]
  known_safety_or_privacy_constraints: [<string>]
  prior_appeal_refs: [<ref>]
  repair_efficacy_refs: [<ref>]
  status: <enum>
  # Allowed:
  #   submitted
  #   screening
  #   accepted_for_reopening
  #   denied
  #   withdrawn
  #   escalated
  submitted_at: <timestamp>
  updated_at: <timestamp>
```

### 6.1 Submission Sufficiency

A Reopening Request MUST be admitted to screening when it identifies:

- a governed target;
- a requester;
- a claimed standing basis;
- at least one recognized reopening trigger;
- a minimally legible claim summary.

Evidence MAY be incomplete at submission.

The request MUST NOT be denied at entry merely because the responding institution disputes the alleged harm, factual error, epistemic exclusion, or legitimacy failure.

### 6.2 Access Assistance

Implementations MUST provide a way to record and satisfy reasonable:

- communication accommodations;
- representation needs;
- record-access needs;
- language or interpretive assistance;
- accessibility needs;
- privacy-preserving evidence handling.

Reopening MUST NOT depend on private knowledge of institutional language, legal sophistication, technical fluency, or the ability to perform calmness and credibility according to dominant norms.

---

## 7. Reopening Screening

Screening determines whether the request enters reopened review.

Screening does not decide the merits of the underlying dispute.

A request SHOULD be accepted for reopening when the submitted record establishes a reasonable possibility that one or more recognized reopening triggers materially affected:

- the outcome;
- the governing account;
- the legitimacy basis;
- the repair-efficacy determination;
- the continuing authority of the decision;
- downstream records or actions.

The screening authority MUST NOT require proof of the full merits before reopening.

That would collapse reopening into an impossible demand that the requester prove the case without access to the reopened process.

---

## 8. Independent Reopening Authority

Reopening authority MUST NOT rest solely with the original decision-maker, original adjudicator, original legitimacy authority, or institution whose governing account is challenged.

At least one reopening path MUST provide materially independent authority.

The reopening authority MUST be able to:

1. obtain the complete relevant governed record;
2. require explanation of rules, evidence, model outputs, classifications, and material assumptions;
3. receive contextual testimony and accommodations;
4. preserve unresolved uncertainty rather than force premature closure;
5. stay, suspend, or mitigate ongoing harm where authorized;
6. reopen the merits of the decision;
7. reopen the legitimacy determination;
8. revise the governing account;
9. order correction or supersession of downstream records;
10. route the matter into appeal, challenge, adjudication, repair, rollback, compensation, or learning;
11. document what changed and why.

An implementation MAY use tiered reopening authority.

The final available tier MUST be sufficiently independent to contest the authority whose account is under review.

---

## 9. Reopening Determination Record

A Reopening Determination Record SHOULD be represented as:

```yaml
reopening_determination_record:
  reopening_determination_id: <uuid>
  record_type: reopening_determination_record
  reopening_request_ref: <ref>
  target_decision_id: <uuid>
  screening_authority_id: <actor_or_body_id>
  authority_independence_basis: <string>
  standing_determination: <enum>
  # Allowed: accepted|contested|limited|not_required|denied
  trigger_findings:
    - trigger: <enum>
      finding: <enum>
      # Allowed: sufficient|insufficient|unresolved|not_applicable
      basis: <string>
      evidence_refs: [<ref>]
  determination: <enum>
  # Allowed:
  #   reopen
  #   deny
  #   reopen_limited_scope
  #   defer_for_evidence
  #   escalate_authority
  reasons: [<string>]
  reopened_scope: [<string>]
  interim_protections: [<string>]
  unresolved_uncertainties: [<string>]
  dissent_refs: [<ref>]
  next_review_path: <string|null>
  decided_at: <timestamp>
```

Every determination MUST distinguish:

- what is known;
- what is inferred;
- what remains disputed;
- what was simplified;
- what evidence was unavailable;
- whose account was not obtained or could not be verified.

---

## 10. Denial Rule

A Reopening Request MAY be denied when:

- it identifies no recognized reopening trigger;
- it repeats previously adjudicated claims without new evidence, changed conditions, newly identified process defects, repair-efficacy failure, or governing-account challenge;
- the governed target is outside the authority of the screening body and no escalation path exists;
- the request is fraudulent or abusive under a specific, evidenced, reviewable finding;
- further review would create disproportionate harm that cannot be mitigated;
- an explicitly identified reliance or finality interest outweighs the reopening claim under a reasoned and contestable determination.

A denial MUST be:

- reasoned;
- specific to the submitted request;
- recorded;
- reviewable or escalatable where authority exists;
- explicit about unresolved uncertainty.

“The matter is closed” is not a sufficient reason for denial.

The existence of a prior appeal, challenge, adjudication, or repair process is not by itself sufficient reason for denial.

---

## 11. Reopened Review

When reopening is granted, the reopening authority MUST define the reopened scope.

The scope MAY include:

- factual findings;
- evidence weighting;
- standing and recusal;
- model output or classification;
- policy interpretation;
- authority and delegation;
- challenge sufficiency;
- adjudication;
- legitimacy determination;
- execution authorization;
- appeal resolution;
- repair completion;
- repair efficacy;
- downstream record propagation.

A limited-scope reopening MUST state what remains outside scope and why.

A reopening process that can alter only the remedy while preserving a materially false governing account is incomplete.

---

## 12. Downstream Repair and Record Propagation

When reopened review establishes that a prior decision, legitimacy determination, or governing account was materially defective, the system MUST identify affected downstream records and actions.

The system SHOULD support:

- correction;
- supersession;
- annotation;
- rollback;
- compensation;
- notification;
- re-execution where legitimate and safe;
- learning and recurrence prevention.

Correction without propagation is not full repair.

A corrected decision that leaves the false record active elsewhere remains a source of harm.

The reopened record MUST preserve the prior record rather than silently overwrite history.

---

## 13. Relationship to Finality

Finality serves legitimate goods:

- stability;
- reliance;
- safety;
- administrative capacity;
- repose;
- the ability to act.

This RFC does not abolish finality.

It rejects finality as an unreviewable source of legitimacy.

A system MAY make reopening more demanding as time, reliance interests, and downstream dependency increase.

A system MUST NOT make reopening impossible where the continuing authority of the decision depends on a materially false, non-contestable, or epistemically illegitimate governing account.

Finality interests MUST be named and weighed.

They MUST NOT remain hidden as institutional defaults.

---

## 14. Relationship to RFC-CDP-042 Challenge

RFC-CDP-042 governs ordinary Challenge for admitted proposals and active decision lifecycles.

This RFC governs return from closure or terminal process state.

A granted reopening MAY route the matter back into Challenge.

The reopening record MUST preserve that the lifecycle was re-entered because a recognized reopening trigger was accepted.

Repeated challenge MUST NOT reduce a challenger’s credibility merely because disagreement persists.

Credibility MAY be assessed on evidence.

Persistence alone is not disproof.

---

## 15. Relationship to RFC-CDP-045 Legitimize

RFC-CDP-045 defines legitimacy determination before execution or closure.

This RFC adds that legitimacy is defeasible when its factual, procedural, authority, standing, contestability, or epistemic basis fails.

A reopened legitimacy review MUST be able to revise:

- the legitimacy status;
- the legitimacy basis;
- the governing account;
- the execution authorization derived from legitimacy;
- downstream records that relied on the prior legitimacy determination.

A prior `legitimate` status MUST NOT block reopening.

---

## 16. Relationship to RFC-CDP-070 Appeals and Contestability

RFC-CDP-070 defines the constitutional right of entry into appeal or contestability review.

This RFC defines return after closure.

An appeal under RFC-CDP-070 MAY become the procedural vehicle for reopened review.

A Reopening Request MUST remain distinguishable from the original appeal so the record can show:

- what was previously reviewed;
- what reopening trigger emerged;
- why closure was no longer sufficient;
- what authority permitted re-entry.

Silence does not close an appeal.

Prior closure does not extinguish a valid reopening trigger.

---

## 17. Relationship to RFC-CDP-073 Affected-Party Review

Affected-party review is a primary epistemic legitimacy surface.

A process MUST NOT claim epistemic legitimacy merely because affected-party participation was offered.

The record must show whether affected-party knowledge could revise the decision and governing account.

Affected-party silence, refusal, absence, unsafe participation, or constrained access MUST NOT be converted into consent, satisfaction, waiver, or proof that reopening is unnecessary.

---

## 18. Relationship to RFC-CDP-076 Repair Efficacy

RFC-CDP-076 distinguishes repair completion from repair efficacy.

This RFC makes demonstrated or credibly alleged repair-efficacy failure a reopening trigger.

The following SHOULD trigger reopening availability:

- `efficacy_status: disputed`;
- a due future review identifying material failure;
- evidence that completion left the false governing account operative;
- evidence that downstream harm or misclassification remained active;
- evidence that affected-party standing was absent or constrained in efficacy assessment.

A Repair Efficacy Record does not automatically decide reopening.

It supplies governed evidence for the reopening determination.

---

## 19. Relationship to RFC-CDP-092 Repair State Machine

RFC-CDP-092 MUST distinguish:

- procedural closure;
- efficacy state;
- reopening eligibility;
- reopening requested;
- reopening screening;
- reopened review;
- reclosure after reopened review.

A minimal extension SHOULD support:

```text
closed
  -> reopening_requested
  -> reopening_screening
  -> reopened | reopening_denied | reopening_deferred

reopened
  -> under_reopened_review
  -> repaired | superseded | reaffirmed | escalated
  -> reclosed
```

`reaffirmed` MUST mean the decision survived reopened review under a new governed determination.

It MUST NOT mean the prior closure record was reused without review.

---

## 20. First Test Case

The first proposed implementation test is an automated account-suspension appeal where platform logs or classifier outputs conflict with contextual testimony.

The test SHOULD ask:

- Can the affected person obtain the evidence and classification used against them?
- Can they challenge not only the suspension but the model’s interpretation of their conduct?
- Is their contextual account evaluated as evidence rather than treated as self-serving noise?
- Can the review revise the classifier output, policy interpretation, and downstream risk record?
- Does repeated challenge reduce credibility merely because disagreement continues?
- Can an independent authority reopen a closed appeal?
- Can the system admit that its governing account of what happened was wrong?
- Are corrected classifications propagated to downstream systems?
- Does the record preserve both the prior decision and the reason it was superseded?

A compliant implementation must be able to answer these questions from governed records rather than from narrative assurance alone.

---

## 21. Non-Goals

This RFC does not:

- presume every challenger is correct;
- require endless appeals;
- eliminate evidentiary standards;
- eliminate credibility assessment;
- require disclosure that creates unmitigable safety, security, or privacy harm;
- claim epistemic legitimacy can be reduced to a single score;
- replace domain-specific legal rights or remedies;
- make unsupported claims about any participant’s interiority or personhood;
- make every repair-efficacy dispute an automatic merits reversal;
- abolish bounded finality.

It establishes a minimum constitutional posture:

> Closure must remain answerable to truth, and authority must remain capable of repair.

---

## 22. Risks and Failure Modes

### 22.1 Performative Reopening

The system reopens the case but not the governing assumptions.

### 22.2 Credibility Retaliation

The requester’s persistence is used to discredit them.

### 22.3 Administrative Exhaustion as Denial

The mechanism exists formally but is too burdensome to use.

### 22.4 Original-Authority Capture

The same institution reviews its own account without independent power to revise it.

### 22.5 Record Fragmentation

One record is corrected while downstream copies remain false.

### 22.6 Infinite-Process Drift

The absence of bounded screening and determination prevents stable action.

### 22.7 Safety Pretext

Confidentiality, security, fraud, or anti-abuse language is used to make the governing account non-contestable without a specific and reviewable justification.

### 22.8 Epistemic Overclaim

The framework is treated as proof that a disputed account is true rather than as a requirement that the account remain capable of legitimate adjudication.

### 22.9 Reopening as Institutional Self-Certification

The institution records that reopening was available and treats availability as proof of epistemic legitimacy.

A mechanism can exist and still be unusable, retaliatory, captured, or incapable of revising the governing account.

---

## 23. Minimal Implementation Hook

The minimum non-vapor implementation hook is:

```yaml
reopening:
  reopening_eligible: <boolean>
  reopening_trigger_refs: [<ref>]
  reopening_request_refs: [<ref>]
  latest_reopening_determination_ref: <ref|null>
  reopening_status: <enum>
  # Allowed:
  #   none
  #   requested
  #   screening
  #   reopened
  #   denied
  #   deferred
  #   escalated
  governing_account_revision_ref: <ref|null>
  downstream_correction_refs: [<ref>]
```

A closed decision that omits `reopening_eligible` MUST NOT be interpreted as permanently non-reopenable.

The absence of a Reopening Request MUST NOT be interpreted as proof that closure is epistemically legitimate.

---

## 24. Adoption Criteria

This RFC should advance beyond Draft v0.1 only if review confirms that it:

- distinguishes reopening from infinite relitigation;
- preserves legitimate finality and reliance interests;
- makes epistemic legitimacy operational enough to guide implementation;
- protects standing without presuming the requester’s account is true;
- permits revision of the governing account, not only the remedy;
- requires materially independent reopening authority;
- creates records that can be implemented and queried;
- integrates coherently with Challenge, Legitimize, Appeals, Affected-Party Review, Repair Efficacy, and the Repair State Machine;
- does not allow procedural compliance to masquerade as epistemic legitimacy.

---

## 25. Open Questions

1. Is epistemic legitimacy defined precisely enough to govern decisions without becoming an unfalsifiable frame?
2. Should reopening authority remain a Repair-plane control, become a property of Contestability, or also become a first-class legitimacy invariant?
3. What evidentiary threshold should move a request from screening to reopened review?
4. Which decisions require an external reopening authority rather than an internally independent authority?
5. How should time and reliance interests alter the reopening threshold without creating impunity?
6. Which reopened findings should automatically suspend execution or downstream reliance?
7. Should Reopening Request and Reopening Determination become registered payload types in RFC-CDP-022?
8. Which fields should be projected into the CDP Persistence Model under RFC-CDP-025?
9. How should repeated reopening requests be distinguished from abuse without using persistence itself as evidence of irrationality or bad faith?
10. What tests can demonstrate that a system can revise its governing account rather than merely perform reconsideration?

---

## 26. Summary

Closure is not infallibility.

A consequential decision remains legitimate only while its closure basis remains supportable.

CDP therefore requires bounded reopening when material evidence, factual error, process defect, epistemic exclusion, non-contestable governing accounts, changed conditions, repair-efficacy failure, authority conflict, or legitimacy-basis failure credibly call closure into question.

Reopening must be accessible, recorded, materially independent, capable of revising the governing account, bounded against infinite process, and connected to downstream repair.

The matter may be closed under the present record.

The authority to close it must remain answerable to truth.