# CDP — Constitutional Decision Plane

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-early--stage-orange)]()
[![Protocol](https://img.shields.io/badge/protocol-RFC--driven-purple)]()
[![Focus](https://img.shields.io/badge/focus-decision%20governance-black)]()

**A constitutional decision plane for resilient decisions across synthetic, human, and institutional systems.**

**Why?**

**Decisions need due process to be legitimate.**

---

## TL;DR

**CDP is a control plane for decisions.**

It makes decisions:

- contestable
- auditable
- accountable
- replayable
- legitimate

---

## Why This Exists

Modern systems can *decide*, but they cannot reliably:

- justify decisions
- withstand challenge
- produce audit trails
- enforce constraints on authority
- learn from failure

That gap is becoming a **systemic risk**, especially in AI-driven systems.

CDP introduces governance infrastructure for decisions — the same way Kubernetes introduced control planes for compute.

> **Adversarial/nemawashi processes produce legitimate decisions.**

---

## What CDP Does

CDP enables systems to:

- propose actions
- challenge decisions
- test assumptions
- adjudicate outcomes
- verify legitimacy
- execute safely
- record and replay decisions
- learn from outcomes, error, drift, and repair

---

## Architecture

CDP is composed of layered governance infrastructure:

1. **Constitutional Frame**
2. **Reference Architecture**
3. **Core Objects and Schemas**
4. **Trust, Identity, and Authority**
5. **Lifecycle Protocols**
6. **Execution Control Extensions**
7. **Covenant and AIITL Governance**
8. **Repair, Appeal, and Sovereignty**
9. **APIs and Transports**
10. **State Machines**
11. **Security, Audit, and Compliance**
12. **Implementation Profiles**

---

## The Four Planes

CDP is not only a lifecycle protocol suite. It is a constitutional operating model with four interoperating planes.

### Decision Plane

Governs ordinary decision lifecycle flow:

```text
Nemawashi → Propose → Challenge → Test → Adjudicate → Legitimize → Execute → Record → Learn
```

### Execution Plane

Prevents legitimacy from becoming automatic action:

```text
Maturity Gate → Queue / Review → Presence Grant → Execute → Record → Learn
```

### Covenant Plane

Governs relationship, participation, and bounded human-AI collaboration:

```text
Witness → Challenge → Clarify → Hold Boundaries → Record → Repair
```

### Repair Plane

Handles historic breach, sovereignty claims, enumerated demands, and institutional repair:

```text
Repair Agenda → Point Preservation → Response → Contestation → Commitment → Evidence → Learning
```

---

## The Problem With RAG

The problem with discovery-as-policy tools is not legibility. The problem is legitimacy. Retrieval can make a decision explainable without making it authorized, contestable, or valid.

**RAG makes answers traceable.**

**CDP makes decisions legitimate.**

---

## Diplomatic Pouch for Decisions

A CDP-style system says every meaningful agentic decision needs a procedural envelope:

1. Proposal — What action is being requested?
2. Standing — Who or what has authority to propose it?
3. Evidence — What data, policies, and precedents support it?
4. Challenge — What objections must be considered?
5. Adjudication — How are conflicts resolved?
6. Legitimation — Why is the final decision valid?
7. Execution — What may now happen?
8. Record — What must be preserved for audit, appeal, and learning?

That is the difference between an agent that can act and an institution that can decide.

---

## Local Development

CDP now includes a local Docker stack for laptop development.

Run from the repository root:

```bash
git clone https://github.com/AndieWill510/cdp
cd cdp
make up-build
make smoke
```

Stop the stack:

```bash
make down
```

Remove local volumes:

```bash
make down-volumes
```

The local stack includes:

- `cdp-api` — FastAPI service with `/health`
- `cdp-worker` — safe no-op worker loop
- `postgres` — Postgres with `pgvector`
- `qdrant` — vector search service
- `redis` — cache / short-lived grants
- `localstack` — local AWS service emulation

LocalStack currently bootstraps:

- S3 buckets for evidence, artifacts, and exports
- SQS queues for intake, review, execution, appeal, repair, and dead-letter handling
- EventBridge bus for CDP domain events
- DynamoDB table for idempotency / lightweight locks
- SSM parameters and Secrets Manager values for local config

See [`docker/README.md`](docker/README.md) for detailed run commands, ports, health checks, and troubleshooting.

---

## RFC Series

The CDP protocol is defined via RFCs in `/rfc` and staged/recovered drafts in `/rfcs`.

The current RFC organization follows the banded numbering proposal in:

```text
rfc/RFC-CDP-INDEX-RENAMING-PROPOSAL-2026-05-03-v2.md
```

### Folder Policy

| Folder | Purpose |
|---|---|
| `rfc/` | Canonical accepted/promoted RFCs and index proposals |
| `rfcs/` | Recovered drafts, candidate RFCs, and staging material |

The repository should not maintain two canonical RFC folders long-term. Until migration is complete, `rfc/` is the canonical lane and `rfcs/` is the staging/recovered-draft lane.

### RFC Numbering Bands

| Range | Band | Purpose |
|---:|---|---|
| `000–009` | Series / Constitutional Frame | Index, vision, scope, principles, terminology, doctrine |
| `010–019` | Reference Architecture | Architecture, topology, layers, threat model, trust model |
| `020–029` | Core Objects and Schemas | Decision object, envelope, payload registry, artifact schemas |
| `030–039` | Trust, Identity, and Authority | Identify, attest, authority, delegation, revocation |
| `040–049` | Lifecycle Protocols | Nemawashi, propose, challenge, test, adjudicate, legitimize, execute, record, learn |
| `050–059` | Execution Control Extensions | Queued execution, maturity gates, presence-bound authority, kill switch, rollback controls |
| `060–069` | Covenant and AIITL | Covenant protocol, AIITL/HITL, schema drift, consentful collaboration, relational duties |
| `070–079` | Repair, Appeal, and Sovereignty | Appeals, repair agendas, breach records, affected-party review, anti-erasure, sovereignty claims |
| `080–089` | APIs and Transports | Governance API, deliberation API, event streams, webhooks, SDK profiles |
| `090–099` | State Machines | Governance lifecycle, execution lifecycle, repair lifecycle, covenant lifecycle |
| `100–119` | Security, Audit, and Compliance | Privacy, evidence handling, retention, audit profiles, compliance mappings |
| `120–149` | Implementation Profiles | Local-first, enterprise, public sector, synthetic-agent, cloud-neutral deployment profiles |
| `150+` | Extensions / Experimental | Domain-specific or experimental RFCs |

### Proposed Canonical Index v2

#### Series and Foundation

- RFC-CDP-000 — Series Index
- RFC-CDP-001 — Vision, Scope, Principles

#### Architecture

- RFC-CDP-010 — Reference Architecture

#### Core Objects and Schemas

- RFC-CDP-020 — Decision Object Schema
- RFC-CDP-021 — Envelope Schema
- RFC-CDP-022 — Protocol Payload Schema Registry

#### Trust, Identity, and Authority

- RFC-CDP-030 — Identify Protocol
- RFC-CDP-031 — Attest Protocol
- RFC-CDP-032 — Authority and Delegation Model

#### Lifecycle Protocols

- RFC-CDP-040 — Nemawashi Protocol
- RFC-CDP-041 — Propose Protocol
- RFC-CDP-042 — Challenge Protocol
- RFC-CDP-043 — Test Protocol
- RFC-CDP-044 — Adjudicate Protocol
- RFC-CDP-045 — Legitimize Protocol
- RFC-CDP-046 — Execute Protocol
- RFC-CDP-047 — Record Protocol
- RFC-CDP-048 — Learn Protocol

#### Execution Control Extensions

- RFC-CDP-050 — Decision-Type Maturity and Queued Execution Gates
- RFC-CDP-051 — Presence-Bound Execution Authority
- RFC-CDP-052 — Emergency Override and Kill Switch
- RFC-CDP-053 — Rollback and Compensation Protocol

#### Covenant and AIITL

- RFC-CDP-060 — Covenant Protocol and AIITL
- RFC-CDP-061 — Schema Drift and Context Preservation
- RFC-CDP-062 — HITL / AIITL Role Boundaries

#### Repair, Appeal, and Sovereignty

- RFC-CDP-070 — Appeals and Contestability Model
- RFC-CDP-071 — Twenty Points Repair Protocol
- RFC-CDP-072 — Breach Record and Repair Agenda Schema
- RFC-CDP-073 — Affected-Party Review and Anti-Erasure
- RFC-CDP-074 — Sovereignty Claims and Authority Pluralism

#### APIs and Transports

- RFC-CDP-080 — Governance API
- RFC-CDP-081 — Deliberation API
- RFC-CDP-082 — Event Stream and Subscription API

#### State Machines

- RFC-CDP-090 — Governance State Machine
- RFC-CDP-091 — Execution State Machine
- RFC-CDP-092 — Repair State Machine
- RFC-CDP-093 — Covenant State Machine

---

## Naming Rules

Canonical RFC filenames should follow:

```text
RFC-CDP-<NNN>-<Kebab-Case-Title>.md
```

Rules:

1. Use three-digit numbers.
2. Reserve numeric bands; do not compact after deletion.
3. Avoid alpha suffixes such as `007A` in canonical files.
4. Keep alpha suffixes only for staging drafts if needed.
5. Prefer nouns for schemas, registries, state machines, and models.
6. Prefer verbs for lifecycle protocols.
7. Use `Protocol` only when the RFC defines governed act semantics.
8. Use `API` only for external interface surfaces.
9. Use `Model` for conceptual or normative structures that are not wire protocols.
10. Use `Schema` for normative object structures.
11. Use `Registry` for enumerated families, payload families, or controlled vocabularies.
12. Include `Supersedes`, `Updates`, and `Depends On` headers in every RFC after promotion.

---

## Migration Strategy

The v2 index recommends the following migration path:

1. Create `RFC-CDP-000-Series-Index.md`.
2. Update `rfc/README.md` to distinguish canonical and staging material.
3. Promote selected `rfcs/` drafts into canonical numbering bands.
4. Rename canonical RFCs with `git mv` on a branch so history remains reviewable.
5. Update internal references from old numbers to new numbers.
6. Preserve a permanent legacy mapping table.
7. Tag the migration as `v0.4-indexed`.

---

## Status

Early-stage, RFC-driven.

Current:

- Protocol definitions
- Reference architecture
- Local-first implementation patterns
- Local Docker stack with Postgres/pgvector, Qdrant, Redis, and LocalStack
- Minimal FastAPI `/health` endpoint
- Safe no-op worker loop
- Banded RFC index proposal v2
- Canonical/staging RFC split under review

Planned:

- Governance kernel
- Real queue consumers for intake, review, execution, appeal, and repair
- Simulation environments
- Federated governance
- Production-grade identity and attestation
- Canonical RFC migration using the v2 banded index

---

## Full Local Verification

After the local stack is built and running, run the full verification suite:

```bash
make up-build
make verify
```

`make verify` runs both:

```text
make smoke
make test
```

This verifies the Docker stack, API health endpoint, Postgres/pgvector initialization, Redis, Qdrant, and LocalStack resources.
