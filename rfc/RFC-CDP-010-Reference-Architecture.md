# RFC-CDP-010 — Reference Architecture

Author: Kevin “Andie” Williams  
Status: Draft v0.4  
Series: Constitutional Decision Plane (CDP)  
Date: May 3, 2026

## Abstract

This document defines the major planes, layers, reference topology, and cross-cutting trust functions of CDP.

CDP is a constitutional control-plane architecture for legitimate decisions, bounded execution, covenantal participation, durable record, learning, and repair.

## 1. Purpose

The Reference Architecture RFC answers:

- what the major architectural planes are;
- how the Decision Plane, Execution Plane, Covenant Plane, and Repair Plane relate;
- how Decision Kernel, Protocol Layer, Execution Control, Covenant, Repair, Record, Learning, and Trust functions fit together;
- what minimal and fuller implementation topologies look like;
- where authority, identity, attestation, presence, record, and learning are enforced.

## 2. Architectural Planes

CDP has at least four interacting planes.

### 2.1 Decision Plane

The Decision Plane governs the ordinary lifecycle of a governed Decision.

It includes:

- Nemawashi;
- Propose;
- Challenge;
- Test;
- Adjudicate;
- Legitimize;
- Execute;
- Record;
- Learn.

The Decision Plane determines whether a Decision has moved through a legitimate governance path.

### 2.2 Execution Plane

The Execution Plane governs whether a legitimate Decision may become action.

It includes:

- decision-type maturity;
- execution gate policies;
- durable queues;
- review routing;
- presence grants;
- presence tokens;
- quorum presence;
- emergency override handling;
- pause, kill switch, rollback, and compensation controls;
- execution telemetry;
- dead-letter and exception handling.

Legitimacy authorizes consideration for execution. Execution Control authorizes action.

### 2.3 Covenant Plane

The Covenant Plane governs participation conditions among human, institutional, and synthetic actors.

It includes:

- HITL and AIITL role boundaries;
- covenant objects;
- schema-drift detection;
- truthful witnessing;
- dignity and agency preservation;
- contestability duties;
- repair-on-error requirements;
- relationship-aware records.

Covenant governs participation conditions, not final authority.

### 2.4 Repair Plane

The Repair Plane governs historic breach, institutional harm, affected-party claims, sovereignty claims, and repair agendas.

It includes:

- repair agendas;
- repair points;
- breach records;
- affected-party review;
- sovereignty claims;
- institutional response states;
- anti-erasure controls;
- repair commitments;
- completion evidence;
- repair learning.

Repair claims are not ordinary stakeholder comments.

## 3. Architectural Layers

### 3.1 Constitutional Frame

The Constitutional Frame defines CDP scope, principles, invariants, non-goals, and authority boundaries.

It constrains all other planes.

### 3.2 Decision Kernel

The Decision Kernel stores and mutates the canonical Decision object. It is the center of decision state.

The Decision Kernel MUST preserve state, status, history, policy scope, authority observations, linked artifacts, and lineage.

### 3.3 Protocol Layer

The Protocol Layer validates governed acts such as Nemawashi, Propose, Challenge, Test, Adjudicate, Legitimize, Execute, Record, Learn, Identify, Attest, and extension protocols.

Protocols provide motion. They do not silently create authority outside policy.

### 3.4 Legitimacy Layer

The Legitimacy Layer determines whether a judged Decision is institutionally enactable.

Legitimacy is required for execution, but legitimacy is not sufficient for execution.

### 3.5 Execution Control Layer

The Execution Control Layer evaluates whether a legitimate Decision may be acted upon now.

It SHOULD evaluate:

- current Decision state;
- execution risk;
- decision-type maturity;
- execution gate policy;
- challenge state;
- presence requirements;
- quorum requirements;
- time windows;
- rollback or compensation readiness;
- emergency override policy;
- target-system constraints.

Execution MUST fail closed when authority, scope, policy, or presence checks fail.

### 3.6 Nemawashi Layer

The Nemawashi Layer manages stakeholder surfacing, readiness, friction, and pre-formal alignment.

Nemawashi may improve deliberation, but it MUST NOT replace Challenge, suppress dissent, or confer legitimacy.

### 3.7 Covenant Layer

The Covenant Layer manages relationship-aware participation.

It records participant roles, duties, boundaries, schema drift, challenge, consent requirements, repair obligations, and limitations on AI authority.

The Covenant Layer MUST NOT assert unsupported AI personhood, consciousness, legal sovereignty, or moral equivalence.

### 3.8 Repair Layer

The Repair Layer manages repair-class claims and agendas.

It preserves enumerated claims, affected-party authority, breach records, institutional responses, dissent, commitments, completion evidence, and learning.

The Repair Layer MUST NOT collapse repair demands into generic sentiment, stakeholder input, or public-relations language.

### 3.9 Record Layer

The Record Layer preserves lineage, envelopes, evidence references, transcripts, challenges, tests, adjudications, legitimacy artifacts, execution results, repair records, covenant records, outcomes, and replay artifacts.

A record can be auditable without being universally public. Implementations MAY require access controls, redaction, affected-party review, or culturally appropriate handling.

### 3.10 Learning Layer

The Learning Layer transforms recorded outcomes into precedent, policy revision, schema revision, operational safeguards, repair lessons, and governance improvement.

Learning MUST NOT erase breach history, dissent, adverse outcomes, repair obligations, or prior record.

## 4. Cross-Cutting Trust and Authority Fabric

CDP trust is not a single layer. It is a fabric across all planes.

Cross-cutting trust functions include:

- identity;
- attestation;
- integrity verification;
- authority resolution;
- delegation;
- revocation;
- authority decay;
- presence verification;
- quorum verification;
- policy evaluation;
- rate limiting and friction controls;
- challenge preservation;
- replay and audit;
- escalation and appeals;
- affected-party review;
- repair authority;
- sovereignty-claim preservation.

Authority types include:

- identity authority;
- protocol authority;
- challenge authority;
- test authority;
- adjudication authority;
- legitimacy authority;
- execution authority;
- presence authority;
- delegated authority;
- emergency authority;
- repair authority;
- affected-party authority;
- sovereignty authority;
- revoked or decayed authority.

Authority decays unless renewed, scoped, and recorded under policy.

## 5. Reference Topology

A minimal implementation MAY consist of:

- FastAPI or equivalent service surface;
- SQLite or local Postgres;
- append-only envelope/event log;
- local file or object store for artifacts;
- local policy module;
- basic identity and attestation checks;
- basic execution gate evaluation;
- basic record writer.

A fuller implementation MAY add:

- search index;
- vector store for precedent similarity;
- durable message bus;
- execution review queue;
- approved execution queue;
- challenge-required queue;
- dead-letter or exception queue;
- maturity-event queue;
- repair-commitment tracker;
- covenant record store;
- external trust registry;
- policy engine such as OPA or Cedar;
- IAM/PAM integration;
- cryptographic signing and tamper-evident storage;
- observability and execution telemetry.

## 6. Reference Data Flow

### 6.1 Decision Flow

1. Client submits Envelope.
2. Identity and Attestation are verified.
3. Protocol-specific validation runs.
4. Decision Kernel performs state mutation.
5. Record Layer persists lineage and artifacts.
6. Learning Layer consumes recorded outcomes when eligible.

### 6.2 Execution Flow

1. Decision reaches a legitimacy-eligible state.
2. Execution Control evaluates maturity, risk, challenge state, and policy.
3. If gated, execution request is routed to review or queue.
4. If required, Presence Grant or quorum presence is obtained.
5. Executor acts within scope and time bounds.
6. Execution telemetry and outcome are recorded.
7. Learn evaluates maturity, safeguards, defects, and repair implications.

### 6.3 Covenant Flow

1. Participants, roles, duties, and boundaries are established.
2. AIITL and HITL participation occurs under explicit constraints.
3. Schema drift, uncertainty, contradiction, or boundary concerns may be surfaced.
4. Challenges, clarifications, dissent, and repair obligations are recorded.
5. Learn updates future participation guidance without erasing prior record.

### 6.4 Repair Flow

1. Repair Agenda or Repair Point is submitted or identified.
2. Affected peoples, authority claims, and provenance are preserved.
3. Each point receives its own record and response state.
4. Challenges and affected-party review are allowed.
5. Institutional commitments are tracked through execution or failure.
6. Completion evidence, dissent, non-response, and learning are recorded.

## 7. Architectural Rules

Envelope provides context. Decision provides structure. Protocols provide motion. Authority bounds action. Covenant governs participation. Repair preserves breach and response. Record makes memory. Learn changes the future.

Implementations MUST distinguish:

- legibility from legitimacy;
- legitimacy from execution authority;
- access from presence;
- consultation from consent;
- stakeholder input from sovereignty claim;
- repair commitment from repair completion;
- AI participation from AI final authority;
- record from public disclosure;
- learning from erasure.

## 8. Failure Domains

The architecture MUST distinguish:

- validation failure;
- identity failure;
- attestation failure;
- authority failure;
- authority decay or revocation;
- policy failure;
- transition failure;
- challenge preservation failure;
- legitimacy failure;
- execution gate failure;
- presence failure;
- quorum failure;
- execution failure;
- rollback or compensation failure;
- persistence failure;
- record integrity failure;
- covenant boundary failure;
- schema drift;
- repair erasure;
- affected-party review failure;
- learning failure.

## 9. Design Constraints

Execution speed MUST remain a function of governance confidence, not merely of system capacity.

Automation is not a switch. Automation is a governed maturity state.

Legitimate decisions MUST NOT become ambiently executable merely because credentials, tools, or queues exist.

Covenant language MUST remain precise and bounded.

Repair records MUST preserve claim structure, provenance, authority, dissent, response, commitment, and completion evidence.

## 10. Minimal Compliance

A minimal CDP implementation SHOULD support:

- canonical Decision object;
- common Envelope;
- Identify and Attest checks;
- Propose, Challenge, Test, Adjudicate, Legitimize, Execute, Record, and Learn protocols;
- basic execution gate policy;
- basic record and replay;
- explicit treatment of authority failure;
- explicit treatment of active challenge;
- explicit record of repair-class claims when present;
- explicit role boundaries for synthetic participants when present.

## 11. Implementation Note

CDP can be implemented locally first. A small SQLite/Postgres-backed service with file artifacts, append-only logs, and a simple policy evaluator is acceptable for early prototypes.

Distributed systems, queues, vector search, external trust registries, and enterprise policy engines are implementation extensions, not prerequisites for the constitutional model.
