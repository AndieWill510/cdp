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
2. **Governance Protocol**  
3. **Governance State Machine**  
4. **Event Log & Replay**  
5. **Identity & Attestation**  
6. **Execution Authorization**

---

## RFC Series

The CDP protocol is defined via RFCs in `/rfc`:

### Foundations
- RFC-CDP-000 — Vision, Scope, Principles  
- RFC-CDP-001 — Architecture  

### Core Governance Protocols
- RFC-CDP-002 — Propose Protocol  
- RFC-CDP-003 — Challenge Protocol  
- RFC-CDP-004 — Test Protocol  
- RFC-CDP-005 — Adjudicate Protocol  
- RFC-CDP-006 — Legitimize Protocol  
- RFC-CDP-007 — Execute Protocol  
- RFC-CDP-008 — Record Protocol  
- RFC-CDP-009 — Learn Protocol  

### Social + Governance Alignment
- RFC-CDP-010 — Nemawashi Protocol  

### Identity & Trust
- RFC-CDP-011 — Attest Protocol  
- RFC-CDP-012 — Identify Protocol  

### Data Models
- RFC-CDP-013 — Decision Schema  
- RFC-CDP-014 — Envelope Schema  
- RFC-CDP-015 — Protocol Payload Schemas  

### Interfaces
- RFC-CDP-016 — Governance API  
- RFC-CDP-017 — Deliberation API  

### State Machines
- RFC-CDP-018 — Governance State Machine  
- RFC-CDP-019 — Execution State Machine  

---

## Status

Early-stage, RFC-driven.

Current:
- Protocol definitions (RFC 000–019)
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
