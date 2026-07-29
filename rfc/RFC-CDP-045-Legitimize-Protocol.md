# RFC-CDP-045 — Legitimize Protocol

Author: Kevin “Andie” Williams  
Status: Draft v0.7  
Series: Constitutional Decision Plane (CDP)  
Date: July 29, 2026  
Updates: RFC-CDP-045 v0.6  
Depends On: RFC-CDP-001, RFC-CDP-021, RFC-CDP-022, RFC-CDP-023, RFC-CDP-024, RFC-CDP-025, RFC-CDP-033, RFC-CDP-041, RFC-CDP-042, RFC-CDP-044, RFC-CDP-070, RFC-CDP-072  
Related: RFC-CDP-002, RFC-CDP-046, RFC-CDP-047, RFC-CDP-048, RFC-CDP-074, RFC-CDP-090

## Abstract

Defines how an adjudicated CDP Decision becomes legitimate and institutionally enactable.

Draft v0.7 distinguishes procedural legitimacy from constitutional legitimacy under the answerability root established in `RFC-CDP-001-Vision-Scope-Principles.md` Section 5.1, and adds the Answerability Gate alongside the existing Proposal Sufficiency and Anti-Premature-Certainty evidence requirements. It classifies every material answerability claim as `resolved`, `preserved_non_blocking`, `blocking`, or `escalated`, and evaluates `constitutional_legitimacy_status` independently of procedural `status`.

A decision MUST NOT be legitimized unless the governed path shows sufficient or validly excepted proposal admission, applicable APC gate satisfaction, valid standing and authority, challenge disposition, every material answerability claim attested and classified, and no unresolved blocking conditions. Procedural completion (`status: granted`) MAY coexist with a blocked or escalated constitutional determination; when it does, the decision MUST NOT advance to `legitimized`, MUST NOT execute, and MUST NOT be represented as legitimate without qualification.

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

These axioms are normative. Legitimize MUST NOT treat completion of the procedural checks in Sections 5, 6, and 8 as though it had also satisfied Section 7. The two are evidenced separately and recorded separately.

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
- every material answerability claim MUST be attested and classified under the Answerability Gate defined in Section 7, whatever that classification turns out to be;
- no unresolved blocking conditions under Section 8 may remain.

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

### 7.1 Claim Classification

Before a decision can be legitimized, the legitimacy record MUST carry `unresolved_answerability_claim_refs` and MUST set `constitutional_legitimacy_status`.

`unresolved_answerability_claim_refs` lists every material answerability claim — affected-party claim, sovereignty claim, denial of recognized standing, or appeal — that touches this decision and has not been fully closed as `resolved`. Each entry MUST carry a `claim_ref` and a `claim_status` drawn from:

- `resolved` — the claim received the constitutionally owed answer identified under question 4 of the Answerability Test (`RFC-CDP-033-Standing-and-Recusal-Model.md` Section 11.3) and is closed.
- `preserved_non_blocking` — the claim remains open, but has received a timely, reasoned disposition from an authorized decision-maker; remains visible and contestable; and does not contest the authority or permissibility of the immediate act being legitimized.
- `blocking` — the claim remains open and has not received such a disposition, or it contests the authority or permissibility of the immediate act being legitimized, or it was erased or institutionally denied as defined below.
- `escalated` — the claim has been referred for institutional resolution and constitutional legitimacy is deferred pending that resolution.

An empty `unresolved_answerability_claim_refs` list is a positive claim that no material answerability claim remains open. It MUST be attested, not assumed, in the same manner as `open_dissent_refs`.

An answerability claim MUST be classified `blocking` when it has been **erased** — it existed in the governed path and no longer appears in any referenced record, detected through cross-reference against Breach Records under RFC-CDP-072 or other independent evidence — or **institutionally denied** — the responding institution rejected it without the rationale, review authority, and contestability path required by RFC-CDP-070 or RFC-CDP-074. A claim that was raised, remains visible, and received no institutional response within the response window required by `RFC-CDP-070-Appeals-and-Contestability-Model.md` is **ignored** and MUST also be classified `blocking`.

The Answerability Gate applies the Answerability Test to every claim referenced by the decision. A claim MUST NOT be classified `resolved` or `preserved_non_blocking` on the strength of Answerability Test questions 1 through 3 alone; that classification requires a visible, adequate answer to question 4.

### 7.2 Constitutional Legitimacy Status

`constitutional_legitimacy_status` MUST be one of `preserved`, `blocked`, or `escalated`, determined as follows:

- `preserved` — every entry in `unresolved_answerability_claim_refs` is classified `resolved` or `preserved_non_blocking`, and no material answerability claim tied to this decision has been erased, ignored, or institutionally denied.
- `blocked` — at least one entry is classified `blocking`.
- `escalated` — no entry is classified `blocking`, and at least one entry is classified `escalated`.

`preserved` requires more than an intact record. A claim's disposition counts toward `preserved` only when it is visible, was answered within the required window, carries reasoned disposition, was decided by an actor with authority to decide it, remains contestable, and — where a remedy or further escalation is owed — identifies that remedy or escalation path. A record that merely notes an objection without these elements is not preserved; it is `blocking`.

### 7.3 Relationship to Procedural Legitimacy

`constitutional_legitimacy_status` is determined independently of `status`. Section 8 governs whether `status` may be `granted`; this section governs `constitutional_legitimacy_status` on its own terms. A `blocking` classification does not by itself prevent Legitimize from recording procedural completion — it is entirely possible for a governed path to satisfy every procedural check in Section 8 while an answerability claim was erased or improperly denied in a way procedural record-presence checks cannot detect. That combination — `status: granted` with `constitutional_legitimacy_status: blocked` — is a valid and expected output of this protocol, not an error state. Section 11 defines what that combination permits and forbids.

Legitimize MUST record both `status` and `constitutional_legitimacy_status`. Neither substitutes for the other, and a decision MUST NOT be presented as constitutionally legitimate on the strength of `status: granted` alone.

---

## 8. Blocking Conditions

Legitimize MUST NOT set `status: granted` when any of the following conditions are true:

1. `proposal_sufficiency_ref` is null or points to a record with `sufficiency_status` other than `sufficient` or `excepted`.
2. APC is required for the decision and `apc_gate_result_refs` is empty.
3. A required APC gate result has `passed: false`, `unknown`, unresolved criteria, or no valid exception.
4. Any unresolved blocking ordinary Challenge exists in `challenge_refs`.
5. Any unresolved Formation Challenge exists in `formation_challenge_refs`.
6. The Decision Lifecycle Envelope has `standing_status` other than `valid`, unless an explicit emergency exception is invoked, recorded, and subject to post-hoc review.
7. `unresolved_answerability_claim_refs` is absent when required, or contains an entry without a valid `claim_status` under Section 7.1.

These are hard stops on procedural legitimacy.

Appeals and affected-party claims are not listed here. They are answerability claims, and their substantive disposition — whether they are `resolved`, `preserved_non_blocking`, `blocking`, or `escalated` — is governed exclusively by Section 7, which determines `constitutional_legitimacy_status`, not `status`. Condition 7 above requires only that every such claim be attested and classified; it does not require any particular classification. An implementation that permits `status: granted` while condition 7 is unmet, or that infers `constitutional_legitimacy_status` from these conditions rather than from Section 7, is non-compliant with this RFC.

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
  unresolved_answerability_claim_refs:
    - claim_ref: <ref>
      claim_status: <resolved|preserved_non_blocking|blocking|escalated>
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

`unresolved_answerability_claim_refs` may be empty on the same terms as `open_dissent_refs`: an empty list is a positive, attested claim that no material answerability claim remains open, erased, ignored, or institutionally denied. When non-empty, every entry MUST carry a `claim_status` classified under Section 7.1. An entry with a missing or invalid `claim_status` trips Blocking Condition 7 in Section 8.

`status: granted` reflects procedural legitimacy only. It MUST NOT be read as also establishing constitutional legitimacy; `constitutional_legitimacy_status` is the field that does that, and it is evidenced separately, and MAY be `blocked` or `escalated` even when `status` is `granted`. See Section 11 for the permitted combinations and what each one authorizes.

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

### 11.1 Permitted Status Combinations

`status` and `constitutional_legitimacy_status` are set independently, per Section 7.3. Not every combination is meaningful. The permitted combinations, and what each authorizes, are:

| `status` | `constitutional_legitimacy_status` | Meaning | Envelope effect |
|---|---|---|---|
| `granted` | `preserved` | Procedural and constitutional legitimacy both hold. | MAY transition to `legitimized`. |
| `granted` | `blocked` | Procedural checks in Section 8 passed, but a material answerability claim is erased, ignored, or institutionally denied. | MUST NOT transition to `legitimized`. MUST NOT execute. MUST NOT be represented as legitimate without express qualification that constitutional legitimacy is blocked. MUST transition to `escalated`. |
| `granted` | `escalated` | Procedural checks passed; a material answerability claim has been referred for institutional resolution. | MUST NOT transition to `legitimized` or execute pending resolution. Envelope transitions to `escalated`. |
| `denied` | `blocked` | Procedural legitimacy failed under Section 8, and the same governed path independently shows an erased, ignored, or institutionally denied answerability claim. | Transitions to `legitimacy_denied`. Recorded for completeness; the decision does not proceed on either basis. |
| `escalated` | `escalated` | Both procedural and constitutional questions are under institutional escalation. | Transitions to `escalated`. Requires resolution of both before any further status. |

`status: denied` combined with `constitutional_legitimacy_status: preserved` MUST NOT be recorded: if procedural legitimacy fails, constitutional legitimacy cannot be certified as preserved on that same governed path.

The envelope MUST NOT advance to `legitimized` unless `status: granted` AND `constitutional_legitimacy_status: preserved`. `status: granted` alone reflects only procedural legitimacy under Section 3 and MUST NOT be treated as sufficient to advance the envelope.

When `status: granted` and `constitutional_legitimacy_status` is `blocked` or `escalated`, the legitimacy record MUST still be persisted under Section 10 so the procedural determination is not lost, but the envelope MUST remain at `adjudicated` or advance only to `escalated`, never to `legitimized`.

Legitimacy does not authorize execution by itself unless execution authority and execution conditions are separately satisfied under RFC-CDP-046. Execution authority under RFC-CDP-046 additionally requires `constitutional_legitimacy_status: preserved`; `status: granted` alone MUST NOT be treated as sufficient authorization to execute.

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
  "unresolved_answerability_claim_refs": [
    {
      "claim_ref": "ref",
      "claim_status": "resolved | preserved_non_blocking | blocking | escalated"
    }
  ],
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

`status` MUST fail (`denied`) or escalate when:

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
- `unresolved_answerability_claim_refs` is missing or contains an unclassified entry;
- time bounds or safety constraints are violated.

`constitutional_legitimacy_status` MUST be `blocked` or `escalated`, independent of `status`, when:

- an affected-party claim, appeal, or sovereignty claim classified `blocking` under Section 7.1 exists;
- a material answerability claim has been erased, ignored, or institutionally denied;
- a repair condition classified `blocking` remains unresolved.

These conditions govern `constitutional_legitimacy_status` rather than `status`; see Section 11.1 for what each resulting combination permits.

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

Promoted into Draft v0.7, following review that found the v0.6 gate design internally inconsistent:

- `claim_status` classification (`resolved`, `preserved_non_blocking`, `blocking`, `escalated`) for every entry in `unresolved_answerability_claim_refs`, replacing a flat, unclassified list;
- appeals and unresolved affected-party claims removed from the hard procedural Blocking Conditions in Section 8 and folded into the Answerability Gate's classification, so that not every open claim freezes procedural completion, while claims that are erased, ignored, contest the immediate act's authority, or lack a reasoned authorized disposition still force `constitutional_legitimacy_status: blocked`;
- Blocking Conditions narrowed to seven purely procedural checks plus a presence-and-classification check, decoupled from the substantive content of answerability claims;
- `status: granted` with `constitutional_legitimacy_status: blocked` established as a valid, expected, and non-contradictory output, with an explicit table of permitted `status` / `constitutional_legitimacy_status` combinations and their envelope and execution effects (Section 11.1);
- `preserved` given an operational definition requiring visibility, a timely response, reasoned disposition, an authorized decision-maker, contestability, and identified remedy or escalation where owed — not mere record preservation;
- Question 4 of the Answerability Test (consumed from RFC-CDP-033) tied explicitly to an identified obligor, recipient, authority source, and response window.

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

A record of an objection is not an answer to it. Preservation without a timely, reasoned, authorized, and contestable disposition is not preservation of constitutional legitimacy — it is a well-organized record of a claim that was still, in substance, ignored.
