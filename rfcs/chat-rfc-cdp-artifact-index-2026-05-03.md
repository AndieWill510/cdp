# Chat RFC-CDP Artifact Index — Latest Recoverable Versions

**Created:** 2026-05-03  
**Repository:** `AndieWill510/cdp`  
**Path:** `rfcs/chat-rfc-cdp-artifact-index-2026-05-03.md`  
**Scope:** Only artifacts with filenames beginning `RFC-CDP-` recovered from ChatGPT/file-library history.

---

## BLUF

A search for the latest 20 recoverable `RFC-CDP-*` artifacts from ChatGPT/file-library history produced **three unique RFC-CDP Markdown files**.

Additional search hits were duplicate chunks of these same files or older `RFC-CCP` / `RFC_drafts.txt` source bundles. Those were intentionally excluded because this index is limited to `RFC-CDP-*` files only.

---

## Latest Unique RFC-CDP Artifacts

### 1. `RFC-CDP-011-Covenant-AIITL.md`

- **Recovered filename:** `RFC-CDP-011-Covenant-AIITL.md`
- **Created:** 2026-04-28T14:54:08Z
- **Status:** Draft 0.1
- **Category:** Standards Track / Constitutional Control Plane
- **Author line:** Andie Williams, with AI-in-the-Loop contribution
- **Intended repository path:** `rfcs/RFC-CDP-011-Covenant-AIITL.md`
- **Depends on:** RFC-CDP-000, RFC-CDP-001, RFC-CDP-003, RFC-CDP-006, RFC-CDP-008, RFC-CDP-009, RFC-CDP-010
- **Summary:** Defines the Covenant Protocol and AI-in-the-Loop (AIITL) as a bounded constitutional role in CDP. Establishes duties of witnessing, truthful speech, gentleness, beauty, schema-drift detection, anti-domination, contestability, and repair.

### 2. `RFC-CDP-007A-Decision-Type-Maturity-and-Queued-Execution-Gates.md`

- **Recovered filename:** `RFC-CDP-007A-Decision-Type-Maturity-and-Queued-Execution-Gates.md`
- **Created:** 2026-04-27T23:11:36Z
- **Status:** Draft
- **Category:** Standards Track
- **Extends:** RFC-CDP-007 Execute Protocol; RFC-CDP-008 Record Protocol; RFC-CDP-009 Learn Protocol
- **Author line:** CDP Project
- **Summary:** Defines Decision-Type Maturity and Queued Execution Gates. Introduces maturity states, first-N review, durable queue routing, graduation/demotion rules, risk-weighted review, and vendor-neutral execution gating for agentic systems.

### 3. `RFC-CDP-011-Presence-Bound-Execution-Authority.md`

- **Recovered filename:** `RFC-CDP-011-Presence-Bound-Execution-Authority.md`
- **Created:** 2026-04-27T23:07:36Z
- **Status:** Draft 0.1
- **Category:** Standards Track
- **Author line:** Andie Williams / CDP Contributors
- **Updates:** RFC-CDP-007 Execute Protocol; RFC-CDP-008 Record Protocol
- **Depends on:** RFC-CDP-001, RFC-CDP-002, RFC-CDP-003, RFC-CDP-004, RFC-CDP-005, RFC-CDP-006, RFC-CDP-008
- **Summary:** Defines Presence-Bound Execution Authority, including Presence Grants, Presence Tokens, quorum presence, execution scope, authority decay, non-replayable execution authority, and emergency override recording.

---

## Duplicate Search Hits Excluded

The following appeared multiple times as search chunks but are not separate versions:

- `RFC-CDP-011-Covenant-AIITL.md`
- `RFC-CDP-007A-Decision-Type-Maturity-and-Queued-Execution-Gates.md`
- `RFC-CDP-011-Presence-Bound-Execution-Authority.md`

These duplicates represent different excerpts from the same underlying files, not distinct file versions.

---

## Non-CDP Artifacts Excluded

The following were deliberately excluded from this RFC-CDP-only index:

- `RFC_drafts.txt` bundles using earlier `RFC-CCP-*` numbering.
- Resume PDFs mentioning CDP.
- CDP graphics, pitch decks, screenshots, and non-Markdown artifacts.
- Any artifact that did not have a recovered filename beginning `RFC-CDP-`.

---

## Numbering Collision

Two recovered artifacts currently claim `RFC-CDP-011`:

1. `RFC-CDP-011-Covenant-AIITL.md`
2. `RFC-CDP-011-Presence-Bound-Execution-Authority.md`

Recommendation: preserve `RFC-CDP-011-Covenant-AIITL.md` as RFC-CDP-011 because it was created later and appears to be the most recent covenant-layer work. Renumber Presence-Bound Execution Authority as `RFC-CDP-012` or another available extension number before promotion.

---

## Recommended Promotion Order

1. Promote `RFC-CDP-011-Covenant-AIITL.md` as the current covenant-layer RFC.
2. Promote `RFC-CDP-007A-Decision-Type-Maturity-and-Queued-Execution-Gates.md` as an extension RFC attached to Execute/Record/Learn.
3. Renumber and promote `RFC-CDP-011-Presence-Bound-Execution-Authority.md` to avoid the `011` collision.
4. Separately mine older `RFC-CCP` draft bundles for conversion into canonical `RFC-CDP-000` through `RFC-CDP-010` files.

---

## Caveat

This index is not a claim that only three RFC-CDP files exist in the GitHub repository. It only records the latest unique `RFC-CDP-*` Markdown artifacts recoverable from ChatGPT/file-library history during this search pass.
