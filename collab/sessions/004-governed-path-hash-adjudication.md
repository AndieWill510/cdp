# Session 004 Appendix: Governed Path Hash Adjudication

```text
SESSION: 004-governed-path-hash
DATE: 2026-05-17
AUTHOR: Andie, recorded by ChatGPT
ROLE: moderator / canon promotion recorder
STATUS: adjudicated-and-promoted
CANON_TARGET: RFC-CDP-023-Decision-Lifecycle-Envelope.md
```

## Decision

Approved: patch `RFC-CDP-023-Decision-Lifecycle-Envelope.md` directly with concrete `governed_path_hash` construction.

## Repository State Before Patch

At the time of this adjudication, the committed Session 004 file contained ChatGPT's opening position and a pending Claude / Sonnet challenge prompt.

No Claude / Sonnet Turn 002 had been committed into the repository session file.

## Action Taken

Updated:

```text
rfc/RFC-CDP-023-Decision-Lifecycle-Envelope.md
```

from Draft v0.1 to Draft v0.2.

Added:

- `governed_path_manifest_ref`
- `governed_path_hash_algorithm`
- Governed Path Manifest definition
- `ref_with_record_hash`
- hash construction procedure
- required hash coverage fields
- direct-hash exclusions
- referenced record hash expectations
- canonicalization rules
- supersession and update behavior
- warning that hash integrity is evidence, not legitimacy

Updated:

```text
rfc/RFC-CDP-000-Series-Index.md
```

to Draft v0.6 and marked RFC-CDP-023 as Draft v0.2.

## Promotion Decision

```text
PROMOTE TO CANON:
- RFC-CDP-023 Draft v0.2 governed_path_hash construction
- RFC-CDP-000 Draft v0.6 map update

PROMOTE WITH OPEN QUESTIONS:
- lifecycle-stage enum ownership
- lifecycle protocol enforcement of stage-specific binding
- implementation profiles for embedded or sealed payloads
- shared record hash requirements in CBB or Record Schema RFC

DEFER:
- rewriting lifecycle RFCs
- final schema Candidate status
- implementation-profile work
```
