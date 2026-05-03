# RFC-CDP-015 — Protocol Payload Schemas

Author: Kevin “Andie” Williams  
Status: Draft v0.3  
Series: Constitutional Decision Plane (CDP)  
Date: March 17, 2026

## Abstract
Defines payload schemas for Propose, Challenge, Test, Adjudicate, Legitimize, Execute, Record, Learn, and Nemawashi.

## 1. Purpose
This RFC answers what each protocol payload contains and standardizes the act-specific body inside the common Envelope.

## 2. Guidance
Each payload schema SHOULD:
- define required fields;
- include `metadata` as extension space;
- reference artifacts by stable identifier;
- avoid duplicating universal Envelope fields.

## 3. Payload Families
### Propose
`proposal_type, title, description, objective, policy_scope, required_authorities`

### Challenge
`challenge_type, severity, argument, requested_action`

### Test
`test_type, claim, method, result`

### Adjudicate
`disposition, rationale, considered_refs`

### Legitimize
`status, basis, scope, expiry`

### Execute
`target, authorization_ref, idempotency_key`

### Record
`record_ref, artifact_refs, summary`

### Learn
`observed_outcome, lessons, recommended_changes`

### Nemawashi
`stakeholders, positions, alignment_status, open_issues`

## 4. Content Types
Default encodings SHOULD use structured syntax suffixes:
- `application/cdp.propose+json`
- `application/cdp.challenge+json`
- `application/cdp.test+json`

Alternate encodings MAY be supported if schema semantics are preserved.

## 5. Principle
Envelope fields are universal. Payload fields are act-specific.
