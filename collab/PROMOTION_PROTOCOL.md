# collab/PROMOTION_PROTOCOL — Collaboration-to-Canon Promotion Protocol

Status: Draft v0.1  
Date: 2026-05-27  
Purpose: Define how material moves from collaboration into CDP canon.

## 1. Why This File Exists

The `collab/` folder is a working space.

It is where ideas are tested, challenged, repaired, rejected, deferred, or promoted.

Without a promotion protocol, `collab/` risks becoming a beautiful junk drawer: rich, moving, and impossible to govern.

Failure mode:

> Collaboration artifact drift — when conversation artifacts accumulate without a clear path to canon, rejection, deferral, or repair.

## 2. Canon Rule

Nothing in `collab/` is canonical merely because it exists.

A collaboration artifact becomes canonical only when:

1. a moderator records a decision;
2. the canonical target is named;
3. the promoted text is rewritten or patched into RFC form;
4. unresolved dissent is preserved or explicitly deferred;
5. the relevant RFC or canonical file is updated;
6. the session record notes what was promoted and what was not.

## 3. Promotion Path

Standard path:

```text
conversation
  -> challenge memo
  -> moderator adjudication
  -> decision record
  -> RFC / schema / index patch
  -> verification
  -> session closure
```

## 4. Artifact States

A collaboration artifact SHOULD be marked as one of:

| State | Meaning |
|---|---|
| `draft` | Proposed material not yet adjudicated. |
| `challenged` | Material has received challenge or dissent. |
| `approved` | Moderator approved the move but canon patch may not yet be applied. |
| `promotion-applied` | Canon patch has been applied. |
| `closed-promoted` | Session has been promoted and closed. |
| `closed-deferred` | Intentionally deferred, with reason. |
| `closed-rejected` | Not promoted. |
| `superseded` | Replaced by later work. |

## 5. Required Session Sections

A session file SHOULD include:

```text
SESSION:
DATE_OPENED:
MODERATOR:
STATUS:
CANON_TARGET:
PURPOSE:
```

And, when ready to close:

```text
PROMOTE TO CANON:
PROMOTE WITH CHANGES:
DO NOT PROMOTE:
DEFER:
OPEN QUESTIONS:
COMMIT(S):
```

## 6. Challenge Memo Requirements

A challenge memo SHOULD:

- name the failure mode precisely;
- identify what is strong;
- identify what is fragile;
- distinguish objections from blockers;
- recommend the narrowest canonical next move;
- state what evidence or files were read;
- state any files that were inaccessible;
- avoid flattery as a substitute for review;
- preserve uncertainty rather than collapsing it.

## 7. Moderator Adjudication

The moderator MAY:

- approve;
- approve with changes;
- reject;
- defer;
- request another challenge;
- split one proposed move into multiple sessions;
- promote only part of a memo.

Moderator approval is not itself canon.

Canon changes only when the relevant canonical file is patched and verified.

## 8. Promotion Requirements

A promotion MUST identify:

- file changed;
- RFC or artifact status change;
- commit SHA;
- material promoted;
- material deferred;
- open questions preserved.

A promotion SHOULD update:

- the relevant RFC or canonical artifact;
- the session file;
- `collab/INDEX.md`;
- `rfc/RFC-CDP-000-Series-Index.md` when RFC numbering, status, or corpus map changes.

## 9. Verification Rule

After a promotion patch, the promoter SHOULD fetch or inspect the changed file to verify the committed result.

Do not claim a patch landed merely because an update was attempted.

If the tool path fails, say so.

## 10. Deferral Rule

Deferred work must be named.

A deferral SHOULD include:

- what is deferred;
- why it is deferred;
- what dependency must land first;
- where the deferred item is tracked.

Untracked deferral becomes hidden debt.

## 11. Rejection Rule

Rejected material should remain visible unless removal is required for safety, confidentiality, or legal reasons.

Rejection should explain whether the issue was:

- wrong;
- premature;
- duplicate;
- unsafe;
- out of scope;
- superseded;
- not yet sufficiently formed.

## 12. Relationship to RFC-CDP-000

This file governs collaboration workflow.

`RFC-CDP-000-Series-Index.md` governs the canonical RFC corpus.

When this file and RFC-CDP-000 disagree about canonical RFC state, RFC-CDP-000 controls.

When this file and a session file disagree about session state, the latest verified canonical commit controls.

## 13. Principle

Conversation is not canon.

Eloquence is not canon.

Consensus is not canon.

Hierarchy is not canon.

Canon is promoted, recorded, verified, and repairable.
