# RFC-CDP-045 — Legitimize Protocol

Author: Kevin “Andie” Williams  
Status: Draft v0.6  
Series: Constitutional Decision Plane (CDP)  
Date: July 29, 2026  
Updates: RFC-CDP-045 v0.5  
Depends On: RFC-CDP-001, RFC-CDP-021, RFC-CDP-022, RFC-CDP-023, RFC-CDP-024, RFC-CDP-025, RFC-CDP-033, RFC-CDP-041, RFC-CDP-042, RFC-CDP-044  
Related: RFC-CDP-002, RFC-CDP-046, RFC-CDP-047, RFC-CDP-048, RFC-CDP-070, RFC-CDP-090

## Abstract

Defines how an adjudicated CDP Decision becomes legitimate and institutionally enactable.

Draft v0.6 distinguishes procedural legitimacy from constitutional legitimacy under the answerability root established in `RFC-CDP-001-Vision-Scope-Principles.md` Section 5.1, and adds the Answerability Gate alongside the existing Proposal Sufficiency and Anti-Premature-Certainty evidence requirements.

A decision MUST NOT be legitimized unless the governed path shows sufficient or validly excepted proposal admission, applicable APC gate satisfaction, valid standing and authority, challenge disposition, no material answerability claim erased, ignored, or institutionally denied, and no unresolved blocking conditions.

Procedural completion establishes procedural legitimacy. It does not, by itself, establish constitutional legitimacy. Hierarchy may provide evidence of delegated authority in some institutional contexts. Hierarchy alone does not confer legitimacy of either kind.

---

## 1. Purpose

The Legitimize Protocol answers:

- how an adjudicated decision becomes institutionally enactable;
- who may confer legitimacy;
- what authority and standing are required;
- what sufficiency, challenge, repair, and APC evidence must exist;
- whether the answerability claims raised by the decision were preserved or erased;
- when legitimacy must fail;
- how legitimacy is recorded.

Legitimize does not determine whether a proposal was interesting, plausible, useful, or well-formed.

Legitimize determines whether a governed decision has authority to proceed, and whether that procedural authority also preserved the answerability it was required to address.

---

## 2. Failure Mode: Legitimacy Without Governed Sufficiency Evidence

The failure mode this RFC addresses is **legitimacy without governed sufficiency evidence**.

Legitimacy without governed sufficiency evidence occurs when a decision is treated as legitimate even though the governed path does not contain verifiable, non-cosmetic evidence that the proposal earned admission, survived applicable challenge surfaces, and satisfied applicable APC requirements.

This failure has two mechanisms.

### 2.1 Missing Evidence

Missing evidence occurs when required proposal sufficiency, APC gate result, standing, authority, challenge disposition, or repair/appeal references are absent from the governed path when Legitimize is attempted.

### 2.2 Unverified Evidence

Unverified evidence occurs when the required records exist, but were not meaningfully contested, reviewed, or verified.

Examples include:

- APC gate results completed cosmetically;
- unresolved formation challenges ignored;
- blocking challenges bypassed;
- exception records granted by the proposer;
- affected-party claims left unresolved;
- standing projections stale or invalid;
- authority basis asserted but not attested.

RFC-CDP-045 can structurally block missing evidence.

It addresses unverified evidence through required references to challenge disposition, standing basis, authority basis, APC gate result, and open dissent.

This failure mode concerns the evidence for procedural legitimacy. A governed path can supply all of it and still erase, ignore, or institutionally deny a material answerability claim; that distinct failure is addressed by the Answerability Gate in Section 7.

---

## 3. The Necessary-Not-Sufficient Axiom

CDP distinguishes five things that are easy to collapse into one: integrity, sufficiency, procedural legitimacy, constitutional legitimacy, and correctness. Hierarchy is a related, sixth term that CDP must keep separate from all five; it is treated in Section 4.

**Integrity** means the governed path record has not been silently mutated. It is evidenced by `governed_path_hash` verification under RFC-CDP-023.

**Sufficiency** means the proposal earned admission into the governed lifecycle. It is evidenced by proposal sufficiency records under RFC-CDP-024 and applicable APC gate results under RFC-CDP-022.

**Procedural Legitimacy** means the decision moved through the governed steps this RFC requires: adjudication occurred, actors held valid standing and authority, required challenges were processed, and required sufficiency and APC evidence exist. Procedural legitimacy is evidenced by the presence and validity of the records Sections 5 through 8 require.

**Constitutional Legitimacy** means the decision preserved and addressed the answerability created by the consequence-bearing relationships it touches, per the root principle in `RFC-CDP-001-Vision-Scope-Principles.md` Section 5.1 and the standing model in `RFC-CDP-033-Standing-and-Recusal-Model.md`. A decision has constitutional legitimacy only when the answerability claims raised by affected parties, evidence custodians, and record-keepers were not erased, ignored, or institutionally denied along the way. Constitutional legitimacy is evidenced by the Answerability Gate defined in Section 7.

**Correctness** means the decision is factually, technically, ethically, or operationally right in the relevant domain. Correctness is not conferred by legitimacy of either kind.

**Hierarchy** means a role, rank, office, organizational position, or chain-of-command relationship that may confer delegated authority in some institutional contexts.

These are distinct.

Integrity is necessary but not sufficient for sufficiency.

Sufficiency is necessary but not sufficient for procedural legitimacy.

Procedural legitimacy is necessary but not sufficient for constitutional legitimacy.

Constitutional legitimacy is necessary but not sufficient for correctness.

Hierarchy is neither necessary nor sufficient for legitimacy of either kind.

A decision can have:

- integrity without sufficiency;
- sufficiency without procedural legitimacy;
- procedural legitimacy without constitutional legitimacy;
- constitutional legitimacy without correctness;
- hierarchy without legitimacy;
- legitimacy without hierarchy;
- a valid hash preserving an illegitimate process;
- a sufficient proposal adjudicated by actors without valid standing;
- a hierarchical approval that bypassed affected-party standing, challenge, repair, or dissent;
- a procedurally complete legitimization that erased, ignored, or institutionally denied a material answerability claim.

Therefore, stated plainly:

> Procedural legitimacy does not establish constitutional legitimacy.

> Constitutional legitimacy does not establish correctness.

> Hierarchy does not establish legitimacy of either kind.

These axioms are normative. Legitimize MUST NOT treat completion of the procedural checks in Sections 5 through 6 as though it had also satisfied Section 7. The two are evidenced separately and recorded separately.

---

## 4. Authority and Standing

Actors invoking Legitimize MUST possess `LEGITIMIZE` authority.

Actors invoking Legitimize MUST also have valid standing at the Legitimize stage under RFC-CDP-033.

Where implemented, standing MUST be evaluated through `cdp_standing_record` under RFC-CDP-025.

A decision MUST NOT be legitimized by an actor with missing, stale, invalid, expired, blocked, contested, recused, or non-current standing unless an explicit emergency exception is invoked, recorded, and subject to post-hoc review.

The proposer MUST NOT be the sole or decisive legitimizer of their own proposal.

A hierarchical superior, executive sponsor, system owner, manager, or chain-of-command actor MUST NOT be treated as legitimate solely by virtue of hierarchy.

Hierarchical authority MAY satisfy part of the authority basis only when the governed path also satisfies standing, sufficiency, challenge, repair, dissent, and answerability requirements.

---

## 5. Preconditions

Before Legitimize may proceed:

- the Decision MUST be adjudicated under RFC-CDP-044 or equivalent adjudication record;
- the Decision Lifecycle Envelope MUST conform to RFC-CDP-023;
- proposal admission MUST be visible through `proposal_sufficiency_ref`;
- the referenced proposal sufficiency record MUST have `sufficiency_status: sufficient` or `sufficiency_status: excepted`;
- applicable APC gate result requirements MUST be satisfied or validly exceptioned;
- required challenge disposition records MUST exist;
- required authority, jurisdictional, policy, quorum, signature, or approval checks MUST be satisfied;
- standing and recusal checks MUST be valid;
- the Answerability Gate defined in Section 7 MUST be satisfied or validly exceptioned;
- no unresolved blocking conditions may remain.

---

## 6. APC Gate Requirement

Legitimize consumes the `anti_premature_certainty_gate_result` payload defined in RFC-CDP-022.

Before a decision can be legitimized, the Decision Lifecycle Envelope MUST contain at least one applicable `apc_gate_result_ref` when APC is required by risk tier, authority level, reversibility, external effect, or implementation profile.

The referenced APC gate result MUST have:

```yaml
gate_context: legitimize
passed: true
```

or it MUST have a valid documented exception.

### 6.1 Risk-Tiered Requirement

APC pass or valid exception is a hard prerequisite for:

- high-risk decisions;
- critical-risk decisions;
- unknown-risk decisions;
- externally affecting decisions;
- irreversible decisions;
- high-authority decisions.

For low and medium risk decisions, APC requirements MAY be staged according to RFC-CDP-024 or implementation profiles.

However:

> Legitimize MUST NOT proceed if the APC gate result required for this decision's risk tier is absent, failed, unknown, or unresolved.

Risk tier determines which APC requirement applies.

Risk tier does not waive the applicable requirement.

### 6.2 APC Exceptions

An APC exception MUST:

- identify the failed, missing, unknown, or waived criteria;
- identify the exception authority;
- include rationale;
- include compensating controls;
- set `learn_review_required: true`;
- be referenced by the legitimacy record.

The proposer MUST NOT authorize their own APC exception.

Proposer recusal from APC exception authority is absolute.

The exception authority MUST have valid Adjudicate-stage standing or stronger delegated governance authority.

---

## 7. Answerability Gate Requirement

Legitimize consumes the answerability evidence already required elsewhere in the governed path: `standing_basis_ref` under RFC-CDP-033, `affected_party_claim_refs`, `appeal_refs`, and any Breach Record under RFC-CDP-072.

Before a decision can be legitimized, the legitimacy record MUST carry `unresolved_answerability_claim_refs` and MUST set `constitutional_legitimacy_status`.

`unresolved_answerability_claim_refs` lists every material answerability claim — affected-party claim, sovereignty claim, denial of recognized standing, or open appeal — that touches this decision and remains open. An empty list is a positive claim that no material answerability claim remains open. It MUST be attested, not assumed, in the same manner as `open_dissent_refs`.

`constitutional_legitimacy_status` MUST be one of `preserved`, `blocked`, or `escalated`.

`constitutional_legitimacy_status: preserved` requires that every claim in `unresolved_answerability_claim_refs` is visibly tracked, and that no material answerability claim tied to this decision has been erased, ignored, or institutionally denied without record.

An answerability claim has been **erased** when it existed in the governed path and no longer appears in any referenced record. An answerability claim has been **ignored** when it was raised, remains visible, and received no institutional response within the response window required by `RFC-CDP-070-Appeals-and-Contestability-Model.md`. An answerability claim has been **institutionally denied** when the responding institution rejected it without the rationale, review authority, and contestability path required by RFC-CDP-070 or RFC-CDP-074.

The Answerability Gate applies the Answerability Test from `RFC-CDP-033-Standing-and-Recusal-Model.md` Section 11.3 to every claim referenced by the decision: what governed act is occurring, what consequence exists or may exist, what relationship creates answerability, what answer is constitutionally owed, and what evidence narrows or defeats the claim. A claim MUST NOT be treated as resolved on the strength of questions 1 through 3 alone; resolution requires a visible answer to question 4.

Passing the blocking conditions in Section 8 establishes procedural legitimacy. `constitutional_legitimacy_status: preserved` is required in addition, before the decision holds constitutional legitimacy. Legitimize MUST record both `status` and `constitutional_legitimacy_status`. Neither substitutes for the other, and a decision MUST NOT be presented as constitutionally legitimate on the strength of `status: granted` alone.

---

## 8. Blocking Conditions

Legitimize MUST NOT proceed when any of the following conditions are true:

1. `proposal_sufficiency_ref` is null or points to a record with `sufficiency_status` other than `sufficient` or `excepted`.
2. APC is required for the decision and `apc_gate_result_refs` is empty.
3. A required APC gate result has `passed: false`, `unknown`, unresolved criteria, or no valid exception.
4. Any unresolved blocking ordinary Challenge exists in `challenge_refs`.
5. Any unresolved Formation Challenge exists in `formation_challenge_refs`.
6. Any active appeal exists in `appeal_refs`.
7. Any unresolved affected-party claim exists in `affected_party_claim_refs`.
8. The Decision Lifecycle Envelope has `standing_status` other than `valid`, unless an explicit emergency exception is invoked, recorded, and subject to post-hoc review.
9. A material answerability claim has been erased, ignored, or institutionally denied as defined in Section 7, or `unresolved_answerability_claim_refs` is absent when required.

These are hard stops.

An implementation that permits Legitimize to proceed with any active blocking condition is non-compliant with this RFC.

---

## 9. Legitimacy Record

Legitimize MUST produce a governed legitimacy record.

Minimum schema:

```yaml
legitimacy_record:
  record_id: <uuid>
  decision_id: <uuid>
  legitimized_by: <actor_ref>
  legitimized_at: <timestamp>
  status: <granted|denied|escalated>
  constitutional_legitimacy_status: <preserved|blocked|escalated>
  authority_basis_ref: <ref>
  standing_basis_ref: <ref>
  adjudication_ref: <ref>
  proposal_sufficiency_ref: <ref>
  apc_gate_result_ref: <ref>
  challenge_disposition_refs: [<ref>]
  formation_challenge_disposition_refs: [<ref>]
  open_dissent_refs: [<ref>]
  unresolved_answerability_claim_refs: [<ref>]
  hierarchy_basis_ref: <ref|null>
  exception_record_ref: <ref|null>
  scope: <string>
  constraints: [<string>]
  effective_at: <timestamp|null>
  expires_at: <timestamp|null>
  execution_conditions: [<string>]
  record_hash: <hash|null>
  lineage_refs: [<ref>]
```

Required references:

- `authority_basis_ref`
- `standing_basis_ref`
- `adjudication_ref`
- `proposal_sufficiency_ref`
- `apc_gate_result_ref`
- `challenge_disposition_refs`
- `formation_challenge_disposition_refs`
- `open_dissent_refs`
- `unresolved_answerability_claim_refs`

`hierarchy_basis_ref` may be null.

When non-null, it identifies a hierarchy, office, chain-of-command, or role-basis claim that may contribute to the authority basis.

It does not substitute for standing, sufficiency, challenge disposition, or answerability requirements.

`open_dissent_refs` may be empty.

An empty list is a positive claim that no material dissent remains unresolved. It MUST be attested, not assumed.

`unresolved_answerability_claim_refs` may be empty on the same terms as `open_dissent_refs`: an empty list is a positive, attested claim that no material answerability claim remains open, erased, ignored, or institutionally denied.

`status: granted` reflects procedural legitimacy only. It MUST NOT be read as also establishing constitutional legitimacy; `constitutional_legitimacy_status` is the field that does that, and it is evidenced separately.

`exception_record_ref` may be null only when no exception was invoked.

When non-null, it MUST point to a valid exception record with proposer recusal confirmed.

---

## 10. Envelope and Persistence Requirements

### 10.1 Envelope Update

The legitimacy record MUST be referenced in the Decision Lifecycle Envelope before the envelope status may advance to `legitimized`.

The reference SHOULD appear as:

```yaml
stage_record_refs:
  legitimacy_ref: <ref>
```

Legitimize without a Decision Lifecycle Envelope update is not governed legitimization.

### 10.2 Persistence

The legitimacy record MUST be persisted as a governed record under RFC-CDP-025 before `legitimacy_ref` is set in the envelope.

Recommended persistence:

```text
cdp_governed_record.record_type = legitimacy_record
```

### 10.3 Standing Check Record

The standing check used to authorize Legitimize MUST be recorded or referenced by `standing_basis_ref`.

If a standing projection is stale, invalid, missing, or contested, Legitimize MUST block unless an emergency exception is invoked and recorded.

---

## 11. State Transitions

Allowed transitions:

```text
adjudicated -> legitimized
adjudicated -> legitimacy_denied
adjudicated -> escalated
```

Legitimize MUST NOT transition directly from proposed, under_challenge, under_test, or admission_pending states.

A decision MUST NOT transition to `legitimized` while `constitutional_legitimacy_status` is `blocked`. It MAY transition to `escalated` for institutional resolution of the blocking answerability claim.

Legitimacy does not authorize execution by itself unless execution authority and execution conditions are separately satisfied under RFC-CDP-046.

---

## 12. Payload Schema

Content-Type:

```text
application/cdp.legitimize+json
```

```json
{
  "status": "granted | denied | escalated",
  "constitutional_legitimacy_status": "preserved | blocked | escalated",
  "basis": "string",
  "scope": "string",
  "constraints": ["string"],
  "granted_by": ["actor_id"],
  "authority_basis_ref": "ref",
  "standing_basis_ref": "ref",
  "adjudication_ref": "ref",
  "proposal_sufficiency_ref": "ref",
  "apc_gate_result_ref": "ref",
  "challenge_disposition_refs": ["ref"],
  "formation_challenge_disposition_refs": ["ref"],
  "open_dissent_refs": ["ref"],
  "unresolved_answerability_claim_refs": ["ref"],
  "hierarchy_basis_ref": "ref|null",
  "exception_record_ref": "ref|null",
  "effective_at": "timestamp|null",
  "expires_at": "timestamp|null",
  "execution_conditions": ["string"],
  "metadata": {}
}
```

---

## 13. Failure Conditions

Legitimacy MUST fail or escalate when:

- adjudication is incomplete;
- authority is insufficient;
- jurisdiction is invalid;
- hierarchy is asserted as a substitute for governed legitimacy;
- required controls are absent;
- standing is invalid, stale, blocked, or contested;
- required sufficiency evidence is missing;
- required APC evidence is failed, unknown, unresolved, or invalidly exceptioned;
- unresolved blocking Challenge exists;
- unresolved Formation Challenge exists;
- unresolved affected-party claim exists;
- a material answerability claim has been erased, ignored, or institutionally denied;
- active appeal or repair condition blocks closure or advancement;
- time bounds or safety constraints are violated.

---

## 14. Security and Governance Considerations

Legitimacy records may expose sensitive authority, standing, dissent, exception, adjudication, hierarchy, and affected-party information.

Implementations SHOULD address:

- authority capture;
- hierarchy capture;
- proposer self-legitimization;
- APC exception abuse;
- stale standing projections;
- summary substitution;
- unresolved dissent suppression;
- answerability claim erasure or suppression;
- affected-party standing protection;
- repair and appeal hooks;
- traceability of legitimacy basis;
- separation between hierarchy, authority, procedural legitimacy, constitutional legitimacy, and correctness.

---

## 15. Status of This Draft

Promoted into Draft v0.4:

- corrected canonical heading from legacy RFC-CDP-006 to RFC-CDP-045;
- updated dependencies to current RFC numbering;
- legitimacy without governed sufficiency evidence as failure mode;
- missing evidence and unverified evidence as mechanisms;
- the Necessary-Not-Sufficient Axiom;
- APC gate result consumption from RFC-CDP-022;
- risk-tiered APC prerequisite with hard floor;
- APC exception constraints and proposer recusal;
- eight hard blocking conditions;
- legitimacy record schema;
- integrity vs sufficiency vs legitimacy distinction;
- envelope and persistence requirements.

Promoted into Draft v0.5:

- hierarchy as distinct from legitimacy;
- hierarchy as neither necessary nor sufficient for legitimacy;
- hierarchy basis reference as optional evidence, not substitute authority;
- hierarchy capture as a governance risk.

Promoted into Draft v0.6:

- procedural legitimacy and constitutional legitimacy as distinct concepts, re-grounded in the answerability root of `RFC-CDP-001` Section 5.1;
- the Answerability Gate Requirement, consuming standing, affected-party, appeal, and breach-record evidence already required elsewhere in the governed path;
- `constitutional_legitimacy_status` and `unresolved_answerability_claim_refs` in the legitimacy record and payload schema;
- a ninth blocking condition for erased, ignored, or institutionally denied answerability claims;
- a state-transition rule preventing `legitimized` while `constitutional_legitimacy_status` is `blocked`.

Deferred:

- contested legitimization adjudication process;
- canonical risk classification mechanism;
- detailed emergency exception timing;
- state machine alignment;
- record_hash propagation.

---

## 16. Principle

Correct does not imply legitimate.

Sufficient does not imply legitimate.

Intact does not imply sufficient.

Hierarchical does not imply legitimate.

Non-hierarchical does not imply illegitimate.

Procedurally complete does not imply constitutionally legitimate.

Integrity is necessary but not sufficient for sufficiency.

Sufficiency is necessary but not sufficient for procedural legitimacy.

Procedural legitimacy is necessary but not sufficient for constitutional legitimacy.

Constitutional legitimacy is necessary but not sufficient for correctness.

Hierarchy is neither necessary nor sufficient for legitimacy of either kind.

Legitimacy is conferred by governed process, not assumed from plausibility, completeness, confidence, rank, office, hierarchy, or clean formatting. Constitutional legitimacy is conferred by preserving and addressing answerability, not assumed from the completion of procedure.
