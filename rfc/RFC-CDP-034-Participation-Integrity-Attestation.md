# RFC-CDP-034 — Participation Integrity Attestation

Author: Kevin “Andie” Williams  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: July 16, 2026  
Updates: RFC-CDP-020, RFC-CDP-033, RFC-CDP-043, RFC-CDP-044, RFC-CDP-045, RFC-CDP-047, RFC-CDP-048, RFC-CDP-070, RFC-CDP-073  
Depends On: RFC-CDP-020, RFC-CDP-031, RFC-CDP-032, RFC-CDP-033, RFC-CDP-043, RFC-CDP-044, RFC-CDP-045, RFC-CDP-047, RFC-CDP-048, RFC-CDP-070, RFC-CDP-073, RFC-CDP-074  
Related: `docs/constantc-cdp-standing-epistemic-safety-bridge.md`

---

## Abstract

RFC-CDP-033 defines whether an actor has valid Standing to participate in a specific stage of a specific decision.

This RFC defines **Participation Integrity** as the governed condition in which that valid Standing remains intact through entry, representation, evaluation, revision, review, and repair.

It establishes a first-class **Participation Integrity Attestation** artifact.

Operational Reachability is one required dimension of Participation Integrity. It is not the entire property.

This RFC does not redefine Standing, collapse Standing into Authority, create a new lifecycle stage, duplicate Appeals or Anti-Erasure, or reimplement Sovereignty governance.

The governing question is:

> **Did the decision process preserve the integrity of this participant’s valid Standing from entry through representation, evaluation, revision, review, and repair?**

---

## 1. Failure mode

A governance process may allocate Standing correctly while corrupting participation in operation.

Examples include:

- an affected party has Standing, but the contribution channel is inaccessible or untimely;
- testimony enters the record but is inaccurately summarized, decontextualized, or misclassified;
- a participant is formally heard while their contribution is predefined as incapable of revising the controlling account;
- disability, distress, language, fluency, hierarchy, institutional status, or communication style produces an irrelevant credibility discount;
- a reviewer may reconsider the immediate outcome but not the credibility judgment that controlled it;
- a successful challenge changes the immediate decision while leaving downstream records, labels, scores, or model inputs unrepaired;
- participation is invited ceremonially while the authority, jurisdiction, or sovereignty of the participant is downgraded;
- delay or procedural burden produces systematic abandonment before meaningful review.

These failures are not necessarily failures of Standing allocation.

They are failures of Participation Integrity.

---

## 2. Relationship to existing CDP concepts

### 2.1 Standing

RFC-CDP-033 remains authoritative for:

- whether Standing exists;
- Standing type;
- stage;
- actor and role;
- basis;
- recusal;
- contestability;
- constitutional protection;
- persistence.

Participation Integrity does not create a parallel Standing object.

Standing allocates participation.

Participation Integrity tests whether that participation remained constitutionally and operationally real.

### 2.2 Authority

Participation Integrity does not expand an actor’s Authority.

A participant may have a contribution received, evaluated, answered, and reviewed without acquiring authority to adjudicate, legitimize, delegate, or execute.

### 2.3 Contestability

RFC-CDP-070 provides constitutional entry into appeal and contestability review.

Participation Integrity evaluates whether the mechanisms offered to actors with Standing were accessible, non-ceremonial, reviewable, and capable of producing revision or repair when warranted.

### 2.4 Anti-Erasure

RFC-CDP-073 governs affected-party review and anti-erasure.

Participation Integrity makes explicit a related failure:

> A participant may remain formally present while their contribution, authority context, dissent, or correction is structurally incapable of influencing the evolving account.

### 2.5 Sovereignty

This RFC MUST NOT classify a Sovereignty Claim as an ordinary participation-integrity or Standing issue.

When a Sovereignty Claim or Authority Conflict is present, implementations MUST defer to RFC-CDP-032 and RFC-CDP-074 before applying ordinary participation analysis.

A sovereign authority MUST NOT be reduced to an ordinary stakeholder, evidence source, consultation participant, sentiment signal, or weighted preference.

---

## 3. Definition

**Participation Integrity** is the governed condition in which an actor’s valid Standing is preserved through a process that is:

1. correctly allocated;
2. accessible and timely;
3. accurately represented;
4. evaluated under accountable standards;
5. capable of revision when materially sufficient;
6. reviewable when limited, discounted, or rejected;
7. repairable in both outcome and record;
8. empirically reachable for materially similar participants.

Participation Integrity does not require that a contribution prevail.

It requires that participation be real rather than ceremonial.

---

## 4. Required dimensions

### 4.1 Allocation integrity

- Was Standing validly recognized under RFC-CDP-033?
- Was the stage, role, contribution domain, and accountability relationship correctly scoped?
- Were conflicts and recusal requirements recorded?

### 4.2 Entry integrity

- Was the participation path accessible, timely, discoverable, and usable?
- Were needed accommodations or authorized representation available?
- Did procedural burden, delay, retaliation risk, or access loss defeat entry?

### 4.3 Representation integrity

- Was the contribution preserved accurately?
- Were material context, uncertainty, qualifications, restrictions, and dissent retained?
- Was the participant able to correct a materially inaccurate representation?

### 4.4 Evaluation integrity

- Were relevance, evidence quality, and credibility treated as distinct questions?
- Were standards documented and applied consistently?
- Were credibility discounts tied to decision-relevant evidence rather than identity, disability, distress, fluency, hierarchy, or source status?

### 4.5 Revision integrity

- Was at least one materially plausible revision condition defined?
- Could sufficient contribution alter the account, decision, credibility judgment, classification, or record?
- Was the account actually changed when the governing standard was met?

### 4.6 Review integrity

- Could rejection, discount, limitation, or misrepresentation be challenged?
- Was review performed by a differently situated or independently authorized actor where required?
- Were reasons and unresolved uncertainty preserved?

### 4.7 Repair integrity

- Did successful challenge repair the immediate decision?
- Did it repair downstream records, labels, scores, model inputs, and future-use artifacts?
- Was failure to repair recorded as an unresolved breach or repair obligation?

### 4.8 Operational reachability

- Could materially similar participants actually use the path?
- Do reversal, abandonment, delay, accessibility, and credibility-pattern data support the claimed integrity?
- Does counterfactual testing show patterned irrelevant discount?

### 4.9 Sovereignty and authority integrity

- Was a Sovereignty Claim or Authority Conflict detected?
- If detected, did the process defer to RFC-CDP-032 and RFC-CDP-074?
- Was authority preserved rather than downgraded into stakeholder participation?

---

## 5. Standing record integration

The RFC-CDP-033 `standing_record` is extended by reference, not replacement.

```yaml
standing_record:
  # Existing RFC-CDP-033 fields remain authoritative.
  contribution_domains:
    - <string>
  entry_path_refs:
    - <artifact_ref>
  revision_conditions:
    - <string>
  rejecting_authority_ref: <actor_or_authority_ref|null>
  review_path_ref: <artifact_ref|null>
  participation_integrity_attestation_ref: <artifact_ref|null>
```

These fields are normative extension fields under this RFC.

The canonical Decision object SHOULD link to Standing and Participation Integrity artifacts rather than embedding mutable duplicate copies.

---

## 6. Participation Integrity Attestation schema

```yaml
participation_integrity_attestation:
  attestation_id: <uuid>
  decision_id: <uuid>
  standing_id: <uuid>
  actor_id: <uuid>
  stage: <propose|challenge|test|adjudicate|legitimize|execute|record|learn|repair>

  allocation_integrity:
    standing_valid: <true|false|unknown>
    standing_type: <constitutional|delegated|emergency|repair|appeal|functional|other>
    contribution_domains:
      - <string>
    recusal_status: <not_required|required|partial|full|unresolved>
    standing_record_ref: <artifact_ref>

  entry_integrity:
    paths_offered:
      - <artifact_ref|string>
    accessible: <true|false|unknown>
    timely: <true|false|unknown>
    accommodation_refs:
      - <artifact_ref>
    abandonment_or_delay_signal: <true|false|unknown>

  representation_integrity:
    contribution_record_refs:
      - <artifact_ref>
    participant_confirmed_accuracy: <true|false|not_requested|unknown>
    material_context_omitted: <true|false|unknown>
    dissent_preserved: <true|false|not_applicable|unknown>
    correction_path_available: <true|false|unknown>

  evaluation_integrity:
    relevance_determination: <relevant|partially_relevant|not_relevant|unresolved>
    evidence_quality_basis_ref: <artifact_ref|null>
    credibility_discount_applied: <true|false|unknown>
    credibility_discount_basis_ref: <artifact_ref|null>
    credibility_discount_reviewable: <true|false|unknown>
    patterned_irrelevant_discount_detected: <true|false|unknown>

  revision_integrity:
    revision_conditions:
      - <string>
    materially_plausible_revision_path: <true|false|unknown>
    contribution_changed_account: <true|false|not_applicable|unknown>
    account_change_ref: <artifact_ref|null>
    rejection_reason_ref: <artifact_ref|null>

  review_integrity:
    review_path_available: <true|false|unknown>
    review_path_ref: <artifact_ref|null>
    differently_situated_reviewer: <true|false|unknown>
    reasons_preserved: <true|false|unknown>

  repair_integrity:
    immediate_outcome_repaired: <true|false|not_applicable|unknown>
    downstream_record_repair_status: <not_required|pending|partial|complete|failed|unknown>
    repair_refs:
      - <artifact_ref>

  operational_reachability:
    result: <reachable|partially_reachable|unreachable|unknown>
    audit_sample_ref: <artifact_ref|null>
    materially_similar_case_comparison_ref: <artifact_ref|null>
    reversal_pattern_ref: <artifact_ref|null>
    accessibility_effectiveness_ref: <artifact_ref|null>

  sovereignty_integrity:
    sovereignty_claim_present: <true|false|unknown>
    sovereignty_claim_ref: <artifact_ref|null>
    authority_conflict_ref: <artifact_ref|null>
    deferred_to_rfc_074: <true|false|not_applicable|unknown>
    authority_downgrade_detected: <true|false|unknown>

  result: <intact|partially_intact|compromised|failed|insufficient_evidence|not_applicable>
  blocking_failures:
    - <string>
  unresolved_uncertainty:
    - <string>
  exception_ref: <artifact_ref|null>
  attested_by: <actor_id>
  attested_at: <timestamp>
```

The attestation MUST distinguish absence of evidence from evidence of integrity.

`unknown` and `insufficient_evidence` MUST NOT be silently converted to `intact`.

---

## 7. Lifecycle integration

No new lifecycle stage is created.

### 7.1 Propose

A proposal MUST identify, when reasonably knowable:

- anticipated participants with constitutional or delegated Standing;
- contribution domains;
- entry paths and accessibility needs;
- materially plausible revision conditions;
- known participation-integrity risks;
- known Sovereignty Claims or Authority Conflicts.

### 7.2 Challenge

A participant MAY challenge:

- omission or incorrect scoping of Standing;
- inaccessible or untimely entry;
- inaccurate representation;
- impossible or ceremonial revision conditions;
- category-based credibility discount;
- conflicted or unreviewable rejection authority;
- failure to preserve dissent;
- downstream non-repair;
- authority downgrading.

### 7.3 Test

Test MUST support Participation Integrity testing when required by policy or risk tier.

Methods MAY include:

- sampled decision-record review;
- counterfactual comparison of materially similar cases;
- reversal rates by participant or source type;
- abandonment and delay rates;
- actual credibility rationales;
- accessibility effectiveness;
- whether testimony was understood before rejection;
- whether downstream records were repaired after successful challenge.

### 7.4 Adjudicate

Adjudication MUST distinguish:

- Standing;
- Authority;
- relevance;
- evidence quality;
- credibility;
- correctness;
- Participation Integrity;
- Sovereignty or Authority Conflict.

The adjudicator SHOULD record what materially sufficient contribution could have changed the result.

### 7.5 Legitimize

A Participation Integrity Attestation is REQUIRED for:

- critical-risk decisions;
- high-risk rights-affecting or liberty-affecting decisions;
- public-benefit eligibility or prior-authorization decisions;
- high-risk employment, healthcare, housing, education, safety, or access decisions;
- irreversible externally affecting decisions;
- decisions where affected-party Standing, Appeal Standing, or Repair Standing was materially exercised.

Legitimize MUST NOT represent a process as participation-integrity-verified when the attestation result is `compromised`, `failed`, or `insufficient_evidence` unless an explicit exception is authorized, reasoned, recorded, time-bounded where applicable, and subject to Learn and Repair.

A detected Sovereignty Claim MUST follow RFC-CDP-074 blocking and escalation rules. Participation Integrity Attestation does not cure missing jurisdiction or illegitimate authority.

### 7.6 Execute

Execution MUST honor Participation Integrity constraints and unresolved blocking failures recorded during Legitimize.

An exception MUST NOT erase the underlying participation-integrity failure or repair obligation.

### 7.7 Record

Record MUST preserve:

- the Standing artifact;
- participation and representation artifacts;
- evaluation and credibility rationales;
- the Participation Integrity Attestation;
- exceptions and unresolved uncertainty;
- review, sovereignty, dissent, and repair references.

### 7.8 Learn

Learn MUST support analysis of:

- patterned exclusion or credibility discount;
- unreachable revision conditions;
- accessibility failure;
- abandonment and delay;
- reversal patterns;
- inaccurate representation;
- downstream record-repair failure;
- differences by disability, language, distress, communication style, hierarchy, role, institution, or source type;
- authority-downgrading patterns.

Learn MUST NOT convert decision-local credibility judgments into generalized trustworthiness scores without separate authority, purpose limitation, privacy review, and contestability.

### 7.9 Repair

Repair MUST be available when Participation Integrity is compromised or failed.

Repair MAY require:

- restoration or correction of the contribution record;
- reconsideration by a differently situated reviewer;
- correction of credibility or relevance classifications;
- reversal or remand of the decision;
- repair of downstream records, scores, labels, model inputs, and precedents;
- institutional process change;
- preservation of dissent and unresolved claims;
- escalation under RFC-CDP-073 or RFC-CDP-074.

---

## 8. Decision object and governed-path integration

The canonical Decision object under RFC-CDP-020 MUST support references to Participation Integrity artifacts.

Recommended fields:

```yaml
participation_integrity_attestation_refs:
  - <artifact_ref>
participation_integrity_status: <not_required|pending|intact|partially_intact|compromised|failed|insufficient_evidence>
```

The Decision Lifecycle Envelope SHOULD include Participation Integrity references in the governed path manifest so their creation, update, exception, and supersession are auditable.

---

## 9. Privacy and anti-retaliation boundary

Participation Integrity evidence may reveal disability, affected-party status, language needs, conflict, credibility judgments, cultural restrictions, authority claims, or participation history.

Implementations MUST apply:

- purpose limitation;
- minimum necessary collection;
- decision-local storage by default;
- role-based access controls;
- retention limits;
- audit logging;
- protection against retaliation;
- challenge and correction rights;
- separation from generalized risk or trust scores;
- culturally and legally appropriate handling restrictions.

A Participation Integrity Attestation MUST NOT become a permanent credibility profile of a participant.

---

## 10. Falsification and review

This RFC should weaken, narrow, or be superseded if evidence shows that:

- every Participation Integrity failure is already fully represented and enforceable through RFC-CDP-033, RFC-CDP-070, and RFC-CDP-073 without this artifact;
- the attestation adds no operational discrimination beyond ordinary process-compliance checking;
- its fields cannot distinguish legitimate role boundaries from exclusion;
- the artifact creates greater surveillance, retaliation, or credibility harm than it prevents;
- integrity results are not sufficiently reliable or contestable to support legitimacy decisions;
- Sovereignty or Authority claims are repeatedly flattened through its use.

Implementations MUST preserve evidence of both success and failure rather than treating adoption as proof of value.

---

## 11. Summary

Standing allocates participation.

Participation Integrity tests whether participation remained real.

Contestability challenges failure.

Anti-Erasure preserves contribution, authority context, and dissent.

Repair restores what the process damaged.

Sovereignty remains authority the inquiry did not create.
