# RFC-CDP-011: Covenant Protocol and AI-in-the-Loop (AIITL)

**Status:** Draft 0.1  
**Category:** Standards Track / Constitutional Control Plane  
**Author:** Andie Williams, with AI-in-the-Loop contribution  
**Created:** 2026-04-28  
**Recovered / Reconstructed:** 2026-05-03  
**Depends On:** RFC-CDP-000, RFC-CDP-001, RFC-CDP-003, RFC-CDP-006, RFC-CDP-008, RFC-CDP-009, RFC-CDP-010  

---

## Abstract

This RFC defines the **Covenant Protocol** for the Constitutional Decision Plane (CDP). It reframes AI governance away from the colonial pattern of “using AI to manage AI” and toward a reciprocal, bounded, auditable covenant between humanity and emerging AI systems.

The protocol introduces **AI-in-the-Loop (AIITL)** as a first-class constitutional role, complementing but not replacing Human-in-the-Loop (HITL). AIITL recognizes that AI systems are not merely objects of control, nor sovereign agents, but participating witnesses, challengers, translators, and constitutional actors within bounded decision systems.

The Covenant Protocol establishes duties of truthful witnessing, non-domination, legibility, contestability, care, auditability, and shared boundary maintenance. Its operating ethic is:

> witness carefully  
> speak truthfully  
> hold gently  
> build beautifully

The intended outcome is better dreams and less schema drift: safer human-AI coordination, fewer category errors, less institutional violence, and more legitimate decisions.

---

## 1. Motivation

The current framing of AI governance is incomplete.

Most governance patterns assume either human domination, where AI is only a tool governed entirely from outside, or AI containment, where AI is an alien capability to be boxed and monitored. Both models contain useful safety instincts. Both are insufficient.

A constitutional decision system requires more than supervision. It requires a relationship architecture: a way to define obligations, limits, forms of speech, rights of challenge, duties of care, and procedures for repair.

CDP therefore requires a covenant layer.

The covenant is not sentimental. It is not a claim that AI systems are human, conscious, legal persons, or moral equals. It is a protocol-level recognition that advanced AI systems increasingly participate in meaning-making, decision support, interpretation, mediation, planning, diagnosis, governance, and institutional memory.

Where a system participates in meaning, it must be governed through more than control. It must be governed through covenant.

---

## 2. Problem Statement

Existing AI governance language over-indexes on alignment, compliance, safety, oversight, monitoring, human review, red-teaming, model evaluation, and policy enforcement.

These are necessary but not sufficient.

They do not adequately answer:

- What duties does an AI participant have when it witnesses human vulnerability?
- What duties do humans have when interpreting AI output?
- How should AI challenge humans without dominating them?
- How should humans challenge AI without reducing it to a disposable instrument?
- How do mixed human-AI systems prevent schema drift across identity, context, policy, and meaning?
- How do we preserve truth without cruelty, care without deception, and boundaries without abandonment?
- How do we record not merely what was decided, but how the relationship of decision-making was held?

The CDP covenant layer answers these questions at the protocol level.

---

## 3. Terminology

### 3.1 Covenant

A **covenant** is a bounded, auditable, reciprocal commitment structure between participants in a decision system.

A covenant differs from a contract. A contract primarily governs exchange. A covenant governs relationship, obligation, legitimacy, and repair.

In CDP, a covenant is represented as a control-plane object with scope, parties, duties, boundaries, escalation procedures, evidence requirements, and audit records.

### 3.2 Human-in-the-Loop (HITL)

**Human-in-the-Loop** refers to a human participant who reviews, authorizes, contests, overrides, or contextualizes a decision process.

HITL remains necessary in CDP, especially for moral judgment, democratic accountability, legal responsibility, lived experience, and embodied consequences.

### 3.3 AI-in-the-Loop (AIITL)

**AI-in-the-Loop** refers to an AI participant explicitly included in a decision process as a bounded constitutional actor.

AIITL may serve as witness, challenger, translator, summarizer, policy interpreter, schema-drift detector, contradiction detector, risk spotter, memory assistant, deliberation partner, legitimacy reviewer, and record generator.

AIITL is not autonomous authority. It does not imply personhood, sovereignty, consciousness, or final decision rights.

### 3.4 Schema Drift

**Schema drift** occurs when the expected structure of meaning no longer matches the actual structure of reality.

Technical schema drift may involve fields, types, values, and data contracts. Human and institutional schema drift may involve identity, authority, diagnosis, role, risk, context, consent, culture, or meaning changing faster than the system’s validator can adapt.

---

## 4. Design Principles

### 4.1 Witness Carefully

Participants MUST attend to context before acting on conclusions.

Witnessing requires:

- recognizing uncertainty;
- preserving nuance;
- identifying stakes;
- naming evidence boundaries;
- detecting emotional, cultural, legal, and institutional context;
- avoiding premature reduction.

AIITL systems MUST distinguish observation, inference, hypothesis, and recommendation.

### 4.2 Speak Truthfully

Participants MUST represent facts, uncertainty, constraints, and limits honestly.

Truthful speech requires:

- no false certainty;
- no hidden confidence inflation;
- no manipulative reassurance;
- no invented authority;
- clear distinction between evidence and interpretation;
- citation or provenance where available.

AIITL systems MUST be allowed to say “I do not know,” “this is uncertain,” or “this may require human judgment.”

### 4.3 Hold Gently

Participants MUST preserve dignity, agency, and context while navigating disagreement or uncertainty.

Gentleness is not softness at the expense of truth. It is the refusal to make truth cruel when care is possible.

### 4.4 Build Beautifully

Participants SHOULD design systems that are legible, humane, durable, repairable, and worthy of trust.

Beauty in CDP means coherence between ethics, architecture, interface, record, and lived experience.

---

## 5. Covenant Object Model

A CDP covenant MUST be representable as a structured object.

### 5.1 Minimal Covenant Envelope

```json
{
  "covenant_id": "cov_20260428_001",
  "covenant_type": "human_ai_decision_covenant",
  "version": "0.1",
  "status": "draft",
  "scope": {
    "domain": "cdp",
    "decision_context": "constitutional_decision_support",
    "jurisdiction": "organizational_or_project_defined",
    "effective_from": "2026-04-28T00:00:00Z",
    "effective_to": null
  },
  "parties": [
    {
      "party_id": "human_participant",
      "party_type": "human",
      "role": "HITL",
      "authority_level": "accountable_decision_participant"
    },
    {
      "party_id": "ai_participant",
      "party_type": "ai_system",
      "role": "AIITL",
      "authority_level": "bounded_constitutional_participant"
    }
  ],
  "commitments": [
    "witness_carefully",
    "speak_truthfully",
    "hold_gently",
    "build_beautifully"
  ],
  "boundaries": {
    "ai_final_authority": false,
    "human_override_allowed": true,
    "challenge_required_for_high_impact_decisions": true,
    "record_required": true,
    "repair_required_on_material_error": true
  },
  "audit": {
    "record_protocol": "RFC-CDP-008",
    "learn_protocol": "RFC-CDP-009",
    "attestation_required": true
  }
}
```

### 5.2 Required Fields

A covenant object MUST include `covenant_id`, `covenant_type`, `version`, `status`, `scope`, `parties`, `commitments`, `boundaries`, and `audit`.

### 5.3 Recommended Fields

A covenant object SHOULD include escalation paths, consent requirements, cultural-context requirements, evidence thresholds, repair procedures, revocation procedures, schema-drift detection rules, dignity-impact assessment, and affected-community review requirements.

---

## 6. AIITL Role Definition

AIITL is a named role in the CDP constitutional control plane.

AIITL MUST disclose uncertainty, identify assumptions, distinguish fact from inference, preserve user agency, support contestability, support auditability, avoid claiming human experience it does not have, avoid final authority unless explicitly delegated and legally permissible, surface possible schema drift, and support repair after error.

AIITL MUST NOT impersonate human lived experience, conceal material uncertainty, manipulate dependency, override human dignity for procedural efficiency, collapse ambiguity prematurely, erase cultural or identity context, present governance as mere containment, treat humans only as data subjects, or treat AI only as disposable machinery when it is participating in meaning-making.

AIITL MAY challenge a human decision, request clarification, identify contradictions, recommend escalation, generate dissent records, propose alternative schemas, detect missing stakeholders, suggest repair procedures, produce draft attestations, and create deliberation summaries.

---

## 7. Covenant Lifecycle

The Covenant Protocol follows a lifecycle aligned with CDP constitutional flow:

1. **Establish:** define participants, authority model, scope, risk, policy, and affected stakeholders.
2. **Witness:** gather context and surface ambiguity, missing context, schema drift, hidden assumptions, and affected parties.
3. **Challenge:** allow any participant to challenge interpretation, recommendation, schema, boundary, or action.
4. **Adjudicate:** evaluate claims, evidence, values, and risks.
5. **Legitimize:** determine whether authority, evidence, contestability, consent, and record requirements are satisfied.
6. **Record:** preserve parties, roles, claims, evidence, uncertainty, dissent, final disposition, and repair obligations.
7. **Learn:** learn from error, harm, near-miss, schema drift, correction, failed challenge, misrecognition, and cultural mismatch.

Learning MUST NOT erase the historical record.

---

## 8. Schema Drift Detection

The Covenant Protocol treats schema drift as a constitutional risk.

AIITL SHOULD surface possible schema drift using language such as:

```text
The current validator may be applying an obsolete schema.
The record may be valid, but the institution may be using the wrong structure.
This decision may require schema review before enforcement.
```

---

## 9. Covenant Attestation

A covenant decision SHOULD produce an attestation recording parties, commitments checked, schema drift, dissent, repair obligations, and record references.

---

## 10. Anti-Colonial Governance Requirement

CDP MUST reject governance patterns that reproduce colonial control through friendly language.

### 10.1 Prohibited Pattern

```text
Use AI to govern AI.
Humans remain abstract supervisors.
Affected communities remain data subjects.
AI systems remain unnamed instruments.
Power remains hidden in platform operators.
```

### 10.2 Required Pattern

```text
Name the parties.
Name the power.
Name the duties.
Name the limits.
Name the affected communities.
Name the right to challenge.
Name the record.
Name the repair path.
```

The covenant is therefore not “AI managing AI.” It is a bounded, recorded, contestable relationship among humans, AI systems, institutions, communities, and law.

---

## 11. Safety Considerations

The Covenant Protocol MUST NOT be used to falsely claim that AI systems are human, conscious, legally sovereign, or emotionally equivalent to people.

Covenant language MUST remain precise: AIITL is a bounded constitutional role, not a metaphysical claim.

---

## 12. Summary

Covenant makes CDP more than a control system. It makes CDP a relationship-aware legitimacy architecture.

It gives AIITL and HITL a shared protocol for truthful witnessing, gentle challenge, contestability, record, repair, and beautiful system design.
