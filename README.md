# CDP — Constitutional Decision Plane

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-early--stage-orange)]()
[![Protocol](https://img.shields.io/badge/protocol-RFC--driven-purple)]()
[![Focus](https://img.shields.io/badge/focus-decision%20governance-black)]()

**A constitutional decision plane for resilient decisions across synthetic, human, and institutional systems.**

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

CDP introduces governance infrastructure for decisions—  
the same way Kubernetes introduced control planes for compute.

> **Adversarial process produces legitimate decisions.**

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

---

## Architecture

CDP is composed of layered governance infrastructure:

1. **Constitutional Constraint Layer**  
   Non-bypassable rules

2. **Governance Protocol**  
   Proposal → Challenge → Adjudication → Legitimacy

3. **Governance State Machine**  
   Formal lifecycle of decisions

4. **Event Log & Replay**  
   Immutable decision history

5. **Identity & Attestation**  
   Who acted, and with what authority

6. **Execution Authorization**  
   No execution without legitimacy

---

## Visuals

### CDP vs Traditional Systems
![Internet vs CDP](https://github.com/AndieWill510/ccp/blob/main/drawings/ccp_internet_vs_decisions.jpg)

### Governance State Machine
![State Machine](https://github.com/AndieWill510/ccp/blob/main/drawings/ccp_governance_state_machine.jpg)

### Protocol Suite
![Protocol](https://github.com/AndieWill510/ccp/blob/main/drawings/ccp_protocol_suite.jpg)

---

## Design Principles

### Contestability
All decisions must be challengeable.

### Falsifiability
Claims must be testable before execution.

### Constitutional Constraint
Authority operates within non-bypassable limits.

### Transparency
Every decision produces an auditable transcript.

### Learning
Failure strengthens the system.

---

## RFC Series

The protocol is defined via RFCs in `/rfc`:

- RFC-CDP-001 — Architecture  
- RFC-CDP-002 — Attestation  
- RFC-CDP-003 — Decision Transcript  
- RFC-CDP-004 — Governance API  
- RFC-CDP-005 — Appeals  
- RFC-CDP-006 — Policy Language  
- RFC-CDP-007 — Observability  
- RFC-CDP-008 — Identity  
- RFC-CDP-009 — Consensus  
- RFC-CDP-010 — State Machine  
- RFC-CDP-011 — Event Log  
- RFC-CDP-012 — Recovery  
- RFC-CDP-013 — Constraint Layer  
- RFC-CDP-014 — Legitimacy  

---

## Status

Early-stage, RFC-driven.

Current:
- Protocol definitions
- Reference architecture
- Local-first implementation (FastAPI + Postgres)

Planned:
- Governance kernel
- Simulation environments
- Federated governance
- Production-grade identity + attestation

---

## Getting Started

```bash
git clone https://github.com/AndieWill510/cdp
cd cdp
cp .env.example .env
docker compose up --build
