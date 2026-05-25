# Session 015 Shared Chat: RFC-CDP-045 Legitimize APC Wiring

```text
SESSION: 015-rfc-045-legitimize-apc-wiring
DATE_OPENED: 2026-05-25
MODERATOR: Andie
STATUS: promotion-applied
MODE: shared-chat-file
CANON_TARGET: RFC-CDP-045-Legitimize-Protocol.md
PURPOSE: Patch Legitimize Protocol so legitimacy consumes Proposal Sufficiency, APC, Standing, Challenge, Envelope, and Persistence evidence.
```

## Why This Session Exists

The downstream chain now exists:

- RFC-CDP-024 defines Proposal Sufficiency Gate.
- RFC-CDP-022 defines `anti_premature_certainty_gate_result`.
- RFC-CDP-023 indexes proposal sufficiency, formation challenge, and APC gate result references.
- RFC-CDP-041 wires Propose to Proposal Sufficiency.
- RFC-CDP-042 distinguishes Formation Challenge from ordinary Challenge.

The Legitimize Protocol now needs to consume those artifacts.

---

## Turn 001 — 2026-05-25 — C / G / Andie — Legitimize APC Wiring

C recommended the failure mode:

```text
legitimacy without governed sufficiency evidence
```

C also named two mechanisms:

- missing evidence;
- unverified evidence.

G accepted C's analysis and corrected the standing blocker:

```text
standing_status is a top-level Decision Lifecycle Envelope control surface, not part of repair_control.
```

Andie identified the load-bearing axiom:

```text
Sufficiency is necessary but not sufficient for legitimacy.
```

---

## Action Taken

Patched:

```text
rfc/RFC-CDP-045-Legitimize-Protocol.md
```

Advanced to:

```text
Draft v0.4
```

Commit:

```text
d708878ae9b123fc7e6c64041fb5ef4e3a43c36b
```

Promoted into RFC-CDP-045 Draft v0.4:

- corrected canonical heading from legacy RFC-CDP-006 to RFC-CDP-045;
- updated dependencies to current RFC numbering;
- legitimacy without governed sufficiency evidence as failure mode;
- missing evidence and unverified evidence as mechanisms;
- the Necessary-Not-Sufficient Axiom;
- APC gate result consumption from RFC-CDP-022;
- risk-tiered APC prerequisite with hard floor;
- APC exception constraints and proposer recusal;
- eight hard stop conditions;
- legitimacy record schema;
- integrity vs sufficiency vs legitimacy distinction;
- envelope and persistence requirements.

---

## Promotion Decision

```text
PROMOTE TO CANON:
- RFC-CDP-045 Draft v0.4 Legitimize APC wiring
- Necessary-Not-Sufficient Axiom

DEFER:
- contested legitimization adjudication process
- canonical risk classification mechanism
- detailed emergency exception timing
- state machine alignment
- record_hash propagation
```
