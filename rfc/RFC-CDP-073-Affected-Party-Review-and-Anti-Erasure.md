# RFC-CDP-073 — Affected-Party Review and Anti-Erasure

Author: Kevin “Andie” Williams  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: May 3, 2026  
Depends On: RFC-CDP-001, RFC-CDP-010, RFC-CDP-032, RFC-CDP-047, RFC-CDP-048, RFC-CDP-061, RFC-CDP-071, RFC-CDP-072  
Updates: RFC-CDP-071, RFC-CDP-072

## Abstract

This RFC defines Affected-Party Review and Anti-Erasure requirements for CDP repair processes.

RFC-CDP-071 establishes that repair claims must not be flattened. RFC-CDP-072 defines the objects that preserve breach records, repair agendas, repair points, institutional responses, commitments, completion evidence, affected-party review, and dissent.

This RFC defines the process rules that make those objects legitimate: who may review, what may be contested, when closure may be blocked, how dissent remains discoverable, and how anti-erasure failures are detected, recorded, challenged, repaired, and learned from.

Nothing about us without us.

Nothing about repair without review.

Nothing about closure without contestability.

---

## 1. Purpose

This RFC answers:

- who qualifies for affected-party review;
- what affected parties may review;
- how affected-party authority is represented;
- how summaries, classifications, evidence, responses, commitments, and closure may be contested;
- when affected-party review is required;
- when closure must be blocked;
- how dissent remains discoverable;
- how anti-erasure failures are recorded;
- how institutions are prevented from grading their own repair;
- how repair learning occurs without erasing breach history.

---

## 2. Core Principle

Repair is not complete because the responding institution says so.

Repair closure requires record, evidence, authority, contestability, and affected-party review when review is required by policy, repair context, or authority claim.

Affected parties MUST have a structured path to contest records about them, summaries of their claims, classifications of their authority, institutional responses, completion evidence, and closure.

---

## 3. Relationship to Existing RFCs

### 3.1 RFC-CDP-071 Twenty Points Repair Protocol

RFC-CDP-071 defines the repair protocol and requires repair claims to be preserved point-by-point without flattening.

This RFC defines review and anti-erasure process requirements for that protocol.

### 3.2 RFC-CDP-072 Breach Record and Repair Agenda Schema

RFC-CDP-072 defines schemas for Breach Records, Repair Agendas, Repair Points, Institutional Responses, Repair Commitments, Completion Evidence, Affected-Party Review, and Dissent.

This RFC defines when and how those records are reviewed, contested, blocked, reopened, or repaired.

### 3.3 RFC-CDP-032 Authority and Delegation Model

Affected-party authority and sovereignty authority MUST be represented as authority claims, not as ordinary preferences.

This RFC defines review rights derived from affected-party authority.

### 3.4 RFC-CDP-061 Schema Drift and Context Preservation

Anti-erasure failures are a form of repair schema drift.

This RFC defines anti-erasure triggers and repair paths when context is collapsed or misclassified.

---

## 4. Terminology

### 4.1 Affected Party

An **Affected Party** is a person, family, lineage, class, community, nation, organization, or other group materially affected by a decision, breach, repair claim, institutional response, repair commitment, or closure decision.

### 4.2 Review Right

A **Review Right** is the authority to inspect, contest, correct, dissent from, approve, reject, defer, or demand clarification of a repair-related record.

### 4.3 Review Target

A **Review Target** is any CDP record subject to affected-party review.

Review targets MAY include Breach Records, Repair Agendas, Repair Points, summaries, classifications, evidence selections, Institutional Responses, Repair Commitments, Completion Evidence, closure decisions, public summaries, redactions, and learning artifacts.

### 4.4 Anti-Erasure

**Anti-Erasure** is the requirement that CDP preserve the meaning, authority, provenance, numbering, context, dissent, and affected-party review of repair claims.

### 4.5 Erasure Event

An **Erasure Event** occurs when a record, process, or classification removes, downgrades, hides, distorts, merges, trivializes, or prematurely closes a repair claim or affected-party authority.

### 4.6 Closure

**Closure** is a state assertion that a Repair Point, Repair Agenda, Breach Record, Repair Commitment, or repair process is completed, resolved, withdrawn, superseded, or no longer active.

Closure MUST be contestable when affected-party review is required.

---

## 5. Review Rights

Affected parties SHOULD be able to review:

- whether they are correctly identified;
- whether their authority is correctly represented;
- whether a Breach Record accurately describes harm or breach;
- whether a Repair Agenda preserves original claims;
- whether each Repair Point preserves original numbering and meaning;
- whether summaries are accurate;
- whether evidence selection is adequate;
- whether institutional response is complete and truthful;
- whether repair commitments are sufficient;
- whether completion evidence supports completion;
- whether closure is legitimate;
- whether redactions are appropriate;
- whether learning artifacts erase breach, dissent, or repair obligations.

Review rights MAY be exercised directly, through authorized representatives, through community authority, or through other policy-defined processes.

---

## 6. Required Review Triggers

Affected-party review SHOULD be required when:

- a Repair Agenda identifies affected peoples;
- a Repair Point concerns identity, culture, sovereignty, treaty, land, jurisdiction, rights, safety, or institutional harm;
- a summary is substituted for original language;
- an institutional response rejects, narrows, or reclassifies a claim;
- a Repair Commitment is marked completed;
- Completion Evidence is submitted;
- closure is proposed;
- a sovereignty claim is implicated;
- record controls restrict access or public summary;
- redaction changes meaning;
- a drift signal indicates repair collapse or affected-party erasure;
- the responding institution is also the evaluator of completion.

Review MUST NOT require disclosure of restricted, ceremonial, confidential, or community-held knowledge unless the affected party or authorized community process chooses to provide it.

---

## 7. Review Target Classes

CDP implementations SHOULD support affected-party review of the following target classes:

| Target Class | Review Questions |
|---|---|
| `breach_record` | Is the breach represented accurately and with appropriate authority? |
| `repair_agenda` | Are the agenda, source, affected peoples, and authority claims preserved? |
| `repair_point` | Is the point preserved distinctly without collapse or distortion? |
| `summary` | Does the summary preserve meaning, uncertainty, limits, and authority? |
| `classification` | Has the claim been classified correctly? |
| `evidence_selection` | Is evidence missing, biased, restricted, or overexposed? |
| `institutional_response` | Does the response answer the point and preserve accountability? |
| `repair_commitment` | Is the commitment specific, resourced, authorized, and trackable? |
| `completion_evidence` | Does the evidence actually support completion? |
| `closure` | Is closure legitimate, premature, contested, or unsupported? |
| `learning_artifact` | Does learning preserve rather than erase breach history? |

---

## 8. Review States

Affected-party review SHOULD use the following states:

```text
pending
accepted
accepted_with_reservations
contested
rejected
insufficient_information
deferred
no_authority_to_review
requires_community_process
requires_cultural_protocol
requires_legal_review
requires_repair
```

### 8.1 Contested Review

A `contested` review means the target MUST NOT be treated as uncontested.

A contested review MAY block closure, trigger Challenge, require new evidence, require reclassification, or require repair.

### 8.2 Accepted With Reservations

`accepted_with_reservations` means the affected party does not block the target but preserves concerns, limitations, dissent, or future review rights.

Reservations MUST remain discoverable.

### 8.3 No Authority to Review

`no_authority_to_review` MUST NOT be interpreted as acceptance.

It means the reviewer does not claim authority over the review target, or the wrong affected party was asked.

### 8.4 Requires Community Process

`requires_community_process` means review cannot be completed by a single individual, institutional proxy, or automated system.

---

## 9. Closure Blocking

Closure MUST be blocked or escalated when:

- affected-party review is required but absent;
- review is contested and unresolved;
- completion evidence is insufficient or contested;
- institutional response fails to answer a Repair Point;
- the original claim was summarized away or renumbered without preservation;
- sovereignty authority was downgraded to stakeholder preference;
- affected-party dissent was hidden, collapsed, or marked resolved without basis;
- restricted knowledge was exposed without authority;
- repair was marked complete without evidence;
- the responding institution is the sole evaluator of completion where independent review is required.

Closure MAY proceed with recorded reservations only when policy permits and affected-party review does not block closure.

---

## 10. Anti-Erasure Violations

CDP implementations SHOULD detect and record anti-erasure violations.

Violations include:

- Repair Point merged without preservation;
- original numbering removed;
- original language discarded without reason;
- public summary substituted for restricted claim without review;
- Breach Record downgraded to risk note;
- Repair Agenda downgraded to stakeholder feedback;
- Sovereignty Claim downgraded to preference;
- Affected-Party Review replaced by internal approval;
- Dissent hidden or marked resolved without authority;
- non-response represented as neutral status;
- delay represented as progress;
- Completion Evidence replaced by institutional assertion;
- closure asserted without review;
- cultural handling requirements ignored;
- AI summary treated as affected-party consent.

---

## 11. Erasure Event Schema

An Erasure Event SHOULD be represented as:

```json
{
  "erasure_event_id": "ee_20260503_001",
  "event_type": "merge | renumber | misclassify | summarize | downgrade_authority | hide_dissent | false_closure | overexpose | non_response | delay | other",
  "target_type": "breach_record | repair_agenda | repair_point | institutional_response | repair_commitment | completion_evidence | affected_party_review | dissent | summary | closure",
  "target_ref": "target_id",
  "detected_by": "actor_or_system_ref",
  "detected_by_type": "affected_party | human_reviewer | AIITL | institution | automated_check | other",
  "severity": "minor | material | blocking | repair_required",
  "description": "string",
  "affected_party_refs": [],
  "authority_claim_refs": [],
  "recommended_action": "record | challenge | restore | reclassify | review | block_closure | repair | escalate",
  "status": "submitted | acknowledged | under_review | resolved | unresolved | superseded",
  "record_refs": [],
  "created_at": "timestamp"
}
```

Erasure Events MUST NOT delete or overwrite the original record. They SHOULD annotate, challenge, restore, or repair it.

---

## 12. Affected-Party Review Procedure

A minimal affected-party review procedure SHOULD include:

1. identify review target;
2. identify affected parties and review authority;
3. provide access to reviewable material or appropriate summary;
4. preserve restricted and culturally sensitive material according to controls;
5. collect review response;
6. record review state;
7. record dissent or requested changes;
8. determine whether review blocks closure;
9. update record, challenge, repair path, or learning path;
10. preserve review outcome.

---

## 13. Summary Contestation

Summaries are reviewable artifacts.

A summary SHOULD preserve:

- original meaning;
- original numbering;
- authority claims;
- uncertainty;
- dissent;
- restrictions;
- affected-party context;
- repair obligations.

A contested summary MUST NOT replace original language as the sole authoritative record.

If a summary is contested, CDP SHOULD preserve both the summary and the contestation record.

---

## 14. Institutional Self-Grading Constraint

A responding institution MUST NOT be the sole judge of:

- whether it caused or preserved breach;
- whether its response answers the claim;
- whether its commitment is sufficient;
- whether completion evidence is adequate;
- whether affected-party review is unnecessary;
- whether dissent is resolved;
- whether repair is closed.

Where policy permits institutional closure, the record MUST still preserve review opportunity, dissent, limitations, and basis for closure.

---

## 15. AIITL Anti-Erasure Duties

AIITL MAY surface possible anti-erasure violations.

AIITL SHOULD distinguish:

- observed record structure;
- inferred erasure risk;
- uncertainty;
- recommended challenge;
- need for affected-party or human review.

AIITL MUST NOT:

- simulate affected-party consent;
- impersonate community authority;
- close repair obligations;
- override cultural handling requirements;
- convert restricted claims into public summaries without authority;
- treat its own summary as dispositive.

AIITL MAY say:

```text
This appears to collapse a repair claim into stakeholder feedback.
This closure may require affected-party review.
This summary may be accurate syntactically but erases authority context.
This dissent should remain discoverable.
```

---

## 16. Record Requirements

Affected-party review records SHOULD preserve:

- reviewer reference;
- authority basis;
- review target;
- review state;
- review text;
- requested changes;
- dissent;
- restrictions;
- timestamps;
- closure effect;
- learning outcome.

Anti-erasure records SHOULD preserve:

- event type;
- target;
- detection source;
- severity;
- affected parties;
- authority claims;
- recommended action;
- disposition;
- repair or learning outcome.

---

## 17. Security, Privacy, and Cultural Handling

Affected-party review may involve sensitive material.

Implementations SHOULD support:

- access controls;
- role-based and community-controlled review;
- redaction;
- public summary with restricted details;
- culturally appropriate handling;
- protection against retaliation;
- non-public evidence references;
- review without forced disclosure;
- audit without universal publication.

Review rights MUST NOT become a mechanism to expose affected parties to harm.

---

## 18. Learning Closure

Affected-party review and anti-erasure outcomes SHOULD produce learning when:

- summaries are repeatedly contested;
- classifications repeatedly erase authority;
- institutions repeatedly close repair without sufficient evidence;
- affected-party review reveals missing context;
- completion evidence is repeatedly insufficient;
- cultural handling requirements are missed;
- AIITL summaries introduce erasure risk;
- repair schema drift is detected.

Learning artifacts MAY include:

- schema update;
- policy update;
- summary guidance;
- affected-party review requirement;
- anti-erasure validator;
- new closure rule;
- new training guidance;
- precedent record.

Learning MUST NOT erase breach history, dissent, review records, or unresolved repair obligations.

---

## 19. Minimal Compliance

A minimal CDP implementation SHOULD support:

- affected-party review records;
- review target references;
- review state tracking;
- contested summary handling;
- closure blocking flag;
- dissent preservation;
- erasure event records;
- anti-erasure severity;
- review-required indicators;
- affected-party review before closure when required;
- learning artifact generation for material anti-erasure failures.

A minimal implementation MUST NOT treat institutional approval as affected-party review.

---

## 20. Summary

RFC-CDP-071 defines the repair protocol. RFC-CDP-072 defines the objects. This RFC defines the process by which affected parties can review, contest, block, and preserve meaning.

Anti-erasure is not sentiment. It is a constitutional requirement that repair claims remain legible, attributable, contestable, and reviewable by those affected.

Nothing about us without us. Nothing about repair without review. Nothing about closure without contestability.
