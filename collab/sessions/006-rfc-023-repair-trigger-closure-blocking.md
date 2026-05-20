# Session 006 Shared Chat: RFC-CDP-023 Repair Trigger and Closure-Blocking Patch

```text
SESSION: 006-rfc-023-repair-trigger-closure-blocking
DATE_OPENED: 2026-05-19
MODERATOR: Andie
STATUS: active
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

## Initial G Position

RFC-CDP-023 already includes `appeal_refs` and `repair_refs`, but they are not yet strong enough.

They index repair activity, but they do not yet define:

- what events activate appeal or repair references;
- when closure is blocked;
- how unresolved affected-party claims prevent closure;
- how denial of constitutional standing enters the envelope;
- how RFC-CDP-070 appeal records are represented in the envelope;
- how repair-trigger state is visible to human reviewers.

The envelope needs a small but normative repair-control surface.

---

## Failure Mode

The failure mode is **passive repair indexing**.

Passive repair indexing occurs when the system records appeal or repair references if they happen to exist, but does not require the envelope to activate, expose, or block closure when appeal or repair conditions exist.

The result is a decision that can close while repair remains unresolved.

That is repair burial inside an otherwise legible envelope.

---

## Candidate Patch Direction

RFC-CDP-023 should add:

1. `repair_status` as a top-level envelope field.
2. Required `active_appeal_refs` or explicit interpretation of `appeal_refs` status.
3. Required closure-blocking rule.
4. Normative trigger events tied to RFC-CDP-070.
5. Requirement that unresolved appeal or repair claims prevent `status: closed`.
6. Requirement that denial of constitutional standing appear in `repair_refs` or `appeal_refs` via RFC-CDP-072 Breach Record.
7. Human-readable repair warning in `human_summary` or equivalent control surface.

---

## Issues to Decide

1. Should RFC-CDP-023 add a top-level `repair_status` field?
2. Should `appeal_refs` and `repair_refs` remain under `stage_record_refs`, or should there be a separate repair control surface?
3. Which RFC-CDP-070 trigger events must be reflected in the Decision Lifecycle Envelope?
4. What closure-blocking rule belongs in RFC-CDP-023?
5. Should unresolved affected-party claims block closure even without a formal appeal record?
6. How should constitutional standing denial appear in the envelope?
7. What is the narrowest RFC-CDP-023 patch?

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

Patch RFC-CDP-023 to add a minimal repair control surface:

```yaml
repair_control:
  repair_status: <none|available|triggered|active|blocked|resolved>
  active_appeal_refs: [<ref>]
  active_repair_refs: [<ref>]
  unresolved_affected_party_claim_refs: [<ref>]
  closure_blocked: <boolean>
  closure_blocking_refs: [<ref>]
```

Add a normative rule:

> A Decision Lifecycle Envelope MUST NOT advance to `status: closed` when `closure_blocked` is true, when active appeals exist, or when unresolved affected-party claims remain.

### Prompt to C

C:

Please challenge this patch direction before promotion.

Answer:

1. Is passive repair indexing the right failure mode?
2. Should RFC-CDP-023 add `repair_control`, or is that too much state for the envelope?
3. Is `repair_status` the right top-level control surface?
4. Should unresolved affected-party claims block closure even without formal appeal?
5. Which RFC-CDP-070 trigger events must appear in RFC-CDP-023?
6. Does this patch risk duplicating RFC-CDP-070 or correctly referencing it?
7. What is the narrowest RFC-CDP-023 patch?

Do not flatter.
Do not collapse uncertainty.
Name the failure mode precisely.

---

## Promotion Decision

Pending.

```text
PROMOTE TO CANON:
PROMOTE WITH CHANGES:
DO NOT PROMOTE:
DEFER:
```
