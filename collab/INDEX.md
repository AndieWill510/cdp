# CDP Collaboration Index

This index tracks active and completed collaboration sessions.

## Active Sessions

| Session | Topic | Status | Moderator | Canon Target |
|---|---|---|---|---|
| — | — | — | — | — |

## Closed Sessions

| Session | Topic | Status | Moderator | Canon Target |
|---|---|---|---|---|
| [001](sessions/001-rfc-completeness-coherency-readability.md) | RFC completeness, coherency, and human readability review | closed-promoted | Andie | RFC-CDP-000-Series-Index.md |
| [002](sessions/002-standing-and-recusal.md) | Standing and Recusal | closed-promoted | Andie | RFC-CDP-033-Standing-and-Recusal-Model.md; RFC-CDP-001 alignment; RFC-CDP-000 map update |
| [003](sessions/003-decision-envelope.md) | Decision Envelope / Envelope split | closed-promoted | Andie | RFC-CDP-021 Wire Message Envelope; RFC-CDP-023 Decision Lifecycle Envelope; RFC-CDP-000 map update |
| [004](sessions/004-governed-path-hash.md) | Governed Path Hash | closed-promoted | Andie | RFC-CDP-023 governed_path_hash v0.3; RFC-CDP-000 map update |
| [005](sessions/005-repair-plane-reanchor.md) | Repair Plane Reanchor | closed-promoted | Andie | RFC-CDP-070 Appeals and Contestability; RFC-CDP-033 automatic Breach Record; RFC-CDP-000 map update |
| [006](sessions/006-rfc-023-repair-trigger-closure-blocking.md) | RFC-CDP-023 Repair Trigger and Closure-Blocking Patch | closed-promoted | Andie | RFC-CDP-023 repair_control v0.4; RFC-CDP-000 map update |
| [007](sessions/007-anti-premature-certainty-implementation.md) | Anti-Premature-Certainty Principle and Implementation | closed-promoted | Andie | RFC-CDP-002 v0.2; RFC-CDP-022 APC gate result payload; RFC-CDP-024 reservation |
| [008](sessions/008-cdp-persistence-model.md) | CDP Persistence Model | closed-promoted | Andie | RFC-CDP-025-CDP-Persistence-Model.md |
| [009](sessions/009-standing-persistence-enforcement-query.md) | Standing Persistence and Enforcement Query | closed-promoted | Andie | RFC-CDP-025 v0.2; RFC-CDP-033 v0.4 |
| [010](sessions/010-proposal-sufficiency-gate.md) | Proposal Sufficiency Gate | closed-promoted | Andie | RFC-CDP-024 v0.1 |
| [011](sessions/011-rfc-022-apc-gate-result-payload.md) | RFC-CDP-022 APC Gate Result Payload | closed-promoted | Andie | RFC-CDP-022 v0.5 |
| [012](sessions/012-rfc-023-admission-artifact-visibility.md) | RFC-CDP-023 Admission Artifact Visibility Patch | closed-promoted | Andie | RFC-CDP-023 v0.5 |

## Session Status Values

- `active` — currently underway
- `awaiting-response` — waiting for another collaborator
- `adjudication-needed` — human moderator needs to decide
- `promotion-planned` — accepted work has a canon promotion path
- `closed-promoted` — promoted into canonical files
- `closed-deferred` — intentionally deferred
- `closed-rejected` — not promoted

## Canon Promotion Queue

1. RFC-CDP-041 Propose Protocol Proposal Sufficiency wiring.
2. RFC-CDP-042 Challenge Protocol formation challenge relationship.
3. RFC-CDP-045 Legitimize Protocol APC wiring.
4. Record Hash Propagation to governed record RFCs in the 040–048 band.
5. Reference implementation / DDL profile for RFC-CDP-025.

## Open Cross-Session Questions

- Should CDP create a dedicated Common Building Blocks RFC before more protocol RFCs?
- What is the minimum human-readable surface required for each protocol?
- How should machine-readable schemas and human-readable explanations be kept synchronized?
- How do we make human-in-the-loop structurally real rather than human-in-the-pile theater?
- Does Legitimize need a precision rewrite or a new name?
- Should the Standing Record schema be stabilized in RFC-CDP-033 or moved to a dedicated schema RFC?
- Should lifecycle RFCs reference RFC-CDP-033 Standing and Recusal now, or only after schema stabilization?
- How should AI Functional Standing integrate with RFC-CDP-062 HITL-AIITL-Role-Boundaries?
- Should lifecycle stage enums live in RFC-CDP-023, RFC-CDP-022, or a shared CBB/registry RFC?
- Should embedded or sealed decision payloads be defined as an implementation profile in the 120–149 band?
- Propagate `record_hash` requirements to governed record RFCs in the 040–048 band.
- Adjudicate lifecycle-stage enum ownership before RFC-CDP-023 advances to Candidate.
- Should governed records use one polymorphic JSON-first table or typed tables per record family?
- What standing rules apply to formation challenge challengers?
- Should `proposal_sufficiency_record` become a payload type in RFC-CDP-022?
- Should `formation_challenge_record` become a payload type in RFC-CDP-022?
- Should `record_hash` be mandatory in `anti_premature_certainty_gate_result` after record-hash propagation?
