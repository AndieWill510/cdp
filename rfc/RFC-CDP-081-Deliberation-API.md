# RFC-CDP-017 — Deliberation API

Author: Kevin “Andie” Williams  
Status: Draft v0.3  
Series: Constitutional Decision Plane (CDP)  
Date: March 17, 2026

## Abstract
Defines how A2A deliberation is carried over the wire.

## 1. Purpose
The Deliberation API answers:
- how challenge/test/adjudicate dialogue is exchanged;
- how bounded loops and convergence signals are represented.

## 2. Message Types
- challenge submission;
- rebuttal;
- clarification request;
- test request;
- test result notice;
- convergence signal;
- escalation notice.

## 3. Bounded Loops
Implementations SHOULD support:
- thread identifiers;
- maximum rounds;
- deadlines;
- unresolved issue lists;
- convergence markers.

## 4. Properties
Each deliberative message SHOULD preserve:
- parent linkage;
- Decision version;
- actor identity;
- attestation where mutating.

## 5. Principle
Conversation is useful, but governance requires bounded, inspectable conversational structure.
