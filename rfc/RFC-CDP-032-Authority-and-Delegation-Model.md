# RFC-CDP-032 — Authority and Delegation Model

Author: Kevin “Andie” Williams  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: May 3, 2026  
Depends On: RFC-CDP-001, RFC-CDP-010, RFC-CDP-030, RFC-CDP-031  
Updates: RFC-CDP-030, RFC-CDP-031, RFC-CDP-045, RFC-CDP-046, RFC-CDP-051, RFC-CDP-060, RFC-CDP-071

## Abstract

This RFC defines the CDP Authority and Delegation Model.

Authority in CDP is not ambient access. Authority is a scoped, attributable, time-bounded, policy-governed, revocable, and recordable capacity to perform or authorize a governed act.

This model connects Identify, Attest, Legitimize, Execute, Presence-Bound Execution Authority, Covenant, and Repair by defining what authority is, how it is granted, how it is delegated, how it decays, how it is revoked, and how it must be recorded.

A CDP system MUST distinguish identity from authority, authority from attestation, legitimacy from execution authority, access from presence, consultation from consent, and affected-party participation from institutional permission.

---

## 1. Purpose

The Authority and Delegation Model answers:

- who may perform a governed act;
- who may delegate authority;
- what scope authority applies to;
- when authority becomes valid;
- when authority expires or decays;
- how revocation behaves;
- how authority chains are recorded;
- how separation of duties is enforced;
- how authority differs across decision, execution, covenant, and repair planes;
- how sovereignty and affected-party authority are preserved without being downgraded to ordinary stakeholder preference.

---

## 2. Relationship to Existing RFCs

### 2.1 RFC-CDP-030 Identify Protocol

Identify establishes actors and links them to possible authority grants.

This RFC defines the authority model those identity records reference.

### 2.2 RFC-CDP-031 Attest Protocol

Attest binds a signer to an act and proves that a claim was made by a verifiable actor.

Attestation is not authority by itself. Attestation converts an authority claim into a verifiable governed claim.

### 2.3 RFC-CDP-045 Legitimize Protocol

Legitimize determines whether a judged Decision is institutionally enactable.

This RFC defines what authority is required to confer legitimacy, how legitimacy authority may be scoped, and what separation-of-duty constraints may apply.

### 2.4 RFC-CDP-046 Execute Protocol

Execute performs bounded enactment.

This RFC defines the authority required to request, approve, dispatch, pause, resume, roll back, or terminate execution.

### 2.5 RFC-CDP-051 Presence-Bound Execution Authority

Presence-Bound Execution Authority governs the moment of action.

This RFC defines how presence authority relates to delegated authority, quorum authority, execution authority, and authority decay.

### 2.6 RFC-CDP-060 Covenant Protocol and AIITL

Covenant defines participation duties and boundaries among human, institutional, and synthetic actors.

This RFC defines what AIITL may and may not be authorized to do, and prevents covenant participation from silently escalating into final authority.

### 2.7 RFC-CDP-071 Twenty Points Repair Protocol

Repair requires preservation of affected-party claims, sovereignty claims, breach records, and response authority.

This RFC distinguishes institutional response authority from affected-party authority and sovereignty authority.

---

## 3. Core Principle

No anonymous authority.

No ambient authority.

No authority without scope.

No authority without record.

No execution authority merely because access exists.

No legitimacy merely because power can act.

---

## 4. Terminology

### 4.1 Actor

An **Actor** is a human, institution, synthetic system, service, role, group, quorum, community, or other entity that may participate in CDP.

Actors are identified through RFC-CDP-030.

### 4.2 Authority

**Authority** is the policy-governed capacity to perform, approve, reject, challenge, attest, legitimate, execute, record, review, repair, or revoke a governed act.

Authority MUST be scoped.

### 4.3 Authority Grant

An **Authority Grant** is a structured record conferring one or more authorities to an actor, role, quorum, institution, or community for a defined scope.

### 4.4 Delegation

**Delegation** is the transfer or assignment of authority from one authorized actor to another actor within a bounded scope.

Delegation MUST NOT exceed the delegator’s own authority.

### 4.5 Revocation

**Revocation** is the invalidation of an authority grant or delegation.

Revocation MAY be immediate, scheduled, conditional, or partial.

### 4.6 Authority Decay

**Authority Decay** is the loss or weakening of authority over time or after a context change.

CDP assumes authority decays unless policy states otherwise.

### 4.7 Scope

**Scope** defines the boundaries within which authority is valid.

Scope MAY include domain, decision type, actor role, jurisdiction, policy, target system, environment, risk level, time window, data class, affected parties, repair agenda, or execution target.

### 4.8 Separation of Duties

**Separation of Duties** is a policy constraint preventing one actor or role from combining authorities that must remain independent.

### 4.9 Quorum Authority

**Quorum Authority** requires approval, presence, or attestation from multiple distinct actors, roles, institutions, or communities.

### 4.10 Affected-Party Authority

**Affected-Party Authority** is the authority of a materially affected person, group, community, class, nation, or lineage to speak to impact, contest summary, preserve claims, review repair records, or challenge closure.

Affected-party authority MUST NOT be downgraded to ordinary stakeholder preference when the claim is about harm, breach, repair, identity, sovereignty, or erasure.

### 4.11 Sovereignty Authority

**Sovereignty Authority** is authority asserted by a sovereign people, nation, community, or jurisdiction whose authority does not originate solely inside the responding institution.

CDP MUST preserve sovereignty authority as an authority claim, not merely as input.

---

## 5. Authority Types

CDP implementations SHOULD distinguish the following authority types.

| Authority | Meaning |
|---|---|
| `IDENTIFY` | Establish or update actor identity. |
| `ATTEST` | Bind actor, authority claim, and act through verifiable proof. |
| `ALIGN` | Facilitate Nemawashi or pre-formal alignment. |
| `PROPOSE` | Introduce, amend, or resubmit a Decision. |
| `CHALLENGE` | Enter structured dissent, objection, or contestation. |
| `TEST` | Run or submit validation, simulation, precedent, or evidence tests. |
| `ADJUDICATE` | Render formal judgment on deliberative posture. |
| `LEGITIMIZE` | Confer institutional enactability under policy. |
| `REQUEST_EXECUTION` | Request execution of a legitimized Decision. |
| `AUTHORIZE_EXECUTION` | Approve execution under scope and policy. |
| `EXECUTE` | Perform the bounded action. |
| `PAUSE_EXECUTION` | Pause an execution in progress. |
| `ROLLBACK` | Reverse, compensate, or mitigate an execution. |
| `OVERRIDE` | Invoke an exceptional emergency path. |
| `RECORD` | Write or finalize official record. |
| `LEARN` | Produce learning, policy, precedent, or schema updates. |
| `COVENANT_PARTICIPATE` | Participate under covenantal role boundaries. |
| `AIITL_CHALLENGE` | Surface contradiction, uncertainty, schema drift, or risk as AIITL. |
| `REPAIR_CLAIM` | Submit or preserve a repair claim or repair agenda. |
| `REPAIR_REVIEW` | Review, contest, or validate repair record or closure. |
| `REPAIR_COMMIT` | Commit resources, duties, timelines, or institutional response. |
| `REVOKE` | Revoke an authority grant or delegation. |
| `DELEGATE` | Delegate authority within scope. |

Implementations MAY define additional authority types, but extensions MUST NOT silently override these semantics.

---

## 6. Authority Grant Object

An Authority Grant SHOULD be represented as a structured object.

```json
{
  "authority_grant_id": "auth_grant_20260503_001",
  "grant_type": "direct | delegated | quorum | presence | emergency | repair | sovereignty",
  "subject": {
    "actor_id": "actor_123",
    "actor_type": "human | institution | synthetic | role | group | quorum | community"
  },
  "authorities": ["PROPOSE", "CHALLENGE"],
  "scope": {
    "domain": "cdp",
    "decision_types": ["policy_change"],
    "policy_scope": "organization_defined",
    "jurisdiction": "organization_or_community_defined",
    "risk_level_max": "medium",
    "environment": "dev | test | prod | public | regulated",
    "target_systems": [],
    "affected_parties": [],
    "repair_agenda_ids": []
  },
  "constraints": {
    "separation_of_duties": [],
    "requires_quorum": false,
    "requires_presence": false,
    "requires_attestation": true,
    "may_delegate": false,
    "may_revoke": false
  },
  "validity": {
    "issued_at": "2026-05-03T00:00:00Z",
    "effective_at": "2026-05-03T00:00:00Z",
    "expires_at": null,
    "decays_on_context_change": true
  },
  "provenance": {
    "issuer_actor_id": "actor_issuer",
    "basis": "policy | role | consent | treaty | law | community_authority | emergency",
    "policy_ref": "policy_authority_v1",
    "source_record_refs": []
  },
  "status": "active | expired | revoked | suspended | superseded",
  "attestation_ref": "attestation_456"
}
```

---

## 7. Required Authority Checks

Before accepting a governed act, a CDP implementation MUST determine:

1. Who is acting?
2. What authority is claimed?
3. What authority is required?
4. Who granted the authority?
5. Was the grant valid at the time of action?
6. Is the action within scope?
7. Has the authority expired, decayed, or been revoked?
8. Is attestation required and valid?
9. Are separation-of-duty rules satisfied?
10. Are quorum or presence requirements satisfied?
11. Are affected-party or sovereignty authority claims implicated?
12. What record will preserve the authority decision?

An act MUST fail closed if required authority cannot be established.

---

## 8. Delegation Rules

Delegation MUST obey the following rules:

1. A delegator MUST possess the authority being delegated.
2. A delegator MUST possess `DELEGATE` authority for the relevant scope.
3. Delegation MUST NOT exceed the delegator’s own scope.
4. Delegation MUST define recipient, authority, scope, validity, and revocation behavior.
5. Delegation MUST be attested.
6. Delegation MUST be recorded.
7. Delegation MUST be revocable unless policy explicitly states otherwise.
8. Delegation chains SHOULD have maximum depth.
9. Delegation chains SHOULD be inspectable and replayable.
10. Delegated authority MUST decay when the parent authority decays unless policy explicitly preserves it.

### 8.1 Prohibited Delegation Pattern

```text
Institution grants broad access to service account.
Service account grants tool access to agent.
Agent acts across domains without scoped authority.
Record only shows final API call.
```

This is ambient access, not CDP authority.

### 8.2 Required Delegation Pattern

```text
Institution grants scoped authority.
Delegation records actor, scope, policy, validity, and constraints.
Agent or service acts only inside scope.
Execution requires separate execution authority where applicable.
Record preserves the full chain.
```

---

## 9. Authority Decay and Expiration

Authority SHOULD decay or expire when:

- time window ends;
- decision state changes;
- policy version changes;
- actor role changes;
- delegation parent is revoked;
- risk classification changes;
- active challenge becomes blocking;
- affected-party review changes the record;
- repair claim alters authority context;
- execution fails;
- emergency condition ends;
- jurisdiction changes;
- scope is exceeded;
- identity trust source changes.

High-risk authority SHOULD be short-lived.

Execution authority SHOULD be shorter-lived than legitimacy authority.

Presence authority SHOULD be ephemeral.

Emergency authority SHOULD expire quickly and require post-hoc review.

---

## 10. Revocation

A CDP implementation MUST support revocation of authority grants when policy permits.

Revocation records SHOULD include:

- revoked authority grant ID;
- revoking actor;
- revocation authority;
- reason;
- effective time;
- affected delegations;
- affected pending actions;
- affected execution queues;
- affected presence grants;
- record references;
- notification requirements.

Revocation MUST propagate to dependent delegations unless policy explicitly defines otherwise.

Revocation MUST NOT erase the historical record of prior valid actions.

---

## 11. Separation of Duties

CDP implementations SHOULD support separation-of-duty rules.

Examples:

- proposer SHOULD NOT be sole adjudicator for high-impact Decisions;
- adjudicator SHOULD NOT silently legitimize when policy requires independent legitimacy review;
- execution requester SHOULD NOT be sole execution authorizer for high-risk actions;
- AIITL MAY challenge or recommend but MUST NOT hold final authority unless explicitly delegated and legally permissible;
- institutional responder SHOULD NOT be the sole judge of repair completion where affected-party review is required;
- emergency override SHOULD require post-hoc independent review.

Separation-of-duty failures MUST be recorded as authority failures.

---

## 12. Quorum Authority

Quorum authority requires multiple actors, roles, institutions, or communities.

A quorum policy SHOULD define:

- required count;
- required roles;
- disallowed role combinations;
- independence requirements;
- time window;
- whether abstention counts;
- whether dissent blocks;
- whether affected-party participation is required;
- whether quorum can be revoked after grant.

Quorum authority SHOULD be required for high-impact, irreversible, rights-affecting, regulated, contested, or repair-sensitive actions.

---

## 13. AIITL Authority Boundaries

AIITL MAY be authorized to:

- summarize;
- detect contradictions;
- surface uncertainty;
- detect schema drift;
- propose challenges;
- recommend escalation;
- draft records;
- identify missing stakeholders;
- detect authority conflicts;
- suggest repair obligations;
- prepare execution context.

AIITL MUST NOT be assumed authorized to:

- confer final legitimacy;
- execute controlled actions;
- mint its own presence grants;
- impersonate human lived experience;
- waive affected-party review;
- settle sovereignty claims;
- close repair obligations;
- override human dignity for procedural efficiency.

AIITL authority MUST be explicit, bounded, and recorded.

---

## 14. Repair and Sovereignty Authority

Repair work requires special authority handling.

CDP MUST distinguish:

- institutional authority to respond;
- affected-party authority to contest;
- community authority to preserve meaning;
- sovereignty authority that does not originate inside the responding institution;
- technical authority to record;
- legal authority to commit;
- financial or operational authority to execute repair.

A responding institution MUST NOT be treated as the sole authority over whether repair claims are valid, complete, or closed.

Sovereignty claims MUST be preserved as authority claims.

Affected-party review MUST be recorded when required by policy or repair-class RFCs.

---

## 15. Presence Authority

Presence authority is a special form of execution authority.

Presence authority MUST be:

- scoped;
- time-bounded;
- non-replayable where represented as a token;
- bound to a decision or execution request;
- recorded;
- challenge-aware;
- revocable where policy permits.

Presence authority MUST NOT be inferred from ordinary login, static credentials, long-lived sessions, or background access alone.

---

## 16. Authority Evaluation Result

Authority evaluation SHOULD produce a structured result.

```json
{
  "authority_evaluation_id": "auth_eval_20260503_001",
  "decision_id": "decision_123",
  "message_id": "message_456",
  "actor_id": "actor_789",
  "required_authorities": ["LEGITIMIZE"],
  "observed_authorities": ["LEGITIMIZE"],
  "result": "pass | fail | conditional | escalated",
  "failure_reasons": [],
  "scope_checks": [
    {
      "scope": "policy_scope",
      "result": "pass"
    }
  ],
  "separation_of_duties": {
    "required": true,
    "result": "pass"
  },
  "quorum": {
    "required": false,
    "result": "not_applicable"
  },
  "presence": {
    "required": false,
    "result": "not_applicable"
  },
  "record_ref": "record_123"
}
```

---

## 17. Security Considerations

Authority records are security-sensitive.

Implementations SHOULD protect:

- authority grants;
- delegation chains;
- revocation records;
- presence grants;
- quorum records;
- emergency overrides;
- affected-party review records;
- sovereignty claims;
- repair authority records.

Protection MAY include access control, encryption, redaction, tamper-evident storage, key rotation, and audit logs.

A record can be auditable without being universally public.

---

## 18. Failure Modes

CDP implementations MUST distinguish:

- unidentified actor;
- unauthenticated actor;
- invalid attestation;
- missing authority;
- insufficient scope;
- expired authority;
- decayed authority;
- revoked authority;
- invalid delegation;
- broken delegation chain;
- separation-of-duty failure;
- missing quorum;
- missing presence;
- active challenge conflict;
- invalid emergency override;
- affected-party authority conflict;
- sovereignty authority conflict;
- record failure.

---

## 19. Minimal Compliance

A minimal CDP implementation SHOULD support:

- actor identity references;
- explicit authority grants;
- authority scope;
- attested mutating acts;
- authority evaluation result;
- revocation status;
- basic separation-of-duty checks;
- record of authority pass/fail;
- execution authority distinct from legitimacy authority.

A minimal implementation MAY defer advanced quorum, sovereignty, and repair authority features, but it MUST NOT collapse them into ordinary stakeholder preference when present.

---

## 20. Summary

Authority is where governance becomes enforceable.

CDP authority is scoped, attributable, time-bounded, delegable only under policy, revocable, decay-aware, attested, and recorded.

Identity names the actor. Attestation proves the claim. Authority determines whether the act may proceed. Legitimacy determines whether a decision may be enacted. Presence determines whether execution may occur now. Repair and sovereignty authority preserve claims that do not originate solely inside the responding institution.

No anonymous authority. No ambient authority. No authority without scope. No authority without record.
