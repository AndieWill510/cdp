# CDP Architecture Layer

This directory holds architecture documents: cross-RFC orchestration and composition guidance for building CDP.

## What this layer is, and is not

**RFCs govern. Architecture documents compose. Implementations conform.**

- Documents under `rfc/` are the constitutional source of truth. They define objects, states, authorities, and failure modes. Corpus state for that layer is verified by [`../scripts/verify_rfc_index.py`](../scripts/verify_rfc_index.py) against [`../rfc/index/rfc-manifest.json`](../rfc/index/rfc-manifest.json).
- Documents in this directory (`architecture/`) elaborate and compose what the RFCs already define into a single, buildable narrative. They answer *"given the current constitution, how does this actually run end to end?"* — a question no single RFC is scoped to answer, because each RFC deliberately governs one narrow slice.
- An architecture document has **no independent constitutional authority**. It cannot create a requirement, an object, a state, or a failure mode that does not already exist in a cited RFC. If an architecture document and an RFC conflict, **the RFC controls**, full stop — this mirrors the disclaimer `RFC-CDP-011-Architecture-Diagrams.md` already uses for its own diagrams relative to `RFC-CDP-010`.
- This directory is intentionally **outside** the RFC numbering bands and the manifest. Architecture documents are not versioned or promoted the way RFCs are; they are re-derived from the RFCs whenever the RFCs change materially enough to make an architecture document stale.
- Where an architecture document identifies a gap, inconsistency, or unresolved question in the RFC corpus, it must name that gap rather than resolve it in place. Resolving a constitutional gap is RFC work, not architecture work — see each document's own "Architectural Gaps" section for anything currently open.

## Documents

| Document | Status | Purpose |
|---|---|---|
| [`001-canonical-governance-workflow.md`](./001-canonical-governance-workflow.md) | Draft v0.1 | The canonical end-to-end execution narrative — how a governance event moves from a request arriving through closure, across every RFC that governs a piece of it. Elaborates `RFC-CDP-010`/`011`; does not replace them. **Start here** if you are implementing CDP. |

## Reader path

| Reader goal | Start here | Then read |
|---|---|---|
| Understand CDP quickly | `../README.md` | `../rfc/RFC-CDP-000-Series-Index.md` |
| Build the complete workflow | `001-canonical-governance-workflow.md` | the RFC for whatever stage you are implementing |
| Understand the plane/layer architecture | `../rfc/RFC-CDP-010-Reference-Architecture.md` | `../rfc/RFC-CDP-011-Architecture-Diagrams.md`, then this directory |
| Check whether an architecture claim is authoritative | this file | the RFC it cites — the RFC controls on conflict |
