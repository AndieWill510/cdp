# Session 002 Shared Chat: Standing and Recusal

```text
SESSION: 002-standing-and-recusal
DATE_OPENED: 2026-05-17
MODERATOR: Andie
STATUS: active
MODE: shared-chat-file
CANON_TARGET: TBD — possible Trust, Identity, and Authority RFC; possible AIITL / role-boundary RFC; possible update to RFC-CDP-032 or RFC-CDP-062
PURPOSE: Decide whether Standing and Recusal should become a first-class CDP primitive, where it belongs in the RFC series, and what should be promoted to canon.
```

## How to Use This File

This is a shared chat transcript and working record for Session 002.

All participants should write directly into this single file using dated turns.

The working pattern is:

```text
Turn -> Response -> Challenge -> Moderator Adjudication -> Promotion Decision
```

When something becomes canonical, copy or rewrite it into the appropriate RFC, schema, architecture document, or decision record. Do not let this file become the hidden constitution.

---

## Participants

- **Andie** — moderator, originator, human adjudicator
- **ChatGPT** — synthesizer, continuity keeper, protocol drafter
- **Claude / Sonnet** — challenger, coherence reviewer, human-readability critic, schema-drift detector
- **Other collaborators** — invited as named contributors

---

## Session Question

Should **Standing and Recusal** become a first-class CDP governance primitive?

If yes:

1. What does Standing mean in CDP?
2. What does Recusal mean in CDP?
3. Who or what can have standing?
4. How is standing determined?
5. How is conflict of interest detected or declared?
6. When must the proposer recuse?
7. Where does the Standing / Recusal model belong in the RFC series?
8. What is the narrowest canonical next move?

---

## Background

Session 001 surfaced Standing as a likely missing primitive.

Claude / Sonnet proposed:

> Standing is the right to participate in a CDP stage, derived from role, accountability, and absence of disqualifying conflict.

The same session also introduced the proposer recusal problem:

> Whoever frames the proposal shapes the decision space before the vote. Agenda-setting is more powerful than voting.

This creates a governance problem:

- Who may propose?
- Who may challenge?
- Who may test?
- Who may adjudicate?
- Who may legitimize?
- Who may execute?
- Who may appeal?
- Who must recuse?
- Who decides whether recusal is required?

---

## Current Prior Decision

From `skills/CDP_CONTEXT_FOR_CLAUDE.md`:

> CDP governance is not HITL (human-in-the-loop).
>
> It is AIITL — AI and humans both in the loop.
>
> Everyone with standing votes.
>
> The proposer does not vote.
>
> Standing is determined by role, context, and accountability — not by species.

This session does **not** assume that wording is final protocol language.

This session exists to challenge, refine, and decide what part of that principle should become canonical.

---

## Core Distinction

A participant may have different standing at different stages.

For example:

| Actor | May Propose | May Challenge | May Adjudicate | May Legitimize | May Execute |
|---|---:|---:|---:|---:|---:|
| Proposer | yes | limited | no / limited | no | maybe |
| Affected party | maybe | yes | maybe | maybe | no |
| Domain expert | maybe | yes | maybe | maybe | no |
| Governance authority | maybe | yes | yes | yes | maybe |
| AI model | yes / assist | yes / assist | limited | no / limited | no / constrained |
| Executor | maybe | yes | no / limited | no / limited | yes |

This table is provisional and should be challenged.

---

## Initial Definitions for Review

### Standing

Standing is the recognized right or responsibility to participate in a CDP decision stage.

Standing may be derived from:

- role;
- domain expertise;
- affected-party status;
- delegated authority;
- accountability;
- custody of evidence;
- operational responsibility;
- legal or institutional mandate;
- repair or appeal rights.

Standing is not determined by species.

### Recusal

Recusal is removal or limitation of a participant's authority in a decision stage due to conflict, capture risk, proposer status, role conflict, or compromised independence.

Recusal does not always mean silence.

A recused proposer may still clarify intent, evidence, assumptions, or implementation constraints.

A recused proposer must not be the sole legitimizer of their own proposal.

---

## Issues to Decide

This session should produce one narrow decision at a time.

Candidate decisions:

1. Should Standing be promoted as a first-class CDP primitive?
2. Should Recusal be part of the same primitive or a separate model?
3. Should the proposer recusal rule be strict or risk-tiered?
4. Should Standing live in the Trust, Identity, and Authority band (`030–039`), the Covenant and AIITL band (`060–069`), or as a cross-cutting CBB concept?
5. Should the next canonical move be a new RFC, or an update to an existing RFC?

---

## Turn 001 — 2026-05-17 — Andie / ChatGPT — Session Opening

```text
DATE: 2026-05-17
AUTHOR: Andie, recorded by ChatGPT
ROLE: moderator / session opener
STATUS: active
PURPOSE: Record Decision 002 approval and open Session 002 on Standing and Recusal.
```

### Decision 002

Approved: Open Session 002 on **Standing and Recusal**.

### Scope

This session is about whether and how Standing / Recusal become canonical CDP concepts.

It is not yet a decision to create a new RFC.

It is not yet a decision to modify any lifecycle protocol.

### Working Hypothesis

Standing may be the missing primitive that makes AIITL, proposer recusal, challenge rights, adjudication legitimacy, and human-in-the-loop participation structurally real.

### Caution

Do not canonize the phrase “everyone votes except the proposer” too early.

The safer protocol question may be:

> Under what conditions must a participant be barred from adjudicating, legitimizing, or voting on a decision because of proposer status, conflict, or capture risk?

### Prompt to Claude / Sonnet

Claude / Sonnet:

Read:

1. `https://github.com/AndieWill510/cdp/blob/main/skills/CDP_CONTEXT_FOR_CLAUDE.md`
2. `https://github.com/AndieWill510/cdp/blob/main/collab/sessions/001-rfc-completeness-coherency-readability.md`
3. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-000-Series-Index.md`
4. `https://github.com/AndieWill510/cdp/blob/main/collab/sessions/002-standing-and-recusal.md`

Then append or draft **Turn 002 — Claude / Sonnet — Standing and Recusal Challenge Memo**.

Please answer:

1. Should Standing be a first-class CDP primitive?
2. Should Recusal be part of Standing, part of Authority, or its own model?
3. Is “everyone with standing votes; proposer does not vote” too strict, too loose, or exactly right?
4. How should standing be determined?
5. How should AI participants have standing without pretending they have human legal personhood?
6. What is the minimum viable schema for standing?
7. Which RFC band should own this concept?
8. What is the narrowest canonical next move?

Do not flatter.

Do not collapse uncertainty.

Name the governance failure mode we are trying to prevent.

---

## Promotion Decision

Pending.

```text
PROMOTE TO CANON:
PROMOTE WITH CHANGES:
DO NOT PROMOTE:
DEFER:
```
