# RFC-CDP-072 — Breach Record and Repair Agenda Schema

Author: Kevin “Andie” Williams  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: May 3, 2026  
Depends On: RFC-CDP-001, RFC-CDP-010, RFC-CDP-020, RFC-CDP-021, RFC-CDP-032, RFC-CDP-047, RFC-CDP-048, RFC-CDP-061, RFC-CDP-071  
Updates: RFC-CDP-071

## Abstract

This RFC defines normative schema structures for breach records, repair agendas, repair points, institutional responses, repair commitments, affected-party review, and completion evidence in CDP.

RFC-CDP-071 defines the Twenty Points Repair Protocol and establishes the constitutional requirement that repair claims be preserved without flattening. This RFC defines the structured objects required to implement that protocol.

The goal is to ensure that historic breach, institutional harm, sovereignty claims, affected-party review, repair commitments, dissent, and completion evidence can be recorded, audited, contested, and learned from without being collapsed into generic stakeholder feedback.

---

## 1. Purpose

This RFC answers:

- how to represent a breach record;
- how to represent a repair agenda;
- how to preserve each repair point distinctly;
- how to represent affected peoples and authority claims;
- how to record institutional responses;
- how to track repair commitments;
- how to record affected-party review;
- how to record completion evidence;
- how to preserve dissent, non-response, delay, and failure;
- how to prevent repair data from becoming decorative metadata.

---

## 2. Core Principle

CDP cannot repair what it cannot remember.

CDP cannot remember what it collapses.

Repair schemas MUST preserve the shape, authority, provenance, numbering, dissent, commitments, and evidence of repair claims.

---

## 3. Relationship to Existing RFCs

### 3.1 RFC-CDP-071 Twenty Points Repair Protocol

RFC-CDP-071 defines the repair protocol and the anti-erasure requirements for enumerated repair agendas.

This RFC provides the formal schemas used by that protocol.

### 3.2 RFC-CDP-032 Authority and Delegation Model

Repair schemas MUST preserve authority claims, including affected-party authority and sovereignty authority.

A responding institution MUST NOT be treated as the only authority over repair validity, sufficiency, or closure.

### 3.3 RFC-CDP-061 Schema Drift and Context Preservation

Repair records are vulnerable to schema drift when repair claims are normalized into ordinary risk notes, stakeholder comments, or sentiment.

This RFC defines structures that preserve repair meaning and context.

### 3.4 RFC-CDP-047 Record Protocol

Breach records, repair agendas, responses, commitments, review records, dissent, and completion evidence are recordable CDP artifacts.

### 3.5 RFC-CDP-048 Learn Protocol

Repair outcomes SHOULD generate learning artifacts, policy updates, schema updates, training guidance, or precedent records.

Learning MUST NOT erase breach history.

---

## 4. Terminology

### 4.1 Breach Record

A **Breach Record** is a structured record of treaty breach, legal breach, policy breach, moral breach, procedural failure, institutional harm, cultural erasure, identity erasure, sovereignty violation, or legitimacy failure.

### 4.2 Repair Agenda

A **Repair Agenda** is an enumerated set of claims, demands, conditions, or requirements offered by an affected party in response to harm, breach, illegitimacy, or structural failure.

### 4.3 Repair Point

A **Repair Point** is one individually preserved item within a Repair Agenda.

A Repair Point MUST NOT be silently merged with another point merely for institutional convenience.

### 4.4 Institutional Response

An **Institutional Response** is a recorded answer, non-answer, deferral, acceptance, rejection, partial acceptance, commitment, or failure by a responding institution.

### 4.5 Repair Commitment

A **Repair Commitment** is a specific promise, duty, resource allocation, policy change, action, or remedy undertaken in response to a Repair Point or Breach Record.

### 4.6 Completion Evidence

**Completion Evidence** is evidence that a Repair Commitment has been fulfilled, failed, deferred, contested, or superseded.

### 4.7 Affected-Party Review

**Affected-Party Review** is review by a materially affected person, community, nation, lineage, class, or authorized representative regarding the accuracy, sufficiency, interpretation, or closure of a repair record.

---

## 5. Breach Record Schema

A Breach Record SHOULD be represented as:

```json
{
  "breach_record_id": "br_20260503_001",
  "record_type": "breach_record",
  "title": "string",
  "summary": "string",
  "breach_types": [
    "treaty",
    "legal",
    "policy",
    "moral",
    "procedural",
    "institutional_harm",
    "cultural_erasure",
    "identity_erasure",
    "sovereignty",
    "other"
  ],
  "status": "alleged | acknowledged | contested | under_review | accepted | rejected | in_repair | completed | failed | superseded",
  "source_context": "string",
  "affected_peoples": [],
  "authority_claims": [],
  "events": [
    {
      "event_id": "event_001",
      "event_type": "act | omission | policy | decision | enforcement | non_response | delay | other",
      "description": "string",
      "occurred_at": "timestamp_or_range",
      "actor_refs": [],
      "institution_refs": [],
      "evidence_refs": []
    }
  ],
  "evidence_refs": [],
  "repair_agenda_refs": [],
  "dissent_refs": [],
  "provenance": {
    "submitted_by": "actor_or_party_ref",
    "submitted_at": "timestamp",
    "source_refs": [],
    "restricted_source_refs": [],
    "public_summary_allowed": true
  },
  "record_controls": {
    "access_level": "public | restricted | confidential | community_controlled",
    "redaction_required": false,
    "affected_party_review_required": true,
    "culturally_sensitive": false
  },
  "metadata": {}
}
```

### 5.1 Required Fields

A Breach Record MUST include:

- `breach_record_id`;
- `record_type`;
- `title`;
- `breach_types`;
- `status`;
- `affected_peoples`;
- `provenance`;
- `record_controls`.

---

## 6. Affected People Schema

Affected peoples SHOULD be represented as:

```json
{
  "affected_party_id": "ap_001",
  "name": "string",
  "party_type": "person | family | lineage | community | nation | class | organization | other",
  "relationship_to_claim": "sovereign_party | affected_party | witness | steward | representative | descendant | other",
  "authority_basis": ["self_attestation", "community_authority", "treaty", "law", "history", "institutional_record", "other"],
  "review_required": true,
  "contact_or_representation_refs": [],
  "sensitivity": {
    "public_name_allowed": true,
    "restricted_details": false,
    "cultural_protocol_required": false
  }
}
```

Affected-party records MUST NOT require disclosure of restricted, ceremonial, confidential, or community-held knowledge merely to prove affected status.

---

## 7. Authority Claim Schema

Authority claims SHOULD be represented as:

```json
{
  "authority_claim_id": "auth_claim_001",
  "claim_type": "institutional | affected_party | sovereignty | treaty | legal | community | repair | other",
  "claimant_ref": "actor_or_party_ref",
  "basis": ["treaty", "law", "policy", "community_authority", "history", "testimony", "record", "other"],
  "scope": {
    "domain": "string",
    "jurisdiction": "string",
    "repair_agenda_refs": [],
    "repair_point_refs": [],
    "decision_refs": []
  },
  "status": "asserted | acknowledged | contested | accepted | rejected | superseded",
  "evidence_refs": [],
  "dissent_refs": []
}
```

Sovereignty claims MUST be preserved as authority claims, not downgraded to stakeholder preferences.

---

## 8. Repair Agenda Schema

A Repair Agenda SHOULD be represented as:

```json
{
  "repair_agenda_id": "ra_20260503_001",
  "record_type": "repair_agenda",
  "title": "string",
  "agenda_type": "twenty_point | enumerated_demands | single_boundary | settlement | policy_repair | community_repair | other",
  "status": "draft | submitted | acknowledged | under_review | contested | in_response | in_repair | completed | failed | superseded | withdrawn",
  "source_context": "string",
  "affected_peoples": [],
  "authority_claims": [],
  "breach_record_refs": [],
  "points": [],
  "record_requirements": {
    "preserve_original_language": true,
    "preserve_numbering": true,
    "allow_dissent": true,
    "affected_party_review_required": true,
    "institutional_response_required": true,
    "completion_evidence_required": true
  },
  "provenance": {
    "submitted_by": "actor_or_party_ref",
    "submitted_at": "timestamp",
    "source_refs": [],
    "restricted_source_refs": []
  },
  "metadata": {}
}
```

### 8.1 Required Fields

A Repair Agenda MUST include:

- `repair_agenda_id`;
- `record_type`;
- `title`;
- `agenda_type`;
- `status`;
- `affected_peoples`;
- `points`;
- `record_requirements`;
- `provenance`.

---

## 9. Repair Point Schema

A Repair Point SHOULD be represented as:

```json
{
  "repair_point_id": "rp_001",
  "repair_agenda_id": "ra_20260503_001",
  "point_number": 1,
  "title": "string",
  "claim_type": "treaty | sovereignty | land | identity | jurisdiction | institutional_repair | record | policy | cultural | resource | other",
  "claim_text": "The claim or demand as preserved.",
  "original_language": "string_or_null",
  "summary": "string",
  "authority_basis": ["treaty", "law", "history", "community_testimony", "institutional_record", "other"],
  "affected_party_refs": [],
  "authority_claim_refs": [],
  "evidence_refs": [],
  "institutional_response_refs": [],
  "repair_commitment_refs": [],
  "affected_party_review_refs": [],
  "dissent_refs": [],
  "repair_status": "unanswered | acknowledged | accepted | accepted_in_part | rejected | deferred | contested | in_repair | completed | failed | withdrawn | superseded",
  "record_controls": {
    "preserve_original_language": true,
    "preserve_numbering": true,
    "may_summarize": true,
    "summary_contestable": true
  },
  "metadata": {}
}
```

### 9.1 Required Fields

A Repair Point MUST include:

- `repair_point_id`;
- `repair_agenda_id`;
- `point_number` when supplied by the source agenda;
- `claim_type`;
- `claim_text`;
- `repair_status`;
- `record_controls`.

### 9.2 Preservation Rule

A Repair Point MUST NOT be merged, renumbered, summarized away, or reclassified without preserving the original point and recording the transformation.

---

## 10. Institutional Response Schema

An Institutional Response SHOULD be represented as:

```json
{
  "institutional_response_id": "ir_001",
  "repair_point_id": "rp_001",
  "responding_institution_ref": "institution_001",
  "response_state": "unanswered | acknowledged | accepted | accepted_in_part | rejected | deferred | contested | in_repair | completed | failed | superseded",
  "response_text": "string",
  "rationale": "string",
  "authority_ref": "authority_grant_or_claim_ref",
  "commitment_refs": [],
  "evidence_refs": [],
  "limitations": [],
  "conditions": [],
  "responded_at": "timestamp",
  "review_required": true,
  "affected_party_review_refs": [],
  "dissent_refs": [],
  "metadata": {}
}
```

Institutional Response MUST support non-response, delay, partial acceptance, contested interpretation, and failure. These are not absence of data; they are recordable states.

---

## 11. Repair Commitment Schema

A Repair Commitment SHOULD be represented as:

```json
{
  "repair_commitment_id": "rc_001",
  "repair_point_id": "rp_001",
  "institutional_response_id": "ir_001",
  "commitment_type": "policy_change | resource | apology | land | jurisdiction | record_correction | access | protection | investigation | compensation | other",
  "description": "string",
  "owner_refs": [],
  "authority_refs": [],
  "resources": {
    "budget": null,
    "staff": [],
    "tools": [],
    "other": []
  },
  "timeline": {
    "committed_at": "timestamp",
    "due_at": "timestamp_or_null",
    "completed_at": null
  },
  "status": "proposed | committed | in_progress | blocked | completed | failed | withdrawn | superseded",
  "dependencies": [],
  "completion_evidence_refs": [],
  "affected_party_review_required": true,
  "metadata": {}
}
```

A Repair Commitment MUST NOT be considered completed without Completion Evidence when completion evidence is required by the Repair Agenda or policy.

---

## 12. Completion Evidence Schema

Completion Evidence SHOULD be represented as:

```json
{
  "completion_evidence_id": "ce_001",
  "repair_commitment_id": "rc_001",
  "evidence_type": "document | policy | payment | transfer | implementation | testimony | audit | inspection | other",
  "summary": "string",
  "evidence_refs": [],
  "submitted_by": "actor_or_party_ref",
  "submitted_at": "timestamp",
  "verification_status": "submitted | verified | contested | rejected | insufficient | superseded",
  "verified_by_refs": [],
  "affected_party_review_refs": [],
  "dissent_refs": [],
  "record_controls": {
    "public_summary_allowed": true,
    "restricted_details": false,
    "redaction_required": false
  }
}
```

Completion Evidence SHOULD be reviewable by affected parties when policy or repair context requires it.

---

## 13. Affected-Party Review Schema

Affected-Party Review SHOULD be represented as:

```json
{
  "affected_party_review_id": "apr_001",
  "reviewer_ref": "affected_party_or_representative_ref",
  "review_target_type": "breach_record | repair_agenda | repair_point | institutional_response | repair_commitment | completion_evidence | summary | closure",
  "review_target_ref": "target_id",
  "review_state": "accepted | accepted_with_reservations | contested | rejected | insufficient_information | no_authority_to_review | deferred",
  "review_text": "string",
  "requested_changes": [],
  "dissent_refs": [],
  "submitted_at": "timestamp",
  "record_controls": {
    "public_summary_allowed": true,
    "restricted_details": false
  }
}
```

Affected-party review MUST NOT be simulated by the responding institution.

---

## 14. Dissent Record Schema

Dissent SHOULD be represented as:

```json
{
  "dissent_id": "dissent_001",
  "dissenting_party_ref": "actor_or_party_ref",
  "target_ref": "record_or_response_ref",
  "dissent_type": "summary_accuracy | authority | evidence | classification | response_sufficiency | closure | cultural_handling | sovereignty | other",
  "statement": "string",
  "evidence_refs": [],
  "submitted_at": "timestamp",
  "status": "submitted | acknowledged | under_review | resolved | unresolved | superseded"
}
```

Dissent MUST remain discoverable even when a repair commitment is completed.

---

## 15. Status Enumerations

### 15.1 Repair Point Status

Repair Point status SHOULD use:

```text
unanswered
acknowledged
accepted
accepted_in_part
rejected
deferred
contested
in_repair
completed
failed
withdrawn
superseded
```

### 15.2 Repair Commitment Status

Repair Commitment status SHOULD use:

```text
proposed
committed
in_progress
blocked
completed
failed
withdrawn
superseded
```

### 15.3 Completion Evidence Status

Completion Evidence verification status SHOULD use:

```text
submitted
verified
contested
rejected
insufficient
superseded
```

---

## 16. Record Requirements

A CDP implementation supporting this RFC SHOULD preserve:

- original repair agenda;
- original numbering;
- original language where legally and ethically permissible;
- public summary where allowed;
- restricted source references where needed;
- affected peoples;
- authority claims;
- breach records;
- repair points;
- institutional responses;
- repair commitments;
- affected-party reviews;
- dissent;
- completion evidence;
- closure disputes;
- learning outcomes.

---

## 17. Anti-Erasure Requirements

Implementations MUST NOT collapse:

```text
Breach Record → risk note
Repair Agenda → stakeholder feedback
Repair Point → sentiment item
Sovereignty Claim → preference
Affected-Party Review → internal approval
Dissent → resolved comment
Non-response → no data
Delay → neutral pending state
Completion Evidence → institution says done
```

Implementations SHOULD preserve these as distinct record types.

---

## 18. Security, Privacy, and Cultural Handling

Repair schemas may contain sensitive cultural, familial, political, legal, ceremonial, or identity information.

Implementations SHOULD support:

- access controls;
- redaction;
- public summaries;
- restricted details;
- affected-party review;
- community-controlled records;
- culturally appropriate handling;
- protection against retaliation;
- provenance without unnecessary exposure;
- audit without universal publication.

A record can be auditable without being universally public.

---

## 19. Learning Closure

Repair schemas SHOULD produce learning artifacts when:

- breach patterns repeat;
- institutional responses fail;
- commitments are not completed;
- affected-party review contests closure;
- repair points require new policy;
- schema drift collapses repair meaning;
- completion evidence is insufficient;
- authority claims are mishandled.

Learning artifacts MAY include:

- policy revision;
- schema revision;
- authority model revision;
- training guidance;
- precedent record;
- new repair point template;
- new affected-party review requirement;
- new anti-erasure control.

Learning MUST NOT erase breach history, dissent, or repair obligations.

---

## 20. Minimal Compliance

A minimal CDP implementation SHOULD support:

- Breach Record;
- Repair Agenda;
- Repair Point;
- Institutional Response;
- Repair Commitment;
- Completion Evidence;
- Affected-Party Review;
- Dissent Record;
- status tracking;
- provenance;
- access controls;
- record references;
- learning output.

A minimal implementation MUST preserve each Repair Point distinctly when an agenda supplies enumerated claims.

---

## 21. Summary

RFC-CDP-071 says repair claims must not be flattened.

This RFC defines the objects that prevent flattening.

Breach Records preserve harm. Repair Agendas preserve the shape of claims. Repair Points preserve distinct demands. Institutional Responses preserve answer and non-answer. Repair Commitments preserve promised action. Completion Evidence preserves whether repair happened. Affected-Party Review preserves legitimacy beyond the responding institution.

Repair is not complete because the institution says so. Repair is complete only when the record, evidence, authority, affected-party review, and learning support closure.
