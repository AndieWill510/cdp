# RFC-CDP-000 — Series Index

Author: Kevin “Andie” Williams  
Status: Draft v1.4  
Series: Constitutional Decision Plane (CDP)  
Date: July 16, 2026

## Abstract

This RFC defines the constitutional map for the CDP RFC corpus: numbering bands, canonical and staging lanes, status taxonomy, promotion rules, and the relationship among human indexes, machine-readable corpus state, and adjudication history.

It is intentionally an **index of indexes**.

Detailed RFC catalogs no longer live here. They live in band indexes under `rfc/index/`. Machine-readable state lives in `rfc/index/rfc-manifest.json`. Detailed adjudication history lives in `rfc/history/RFC-CORPUS-ADJUDICATION-HISTORY.md`.

A constitutional protocol suite must remember its own structure without making one file too large to update safely.

---

## 1. Reader path

| Reader goal | Start here | Then read |
|---|---|---|
| Understand CDP quickly | `README.md` | this RFC |
| Browse the canonical RFC corpus | this RFC | `rfc/index/README.md` |
| Review a specific band | `rfc/index/README.md` | the relevant band index |
| Verify corpus state | `rfc/index/rfc-manifest.json` | `scripts/verify_rfc_index.py` |
| Review promotion history | this RFC | `rfc/history/RFC-CORPUS-ADJUDICATION-HISTORY.md` |
| Join active collaboration | `collab/INDEX.md` | active session files |

The shortest useful route to current RFC state is:

1. this RFC;
2. `rfc/index/README.md`;
3. the relevant band index;
4. the RFC itself.

---

## 2. Source-of-truth architecture

No single file is the sole keeper of corpus truth.

### 2.1 Protocol authority

Canonical RFC files under `rfc/` define protocol behavior.

### 2.2 Constitutional map

This RFC defines corpus organization, numbering, status, and promotion policy.

### 2.3 Human navigation

Band indexes under `rfc/index/` provide concise catalogs by RFC number range.

### 2.4 Machine-readable state

`rfc/index/rfc-manifest.json` records RFC number, title, canonical filename, status/version, and band.

### 2.5 Integrity verification

`scripts/verify_rfc_index.py` checks for duplicate numbers, duplicate filenames, missing canonical files, malformed headers, status drift, incorrect band placement, and omissions from band indexes.

Run:

```text
make verify-rfc-index
```

The full repository verification target includes this check:

```text
make verify
```

### 2.6 Provenance

Detailed promotion and adjudication history lives in:

`rfc/history/RFC-CORPUS-ADJUDICATION-HISTORY.md`

Git history remains the complete source record for earlier forms of this RFC.

---

## 3. Folder policy

The canonical RFC folder is:

```text
rfc/
```

The staging and recovered-draft folder is:

```text
rfcs/
```

### 3.1 Canonical lane

The `rfc/` folder contains promoted, canonical, or intentionally indexed RFCs.

Canonical filenames MUST follow:

```text
RFC-CDP-<NNN>-<Kebab-Case-Title>.md
```

### 3.2 Staging lane

The `rfcs/` folder MAY contain recovered drafts, experimental work, candidate drafts, chat-derived artifacts, and unpromoted material.

Material in `rfcs/` MUST NOT be treated as canonical unless a canonical RFC explicitly incorporates or promotes it.

### 3.3 Promotion rule

When a staged document is promoted:

- it receives a canonical three-digit number;
- it moves or is copied into `rfc/`;
- the staging copy is removed or marked superseded;
- the manifest and relevant band index are updated;
- the adjudication ledger records the promotion;
- the verifier must pass.

---

## 4. Numbering bands

| Range | Band | Purpose |
|---:|---|---|
| `000–009` | Series / Constitutional Frame | index, vision, scope, principles, terminology, doctrine |
| `010–019` | Reference Architecture | architecture, topology, layers, threat model, trust model |
| `020–029` | Core Objects and Schemas | decision objects, envelopes, payload registries, artifact schemas, persistence |
| `030–039` | Trust, Identity, and Authority | identity, attestation, authority, delegation, standing, recusal, participation integrity |
| `040–049` | Lifecycle Protocols | Nemawashi, Propose, Challenge, Test, Adjudicate, Legitimize, Execute, Record, Learn |
| `050–059` | Execution Safety, Rollback, and Remedy | maturity gates, presence, emergency override, rollback, compensation, remedy |
| `060–069` | Covenant and AIITL | covenant protocol, HITL/AIITL, schema drift, consentful collaboration, relational duties |
| `070–079` | Repair, Appeal, and Sovereignty | appeals, repair agendas, anti-erasure, sovereignty, rematriation-capable repair |
| `080–089` | APIs and Transports | governance API, deliberation API, event streams, webhooks, SDK profiles |
| `090–099` | State Machines | governance, execution, repair, and covenant state machines |
| `100–119` | Security, Audit, and Compliance | privacy, evidence handling, retention, audit profiles, compliance mappings |
| `120–149` | Implementation Profiles | local-first, enterprise, public-sector, synthetic-agent, cloud-neutral profiles |
| `150+` | Extensions / Experimental | domain-specific and experimental RFCs |

The active human-readable catalogs are linked from:

`rfc/index/README.md`

---

## 5. Status taxonomy

Each RFC SHOULD declare one base status.

| Status | Meaning |
|---|---|
| `Draft` | Active working document; not yet stable. |
| `Candidate` | Proposed for implementation or review; expected to stabilize soon. |
| `Accepted` | Canonical enough to build against. |
| `Superseded` | Replaced by another RFC. |
| `Deprecated` | Retained for history; should not be used for new work. |
| `Experimental` | Exploratory; may change or be removed. |
| `Informational` | Useful explanatory material; not normative. |
| `Reserved` | Number intentionally held for future work; a file may not yet exist. |

A version qualifier MAY be appended, for example `Draft v0.5`.

The manifest status MUST match the RFC header for non-reserved entries.

---

## 6. Canonical navigation

The canonical corpus is indexed by band rather than duplicated here.

Start at:

- `rfc/index/README.md`

The machine-readable catalog is:

- `rfc/index/rfc-manifest.json`

The current Trust, Identity, and Authority band includes:

- RFC-CDP-033 — Standing and Recusal Model;
- RFC-CDP-034 — Participation Integrity Attestation.

RFC-CDP-034 is canonical in `rfc/`, not peripheral staging material.

---

## 7. Change discipline

A corpus change that creates, promotes, renames, supersedes, reserves, or deprecates an RFC MUST update, as applicable:

1. the RFC file;
2. the machine-readable manifest;
3. the relevant band index;
4. this RFC only when corpus policy or band structure changes;
5. the adjudication history ledger;
6. dependencies and related references in affected RFCs.

The verifier MUST pass before the change is represented as fully indexed.

Do not silently repair the map.

Name:

- what changed;
- what was read;
- what was not read;
- what remains uncertain;
- what verification was performed.

---

## 8. Size and scope boundary

This RFC SHOULD remain a compact constitutional map.

It should not absorb:

- full per-RFC catalogs;
- detailed session narratives;
- implementation schemas;
- active design debates that belong in collaboration records;
- generated dependency graphs;
- migration tables better represented in the manifest or history ledger.

The design target is a document small enough to read and replace safely while remaining complete about corpus policy.

A map that becomes the territory stops being a map.

---

## 9. Current corpus-level questions

The following remain open until separately adjudicated:

- how lifecycle protocols consume Participation Integrity requirements by risk tier;
- whether manifest entries should include full dependency graphs or whether those should be generated from RFC headers;
- whether band indexes should be generated automatically from the manifest;
- how CI should distinguish warnings for newly discovered RFCs from hard failures;
- how implementation profiles translate canonical object schemas into concrete DDL;
- how record-hash requirements propagate across governed records.

These questions do not block the index-of-indexes architecture.

---

## 10. Summary

RFC-CDP-000 is the constitutional index of indexes.

- RFCs define protocol.
- Band indexes help humans navigate.
- The manifest gives machines a stable catalog.
- The verifier detects drift.
- The adjudication ledger and Git history preserve formation and repair.

The corpus is distributed, but reconciled.
