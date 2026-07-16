# CDP RFC Indexes

This directory is the human navigation layer for the canonical RFC corpus.

The index architecture has three layers:

1. [`../RFC-CDP-000-Series-Index.md`](../RFC-CDP-000-Series-Index.md) — constitutional map, numbering policy, promotion rules, and corpus-level orientation.
2. Band indexes in this directory — concise human-readable catalogs by RFC number range.
3. [`rfc-manifest.json`](./rfc-manifest.json) — machine-readable corpus state verified by [`../../scripts/verify_rfc_index.py`](../../scripts/verify_rfc_index.py).

Detailed adjudication and promotion history lives in:

- [`../history/RFC-CORPUS-ADJUDICATION-HISTORY.md`](../history/RFC-CORPUS-ADJUDICATION-HISTORY.md)

## Band indexes

- [`000–009 — Series and Constitutional Frame`](./000-009-series-and-constitutional-frame.md)
- [`010–019 — Reference Architecture`](./010-019-reference-architecture.md)
- [`020–029 — Core Objects and Schemas`](./020-029-core-objects-and-schemas.md)
- [`030–039 — Trust, Identity, and Authority`](./030-039-trust-identity-and-authority.md)
- [`040–049 — Lifecycle Protocols`](./040-049-lifecycle-protocols.md)
- [`050–059 — Execution Safety, Rollback, and Remedy`](./050-059-execution-safety-and-remedy.md)
- [`060–069 — Covenant and AIITL`](./060-069-covenant-and-aiitl.md)
- [`070–079 — Repair, Appeal, and Sovereignty`](./070-079-repair-appeal-and-sovereignty.md)
- [`080–089 — APIs and Transports`](./080-089-apis-and-transports.md)
- [`090–099 — State Machines`](./090-099-state-machines.md)
- [`100–119 — Security, Audit, and Compliance`](./100-119-security-audit-and-compliance.md)
- [`120–149 — Implementation Profiles`](./120-149-implementation-profiles.md)
- [`150+ — Extensions and Experimental`](./150-plus-extensions.md)

## Source-of-truth rule

No single Markdown file is the sole keeper of corpus state.

- RFC files define protocol behavior.
- RFC-CDP-000 defines corpus policy.
- Band indexes provide navigation.
- The manifest provides machine-readable state.
- The verifier detects drift.
- Git history and the adjudication ledger preserve provenance.
