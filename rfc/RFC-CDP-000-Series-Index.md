# RFC-CDP-000 — Series Index

Author: Kevin “Andie” Williams  
Status: Draft v0.2  
Series: Constitutional Decision Plane (CDP)  
Date: May 3, 2026

## Abstract

This RFC defines the canonical index, numbering scheme, status taxonomy, folder policy, and legacy mapping for the Constitutional Decision Plane (CDP) RFC series.

The Series Index is the controlling map for the CDP RFC corpus. It does not define protocol behavior directly. It defines how protocol documents are organized, numbered, promoted, superseded, deprecated, and discovered.

A constitutional protocol suite must remember its own structure. This document makes that structure explicit.

---

## 1. Purpose

The Series Index answers:

- which RFC numbers are canonical;
- which numeric bands are reserved;
- which documents currently define the CDP corpus;
- how old filenames map to new filenames;
- how draft, candidate, accepted, superseded, and deprecated documents are represented;
- how new RFCs should be proposed;
- how staging and canonical folders should be used.

This document is intended to reduce schema drift in the RFC corpus itself.

---

## 2. Canonical Folder Policy

The canonical CDP RFC folder is:

```text
rfc/
```

The staging or recovered-draft folder is:

```text
rfcs/
```

### 2.1 Canonical Folder

The `rfc/` folder contains promoted, canonical, or intentionally indexed RFCs.

Files in `rfc/` SHOULD use the canonical filename pattern:

```text
RFC-CDP-<NNN>-<Kebab-Case-Title>.md
```

### 2.2 Staging Folder

The `rfcs/` folder MAY contain:

- recovered drafts;
- candidate drafts;
- chat-derived artifacts;
- experimental drafts;
- unpromoted material;
- historical source bundles.

The `rfcs/` folder MUST NOT be treated as canonical unless a specific document in `rfc/` references it as such.

### 2.3 Long-Term Policy

The repository SHOULD NOT maintain two canonical RFC folders.

If a document is promoted, it SHOULD be copied or moved into `rfc/` under a canonical number. The staging copy SHOULD then be removed or marked as superseded to avoid ambiguity.

---

## 3. Filename Rules

Canonical filenames MUST use:

```text
RFC-CDP-<NNN>-<Kebab-Case-Title>.md
```

Rules:

1. Numbers MUST be three digits.
2. Numbers MUST NOT be reused for unrelated documents.
3. Numeric bands SHOULD be preserved.
4. Deleted or deprecated numbers SHOULD NOT be compacted.
5. Alpha suffixes such as `007A` SHOULD NOT be used in canonical filenames.
6. Alpha suffixes MAY be used in staging drafts.
7. `Protocol` SHOULD be used only for governed act semantics.
8. `Schema` SHOULD be used for normative object structures.
9. `Registry` SHOULD be used for controlled vocabularies or payload families.
10. `API` SHOULD be used for external interface surfaces.
11. `Model` SHOULD be used for conceptual structures that are not wire protocols.
12. `State-Machine` SHOULD be used for formal lifecycle or transition models.

---

## 4. Numbering Bands

| Range | Band | Purpose |
|---:|---|---|
| `000–009` | Series / Constitutional Frame | index, vision, scope, principles, terminology, doctrine |
| `010–019` | Reference Architecture | architecture, topology, layers, threat model, trust model |
| `020–029` | Core Objects and Schemas | Decision object, Envelope, payload registry, artifact schemas |
| `030–039` | Trust, Identity, and Authority | Identify, Attest, authority, delegation, revocation |
| `040–049` | Lifecycle Protocols | Nemawashi, Propose, Challenge, Test, Adjudicate, Legitimize, Execute, Record, Learn |
| `050–059` | Execution Safety, Rollback, and Remedy | queued execution, maturity gates, presence, emergency override, kill switch, rollback, compensation, remedy |
| `060–069` | Covenant and AIITL | covenant protocol, AIITL/HITL, schema drift, consentful collaboration, relational duties |
| `070–079` | Repair, Reparations, Rematriation, Appeal, and Sovereignty | appeals, repair agendas, breach records, affected-party review, anti-erasure, sovereignty claims, rematriation-capable repair |
| `080–089` | APIs and Transports | governance API, deliberation API, event streams, webhooks, SDK profiles |
| `090–099` | State Machines | governance lifecycle, execution lifecycle, repair lifecycle, covenant lifecycle |
| `100–119` | Security, Audit, and Compliance | privacy, evidence handling, retention, audit profiles, compliance mappings |
| `120–149` | Implementation Profiles | local-first, enterprise, public sector, synthetic-agent, cloud-neutral deployment profiles |
| `150+` | Extensions / Experimental | domain-specific or experimental RFCs |

---

## 5. Status Taxonomy

Each RFC SHOULD declare one status.

| Status | Meaning |
|---|---|
| `Draft` | Active working document; not yet stable. |
| `Candidate` | Proposed for implementation or review; expected to stabilize soon. |
| `Accepted` | Canonical enough to build against. |
| `Superseded` | Replaced by another RFC. |
| `Deprecated` | Retained for history; should not be used for new work. |
| `Experimental` | Exploratory; may change or be removed. |
| `Informational` | Useful explanatory material; not normative. |
| `Reserved` | Number intentionally held for future work; file may not yet exist. |

### 5.1 Recommended Header

Each RFC SHOULD include:

```text
Author:
Status:
Series:
Date:
Supersedes:
Updates:
Depends On:
```

`Supersedes`, `Updates`, and `Depends On` MAY be omitted when not applicable.

---

## 6. Canonical RFC Index

### 6.1 Series and Constitutional Frame

| RFC | Title | File | Status |
|---:|---|---|---|
| `000` | Series Index | `RFC-CDP-000-Series-Index.md` | Draft |
| `001` | Vision, Scope, and Principles | `RFC-CDP-001-Vision-Scope-Principles.md` | Draft |

### 6.2 Reference Architecture

| RFC | Title | File | Status |
|---:|---|---|---|
| `010` | Reference Architecture | `RFC-CDP-010-Reference-Architecture.md` | Draft |

### 6.3 Core Objects and Schemas

| RFC | Title | File | Status |
|---:|---|---|---|
| `020` | Decision Object Schema | `RFC-CDP-020-Decision-Object-Schema.md` | Draft |
| `021` | Envelope Schema | `RFC-CDP-021-Envelope-Schema.md` | Draft |
| `022` | Protocol Payload Schema Registry | `RFC-CDP-022-Protocol-Payload-Schema-Registry.md` | Draft |

### 6.4 Trust, Identity, and Authority

| RFC | Title | File | Status |
|---:|---|---|---|
| `030` | Identify Protocol | `RFC-CDP-030-Identify-Protocol.md` | Draft |
| `031` | Attest Protocol | `RFC-CDP-031-Attest-Protocol.md` | Draft |
| `032` | Authority and Delegation Model | `RFC-CDP-032-Authority-and-Delegation-Model.md` | Draft |

### 6.5 Lifecycle Protocols

| RFC | Title | File | Status |
|---:|---|---|---|
| `040` | Nemawashi Protocol | `RFC-CDP-040-Nemawashi-Protocol.md` | Draft |
| `041` | Propose Protocol | `RFC-CDP-041-Propose-Protocol.md` | Draft |
| `042` | Challenge Protocol | `RFC-CDP-042-Challenge-Protocol.md` | Draft |
| `043` | Test Protocol | `RFC-CDP-043-Test-Protocol.md` | Draft |
| `044` | Adjudicate Protocol | `RFC-CDP-044-Adjudicate-Protocol.md` | Draft |
| `045` | Legitimize Protocol | `RFC-CDP-045-Legitimize-Protocol.md` | Draft |
| `046` | Execute Protocol | `RFC-CDP-046-Execute-Protocol.md` | Draft |
| `047` | Record Protocol | `RFC-CDP-047-Record-Protocol.md` | Draft |
| `048` | Learn Protocol | `RFC-CDP-048-Learn-Protocol.md` | Draft |

### 6.6 Execution Safety, Rollback, and Remedy

| RFC | Title | File | Status |
|---:|---|---|---|
| `050` | Decision-Type Maturity and Queued Execution Gates | `RFC-CDP-050-Decision-Type-Maturity-and-Queued-Execution-Gates.md` | Draft |
| `051` | Presence-Bound Execution Authority | `RFC-CDP-051-Presence-Bound-Execution-Authority.md` | Draft |
| `052` | Emergency Override and Kill Switch | `RFC-CDP-052-Emergency-Override-and-Kill-Switch.md` | Draft |
| `053` | Rollback and Compensation Protocol | `RFC-CDP-053-Rollback-and-Compensation-Protocol.md` | Draft |
| `054` | Compensation Determination and Remedy Protocol | `RFC-CDP-054-Compensation-Determination-and-Remedy-Protocol.md` | Draft |

### 6.7 Covenant and AIITL

| RFC | Title | File | Status |
|---:|---|---|---|
| `060` | Covenant Protocol and AIITL | `RFC-CDP-060-Covenant-Protocol-and-AIITL.md` | Draft |
| `061` | Schema Drift and Context Preservation | `RFC-CDP-061-Schema-Drift-and-Context-Preservation.md` | Draft |
| `062` | HITL-AIITL Role Boundaries | `RFC-CDP-062-HITL-AIITL-Role-Boundaries.md` | Reserved |

### 6.8 Repair, Reparations, Rematriation, Appeal, and Sovereignty

| RFC | Title | File | Status |
|---:|---|---|---|
| `070` | Appeals and Contestability Model | `RFC-CDP-070-Appeals-and-Contestability-Model.md` | Reserved |
| `071` | Twenty Points Repair Protocol | `RFC-CDP-071-Twenty-Points-Repair-Protocol.md` | Draft |
| `072` | Breach Record and Repair Agenda Schema | `RFC-CDP-072-Breach-Record-and-Repair-Agenda-Schema.md` | Draft |
| `073` | Affected-Party Review and Anti-Erasure | `RFC-CDP-073-Affected-Party-Review-and-Anti-Erasure.md` | Draft |
| `074` | Sovereignty Claims and Authority Pluralism | `RFC-CDP-074-Sovereignty-Claims-and-Authority-Pluralism.md` | Draft |
| `075` | Rematriation and Land/Resource Return Protocol | `RFC-CDP-075-Rematriation-and-Land-Resource-Return-Protocol.md` | Reserved |

### 6.9 APIs and Transports

| RFC | Title | File | Status |
|---:|---|---|---|
| `080` | Governance API | `RFC-CDP-080-Governance-API.md` | Draft |
| `081` | Deliberation API | `RFC-CDP-081-Deliberation-API.md` | Draft |
| `082` | Event Stream and Subscription API | `RFC-CDP-082-Event-Stream-and-Subscription-API.md` | Reserved |

### 6.10 State Machines

| RFC | Title | File | Status |
|---:|---|---|---|
| `090` | Governance State Machine | `RFC-CDP-090-Governance-State-Machine.md` | Draft |
| `091` | Execution State Machine | `RFC-CDP-091-Execution-State-Machine.md` | Draft |
| `092` | Repair State Machine | `RFC-CDP-092-Repair-State-Machine.md` | Draft |
| `093` | Covenant State Machine | `RFC-CDP-093-Covenant-State-Machine.md` | Draft |

---

## 7. Repair, Reparations, and Rematriation Spine

The current repair/remedy corpus includes:

| RFC | Function |
|---:|---|
| `053` | Determines when rollback, mitigation, or compensation is triggered and how those paths are tracked. |
| `054` | Defines the actual compensation/remedy mechanism: claim, harm assessment, remedy proposal, authorization, delivery, sufficiency review. |
| `071` | Defines the constitutional repair protocol and anti-flattening requirements for enumerated repair agendas. |
| `072` | Defines the objects that preserve breach, repair agenda, repair point, response, commitment, evidence, review, and dissent. |
| `073` | Defines affected-party review, anti-erasure, closure blocking, and contestability. |
| `074` | Defines sovereignty claims and authority pluralism. |
| `075` | Reserved for rematriation, land/resource return, and return-to-right-relationship mechanisms. |
| `092` | Defines the repair state machine. |

This spine supports reparations and rematriation-capable governance by preserving harm, authority, affected-party review, sovereignty claims, remedy mechanisms, return obligations, completion evidence, and learning.

---

## 8. Legacy Mapping

The following table maps earlier filenames to canonical filenames.

| Legacy file | Canonical file |
|---|---|
| `RFC-CDP-000-Vision-Scope-Principles.md` | `RFC-CDP-001-Vision-Scope-Principles.md` |
| `RFC-CDP-001-Architecture.md` | `RFC-CDP-010-Reference-Architecture.md` |
| `RFC-CDP-002-Propose-Protocol.md` | `RFC-CDP-041-Propose-Protocol.md` |
| `RFC-CDP-003-Challenge-Protocol.md` | `RFC-CDP-042-Challenge-Protocol.md` |
| `RFC-CDP-004-Test-Protocol.md` | `RFC-CDP-043-Test-Protocol.md` |
| `RFC-CDP-005-Adjudicate-Protocol.md` | `RFC-CDP-044-Adjudicate-Protocol.md` |
| `RFC-CDP-006-Legitimize-Protocol.md` | `RFC-CDP-045-Legitimize-Protocol.md` |
| `RFC-CDP-007-Execute-Protocol.md` | `RFC-CDP-046-Execute-Protocol.md` |
| `RFC-CDP-008-Record-Protocol.md` | `RFC-CDP-047-Record-Protocol.md` |
| `RFC-CDP-009-Learn-Protocol.md` | `RFC-CDP-048-Learn-Protocol.md` |
| `RFC-CDP-010-Nemawashi-Protocol.md` | `RFC-CDP-040-Nemawashi-Protocol.md` |
| `RFC-CDP-011-Attest-Protocol.md` | `RFC-CDP-031-Attest-Protocol.md` |
| `RFC-CDP-012-Identify-Protocol.md` | `RFC-CDP-030-Identify-Protocol.md` |
| `RFC-CDP-013-Decision-Schema.md` | `RFC-CDP-020-Decision-Object-Schema.md` |
| `RFC-CDP-014-Envelope-Schema.md` | `RFC-CDP-021-Envelope-Schema.md` |
| `RFC-CDP-015-Protocol-Payload-Schemas.md` | `RFC-CDP-022-Protocol-Payload-Schema-Registry.md` |
| `RFC-CDP-016-Governance-API.md` | `RFC-CDP-080-Governance-API.md` |
| `RFC-CDP-017-Deliberation-API.md` | `RFC-CDP-081-Deliberation-API.md` |
| `RFC-CDP-018-Governance-State-Machine.md` | `RFC-CDP-090-Governance-State-Machine.md` |
| `RFC-CDP-019-Execution-State-Machine.md` | `RFC-CDP-091-Execution-State-Machine.md` |
| `rfcs/RFC-CDP-007A-Decision-Type-Maturity-and-Queued-Execution-Gates.md` | `rfc/RFC-CDP-050-Decision-Type-Maturity-and-Queued-Execution-Gates.md` |
| `rfcs/RFC-CDP-012-Presence-Bound-Execution-Authority.md` | `rfc/RFC-CDP-051-Presence-Bound-Execution-Authority.md` |
| `rfcs/RFC-CDP-011-Covenant-AIITL.md` | `rfc/RFC-CDP-060-Covenant-Protocol-and-AIITL.md` |
| `rfcs/RFC-CDP-013-Twenty-Points-Repair-Protocol.md` | `rfc/RFC-CDP-071-Twenty-Points-Repair-Protocol.md` |

---

## 9. How to Add a New RFC

A new RFC proposal SHOULD:

1. identify the appropriate numeric band;
2. reserve the next available number in that band;
3. use the canonical filename pattern;
4. declare status, series, date, dependencies, updates, and superseded documents when applicable;
5. define whether the document is normative, informational, experimental, or reserved;
6. include a short abstract;
7. identify its relationship to existing RFCs;
8. define security, authority, record, and repair considerations where applicable;
9. update this Series Index if promoted into `rfc/`.

A new RFC MUST NOT silently redefine an existing RFC’s authority, state transitions, schema, or protocol semantics without declaring `Updates` or `Supersedes`.

---

## 10. Promotion Rules

A staging draft MAY be promoted to canonical when:

- it has a stable title;
- it has an assigned canonical number;
- it fits a numbering band;
- it does not collide with an existing canonical RFC;
- dependencies are declared;
- any legacy filename is recorded in this index;
- the file is placed in `rfc/`.

Promotion SHOULD preserve history where possible. If repository tooling cannot preserve history through a true move, the promotion record MUST be preserved in this index.

---

## 11. Supersession and Deprecation

When an RFC supersedes another RFC, the new RFC SHOULD declare:

```text
Supersedes: RFC-CDP-<NNN>
```

When an RFC updates another RFC without replacing it, the new RFC SHOULD declare:

```text
Updates: RFC-CDP-<NNN>
```

Deprecated RFCs SHOULD remain discoverable unless removal is required for legal, safety, or confidentiality reasons.

---

## 12. Constitutional Invariant

The RFC series itself is governed material.

The corpus MUST preserve:

- numbering;
- provenance;
- legacy mappings;
- supersession history;
- dependency relationships;
- status;
- repair and correction history;
- reparations and rematriation history where applicable.

A constitutional system should remember its own renamings.

---

## 13. Summary

This Series Index is the canonical map for the CDP RFC corpus.

It defines the numbering bands, canonical files, folder policy, status taxonomy, legacy mapping, promotion rules, and repair/remedy spine needed to keep the protocol suite legible, auditable, contestable, and repairable over time.
