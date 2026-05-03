# RFC-CDP Index and Renaming Proposal v2

Author: Kevin “Andie” Williams / ChatGPT
Status: Draft Proposal v2
Series: Constitutional Decision Plane (CDP)
Date: May 3, 2026
Supersedes: `rfc/RFC-CDP-INDEX-RENAMING-PROPOSAL-2026-05-03.md`

## Abstract

This document revises the CDP RFC index and renaming proposal after including both the canonical `rfc/` corpus and the newly added `rfcs/` material.

The first proposal assumed only the canonical 20-document `rfc/` set. The `rfcs/` folder now adds important reconstructed and extension work:

- `RFC-CDP-007A-Decision-Type-Maturity-and-Queued-Execution-Gates.md`
- `RFC-CDP-011-Covenant-AIITL.md`
- `RFC-CDP-012-Presence-Bound-Execution-Authority.md`
- `RFC-CDP-013-Twenty-Points-Repair-Protocol.md`
- `chat-rfc-cdp-artifact-index-2026-05-03.md`

These documents are not just appendices. They reveal three additional constitutional axes that the original numbering proposal under-modeled:

1. **Covenant / AIITL relationship governance**
2. **Execution authority and maturity gates**
3. **Repair, sovereignty, and historic breach handling**

Therefore v2 introduces a stronger multi-track numbering system that separates the canonical protocol spine from constitutional extensions and repair protocols.

---

## 1. Findings

### 1.1 Canonical `rfc/` Corpus

The `rfc/` folder contains a coherent 20-document starter set ordered approximately as:

```text
Vision / Scope → Architecture → Lifecycle Protocols → Trust Protocols → Schemas → APIs → State Machines
```

This is historically sensible but architecturally mixed.

The canonical set includes:

- `000` Vision, Scope, Principles
- `001` Architecture
- `002–010` Lifecycle and Nemawashi protocols
- `011–012` Attest and Identify
- `013–015` Decision, Envelope, Payload schemas
- `016–017` APIs
- `018–019` State machines

### 1.2 Added `rfcs/` Corpus

The `rfcs/` folder adds reconstructed work that does not fit neatly into the original 000–019 spine:

| File | Core contribution |
|---|---|
| `RFC-CDP-007A-Decision-Type-Maturity-and-Queued-Execution-Gates.md` | Maturity-aware execution gating; queue-based supervised automation; first-N review; graduation/demotion. |
| `RFC-CDP-011-Covenant-AIITL.md` | Covenant Protocol; AI-in-the-Loop as bounded constitutional role; schema-drift detection; relational governance. |
| `RFC-CDP-012-Presence-Bound-Execution-Authority.md` | Presence Grants; execution authority as time-bound, scoped, non-replayable, challenge-aware authority. |
| `RFC-CDP-013-Twenty-Points-Repair-Protocol.md` | Enumerated repair agendas; sovereignty-aware repair claims; breach records; anti-erasure requirements. |
| `chat-rfc-cdp-artifact-index-2026-05-03.md` | Provenance/index note for recovered ChatGPT artifacts. |

### 1.3 Numbering Collisions

There are conceptual and numeric collisions:

- Canonical `rfc/RFC-CDP-011-Attest-Protocol.md` conflicts numerically with `rfcs/RFC-CDP-011-Covenant-AIITL.md`.
- Canonical `rfc/RFC-CDP-012-Identify-Protocol.md` conflicts numerically with `rfcs/RFC-CDP-012-Presence-Bound-Execution-Authority.md`.
- Canonical `rfc/RFC-CDP-013-Decision-Schema.md` conflicts numerically with `rfcs/RFC-CDP-013-Twenty-Points-Repair-Protocol.md`.
- `RFC-CDP-007A` is a useful extension pattern but should become a proper numbered extension rather than an alpha suffix once promoted.

These collisions are not failures. They are evidence of real growth. The system has outgrown a single linear numbering path.

---

## 2. Design Goal

The new index should make CDP legible as a protocol suite, not merely a chronological pile of drafts.

The numbering should answer, at a glance:

1. Is this foundational?
2. Is this architecture?
3. Is this a schema/object?
4. Is this trust/authority?
5. Is this a lifecycle verb?
6. Is this an execution-control extension?
7. Is this covenant/AIITL/relationship governance?
8. Is this repair/appeal/sovereignty/harm handling?
9. Is this an API/transport?
10. Is this a state machine?

---

## 3. Proposed Numbering Bands v2

| Range | Band | Purpose |
|---:|---|---|
| `000–009` | Series / Constitutional Frame | index, vision, scope, principles, terminology, doctrine |
| `010–019` | Reference Architecture | architecture, topology, layers, threat model, trust model |
| `020–029` | Core Objects and Schemas | Decision object, Envelope, payload registry, artifact schemas |
| `030–039` | Trust, Identity, and Authority | Identify, Attest, authority, delegation, revocation |
| `040–049` | Lifecycle Protocols | Nemawashi, Propose, Challenge, Test, Adjudicate, Legitimize, Execute, Record, Learn |
| `050–059` | Execution Control Extensions | queued execution, decision-type maturity, presence-bound authority, kill switch, rollback controls |
| `060–069` | Covenant and AIITL | covenant protocol, AIITL/HITL, schema drift, consentful collaboration, relational duties |
| `070–079` | Repair, Appeal, and Sovereignty | appeals, repair agendas, breach records, affected-party review, anti-erasure, sovereignty claims |
| `080–089` | APIs and Transports | governance API, deliberation API, event streams, webhooks, SDK profiles |
| `090–099` | State Machines | governance lifecycle, execution lifecycle, repair lifecycle, covenant lifecycle |
| `100–119` | Security, Audit, and Compliance | privacy, evidence handling, retention, audit profiles, compliance mappings |
| `120–149` | Implementation Profiles | local-first, enterprise, public sector, synthetic-agent, cloud-neutral deployment profiles |
| `150+` | Extensions / Experimental | domain-specific or experimental RFCs |

---

## 4. Proposed Canonical Index v2

### 4.1 Series and Foundation

| New # | Proposed File | Source |
|---:|---|---|
| `000` | `RFC-CDP-000-Series-Index.md` | Promote from `rfc/README.md` and artifact index material |
| `001` | `RFC-CDP-001-Vision-Scope-Principles.md` | `rfc/RFC-CDP-000-Vision-Scope-Principles.md` |

### 4.2 Architecture

| New # | Proposed File | Source |
|---:|---|---|
| `010` | `RFC-CDP-010-Reference-Architecture.md` | `rfc/RFC-CDP-001-Architecture.md` |

### 4.3 Core Objects and Schemas

| New # | Proposed File | Source |
|---:|---|---|
| `020` | `RFC-CDP-020-Decision-Object-Schema.md` | `rfc/RFC-CDP-013-Decision-Schema.md` |
| `021` | `RFC-CDP-021-Envelope-Schema.md` | `rfc/RFC-CDP-014-Envelope-Schema.md` |
| `022` | `RFC-CDP-022-Protocol-Payload-Schema-Registry.md` | `rfc/RFC-CDP-015-Protocol-Payload-Schemas.md` |

### 4.4 Trust, Identity, and Authority

| New # | Proposed File | Source |
|---:|---|---|
| `030` | `RFC-CDP-030-Identify-Protocol.md` | `rfc/RFC-CDP-012-Identify-Protocol.md` |
| `031` | `RFC-CDP-031-Attest-Protocol.md` | `rfc/RFC-CDP-011-Attest-Protocol.md` |
| `032` | `RFC-CDP-032-Authority-and-Delegation-Model.md` | New / split from Identify, Attest, Presence |

### 4.5 Lifecycle Protocols

| New # | Proposed File | Source |
|---:|---|---|
| `040` | `RFC-CDP-040-Nemawashi-Protocol.md` | `rfc/RFC-CDP-010-Nemawashi-Protocol.md` |
| `041` | `RFC-CDP-041-Propose-Protocol.md` | `rfc/RFC-CDP-002-Propose-Protocol.md` |
| `042` | `RFC-CDP-042-Challenge-Protocol.md` | `rfc/RFC-CDP-003-Challenge-Protocol.md` |
| `043` | `RFC-CDP-043-Test-Protocol.md` | `rfc/RFC-CDP-004-Test-Protocol.md` |
| `044` | `RFC-CDP-044-Adjudicate-Protocol.md` | `rfc/RFC-CDP-005-Adjudicate-Protocol.md` |
| `045` | `RFC-CDP-045-Legitimize-Protocol.md` | `rfc/RFC-CDP-006-Legitimize-Protocol.md` |
| `046` | `RFC-CDP-046-Execute-Protocol.md` | `rfc/RFC-CDP-007-Execute-Protocol.md` |
| `047` | `RFC-CDP-047-Record-Protocol.md` | `rfc/RFC-CDP-008-Record-Protocol.md` |
| `048` | `RFC-CDP-048-Learn-Protocol.md` | `rfc/RFC-CDP-009-Learn-Protocol.md` |

### 4.6 Execution Control Extensions

| New # | Proposed File | Source |
|---:|---|---|
| `050` | `RFC-CDP-050-Decision-Type-Maturity-and-Queued-Execution-Gates.md` | `rfcs/RFC-CDP-007A-Decision-Type-Maturity-and-Queued-Execution-Gates.md` |
| `051` | `RFC-CDP-051-Presence-Bound-Execution-Authority.md` | `rfcs/RFC-CDP-012-Presence-Bound-Execution-Authority.md` |
| `052` | `RFC-CDP-052-Emergency-Override-and-Kill-Switch.md` | New / split from Presence and Execute |
| `053` | `RFC-CDP-053-Rollback-and-Compensation-Protocol.md` | New / split from execution state machine and repair work |

### 4.7 Covenant and AIITL

| New # | Proposed File | Source |
|---:|---|---|
| `060` | `RFC-CDP-060-Covenant-Protocol-and-AIITL.md` | `rfcs/RFC-CDP-011-Covenant-AIITL.md` |
| `061` | `RFC-CDP-061-Schema-Drift-and-Context-Preservation.md` | New / split from Covenant |
| `062` | `RFC-CDP-062-HITL-AIITL-Role-Boundaries.md` | New / split from Covenant |

### 4.8 Repair, Appeal, and Sovereignty

| New # | Proposed File | Source |
|---:|---|---|
| `070` | `RFC-CDP-070-Appeals-and-Contestability-Model.md` | New / older CCP material likely candidate |
| `071` | `RFC-CDP-071-Twenty-Points-Repair-Protocol.md` | `rfcs/RFC-CDP-013-Twenty-Points-Repair-Protocol.md` |
| `072` | `RFC-CDP-072-Breach-Record-and-Repair-Agenda-Schema.md` | New / split from Twenty Points Repair |
| `073` | `RFC-CDP-073-Affected-Party-Review-and-Anti-Erasure.md` | New / split from Twenty Points Repair |
| `074` | `RFC-CDP-074-Sovereignty-Claims-and-Authority-Pluralism.md` | New / split from Twenty Points Repair |

### 4.9 APIs and Transports

| New # | Proposed File | Source |
|---:|---|---|
| `080` | `RFC-CDP-080-Governance-API.md` | `rfc/RFC-CDP-016-Governance-API.md` |
| `081` | `RFC-CDP-081-Deliberation-API.md` | `rfc/RFC-CDP-017-Deliberation-API.md` |
| `082` | `RFC-CDP-082-Event-Stream-and-Subscription-API.md` | New / split from APIs and Record |

### 4.10 State Machines

| New # | Proposed File | Source |
|---:|---|---|
| `090` | `RFC-CDP-090-Governance-State-Machine.md` | `rfc/RFC-CDP-018-Governance-State-Machine.md` |
| `091` | `RFC-CDP-091-Execution-State-Machine.md` | `rfc/RFC-CDP-019-Execution-State-Machine.md` |
| `092` | `RFC-CDP-092-Repair-State-Machine.md` | New / derived from Twenty Points Repair |
| `093` | `RFC-CDP-093-Covenant-State-Machine.md` | New / derived from Covenant |

---

## 5. Why v2 Changes the Original Proposal

The first proposal correctly noticed that schemas should move before lifecycle protocols. That remains true.

But the newly added `rfcs/` material shows that CDP is not only a decision protocol suite. It is becoming a constitutional operating model with at least four planes:

```text
Decision Plane
Execution Plane
Covenant Plane
Repair Plane
```

The numbering should honor those planes.

### 5.1 Decision Plane

The Decision Plane governs ordinary lifecycle flow:

```text
Nemawashi → Propose → Challenge → Test → Adjudicate → Legitimize → Execute → Record → Learn
```

### 5.2 Execution Plane

The Execution Plane prevents legitimacy from becoming automatic action:

```text
Maturity Gate → Queue / Review → Presence Grant → Execute → Record → Learn
```

### 5.3 Covenant Plane

The Covenant Plane governs relationship and participation between humans, institutions, and AI systems:

```text
Witness → Challenge → Clarify → Hold Boundaries → Record → Repair
```

### 5.4 Repair Plane

The Repair Plane handles historic breach, sovereignty claims, enumerated demands, and institutional repair:

```text
Repair Agenda → Point Preservation → Response → Contestation → Commitment → Evidence → Learning
```

---

## 6. Recommended Folder Policy

The repo currently has both `rfc/` and `rfcs/`.

Recommended policy:

| Folder | Purpose |
|---|---|
| `rfc/` | Canonical accepted/promoted RFCs and index proposals |
| `rfcs/` | Recovered drafts, candidate RFCs, and staging material |

Alternative policy:

| Folder | Purpose |
|---|---|
| `rfcs/` | All RFCs, following common open-source convention |
| `rfc/` | Deprecated legacy folder |

Preferred recommendation: **keep `rfc/` canonical for now** because it already contains the 20-document starter set, but add a clear `README.md` note that `rfcs/` is the staging/recovered-draft lane until migration.

Do not maintain two canonical RFC folders long-term. That will create schema drift in the repo itself. Tiny goblin with a clipboard, but real.

---

## 7. Naming Rules v2

Recommended filename pattern:

```text
RFC-CDP-<NNN>-<Kebab-Case-Title>.md
```

Rules:

1. Use three-digit numbers forever.
2. Reserve numeric bands; do not compact after deletion.
3. Avoid alpha suffixes such as `007A` in canonical files. Use proper extension bands instead.
4. Keep alpha suffixes only for staging drafts if needed.
5. Prefer nouns for schemas, registries, state machines, and models.
6. Prefer verbs for lifecycle protocols.
7. Use `Protocol` only when the RFC defines governed act semantics.
8. Use `API` only for external interface surfaces.
9. Use `Model` for conceptual/normative structures that are not wire protocols.
10. Use `Schema` for normative object structures.
11. Use `Registry` for enumerated families, payload families, or controlled vocabularies.
12. Include `Supersedes`, `Updates`, and `Depends On` headers in every RFC after promotion.

---

## 8. Migration Strategy v2

### Phase 1: Stabilize Index

- Create `RFC-CDP-000-Series-Index.md`.
- Update `rfc/README.md` to distinguish canonical and staging material.
- Mark this file as the current renaming proposal.

### Phase 2: Promote Staging RFCs

Promote these from `rfcs/` into canonical numbering:

| Current | Promote as |
|---|---|
| `RFC-CDP-007A-Decision-Type-Maturity-and-Queued-Execution-Gates.md` | `RFC-CDP-050-Decision-Type-Maturity-and-Queued-Execution-Gates.md` |
| `RFC-CDP-011-Covenant-AIITL.md` | `RFC-CDP-060-Covenant-Protocol-and-AIITL.md` |
| `RFC-CDP-012-Presence-Bound-Execution-Authority.md` | `RFC-CDP-051-Presence-Bound-Execution-Authority.md` |
| `RFC-CDP-013-Twenty-Points-Repair-Protocol.md` | `RFC-CDP-071-Twenty-Points-Repair-Protocol.md` |

### Phase 3: Rename Canonical RFCs

Use `git mv` on a branch, not ad hoc delete/create, so history remains reviewable.

### Phase 4: Update References

Update all internal references from old numbers to new numbers.

For example:

| Old reference | New reference |
|---|---|
| `RFC-CDP-007` Execute | `RFC-CDP-046` Execute |
| `RFC-CDP-008` Record | `RFC-CDP-047` Record |
| `RFC-CDP-009` Learn | `RFC-CDP-048` Learn |
| `RFC-CDP-011` Attest | `RFC-CDP-031` Attest |
| `RFC-CDP-012` Identify | `RFC-CDP-030` Identify |
| `RFC-CDP-013` Decision Schema | `RFC-CDP-020` Decision Object Schema |

### Phase 5: Release Tag

Tag the migration as:

```text
v0.4-indexed
```

---

## 9. Open Questions

1. Should `rfc/` or `rfcs/` be the final canonical folder?
2. Should Covenant be a `060` band peer plane, or should it become `002` because it is doctrinally foundational?
3. Should Twenty Points Repair remain one RFC, or split into schema, protocol, and state-machine RFCs immediately?
4. Should Presence-Bound Execution Authority live under trust/authority (`030`) or execution control (`050`)?
5. Should old `RFC-CCP-*` material be mined into `100+` experimental RFCs or normalized into the new numbered bands?

---

## 10. Recommendation

Adopt the v2 banded numbering scheme.

Do not force all CDP work into one linear lifecycle. The repo now contains enough material to show CDP has at least four distinct but interoperating planes:

```text
Decision Plane
Execution Plane
Covenant Plane
Repair Plane
```

The canonical index should make those planes legible.

Recommended next action:

1. Create `RFC-CDP-000-Series-Index.md`.
2. Promote the four `rfcs/` drafts into canonical bands.
3. Use a single branch and `git mv` to rename the old canonical files.
4. Preserve a legacy mapping table permanently.

A constitutional system should remember its own renamings. Otherwise the governance framework starts by gaslighting its own file tree, which is funny for about nine seconds and then becomes architecture debt.
