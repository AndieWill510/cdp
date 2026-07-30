# RFC-CDP-078 — Relationship Taxonomy and Recognition Model

Author: Kevin “Andie” Williams  
Status: Draft v0.3  
Series: Constitutional Decision Plane (CDP)  
Date: July 30, 2026  
Updates: RFC-CDP-078 v0.2  
Depends On: RFC-CDP-001, RFC-CDP-032, RFC-CDP-033, RFC-CDP-045, RFC-CDP-074, RFC-CDP-092  
Related: RFC-CDP-070, RFC-CDP-071, RFC-CDP-073

## Abstract

CDP already asks whether an actor has standing (`RFC-CDP-033`), what authority an actor holds (`RFC-CDP-032`), whether authority originates outside the institution (`RFC-CDP-074`), and what became of a relationship after Repair (`RFC-CDP-092`). None of these ask what *kind* of relationship existed between the parties in the first place.

This RFC defines **Relationship Type** as a constitutional fact distinct from standing, authority, sovereignty, and disposition. The kind of relationship a governed act arises within shapes what answer is owed, what repair pathways are appropriate, and what obligations may survive a relationship's conclusion or separation.

Relationship Type is an explanatory layer, not a gateway. The gateway is Answerability: whether a consequence-bearing relationship exists, under `RFC-CDP-001` Section 5.1 and the Answerability Test in `RFC-CDP-033` Section 11.3. That determination does not require, and MUST NOT be made to wait for, agreement on what *kind* of relationship it was. Relationship Type explains the character of an obligation that Answerability has already established; it does not decide whether that obligation exists. A dispute over Relationship Type MUST NOT suspend, delay, diminish, or defeat Standing, Answerability, Legitimacy, or Repair. Otherwise a respondent could convert a question about how to describe a relationship into a reason to delay answering for what was done within it.

CDP does not create relationship types and does not adjudicate their substantive meaning. It recognizes a classification, sourced from law, agreement, custom, ceremony, community authority, or self-identification, and uses that classification to inform — never to gate — the answerability, standing, and repair questions governed elsewhere.

---

## 1. Purpose

This RFC answers:

- what a Relationship Type is, and how it differs from standing, authority, sovereignty, and disposition;
- why Relationship Type MUST NOT function as a gateway or jurisdictional prerequisite for Standing, Answerability, Legitimacy, or Repair;
- a canonical, non-exhaustive taxonomy of relationship types;
- how a relationship type is claimed, recognized, and contested;
- how relationship type informs, without determining or gating, the Answerability Test (`RFC-CDP-033` Section 11.3), the Answerability Gate (`RFC-CDP-045` Section 7), and Relationship Disposition (`RFC-CDP-092` Section 13);
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

### 2.1 Taxonomy Litigation

A second, related failure mode is **taxonomy litigation**: a respondent using a dispute over Relationship Type itself to delay or avoid answering for the underlying conduct.

Taxonomy litigation occurs when:

- a respondent denies that a claimed relationship type applies, and treats that denial as though it also defeats the claimant's Standing or Answerability;
- an institution declines to respond substantively while a Relationship Type Claim remains contested, treating classification as a precondition it must resolve before it can answer at all;
- a Repair process pauses pending resolution of what to call the relationship, rather than proceeding on the answerability the relationship already established;
- months or years are spent arguing whether a relationship was fiduciary, contractual, or something else, while the question of what was actually done goes unanswered.

Taxonomy litigation is more dangerous than flattening, because it does not need to succeed to work. A respondent who never wins the classification argument can still benefit enormously from making CDP wait on it. Section 8 states the constitutional principle that closes this: Relationship Type is never the gateway, so there is nothing to win by arguing it.

---

## 3. Core Principle

Relationship type is not standing. Relationship type is not authority. Relationship type is not sovereignty. Relationship type is not disposition. Relationship type is not the gateway.

The gateway is Answerability. `RFC-CDP-001` Section 5.1 establishes the constitutional primitive: power becomes answerable when it enters a consequence-bearing relationship. `RFC-CDP-033` Section 11.3 tests for that primitive directly — what governed act, what consequence, what relationship creates answerability — without asking what to call the relationship. Fiduciary, contractual, kinship, therapeutic, and every other entry in Section 5's taxonomy are ways of describing a consequence-bearing relationship after Answerability has already identified one. They are not additional facts that must be established before Answerability applies.

A **Relationship Type** is the socially, legally, culturally, or ceremonially recognized character of the relationship between the parties to a governed act — the frame that explains what is ordinarily owed within that kind of relationship, independent of any single decision made inside it. It explains an obligation Answerability has already established. It does not decide whether that obligation exists.

CDP does not create relationship types. It recognizes a claimed or evidenced classification and preserves it as a fact relevant to answerability and repair, on the same terms established for standing in `RFC-CDP-033`: existence does not depend on recognition, and recognition does not manufacture what it recognizes.

Relationship Type is a constitutional fact about the relationship. A Relationship Type Claim, and the recognition status attached to it, is a constitutional *record* — what CDP presently knows, has been told, or has procedurally recognized. The two MUST NOT be conflated. A claim can be wrong. A recognition can be withheld, delayed, or denied. Neither of those failures changes what the relationship actually was, and neither of them pauses Answerability. Section 8 states that rule directly.

---

## 4. Relationship to Existing RFCs

This dependency runs one way. `RFC-CDP-033`, `RFC-CDP-045`, and `RFC-CDP-092` do not depend on this RFC and do not require a resolved Relationship Type to operate; each of them establishes its own determination — standing, legitimacy, disposition — on grounds this RFC does not supply. This RFC depends on them: it takes the consequence-bearing relationship they already recognize and adds an explanatory account of its character. Section 8 makes this direction of dependency a normative rule, not merely a description.

### 4.1 RFC-CDP-033 Standing and Recusal Model

Standing determines whether an actor may participate in a decision stage. Standing and the Answerability Test do not require a Relationship Type. Relationship Type informs, but does not determine or gate, what answer is owed under question 4 of the Answerability Test — it supplies the context of ordinary duty that makes an owed answer specific rather than generic, once questions 1 through 3 have already established that answerability exists.

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
| `indigenous_sovereignty` | Records that the relationship is governed by or implicates Indigenous sovereignty. This value is a routing marker only; it is not a classification of the sovereignty itself. `RFC-CDP-074` exclusively governs the sovereignty claim, its authority, and its meaning. |
| `contractual` | Duties are bounded by the terms of an agreement between parties presumed to bargain at arm's length. |
| `educational` | Duties arise from a teaching, mentoring, or institutional-learning relationship. |
| `therapeutic` | Duties arise from a care, healing, or clinical relationship and MAY carry heightened confidentiality and non-abandonment expectations. |
| `friendship` | Duties are informal and self-defined by the parties; CDP records the claim without imposing external duty content. |
| `governance` | Duties arise from a governing or governed relationship between an authority and those subject to or represented by it. |
| `guardianship` | Duties arise from responsibility for a dependent party's welfare and ordinarily survive the specific decision or proceeding. |
| `other` | A claimed type not enumerated above. A `type_description` SHOULD be provided. |
| `unclassified` | No relationship type has yet been claimed or assessed. |

Normative constraints on the taxonomy:

- Multiple relationship types MAY apply simultaneously to the same parties (an employment relationship that is also fiduciary, for example). Section 7 requires each to carry its own recognition status rather than sharing one status across the whole claim.
- A relationship type MAY change over time and MAY itself be contested.
- CDP MUST NOT treat this table as defining the substantive content of any relationship type. The table names illustrative duty character for routing purposes only; it does not supply the law, custom, ceremony, or agreement that actually governs the relationship.
- `indigenous_sovereignty` in particular MUST NOT be read as CDP's classification of a sovereignty claim. It only marks that a claim under `RFC-CDP-074` is implicated; that RFC's status values, not this taxonomy, govern the claim's substance.

---

## 6. Existence, Claim, and Recognition

CDP treats Relationship Type as three separate questions, mirroring the existence, recognition, and scope distinction established for Standing in `RFC-CDP-033` Section 11.2.

**Existence** asks whether a relationship of a given type in fact holds between the parties. Existence is a fact about the relationship. It does not depend on CDP, on any actor's approval, or on institutional process. This is a narrower question than the existence question the Answerability Test asks under `RFC-CDP-033` Section 11.3: that test asks whether a consequence-bearing relationship exists at all, and is answered independently of this one. A Relationship Type's existence may remain unsettled while the underlying answerability relationship's existence is already settled.

**Claim** asks what relationship type an actor asserts. A claim is not thereby true merely for being asserted, and CDP's role is to preserve and route the claim, not to adjudicate whether it correctly describes the world, except where a specific downstream RFC (most often `RFC-CDP-074` for sovereignty-adjacent types) assigns that adjudication.

**Recognition** asks whether CDP has procedurally acknowledged a claimed relationship type for the purpose of routing answerability and repair questions. Recognition is what CDP does. It can be granted promptly, delayed, wrongly withheld, or denied outright, and a wrongful denial of recognition does not erase the underlying relationship it fails to recognize.

Denial is a distinct, governed determination, not a synonym for silence or contest. Section 7 requires it to be representable in its own right — with its own authority basis, rationale, and review path — precisely so that a relationship type CDP wrongly refuses to recognize does not collapse into the same record state as one nobody has yet raised a question about.

Non-recognition MUST NOT be treated as proof that no relationship of the claimed type exists. A sustained claim MUST NOT be treated as proof that CDP's recognition created the relationship. Absence of contest MUST NOT be treated as recognition; Section 10 governs that boundary.

---

## 7. Relationship Type Claim Object

A Relationship Type Claim SHOULD be represented as a structured object. Because multiple relationship types MAY apply simultaneously (Section 5), and each MAY reach a different recognition outcome, recognition is tracked per asserted type, not once for the whole claim:

```json
{
  "relationship_type_claim_id": "rtc_20260730_001",
  "claimant_ref": "actor_or_party_ref",
  "counterparty_refs": ["actor_or_party_ref"],
  "claim_text": "string",
  "evidence_refs": [],
  "restricted_evidence_refs": [],
  "type_assertions": [
    {
      "relationship_type": "employment",
      "type_description": "string|null",
      "basis": ["law", "custom", "ceremony", "agreement", "self_identification", "community_authority", "other"],
      "recognition_status": "asserted",
      "contest_refs": [],
      "denial": null,
      "sovereignty_claim_ref": null
    }
  ],
  "authority_basis_ref": "ref|null",
  "record_controls": {
    "access_level": "public | restricted | confidential | community_controlled",
    "redaction_required": false,
    "cultural_protocol_required": false,
    "public_summary_allowed": true
  },
  "created_at": "timestamp"
}
```

### 7.1 Type Assertions

`type_assertions` MUST contain at least one entry. Each entry MUST carry a `relationship_type` drawn from Section 5, or `other` with a `type_description` provided, and its own `recognition_status`.

`recognition_status` MUST be one of:

- `asserted` — the assertion has been submitted or recorded. It does not mean CDP or the responding institution has accepted, resolved, or adjudicated it.
- `acknowledged` — receipt is recorded. Acknowledgment is not agreement.
- `provisionally_recognized` — the assertion may be used for routing answerability and repair questions pending fuller review, on the terms Section 10 defines.
- `recognized` — the assertion has been procedurally acknowledged as a basis for routing. It MUST NOT be read as a determination that the assertion is legally, factually, or culturally conclusive beyond that routing purpose.
- `contested` — a party has raised a live contest as to this specific assertion. `contested` describes the existence of an active contest; it is not itself an outcome, and it MUST resolve to one of `recognized`, `recognition_withheld`, `denied`, or `unresolved`.
- `recognition_withheld` — recognition has not been extended and is deferred or paused pending further evidence or process, without an affirmative governed denial.
- `denied` — a governed recognition determination has affirmatively refused recognition. `denied` MUST carry a `denial` object under Section 7.2. `denied` MUST NOT be inferred from silence, delay, or the mere existence of a contest.
- `unresolved` — neither recognition nor denial has been reached and the assertion remains materially open.
- `superseded` — a later assertion or agreement replaces this one.
- `withdrawn` — the claimant has withdrawn this assertion. Withdrawal describes the assertion, not the underlying relationship, and does not by itself resolve whatever answerability question the relationship independently raises.

### 7.2 Denial Requirements

When `recognition_status` is `denied`, the type assertion MUST carry a `denial` object:

```json
{
  "denied_by": "actor_or_authority_ref",
  "authority_basis_ref": "ref",
  "rationale": "string",
  "review_ref": "ref|null",
  "denied_at": "timestamp"
}
```

A denial MUST preserve the underlying assertion unchanged. Denial removes recognition; it does not remove the record of what was claimed, who claimed it, or on what basis.

A responding institution MUST NOT be the sole reviewer of its own denial where the assertion is sovereignty-adjacent under `RFC-CDP-074` or affected-party-adjacent under `RFC-CDP-073`.

### 7.3 Claim-Level and Assertion-Level Fields

`claimant_ref`, `counterparty_refs`, `claim_text`, `evidence_refs`, and `restricted_evidence_refs` describe the claim as a whole and apply across all of its type assertions.

`sovereignty_claim_ref`, when non-null on a given type assertion, MUST point to a Sovereignty Claim under `RFC-CDP-074`, and that claim's status governs wherever the two conflict. It SHOULD be set on the `indigenous_sovereignty` assertion when present, and MAY be set on others where a sovereignty claim is otherwise implicated.

`restricted_evidence_refs` MUST be handled under the security and cultural-handling requirements of Section 12.

---

## 8. Relationship Type Is Explanatory, Not a Gateway

### 8.1 Answerability Is the Gateway

Governance under this constitutional model has a single gateway: whether a consequence-bearing relationship exists, per `RFC-CDP-001` Section 5.1 and the Answerability Test in `RFC-CDP-033` Section 11.3. That gateway does not require, and MUST NOT be made to require, a resolved Relationship Type. Questions 1 through 3 of the Answerability Test — what governed act, what consequence, what relationship creates answerability — are answerable without knowing what to call the relationship.

Relationship Type answers a later, narrower question: what kind of relationship best explains the character of the obligations that consequence-bearing relationship already created. It is an explanatory layer over an answerability determination made on its own terms, not a precondition for making that determination at all.

### 8.2 Non-Suspension Rule

Relationship Type MUST NOT be used as a jurisdictional prerequisite for Standing, Answerability, Legitimacy, Repair, or continuing obligations.

A dispute, contest, denial, or unresolved status concerning Relationship Type MUST NOT suspend, delay, diminish, or defeat any determination governed by `RFC-CDP-033`, `RFC-CDP-045`, or `RFC-CDP-092`. Those determinations proceed on the existence of the consequence-bearing relationship. They do not wait for agreement on what to call it.

This is deliberate. A respondent facing a claim of harm can always argue that the relationship was not really fiduciary, not really a guardianship, not really what the claimant says it was — Section 10 preserves that argument in full. What it MUST NOT do is convert a dispute about the claimant's account of a relationship's character into a reason to delay answering for the underlying conduct. Taxonomy litigation (Section 2.1) MUST NOT become a substitute for, or a precondition of, answering for what was done.

An implementation that pauses Legitimize, blocks Execute, or defers a Repair determination pending resolution of a Relationship Type Claim, when no other RFC's own conditions independently require that pause, is non-compliant with this RFC.

### 8.3 How Relationship Type Informs Answerability and Repair

Subject to Section 8.2, Relationship Type informs, without substituting for or gating, the constitutional determinations governed elsewhere:

- It informs question 4 of the Answerability Test (`RFC-CDP-033` Section 11.3) by supplying context about the ordinary duties of the claimed relationship type, once questions 1 through 3 have already established that answerability exists. It does not answer question 4 by itself; the test's five questions still apply in full. A type assertion informing this determination SHOULD carry `recognition_status: recognized` or `provisionally_recognized`; a `denied` or `withdrawn` assertion MUST NOT be used to supply that context. Absence of a resolved Relationship Type MUST NOT delay an answer to question 4 that can be given on other grounds.
- It informs which Relationship Disposition values (`RFC-CDP-092` Section 13.1) are coherent outcomes. A relationship type whose duty character does not ordinarily conclude MAY still receive a disposition of `CONCLUDED` or `SEPARATED_WITH_OBLIGATIONS`, but a `RESTORED` or `CONTINUING_WITH_RESERVATIONS` disposition SHOULD be considered before treating the relationship as concludable on ordinary contractual terms.
- It MAY inform the authority basis considered under `RFC-CDP-032`, but it MUST NOT be treated as itself granting or extinguishing authority.

Implementations MUST NOT treat a Relationship Type Claim as a formula that mechanically outputs a required answer, disposition, or authority grant, and MUST NOT treat an unresolved or contested Relationship Type Claim as grounds to withhold a determination that Section 8.2 requires to proceed regardless. It is evidence to be weighed by the process each of those RFCs already governs, not a bypass of — or precondition for — that process.

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

A Relationship Type Claim, and each of its type assertions, MUST be contestable by any party with recognized standing to the decision, breach, or repair process it is attached to, on the same contestability terms as the answerability claims it informs.

A contest MAY address the claimed type, the claimed basis, or the scope of duty implied by the type. A contest MUST NOT be resolved by the responding institution acting as sole adjudicator where the claim is sovereignty-adjacent under `RFC-CDP-074` or affected-party-adjacent under `RFC-CDP-073`.

A contest over a type assertion is a contest over that assertion. It is not, by itself, a contest over Standing, Answerability, Legitimacy, or Repair, and per Section 8.2 it MUST NOT suspend, delay, or condition any determination governed by `RFC-CDP-033`, `RFC-CDP-045`, or `RFC-CDP-092`. A party contesting Relationship Type retains full standing to also contest those other determinations, on their own terms, at the same time.

Absence of contest MAY permit a type assertion to remain `provisionally_recognized` for routing, subject to applicable notice, review, and authority requirements. Absence of contest MUST NOT be treated as concurrence, recognition, waiver, or proof of the claimed type. A party may fail to contest an assertion for reasons that have nothing to do with its correctness: absence, incapacity, intimidation, inaccessible process, lack of notice, or refusal to accept CDP's jurisdiction over the question at all. None of those reasons make the assertion true, and none of them entitle it to move to `recognized` on silence alone.

A contested or previously uncontested assertion remains subject to later contest through appeal or repair channels and MUST NOT be treated as permanently foreclosed.

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
- treat its own summary of a relationship as a substitute for the claimant's or community's own account;
- set, clear, or move a `recognition_status`, including moving an assertion into or out of `denied`;
- treat an uncontested assertion as though it were recognized;
- recommend suspending, delaying, or conditioning a Standing, Answerability, Legitimacy, or Repair determination pending resolution of a Relationship Type Claim.

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

- a Relationship Type Claim record with one or more type assertions;
- `relationship_type` per assertion, drawn from Section 5 or `other`;
- `recognition_status` per assertion, including a distinct `denied` state with its required denial fields;
- contestability per assertion;
- a reference from the relevant standing, legitimacy, or repair record to the applicable Relationship Type Claim;
- record controls sufficient to withhold restricted or ceremonial evidence from public view;
- Standing, Legitimize, and Repair workflows that proceed to their own determinations without checking Relationship Type Claim status as a precondition.

A minimal implementation MUST NOT infer a Relationship Type from institutional convenience, from the absence of a contest, or from the presence of a contract document alone. It MUST NOT collapse `denied` into `contested` or `unresolved`, and it MUST NOT allow `provisionally_recognized` to silently become `recognized` merely because time has passed without a contest. It MUST NOT gate any determination under `RFC-CDP-033`, `RFC-CDP-045`, or `RFC-CDP-092` on Relationship Type Claim resolution.

---

## 14. Summary

Standing asks who may participate. Answerability asks whether power entered a consequence-bearing relationship at all. Authority asks what an actor may do. Sovereignty asks whether authority originates outside the institution. Disposition asks what became of a relationship after Repair.

Relationship Type asks a different question, and it asks it last: what kind of relationship explains the obligations Answerability already found. It is not a gate anything else must pass through. It is an account offered after the gate has already opened.

CDP does not invent what a family, a treaty, a fiduciary duty, or a covenant of guardianship means. It recognizes the claim, preserves it, routes it to the questions that already govern answerability and repair, and refuses to let institutional convenience flatten one kind of relationship into another. It also refuses to let a dispute over that classification become a reason to stop governing. A respondent may argue endlessly about what a relationship should be called. That argument does not buy them a single day's delay in answering for what they did within it.

What the relationship was is a fact. What CDP has been told, and what it has recognized or denied, is a record. Silence keeps that record incomplete. It does not complete it. And an incomplete record of what to call a relationship is never a reason to leave the underlying answerability unaddressed.
