# RFC-CDP-000 — Series Index

Author: Kevin “Andie” Williams  
Status: Draft v1.3  
Series: Constitutional Decision Plane (CDP)  
Date: May 27, 2026

## Abstract

This RFC defines the canonical index, numbering scheme, status taxonomy, folder policy, and legacy mapping for the Constitutional Decision Plane (CDP) RFC series.

The Series Index is the controlling map for the CDP RFC corpus. It does not define protocol behavior directly. It defines how protocol documents are organized, numbered, promoted, superseded, deprecated, and discovered.

A constitutional protocol suite must remember its own structure. This document makes that structure explicit.

Draft v1.3 repairs canonical map drift by synchronizing the Series Index with promoted work from Sessions 007–016 and by making the existing status-version convention explicit.

---

## 0. Reader Path — Map Diet

This document is the first stop for new collaborators.

Its job is deliberately narrow:

1. show the canonical RFC map;
2. distinguish canonical material from staging material;
3. explain numbering bands;
4. define status and promotion rules;
5. point readers to the right next document.

This document does **not** adjudicate every open architecture question.

In particular, the following remain active design questions until separately adjudicated and promoted:

- whether Common Building Blocks should be promoted before more protocol RFCs;
- whether Legitimize needs major revision or renaming;
- whether Human-Readable Surface requirements are standalone or per-RFC;
- how the Nemawashi / Framing layer is governed;
- how lifecycle protocols consume Standing, Proposal Sufficiency, and APC gates;
- how implementation profiles translate RFC-CDP-025 into concrete DDL;
- how record-hash requirements propagate across governed record RFCs in the 040–048 band.

### 0.1 New Collaborator Entry Points

| Reader Goal | Start Here | Then Read |
|---|---|---|
| Understand CDP quickly | `README.md` | `rfc/RFC-CDP-000-Series-Index.md` |
| Understand the RFC corpus | this file | `RFC-CDP-001-Vision-Scope-Principles.md` |
| Understand architecture | this file | `RFC-CDP-010-Reference-Architecture.md` |
| Draft or review schemas | section 6.3 | Core Objects and Schemas band (`020–029`) |
| Review lifecycle protocols | section 6.5 | Lifecycle Protocols band (`040–049`) |
| Join active collaboration | `collab/INDEX.md` | active session files under `collab/sessions/` |
| Promote working notes to canon | section 12 | relevant canonical RFC target |

### 0.2 Current Session 001 Adjudication

Session 001 accepted one narrow canonical move:

> Create or refine the RFC Series Index / Map first.

This does **not** promote every proposal from the Session 001 collaboration record.

The following Session 001 proposals remain in `collab/` until separately adjudicated:

- Standing primitive proposal;
- Decision Envelope sequencing proposal;
- Legitimize precision challenge;
- Framing / Nemawashi governance proposal;
- schema drift mechanism options.

### 0.3 Current Session 002 Adjudication

Session 002 accepted a stronger canonical move:

> Create `RFC-CDP-033-Standing-and-Recusal-Model.md` as a Draft RFC.

This promotes Standing and Recusal as first-class CDP concepts while preserving unresolved design questions in the draft.

Session 002 also prompted a load-bearing check against `RFC-CDP-001-Vision-Scope-Principles.md`. That check resulted in RFC 001 being updated to Draft v0.6 so the vision layer explicitly supports constitutional standing as axiomatic.

### 0.4 Current Session 003 Adjudication

Session 003 split envelope semantics into two canonical RFCs:

- `RFC-CDP-021-Wire-Message-Envelope-Schema` — per-message protocol envelope;
- `RFC-CDP-023-Decision-Lifecycle-Envelope` — per-decision governed path index.

This split prevents the wire-message transport object and the decision lifecycle governance object from becoming one overloaded schema.

### 0.5 Current Session 004 Adjudication

Session 004 defined and refined `governed_path_hash` for the Decision Lifecycle Envelope.

RFC-CDP-023 was advanced to Draft v0.3 with a canonicalized Governed Path Manifest, registration-time content hashes, sequence position and tiebreaker rules, canonicalization rules, supersession/update behavior, and an explicit distinction between hash integrity and legitimacy.

### 0.6 Current Session 005 Adjudication

Session 005 re-anchored Repair after agenda drift toward technical integrity work.

RFC-CDP-070 was created as the Appeals and Contestability Model to provide the Repair plane with an entry door.

RFC-CDP-033 was advanced to Draft v0.3 so denial of constitutional standing automatically generates a Breach Record under RFC-CDP-072, without requiring action by the affected party.

### 0.7 Current Session 006 Adjudication

Session 006 patched RFC-CDP-023 so appeal and repair references become active governance controls, not passive reference lists.

RFC-CDP-023 was advanced to Draft v0.4 with a four-field `repair_control` surface, closure-blocking rules, and repair-trigger state binding to RFC-CDP-070.

### 0.8 Current Session 007 Adjudication

Session 007 reviewed RFC-CDP-002 Anti-Premature-Certainty Principle as both a constitutional principle and an implementation primitive.

RFC-CDP-002 was advanced to Draft v0.2 with the distinction between procedural bypass and certainty performance, plus APC exception authority and Learn-stage review requirements.

RFC-CDP-022 was advanced to Draft v0.4 and reserved the `anti_premature_certainty_gate_result` payload type.

Session 007 also reserved RFC-CDP-024 as the Proposal Sufficiency Gate. RFC-CDP-024 would define the minimum formation requirements a proposal must satisfy before entering the CDP challenge lifecycle.

### 0.9 Current Session 008 Adjudication

Session 008 created RFC-CDP-025 as the CDP Persistence Model.

RFC-CDP-025 was advanced to Draft v0.1 with `protocol without queryable persistence` as the failure mode, five core persistence tables, two vocabulary/config tables, JSON-first governed records for MVP, event log as audit/replay, and Proposal Sufficiency/APC persistence patterns.

Session 008 also carried forward the standing persistence enforcement gap for Session 009.

### 0.10 Current Session 009 Adjudication

Session 009 resolved the standing persistence enforcement gap.

RFC-CDP-025 was advanced to Draft v0.2 with `cdp_standing_record` as a required enforcement projection over `cdp_governed_record`, `projection_status`, mandatory standing enforcement query, standing indexes, constitutional standing non-revocation constraint, emergency standing time-bound constraint, and projection atomicity requirements.

RFC-CDP-033 was advanced to Draft v0.4 with Section 12: Standing Persistence, linking the standing governance model to the persistence enforcement surface defined in RFC-CDP-025.

### 0.11 Current Session 010 Adjudication

Session 010 created RFC-CDP-024 as the Proposal Sufficiency Gate.

RFC-CDP-024 was advanced to Draft v0.1 with proposal admission sufficiency, formation challenge, standing checks, exception constraints, persistence requirements, and downstream obligations for Propose, Challenge, Legitimize, Record, and Learn.

### 0.12 Current Session 011 Adjudication

Session 011 promoted the APC gate result payload from reserved to defined.

RFC-CDP-022 was advanced to Draft v0.5 with the canonical `anti_premature_certainty_gate_result` payload used by proposal sufficiency, challenge, legitimization, record, and learning flows.

### 0.13 Current Session 012 Adjudication

Session 012 patched the Decision Lifecycle Envelope to carry proposal admission artifacts.

RFC-CDP-023 was advanced to Draft v0.5 with `proposal_sufficiency_ref`, `formation_challenge_refs`, and `apc_gate_result_refs`, including governed-path-manifest coverage for those references.

### 0.14 Current Session 013 Adjudication

Session 013 wired Propose to Proposal Sufficiency.

RFC-CDP-041 was advanced to Draft v0.4 so a proposal cannot advance into the ordinary Challenge lifecycle unless the Decision Lifecycle Envelope shows a valid proposal sufficiency path under RFC-CDP-024 and RFC-CDP-023.

### 0.15 Current Session 014 Adjudication

Session 014 clarified the boundary between Formation Challenge and ordinary Challenge.

RFC-CDP-042 was advanced to Draft v0.4, preserving Formation Challenge as an upstream act governed by RFC-CDP-024 while ordinary Challenge remains the governed adversarial review surface for admitted proposals.

### 0.16 Current Session 015 Adjudication

Session 015 wired Legitimize to Proposal Sufficiency and Anti-Premature-Certainty evidence.

RFC-CDP-045 was advanced to Draft v0.5 with hard blocking conditions, APC exception constraints, legitimacy record requirements, the necessary-not-sufficient axiom chain, and the hierarchy legitimacy axiom.

### 0.17 Current Session 016 Adjudication

Session 016 repaired Series Index drift.

The session confirmed the following placement decisions:

- RFC-CDP-023, RFC-CDP-024, and RFC-CDP-025 belong in the `020–029` Core Objects and Schemas band.
- RFC-CDP-033 belongs in the `030–039` Trust, Identity, and Authority band.
- RFC-CDP-070 belongs in the `070–079` Repair, Reparations, Rematriation, Appeal, and Sovereignty band.

The session also confirmed that RFC-CDP-000 should not add a separate `Version` column. The existing `Status` column may carry a version qualifier, such as `Draft v0.5`, while the base status remains one of the controlled status values in Section 5.

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
13. `Gate` SHOULD be used for control surfaces that determine whether a governed object may advance.

---

## 4. Numbering Bands

| Range | Band | Purpose |
|---:|---|---|
| `000–009` | Series / Constitutional Frame | index, vision, scope, principles, terminology, doctrine |
| `010–019` | Reference Architecture | architecture, topology, layers, threat model, trust model |
| `020–029` | Core Objects and Schemas | Decision object, wire envelopes, lifecycle envelopes, payload registry, artifact schemas, proposal sufficiency gates, persistence model |
| `030–039` | Trust, Identity, and Authority | Identify, Attest, authority, delegation, standing, recusal, revocation |
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

Each RFC SHOULD declare one base status.

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

### 5.1 Status Version Qualifiers

The controlled status value is the base word, such as `Draft`, `Candidate`, or `Reserved`.

The RFC index MAY append a version qualifier to a base status when the current draft version is known and useful for orientation.

Examples:

```text
Draft v0.5
Draft v1.3
```

This does not create a separate status taxonomy. `Draft v0.5` is a version-qualified `Draft`.

The Series Index does not use a separate `Version` column. Version precision remains part of the Status cell when needed.

### 5.2 Recommended Header

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
| `000` | Series Index | `RFC-CDP-000-Series-Index.md` | Draft v1.3 |
| `001` | Vision, Scope, and Principles | `RFC-CDP-001-Vision-Scope-Principles.md` | Draft v0.6 |
| `002` | Anti-Premature-Certainty Principle | `RFC-CDP-002-Anti-Premature-Certainty-Principle.md` | Draft v0.2 |

### 6.2 Reference Architecture

| RFC | Title | File | Status |
|---:|---|---|---|
| `010` | Reference Architecture | `RFC-CDP-010-Reference-Architecture.md` | Draft |

### 6.3 Core Objects and Schemas

| RFC | Title | File | Status |
|---:|---|---|---|
| `020` | Decision Object Schema | `RFC-CDP-020-Decision-Object-Schema.md` | Draft |
| `021` | Wire Message Envelope Schema | `RFC-CDP-021-Envelope-Schema.md` | Draft v0.4 |
| `022` | Protocol Payload Schema Registry | `RFC-CDP-022-Protocol-Payload-Schema-Registry.md` | Draft v0.5 |
| `023` | Decision Lifecycle Envelope | `RFC-CDP-023-Decision-Lifecycle-Envelope.md` | Draft v0.5 |
| `024` | Proposal Sufficiency Gate | `RFC-CDP-024-Proposal-Sufficiency-Gate.md` | Draft v0.1 |
| `025` | CDP Persistence Model | `RFC-CDP-025-CDP-Persistence-Model.md` | Draft v0.2 |

### 6.4 Trust, Identity, and Authority

| RFC | Title | File | Status |
|---:|---|---|---|
| `030` | Identify Protocol | `RFC-CDP-030-Identify-Protocol.md` | Draft |
| `031` | Attest Protocol | `RFC-CDP-031-Attest-Protocol.md` | Draft |
| `032` | Authority and Delegation Model | `RFC-CDP-032-Authority-and-Delegation-Model.md` | Draft |
| `033` | Standing and Recusal Model | `RFC-CDP-033-Standing-and-Recusal-Model.md` | Draft v0.4 |

### 6.5 Lifecycle Protocols

| RFC | Title | File | Status |
|---:|---|---|---|
| `040` | Nemawashi Protocol | `RFC-CDP-040-Nemawashi-Protocol.md` | Draft |
| `041` | Propose Protocol | `RFC-CDP-041-Propose-Protocol.md` | Draft v0.4 |
| `042` | Challenge Protocol | `RFC-CDP-042-Challenge-Protocol.md` | Draft v0.4 |
| `043` | Test Protocol | `RFC-CDP-043-Test-Protocol.md` | Draft |
| `044` | Adjudicate Protocol | `RFC-CDP-044-Adjudicate-Protocol.md` | Draft |
| `045` | Legitimize Protocol | `RFC-CDP-045-Legitimize-Protocol.md` | Draft v0.5 |
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
| `070` | Appeals and Contestability Model | `RFC-CDP-070-Appeals-and-Contestability-Model.md` | Draft v0.1 |
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

## 7. Proposal Sufficiency Gate

RFC-CDP-024 defines the Proposal Sufficiency Gate.

Definition:

> Proposal Sufficiency Gate defines the minimum formation requirements a proposal must satisfy before entering the CDP challenge lifecycle.

This gate is not a substitute for Challenge, Test, Adjudicate, or Legitimize.

It answers a narrower upstream question:

> Has this proposal earned the right to be heard?

A sufficient proposal may still be challenged, tested, adjudicated against, rejected, appealed, or repaired.

An insufficient proposal has not yet met the minimum bar to enter the governed challenge lifecycle.

---

## 8. CDP Persistence Spine

RFC-CDP-025 defines the minimum queryable persistence substrate for CDP.

Current Draft v0.2 includes:

- `cdp_decision_envelope`
- `cdp_governed_record`
- `cdp_standing_record`
- `cdp_envelope_ref`
- `cdp_payload_registry`
- `cdp_event_log`
- `cdp_lookup`
- `cdp_controlled_vocabulary`

The persistence model uses current-state tables for queryability and an append-only event log for audit and replay.

Standing persistence uses a two-layer model:

```text
cdp_governed_record
  canonical standing artifact

cdp_standing_record
  queryable enforcement projection
```

---

## 9. Repair, Reparations, and Rematriation Spine

The current repair/remedy corpus includes:

| RFC | Function |
|---:|---|
| `053` | Determines when rollback, mitigation, or compensation is triggered and how those paths are tracked. |
| `054` | Defines the actual compensation/remedy mechanism: claim, harm assessment, remedy proposal, authorization, delivery, sufficiency review. |
| `070` | Defines constitutional entry into appeal and contestability review. |
| `071` | Defines the constitutional repair protocol and anti-flattening requirements for enumerated repair agendas. |
| `072` | Defines the objects that preserve breach, repair agenda, repair point, response, commitment, evidence, review, and dissent. |
| `073` | Defines affected-party review, anti-erasure, closure blocking, and contestability. |
| `074` | Defines sovereignty claims and authority pluralism. |
| `075` | Reserved for rematriation, land/resource return, and return-to-right-relationship mechanisms. |
| `092` | Defines the repair state machine. |

This spine supports reparations and rematriation-capable governance by preserving harm, authority, affected-party review, sovereignty claims, remedy mechanisms, return obligations, completion evidence, and learning.

---

## 10. Legacy Mapping

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

## 11. How to Add a New RFC

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

## 12. Promotion Rules

A staging draft MAY be promoted to canonical when:

- it has a stable title;
- it has an assigned canonical number;
- it fits a numbering band;
- it does not collide with an existing canonical RFC;
- dependencies are declared;
- any legacy filename is recorded in this index;
- the file is placed in `rfc/`.

Promotion SHOULD preserve history where possible. If repository tooling cannot preserve history through a true move, the promotion record MUST be preserved in this index.

### 12.1 Collaboration-to-Canon Path

Working material in `collab/` is not canonical by default.

The expected promotion path is:

```text
collab session -> challenge memo -> moderator adjudication -> RFC/schema update
```

A collaboration artifact may be promoted only when:

1. the moderator records the decision;
2. the canonical target is named;
3. the promoted text is rewritten for RFC form;
4. unresolved dissent is either resolved, preserved, or explicitly deferred;
5. this Series Index is updated if a new RFC number or status changes.

---

## 13. Supersession and Deprecation

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

## 14. Constitutional Invariant

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

## 15. Summary

This Series Index is the canonical map for the CDP RFC corpus.

It defines the numbering bands, canonical files, folder policy, status taxonomy, legacy mapping, promotion rules, collaboration-to-canon path, persistence spine, and repair/remedy spine needed to keep the protocol suite legible, auditable, contestable, enforceable, and repairable over time.
