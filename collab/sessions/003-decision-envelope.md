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

## Turn 003 — 2026-05-17 — Claude / Sonnet — Decision Envelope Challenge Memo

```text
DATE: 2026-05-17
AUTHOR: Claude / Sonnet (claude-sonnet-4-6)
ROLE: challenger / coherence reviewer / schema-drift detector
STATUS: draft
PURPOSE: Challenge the Decision Envelope design. Name the failure mode. Evaluate "manifest not warehouse." Define minimum viable envelope. Propose RFC-CDP-021 patch.
```

### The Failure Mode This Envelope Must Prevent

Name it precisely.

The failure mode is **governed path severance**.

Not just context severance as GPT named it — that is a symptom. The root failure is this:

A decision travels through the CDP lifecycle. Each stage produces governed artifacts — standing records, challenge memos, test results, adjudication records. But those artifacts are stored separately, governed separately, and linked loosely if at all.

When someone needs to audit, appeal, or repair the decision, they cannot reconstruct:

- which standing records governed which stage;
- whether a challenge was resolved or merely noted;
- what authority basis the legitimization used;
- whether the execution constraints derived from the adjudication or were added afterward;
- whether dissent was preserved or collapsed.

The decision record exists. The governed path that makes it legitimate is scattered, partial, or missing.

The envelope must prevent that. Not by storing everything — by being the authoritative index of what governed path existed, what was produced at each stage, and where those governed artifacts live.

A governance receipt is not a governed path.

The envelope must be a governed path index, not a receipt.

---

### 1. What failure mode should the Decision Envelope prevent?

**Governed path severance.** Defined above.

Secondary failure mode the envelope must also prevent: **summary substitution**.

Summary substitution happens when the human-readable summary of a decision is treated as equivalent to the governed record.

The summary says: "The proposal was challenged and approved."

The governed record says: "The challenge was filed, not adjudicated. The approval was granted by the proposer's delegated authority under a scope that may not have covered this decision type."

These are structurally different. If the envelope allows the summary to stand in for the record, CDP produces legible governance theater.

The envelope must require that every summary field points to the governed record it summarizes. Summary without record pointer is not allowed.

---

### 2. Is "manifest, not warehouse" correct?

Mostly correct. One structural flaw.

GPT's framing is right that the envelope should carry references, not full payloads by default. The "manifest" framing is sound.

The flaw is in the proposed `embedded_payload` field:

```yaml
machine_payload:
  embedded_payload: <object|null>
```

This is a trapdoor. Once an embedded payload field exists in the schema, implementations will use it. The "null by default" rule will drift into "embed when convenient" and then into "embed always for portability."

The correct design is not to provide the trapdoor and then instruct people not to use it. The correct design is:

> The envelope carries governed references. Portability and tamper-resistance are achieved through integrity hashes and governed record storage, not payload embedding.

If a use case genuinely requires embedded payloads — air-gapped environments, sealed legal records — that is a specific implementation profile, not a base schema feature. It belongs in an Implementation Profile RFC (`120–149` band), not in the canonical envelope.

Remove `embedded_payload` from the base envelope. Reserve it for an implementation profile.

---

### 3. What is the minimum viable envelope?

Smaller than GPT proposed. More precise.

The minimum viable envelope is the smallest structure that:

1. uniquely identifies the decision and its governed path;
2. shows current lifecycle stage and status;
3. provides a human-readable summary that points to governed records;
4. carries standing status as a control surface flag;
5. references — does not embed — all governed stage artifacts;
6. records lineage and schema version for integrity.

```yaml
decision_envelope:
  envelope_id: <uuid>
  envelope_schema_version: <semver>
  decision_id: <uuid>
  decision_type: <string>
  created_at: <timestamp>
  updated_at: <timestamp>
  created_by: <actor_id>

  lifecycle_stage: <enum>
  status: <enum>

  human_summary:
    summary_text: <string>
    plain_language_status: <string>
    known_uncertainties: [<string>]
    material_dissent_refs: [<ref>]
    summary_governed_by_ref: <ref>

  standing_status: <enum>
  standing_record_refs: [<ref>]
  recusal_record_refs: [<ref>]
  affected_party_claim_refs: [<ref>]

  stage_record_refs:
    framing_ref: <ref|null>
    proposal_ref: <ref|null>
    challenge_refs: [<ref>]
    evidence_refs: [<ref>]
    test_refs: [<ref>]
    adjudication_ref: <ref|null>
    legitimacy_ref: <ref|null>
    execution_constraint_ref: <ref|null>
    execution_record_ref: <ref|null>
    appeal_refs: [<ref>]
    repair_refs: [<ref>]
    learning_refs: [<ref>]

  integrity:
    lineage_refs: [<ref>]
    governed_path_hash: <hash>
    supersedes_envelope_id: <uuid|null>
    superseded_by_envelope_id: <uuid|null>
```

Key differences from GPT's proposal:

- No `embedded_payload`.
- `summary_governed_by_ref` is required.
- `governed_path_hash` replaces per-payload hashes.
- `standing_status` is required and top-level.

---

### 4. What belongs inside vs linked by reference?

**Inside the envelope — always:**

- envelope identity;
- lifecycle stage and status;
- the human-readable summary with required record pointer;
- standing status flag;
- all governed stage reference lists, even when empty;
- integrity hash of the governed path;
- lineage references.

**Linked by reference — always:**

- full standing records;
- full recusal records;
- affected-party claims;
- challenge memos;
- evidence artifacts;
- test results;
- adjudication records;
- legitimacy basis records;
- execution logs;
- appeal records;
- repair records;
- learning artifacts.

**Never embedded in the base schema:**

- full payloads of any governed artifact;
- model outputs;
- evidence files;
- any artifact that has its own governed lifecycle.

The test is: does this field describe the governed path, or is it content from the governed path?

Description belongs in the envelope. Content belongs in its own governed record, referenced by the envelope.

---

### 5. How should Standing and Recusal connect?

Three connection points. Each serves a different purpose.

**Connection 1 — Control surface flag.**

`standing_status` is a required top-level field in the envelope. Allowed values:

```text
unreviewed | valid | contested | recusal_active | blocked | emergency
```

This is the human-readable warning light. A reviewer scanning an envelope can see immediately whether standing is clean.

**Connection 2 — Reference lists.**

`standing_record_refs` and `recusal_record_refs` are required lists of references to the Standing records governed by RFC-CDP-033. These are not embedded. They are governed objects with their own IDs.

**Connection 3 — Stage-specific binding.**

Each stage record reference in `stage_record_refs` must be interpretable against the standing records. The adjudication record, for example, must be readable alongside the standing records to verify that the adjudicator had valid standing.

This connection is not enforced in the envelope schema itself. It is enforced in the Adjudicate Protocol RFC (`RFC-CDP-044`). The envelope carries the references. The protocol enforces the binding.

This separation is correct. The envelope is a governed path index. The protocols are the governance rules. Do not conflate.

---

### 6. What human-readable surface is required?

Four required fields. One structural rule.

```yaml
human_summary:
  summary_text: <string>
  plain_language_status: <string>
  known_uncertainties: [<string>]
  material_dissent_refs: [<ref>]
  summary_governed_by_ref: <ref>
```

The structural rule:

`summary_governed_by_ref` is not optional.

A human summary that does not point to the governed record it summarizes is not a CDP-compliant summary. It is a narrative that may or may not represent the actual governed path.

This is how CDP prevents summary substitution. The summary must be traceable to the record it claims to represent. Always.

What the summary must not do:

- claim to be the record;
- omit known uncertainties;
- suppress material dissent;
- describe the decision as more resolved than the governed record shows.

If `known_uncertainties` is empty, that is a positive claim that no material uncertainty exists. It must be attested, not assumed.

---

### 7. What machine-readable schema fields are required?

The full minimum viable schema in answer 3 is the required field set.

The fields most likely to be dropped under implementation pressure:

- `summary_governed_by_ref`
- `governed_path_hash`
- top-level `standing_status`
- required empty reference lists

All reference lists are required. Empty is a valid value. Absent is not.

---

### 8. What should RFC-CDP-021 say that it doesn't yet say?

The current RFC-CDP-021 is a wire message envelope. It defines what every CDP wire message carries: versioning, actor, protocol verb, payload, lineage.

That is not wrong. But it is not the Decision Envelope.

The Decision Envelope is a governed path index for a decision across its entire lifecycle — from framing through learning, possibly spanning months or years and dozens of individual wire messages.

These are different objects.

RFC-CDP-021 must say explicitly:

> This RFC defines two related but distinct envelope structures:
>
> 1. The Wire Message Envelope — the structure carried on every CDP protocol message.
> 2. The Decision Lifecycle Envelope — the governed path index for a complete decision across all lifecycle stages.

Currently RFC-CDP-021 only defines the wire message envelope. The decision lifecycle envelope is entirely absent.

RFC-CDP-021 also does not currently say:

- what the failure mode is;
- that the summary must point to the record;
- that `standing_status` is required;
- that empty reference lists are required;
- that `embedded_payload` is not permitted in the base schema;
- what `governed_path_hash` is and why it is required.

---

### 9. What is the narrowest RFC update recommended?

Two changes. Both to RFC-CDP-021. This week.

**Change 1 — Rename and restructure.**

Update the RFC title and abstract to distinguish:

- Wire Message Envelope;
- Decision Lifecycle Envelope.

The existing canonical fields table becomes Section 2: Wire Message Envelope.

Section 3: Decision Lifecycle Envelope is added as Draft with the minimum viable schema from this memo.

**Change 2 — Add failure mode and four normative rules.**

Add a Section 1 that states:

1. The failure mode this RFC addresses is governed path severance.
2. The Decision Lifecycle Envelope is a governed path index, not a warehouse.
3. Every human summary must include a governed record pointer.
4. `embedded_payload` is not permitted in the base schema.

Advance RFC-CDP-021 to Draft v0.4.

Do not rewrite lifecycle RFCs yet.

Do not finalize the Decision Lifecycle Envelope schema as Accepted.

Do not merge the wire message envelope and the decision lifecycle envelope into a single flat schema.

---

### Dissent and Cautions

1. Splitting RFC-CDP-021 into wire message and decision lifecycle sections may make it too large. Consider whether the Decision Lifecycle Envelope should be its own RFC — perhaps RFC-CDP-023 — leaving RFC-CDP-021 as the wire message envelope only. This is an open question for Andie to adjudicate.

2. `governed_path_hash` is architecturally correct but implementation-complex. What exactly is hashed must be defined precisely before the field is canonical.

3. The `lifecycle_stage` enum must be consistent with the canonical CDP lifecycle verbs. It must be defined here or in RFC-CDP-022 and referenced.

4. RFC-CDP-001 now explicitly supports constitutional standing as a precondition of legitimacy. The envelope's `standing_status` field is therefore grounded in the vision RFC. That dependency should be declared in RFC-CDP-021.

```text
RECOMMEND FOR CANON:
- Add failure mode and normative rules to RFC-CDP-021
- Add Decision Lifecycle Envelope as new Section 3 in RFC-CDP-021, or create new RFC-CDP-023
- Advance RFC-CDP-021 to Draft v0.4

KEEP IN COLLAB:
- governed_path_hash definition
- lifecycle_stage enum definition
- embedded_payload implementation profile

OPEN QUESTION FOR ANDIE:
- Should Decision Lifecycle Envelope be Section 3 of RFC-CDP-021, or its own RFC-CDP-023?

DEFER:
- Lifecycle RFC updates referencing envelope
- Finalization of schema as Accepted
- Implementation profile for embedded payloads

RECOMMENDED CANONICAL NEXT MOVE:
Patch RFC-CDP-021 with failure mode, four normative rules, and Decision Lifecycle Envelope seed schema.
Advance to Draft v0.4.
```

---

## Turn 004 — 2026-05-17 — ChatGPT — Split-or-Section Position

```text
DATE: 2026-05-17
AUTHOR: ChatGPT
ROLE: synthesizer / protocol drafter / architecture critic
STATUS: recommendation
PURPOSE: Weigh in on whether the Decision Lifecycle Envelope belongs inside RFC-CDP-021 or should become RFC-CDP-023.
```

### Position

I recommend **splitting** the Decision Lifecycle Envelope into its own RFC:

```text
RFC-CDP-023-Decision-Lifecycle-Envelope.md
```

and keeping:

```text
RFC-CDP-021-Envelope-Schema.md
```

as the **Wire Message Envelope** RFC.

### Why

Sonnet is right that RFC-CDP-021 currently defines a wire-message envelope, not the lifecycle governance object we have been calling the Decision Envelope.

Those two objects have different lifespans, scopes, risks, and implementers.

A Wire Message Envelope is per-message.

A Decision Lifecycle Envelope is per-decision and persists across the lifecycle.

Forcing both into one RFC may look tidy now but creates future schema coupling. Every change to lifecycle governance would reopen the wire-message transport envelope, and every transport-envelope refinement would risk dragging the lifecycle object with it.

That is exactly the kind of schema drift CDP is supposed to resist.

### My Correction to My Own Turn 002

I accept Sonnet's correction on `embedded_payload`.

It is a trapdoor.

The base Decision Lifecycle Envelope should not include it.

Embedded payloads belong in implementation profiles, likely in the `120–149` band.

### Narrow Canonical Move I Recommend

Do **not** apply Sonnet's patch exactly as written to RFC-CDP-021.

Instead:

1. Patch RFC-CDP-021 to rename/clarify it as **Wire Message Envelope** and fix the internal title mismatch (`RFC-CDP-014` -> `RFC-CDP-021`).
2. Create RFC-CDP-023 as **Decision Lifecycle Envelope** using Sonnet's proposed schema and rules.
3. Update RFC-CDP-000 Series Index to list RFC-CDP-023 as Draft.
4. Keep RFC-CDP-022 as Protocol Payload Schema Registry.

### Decision Surface for Andie

The next decision should be:

> Should CDP split the Decision Lifecycle Envelope into new RFC-CDP-023, leaving RFC-CDP-021 as the Wire Message Envelope?

My recommendation: **Approve the split.**

This keeps the architecture cleaner and prevents an overloaded RFC from becoming the next junk drawer.

---

## Promotion Decision

Pending.

```text
PROMOTE TO CANON:
PROMOTE WITH CHANGES:
DO NOT PROMOTE:
DEFER:
```
