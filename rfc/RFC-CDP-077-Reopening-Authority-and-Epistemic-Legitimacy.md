# RFC-CDP-077 — Reopening Authority and Epistemic Legitimacy

Author: Kevin “Andie” Williams  
Status: Draft v0.2  
Series: Constitutional Decision Plane (CDP)  
Date: July 14, 2026  
Updates: RFC-CDP-045, RFC-CDP-070, RFC-CDP-073, RFC-CDP-076, RFC-CDP-092  
Depends On: RFC-CDP-001, RFC-CDP-002, RFC-CDP-023, RFC-CDP-033, RFC-CDP-042, RFC-CDP-044, RFC-CDP-045, RFC-CDP-070, RFC-CDP-073, RFC-CDP-074, RFC-CDP-076

## Abstract

This RFC defines **Reopening Authority and Epistemic Legitimacy** for the CDP Repair plane.

A consequential decision does not become permanently legitimate merely because the decision lifecycle, appeal process, legitimacy determination, or repair process reached procedural closure.

A closed decision MUST remain eligible for bounded reopening when material evidence, factual error, process defect, epistemic exclusion, a non-contestable governing account, changed governing conditions, repair-efficacy failure, recurring harm, sovereignty claims, unresolved authority conflict, or a failed legitimacy basis credibly call closure into question.

This RFC defines:

- the canonical reopening-trigger registry;
- Reopening Request and Reopening Determination records;
- operational independence modes;
- a truthful fallback when material independence is unavailable;
- screening and denial rules;
- bounded closure;
- legitimacy revision without destruction of the original record;
- downstream correction propagation;
- integration with Appeals, Affected-Party Review, Repair Efficacy, Legitimize, and the Repair State Machine.

The purpose is not endless relitigation.

The purpose is to prevent procedural finality from laundering epistemic failure into durable authority.

Draft v0.2 incorporates the blocking challenge findings recorded in Session 019.

---

## 1. Failure Mode

The primary failure mode is **closure laundering epistemic illegitimacy**.

A CDP-governed process may be formally complete while remaining epistemically defective:

- an appeal existed, but the appellant was treated as presumptively confused, unstable, biased, nontechnical, adversarial, or incapable of interpreting their own experience;
- testimony entered the record but could not revise the institution’s governing account;
- a challenge could dispute the outcome but not the classification, policy interpretation, model output, credibility rule, authority claim, or factual narrative that produced it;
- a repair process completed, but repair efficacy remained disputed or unassessed;
- authoritative records, systems, reviewers, affected parties, institutions, communities, or sovereign authorities materially disagreed and the disagreement was resolved by hierarchy rather than adjudication;
- repeated contestation was treated as evidence that the challenger lacked credibility;
- a reopening authority was described as independent while remaining inside the same unexamined power relationship;
- “the matter is closed” was used as the reason closure could not be examined.

A formally contestable process can still be epistemically illegitimate.

CDP MUST prevent closure from becoming an unreviewable source of legitimacy.

---

## 2. Core Principle

> A consequential decision does not earn legitimacy merely because it can be challenged. The challenge process must preserve the challenger’s standing as a knower and permit evidence to revise both the decision and the governing account by which the decision is justified.

A decision remains legitimate only while its legitimacy and closure bases remain supportable.

Where closure depends on silencing, pathologizing, discrediting, or structurally excluding relevant knowledge, reopening is not a courtesy.

It is a repair obligation.

This principle protects standing as a knower.

It does not presume that the challenger’s account is true.

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

**Epistemic Legitimacy** is the property of a decision process that preserves a real, governed, and reviewable possibility that relevant participants can contribute knowledge capable of revising:

- the outcome;
- the factual record;
- the evidentiary interpretation;
- the classification or model output;
- the policy or rule application;
- the credibility determination;
- the governing account;
- the legitimacy determination;
- downstream records and actions.

Permission to object is necessary but not sufficient.

Objection must remain capable of mattering.

Epistemic legitimacy MUST NOT be inferred solely from the presence of required fields, a completed appeal, or a recorded determination.

Implementations SHOULD audit epistemic legitimacy across cases by testing whether materially similar evidence receives materially different treatment depending on identity, disability, communication style, affect, institutional status, or relationship to authority.

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

> closed under the present governed record, while remaining reopenable upon recognized evidence of material error, epistemic exclusion, changed governing conditions, unresolved authority conflict, sovereignty claim, recurring harm, or failed repair.

Bounded closure preserves stability without claiming infallibility.

### 3.5 Material Independence

**Material Independence** exists when the reopening authority is sufficiently separated from the challenged authority that the challenged actor or institution cannot solely determine the scope, evidence, findings, outcome, or record of reopening review.

Material independence concerns power, not branding.

A different reviewer inside the same unexamined reporting chain is not automatically independent.

---

## 4. Canonical Reopening-Trigger Registry

This section is the canonical reopening-trigger registry for CDP.

RFC-CDP-092 and implementation profiles MUST consume this registry rather than maintain an overlapping independent trigger list.

Where RFC-CDP-092 §11 or another earlier RFC contains a conflicting or incomplete reopening list, this RFC controls for reopening eligibility and trigger naming.

Allowed trigger values are:

```text
material_new_evidence
material_factual_error
material_process_defect
epistemic_exclusion
non_contestable_governing_account
changed_governing_conditions
repair_efficacy_failure
conflict_of_evidence_or_authority
legitimacy_basis_failure
sovereignty_claim_material
recurring_harm_pattern
```

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

### 4.7 Repair-Efficacy Failure

A Repair Efficacy Record under RFC-CDP-076 shows or credibly alleges that:

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

### 4.10 Material Sovereignty Claim

A sovereignty, jurisdiction, treaty, land, resource, peoplehood, rematriation, or plural-authority claim materially affects the decision’s authority or legitimacy and was absent, denied, flattened, or left unresolved.

### 4.11 Recurring Harm Pattern

Evidence shows that substantially similar harm recurred after closure, repair, compensation, policy correction, or implementation change, calling the original governing account or repair efficacy into question.

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

Submission MUST NOT require permission from the original decision-maker.

Standing MAY be challenged during screening or reopened review.

Standing MUST NOT be denied merely because the requester challenges the institution’s account of the requester, event, decision, or harm.

Requesting reopening MUST NOT itself be treated as evidence that the requester is irrational, malicious, unstable, difficult, disloyal, or incapable of knowing.

---

## 6. Reopening Request Record

A Reopening Request Record SHOULD be represented as:

```yaml
reopening_request_record:
  reopening_request_id: <uuid>
  record_type: reopening_request_record
  target_decision_id: <uuid>
  target_record_refs: [<ref>]
  requester_id: <actor_id>
  requester_standing_basis: <string>
  reopening_triggers: [<canonical_trigger_enum>]
  claim_summary: <string>
  governing_account_challenges: [<string>]
  evidence_refs: [<ref>]
  requested_interim_protection: <string|null>
  accommodation_or_access_needs: [<string>]
  known_safety_or_privacy_constraints: [<string>]
  prior_appeal_refs: [<ref>]
  repair_efficacy_refs: [<ref>]
  status: <submitted|screening|accepted_for_reopening|denied|withdrawn|escalated>
  submitted_at: <timestamp>
  updated_at: <timestamp>
```

A request MUST be admitted to screening when it identifies:

- a governed target;
- a requester;
- a claimed standing basis;
- at least one canonical reopening trigger;
- a minimally legible claim summary.

Evidence MAY be incomplete at submission.

The request MUST NOT be denied at entry merely because the responding institution disputes the alleged harm, factual error, epistemic exclusion, sovereignty claim, recurring harm, or legitimacy failure.

Implementations MUST provide a way to record and satisfy reasonable communication, representation, record-access, language, accessibility, and privacy-preserving evidence needs.

Reopening MUST NOT depend on legal sophistication, technical fluency, institutional vocabulary, or performance of calmness and credibility according to dominant norms.

---

## 7. Screening Standard

Screening determines whether the request enters reopened review.

Screening does not decide the merits.

A request SHOULD be accepted when the submitted record establishes a **reasonable possibility of material effect** on one or more of:

- the outcome;
- the governing account;
- the legitimacy basis;
- the repair-efficacy determination;
- the continuing authority of the decision;
- downstream records or actions.

The screening authority MUST NOT require proof of the full merits before reopening.

The screening record MUST identify which evidence would be needed to resolve any deferred or unresolved trigger finding.

Implementation profiles MAY define risk-tiered evidentiary thresholds, but MUST NOT make the threshold so high that evidence inaccessible without reopening is required to obtain reopening.

---

## 8. Independence Model

### 8.1 Independence Modes

A Reopening Determination MUST classify the authority mode using one of these controlled values:

```text
independent_external
independent_internal_separate_reporting_line
independent_cross_authority
non_independent_with_safeguards
```

#### `independent_external`

The authority is outside the challenged institution or organizational control structure and has no material reporting, financial, supervisory, or decisional dependence on the original authority.

#### `independent_internal_separate_reporting_line`

The authority is inside the same institution but operates under a separate reporting line, conflict policy, decisional mandate, and record authority that prevent the challenged authority from controlling the review.

#### `independent_cross_authority`

The authority derives from a distinct jurisdictional, sovereign, community, regulatory, contractual, or constitutional authority capable of contesting the original authority.

#### `non_independent_with_safeguards`

True material independence is unavailable.

This value tells the truth. It MUST NOT be represented as a weaker form of independence.

### 8.2 Minimum Independence Test

An authority qualifies as materially independent only when all applicable statements are true:

- the challenged authority cannot select or remove the reviewer solely for the case outcome;
- the challenged authority cannot unilaterally restrict the evidence considered;
- the challenged authority cannot silently rewrite or suppress findings;
- the reviewer can record disagreement and unresolved uncertainty;
- the reviewer can issue or escalate a determination adverse to the original authority;
- material conflicts of interest are disclosed;
- the authority basis is reviewable.

A different individual in the same chain of command does not satisfy this test by itself.

### 8.3 Non-Independent Fallback

`non_independent_with_safeguards` MAY be used only when the record states why material independence is unavailable and includes:

- explicit non-independence disclosure;
- conflict-of-interest record;
- preserved dissent;
- full audit exposure;
- an identified escalation or external-review path when one exists;
- prohibition on claiming that the result satisfies a requirement for independent review;
- heightened Learn-stage review.

Where law, constitution, policy, contract, or risk tier requires independent authority, `non_independent_with_safeguards` is non-satisfying and MUST escalate rather than close the requirement.

### 8.4 Relationship to Affected-Party Review

RFC-CDP-073’s rule that an institution MUST NOT be the sole judge of its own closure is implemented through this independence model.

Affected-party participation is necessary where required, but affected-party participation alone does not convert institutional self-review into independent review.

---

## 9. Reopening Determination Record

```yaml
reopening_determination_record:
  reopening_determination_id: <uuid>
  record_type: reopening_determination_record
  reopening_request_ref: <ref>
  target_decision_id: <uuid>
  screening_authority_id: <actor_or_body_id>
  authority_mode: <independent_external|independent_internal_separate_reporting_line|independent_cross_authority|non_independent_with_safeguards>
  authority_basis_ref: <ref>
  conflict_of_interest_refs: [<ref>]
  safeguard_refs: [<ref>]
  standing_determination: <accepted|contested|limited|not_required|denied>
  trigger_findings:
    - trigger: <canonical_trigger_enum>
      finding: <sufficient|insufficient|unresolved|not_applicable>
      basis: <string>
      evidence_refs: [<ref>]
  determination: <reopen|deny|reopen_limited_scope|defer_for_evidence|escalate_authority>
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

The old free-text-only field `authority_independence_basis` is replaced by controlled `authority_mode` plus governed references.

---

## 10. Denial Rule

A Reopening Request MAY be denied when:

- it identifies no canonical reopening trigger;
- it repeats previously adjudicated claims without new evidence, changed conditions, newly identified defects, repair-efficacy failure, sovereignty claim, recurring harm, or governing-account challenge;
- the governed target is outside the authority of the screening body and no escalation path exists;
- the request is fraudulent or abusive under a specific, evidenced, reviewable finding;
- further review would create disproportionate harm that cannot be mitigated;
- an explicitly identified reliance or finality interest outweighs the reopening claim under a reasoned and contestable determination.

A denial MUST be reasoned, specific, recorded, reviewable or escalatable where authority exists, and explicit about unresolved uncertainty.

“The matter is closed” is not a sufficient reason.

The existence of a prior appeal, challenge, adjudication, or repair process is not by itself sufficient reason.

---

## 11. Reopened Review

When reopening is granted, the authority MUST define the reopened scope.

The scope MAY include:

- factual findings;
- evidentiary interpretation;
- credibility determinations;
- classification or model output;
- policy or rule application;
- standing or authority;
- adjudication;
- legitimacy;
- remedy;
- repair efficacy;
- sovereignty or jurisdiction;
- downstream records and actions.

A reopened review MUST be able to revise the governing account, not merely provide a new remedy while preserving a materially false account.

The review MUST preserve dissent, uncertainty, unavailable evidence, and scope limitations.

---

## 12. Legitimacy Is Defeasible

RFC-CDP-045 is updated by this section.

A prior legitimacy record remains an immutable historical record of the determination made at that time.

It MUST NOT be overwritten to conceal that legitimacy was once granted.

Reopening affects legitimacy through a separate **Legitimacy Revision Record**.

```yaml
legitimacy_revision_record:
  legitimacy_revision_id: <uuid>
  record_type: legitimacy_revision_record
  decision_id: <uuid>
  original_legitimacy_record_ref: <ref>
  reopening_determination_ref: <ref>
  revision_status: <affirmed|suspended|revoked|superseded|reopened|unresolved>
  revision_basis: <string>
  evidence_refs: [<ref>]
  authority_ref: <ref>
  effective_at: <timestamp>
  superseding_legitimacy_record_ref: <ref|null>
  dissent_refs: [<ref>]
  lineage_refs: [<ref>]
```

The current effective legitimacy state MUST be derived from:

1. the original legitimacy record;
2. all valid Legitimacy Revision Records in lineage order;
3. any superseding legitimacy record.

A decision with `revision_status: suspended`, `revoked`, `reopened`, or `unresolved` MUST NOT be treated as presently executable solely because the original legitimacy record says `granted`.

`superseded` means a later legitimacy record now governs.

`affirmed` means reopened review found the existing legitimacy basis remains supportable.

This structure preserves audit history while making legitimacy writable and defeasible.

---

## 13. Relationship to Finality

Finality serves real goods:

- stability;
- reliance;
- safety;
- administrative capacity;
- repose;
- ability to act.

This RFC does not abolish finality.

It rejects finality as an unreviewable source of legitimacy.

A system MAY make reopening harder as time, reliance, irreversibility, and third-party dependence increase.

Any increased threshold MUST be explicit, risk-tiered where appropriate, reasoned, and contestable.

No reliance interest makes a materially false governing account true.

Where reopening cannot unwind all consequences, the system MUST still preserve correction, supersession, compensation, disclosure, learning, or other available repair.

---

## 14. Downstream Correction and Propagation

When reopened review establishes material defect, the system MUST identify downstream effects.

Potential actions include:

- correct;
- supersede;
- annotate;
- revoke;
- suspend;
- compensate;
- rollback;
- notify dependent systems;
- preserve historical lineage;
- create a learning record.

Correction without propagation is incomplete repair.

A repaired source record that leaves false downstream copies active remains a source of harm.

---

## 15. Repair-State-Machine Integration

RFC-CDP-092 is updated by this section.

The Repair State Machine MUST use the canonical trigger registry in Section 4.

A reopening transition MUST reference a Reopening Request Record and, once screened, a Reopening Determination Record.

Recommended transition semantics:

```text
closed -> reopening_requested
reopening_requested -> reopening_screening
reopening_screening -> reopened
reopening_screening -> reopening_denied
reopening_screening -> reopening_deferred
reopening_screening -> reopening_escalated
reopened -> under_review
under_review -> reclosed
under_review -> repair_active
under_review -> legitimacy_revised
```

Earlier RFC-CDP-092 reopening conditions remain informative only to the extent they map to the canonical Section 4 trigger values.

`sovereignty_claim_material` and `recurring_harm_pattern` are explicitly retained.

---

## 16. Decision-Lifecycle-Envelope Integration

RFC-CDP-023 implementations SHOULD expose:

```yaml
repair_control:
  reopening_eligible: <boolean>
  reopening_request_refs: [<ref>]
  reopening_determination_refs: [<ref>]
  legitimacy_revision_refs: [<ref>]
  current_effective_legitimacy_status: <string|null>
```

`reopening_eligible: false` MUST NOT be inferred solely from procedural closure.

The basis for ineligibility MUST be governed and reviewable.

---

## 17. Non-Goals

This RFC does not:

- presume every challenger is correct;
- require endless appeals;
- abolish evidentiary standards;
- abolish credibility assessment;
- require unsafe disclosure;
- reduce epistemic legitimacy to a single score;
- claim that completed fields prove legitimacy;
- erase original legitimacy records;
- make unsupported claims about interiority or personhood;
- replace domain-specific legal rights or remedies.

It establishes a minimum governance posture:

> closure must remain answerable to truth, and authority must remain capable of repair.

---

## 18. Failure Modes and Audit Tests

### 18.1 Performative Reopening

The system reopens the case but not the governing assumptions.

### 18.2 Credibility Retaliation

Persistence or disagreement is used to discredit the requester.

### 18.3 Administrative Exhaustion

The mechanism exists formally but is too burdensome to use.

### 18.4 Original-Authority Capture

A nominally different reviewer preserves the same power relationship.

Audit test: does `authority_mode` match the actual reporting, removal, evidence, publication, and escalation powers?

### 18.5 Record Fragmentation

One record is corrected while downstream copies remain false.

### 18.6 Infinite-Process Drift

No bounded termination permits stable action.

### 18.7 Safety Pretext

Confidentiality, security, or anti-abuse language makes the governing account non-contestable without specific reviewable justification.

### 18.8 Epistemic Overclaim

Protecting standing is treated as proof the disputed account is true.

### 18.9 Adjudication Theater

All required fields are present, but evidence cannot revise the outcome, governing account, authority claim, or downstream record.

### 18.10 False Independence

A free-text assertion or organizational label is treated as proof of independence.

This failure is non-compliant with Draft v0.2.

---

## 19. Minimal Implementation Hook

A minimum compliant implementation exposes:

```yaml
reopening:
  trigger_registry_version: RFC-CDP-077-v0.2
  request_ref: <ref>
  determination_ref: <ref|null>
  authority_mode: <controlled_enum|null>
  current_status: <submitted|screening|reopened|denied|deferred|escalated|closed>
  legitimacy_revision_ref: <ref|null>
  downstream_correction_refs: [<ref>]
```

Schema presence alone does not establish epistemic legitimacy.

---

## 20. Adoption Criteria

This RFC should advance beyond Draft v0.2 only if review confirms that it:

- distinguishes reopening from infinite relitigation;
- preserves legitimate finality interests;
- defines material independence operationally;
- tells the truth when independence is unavailable;
- provides a controlled and queryable authority mode;
- owns one canonical reopening-trigger registry;
- preserves sovereignty and recurring-harm triggers;
- protects challengers without presuming correctness;
- permits revision of the governing account;
- makes legitimacy defeasible without erasing history;
- provides downstream correction propagation;
- remains compatible with anti-premature certainty, standing, contestability, affected-party review, repair efficacy, and repair-state-machine commitments.

---

## 21. Session 019 Disposition

Session 019 challenged Draft v0.1 and required four blocking repairs:

1. define material independence operationally;
2. reconcile reopening triggers with RFC-CDP-092;
3. make defeasible legitimacy writable;
4. repair RFC-series discoverability for RFC-CDP-076 and RFC-CDP-077.

Draft v0.2 implements the first three within this RFC.

The canonical Series Index still requires its safe v1.4 map update as a separate corpus-maintenance change.

The RFC remains **Draft v0.2 pending C’s verification of the repaired blocker set and Andie’s final adjudication**.
