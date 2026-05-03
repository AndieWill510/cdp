# RFC-CDP Index and Renaming Proposal

Author: Kevin “Andie” Williams / ChatGPT
Status: Draft Proposal
Series: Constitutional Decision Plane (CDP)
Date: May 3, 2026

## Abstract

This document proposes a revised numbering and naming convention for the CDP RFC corpus. The current corpus is valuable but has accreted quickly: lifecycle protocols, cross-cutting trust protocols, schemas, APIs, and state machines currently sit in a mostly chronological sequence. That makes sense historically, but it makes the corpus harder to navigate as a protocol suite.

This proposal keeps the existing conceptual backbone while introducing reserved numeric bands, clearer file names, and a stable index structure.

## 1. Findings

The canonical `rfc/` folder currently contains a 20-document starter set ordered as:

- vision/scope
- architecture
- lifecycle protocols
- schemas
- APIs
- state machines

That order is buildable, but it mixes different document classes:

- constitutional / framing documents
- reference architecture
- lifecycle protocols
- trust and authority protocols
- wire schemas
- API surfaces
- state machines

The current `rfcs/` plural folder was not found on `main` during this review. If it exists on another branch or locally, it should either be migrated into `rfc/` or treated as deprecated.

## 2. Proposed Numbering Bands

Use numeric bands so readers can infer document type from the number.

| Range | Band | Purpose |
|---:|---|---|
| 000–009 | Series / Constitutional Frame | index, vision, scope, principles, terminology |
| 010–019 | Architecture | reference architecture, topology, layers, threat model |
| 020–029 | Core Objects and Schemas | Decision object, Envelope, payload registry, artifact schemas |
| 030–039 | Trust, Identity, and Authority | Identify, Attest, authority, delegation, revocation |
| 040–049 | Lifecycle Protocols | Nemawashi, Propose, Challenge, Test, Adjudicate, Legitimize, Execute, Record, Learn |
| 050–059 | Review, Appeal, Repair, and Exception Handling | escalation, appeal, rollback, dissent preservation, harm repair |
| 060–069 | APIs and Transports | governance API, deliberation API, event stream, webhooks |
| 070–079 | State Machines | governance lifecycle, execution lifecycle, terminal states |
| 080–089 | Implementation Profiles | local-first, enterprise, public-sector, synthetic-agent profiles |
| 090–099 | Security, Audit, and Compliance | audit profile, privacy, retention, evidence handling |
| 100+ | Extensions | domain-specific or experimental RFCs |

## 3. Proposed Canonical Index

| New # | Proposed File | Current File | Rationale |
|---:|---|---|---|
| 000 | `RFC-CDP-000-Series-Index.md` | `README.md` | Make the index a first-class RFC-like document. |
| 001 | `RFC-CDP-001-Vision-Scope-Principles.md` | `RFC-CDP-000-Vision-Scope-Principles.md` | Constitutional frame remains first normative document. |
| 010 | `RFC-CDP-010-Reference-Architecture.md` | `RFC-CDP-001-Architecture.md` | Architecture belongs in its own reserved band. |
| 020 | `RFC-CDP-020-Decision-Object-Schema.md` | `RFC-CDP-013-Decision-Schema.md` | Decision is the core governed object and should precede wire protocols. |
| 021 | `RFC-CDP-021-Envelope-Schema.md` | `RFC-CDP-014-Envelope-Schema.md` | Envelope is the universal message wrapper. |
| 022 | `RFC-CDP-022-Protocol-Payload-Schema-Registry.md` | `RFC-CDP-015-Protocol-Payload-Schemas.md` | Rename as registry to avoid suggesting a monolithic schema blob. |
| 030 | `RFC-CDP-030-Identify-Protocol.md` | `RFC-CDP-012-Identify-Protocol.md` | Identity is cross-cutting and should precede authority-bearing acts. |
| 031 | `RFC-CDP-031-Attest-Protocol.md` | `RFC-CDP-011-Attest-Protocol.md` | Attestation binds authority to acts. |
| 040 | `RFC-CDP-040-Nemawashi-Protocol.md` | `RFC-CDP-010-Nemawashi-Protocol.md` | Nemawashi is pre-formal and continuous, so it leads lifecycle protocols. |
| 041 | `RFC-CDP-041-Propose-Protocol.md` | `RFC-CDP-002-Propose-Protocol.md` | Lifecycle starts with proposal. |
| 042 | `RFC-CDP-042-Challenge-Protocol.md` | `RFC-CDP-003-Challenge-Protocol.md` | Challenge follows proposal. |
| 043 | `RFC-CDP-043-Test-Protocol.md` | `RFC-CDP-004-Test-Protocol.md` | Testing follows challenge or policy need. |
| 044 | `RFC-CDP-044-Adjudicate-Protocol.md` | `RFC-CDP-005-Adjudicate-Protocol.md` | Judgment follows deliberation/test. |
| 045 | `RFC-CDP-045-Legitimize-Protocol.md` | `RFC-CDP-006-Legitimize-Protocol.md` | Legitimacy gates execution. |
| 046 | `RFC-CDP-046-Execute-Protocol.md` | `RFC-CDP-007-Execute-Protocol.md` | Execution follows legitimacy. |
| 047 | `RFC-CDP-047-Record-Protocol.md` | `RFC-CDP-008-Record-Protocol.md` | Recording follows execution or terminal disposition. |
| 048 | `RFC-CDP-048-Learn-Protocol.md` | `RFC-CDP-009-Learn-Protocol.md` | Learning closes the cycle. |
| 060 | `RFC-CDP-060-Governance-API.md` | `RFC-CDP-016-Governance-API.md` | API surface belongs in transport/interface band. |
| 061 | `RFC-CDP-061-Deliberation-API.md` | `RFC-CDP-017-Deliberation-API.md` | Pair with governance API. |
| 070 | `RFC-CDP-070-Governance-State-Machine.md` | `RFC-CDP-018-Governance-State-Machine.md` | State machines should be separated from protocols. |
| 071 | `RFC-CDP-071-Execution-State-Machine.md` | `RFC-CDP-019-Execution-State-Machine.md` | Execution state machine belongs beside governance state machine. |

## 4. Naming Rules

Recommended filename pattern:

```text
RFC-CDP-<NNN>-<Kebab-Case-Title>.md
```

Rules:

1. Use three-digit numbers forever.
2. Reserve numeric bands; do not compact numbers after deletion.
3. Prefer nouns for schemas and state machines.
4. Prefer verbs for lifecycle protocols.
5. Use `Protocol` only for governed act semantics.
6. Use `API` only for external interface surfaces.
7. Use `Schema` for normative structures and `Registry` for enumerated families.
8. Keep `README.md` as human landing page, but point it to `RFC-CDP-000-Series-Index.md`.

## 5. Migration Strategy

Recommended migration should be non-destructive and auditable.

Phase 1: Add the new index and this proposal.

Phase 2: Rename files using `git mv` so GitHub preserves history.

Phase 3: Update intra-RFC references.

Phase 4: Add redirects or a legacy mapping table in `README.md`.

Phase 5: Open a release tag such as `v0.4-indexed`.

## 6. Design Judgment

The strongest structural change is moving schemas before protocols. CDP repeatedly says that the Decision is the governed object, the Envelope is the universal wrapper, and protocols provide motion. The index should reflect that architecture:

```text
Frame → Architecture → Objects/Schemas → Trust → Lifecycle → APIs → State Machines → Profiles
```

This gives CDP a more IETF-like spine and makes future growth easier without renumbering churn.

## 7. Open Questions

1. Should `Nemawashi` remain a lifecycle protocol, or should it become a social-governance substrate in the 030 trust/authority band?
2. Should appeals, rollback, and repair become separate RFCs in the 050 band?
3. Should the payload schema document be split into one schema RFC per lifecycle protocol once implementation begins?
4. Should `README.md` remain prose-only, or should it become generated from the canonical index?

## 8. Recommended Immediate Next Step

Create `RFC-CDP-000-Series-Index.md` and update `README.md` to point to it. Do not rename the full corpus until references are checked and a branch/PR can preserve reviewability.
