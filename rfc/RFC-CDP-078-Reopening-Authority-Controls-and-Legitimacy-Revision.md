# RFC-CDP-078 — Reopening Authority Controls and Legitimacy Revision

Author: Kevin “Andie” Williams  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: July 14, 2026  
Updates: RFC-CDP-045, RFC-CDP-073, RFC-CDP-077, RFC-CDP-092  
Depends On: RFC-CDP-023, RFC-CDP-033, RFC-CDP-045, RFC-CDP-070, RFC-CDP-073, RFC-CDP-074, RFC-CDP-076, RFC-CDP-077, RFC-CDP-092

## Abstract

This RFC resolves four blocking issues identified during Session 019 review of RFC-CDP-077:

1. materially independent reopening authority was required but not operationally defined;
2. `authority_independence_basis` was free text and therefore not queryable;
3. RFC-CDP-077 and RFC-CDP-092 carried overlapping but non-identical reopening trigger taxonomies;
4. RFC-CDP-045 had no governed way to represent later suspension, revocation, supersession, or reopening of an earlier legitimacy grant.

This RFC defines a controlled independence model, a canonical reopening-trigger registry, a Legitimacy Revision Record, state-machine consumption rules, and explicit lineage between affected-party review and reopening authority.

Where this RFC conflicts with reopening, independence, or legitimacy-revision language in RFC-CDP-045, RFC-CDP-073, RFC-CDP-077, or RFC-CDP-092, this RFC controls until those documents are revised or superseded.

---

## 1. Material Independence

A reopening authority is **materially independent** only when the authority is structurally capable of contesting the original governing account without being subordinate to the actor or body whose decision is under review.

Independence MUST be recorded using one of the following controlled values:

```text
independent_external
independent_internal_separate_reporting_line
independent_cross_authority
non_independent_with_safeguards
```

### 1.1 `independent_external`

The reopening authority is outside the institution, authority chain, or organizational unit that produced or legitimized the original decision.

The authority MUST have independent review power and MUST NOT be controlled by the original decision-maker.

### 1.2 `independent_internal_separate_reporting_line`

The reopening authority is inside the same institution but:

- is not the original decision-maker;
- is not in the original decision-maker's reporting line;
- is not evaluated, compensated, or removable solely by the original authority;
- has documented authority to revise the governing account and outcome;
- has protected access to the complete governed record.

A different individual in the same reporting line does not satisfy this value.

### 1.3 `independent_cross_authority`

The reopening authority derives authority from a distinct constitutional, jurisdictional, community, sovereign, regulatory, or delegated authority domain capable of contesting the original authority.

The authority relationship MUST be recorded and contestable.

### 1.4 `non_independent_with_safeguards`

This value states that materially independent review is not available.

It MUST NOT be described as a weaker form of independence.

Use of this value requires all of the following:

- explicit disclosure that the reviewer is not materially independent;
- conflict-of-interest recording;
- preserved affected-party dissent;
- preserved reviewer dissent;
- complete audit exposure of the independence limitation;
- a named escalation path if one exists;
- prohibition on self-certifying the review as independent;
- a reasoned statement explaining why independent authority was unavailable.

`non_independent_with_safeguards` MUST NOT satisfy any policy or implementation profile that explicitly requires materially independent review.

---

## 2. Independence Record

A reopening determination MUST include a queryable independence control surface:

```yaml
independence_control:
  independence_mode: <enum>
  # Allowed:
  #   independent_external
  #   independent_internal_separate_reporting_line
  #   independent_cross_authority
  #   non_independent_with_safeguards
  original_authority_ref: <ref>
  reopening_authority_ref: <ref>
  reporting_line_separation_attested: <boolean|null>
  authority_domain_separation_attested: <boolean|null>
  conflict_of_interest_refs: [<ref>]
  safeguard_refs: [<ref>]
  escalation_path_ref: <ref|null>
  independence_attestation_ref: <ref>
  limitations: [<string>]
```

`authority_independence_basis` MAY remain as a human-readable explanation, but it MUST NOT be the only independence field.

An implementation that stores only free text is non-compliant with this RFC.

---

## 3. Canonical Reopening Trigger Registry

RFC-CDP-077 owns the canonical reopening-trigger vocabulary.

RFC-CDP-092 MUST consume this registry as state-machine input and MUST NOT maintain an overlapping independent trigger list.

The canonical reopening triggers are:

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

### 3.1 `sovereignty_claim_material`

A sovereignty, jurisdiction, authority-pluralism, land, resource, rematriation, or community-authority claim becomes material to the continuing legitimacy of the decision or repair process.

### 3.2 `recurring_harm_pattern`

New evidence shows that the closed decision, governing account, policy, model, classification, or repair process participates in a recurring pattern of materially similar harm.

A recurring pattern may justify reopening even when no single new event independently establishes the full merits.

### 3.3 Registry Rule

Lifecycle and state-machine RFCs MAY define how a trigger affects transitions.

They MUST NOT redefine the trigger name or maintain a conflicting list.

New reopening triggers require an update to RFC-CDP-077 or a later RFC that explicitly updates the canonical registry.

---

## 4. State-Machine Consumption

RFC-CDP-092 MUST treat the canonical trigger registry as the source for reopening transition eligibility.

A Repair State Machine MAY add transition-specific preconditions, but it MUST preserve the originating trigger value in the governed record.

Recommended transition input:

```yaml
reopening_transition_input:
  reopening_request_ref: <ref>
  reopening_trigger: <canonical_trigger_enum>
  determination_ref: <ref>
  transition_authority_ref: <ref>
  independence_control_ref: <ref>
  prior_state: <state>
  requested_state: <state>
```

A trigger must not be silently translated into a generic `other` value.

---

## 5. Legitimacy Is Defeasible

A legitimacy grant is a governed determination made under a bounded record.

It is not a permanent declaration of correctness or infallibility.

A prior `status: granted` record MUST NOT be mutated to erase the original determination.

Later change MUST be represented through a Legitimacy Revision Record linked by lineage.

---

## 6. Legitimacy Revision Record

A Legitimacy Revision Record SHOULD be represented as:

```yaml
legitimacy_revision_record:
  record_id: <uuid>
  record_type: legitimacy_revision_record
  decision_id: <uuid>
  original_legitimacy_record_ref: <ref>
  reopening_determination_ref: <ref|null>
  revision_status: <enum>
  # Allowed:
  #   affirmed
  #   suspended
  #   revoked
  #   superseded
  #   reopened
  #   unresolved
  revision_basis: <string>
  evidence_refs: [<ref>]
  authority_ref: <ref>
  standing_basis_ref: <ref>
  independence_control_ref: <ref|null>
  effective_at: <timestamp>
  expires_at: <timestamp|null>
  replacement_legitimacy_record_ref: <ref|null>
  downstream_correction_refs: [<ref>]
  open_dissent_refs: [<ref>]
  unresolved_uncertainties: [<string>]
  lineage_refs: [<ref>]
  record_hash: <hash|null>
```

### 6.1 Revision Status Semantics

`affirmed` means reopened review examined the legitimacy basis and preserved the prior grant.

`suspended` means the prior grant is temporarily non-operative pending further evidence, adjudication, or repair.

`revoked` means the prior legitimacy basis no longer supports institutional enactability.

`superseded` means a later legitimacy record replaces the earlier record without erasing it.

`reopened` means the legitimacy determination has returned to active governed review and has not yet reached a new terminal status.

`unresolved` means the review cannot currently support affirmation, revocation, or supersession and preserves that uncertainty explicitly.

---

## 7. Effective Legitimacy State

The current legitimacy state of a decision MUST be derived from:

1. the original Legitimacy Record under RFC-CDP-045;
2. all subsequent Legitimacy Revision Records in lineage order;
3. any active reopening, appeal, suspension, or blocking condition.

A system MUST NOT determine current legitimacy solely by reading the first `status: granted` record.

Recommended derived values:

```text
legitimacy_granted
legitimacy_denied
legitimacy_escalated
legitimacy_suspended
legitimacy_revoked
legitimacy_superseded
legitimacy_reopened
legitimacy_unresolved
```

These are derived effective states, not mutations of the original record.

---

## 8. Execution Consequences

When effective legitimacy becomes `legitimacy_suspended`, `legitimacy_revoked`, `legitimacy_reopened`, or `legitimacy_unresolved`:

- new execution MUST block unless an explicit emergency authority applies;
- queued execution MUST pause;
- continuing execution MUST be reviewed for stay, rollback, mitigation, compensation, or exception;
- the Decision Lifecycle Envelope MUST expose the active legitimacy revision reference;
- affected downstream records MUST be identified for correction or supersession.

An emergency exception MUST be time-bound, reasoned, recorded, and subject to later review.

---

## 9. Relationship to Affected-Party Review

RFC-CDP-073's rule that the institution MUST NOT be the sole judge of its own closure is implemented through the independence model in this RFC.

Affected-party review MUST record whether reopening review used:

- materially independent authority; or
- `non_independent_with_safeguards`.

Affected-party participation does not by itself make institutional authority independent.

Institutional approval does not substitute for affected-party review.

Affected-party review does not automatically validate the affected party's claim.

It preserves standing, evidence, dissent, and contestability.

---

## 10. Compliance Failure Modes

An implementation is non-compliant when it:

- claims independence using free text without a controlled independence mode;
- labels a different individual in the same reporting line as materially independent;
- uses `non_independent_with_safeguards` while presenting the review as independent;
- omits sovereignty or recurring-harm triggers from reopening eligibility;
- maintains a conflicting trigger registry in the Repair State Machine;
- overwrites or deletes the original legitimacy grant when legitimacy changes;
- treats the first legitimacy grant as permanently controlling despite a later revision record;
- permits execution to continue silently after suspension, revocation, or reopening;
- allows the authority whose account is challenged to self-certify its own independence.

---

## 11. Migration Rules

Implementations of RFC-CDP-077 Draft v0.1 SHOULD migrate as follows:

1. replace free-text-only independence claims with `independence_control`;
2. map existing reopening triggers to the canonical registry;
3. add `sovereignty_claim_material` and `recurring_harm_pattern` where applicable;
4. preserve existing legitimacy records unchanged;
5. represent later legitimacy changes through Legitimacy Revision Records;
6. expose effective legitimacy state as a derived query surface;
7. make RFC-CDP-092 consume the RFC-CDP-077 trigger registry;
8. preserve all prior records and lineage.

---

## 12. Non-Goals

This RFC does not:

- require external review in every context;
- claim that internal review is always illegitimate;
- permit non-independent review to masquerade as independent;
- presume that a reopening requester is correct;
- abolish finality;
- require mutation of historical legitimacy records;
- define every domain-specific conflict-of-interest rule;
- replace affected-party review, adjudication, appeal, repair efficacy, or sovereign authority analysis.

---

## 13. Disposition

This RFC implements the Session 019 adjudication:

- use truthful `non_independent_with_safeguards` language rather than `independence_limited`;
- make RFC-CDP-077 the canonical reopening-trigger registry;
- absorb `sovereignty_claim_material` and `recurring_harm_pattern` into that registry;
- preserve original legitimacy records and add revision lineage;
- bind RFC-CDP-073 and RFC-CDP-092 to the same independence and trigger semantics.

RFC-CDP-077 remains Draft v0.1 until a collaborator verifies that this corrective RFC resolves the blocking review findings. After verification, the paired RFCs may advance through the promotion protocol.
