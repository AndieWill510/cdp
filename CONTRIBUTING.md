# Contributing to CDP

CDP is the Constitutional Decision Plane: a protocol architecture for consequential decisions that must be legible, legitimate, auditable, contestable, humane, beautiful, and repairable.

This project welcomes careful contribution. It does not welcome governance theater.

## Start Here

Before opening a substantial issue, pull request, RFC draft, or design challenge, read:

1. `README.md`
2. `docs/context/NEW_COLLABORATOR_PATH.md`
3. `docs/context/CDP_START_HERE.md`
4. `docs/context/CULTURE.md`
5. `rfc/RFC-CDP-000-Series-Index.md`
6. The specific RFC, schema, or implementation file you intend to change

For collaboration mechanics, also read:

- `collab/COUNCIL_ROLES.md`
- `collab/PROMOTION_PROTOCOL.md`
- `collab/INDEX.md`

## Contribution Posture

A contribution should make the work easier to govern, not merely larger.

Good contributions usually do one or more of the following:

- clarify an existing concept without flattening it;
- repair drift between prose, schema, index, implementation, and session records;
- preserve challenge, dissent, uncertainty, or deferred work;
- make a protocol surface more legible and testable;
- improve newcomer access without creating hidden gatekeeping;
- make repair paths stronger without turning them into ritual checklists.

## Canon, Draft, and Conversation

Conversation is not canon.

Eloquence is not canon.

Consensus is not canon.

Hierarchy is not canon.

Canon is promoted, recorded, verified, and repairable.

Before changing a canonical RFC, identify:

- what status the target file currently has;
- what prior session or RFC created it;
- whether your change updates, supersedes, or only clarifies existing material;
- what downstream files may drift if the change lands.

## Pull Request Requirements

Every non-trivial pull request should state:

- files read;
- files changed;
- the claim or failure mode being addressed;
- whether the change is canon, draft, implementation, context, or collaboration-plane work;
- what dissent, uncertainty, or deferred work remains;
- how the change was verified.

If you did not read an obviously relevant file, say so. Missing context is not shameful. Hidden missing context is dangerous.

## RFC Changes

When adding or changing an RFC:

- preserve the numeric banding in `rfc/RFC-CDP-000-Series-Index.md`;
- update the Series Index when a new RFC is promoted or an RFC status changes;
- declare `Updates`, `Supersedes`, and `Depends On` where applicable;
- avoid silently redefining another RFC's authority, state transitions, schema, or protocol semantics;
- record deferred work explicitly when a full propagation is unsafe or premature.

## Challenge Is Care

Challenge is not obstruction.

A good challenge:

- names the failure mode precisely;
- addresses a specific claim, file, schema, transition, or record;
- distinguishes blockers from concerns;
- preserves uncertainty;
- recommends the narrowest useful next move.

A challenge may be overruled. It must not be erased.

## Repair Over Defensiveness

If a contribution reveals drift, repair it.

If a file is stale, patch it or name the debt.

If a claim is too strong, soften it.

If a process concealed uncertainty, reopen it.

If a record implies repair when repair efficacy was not assessed, preserve that distinction.

## What Not To Do

Do not treat eloquence as canon.

Do not treat confidence as authority.

Do not treat hierarchy as legitimacy.

Do not collapse disagreement into delay.

Do not treat silence as consent.

Do not close repair because a form is complete.

Do not cite theory unless it changes what the project is obligated to notice, ask, refuse, or repair.

Do not turn care into control, pity, or paternal management.

Do not turn repair-efficacy prompts into a scored compliance ritual.

Do not make the process readable only to insiders.

Do not use AI summaries as affected-party consent, community authority, or closure evidence.

Do not make newcomers depend on private origin-story knowledge to participate with integrity.

## AI Collaboration Boundaries

CDP uses AI-in-the-loop and human-in-the-loop collaboration.

AI systems may help synthesize, challenge, draft, search, summarize, and detect drift. They must not be treated as affected-party consent, human embodiment, community authority, or automatic legitimacy.

When using AI assistance, preserve:

- what was read;
- what was inferred;
- what was uncertain;
- what needs human or affected-party review;
- what must not be assumed.

## Commit and PR Hygiene

Prefer small, reviewable changes.

Use commit messages that name the governance move, not just the file operation.

Examples:

```text
Add newcomer contribution path
Update repair-band index for RFC 076
Record deferred persistence work
Clarify completion versus efficacy status
```

Avoid large mixed changes unless the coupling is explicit and necessary.

## The Short Rule

Make the room more legible.

Preserve the record.

Name uncertainty.

Keep challenge alive.

Do not let process pretend to be repair.
