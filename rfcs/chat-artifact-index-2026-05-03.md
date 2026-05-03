# Chat Artifact Index — Control Plane Markdown Candidates

**Created:** 2026-05-03  
**Source:** ChatGPT file library / session artifact search  
**Purpose:** Identify the most recent control-plane Markdown or Markdown-candidate artifacts recovered from ChatGPT history for possible promotion into the CDP repository.

---

## Summary

Search recovered three unique recent Markdown RFC artifacts and several older `RFC_drafts.txt` bundles that contain earlier control-plane/RFC planning material.

This is not a complete source-of-truth inventory of the repository. It is an index of what was recoverable from ChatGPT/session artifacts at this time.

---

## Most Recent Recovered Control-Plane Markdown Artifacts

### 1. `RFC-CDP-011-Covenant-AIITL.md`

- **Created:** 2026-04-28
- **Status:** Draft 0.1
- **Category:** Standards Track / Constitutional Control Plane
- **Intended path:** `rfcs/RFC-CDP-011-Covenant-AIITL.md`
- **Theme:** Covenant Protocol, AI-in-the-Loop, HITL/AIITL, relational governance, schema drift, repair, anti-colonial governance.
- **Note:** This appears to be the latest recovered full Markdown RFC artifact.

### 2. `RFC-CDP-007A-Decision-Type-Maturity-and-Queued-Execution-Gates.md`

- **Created:** 2026-04-27
- **Status:** Draft
- **Category:** Standards Track
- **Extends:** RFC-CDP-007, RFC-CDP-008, RFC-CDP-009
- **Theme:** Decision-type maturity, queued execution gates, canary deployment for decisions, governed autonomy.
- **Note:** Vendor-neutral durable-queue pattern for human review, challenge, approval, rejection, execution, and dead-letter routing.

### 3. `RFC-CDP-011-Presence-Bound-Execution-Authority.md`

- **Created:** 2026-04-27
- **Status:** Draft 0.1
- **Category:** Standards Track
- **Updates:** RFC-CDP-007, RFC-CDP-008
- **Theme:** Presence grants, ephemeral execution authority, quorum presence, non-replayable authority tokens, separating legitimacy from present authorization.
- **Note:** Filename collides numerically with Covenant AIITL; recommend renumbering one of the two RFC-011 candidates before promotion.

---

## Older Recovered Control-Plane Draft Bundles

### 4. `RFC_drafts.txt` — 2026-03-18 01:08

- **Theme:** Cleaned build order: vision/scope → architecture → protocols → schemas → APIs → state machines.
- **Contains:** RFC-CCP-000 through RFC-CCP-019 planning table and Governance-Aligned Acceleration pattern material.
- **Note:** Text artifact, not a clean standalone Markdown file, but contains core control-plane architecture source material.

### 5. `RFC_drafts.txt` — 2026-03-18 01:02

- **Theme:** Earlier/parallel build-order and canonical message envelope material.
- **Contains:** RFC-CCP-000 through RFC-CCP-019 planning table plus canonical message envelope concepts.
- **Note:** Likely overlaps with the 01:08 artifact; needs deduplication.

### 6. `RFC_drafts.txt` — 2026-03-18 00:41

- **Theme:** RFC build-order material and canonical envelope draft seed.
- **Contains:** RFC-CCP list, execution state machine entry, and initial canonical message envelope field definitions.
- **Note:** Older source bundle; useful for reconstructing early CDP/CCP schema decisions.

---

## Recommended Promotion Actions

1. Promote `RFC-CDP-011-Covenant-AIITL.md` as a first-class RFC.
2. Promote `RFC-CDP-007A-Decision-Type-Maturity-and-Queued-Execution-Gates.md` as an extension RFC.
3. Promote `RFC-CDP-011-Presence-Bound-Execution-Authority.md`, but renumber it before merge to avoid collision with Covenant AIITL.
4. Deduplicate the three `RFC_drafts.txt` bundles.
5. Extract the canonical envelope material from `RFC_drafts.txt` into a clean schema RFC.
6. Preserve the build-order table as `docs/rfc-roadmap.md` or similar.

---

## Caveats

- This index reflects only artifacts visible through ChatGPT file-library search.
- The search did not recover six clean standalone Markdown RFC files.
- Several recovered items are `.txt` source bundles rather than `.md` files.
- Two distinct recovered RFCs currently use `RFC-CDP-011`; renumbering is required before formal publication.
