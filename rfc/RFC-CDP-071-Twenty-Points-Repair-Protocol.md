# RFC-CDP-013: Twenty Points Repair Protocol

**Status:** Draft 0.1  
**Category:** Standards Track / Constitutional Repair  
**Author:** Andie Williams, with AI-in-the-Loop contribution  
**Created:** 2026-05-03  
**Context:** Informed by discussion of the Trail of Broken Treaties and the Twenty Points  
**Depends On:** RFC-CDP-000, RFC-CDP-001, RFC-CDP-003, RFC-CDP-005, RFC-CDP-006, RFC-CDP-008, RFC-CDP-009, RFC-CDP-010, RFC-CDP-011  

---

## 1. Abstract

This RFC defines the **Twenty Points Repair Protocol** for the Constitutional Decision Plane (CDP).

The protocol establishes a structured way for CDP systems to handle historic grievance, treaty breach, institutional harm, sovereignty claims, and repair demands without flattening them into ordinary stakeholder feedback.

The name references the discipline of enumerated demands embodied by the Twenty Points advanced during the Trail of Broken Treaties. This RFC does not claim to restate, replace, interpret, or own those demands. Instead, it learns from their constitutional form: when legitimacy has failed, affected peoples may need to bring a numbered, public, auditable repair agenda to institutions that have repeatedly broken trust.

The Twenty Points Repair Protocol gives CDP a formal mechanism for:

- receiving enumerated repair claims;
- preserving each claim as a distinct point;
- mapping each point to duties, authorities, evidence, and affected peoples;
- preventing premature compromise or summary;
- recording institutional response;
- tracking repair commitments over time.

---

## 2. Motivation

CDP is a constitutional control plane. If it can only govern future decisions while leaving historic breach unmodeled, it is incomplete.

Many institutional decisions occur in the shadow of prior harm:

- broken treaties;
- forced removal;
- land theft;
- cultural suppression;
- identity erasure;
- administrative violence;
- medical, legal, educational, or welfare-system harm;
- ignored testimony;
- failed consultation;
- procedural delay used as denial.

Ordinary decision workflows tend to collapse these histories into generic risk notes, stakeholder comments, or legal constraints. That is not enough.

When harm is structural, the repair agenda must be structural. When a community brings twenty points, five demands, seven conditions, or one sacred non-negotiable boundary, CDP MUST preserve the shape of that claim.

---

## 3. Non-Appropriation Requirement

This protocol MUST NOT be used to appropriate Indigenous struggle, ceremonial knowledge, treaty claims, or community demands.

A CDP implementation using this protocol MUST:

1. identify affected peoples and communities;
2. distinguish public source material from restricted, ceremonial, confidential, or community-held knowledge;
3. avoid converting living claims into decorative governance language;
4. preserve attribution and provenance;
5. allow affected communities to contest summaries, mappings, and response records;
6. avoid treating historic demands as merely symbolic;
7. avoid replacing political, legal, or sovereign claims with technical process.

CDP MAY help structure repair work. CDP MUST NOT claim ownership over the repair.

---

## 4. Terminology

### 4.1 Repair Agenda

A **Repair Agenda** is an enumerated set of claims, demands, conditions, or requirements offered by an affected party in response to harm, breach, illegitimacy, or structural failure.

### 4.2 Repair Point

A **Repair Point** is one individually preserved item within a Repair Agenda.

A Repair Point MUST NOT be silently merged with another point merely for institutional convenience.

### 4.3 Breach Record

A **Breach Record** is a record of treaty breach, legal breach, policy breach, moral breach, procedural failure, or legitimacy failure.

### 4.4 Affected People

An **Affected People** is a community, nation, group, class, family, lineage, or person materially affected by the decision, breach, or repair process.

### 4.5 Sovereignty Claim

A **Sovereignty Claim** is a claim that authority does not originate solely inside the responding institution.

Sovereignty claims MUST be preserved as authority claims, not downgraded to stakeholder preferences.

---

## 5. Repair Agenda Object

A Repair Agenda SHOULD be represented as a structured object.

```json
{
  "repair_agenda_id": "ra_20260503_001",
  "title": "Twenty Points Repair Agenda",
  "source_context": "Trail of Broken Treaties / Twenty Points discussion",
  "status": "draft",
  "affected_peoples": [
    {
      "name": "community_or_people_name",
      "relationship_to_claim": "sovereign_party | affected_party | witness | steward"
    }
  ],
  "points": [
    {
      "point_number": 1,
      "title": "Point title",
      "claim_type": "treaty | sovereignty | land | identity | jurisdiction | institutional_repair | record | other",
      "claim_text": "The claim or demand as preserved.",
      "authority_basis": ["treaty", "law", "history", "community testimony"],
      "evidence_refs": [],
      "institutional_response_required": true,
      "repair_status": "unanswered"
    }
  ],
  "record_requirements": {
    "preserve_original_language": true,
    "preserve_numbering": true,
    "allow_dissent": true,
    "affected_party_review_required": true
  }
}
```

---

## 6. Normative Requirements

A CDP-compliant implementation of this protocol:

1. MUST preserve each Repair Point as a distinct record.
2. MUST preserve original numbering when supplied.
3. MUST preserve original language where legally and ethically permissible.
4. MUST identify affected peoples and authority claims.
5. MUST distinguish sovereignty claims from ordinary stakeholder input.
6. MUST record institutional response to each point.
7. MUST allow affected parties to contest summaries and mappings.
8. MUST record non-response, delay, deferral, denial, partial acceptance, and repair commitments.
9. MUST support dissent records.
10. MUST NOT collapse repair demands into generic sentiment analysis.
11. MUST NOT treat repair as completed without recorded evidence.
12. MUST NOT let the responding institution be the sole judge of legitimacy.

---

## 7. Relationship to CDP Lifecycle

### 7.1 Propose

A Repair Agenda may enter CDP as a proposal, but it SHOULD be marked as a repair-class proposal.

Repair-class proposals require heightened preservation of original claims and affected-party authority.

### 7.2 Challenge

Any affected party MAY challenge:

- summary accuracy;
- point classification;
- authority mapping;
- evidence selection;
- institutional response;
- closure status;
- proposed repair sufficiency.

Challenges MUST be recorded.

### 7.3 Test

Repair Points SHOULD be tested against:

- historical record;
- treaty or legal record;
- affected-party testimony;
- institutional archives;
- public commitments;
- prior decisions;
- outcome evidence.

Testing MUST NOT be used to erase testimony merely because institutional archives are incomplete.

### 7.4 Adjudicate

Adjudication MUST distinguish:

- factual disputes;
- legal disputes;
- sovereignty disputes;
- moral claims;
- institutional accountability claims;
- repair feasibility claims.

### 7.5 Legitimize

A repair decision is not legitimate merely because an institution accepts its own response.

Legitimacy SHOULD require affected-party review, challenge opportunity, record completeness, and explicit treatment of authority.

### 7.6 Execute

Repair execution MUST be tracked as commitments, owners, timelines, resources, and completion evidence.

### 7.7 Record

The Record Protocol MUST preserve the original agenda, point mappings, responses, dissent, commitments, and evidence of completion or failure.

### 7.8 Learn

The Learn Protocol MUST update institutional policy, schema, training, and future decision pathways based on repair outcomes.

Learning MUST NOT erase breach history.

---

## 8. Twenty-Point Pattern

The Twenty-Point Pattern is a general CDP pattern for enumerated repair agendas.

It applies when:

- affected parties present a numbered list of demands;
- the list is part of a constitutional, treaty, legal, or institutional repair context;
- each point carries independent meaning;
- institutional response must be tracked point-by-point;
- aggregation would distort accountability.

The pattern is not limited to twenty items. The number is historically resonant, not technically fixed.

---

## 9. Institutional Response States

Each Repair Point SHOULD have one of the following response states:

| State | Meaning |
|---|---|
| `unanswered` | No substantive response recorded |
| `acknowledged` | Institution acknowledges receipt but has not answered |
| `accepted` | Institution accepts the point |
| `accepted_in_part` | Institution accepts part of the point |
| `rejected` | Institution rejects the point |
| `deferred` | Institution delays response |
| `contested` | Interpretation, authority, evidence, or remedy is disputed |
| `in_repair` | Repair commitment is active |
| `completed` | Repair evidence recorded and reviewable |
| `failed` | Institution failed to complete repair |
| `withdrawn` | Claim withdrawn by authorized affected party |
| `superseded` | Replaced by later agenda or agreement |

---

## 10. Anti-Erasure Requirements

CDP MUST avoid the following failure modes:

- converting demands into vague values;
- treating consultation as consent;
- treating delay as neutrality;
- treating silence as closure;
- treating institutional archive absence as proof of no harm;
- treating sovereign parties as stakeholders only;
- treating repair as public relations;
- treating ceremony, identity, or belonging as data decoration;
- treating enumeration as a checklist to minimize rather than a record to answer.

---

## 11. Security and Safety Considerations

Repair records may contain sensitive cultural, legal, familial, political, or identity information.

Implementations MUST support:

- access controls;
- redaction;
- affected-party review;
- culturally appropriate handling;
- provenance;
- dissent;
- non-public evidence references;
- protection against retaliation.

A record can be auditable without being universally public.

---

## 12. Summary

The Twenty Points Repair Protocol gives CDP a way to receive historic and structural repair claims without flattening them.

It makes repair agendas:

- enumerated;
- preserved;
- contestable;
- authority-aware;
- sovereignty-aware;
- recordable;
- actionable;
- reviewable over time.

CDP cannot repair what it cannot remember. It cannot remember what it collapses. This protocol preserves the points.
