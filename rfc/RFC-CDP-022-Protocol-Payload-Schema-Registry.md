# RFC-CDP-022 — Protocol Payload Schema Registry

Author: Kevin “Andie” Williams  
Status: Draft v0.4  
Series: Constitutional Decision Plane (CDP)  
Date: May 23, 2026  
Updates: RFC-CDP-015 legacy numbering  
Depends On: RFC-CDP-002

## Abstract

Defines payload schemas and registered payload families for Propose, Challenge, Test, Adjudicate, Legitimize, Execute, Record, Learn, Nemawashi, and cross-cutting governance gates.

## 1. Purpose

This RFC answers what each protocol payload contains and standardizes the act-specific body inside the common Envelope.

It also reserves named cross-cutting payload types used by multiple protocols.

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

## 4. Cross-Cutting Gate Payloads

### 4.1 Anti-Premature-Certainty Gate Result

Payload name:

```text
anti_premature_certainty_gate_result
```

Status:

```text
Reserved
```

Defined by:

```text
RFC-CDP-002-Anti-Premature-Certainty-Principle.md
```

Purpose:

Records the result of evaluating the Anti-Premature-Certainty Gate for a CDP decision.

This payload is reserved before downstream RFCs require it so that Propose, Challenge, Legitimize, Record, and Learn can reference the same object rather than inventing separate gate-result shapes.

Minimum reserved schema:

```yaml
anti_premature_certainty_gate_result:
  gate_id: <uuid>
  decision_id: <uuid>
  evaluated_at: <timestamp>
  evaluator: <actor_ref>
  risk_tier: <low|medium|high|critical|unknown>
  passed: <boolean>
  failures: [<string>]
  unwaived_failures: [<string>]
  waivers:
    - criterion: <string>
      authority: <actor_ref>
      reason: <string>
      expires_at: <timestamp|null>
  record_ref: <ref>
```

Notes:

- This payload is Reserved, not yet Accepted.
- Downstream RFCs MUST NOT require this payload as a precondition until its schema is promoted beyond Reserved or explicitly referenced as Draft-compatible.
- Future revisions SHOULD define record-hash requirements for this payload.
- Future revisions SHOULD define how this payload is linked from the Decision Lifecycle Envelope and Record Protocol.

## 5. Content Types

Default encodings SHOULD use structured syntax suffixes:

- `application/cdp.propose+json`
- `application/cdp.challenge+json`
- `application/cdp.test+json`
- `application/cdp.apc-gate-result+json`

Alternate encodings MAY be supported if schema semantics are preserved.

## 6. Principle

Envelope fields are universal. Payload fields are act-specific or gate-specific.

Payload schemas MUST NOT silently redefine universal envelope semantics.

## 7. Legacy Note

This file previously carried the title `RFC-CDP-015 — Protocol Payload Schemas` after renumbering.

Draft v0.4 updates the heading to match the canonical filename and Series Index entry.
