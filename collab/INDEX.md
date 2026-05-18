# CDP Collaboration Index

This index tracks active and completed collaboration sessions.

## Active Sessions

| Session | Topic | Status | Moderator | Canon Target |
|---|---|---|---|---|
| [004](sessions/004-governed-path-hash.md) | Governed Path Hash | active | Andie | RFC-CDP-023-Decision-Lifecycle-Envelope.md |

## Closed Sessions

| Session | Topic | Status | Moderator | Canon Target |
|---|---|---|---|---|
| [001](sessions/001-rfc-completeness-coherency-readability.md) | RFC completeness, coherency, and human readability review | closed-promoted | Andie | RFC-CDP-000-Series-Index.md |
| [002](sessions/002-standing-and-recusal.md) | Standing and Recusal | closed-promoted | Andie | RFC-CDP-033-Standing-and-Recusal-Model.md; RFC-CDP-001 alignment; RFC-CDP-000 map update |
| [003](sessions/003-decision-envelope.md) | Decision Envelope / Envelope split | closed-promoted | Andie | RFC-CDP-021 Wire Message Envelope; RFC-CDP-023 Decision Lifecycle Envelope; RFC-CDP-000 map update |

## Session Status Values

- `active` — currently underway
- `awaiting-response` — waiting for another collaborator
- `adjudication-needed` — human moderator needs to decide
- `promotion-planned` — accepted work has a canon promotion path
- `closed-promoted` — promoted into canonical files
- `closed-deferred` — intentionally deferred
- `closed-rejected` — not promoted

## Canon Promotion Queue

Nothing currently queued.

## Open Cross-Session Questions

- Should CDP create a dedicated Common Building Blocks RFC before more protocol RFCs?
- What is the minimum human-readable surface required for each protocol?
- How should machine-readable schemas and human-readable explanations be kept synchronized?
- How do we make human-in-the-loop structurally real rather than human-in-the-pile theater?
- Does Legitimize need a precision rewrite or a new name?
- Should the Standing Record schema be stabilized in RFC-CDP-033 or moved to a dedicated schema RFC?
- Should lifecycle RFCs reference RFC-CDP-033 Standing and Recusal now, or only after schema stabilization?
- How should AI Functional Standing integrate with RFC-CDP-062 HITL-AIITL Role Boundaries?
- How should `governed_path_hash` be computed for RFC-CDP-023?
- Should lifecycle stage enums live in RFC-CDP-023, RFC-CDP-022, or a shared CBB/registry RFC?
- Should embedded or sealed decision payloads be defined as an implementation profile in the 120–149 band?
- Which lifecycle RFCs should reference RFC-CDP-023 first?
