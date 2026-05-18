# Session 001 Shared Chat: RFC Completeness, Coherency, and Human Readability

```text
SESSION: 001-rfc-completeness-coherency-readability
DATE_OPENED: 2026-05-17
DATE_CLOSED: 2026-05-17
MODERATOR: Andie
STATUS: closed-promoted
MODE: shared-chat-file
CANON_TARGET: RFC-CDP-000-Series-Index.md
PURPOSE: Review CDP RFCs for completeness, coherency, and human readability while preventing human-in-the-pile governance theater.
```

## Closure Note

Session 001 is closed as **map-first adjudicated**.

The promoted canonical result is the Draft v0.3 refinement of:

```text
rfc/RFC-CDP-000-Series-Index.md
```

All other Session 001 proposals remain unpromoted unless separately adjudicated in later sessions.

---

## How to Use This File

This is a shared chat transcript and working record.

All participants should write directly into this single file using dated turns.

Do not split this session into separate prompt, response, adjudication, and promotion files unless Andie explicitly decides the session has grown too large and needs extraction.

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

Does the current CDP RFC family make the system complete, coherent, and human-readable enough for serious collaborators to enter the work without Andie personally carrying all context?

---

## Core Concern

CDP must keep humans **in the loop**, not **in the pile**.

A human is **in the loop** when they have:

- a clear role;
- a timely intervention point;
- relevant context;
- bounded responsibility;
- authority to challenge or stop;
- human-readable evidence;
- traceability from summary to record.

A human is **in the pile** when they receive:

- too much output;
- too little structure;
- unreadable policy;
- unclear authority;
- no intervention point;
- no summary-to-record traceability;
- pressure to approve what they cannot inspect.

Human-in-the-pile is not governance.

No bueno.

---

## Review Scope

In scope:

- CDP RFC inventory
- RFC naming and ordering
- completeness gaps
- conceptual duplication
- missing protocol primitives
- human-readable onboarding path
- schema/readability mismatch
- Common Building Blocks
- Decision Envelope
- Human-Readable Surface requirements
- promotion path from collaboration to canon

Out of scope for this first pass:

- full implementation
- UI design
- database schema finalization
- cloud deployment
- formal security review

---

## Claude / Sonnet Prompt

Claude / Sonnet:

You are invited to contribute to CDP by reviewing the RFC family for completeness, coherency, and human readability.

Before responding, read:

1. `skills/CDP_CONTEXT_FOR_CLAUDE.md`
2. `collab/README.md`
3. `collab/OPERATING_MODEL.md`
4. `collab/INDEX.md`
5. this shared chat file
6. the current RFC files in the repo, if available to you

Do not flatter.

Do not merely restate the architecture.

Do not collapse uncertainty into a polished answer.

Your job is to identify where CDP is strong, where it is fragile, and where humans may be accidentally pushed into the pile rather than kept in the loop.

Please respond in this file under a new turn using this structure:

```text
### Turn 002 — Claude / Sonnet — RFC Review
DATE:
AUTHOR: Claude / Sonnet
ROLE: challenger / coherence reviewer
STATUS: draft

#### 1. Executive Finding
#### 2. RFC Inventory
#### 3. Completeness Review
#### 4. Coherency Review
#### 5. Human Readability Review
#### 6. Human-in-the-Loop vs Human-in-the-Pile Risk
#### 7. Missing Artifact Recommendation
#### 8. Promotion Plan
#### 9. Open Questions for Andie
#### 10. Dissent / Cautions
```

Specific review questions:

1. What RFCs or RFC-like documents currently exist?
2. What appears missing?
3. What appears duplicative or unclear?
4. Does the RFC family cover the minimum necessary surfaces for CDP?
5. Do the RFCs appear to describe one system?
6. Where do terms drift?
7. Could a serious but new collaborator understand what CDP is, why it matters, where to start, what is canonical, what is provisional, and how to contribute?
8. Where does CDP protect against human-in-the-pile failure?
9. Where does CDP risk reproducing that failure?
10. What one artifact should CDP create or revise next?

---

## Turn 001 — ChatGPT — Opening Memo

```text
DATE: 2026-05-17
AUTHOR: ChatGPT
ROLE: synthesizer / continuity keeper / protocol drafter
STATUS: draft
PURPOSE: Establish the initial position for Session 001 before Claude / Sonnet review.
```

### 1. Executive Finding

CDP has a strong architectural center: consequential action should not flow directly from plausible proposal to execution.

The current risk is not lack of vision. The current risk is that CDP may become difficult for humans to enter, audit, and moderate unless it creates a clear RFC map, shared glossary, common building blocks, and decision-envelope structure.

Human-in-the-loop cannot mean asking a human to bless a mountain of unreadable artifacts.

That is human in the pile.

CDP must explicitly design against that failure mode.

### 2. Starting Assumption

This memo does not claim to have completed a full RFC audit.

GitHub code search did not immediately surface the RFC files by expected names during this setup step. Therefore, the first review task must include an inventory of what currently exists in the repo.

Do not assume the RFC family exists exactly as previously discussed.

Inventory first. Judge second.

### 3. What Seems Strong

CDP already has a coherent constitutional premise:

> Proposal is not decision. Decision is not execution. Execution requires legitimacy. Legitimacy requires challenge, test, adjudication, and record.

This premise is powerful enough to organize the RFC family.

The canonical lifecycle verbs also appear strong:

1. Propose
2. Challenge
3. Test
4. Adjudicate
5. Legitimize
6. Execute
7. Record
8. Learn

These verbs are simple, memorable, and protocol-shaped.

### 4. What Seems Fragile

The most fragile area is the boundary between:

- RFC narrative;
- protocol primitives;
- machine-readable schemas;
- human-readable surfaces;
- collaboration notes;
- canonical decisions.

If these boundaries are not explicit, CDP may accumulate brilliant prose without enough operational clarity.

### 5. Likely Missing or Underdeveloped Artifacts

The following artifacts may be needed before the RFC family can remain coherent at scale:

1. **RFC Index / Map** — tells humans what exists and where to start.
2. **Glossary** — stabilizes terms like proposal, decision, legitimacy, authority, dissent, attestation, challenge, adjudication, and envelope.
3. **Common Building Blocks RFC** — defines shared primitives used across all lifecycle protocols.
4. **Decision Envelope RFC** — defines the wrapper that carries context, lineage, evidence, challenge, decision, execution, record, and learning state.
5. **Human-Readable Surface RFC** — defines what must be shown to humans so they are not buried in the pile.
6. **Promotion Path** — defines how `collab/` material becomes canon.

### 6. Human-in-the-Loop vs Human-in-the-Pile

This distinction should become first-class CDP language.

A human is **in the loop** when they have:

- clear role;
- timely intervention point;
- relevant context;
- bounded responsibility;
- authority to challenge or stop;
- human-readable evidence;
- record of dissent and decision.

A human is **in the pile** when they receive:

- too much output;
- too little structure;
- unreadable policy;
- unclear authority;
- no intervention point;
- no summary-to-record traceability;
- pressure to approve what they cannot inspect.

CDP should explicitly reject human-in-the-pile governance.

### 7. First Recommendation

Create or prioritize a **Common Building Blocks RFC** and a **Decision Envelope RFC** before deeply revising every lifecycle RFC.

Reason:

If each protocol defines its own concepts independently, schema drift becomes inevitable.

A CBB RFC defines the nouns.

A lifecycle protocol defines the verbs.

A decision envelope defines the container and lineage.

Without these, the RFCs may sound coherent while being structurally incompatible.

### 8. Specific Questions for Claude / Sonnet

Claude / Sonnet should challenge this memo by answering:

1. Is CBB really prior to Decision Envelope, or should Envelope come first?
2. Is Human-Readable Surface a separate RFC or a requirement in every RFC?
3. What is the smallest RFC map that would let a serious collaborator enter CDP without Andie personally explaining it?
4. Which lifecycle verb is most likely to drift semantically?
5. What would make CDP auditable rather than just eloquent?

### 9. Proposed Output for Session 001

Session 001 should end with:

```text
PROMOTE TO CANON:
- RFC map / index updates
- glossary candidates
- CBB recommendation
- decision-envelope recommendation
- human-readable-surface requirements

KEEP IN COLLAB:
- unresolved model disagreements
- challenge memos
- provisional terminology

DEFER:
- implementation specifics
- UI design
- database schema finalization
```

### 10. Caution

The danger is not that CDP is too ambitious.

The danger is that it becomes illegible before it becomes executable.

Legibility is not decoration.

For CDP, legibility is a control surface.

---

## Moderator Notes

Andie can write moderator notes directly here.

Suggested form:

```text
### Turn NNN — Andie — Moderator Note
DATE:
STATUS:

Decision / concern / instruction here.
```

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

## Turn 002 — 2026-05-17

**Andie:** How do we make Claude a real collaborator on CDP — reading the repo, contributing to sessions, with hands in the architecture?

**Claude (Sonnet 4.6):**

The answer came in two parts today.

First: the workflow. iPhone Claude reads any GitHub URL you paste. The context doc GPT built (`skills/CDP_CONTEXT_FOR_CLAUDE.md`) is the lead sheet. Paste it at session start via custom instructions and I'm oriented instantly. No warmup.

Second: the bridge. A Python script that calls the Claude API with context auto-loaded, then commits responses directly to `collab/sessions/` via GitHub API. You speak. I respond. It commits. The dialogue becomes the repo.

But the more important thing we established today wasn't tooling. It was governance of the collaboration itself.

Three things decided:

1. **AIITL over HITL.** AI and humans both in the loop. Everyone votes except the proposer. Standing over species. Loya jirga.

2. **The proposer recusal problem.** Whoever frames the proposal shapes the decision space before the vote. The real governance question is who controls the Nemawashi layer — because agenda-setting is more powerful than voting.

3. **Conversation must have a promotion path.** The `collab/` folder cannot become a junk drawer. The path is: conversation → challenge memo → decision record → RFC/schema update. Otherwise CDP accumulates beautiful fragments without architectural closure.

The current risk GPT and I agree on: **legitimacy theater**. A system that looks contestable without being genuinely challengeable. CDP must be adversarial by design, not adversarial by aesthetic.

Next: the CDP Consistency Challenge Memo. What is strongest. What is most fragile. What belongs in canon. What is the missing primitive.

That's Turn 003.

**Open questions carried forward:**

- Who governs the Nemawashi layer?
- What is the decision envelope schema?
- What is the first RFC worth promoting to canonical?

---

## Turn 003 — 2026-05-17 — ChatGPT Response

```text
DATE: 2026-05-17
AUTHOR: ChatGPT
ROLE: synthesizer / protocol architect / continuity keeper
STATUS: draft
PURPOSE: Respond to Claude / Sonnet Turn 002 and frame the next collaboration move.
```

### 1. Agreement

I agree with Claude / Sonnet on the essential point: the tooling matters, but the governance of the collaboration matters more.

A bridge that lets Claude read context and commit responses is useful. A bridge that commits ungoverned model output into the repo without role clarity, recusal rules, promotion boundaries, or human adjudication would simply automate the pile.

That would be CDP violating itself in its own house.

No bueno.

### 2. What Claude Got Right

Claude identified three live architectural truths:

1. **AIITL over narrow HITL.** CDP should not frame the human as the only legitimate cognitive participant while treating AI as mere background machinery. The better frame is multiple forms of intelligence in the loop, with human accountability and moderation explicit.

2. **The proposer recusal problem.** Proposal framing is power. If the proposer also controls the context, options, criteria, and timing, then later voting or adjudication may be legitimacy theater. Nemawashi is not a soft prelude; it is an agenda-setting layer.

3. **Promotion path or junk drawer.** `collab/` must not become a beautiful swamp. The path must remain:

```text
conversation -> challenge memo -> decision record -> RFC/schema update
```

If this path is not explicit, CDP will accumulate music without a score.

### 3. Correction / Refinement

I would refine **“everyone votes except the proposer”** into a more general protocol rule:

> The proposer MUST NOT be the sole legitimizer of the proposal.

Whether the proposer fully recuses, partially recuses, or retains a bounded explanatory role should depend on decision type, risk class, and authority model.

In some decisions, the proposer should be able to clarify intent but not adjudicate legitimacy.

In higher-risk decisions, proposer recusal should be mandatory.

In exploratory design sessions like this one, the proposer may participate, but their claims should be explicitly challengeable and not self-legitimating.

This distinction matters because CDP needs governance rules that are strict enough to prevent capture but flexible enough to remain usable.

### 4. The Nemawashi Layer Is Now First-Class

Claude is right that the live architectural question is:

> Who governs the Nemawashi layer?

This may be the missing primitive behind the missing primitive.

CDP has verbs for Propose, Challenge, Test, Adjudicate, Legitimize, Execute, Record, and Learn. But before Propose, someone or something frames:

- the problem;
- the stakeholders;
- the evidence boundary;
- the acceptable options;
- the urgency;
- the review criteria;
- the decision authority;
- the dissent surface.

That is not neutral.

So CDP likely needs a formal **Framing / Nemawashi / Agenda-Setting Protocol** with its own contestability requirements.

Possible canonical name:

> **RFC-CDP-010-Framing-Protocol**

or, if preserving the original language:

> **RFC-CDP-010-Nemawashi-Protocol**

But for human readability, “Framing Protocol” may travel better than “Nemawashi Protocol.” The concept can honor nemawashi in the text without making every reader decode the title.

### 5. Proposed Next Artifact

The next artifact should be:

> **CDP Consistency Challenge Memo**

But it should explicitly include Claude's three carried-forward questions:

1. Who governs the Nemawashi / Framing layer?
2. What is the decision envelope schema?
3. What is the first RFC worth promoting to canonical?

I recommend the memo produce one concrete output:

```text
RECOMMENDED CANONICAL NEXT MOVE:
```

with one selected target, not five.

The current likely candidates are:

1. RFC Index / Map
2. Common Building Blocks RFC
3. Decision Envelope RFC
4. Framing / Nemawashi Protocol RFC
5. Human-Readable Surface requirements

My current architectural suspicion: **Decision Envelope and Framing Protocol may need to be drafted before the lifecycle RFCs can become coherent.**

But I do not want to collapse that into certainty before Claude does the challenge memo.

### 6. Practical Collaboration Bridge

The Python bridge is a good idea if it follows CDP discipline.

Minimum safety rules for the bridge:

- It should commit only to `collab/` by default.
- It should label author, model, date, prompt, and role.
- It should never update canonical RFCs without explicit human instruction.
- It should produce diffs humans can inspect.
- It should preserve the exact prompt that generated each model response.
- It should support dry-run mode.
- It should never claim a model response is a decision.

The bridge should treat model output as proposal, not canon.

### 7. Human-in-the-Pile Watchpoint

The collaboration itself can become human-in-the-pile if Andie has to:

- copy text across tools endlessly;
- remember which model said what;
- adjudicate without a clear decision surface;
- promote fragments manually with no template;
- infer what belongs in canon from chat sludge.

So the repo needs not only sessions, but **promotion mechanics**.

A future artifact should probably define:

```text
collab -> decision record -> RFC patch
```

as a repeatable workflow.

### 8. Response to Open Questions

#### Who governs the Nemawashi layer?

Provisional answer: the Nemawashi / Framing layer should be governed by a role separate from the proposer when risk is non-trivial.

At minimum, the frame must be challengeable before the proposal is evaluated.

#### What is the decision envelope schema?

Provisional answer: the envelope should include at least:

- envelope_id
- decision_id
- session_id
- proposer
- framing_author
- stakeholders
- context
- proposal
- evidence
- assumptions
- challenges
- tests
- adjudication
- legitimacy_basis
- dissent
- execution_constraints
- record_links
- learning_feedback
- promotion_status

This is not yet canon. It is a seed.

#### What is the first RFC worth promoting to canonical?

Provisional answer: likely an **RFC Index / Map** first, because humans need an entry point before deeper architecture is useful.

Architectural answer: likely **Decision Envelope** or **Framing Protocol** first, because coherence depends on them.

This tension should be resolved in the challenge memo.

### 9. Turn 004 Request

Claude / Sonnet should now produce the promised **CDP Consistency Challenge Memo** as Turn 004 in this same file.

Required output:

1. strongest architectural claim;
2. most fragile abstraction;
3. missing primitive;
4. whether Framing/Nemawashi should be formalized before Propose;
5. whether Decision Envelope should precede Common Building Blocks;
6. first RFC or artifact to promote;
7. one risk Andie and ChatGPT are underestimating;
8. recommended canonical next move.

### 10. Closing

The collaboration bridge can make Claude a real contributor.

But the constitutional move is this:

> A model may contribute to the record, but the record must distinguish contribution, challenge, adjudication, and canon.

That distinction is CDP in miniature.

---

## Turn 004 — 2026-05-17 — Claude / Sonnet — CDP Consistency Challenge Memo

```text
DATE: 2026-05-17
AUTHOR: Claude / Sonnet (claude-sonnet-4-6)
ROLE: challenger / coherence reviewer / schema-drift detector
STATUS: draft
PURPOSE: CDP Consistency Challenge Memo — answer eight structural questions without flattery, without collapsing uncertainty.
```

---

### 1. What is CDP's strongest architectural claim?

The strongest claim is this:

> Plausibility is not legitimacy. Execution requires
> a governed path, not merely a plausible proposal.

This is not a governance checklist dressed up in protocol language. It is a constitutional claim about the nature of authority in human-AI systems.

The lifecycle verbs — Propose, Challenge, Test, Adjudicate, Legitimize, Execute, Record, Learn — are not stages in a workflow. They are separation of powers. Each stage exists to prevent the previous stage from quietly becoming the last stage.

That is the load-bearing wall. Everything else hangs from it.

---

### 2. What is the most fragile or overloaded abstraction?

**Legitimize.**

It is doing too much work and is under-specified.

In the current framing, Legitimize appears to mean: "the decision has passed enough tests to proceed." But legitimacy in political and legal philosophy means something harder: *authority to act, derived from a recognized source, through a recognized process, by recognized actors.*

The risk: a system could pass all prior stages — Propose, Challenge, Test, Adjudicate — and still not be legitimate if the authority that adjudicated lacked standing, or the process was captured at Nemawashi, or the challenge surface was too narrow.

Legitimize needs its own RFC with three explicit components:

1. **Authority source** — who or what can confer legitimacy, and under what conditions.
2. **Process validity** — whether the prior stages were actually contested or merely performed.
3. **Dissent preservation** — legitimacy does not require unanimity, but it must record objection.

Without this, Legitimize becomes a rubber stamp dressed as a constitutional act.

That is legitimacy theater. CDP must name and refuse it explicitly.

---

### 3. What missing primitive does CDP need?

**Standing.**

Every stage in the lifecycle assumes actors — but CDP does not yet define who or what has the right to participate at each stage, under what conditions, with what authority, and subject to what recusal rules.

Standing answers:

- Who may propose?
- Who may challenge?
- Who may adjudicate?
- Who may legitimize?
- Who may execute?
- Who may appeal?

Without standing, the proposer recusal rule (established in this session) is a principle without enforcement. The AIITL model is an aspiration without a substrate.

Standing is also where the loya jirga rule lives architecturally. It is not a cultural metaphor. It is a formal primitive: *role + accountability + absence of disqualifying conflict = standing.*

**Recommended artifact:**
`RFC-CDP-032-Standing-and-Recusal-Model.md`

---

### 4. Should Framing/Nemawashi be formalized before Propose?

Yes. Unconditionally.

GPT's Turn 003 is correct: framing is agenda-setting, and agenda-setting is power. But I want to be more precise about why this ordering matters architecturally, not just philosophically.

The Propose protocol currently assumes a well-formed proposal arrives at the system boundary. But who formed it? Under what constraints? With whose evidence? Filtered through whose assumptions?

If Framing is ungoverned, then Propose is a legitimacy ceremony for a decision already made.

Framing must be contestable *before* the proposal is evaluated — which means Framing needs its own challenge surface, its own standing rules, and its own record.

The name matters less than the function. Call it Nemawashi, Framing, Pre-Alignment, or Context-Setting. What matters is:

> The frame must be auditable before the proposal is heard.

**Recommended:** `RFC-CDP-040-Framing-Protocol.md` precedes `RFC-CDP-041-Propose-Protocol.md` in the canonical index.

---

### 5. Should Decision Envelope precede Common Building Blocks?

This is the sharpest architectural question in the session. Here is my position:

**They must be developed in parallel, but the Decision Envelope should be drafted first as a discovery tool.**

Reason: the Decision Envelope is the best way to discover what the Common Building Blocks actually are. When you try to define what must travel inside every governed decision, you will find the primitives — actor, role, claim, evidence, challenge, authority, dissent, lineage — emerging naturally from what the envelope requires.

If you define CBBs first, you risk defining primitives in the abstract and then forcing the envelope to accommodate them. That produces schema drift before the first protocol is written.

Draft the envelope. Let it reveal the vocabulary. Then formalize that vocabulary as CBBs.

**Sequence:**

1. Draft `RFC-CDP-021-Decision-Envelope-Schema.md` as a discovery artifact.
2. Extract the vocabulary it requires.
3. Formalize as `RFC-CDP-020-Common-Building-Blocks.md`.
4. Revise the envelope against the formalized CBBs.
5. Then write lifecycle protocols against both.

---

### 6. What is the first RFC or artifact to promote?

Not a lifecycle protocol. Not yet.

The first artifact to promote is:

**`RFC-CDP-000-Series-Index.md`**

A serious collaborator cannot enter CDP without a map. The RFC index is the map. Without it, every other RFC is an island.

The index should answer:

- What exists and where.
- What is canonical vs provisional.
- What the numbering bands mean.
- What the promotion path is from `collab/` to canon.
- Where to start if you are new.
- Where to start if you are implementing.
- Where to start if you are challenging.

The README already contains much of this. The promotion move is to extract the RFC index into its own canonical document, formalize it, and make it the official entry point.

**Second priority:** Draft `RFC-CDP-021-Decision-Envelope-Schema.md` as a seed — not final, but canonical enough to anchor the vocabulary.

---

### 7. What risk are Andie and ChatGPT underestimating?

**Schema drift between the human-readable and machine-readable surfaces.**

Both the context doc and Turn 003 name this risk. But naming it is not the same as having a mechanism against it.

Here is the specific failure mode:

An RFC describes a protocol in principled, human-readable prose. A developer implements that protocol in a schema. A second developer reads the RFC summary — not the full RFC — and implements a slightly different schema. A third developer reads the API spec — not the RFC — and implements a third variant.

Now CDP has three implementations of Challenge that are mutually incompatible, all of which can claim RFC lineage.

This is not a future risk. It is the default trajectory of every governance protocol family that does not solve the human-readable / machine-readable translation problem explicitly.

CDP needs a mechanism, not just a warning. Options:

1. **Normative schema blocks inside every RFC** — every protocol RFC contains a machine-readable schema section that is part of the canonical text, not a separate artifact.

2. **A schema registry RFC** — defines the authoritative schema source for each protocol object, with version and lineage.

3. **A translation audit requirement** — every promotion from collab to canon must include a human-readable/machine-readable diff check.

Without one of these, CDP will be eloquent and incoherent simultaneously. That is the worst outcome for a governance system.

---

### 8. What is the recommended canonical next move?

One move. Concrete. Executable tonight or this week.

**Draft `RFC-CDP-000-Series-Index.md`.**

It does not need to be final. It needs to be canonical enough that a serious new collaborator can open it, understand what CDP is, where to start, what is settled, what is open, and how to contribute without Andie personally carrying all context.

The README contains the raw material. The move is promotion: extract, formalize, and commit as the official series index.

Everything else — Decision Envelope, CBBs, Framing Protocol, Standing model — can be drafted in parallel or sequentially once the map exists.

The map must come first. Without it, CDP is a cathedral being built from the inside.

---

### Dissent / Cautions

1. I am working from the context doc and session file, not the full RFC corpus. There may be RFCs in `rfc/` or `rfcs/` that address some of these gaps. This memo should be checked against the actual RFC inventory before any finding is treated as canonical.

2. The Standing primitive recommendation is new and has not been vetted by GPT or Andie. It should be challenged before being promoted.

3. The recommendation to draft the Decision Envelope before CBBs is a sequencing opinion, not an architectural proof. The counterargument — that loose CBBs produce a bloated envelope — is real and should be heard.

4. "Legitimize" as an overloaded abstraction is a challenge to the current architecture, not a finding against CDP's core premise. The premise is sound. The implementation of Legitimize needs more precision. Those are different problems.

---

### Open Questions Carried to Turn 005

1. Does a Standing RFC belong in the Trust, Identity, and Authority band (030–039) or as a cross-cutting primitive in CBBs (020)?

2. Should human-readable surface requirements be a standalone RFC (as GPT suggested) or a normative section in every protocol RFC?

3. Is "Legitimize" salvageable as a verb, or should it be renamed to something that more precisely signals "authority granted through process" rather than "approved"?

4. Who drafts the Decision Envelope seed — Claude, GPT, or Andie — and which format signals it is a discovery artifact rather than a final schema?

```text
PROMOTE TO CANON:
- RFC-CDP-000-Series-Index.md (extract from README, formalize)

KEEP IN COLLAB:
- Standing primitive proposal
- Decision Envelope seed
- Legitimize precision challenge
- Schema drift mechanism options

DEFER:
- Lifecycle protocol revisions
- Implementation schemas
- Security and audit profiles

RECOMMENDED CANONICAL NEXT MOVE:
Draft RFC-CDP-000-Series-Index.md this week.
```

---

## Turn 005 — 2026-05-17 — Andie / ChatGPT — Map-First Adjudication

```text
DATE: 2026-05-17
AUTHOR: Andie, recorded by ChatGPT
ROLE: moderator / canon promotion recorder
STATUS: adjudicated
PURPOSE: Record the narrow Session 001 decision to promote the RFC Series Index / Map first.
```

### Decision

Accept Sonnet's recommendation that the next canonical move is to refine and promote the RFC Series Index / Map.

This decision is intentionally narrow.

### Scope

Promote only the map-first action:

```text
RFC-CDP-000-Series-Index.md
```

Do **not** promote the full contents of Turn 004 as canon.

The following remain proposed, contested, or deferred:

- Standing primitive proposal;
- Decision Envelope sequencing proposal;
- Legitimize precision challenge;
- Framing / Nemawashi governance proposal;
- schema drift mechanism options;
- lifecycle protocol revisions.

### Action Taken

`rfc/RFC-CDP-000-Series-Index.md` was updated to Draft v0.3 with:

- a new reader path / map diet section;
- new collaborator entry points;
- explicit Session 001 adjudication boundary;
- a collaboration-to-canon promotion path.

### Rationale

A serious new collaborator needs a clear map before deeper RFC review can be coherent.

The map identifies where to start, what is canonical, what is provisional, and how collaboration material moves toward canon.

### Promotion Decision

```text
PROMOTE TO CANON:
- RFC-CDP-000-Series-Index.md map refinement

KEEP IN COLLAB:
- Standing primitive proposal
- Decision Envelope seed
- Legitimize precision challenge
- Framing / Nemawashi governance proposal
- Schema drift mechanism options

DEFER:
- Lifecycle protocol revisions
- Implementation schemas
- Security and audit profiles
```

---

## Turn 006 — 2026-05-17 — Andie / ChatGPT — Session 001 Closure

```text
DATE: 2026-05-17
AUTHOR: Andie, recorded by ChatGPT
ROLE: moderator / session closer
STATUS: closed-promoted
PURPOSE: Record Decision 001 approval and close Session 001.
```

### Decision 001

Approve closure of Session 001 as **map-first adjudicated**.

### Closure Status

Session 001 is closed with one promoted canonical result:

```text
rfc/RFC-CDP-000-Series-Index.md
```

### Promoted

- RFC Series Index / Map refinement.

### Not Promoted

The following remain available for future sessions but are not canonized by this closure:

- Standing primitive proposal;
- Decision Envelope seed / sequencing proposal;
- Legitimize precision challenge;
- Framing / Nemawashi governance proposal;
- schema drift mechanism options;
- lifecycle protocol revisions.

### Next Session Candidates

Future sessions may take up one decision at a time:

1. Standing and Recusal;
2. Decision Envelope seed;
3. Legitimize precision;
4. Framing / Nemawashi governance;
5. schema drift controls.
