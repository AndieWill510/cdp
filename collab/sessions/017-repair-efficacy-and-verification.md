# Session 017 — Repair Efficacy and Verification

SESSION: 017  
DATE_OPENED: 2026-07-03  
DATE_CLOSED: 2026-07-03  
MODERATOR: Andie  
STATUS: closed-promoted  
CANON_TARGET: `rfc/RFC-CDP-076-Repair-Efficacy-and-Verification.md`

## Purpose

Promote the ConstantC repair-completion versus repair-efficacy distinction into the CDP Repair plane without allowing it to remain only a good idea.

## Failure Mode

**Repair completion masquerading as repair efficacy.**

A repair process can execute every step in the playbook and still leave the harmed party unrepaired.

CDP already has appeal entry, breach records, repair agendas, repair commitments, completion evidence, affected-party review, dissent preservation, and closure blocking. The missing hook was a separate, queryable efficacy state so procedural completion cannot silently imply repair.

## Source Material

The promoted RFC draws from ConstantC culture work:

- `culture/repair-completion-vs-repair-efficacy.md`
- `culture/justice-liberty-freedom-gap.md`, including the aperture model

Core carried principle:

> A completed repair process is not yet proof of repair.

## Promoted

- Created `rfc/RFC-CDP-076-Repair-Efficacy-and-Verification.md` as Draft v0.1.
- Introduced the distinction between `completion_status` and `efficacy_status`.
- Added a minimal Repair Efficacy Record surface.
- Added the non-certification rule: completion evidence may support an efficacy claim, but must not silently become one.
- Added the checklist-can-eat-itself guardrail.
- Added the silence-is-not-consent rule.
- Added the minimal implementation hook:

```yaml
repair:
  completion_status: pending | completed | failed | withdrawn | superseded
  efficacy_status: unassessed | claimed | disputed | not_assessable | requires_future_review
  efficacy_claim: string | null
  efficacy_evidence_refs: []
  affected_party_standing: unknown | present | absent | constrained | disputed
  silence_policy: silence_may_pause_but_must_not_close
```

## Deferred

- Whether `repair_efficacy_record` should be registered in RFC-CDP-022 as a protocol payload type.
- How RFC-CDP-025 persistence projections should query efficacy state.
- How RFC-CDP-092 should model separate procedural and efficacy state transitions.
- Whether RFC-CDP-072 should later inline Repair Efficacy Record as a first-class schema section rather than depending on RFC-CDP-076.
- Whether RFC-CDP-000 should be advanced to Draft v1.4 after wider repair-band map review.

## Open Questions

- What counts as sufficient evidence of repair efficacy across domains?
- Who may verify repair efficacy when affected parties are unavailable, unsafe, constrained, or absent?
- How should CDP distinguish repair incomplete, repair refused, repair impossible, and harm irreversible?
- How should efficacy review avoid becoming a scored compliance ritual?

## Files Read

- `docs/context/CDP_START_HERE.md`
- `docs/context/CULTURE.md`
- `docs/context/README.md`
- `docs/context/LIVING_COVENANT.md`
- `docs/context/SESSION-HANDOFF.md`
- `docs/context/AI-MEMORY-BRIEF.md`
- `docs/context/C_CDP_PREFERENCES.md`
- `collab/COUNCIL_ROLES.md`
- `collab/PROMOTION_PROTOCOL.md`
- `collab/INDEX.md`
- `rfc/RFC-CDP-000-Series-Index.md`
- `rfc/RFC-CDP-070-Appeals-and-Contestability-Model.md`
- `rfc/RFC-CDP-071-Twenty-Points-Repair-Protocol.md`
- `rfc/RFC-CDP-072-Breach-Record-and-Repair-Agenda-Schema.md`
- `rfc/RFC-CDP-073-Affected-Party-Review-and-Anti-Erasure.md`

## Not Read / Deferred Context

- Full `RFC-CDP-074-Sovereignty-Claims-and-Authority-Pluralism.md`
- Full `RFC-CDP-092-Repair-State-Machine.md`
- ConstantC files in-repo during this session; ConstantC state came from immediately preceding verified GitHub work in the active conversation.

## Verification Method

- New RFC created in `rfc/` on a branch.
- Session record created in `collab/sessions/`.
- `collab/INDEX.md` patched to record Session 017.
- Post-merge verification should fetch the new RFC and session record from `main`.

## Do Not Assume

- Do not assume repair efficacy is verified merely because a Repair Efficacy Record exists.
- Do not assume silence from an affected party means consent, satisfaction, waiver, forgiveness, or closure.
- Do not assume completion evidence proves efficacy without a separate efficacy claim and contestable evidence surface.
- Do not turn efficacy prompts into a scored rubric.
