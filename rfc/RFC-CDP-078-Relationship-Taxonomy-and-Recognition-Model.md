# RFC-CDP-078 — Relationship Taxonomy and Recognition Model

Author: Kevin “Andie” Williams  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: July 30, 2026  
Depends On: RFC-CDP-001, RFC-CDP-032, RFC-CDP-033, RFC-CDP-045, RFC-CDP-074, RFC-CDP-092  
Related: RFC-CDP-070, RFC-CDP-071, RFC-CDP-073

## Abstract

CDP already asks whether an actor has standing (`RFC-CDP-033`), what authority an actor holds (`RFC-CDP-032`), whether authority originates outside the institution (`RFC-CDP-074`), and what became of a relationship after Repair (`RFC-CDP-092`). None of these ask what *kind* of relationship existed between the parties in the first place.

This RFC defines **Relationship Type** as a constitutional fact distinct from standing, authority, sovereignty, and disposition. The kind of relationship a governed act arises within shapes what answer is owed, what repair pathways are appropriate, and what obligations may survive a relationship's conclusion or separation.

CDP does not create relationship types and does not adjudicate their substantive meaning. It recognizes a classification, sourced from law, agreement, custom, ceremony, community authority, or self-identification, and uses that classification to inform — not to determine — the answerability, standing, and repair questions governed elsewhere.

---

## 1. Purpose

This RFC answers:

- what a Relationship Type is, and how it differs from standing, authority, sovereignty, and disposition;
- a canonical, non-exhaustive taxonomy of relationship types;
- how a relationship type is claimed, recognized, and contested;
- how relationship type informs, without determining, the Answerability Test (`RFC-CDP-033` Section 11.3), the Answerability Gate (`RFC-CDP-045` Section 7), and Relationship Disposition (`RFC-CDP-092` Section 13);
- what CDP MUST NOT do with relationship-type information.

---

## 2. Failure Mode: Relationship Flattening

The failure mode this RFC addresses is **relationship flattening**: treating every governed relationship as though it were the same kind of relationship, typically by defaulting to whichever frame is most convenient to the responding institution.

Relationship flattening occurs when:

- a fiduciary breach is treated as an ordinary contract dispute;
- a kinship or guardianship harm is treated as an employment grievance;
- an indigenous sovereignty relationship is treated as a stakeholder relationship — a specific instance of the authority downgrading already named in `RFC-CDP-074`, recurring here at the relationship-classification layer;
- a uniform repair or remedy standard is applied regardless of what the relationship actually obligated the parties to each other;
- an institution selects whichever relationship frame minimizes its own owed duties.

Relationship flattening is not solved by better standing rules, better authority rules, or better repair rules alone. Each of those governs a different question. Flattening happens at the layer beneath all of them: the failure to ask what kind of relationship this was before asking what is owed within it.

---

## 3. Core Principle

Relationship type is not standing. Relationship type is not authority. Relationship type is not sovereignty. Relationship type is not disposition.

A **Relationship Type** is the socially, legally, culturally, or ceremonially recognized character of the relationship between the parties to a governed act — the frame that establishes what is ordinarily owed within that kind of relationship, independent of any single decision made inside it.

CDP does not create relationship types. It recognizes a claimed or evidenced classification and preserves it as a fact relevant to answerability and repair, on the same terms established for standing in `RFC-CDP-033`: existence does not depend on recognition, and recognition does not manufacture what it recognizes.

---

## 4. Relationship to Existing RFCs

### 4.1 RFC-CDP-033 Standing and Recusal Model

Standing determines whether an actor may participate in a decision stage. Relationship Type informs, but does not determine, what answer is owed under question 4 of the Answerability Test — it supplies the context of ordinary duty that makes an owed answer specific rather than generic.

### 4.2 RFC-CDP-032 Authority and Delegation Model

Authority determines what an actor may do. Relationship Type may inform the scope or duty implied by an authority grant — a fiduciary authority carries duties a bare contractual authorization does not — but Relationship Type does not itself grant, extend, or extinguish authority.

### 4.3 RFC-CDP-074 Sovereignty Claims and Authority Pluralism

Sovereignty claims and indigenous or community relationship types overlap substantially. This RFC MUST NOT be used to reclassify, narrow, or adjudicate a sovereignty claim. Wherever a relationship type claim is also a sovereignty claim, `RFC-CDP-074` governs, and `RFC-CDP-074` controls in the event of any conflict between the two.

### 4.4 RFC-CDP-092 Repair State Machine

Relationship Disposition (`RFC-CDP-092` Section 13) describes what became of a relationship after Repair. Relationship Type describes what kind of relationship it was before, during, and after — relevant to which disposition values are even coherent for it. An employment relationship may reasonably reach `CONCLUDED`; a guardianship or kinship relationship's obligations do not ordinarily conclude merely because a governed process closes.

### 4.5 RFC-CDP-071 Twenty Points Repair Protocol and RFC-CDP-073 Affected-Party Review

Where a relationship type is asserted as part of an enumerated repair agenda or an anti-erasure claim, this RFC's classification is preserved as claimed under those RFCs' existing preservation and anti-erasure requirements. It is not adjudicated de novo by institutional response.

---

## 5. Relationship Type Taxonomy

The following taxonomy is illustrative and non-exhaustive. Implementations, communities, and policy profiles MAY extend it.

| Relationship Type | Illustrative Duty Character |
|---|---|
| `fiduciary` | Duty of loyalty and care ordinarily survives the specific transaction and constrains self-interested action. |
| `employment` | Duties are bounded by role, term, and applicable labor law or agreement. |
| `kinship` | Duties arise from family, lineage, or community relation and are not ordinarily created or dissolved by institutional process. |
| `treaty` | Duties arise from a negotiated instrument between peoples, nations, or sovereign parties. |
| `indigenous_sovereignty` | Authority and duty arise from a people's own governance, law, or ceremony, not from the responding institution. Governed jointly with `RFC-CDP-074`. |
| `contractual` | Duties are bounded by the terms of an agreement between parties presumed to bargain at arm's length. |
| `educational` | Duties arise from a teaching, mentoring, or institutional-learning relationship. |
| `therapeutic` | Duties arise from a care, healing, or clinical relationship and MAY carry heightened confidentiality and non-abandonment expectations. |
| `friendship` | Duties are informal and self-defined by the parties; CDP records the claim without imposing external duty content. |
| `governance` | Duties arise from a governing or governed relationship between an authority and those subject to or represented by it. |
| `guardianship` | Duties arise from responsibility for a dependent party's welfare and ordinarily survive the specific decision or proceeding. |
| `other` | A claimed type not enumerated above. `disposition_rationale`-equivalent description SHOULD be provided. |
| `unclassified` | No relationship type has yet been claimed or assessed. |

Normative constraints on the taxonomy:

- Multiple relationship types MAY apply simultaneously to the same parties (an employment relationship that is also fiduciary, for example).
- A relationship type MAY change over time and MAY itself be contested.
- CDP MUST NOT treat this table as defining the substantive content of any relationship type. The table names illustrative duty character for routing purposes only; it does not supply the law, custom, ceremony, or agreement that actually governs the relationship.

---

## 6. Existence, Claim, and Recognition

CDP treats Relationship Type as three separate questions, mirroring the existence, recognition, and scope distinction established for Standing in `RFC-CDP-033` Section 11.2.

**Existence** asks whether a relationship of a given type in fact holds between the parties. Existence is a fact about the relationship. It does not depend on CDP, on any actor's approval, or on institutional process.

**Claim** asks what relationship type an actor asserts. A claim is not thereby true merely for being asserted, and CDP's role is to preserve and route the claim, not to adjudicate whether it correctly describes the world, except where a specific downstream RFC (most often `RFC-CDP-074` for sovereignty-adjacent types) assigns that adjudication.

**Recognition** asks whether CDP has procedurally acknowledged a claimed relationship type for the purpose of routing answerability and repair questions. Recognition is what CDP does. It can be granted promptly, delayed, wrongly withheld, or denied outright, and a wrongful denial of recognition does not erase the underlying relationship it fails to recognize.

Non-recognition MUST NOT be treated as proof that no relationship of the claimed type exists. A sustained claim MUST NOT be treated as proof that CDP's recognition created the relationship.

---

## 7. Relationship Type Claim Object

A Relationship Type Claim SHOULD be represented as a structured object:

```json
{
  "relationship_type_claim_id": "rtc_20260730_001",
  "claimed_types": ["fiduciary", "kinship"],
  "claimant_ref": "actor_or_party_ref",
  "counterparty_refs": ["actor_or_party_ref"],
  "basis": ["law", "custom", "ceremony", "agreement", "self_identification", "community_authority", "other"],
  "claim_text": "string",
  "evidence_refs": [],
  "restricted_evidence_refs": [],
  "recognition_status": "asserted | acknowledged | recognized | contested | disputed | unresolved | superseded",
  "contest_refs": [],
  "authority_basis_ref": "ref|null",
  "sovereignty_claim_ref": "ref|null",
  "record_controls": {
    "access_level": "public | restricted | confidential | community_controlled",
    "redaction_required": false,
    "cultural_protocol_required": false,
    "public_summary_allowed": true
  },
  "created_at": "timestamp"
}
```

`claimed_types` MUST include at least one value from Section 5 or `other`.

`recognition_status: asserted` means the claim has been submitted or recorded. It does not mean CDP or the responding institution has accepted, resolved, or adjudicated the claim.

`recognition_status: recognized` means the claim has been procedurally acknowledged as a basis for routing answerability and repair questions under this RFC. It MUST NOT be read as a determination that the claim is legally, factually, or culturally conclusive beyond that routing purpose.

`sovereignty_claim_ref` MAY be null. When non-null, it MUST point to a Sovereignty Claim under `RFC-CDP-074`, and that claim's status governs wherever the two conflict.

`restricted_evidence_refs` MUST be handled under the security and cultural-handling requirements of Section 12.

---

## 8. How Relationship Type Informs Answerability and Repair

Relationship Type informs, without substituting for, the constitutional determinations governed elsewhere:

- It informs question 4 of the Answerability Test (`RFC-CDP-033` Section 11.3) by supplying context about the ordinary duties of the claimed relationship type. It does not answer question 4 by itself; the test's five questions still apply in full.
- It informs which Relationship Disposition values (`RFC-CDP-092` Section 13.1) are coherent outcomes. A relationship type whose duty character does not ordinarily conclude MAY still receive a disposition of `CONCLUDED` or `SEPARATED_WITH_OBLIGATIONS`, but a `RESTORED` or `CONTINUING_WITH_RESERVATIONS` disposition SHOULD be considered before treating the relationship as concludable on ordinary contractual terms.
- It MAY inform the authority basis considered under `RFC-CDP-032`, but it MUST NOT be treated as itself granting or extinguishing authority.

Implementations MUST NOT treat a Relationship Type Claim as a formula that mechanically outputs a required answer, disposition, or authority grant. It is evidence to be weighed by the process each of those RFCs already governs, not a bypass of that process.

---

## 9. Non-Appropriation and Anti-Flattening Requirements

This RFC MUST NOT be used to appropriate, simulate, or finally define ceremonial, kinship, or indigenous-sovereignty relationship content.

A CDP implementation using this RFC MUST NOT:

- require disclosure of restricted or ceremonial knowledge to preserve a relationship type claim;
- treat a claimed relationship type as invalid merely because it is not independently verifiable in institutional records;
- let institutional convenience determine which of several plausible relationship types applies;
- allow the responding institution to unilaterally reclassify a relationship type without affected-party or community concurrence where such concurrence is required by policy, law, or `RFC-CDP-074`;
- treat public information about a relationship as sufficient to override a restricted or community-controlled claim about its type.

CDP MAY help structure and route relationship type claims. CDP MUST NOT claim ownership over what a family, a treaty, a fiduciary duty, or a covenant of guardianship means.

---

## 10. Contestability

A Relationship Type Claim MUST be contestable by any party with recognized standing to the decision, breach, or repair process it is attached to, on the same contestability terms as the answerability claims it informs.

A contest MAY address the claimed type, the claimed basis, or the scope of duty implied by the type. A contest MUST NOT be resolved by the responding institution acting as sole adjudicator where the claim is sovereignty-adjacent under `RFC-CDP-074` or affected-party-adjacent under `RFC-CDP-073`.

An uncontested Relationship Type Claim becomes stable for the decision or repair item it is attached to. It remains subject to later contest through appeal or repair channels and MUST NOT be treated as permanently foreclosed.

---

## 11. AIITL Boundaries

AIITL MAY:

- surface a possible relationship-type mismatch, for example flagging that a matter is being processed as contractual when the record suggests a fiduciary or guardianship relationship;
- identify where a Relationship Type Claim is missing entirely;
- identify where a claimed type's ordinary duty character appears inconsistent with the disposition or remedy being proposed.

AIITL MUST NOT:

- determine, assign, or resolve a contested relationship type;
- infer a ceremonial, kinship, or indigenous-sovereignty relationship type from public records alone;
- treat absence of institutional recognition as evidence against a claimed type;
- treat its own summary of a relationship as a substitute for the claimant's or community's own account.

---

## 12. Security, Privacy, and Cultural Handling

Relationship Type Claims may reveal familial, cultural, therapeutic, financial, or ceremonial information.

Implementations MUST support:

- restricted records and community-controlled access;
- redaction;
- public summaries with restricted details withheld;
- culturally appropriate handling protocols;
- protection against retaliation;
- non-public evidence references;
- review without forced disclosure of restricted or ceremonial material.

A record can be auditable without being universally public.

---

## 13. Minimal Compliance

A minimal CDP implementation SHOULD support:

- a Relationship Type Claim record;
- `claimed_types` drawn from Section 5 or `other`;
- `recognition_status`;
- contestability;
- a reference from the relevant standing, legitimacy, or repair record to the applicable Relationship Type Claim;
- record controls sufficient to withhold restricted or ceremonial evidence from public view.

A minimal implementation MUST NOT infer a Relationship Type from institutional convenience, from the absence of a contest, or from the presence of a contract document alone.

---

## 14. Summary

Standing asks who may participate. Authority asks what an actor may do. Sovereignty asks whether authority originates outside the institution. Disposition asks what became of a relationship after Repair.

Relationship Type asks a different, prior question: what kind of relationship this was.

CDP does not invent what a family, a treaty, a fiduciary duty, or a covenant of guardianship means. It recognizes the claim, preserves it, routes it to the questions that already govern answerability and repair, and refuses to let institutional convenience flatten one kind of relationship into another.
