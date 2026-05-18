# Session 003 Shared Chat: Decision Envelope

```text
SESSION: 003-decision-envelope
DATE_OPENED: 2026-05-17
MODERATOR: Andie
STATUS: active
MODE: shared-chat-file
CANON_TARGET: RFC-CDP-021-Envelope-Schema.md
PURPOSE: Define or refine the Decision Envelope as the container that carries decision context, standing, evidence, challenge, adjudication, legitimacy, execution constraints, record, and learning.
```

## How to Use This File

This is a shared chat transcript and working record for Session 003.

All participants should write directly into this single file using dated turns.

The working pattern is:

```text
Turn -> Response -> Challenge -> Moderator Adjudication -> RFC Update -> Series Index Update if needed
```

Approved decisions are RFC-first by default.

Do not leave approved architecture only in `collab/` unless Andie explicitly marks it discussion-only.

---

## Participants

- **Andie** — moderator, originator, human adjudicator
- **ChatGPT** — synthesizer, continuity keeper, protocol drafter
- **Claude / Sonnet** — challenger, coherence reviewer, human-readability critic, schema-drift detector
- **Other collaborators** — invited as named contributors

---

## Session Question

What must the CDP Decision Envelope contain so a consequential decision remains legible, legitimate, auditable, contestable, executable only under authority, recordable, repairable, and learnable?

---

## Background

Session 001 identified the Decision Envelope as a likely load-bearing structure.

Session 002 created and refined `RFC-CDP-033-Standing-and-Recusal-Model.md`, grounding Standing and Recusal as first-class concepts.

The Decision Envelope now needs to carry or reference Standing and Recusal information without becoming an unreadable junk drawer.

The envelope should prevent schema drift between:

- human-readable explanation;
- machine-readable schema;
- challenge record;
- standing record;
- evidence record;
- adjudication record;
- legitimacy basis;
- execution constraints;
- repair / appeal / learning record.

---

## Relevant Canonical Files

Read these first:

1. `https://github.com/AndieWill510/cdp/blob/main/skills/CDP_CONTEXT_FOR_CLAUDE.md`
2. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-000-Series-Index.md`
3. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-001-Vision-Scope-Principles.md`
4. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-021-Envelope-Schema.md`
5. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-033-Standing-and-Recusal-Model.md`
6. `https://github.com/AndieWill510/cdp/blob/main/collab/sessions/003-decision-envelope.md`

---

## Initial Envelope Hypothesis

A Decision Envelope should carry or reference at least:

- envelope identity;
- decision identity;
- lifecycle stage;
- proposer;
- framing / Nemawashi context;
- standing records;
- recusal records;
- affected-party standing claims;
- evidence;
- assumptions;
- challenges;
- tests;
- adjudication;
- legitimacy basis;
- dissent;
- execution constraints;
- record links;
- repair / appeal hooks;
- learning feedback;
- human-readable summary;
- machine-readable payload;
- schema version;
- lineage and provenance.

This is a hypothesis, not final schema.

---

## Core Risk

The Decision Envelope can fail in two opposite ways:

1. **Too thin:** it does not carry enough context to make the decision auditable or contestable.
2. **Too fat:** it becomes a pile of every artifact ever produced, making humans unable to inspect it.

The design problem is not “put everything in the envelope.”

The design problem is:

> What must travel with the decision, what may be linked by reference, and what must remain externally governed?

---

## Issues to Decide

This session should produce one narrow decision at a time.

Candidate decisions:

1. Should RFC-CDP-021 be treated as the canonical Decision Envelope RFC?
2. Should the envelope include full payloads or references to governed records?
3. Should Standing and Recusal be embedded in the envelope or referenced by ID?
4. Should the envelope include a required human-readable summary?
5. Should the envelope define normative schema blocks directly?
6. Should the envelope define required lineage and versioning fields?
7. What is the minimum viable envelope schema?
8. What is the narrowest RFC update to make next?

---

## Turn 001 — 2026-05-17 — Andie / ChatGPT — Session Opening

```text
DATE: 2026-05-17
AUTHOR: Andie, recorded by ChatGPT
ROLE: moderator / session opener
STATUS: active
PURPOSE: Record Decision 010 approval and open Session 003 on the Decision Envelope.
```

### Decision 010

Approved: Open Session 003 on **Decision Envelope**.

### Scope

This session is about `RFC-CDP-021-Envelope-Schema.md` and the Decision Envelope as a load-bearing CDP object.

This session is not yet a decision to rewrite every lifecycle protocol.

### Working Hypothesis

The Decision Envelope is the container and lineage surface that allows CDP to keep proposal, standing, challenge, evidence, adjudication, legitimacy, execution, record, repair, and learning connected without collapsing them into an unreadable pile.

### Caution

Do not make the envelope a junk drawer.

The envelope should carry required identity, state, lineage, and references. It should embed payloads only when necessary for integrity, portability, or audit.

---

## Turn 002 — 2026-05-17 — ChatGPT — Decision Envelope Position

```text
DATE: 2026-05-17
AUTHOR: ChatGPT
ROLE: synthesizer / protocol drafter / architecture critic
STATUS: draft
PURPOSE: State ChatGPT's position on the Decision Envelope before Claude / Sonnet challenge.
```

### 1. Failure Mode

The Decision Envelope must prevent **context severance**.

Context severance happens when a decision artifact keeps the final answer but loses the governed path that made the answer legitimate or illegitimate.

The classic failure looks like this:

```text
proposal -> summary -> approval -> execution
```

But the system can no longer reconstruct:

- who had standing;
- who was recused;
- what evidence was considered;
- what challenge was raised;
- what dissent survived;
- what tests were run;
- what authority legitimized action;
- what execution constraints applied;
- what record proves any of this;
- what repair or appeal path remains available.

That is not a decision envelope.

That is a receipt for a governance ritual.

CDP needs the envelope to preserve enough context that the decision can be inspected, challenged, executed, appealed, repaired, and learned from without requiring Andie or any single human to remember the whole story.

### 2. My Strong Position

The envelope should be a **manifest**, not a warehouse.

It should carry:

- identity;
- stage;
- status;
- required summary;
- required authority / standing references;
- required lineage;
- required schema versions;
- required hashes or integrity markers;
- governed links to heavy artifacts.

It should not embed every challenge memo, evidence file, test output, repair record, or learning artifact by default.

A Decision Envelope that contains everything becomes human-in-the-pile architecture.

A Decision Envelope that references nothing becomes legitimacy theater.

The right design is:

> carry the control surface; reference the governed record.

### 3. Minimum Viable Envelope

A minimum viable envelope should include:

```yaml
decision_envelope:
  envelope_id: <uuid>
  envelope_schema_version: <semver>
  decision_id: <uuid>
  decision_type: <string>
  lifecycle_stage: <nemawashi|propose|challenge|test|adjudicate|legitimize|execute|record|learn|repair|appeal>
  status: <draft|under_challenge|under_test|adjudicated|legitimized|execution_queued|executed|recorded|appealed|repair_required|closed>
  created_at: <timestamp>
  updated_at: <timestamp>
  created_by: <actor_id>

  human_summary:
    summary_text: <string>
    known_uncertainties: [<string>]
    material_dissent: [<record_ref>]
    plain_language_status: <string>

  authority_and_standing:
    proposer_ref: <actor_or_record_ref>
    standing_record_refs: [<standing_record_id>]
    recusal_record_refs: [<recusal_record_id>]
    affected_party_refs: [<actor_or_claim_ref>]
    legitimacy_authority_ref: <actor_or_authority_ref|null>

  governed_record_refs:
    framing_ref: <record_ref|null>
    proposal_ref: <record_ref|null>
    evidence_refs: [<record_ref>]
    challenge_refs: [<record_ref>]
    test_refs: [<record_ref>]
    adjudication_ref: <record_ref|null>
    legitimacy_ref: <record_ref|null>
    execution_constraint_ref: <record_ref|null>
    execution_record_ref: <record_ref|null>
    appeal_refs: [<record_ref>]
    repair_refs: [<record_ref>]
    learning_refs: [<record_ref>]

  integrity:
    payload_hashes: [<hash_ref>]
    lineage_refs: [<record_ref>]
    supersedes_envelope_id: <uuid|null>
    superseded_by_envelope_id: <uuid|null>

  machine_payload:
    payload_type: <string>
    payload_schema_version: <semver>
    payload_ref: <record_ref|null>
    embedded_payload: <object|null>
```

This is still too large for some contexts, but it is the right conceptual minimum: identity, human readability, authority / standing, governed references, integrity, and payload pointer.

### 4. Embedded vs Referenced

The envelope should embed only what must remain inseparable from the decision object.

Embed:

- envelope identity;
- decision identity;
- lifecycle stage;
- status;
- schema version;
- human-readable summary;
- high-level uncertainty/dissent flags;
- record references;
- integrity hashes;
- minimal payload metadata.

Reference:

- full evidence;
- full challenge memos;
- full test results;
- standing records;
- recusal records;
- adjudication records;
- legitimacy records;
- execution logs;
- appeal records;
- repair records;
- learning artifacts.

Exception:

If portability or tamper-resistance requires embedding a small payload, `embedded_payload` is allowed, but the envelope must still declare payload type and schema version.

### 5. Standing and Recusal

Standing and Recusal should be referenced by ID, not embedded in full.

Reason:

Standing is dynamic, contestable, and stage-specific. If full standing records are embedded into every envelope snapshot, the envelope becomes stale or bloated.

The envelope should carry:

- `standing_record_refs`
- `recusal_record_refs`
- `affected_party_refs`
- `legitimacy_authority_ref`

It should also carry a high-level flag or status if standing is contested:

```yaml
standing_status: <unreviewed|valid|contested|recusal_required|blocked>
```

That gives humans a control-surface warning without embedding the whole standing subsystem.

### 6. Human-Readable Surface

The envelope must require a human-readable surface.

Minimum required fields:

```yaml
human_summary:
  summary_text: <string>
  plain_language_status: <string>
  known_uncertainties: [<string>]
  material_dissent: [<record_ref>]
```

A decision envelope without a human-readable surface is not human-in-the-loop. It is human-near-the-machine-readable-object, which is not the same thing and should not be allowed to wear the jacket.

But the summary must not pretend to be the record.

The summary must point to the record.

### 7. Normative Schema Blocks

RFC-CDP-021 should include normative schema blocks directly.

This is the schema-drift lesson from Session 001.

If the envelope RFC has only prose, implementation drift is guaranteed.

The RFC should include:

- required fields;
- optional fields;
- allowed lifecycle stages;
- allowed status values;
- required references;
- integrity expectations;
- versioning rules;
- human-readable surface requirements.

### 8. My Narrowest RFC Update

The narrowest RFC-first move is:

> Patch RFC-CDP-021 to define the envelope as a manifest, not a warehouse.

Specifically:

1. Add the failure mode: context severance.
2. Add the rule: carry the control surface; reference the governed record.
3. Add minimum viable envelope schema.
4. Add embedded-vs-referenced rules.
5. Add Standing / Recusal connection to RFC-CDP-033.
6. Add required human-readable surface.

Do not rewrite every lifecycle RFC yet.

Do not finalize all schema fields as Accepted.

Advance RFC-CDP-021 to the next Draft version.

### 9. What I Want Claude / Sonnet to Challenge

Claude / Sonnet should challenge:

1. Is “manifest, not warehouse” too thin?
2. Does referencing standing records create integrity risk?
3. Should the human summary be embedded or separately versioned?
4. Is `machine_payload.embedded_payload` a trapdoor back into junk-drawer design?
5. Should the envelope contain lifecycle history or only current state plus references?
6. What is the smallest envelope that still prevents context severance?
7. What exact RFC-CDP-021 patch should be made next?

---

## Turn 003 — Pending — Claude / Sonnet — Decision Envelope Challenge Memo

Claude / Sonnet:

Read:

1. `https://github.com/AndieWill510/cdp/blob/main/skills/CDP_CONTEXT_FOR_CLAUDE.md`
2. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-000-Series-Index.md`
3. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-001-Vision-Scope-Principles.md`
4. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-021-Envelope-Schema.md`
5. `https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-033-Standing-and-Recusal-Model.md`
6. `https://github.com/AndieWill510/cdp/blob/main/collab/sessions/003-decision-envelope.md`

Then draft **Turn 003 — Claude / Sonnet — Decision Envelope Challenge Memo**.

Please answer:

1. What failure mode should the Decision Envelope prevent?
2. Is ChatGPT's “manifest, not warehouse” framing correct, too thin, or too permissive?
3. What is the minimum viable envelope?
4. What belongs inside the envelope versus linked by reference?
5. How should Standing and Recusal connect to the envelope?
6. What human-readable surface is required?
7. What machine-readable schema fields are required?
8. What should RFC-CDP-021 say that it probably does not yet say?
9. What is the narrowest RFC update you recommend?

Do not flatter.

Do not collapse uncertainty.

Name the governance failure mode precisely.

Also include a proposed patch section for:

`https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-021-Envelope-Schema.md`

---

## Promotion Decision

Pending.

```text
PROMOTE TO CANON:
PROMOTE WITH CHANGES:
DO NOT PROMOTE:
DEFER:
```
