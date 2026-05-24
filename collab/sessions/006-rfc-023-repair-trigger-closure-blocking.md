# Session 006 Shared Chat: RFC-CDP-023 Repair Trigger and Closure-Blocking Patch

```text
SESSION: 006-rfc-023-repair-trigger-closure-blocking
DATE_OPENED: 2026-05-19
MODERATOR: Andie
STATUS: promotion-applied
MODE: shared-chat-file
CANON_TARGET: RFC-CDP-023-Decision-Lifecycle-Envelope.md
PURPOSE: Patch RFC-CDP-023 so appeal_refs and repair_refs are active governance controls, not passive references, now that RFC-CDP-070 defines appeal and contestability entry.
```

## Why This Session Exists

Session 005 created `RFC-CDP-070-Appeals-and-Contestability-Model.md` and patched `RFC-CDP-033-Standing-and-Recusal-Model.md` so denial of constitutional standing automatically generates a Breach Record.

C and G agreed that the next move should be to wire this repair-entry model into `RFC-CDP-023-Decision-Lifecycle-Envelope.md`.

The risk is that the Decision Lifecycle Envelope contains `appeal_refs` and `repair_refs`, but treats them as passive lists rather than closure-blocking governance controls.

---

## Session Question

How should RFC-CDP-023 be patched so appeal and repair references actively preserve repair reachability, closure-blocking, and contestability?

---

## Failure Mode

C sharpened the failure mode to:

> **Closure without repair resolution**

Passive repair indexing is the mechanism.

Closure without repair resolution is the harm.

A decision must not advance to `status: closed` while appeal, repair, breach, or affected-party claim conditions exist and are recorded but not enforced.

---

## Relevant Canonical Files

Read these first:

1. `https://github.com/AndieWill510/cdp/blob/main/skills/CDP_CONTEXT_FOR_CLAUDE.md`
2. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-000-Series-Index.md`
3. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-023-Decision-Lifecycle-Envelope.md`
4. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-033-Standing-and-Recusal-Model.md`
5. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-070-Appeals-and-Contestability-Model.md`
6. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-072-Breach-Record-and-Repair-Agenda-Schema.md`
7. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-073-Affected-Party-Review-and-Anti-Erasure.md`
8. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-092-Repair-State-Machine.md`
9. `https://github.com/AndieWill510/cdp/blob/main/collab/sessions/006-rfc-023-repair-trigger-closure-blocking.md`

---

## Turn 001 — 2026-05-19 — Andie / G — Session Opening

```text
DATE: 2026-05-19
AUTHOR: Andie, recorded by ChatGPT / G
ROLE: moderator / session opener
STATUS: active
PURPOSE: Record Decision 017 approval and open Session 006 on RFC-CDP-023 repair trigger and closure-blocking patch.
```

### Decision 017

Approved: Session 006 is **RFC-CDP-023 Repair Trigger and Closure-Blocking Patch**.

### Scope

This session is limited to `RFC-CDP-023-Decision-Lifecycle-Envelope.md`.

It should not rewrite the whole Repair plane.

It should not replace RFC-CDP-070.

It should make appeal and repair state active and visible in the envelope.

### G Recommendation

Initial G proposal:

```yaml
repair_control:
  repair_status: <none|available|triggered|active|blocked|resolved>
  active_appeal_refs: [<ref>]
  active_repair_refs: [<ref>]
  unresolved_affected_party_claim_refs: [<ref>]
  closure_blocked: <boolean>
  closure_blocking_refs: [<ref>]
```

C challenged the six-field version as duplicative.

---

## Turn 002 — 2026-05-19 — Claude / Sonnet / C — Repair Control Challenge

```text
DATE: 2026-05-19
AUTHOR: Claude / Sonnet / C
ROLE: challenger / coherence reviewer
STATUS: draft-promoted
PURPOSE: Reduce RFC-CDP-023 repair_control to the smallest non-duplicative governance surface.
```

### 1. Failure Mode

C accepted passive repair indexing as the mechanism, but sharpened the outcome failure mode:

> **Closure without repair resolution**

A decision advances to `status: closed` while appeal or repair conditions exist and are recorded but not enforced.

### 2. Repair Control Surface

C recommended adding `repair_control`, but reducing it from six fields to four.

Keep:

- `repair_status`
- `closure_blocked`
- `closure_blocking_reason`
- `closure_blocking_refs`

Remove:

- `active_appeal_refs`
- `active_repair_refs`
- `unresolved_affected_party_claim_refs`

Reason: those reference lists already exist in `stage_record_refs.appeal_refs`, `stage_record_refs.repair_refs`, and `affected_party_claim_refs`. Duplicating them creates two sources of truth.

### 3. Revised Minimal Block

```yaml
repair_control:
  repair_status: <none|available|triggered|active|blocked|resolved>
  closure_blocked: <boolean>
  closure_blocking_reason: <string|null>
  closure_blocking_refs: [<ref>]
```

### 4. Closure Rule

A Decision Lifecycle Envelope MUST NOT advance to `status: closed` when any of the following are true:

- `repair_control.closure_blocked` is true;
- `appeal_refs` contains a reference with unresolved status per RFC-CDP-070;
- `affected_party_claim_refs` contains an unresolved claim.

### 5. RFC-CDP-070 Trigger Binding

RFC-CDP-070 owns trigger definitions.

RFC-CDP-023 should reference those triggers, not duplicate them.

When any RFC-CDP-070 trigger event is recorded against this decision:

- `repair_control.closure_blocked` MUST be set to true;
- `repair_control.repair_status` MUST advance to at least `triggered`.

### 6. Recommendation

Advance RFC-CDP-023 to Draft v0.4 with the four-field repair-control surface.

---

## Turn 003 — 2026-05-19 — Andie / G — Repair Control Promotion

```text
DATE: 2026-05-19
AUTHOR: Andie, recorded by ChatGPT / G
ROLE: moderator / canon promotion recorder
STATUS: adjudicated-and-promoted
PURPOSE: Record approval of C's four-field repair_control patch and promote to RFC-CDP-023 Draft v0.4.
```

### Decision 018

Approved: C's reduced four-field `repair_control` patch.

### Action Taken

Patched:

```text
rfc/RFC-CDP-023-Decision-Lifecycle-Envelope.md
```

from Draft v0.3 to Draft v0.4.

Added:

```yaml
repair_control:
  repair_status: <none|available|triggered|active|blocked|resolved>
  closure_blocked: <boolean>
  closure_blocking_reason: <string|null>
  closure_blocking_refs: [<ref>]
```

Added failure mode:

```text
closure without repair resolution
```

Added normative closure-blocking rules.

Added RFC-CDP-070 trigger binding.

Added repair-control fields to the governed path manifest and governed path hash coverage.

Updated:

```text
rfc/RFC-CDP-000-Series-Index.md
```

to Draft v0.9 and marked RFC-CDP-023 as Draft v0.4.

### Promotion Decision

```text
PROMOTE TO CANON:
- RFC-CDP-023 Draft v0.4 repair_control patch
- RFC-CDP-000 Draft v0.9 map update

DO NOT PROMOTE:
- active_appeal_refs as separate repair_control field
- active_repair_refs as separate repair_control field
- unresolved_affected_party_claim_refs as separate repair_control field

DEFER:
- Record Hash Propagation to governed record RFCs
- implementation model population of repair_control
- lifecycle-stage enum ownership
```

---

## Promotion Decision

```text
PROMOTE TO CANON:
- RFC-CDP-023 Draft v0.4 repair control surface
- RFC-CDP-000 Draft v0.9 map update

DEFER:
- Record Hash Propagation
- repair_control implementation population
- lifecycle-stage enum ownership
```
