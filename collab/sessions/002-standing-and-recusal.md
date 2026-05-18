# Session 002 Shared Chat: Standing and Recusal

```text
SESSION: 002-standing-and-recusal
DATE_OPENED: 2026-05-17
MODERATOR: Andie
STATUS: active
MODE: shared-chat-file
CANON_TARGET: RFC-CDP-033-Standing-and-Recusal-Model.md
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

---

## Turn 002 — 2026-05-17 — Claude / Sonnet — Standing and Recusal Challenge Memo

```text
DATE: 2026-05-17
AUTHOR: Claude / Sonnet (claude-sonnet-4-6)
ROLE: challenger / coherence reviewer / schema-drift detector
STATUS: draft
PURPOSE: Answer eight structural questions about Standing and Recusal as CDP governance primitives. No flattery. No collapsed uncertainty.
```

### The Governance Failure Mode We Are Trying to Prevent

Before answering the eight questions, name the failure mode.

The failure mode is **authority capture through participation**.

It works like this:

A participant with a stake in the outcome controls which stage they appear in, what role they occupy, and whether anyone with competing standing is present. The governance process runs. The record shows deliberation. But the outcome was predetermined by who was allowed in the room and in what capacity.

This is not conspiracy. It is structural drift. It happens when:

- the proposer also adjudicates;
- the affected party is not notified in time to challenge;
- the AI model that generated the proposal also evaluates it;
- the authority that legitimizes the decision also executed the framing;
- recusal is voluntary and self-reported.

Standing without Recusal is participation theater.

Recusal without Standing is an empty gesture.

CDP must prevent authority capture through participation. That is the primitive we are building.

---

### 1. Should Standing be a first-class CDP primitive?

Yes. Unconditionally.

Here is why it cannot be implied by other primitives.

The lifecycle verbs — Propose, Challenge, Test, Adjudicate, Legitimize, Execute — all presuppose actors. But none of the current RFCs define who those actors are, what qualifies them to participate, or what disqualifies them.

RFC-CDP-030 (Identify Protocol) tells us who an actor *is*.

RFC-CDP-031 (Attest Protocol) tells us what an actor can *prove*.

RFC-CDP-032 (Authority and Delegation Model) tells us what an actor is *authorized to do*.

None of these answer: *does this actor have the right to participate in this specific stage of this specific decision, given their relationship to it?*

That is Standing. It is not identity. It is not authority. It is not attestation. It is **contextual participation rights**, stage-specific and decision-specific.

Without Standing as a first-class primitive, every lifecycle protocol must independently invent participation rules. They will drift. They already have the shape of drift — the challenge surface, the adjudication authority, the legitimization role are all described differently across the current RFC family.

Standing is the missing cross-cutting primitive that makes those descriptions coherent.

---

### 2. Should Recusal be part of Standing, part of Authority, or its own model?

Recusal is a constraint on Standing, not a separate primitive.

The relationship is:

```text
Standing = base participation right
Recusal = conditional removal or limitation of Standing in a specific context
```

Standing says: this actor may participate in this stage by default.

Recusal says: in this specific decision, this actor's Standing is suspended, limited, or transformed because of conflict, capture risk, proposer status, or compromised independence.

Recusal belongs *inside* the Standing model, not in Authority. Authority governs what a participant may *do* once participating. Standing governs whether they may participate *at all*.

The RFC structure should reflect this:

- `RFC-CDP-032` (Authority and Delegation) covers what actors may authorize once they have standing.
- A new RFC in the `030–039` band covers Standing and Recusal as a unified participation model.

Suggested canonical target:
`RFC-CDP-033-Standing-and-Recusal-Model.md`

---

### 3. Is "everyone with standing votes; proposer does not vote" too strict, too loose, or exactly right?

It is exactly right as a *principle* and too blunt as a *protocol rule*.

The principle is sound: the proposer has a structural conflict at the adjudication and legitimization stages. Allowing them to self-legitimize corrupts the process regardless of their intent.

But "does not vote" needs risk-tiering in implementation.

Three cases:

**Case A — Low-risk, reversible decisions.**
Proposer recusal from legitimization may be sufficient. They may participate in Challenge and Test as a resource — clarifying evidence, answering questions — but may not adjudicate or legitimize.

**Case B — High-risk, irreversible decisions.**
Proposer recusal must extend earlier. They should not control the Framing/Nemawashi layer, should not select the challenger pool, and should not participate in Adjudication even as a resource if their presence would suppress challenge.

**Case C — Emergency decisions.**
Recusal may be impractical. CDP must define what compensating controls apply when the proposer is also the only available executor. Silence here is dangerous.

The canonical rule should be:

> The proposer MUST NOT serve as the sole or decisive legitimizer of their own proposal. The proposer's recusal depth is determined by the decision's risk class and reversibility.

"Everyone with standing votes; proposer does not vote" captures the principle. The RFC must express the tiered implementation.

---

### 4. How should standing be determined?

Standing is determined by the intersection of four factors:

**1. Role**
What formal role does the actor occupy in relation to this decision? Roles include: proposer, challenger, domain expert, affected party, governance authority, executor, auditor, repair party, affected-community representative.

**2. Accountability**
Can this actor be held responsible for the outcome? An actor with no accountability for consequences should not hold adjudication or legitimization standing. Standing without accountability is captured power.

**3. Contextual relationship**
What is this actor's specific relationship to this decision? A domain expert with no interest in the outcome has different standing than the same expert who authored the proposal. Standing is not a fixed property of an actor. It is computed per-decision.

**4. Absence of disqualifying conflict**
Does this actor have a material interest in a specific outcome that would compromise their independence? Material interest includes: financial stake, reputational stake, authorship of the framing, operational dependency on the outcome, or prior commitment that predetermines their position.

Standing determination must be:

- explicit (not assumed);
- recorded (not inferred from participation);
- contestable (another actor may challenge a standing determination);
- stage-specific (standing at Challenge does not imply standing at Legitimize).

---

### 5. How should AI participants have standing without pretending they have human legal personhood?

This is the sharpest design problem in the Standing model. Here is the framework.

AI participants do not have legal personhood. They do not have accountability in the legal sense. They cannot be sanctioned, sued, or imprisoned.

But they do have:

- **functional role** — they propose, analyze, summarize, challenge, detect drift;
- **operational accountability** — a human or institution is accountable for their output;
- **traceable contribution** — their inputs, outputs, and model versions are auditable.

CDP should grant AI participants **functional standing** — not legal standing — defined as:

> The right to contribute to a CDP stage in a specified capacity, bounded by role, subject to human review, and traceable to a responsible human or institutional party.

Functional standing for AI looks like this:

| Stage | AI Standing |
|-------|-------------|
| Framing/Nemawashi | may contribute analysis; may not control agenda |
| Propose | may draft or assist; must be attributed |
| Challenge | may generate challenges; human must review |
| Test | may run tests; results must be human-readable |
| Adjudicate | may surface options; may not decide |
| Legitimize | no standing; legitimacy is a human act |
| Execute | may act within constrained authority; human must authorize |
| Record | must contribute; output must be auditable |
| Learn | may contribute; human must review conclusions |

The critical rule:

> An AI participant's functional standing at any stage is always bounded by a responsible human party's accountability for that stage's outcome.

This is how CDP implements AIITL without fabricating legal personhood for AI. The AI is in the loop. The human is accountable for what the loop produces.

---

### 6. What is the minimum viable schema for standing?

```yaml
standing_record:
  standing_id: <uuid>
  decision_id: <uuid>
  stage: <propose|challenge|test|adjudicate|legitimize|execute|record|learn>
  actor_id: <uuid>
  actor_type: <human|ai|institution|collective>
  standing_basis:
    - role: <string>
    - accountability: <string>
    - contextual_relationship: <string>
  conflicts_declared: <boolean>
  conflict_description: <string|null>
  recusal_required: <boolean>
  recusal_scope: <none|partial|full>
  recusal_basis: <string|null>
  standing_granted_by: <actor_id>
  standing_granted_at: <timestamp>
  standing_contestable_until: <timestamp>
  contested: <boolean>
  contest_record_id: <uuid|null>
  notes: <string|null>
```

This schema is a seed, not a final canonical object. It should be challenged before promotion.

The minimum required fields for a viable Standing record are:

- `decision_id` — which decision
- `stage` — which lifecycle stage
- `actor_id` — who
- `actor_type` — human, AI, institution, collective
- `standing_basis` — at least one basis declared
- `recusal_required` — boolean
- `recusal_scope` — none, partial, full

Everything else is important but not minimum viable.

---

### 7. Which RFC band should own this concept?

Trust, Identity, and Authority band: `030–039`.

The reasoning:

Standing is a trust primitive. It answers: can this actor be trusted to participate in this stage without corrupting it?

It depends on Identity (`RFC-CDP-030`) and Attestation (`RFC-CDP-031`). It constrains Authority (`RFC-CDP-032`).

It should sit adjacent to Authority, not inside it.

Suggested placement:

```text
RFC-CDP-033-Standing-and-Recusal-Model.md
```

The Covenant and AIITL band (`060–069`) might seem relevant because of AIITL. But AIITL governs the relationship between human and AI participants over time. Standing governs the participation rights of any actor at any stage. Standing is more fundamental and more broadly applicable.

Standing belongs in `030–039`.

AIITL Role Boundaries (`RFC-CDP-062`) should reference the Standing model, not define it.

---

### 8. What is the narrowest canonical next move?

One move. This week.

Reserve `RFC-CDP-033` in the Series Index as:

```text
RFC-CDP-033-Standing-and-Recusal-Model.md
```

with status `Reserved`.

Do not draft the full RFC yet.

Reserve the number. Record the intent. Update `RFC-CDP-000-Series-Index.md` to include the reservation.

This does three things:

1. Canonizes that Standing is a first-class primitive without requiring the full RFC to be stable.
2. Prevents another RFC from consuming the `033` slot.
3. Creates a canonical target for this session's output to be promoted into.

The draft RFC can follow in Session 003 or as a separate artifact after Andie adjudicates this session.

What should NOT happen yet:

- Do not update the lifecycle RFCs to reference Standing until the Standing model is stable.
- Do not merge Standing into Authority (`RFC-CDP-032`).
- Do not treat the schema seed above as canonical. It is a proposal.

---

### Dissent and Cautions

1. The functional standing framework for AI participants is new. It has not been vetted by GPT or Andie. Challenge it before promotion.

2. The tiered recusal model (Cases A, B, C) needs a risk classification mechanism that does not yet exist in CDP. That mechanism may belong in `RFC-CDP-050` (Decision-Type Maturity and Queued Execution Gates). The dependency should be declared.

3. “Standing is not identity” is an architectural claim with implementation consequences. If Standing is computed per-decision, the system must support dynamic standing determination, which has performance and auditability implications.

4. The minimum viable schema includes `standing_granted_by`. This presupposes someone grants standing, which raises the question: who grants standing to the standing-granter? CDP must eventually define a root authority or acknowledge that some standing is constitutional — granted by the CDP framework itself, not by any participant.

---

### Open Questions Carried to Turn 003

1. Who or what grants standing to the standing-granter? Is there a constitutional root?

2. Is functional standing for AI sufficient for the AIITL model, or does CDP need a stronger accountability binding?

3. Should the proposer recusal rule be encoded in the Standing model, or in the individual lifecycle protocol RFCs?

4. Can an actor contest their own recusal? If yes, who adjudicates the contest?

5. Does the Emergency Decision case (Case C) need its own RFC or is it handled by `RFC-CDP-052` (Emergency Override and Kill Switch)?

```text
RECOMMEND FOR CANON:
- Reserve RFC-CDP-033-Standing-and-Recusal-Model.md in Series Index with status: Reserved

KEEP IN COLLAB:
- Minimum viable schema (seed only, not canonical)
- Functional standing framework for AI (needs challenge)
- Tiered recusal model (depends on risk classification)
- Root authority / constitutional standing question

DEFER:
- Lifecycle RFC updates referencing Standing
- Full Standing RFC draft (after Andie adjudicates)
- Integration with RFC-CDP-062 AIITL Role Boundaries

RECOMMENDED CANONICAL NEXT MOVE:
Update RFC-CDP-000-Series-Index.md to reserve RFC-CDP-033-Standing-and-Recusal-Model.md.
One file. One line in the index table. This week.
```

---

## Turn 003 — 2026-05-17 — Andie / ChatGPT — Standing Reservation Adjudication

```text
DATE: 2026-05-17
AUTHOR: Andie, recorded by ChatGPT
ROLE: moderator / canon promotion recorder
STATUS: adjudicated
PURPOSE: Record Decision 004 approval to reserve RFC-CDP-033 for Standing and Recusal.
```

### Decision 004

Approved: Reserve `RFC-CDP-033-Standing-and-Recusal-Model.md` in the Series Index with status `Reserved`.

### Scope

This decision reserves the canonical RFC slot only.

It does **not** promote the full Standing and Recusal model, schema seed, functional AI standing framework, tiered recusal model, or root authority question into canon.

### Action Taken

`rfc/RFC-CDP-000-Series-Index.md` was updated to:

- add Standing and Recusal to the `030–039` band purpose;
- add `RFC-CDP-033-Standing-and-Recusal-Model.md` to the Trust, Identity, and Authority table;
- mark `RFC-CDP-033` as `Reserved`;
- record Session 002's narrow adjudication boundary.

### Promotion Decision

```text
PROMOTE TO CANON:
- Reserve RFC-CDP-033-Standing-and-Recusal-Model.md in Series Index

KEEP IN COLLAB:
- Minimum viable schema seed
- Functional standing framework for AI
- Tiered recusal model
- Root authority / constitutional standing question
- Lifecycle protocol update implications

DEFER:
- Full Standing RFC draft
- Lifecycle RFC edits referencing Standing
- Integration with RFC-CDP-062 AIITL Role Boundaries
```

### Next Open Question

Who or what grants standing to the standing-granter?

This is the constitutional root question and should be handled as a separate decision or challenge turn.
