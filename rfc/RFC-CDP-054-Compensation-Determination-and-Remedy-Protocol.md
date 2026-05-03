# RFC-CDP-054 — Compensation Determination and Remedy Protocol

Author: Kevin “Andie” Williams  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: May 3, 2026  
Depends On: RFC-CDP-001, RFC-CDP-010, RFC-CDP-032, RFC-CDP-047, RFC-CDP-048, RFC-CDP-053, RFC-CDP-061, RFC-CDP-071, RFC-CDP-072, RFC-CDP-073, RFC-CDP-074  
Updates: RFC-CDP-053

## Abstract

This RFC defines the Compensation Determination and Remedy Protocol for the Constitutional Decision Plane (CDP).

RFC-CDP-053 defines when compensation may be required and how compensation is tracked alongside rollback and mitigation. This RFC defines the actual mechanism by which compensation is claimed, assessed, proposed, reviewed, authorized, delivered, contested, evaluated for sufficiency, recorded, and learned from.

Compensation is not whatever the responding institution is willing to offer. Compensation is a contested remedy process with authority, evidence, affected-party review, resource authorization, delivery, sufficiency review, and residual-harm handling.

---

## 1. Purpose

This RFC answers:

- how compensation is initiated;
- how harm is assessed;
- how remedies are proposed;
- who may determine or authorize remedies;
- how affected parties review proposed remedies;
- how resources are authorized;
- how remedies are delivered;
- how remedy sufficiency is evaluated;
- how residual harm is preserved;
- how refusal, impossibility, partial compensation, or contested remedy is recorded;
- how compensation produces learning without erasing harm.

---

## 2. Core Principle

Compensation is not institutional generosity.

Compensation is a governed response to harm, breach, loss, burden, misclassification, exclusion, erasure, rights impact, or failed execution when rollback is impossible, incomplete, unsafe, or insufficient.

Compensation MUST be reviewable, contestable, attributable, authorized, recorded, and evaluated for sufficiency.

---

## 3. Relationship to Existing RFCs

### 3.1 RFC-CDP-053 Rollback and Compensation Protocol

RFC-CDP-053 defines triggers and tracking for rollback, compensation, and mitigation.

This RFC defines the compensation mechanism.

### 3.2 RFC-CDP-072 Breach Record and Repair Agenda Schema

Compensation may satisfy or partially satisfy Repair Commitments, Completion Evidence, or Repair Points.

This RFC defines compensation-specific remedy objects that may link to those records.

### 3.3 RFC-CDP-073 Affected-Party Review and Anti-Erasure

Affected parties may review, contest, accept, reject, or reserve judgment on remedy proposals and sufficiency.

### 3.4 RFC-CDP-074 Sovereignty Claims and Authority Pluralism

Compensation affecting sovereignty claims, land, jurisdiction, cultural material, or community authority MUST preserve authority pluralism and review requirements.

---

## 4. Compensation Lifecycle

The canonical compensation lifecycle is:

```text
HARM_IDENTIFIED
  → COMPENSATION_CLAIMED
  → HARM_ASSESSED
  → REMEDY_PROPOSED
  → AFFECTED_PARTY_REVIEW
  → REMEDY_DETERMINED
  → RESOURCE_AUTHORIZED
  → REMEDY_DELIVERED
  → SUFFICIENCY_REVIEW
  → RECORDED
  → LEARNED
```

The lifecycle may branch into contested, partial, impossible, refused, reopened, escalated, or residual-harm states.

---

## 5. Terminology

### 5.1 Compensation Claim

A **Compensation Claim** is a request, assertion, or determination that compensation may be owed.

### 5.2 Harm Assessment

A **Harm Assessment** is a structured evaluation of what harm occurred, who or what was affected, what caused it, whether rollback is possible, and what remedies may be appropriate.

### 5.3 Remedy

A **Remedy** is a proposed or authorized action intended to address harm.

Remedies may include restoration, resource transfer, monetary compensation, record correction, access correction, policy change, protection, apology, service, support, land/resource return, jurisdictional correction, or other appropriate action.

### 5.4 Remedy Determination

A **Remedy Determination** is the governed decision selecting or authorizing one or more remedies.

### 5.5 Resource Authorization

**Resource Authorization** is the authority to commit funds, labor, access, policy changes, institutional duties, or other resources required to deliver a remedy.

### 5.6 Remedy Delivery

**Remedy Delivery** is the execution of an authorized remedy.

### 5.7 Sufficiency Review

**Sufficiency Review** evaluates whether delivered remedy adequately addresses the harm under the relevant authority, evidence, affected-party review, and repair context.

### 5.8 Residual Harm

**Residual Harm** is harm that remains after rollback, mitigation, or compensation.

Residual harm MUST NOT be erased merely because a remedy was delivered.

---

## 6. Compensation Claim Object

A Compensation Claim SHOULD be represented as:

```json
{
  "compensation_claim_id": "cc_20260503_001",
  "claim_type": "execution_harm | rollback_failure | breach | misclassification | exclusion | delay | exposure | cultural_harm | sovereignty | repair | other",
  "decision_id": "decision_123",
  "execution_ref": "execution_456",
  "rollback_ref": "rollback_or_null",
  "repair_point_refs": [],
  "breach_record_refs": [],
  "sovereignty_claim_refs": [],
  "claimed_by": "actor_or_party_ref",
  "affected_party_refs": [],
  "harm_summary": "string",
  "basis": "string",
  "evidence_refs": [],
  "urgency": "low | medium | high | emergency",
  "status": "submitted | acknowledged | under_review | accepted_for_process | rejected_for_process | contested | superseded",
  "record_controls": {
    "access_level": "public | restricted | confidential | community_controlled",
    "redaction_required": false,
    "affected_party_review_required": true
  },
  "created_at": "timestamp"
}
```

---

## 7. Harm Assessment Object

A Harm Assessment SHOULD be represented as:

```json
{
  "harm_assessment_id": "ha_20260503_001",
  "compensation_claim_id": "cc_20260503_001",
  "assessment_type": "initial | revised | independent | affected_party | institutional | expert | community | other",
  "assessed_by": "actor_or_party_ref",
  "authority_ref": "authority_claim_or_grant_ref",
  "harm_types": [
    "financial",
    "access",
    "rights",
    "identity",
    "reputation",
    "safety",
    "privacy",
    "cultural",
    "jurisdictional",
    "sovereignty",
    "emotional",
    "operational",
    "other"
  ],
  "severity": "low | medium | high | critical",
  "causal_chain_refs": [],
  "affected_party_refs": [],
  "evidence_refs": [],
  "rollback_possible": true,
  "rollback_sufficient": false,
  "mitigation_required": false,
  "compensation_required": true,
  "residual_harm_expected": true,
  "uncertainty": {
    "known_limits": [],
    "unknowns": [],
    "confidence": "low | medium | high"
  },
  "status": "draft | submitted | contested | accepted_for_process | superseded",
  "created_at": "timestamp"
}
```

---

## 8. Remedy Proposal Object

A Remedy Proposal SHOULD be represented as:

```json
{
  "remedy_proposal_id": "rp_20260503_001",
  "compensation_claim_id": "cc_20260503_001",
  "harm_assessment_id": "ha_20260503_001",
  "proposed_by": "actor_or_party_ref",
  "remedy_types": [
    "restoration",
    "monetary",
    "resource",
    "record_correction",
    "access_correction",
    "policy_change",
    "protection",
    "service",
    "apology",
    "land_or_resource_return",
    "jurisdictional_correction",
    "other"
  ],
  "description": "string",
  "scope": {
    "affected_party_refs": [],
    "repair_point_refs": [],
    "sovereignty_claim_refs": [],
    "records_to_correct": [],
    "systems_to_update": []
  },
  "resources_required": {
    "budget": null,
    "staff": [],
    "authority_refs": [],
    "time": "string",
    "other": []
  },
  "delivery_plan_refs": [],
  "review_required": true,
  "affected_party_review_refs": [],
  "status": "proposed | under_review | contested | revised | withdrawn | superseded",
  "metadata": {}
}
```

---

## 9. Remedy Determination Object

A Remedy Determination SHOULD be represented as:

```json
{
  "remedy_determination_id": "rd_20260503_001",
  "compensation_claim_id": "cc_20260503_001",
  "selected_remedy_proposal_refs": [],
  "determined_by": "actor_or_body_ref",
  "authority_ref": "authority_grant_or_claim_ref",
  "determination_type": "accepted | accepted_in_part | rejected | deferred | contested | escalated",
  "rationale": "string",
  "conditions": [],
  "affected_party_review_refs": [],
  "dissent_refs": [],
  "resource_authorization_required": true,
  "status": "draft | issued | contested | superseded",
  "created_at": "timestamp"
}
```

A Remedy Determination MUST NOT erase rejected or contested remedy proposals.

---

## 10. Resource Authorization Object

A Resource Authorization SHOULD be represented as:

```json
{
  "resource_authorization_id": "rauth_20260503_001",
  "remedy_determination_id": "rd_20260503_001",
  "authorized_by": "actor_or_body_ref",
  "authority_ref": "authority_grant_ref",
  "resources_authorized": {
    "budget": null,
    "staff": [],
    "systems": [],
    "access_changes": [],
    "policy_changes": [],
    "other": []
  },
  "constraints": [],
  "validity": {
    "effective_at": "timestamp",
    "expires_at": "timestamp_or_null"
  },
  "status": "authorized | denied | partial | expired | revoked | superseded",
  "record_refs": []
}
```

Resource Authorization MUST be distinct from Remedy Determination when policy requires separate financial, operational, legal, or community authority.

---

## 11. Remedy Delivery Object

Remedy Delivery SHOULD be represented as:

```json
{
  "remedy_delivery_id": "rdel_20260503_001",
  "remedy_determination_id": "rd_20260503_001",
  "resource_authorization_id": "rauth_20260503_001",
  "delivered_by": "actor_or_system_ref",
  "delivery_type": "payment | access_change | record_correction | service | policy_change | transfer | apology | protection | other",
  "delivery_summary": "string",
  "delivered_at": "timestamp_or_null",
  "evidence_refs": [],
  "affected_party_review_required": true,
  "status": "pending | in_progress | delivered | partially_delivered | failed | refused | contested | superseded",
  "residual_harm": {
    "expected": true,
    "summary": "string",
    "residual_harm_refs": []
  },
  "record_refs": []
}
```

---

## 12. Sufficiency Review Object

A Sufficiency Review SHOULD be represented as:

```json
{
  "sufficiency_review_id": "sr_20260503_001",
  "remedy_delivery_id": "rdel_20260503_001",
  "reviewed_by": "affected_party_or_authorized_reviewer_ref",
  "review_type": "affected_party | institutional | independent | community | expert | other",
  "review_state": "sufficient | sufficient_with_reservations | insufficient | contested | refused | deferred | no_authority_to_review",
  "review_text": "string",
  "remaining_harm": "string",
  "requested_changes": [],
  "additional_remedy_required": false,
  "dissent_refs": [],
  "submitted_at": "timestamp",
  "record_controls": {
    "public_summary_allowed": true,
    "restricted_details": false
  }
}
```

Sufficiency Review MUST NOT be simulated by the responding institution when affected-party review is required.

---

## 13. Compensation States

Compensation status SHOULD use:

```text
harm_identified
claimed
acknowledged
under_review
harm_assessed
remedy_proposed
contested
remedy_determined
resource_authorized
resource_denied
in_delivery
delivered
partially_delivered
failed
refused
sufficiency_review
sufficient
sufficient_with_reservations
insufficient
residual_harm
closed
reopened
learned
```

`delivered` is not necessarily `sufficient`.

`refused` is not necessarily `resolved`.

`resource_denied` is not necessarily `not owed`.

---

## 14. Affected-Party Review Requirements

Affected-party review SHOULD be required for:

- harm assessment;
- remedy proposal;
- remedy determination;
- remedy delivery;
- sufficiency review;
- residual harm;
- closure.

Affected parties MAY accept, reject, contest, defer, refuse, or accept with reservations.

A refusal to accept a remedy MUST NOT automatically erase the compensation obligation. The reason for refusal SHOULD be recorded where appropriate.

---

## 15. Authority Requirements

CDP implementations SHOULD distinguish:

- authority to submit compensation claim;
- authority to assess harm;
- authority to propose remedy;
- authority to determine remedy;
- authority to authorize resources;
- authority to deliver remedy;
- authority to review sufficiency;
- authority to close compensation.

The same actor SHOULD NOT hold all compensation authorities in high-impact or contested cases.

---

## 16. Sovereignty and Repair Considerations

When compensation implicates sovereignty claims, land, jurisdiction, cultural material, treaty, community authority, or repair agenda, CDP MUST preserve:

- sovereignty claim refs;
- affected-party or sovereign-party review;
- authority conflict refs;
- restricted evidence controls;
- non-appropriation requirements;
- dissent;
- residual harm.

Compensation MUST NOT be used to purchase silence unless the affected party or sovereign authority explicitly agrees under a legitimate and reviewable process.

---

## 17. Closure Rules

Compensation closure SHOULD require:

- compensation claim disposition;
- harm assessment;
- remedy determination;
- resource authorization disposition;
- delivery record;
- sufficiency review where required;
- residual harm disposition;
- dissent preservation;
- learning path.

Compensation MUST NOT be closed merely because a remedy was offered.

Compensation MUST NOT be closed merely because a remedy was delivered if sufficiency is contested.

---

## 18. Failure Modes

CDP implementations SHOULD distinguish:

- harm assessment contested;
- remedy proposal insufficient;
- remedy determination contested;
- resource authorization denied;
- resource authorization partial;
- remedy delivery failed;
- remedy delivery refused;
- remedy delivered but insufficient;
- residual harm remains;
- sovereignty conflict unresolved;
- affected-party review absent;
- institutional self-grading;
- compensation closure contested.

---

## 19. Record Requirements

CDP implementations SHOULD record:

- compensation claim;
- harm assessment;
- remedy proposals;
- remedy determination;
- resource authorization;
- remedy delivery;
- affected-party review;
- sufficiency review;
- dissent;
- residual harm;
- closure disposition;
- learning artifacts.

Compensation records MUST preserve rejected, contested, partial, refused, and insufficient outcomes.

---

## 20. Learning Hooks

Compensation SHOULD trigger Learn when:

- compensation claim is accepted for process;
- harm assessment reveals policy defect;
- remedy is contested;
- resource authorization is denied;
- delivery fails;
- sufficiency is contested;
- residual harm remains;
- compensation exposes recurring breach;
- affected-party review identifies erasure;
- sovereignty conflict affects remedy.

Learning artifacts MAY include:

- remedy precedent;
- compensation policy update;
- authority model update;
- resource authorization rule;
- affected-party review requirement;
- repair agenda update;
- rollback policy update;
- training guidance.

Learning MUST NOT erase harm, dissent, residual obligations, or rejected proposals.

---

## 21. Minimal Compliance

A minimal CDP implementation SHOULD support:

- Compensation Claim;
- Harm Assessment;
- Remedy Proposal;
- Remedy Determination;
- Resource Authorization;
- Remedy Delivery;
- Sufficiency Review;
- residual harm;
- affected-party review flag;
- dissent references;
- learning hook.

A minimal implementation MUST NOT treat remedy offer, remedy delivery, or institutional approval as compensation sufficiency when review is required.

---

## 22. Summary

Compensation requires a mechanism.

Harm must be claimed or identified. Harm must be assessed. Remedy must be proposed. Affected parties must be able to review. Resources must be authorized. Remedy must be delivered. Sufficiency must be evaluated. Residual harm must be preserved. Learning must follow.

Compensation is not whatever the institution is willing to offer. Compensation is a governed remedy process.
