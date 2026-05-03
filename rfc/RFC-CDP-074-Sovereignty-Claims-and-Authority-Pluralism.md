# RFC-CDP-074 — Sovereignty Claims and Authority Pluralism

Author: Kevin “Andie” Williams  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: May 3, 2026  
Depends On: RFC-CDP-001, RFC-CDP-010, RFC-CDP-032, RFC-CDP-047, RFC-CDP-061, RFC-CDP-071, RFC-CDP-072, RFC-CDP-073  
Updates: RFC-CDP-032, RFC-CDP-071, RFC-CDP-072, RFC-CDP-073

## Abstract

This RFC defines Sovereignty Claims and Authority Pluralism for the Constitutional Decision Plane (CDP).

A sovereignty claim asserts that relevant authority does not originate solely inside the responding institution, platform, agency, organization, model operator, or system owner. CDP MUST preserve such claims as authority claims, not downgrade them to stakeholder preference, sentiment, consultation input, or ordinary dissent.

Authority pluralism recognizes that multiple authority systems may coexist, overlap, conflict, or remain unresolved. CDP does not resolve all sovereignty disputes. It preserves them, routes them, records their status, prevents erasure, and blocks illegitimate closure when unresolved authority claims are material.

---

## 1. Purpose

This RFC answers:

- what a sovereignty claim is;
- how sovereignty claims differ from ordinary stakeholder input;
- how authority pluralism is represented;
- how CDP records competing authority claims;
- when sovereignty claims block closure or execution;
- how institutional response must treat non-institutional authority;
- how affected-party review interacts with sovereignty;
- how CDP avoids appropriating, resolving, or flattening sovereign authority it does not hold.

---

## 2. Core Principle

Some authority does not originate inside the institution using CDP.

A CDP implementation MUST NOT treat institutional legibility as the source of all legitimacy.

Sovereignty claims MUST be preserved as authority claims.

CDP may structure, record, route, challenge, and preserve sovereignty claims. CDP MUST NOT claim to own, extinguish, simulate, or finally adjudicate sovereign authority unless such authority has been explicitly delegated through a legitimate process.

---

## 3. Relationship to Existing RFCs

### 3.1 RFC-CDP-032 Authority and Delegation Model

RFC-CDP-032 defines sovereignty authority as an authority type that does not originate solely inside the responding institution.

This RFC formalizes how such authority claims are represented, reviewed, contested, and preserved.

### 3.2 RFC-CDP-071 Twenty Points Repair Protocol

RFC-CDP-071 requires sovereignty claims to be preserved as authority claims, not downgraded to stakeholder preferences.

This RFC defines the process for doing so.

### 3.3 RFC-CDP-072 Breach Record and Repair Agenda Schema

RFC-CDP-072 defines Authority Claim objects and related repair schemas.

This RFC adds sovereignty-specific fields, status semantics, and closure rules.

### 3.4 RFC-CDP-073 Affected-Party Review and Anti-Erasure

RFC-CDP-073 defines review and anti-erasure requirements.

This RFC defines sovereignty downgrading as a material anti-erasure violation.

---

## 4. Terminology

### 4.1 Sovereignty Claim

A **Sovereignty Claim** is a claim that authority over a decision, repair agenda, record, land, people, cultural matter, jurisdiction, identity, resource, ceremony, law, history, or obligation does not originate solely inside the responding institution.

### 4.2 Authority Pluralism

**Authority Pluralism** is the condition in which multiple authority systems coexist, overlap, conflict, or remain unresolved.

Examples include institutional authority, community authority, treaty authority, legal authority, ceremonial authority, family or lineage authority, professional authority, technical authority, and affected-party authority.

### 4.3 Responding Institution

A **Responding Institution** is the organization, agency, platform, system owner, model operator, company, or governance body responding to a decision, breach, repair claim, or sovereignty claim.

### 4.4 Sovereign Party

A **Sovereign Party** is a nation, people, community, government, or recognized authority asserting that relevant authority exists outside or alongside the responding institution.

CDP does not determine sovereign status merely by recording a party as sovereign. It records the claim, basis, contestation, and authority relationships.

### 4.5 Authority Conflict

An **Authority Conflict** occurs when two or more authority claims produce incompatible requirements, scopes, decisions, closure rules, or execution conditions.

### 4.6 Authority Downgrading

**Authority Downgrading** occurs when a sovereignty claim or affected-party authority claim is represented as ordinary stakeholder input, preference, sentiment, public comment, or consultation feedback.

Authority downgrading is an anti-erasure violation.

---

## 5. Sovereignty Claim Schema

A Sovereignty Claim SHOULD be represented as:

```json
{
  "sovereignty_claim_id": "sc_20260503_001",
  "claim_type": "sovereignty_claim",
  "claimant": {
    "claimant_ref": "party_or_actor_ref",
    "claimant_type": "nation | people | community | government | lineage | family | organization | other",
    "public_name_allowed": true
  },
  "authority_basis": [
    "treaty",
    "law",
    "customary_law",
    "community_authority",
    "ceremonial_authority",
    "history",
    "land_relationship",
    "self_determination",
    "affected_party_authority",
    "other"
  ],
  "scope": {
    "domains": [],
    "jurisdictions": [],
    "lands_or_places": [],
    "peoples_or_communities": [],
    "repair_agenda_refs": [],
    "repair_point_refs": [],
    "breach_record_refs": [],
    "decision_refs": [],
    "restricted_knowledge": false
  },
  "claim_text": "string",
  "summary": "string",
  "evidence_refs": [],
  "restricted_evidence_refs": [],
  "status": "asserted | acknowledged | contested | under_review | accepted_for_process | rejected_for_process | unresolved | superseded",
  "responding_institution_refs": [],
  "authority_conflict_refs": [],
  "affected_party_review_refs": [],
  "dissent_refs": [],
  "record_controls": {
    "access_level": "public | restricted | confidential | community_controlled",
    "redaction_required": false,
    "cultural_protocol_required": false,
    "public_summary_allowed": true
  },
  "created_at": "timestamp",
  "metadata": {}
}
```

### 5.1 Required Fields

A Sovereignty Claim MUST include:

- `sovereignty_claim_id`;
- `claim_type`;
- `claimant`;
- `authority_basis`;
- `scope`;
- `claim_text` or protected source reference;
- `status`;
- `record_controls`.

---

## 6. Sovereignty Claim Status

Sovereignty Claim status SHOULD use:

```text
asserted
acknowledged
contested
under_review
accepted_for_process
rejected_for_process
unresolved
superseded
```

### 6.1 Asserted

`asserted` means the claim has been submitted or recorded.

It does not mean the responding institution has accepted, resolved, or adjudicated the claim.

### 6.2 Acknowledged

`acknowledged` means the responding institution or CDP process acknowledges receipt and preservation of the claim.

Acknowledgment is not agreement.

### 6.3 Accepted for Process

`accepted_for_process` means the claim is accepted as procedurally relevant and must be carried through review, response, or repair handling.

It does not necessarily mean the responding institution concedes the entire substance of the claim.

### 6.4 Rejected for Process

`rejected_for_process` means the responding institution refuses to treat the claim as procedurally relevant.

Such rejection MUST include rationale and MUST be contestable.

### 6.5 Unresolved

`unresolved` means the claim remains material and unresolved.

Unresolved sovereignty claims MAY block closure or execution depending on scope, risk, and policy.

---

## 7. Authority Conflict Schema

An Authority Conflict SHOULD be represented as:

```json
{
  "authority_conflict_id": "ac_20260503_001",
  "conflict_type": "jurisdiction | closure | execution | record | repair | evidence | access | cultural_protocol | other",
  "claims": [
    {
      "claim_ref": "authority_or_sovereignty_claim_ref",
      "claimant_ref": "party_or_actor_ref",
      "claim_status": "asserted | acknowledged | contested | accepted_for_process | unresolved"
    }
  ],
  "conflict_summary": "string",
  "affected_records": [],
  "affected_decisions": [],
  "affected_repair_points": [],
  "severity": "informational | material | blocking | repair_required",
  "default_action": "record | review | defer | challenge | block_closure | block_execution | escalate | repair",
  "resolution_status": "open | under_review | partially_resolved | resolved | unresolved | superseded",
  "resolution_refs": [],
  "dissent_refs": [],
  "created_at": "timestamp"
}
```

Authority conflicts MUST be recorded when material authority claims cannot be simultaneously satisfied.

---

## 8. Process Requirements

When a sovereignty claim is submitted or identified, CDP SHOULD:

1. record the claim without downgrading it;
2. identify claimant, scope, authority basis, and record controls;
3. distinguish public and restricted material;
4. identify affected decisions, repair points, breach records, or execution requests;
5. check for authority conflicts;
6. determine whether affected-party or sovereign-party review is required;
7. determine whether execution, closure, summary, or institutional response must be deferred;
8. record institutional acknowledgment or refusal;
9. preserve dissent;
10. produce learning when schema or authority handling must change.

---

## 9. Closure and Execution Blocking

A material sovereignty claim SHOULD block closure when:

- the claim concerns the repair point being closed;
- affected-party or sovereign-party review is required but absent;
- institutional response downgrades the claim to preference or stakeholder feedback;
- completion evidence is disputed by a sovereign or affected party;
- the responding institution claims sole authority over closure despite unresolved authority conflict;
- closure would erase breach history, authority basis, or dissent.

A material sovereignty claim SHOULD block execution when:

- execution would affect land, jurisdiction, community, cultural material, identity, rights, or repair obligations within the claim scope;
- required review is absent;
- authority conflict is unresolved;
- execution would expose restricted knowledge;
- execution would create irreversible harm;
- the Presence Grant or execution authority ignores the sovereignty claim.

---

## 10. Non-Appropriation Requirements

CDP MUST NOT use sovereignty-claim records to appropriate, simulate, or replace sovereign authority.

Implementations MUST NOT:

- treat recorded sovereignty as consent;
- treat consultation as delegation;
- treat public information as unrestricted authority;
- require disclosure of restricted or ceremonial knowledge to preserve a claim;
- convert sovereign authority into stakeholder sentiment;
- let institutional formatting determine sovereign legitimacy;
- allow AIITL to impersonate sovereign voice or community authority;
- treat lack of institutional recognition as automatic invalidity;
- treat unresolved authority conflict as closure.

---

## 11. Institutional Response Requirements

A responding institution SHOULD respond to a sovereignty claim with:

- acknowledgment of receipt;
- procedural status;
- whether it accepts the claim for process;
- what authority it claims for its own response;
- what it contests;
- what it cannot determine;
- what review, consultation, or affected-party process is required;
- whether execution or closure is deferred;
- what record controls apply;
- what repair or learning actions are triggered.

Institutional response MUST NOT be the only record of the sovereignty claim.

---

## 12. AIITL Boundaries

AIITL MAY help:

- detect possible authority downgrading;
- identify unresolved authority conflict;
- distinguish sovereignty claim from stakeholder preference;
- summarize public materials with uncertainty;
- recommend affected-party or sovereign-party review;
- flag closure or execution risks;
- preserve dissent records.

AIITL MUST NOT:

- claim to speak for a sovereign party;
- infer consent from public records;
- determine final sovereignty status;
- convert restricted knowledge into summary;
- waive review rights;
- close sovereignty claims;
- treat institutional recognition as the only source of authority;
- treat its own summary as community consent.

AIITL MAY say:

```text
This appears to be an authority claim, not ordinary stakeholder input.
This sovereignty claim may need to be preserved before closure.
This institutional response appears to downgrade authority to preference.
This issue may require review by the affected or sovereign party.
```

---

## 13. Record Requirements

CDP implementations SHOULD preserve:

- original sovereignty claim;
- authority basis;
- claimant reference;
- affected records and repair points;
- public and restricted evidence references;
- institutional responses;
- authority conflicts;
- affected-party or sovereign-party reviews;
- dissent;
- closure or execution blocks;
- learning artifacts.

Records MUST preserve unresolved authority claims as unresolved, not silently close them.

---

## 14. Security, Privacy, and Cultural Handling

Sovereignty claims may involve sensitive cultural, political, legal, familial, ceremonial, or geographic information.

Implementations SHOULD support:

- restricted records;
- community-controlled access;
- redaction;
- public summaries with restricted details;
- culturally appropriate handling;
- protection against retaliation;
- non-public evidence references;
- review without forced disclosure;
- audit without universal publication.

A record can be auditable without being universally public.

---

## 15. Anti-Erasure Violations

The following SHOULD be treated as anti-erasure violations:

- sovereignty claim recorded as stakeholder feedback;
- sovereignty claim recorded only as sentiment;
- authority basis omitted;
- claimant authority hidden;
- original claim replaced by institutional summary;
- restricted knowledge exposed without authority;
- institutional response treated as final resolution;
- unresolved authority conflict marked resolved;
- affected-party review skipped;
- closure asserted despite unresolved material claim;
- AIITL summary treated as sovereign consent.

Material violations SHOULD trigger review, challenge, repair, or schema drift handling.

---

## 16. Minimal Compliance

A minimal CDP implementation SHOULD support:

- Sovereignty Claim record;
- Authority Conflict record;
- authority basis field;
- claimant reference;
- scope;
- record controls;
- institutional response;
- unresolved status;
- closure block flag;
- execution block flag;
- affected-party or sovereign-party review references;
- dissent references.

A minimal implementation MUST NOT downgrade sovereignty claims to ordinary stakeholder preference.

---

## 17. Summary

Authority pluralism is real. CDP must be able to represent it without pretending to resolve everything.

A sovereignty claim says that the responding institution is not the only source of authority. CDP must preserve that claim, record its basis, identify conflicts, prevent downgrading, block illegitimate closure when required, and preserve review and dissent.

CDP does not own sovereignty. CDP must remember when sovereignty has been asserted.
