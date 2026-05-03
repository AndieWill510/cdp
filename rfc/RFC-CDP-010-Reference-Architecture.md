# RFC-CDP-001 — Architecture

Author: Kevin “Andie” Williams  
Status: Draft v0.3  
Series: Constitutional Decision Plane (CDP)  
Date: March 17, 2026

## Abstract
This document defines the major layers, reference topology, and cross-cutting trust functions of CDP.

## 1. Purpose
The Architecture RFC answers:
- what the major layers are;
- how Decision Kernel, Nemawashi, Legitimacy, Record, and cross-cutting trust fit together;
- what a minimal and fuller topology look like.

## 2. Architectural Layers
### 2.1 Decision Kernel
The Decision Kernel stores and mutates the canonical Decision object. It is the center of state.

### 2.2 Protocol Layer
The Protocol Layer validates acts such as Propose, Challenge, Test, Adjudicate, Legitimize, Execute, Record, and Learn.

### 2.3 Legitimacy Layer
The Legitimacy Layer determines whether a judged decision is institutionally enactable.

### 2.4 Nemawashi Layer
The Nemawashi Layer manages stakeholder surfacing, readiness, friction, and pre-formal alignment.

### 2.5 Record Layer
The Record Layer preserves lineage, evidence refs, transcripts, outcomes, and replay artifacts.

### 2.6 Learning Layer
The Learning Layer transforms outcomes into precedent, policy revision, and governance improvement.

## 3. Cross-Cutting Trust Functions
- identity;
- attestation;
- integrity verification;
- authority resolution;
- rate limiting and friction controls;
- replay and audit;
- escalation and appeals.

## 4. Reference Topology
A minimal implementation MAY consist of:
- FastAPI or equivalent service surface;
- SQLite or local Postgres;
- append-only envelope/event log;
- local file or object store for artifacts;
- local policy module.

A fuller implementation MAY add:
- search index;
- vector store for precedent similarity;
- message bus;
- external trust registry;
- policy engine such as OPA or Cedar.

## 5. Data Flow
1. Client submits Envelope.
2. Identity and Attestation are verified.
3. Protocol-specific validation runs.
4. Decision Kernel performs state mutation.
5. Record Layer persists lineage and artifacts.
6. Learning Layer consumes recorded outcomes.

## 6. Architectural Rule
Envelope provides context. Decision provides structure. Protocols provide motion.

## 7. Failure Domains
The architecture MUST distinguish:
- validation failure;
- authority failure;
- policy failure;
- transition failure;
- execution failure;
- persistence failure.

## 8. Design Constraint
Execution speed MUST remain a function of governance confidence, not merely of system capacity.
