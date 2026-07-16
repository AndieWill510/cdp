# RFC-CDP-033A — Operational Reachability Attestation

**Status:** Staged companion draft  
**Date:** July 15, 2026  
**Series:** Constitutional Decision Plane (CDP)  
**Extends:** RFC-CDP-033  
**Depends On:** RFC-CDP-020, RFC-CDP-031, RFC-CDP-033, RFC-CDP-043, RFC-CDP-045, RFC-CDP-047, RFC-CDP-048, RFC-CDP-070, RFC-CDP-073  
**Defers To:** RFC-CDP-032 and RFC-CDP-074 for sovereignty and authority pluralism  
**Related:** `docs/constantc-cdp-standing-epistemic-safety-bridge.md`

---

## Abstract

RFC-CDP-033 defines whether an actor has valid Standing to participate in a specific stage of a specific decision.

This companion draft proposes a separate **Operational Reachability Attestation** for evaluating whether allocated Standing can actually be exercised in practice.

The proposal does not redefine Standing, create a new lifecycle stage, or duplicate Appeals, Anti-Erasure, or Sovereignty governance.

It asks a narrower question:

> Was the participant's valid standing operationally reachable enough for their contribution to be received, understood, evaluated, answered, and—when materially relevant—capable of revising the controlling account?

---

## 1. Problem statement

A governance process may allocate Standing correctly while defeating that Standing in operation.

Examples include:

- an affected party has standing to challenge but the challenge channel is inaccessible;
- testimony enters the record but is categorically discounted because of disability, distress, language, fluency, hierarchy, or source status;
- the stated evidentiary threshold can never realistically be met by the participant assigned to satisfy it;
- a reviewer may reconsider the outcome but not the credibility judgment that controlled it;
- a successful appeal changes the immediate result while leaving downstream records, labels, scores, or model inputs unrepaired;
- delay or procedural burden causes systematic abandonment before review can occur.

These are not necessarily failures of Standing allocation.

They are failures of operational reachability.

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

This draft does not create a parallel Standing object.

### 2.2 Authority

Operational reachability does not expand an actor's Authority.

A participant may have a contribution heard and evaluated without acquiring authority to adjudicate, legitimize, or execute.

### 2.3 Contestability

RFC-CDP-070 provides a constitutional right of entry into appeal or contestability review.

Operational reachability evaluates whether that right can be exercised effectively in practice.

### 2.4 Anti-Erasure

RFC-CDP-073 governs affected-party review and anti-erasure.

Operational reachability supplies a possible audit artifact for detecting a narrower failure:

> the participant remains formally present while their contribution is structurally incapable of influencing the evolving account.

### 2.5 Sovereignty

This draft MUST NOT classify a sovereignty claim as an ordinary standing or reachability issue.

When a sovereignty claim or authority conflict is present, implementations MUST defer to RFC-CDP-032 and RFC-CDP-074 before applying ordinary participant-standing analysis.

---

## 3. Working definition

**Operational Reachability** is the demonstrable ability of an actor with valid Standing to use an accessible governed path through which a relevant contribution is:

1. received;
2. represented accurately;
3. evaluated under accountable standards;
4. answered with reasons;
5. reviewable when discounted or rejected;
6. capable of revising the decision, account, credibility judgment, or record when materially sufficient.

Reachability does not require that the contribution prevail.

It requires that the path be real rather than ceremonial.

---

## 4. Reachability dimensions

A reachability evaluation SHOULD consider:

### 4.1 Domain

What contribution is the participant entitled or responsible to make at this stage?

### 4.2 Entry

Through what accessible mechanism can the contribution enter the governed record?

### 4.3 Representation

Was the contribution preserved accurately, including accommodations, uncertainty, and context?

### 4.4 Evaluation

What evidentiary, relevance, and credibility standards were applied?

### 4.5 Revision

What contribution could alter the controlling account, decision, credibility assessment, or record?

### 4.6 Rejection

Who may reject or limit the contribution, under what authority and standard, and with what reasons?

### 4.7 Review

Can the rejection, limitation, or credibility judgment be challenged by a differently situated or authorized reviewer?

### 4.8 Repair

Can a successful challenge repair both the immediate outcome and downstream records or model inputs?

### 4.9 Empirical reachability

Do materially similar participants actually succeed in using the path without patterned irrelevant discount?

---

## 5. Proposed standing-record extension

The existing RFC-CDP-033 `standing_record` MAY be extended by reference rather than replacement:

```yaml
standing_record:
  # existing RFC-CDP-033 fields remain authoritative
  contribution_domains:
    - <string>
  entry_path_refs:
    - <artifact_ref>
  revision_conditions:
    - <string>
  rejecting_authority_ref: <actor_or_authority_ref|null>
  review_path_ref: <artifact_ref|null>
  reachability_attestation_ref: <artifact_ref|null>
```

These fields SHOULD remain optional until this draft is promoted or superseded.

The canonical Decision object SHOULD link to Standing and Reachability artifacts rather than embed a mutable duplicate of them.

---

## 6. Reachability Attestation seed

```yaml
reachability_attestation:
  attestation_id: <uuid>
  decision_id: <uuid>
  standing_id: <uuid>
  actor_id: <uuid>
  stage: <propose|challenge|test|adjudicate|legitimize|execute|record|learn>

  contribution_domains:
    - <string>

  entry:
    paths_offered:
      - <artifact_ref|string>
    accessible: <true|false|unknown>
    accommodation_refs:
      - <artifact_ref>

  representation:
    contribution_record_refs:
      - <artifact_ref>
    participant_confirmed_accuracy: <true|false|not_requested|unknown>
    material_context_omitted: <true|false|unknown>

  evaluation:
    relevance_determination: <relevant|partially_relevant|not_relevant|unresolved>
    evidence_quality_basis_ref: <artifact_ref|null>
    credibility_discount_applied: <true|false|unknown>
    credibility_discount_basis_ref: <artifact_ref|null>
    credibility_discount_reviewable: <true|false|unknown>

  revision:
    revision_conditions:
      - <string>
    contribution_changed_account: <true|false|not_applicable|unknown>
    account_change_ref: <artifact_ref|null>
    rejection_reason_ref: <artifact_ref|null>

  review:
    review_path_available: <true|false|unknown>
    review_path_ref: <artifact_ref|null>
    differently_situated_reviewer: <true|false|unknown>

  repair:
    immediate_outcome_repaired: <true|false|not_applicable|unknown>
    downstream_record_repair_status: <not_required|pending|partial|complete|failed|unknown>
    repair_refs:
      - <artifact_ref>

  empirical_evidence:
    audit_sample_ref: <artifact_ref|null>
    materially_similar_case_comparison_ref: <artifact_ref|null>
    patterned_discount_detected: <true|false|unknown>
    abandonment_or_delay_signal: <true|false|unknown>

  result: <reachable|partially_reachable|unreachable|insufficient_evidence|not_applicable>
  unresolved_uncertainty:
    - <string>
  attested_by: <actor_id>
  attested_at: <timestamp>
```

This is a schema seed, not adopted protocol.

---

## 7. Lifecycle integration

No new lifecycle stage is created.

### 7.1 Propose

The proposal MAY identify anticipated participants, contribution domains, accessibility needs, and expected revision conditions.

### 7.2 Challenge

A participant MAY challenge:

- omission from a relevant domain;
- inaccessible entry paths;
- impossible revision conditions;
- category-based credibility discounts;
- conflicted rejecting authority;
- failure to preserve the contribution accurately.

### 7.3 Test

Test MAY evaluate reachability through:

- sampled decision records;
- counterfactual comparison of materially similar cases;
- reversal rates by participant or source type;
- abandonment and delay rates;
- actual credibility rationales;
- accessibility effectiveness;
- whether testimony was understood before rejection;
- whether downstream records were repaired after successful challenge.

### 7.4 Adjudicate

Adjudication SHOULD distinguish:

- Standing;
- Authority;
- relevance;
- evidence quality;
- credibility;
- correctness;
- reachability.

The adjudicator SHOULD record what materially sufficient contribution could have changed the result.

### 7.5 Legitimize

Legitimization MAY require a Reachability Attestation for high-risk, rights-affecting, liberty-affecting, public-benefit, employment, healthcare, safety, or irreversible decisions.

A decision SHOULD NOT be represented as reachability-verified when the attestation result is `unreachable` or `insufficient_evidence` without an explicit exception, rationale, authority basis, and recorded risk acceptance.

### 7.6 Record

The Record stage SHOULD preserve:

- the Standing artifact;
- contribution and representation artifacts;
- evaluation and credibility rationales;
- the Reachability Attestation;
- unresolved uncertainty;
- review and repair references.

### 7.7 Learn

Learn MAY analyze:

- patterned exclusion or credibility discount;
- unreachable revision conditions;
- accessibility failure;
- abandonment and delay;
- reversal rates;
- downstream record-repair failure;
- differences by disability, language, distress, communication style, hierarchy, role, or source type.

Learn MUST NOT convert decision-local credibility judgments into a generalized trustworthiness score without separate authority, purpose limitation, contestability, and privacy review.

---

## 8. Governance and privacy boundary

Reachability evidence may reveal disability, affected-party status, language needs, conflict, credibility judgments, or participation history.

Implementations SHOULD apply:

- purpose limitation;
- minimum necessary collection;
- decision-local storage by default;
- access controls;
- retention limits;
- audit logging;
- protection against retaliation;
- challenge and correction rights;
- separation from generalized risk or trust scores.

A Reachability Attestation MUST NOT become a permanent credibility profile of a participant.

---

## 9. Falsification and challenge

This proposal should weaken or fail if evidence shows that:

- RFC-CDP-033 and RFC-CDP-070 already fully capture every proposed reachability obligation without additional fields or attestations;
- no case exists where valid Standing and a formal challenge path coexist with a structurally unusable revision path;
- the attestation adds no operational discrimination beyond existing anti-erasure review;
- reachability cannot be assessed without creating disproportionate surveillance or credibility harms;
- the schema creates more ceremonial compliance than useful evidence;
- every identified failure is better repaired through a narrower accessibility, evidence, appeal, or anti-erasure amendment.

The goal is not to preserve this artifact.

The goal is to determine whether the gap is real and whether this is the smallest legitimate way to govern it.

---

## 10. Explicit non-goals

This RFC does not:

- redefine Standing;
- rename Standing;
- create a new lifecycle stage;
- create a separate standing tribunal;
- duplicate sovereignty governance;
- confer equal authority on every participant;
- require every contribution to prevail;
- require infinite reopening;
- establish AI personhood;
- create a generalized credibility score;
- promote ConstantC culture notes into CDP canon.

---

## 11. Status and next review

This is a staged companion draft in `rfcs/`, not a canonical RFC in `rfc/`.

Before promotion or amendment of RFC-CDP-033, review should determine:

1. whether the gap is already governed by existing Standing, Appeals, and Anti-Erasure provisions;
2. whether a separate attestation is necessary or a smaller amendment is sufficient;
3. which decisions require reachability evidence;
4. whether the schema is proportionate and privacy-preserving;
5. whether Test and Legitimize are the correct integration points;
6. whether implementation profiles should carry most of the empirical audit requirements.

Until that review occurs, existing RFC-CDP-033, RFC-CDP-070, RFC-CDP-073, and RFC-CDP-074 remain unchanged and authoritative.
