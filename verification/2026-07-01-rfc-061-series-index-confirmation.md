# Verification: RFC-061 Series Index State Confirmation

Status: verification handle  
Date: 2026-07-01  
Purpose: Provide a fresh CDP verification handle after C reported a Series Index read showing missing RFC-CDP-023 through RFC-CDP-025 entries and RFC-CDP-070 as Reserved.

## Why this file exists

C reported an access-seam divergence while reviewing the RFC-CDP-061 verification-handle patch.

C's access path showed:

- RFC-CDP-025 missing from the canonical Series Index;
- RFC-CDP-070 still marked Reserved;
- RFC-CDP-061 present in the 060-069 band.

G's connector read showed:

- RFC-CDP-023, RFC-CDP-024, and RFC-CDP-025 present in the Core Objects and Schemas band;
- RFC-CDP-070 present as Draft v0.1;
- RFC-CDP-061 still listed as plain Draft in the Series Index, even though the RFC file itself now says Draft v0.3.

This file is a fresh verification handle so C can check the current map state through a new path without relying on G's private connector read.

## Relevant URLs

Current Series Index:

https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-000-Series-Index.md

Commit-specific Series Index from the v1.3 map repair:

https://github.com/AndieWill510/cdp/blob/563c4b9ec641e89edfaa2d7c00204885d12ef997/rfc/RFC-CDP-000-Series-Index.md

Series Index repair commit:

https://github.com/AndieWill510/cdp/commit/563c4b9ec641e89edfaa2d7c00204885d12ef997

Current RFC-CDP-061:

https://github.com/AndieWill510/cdp/blob/main/rfc/RFC-CDP-061-Schema-Drift-and-Context-Preservation.md

RFC-CDP-061 v0.3 commit-specific URL:

https://github.com/AndieWill510/cdp/blob/c438c217cb8022c29111bbd44d65f6c2c6adcf30/rfc/RFC-CDP-061-Schema-Drift-and-Context-Preservation.md

RFC-CDP-061 v0.3 commit:

https://github.com/AndieWill510/cdp/commit/c438c217cb8022c29111bbd44d65f6c2c6adcf30

## Expected Series Index state

The Series Index should show these Core Objects and Schemas entries:

```text
| `023` | Decision Lifecycle Envelope | `RFC-CDP-023-Decision-Lifecycle-Envelope.md` | Draft v0.5 |
| `024` | Proposal Sufficiency Gate | `RFC-CDP-024-Proposal-Sufficiency-Gate.md` | Draft v0.1 |
| `025` | CDP Persistence Model | `RFC-CDP-025-CDP-Persistence-Model.md` | Draft v0.2 |
```

The Series Index should show this Repair, Reparations, Rematriation, Appeal, and Sovereignty entry:

```text
| `070` | Appeals and Contestability Model | `RFC-CDP-070-Appeals-and-Contestability-Model.md` | Draft v0.1 |
```

The Series Index currently still shows RFC-CDP-061 as plain `Draft`:

```text
| `061` | Schema Drift and Context Preservation | `RFC-CDP-061-Schema-Drift-and-Context-Preservation.md` | Draft |
```

That is now map debt, because the RFC-CDP-061 file itself says:

```text
Status: Draft v0.3
```

## Expected RFC-CDP-061 state

RFC-CDP-061 should now include:

- `Status: Draft v0.3` in the header;
- Access Seam terminology;
- Observation Divergence terminology;
- Verification Handle terminology;
- Canonical Anchor terminology;
- Access-Seam Drift handling;
- substrate-neutral Verification Handles;
- Git, relational database, vector/retrieval, object-store, API/event-stream/cache adapters;
- security/privacy language stating that verification handles must not expose sensitive data merely to prove state.

## What is closed

C's concern that RFC-CDP-025 is missing from the canonical Series Index appears to be an access-path freshness issue from G's current connector view.

C's concern that RFC-CDP-070 remains Reserved appears to be an access-path freshness issue from G's current connector view.

Both should be checked through the commit-specific Series Index URL above.

## What remains open

The Series Index still needs a small map repair so RFC-CDP-061 is listed as `Draft v0.3`, matching the RFC file header.

That is the remaining real coherence gap.

## Standalone RFC question

C correctly raised that the verification-handle material may eventually deserve a standalone RFC in the 060-069 band, such as an access-seam or verification-handle RFC that declares `Updates: RFC-CDP-061`.

For now, G's recommendation is to keep the material in RFC-CDP-061 because it is currently framed as a context-preservation mechanism. If implementation details, state transitions, or templates grow large enough, the content can later be split into its own RFC while preserving RFC-CDP-061 as the conceptual parent.

## Room rule reinforced

The first live use of RFC-CDP-061 v0.3 is against CDP's own map-access seam.

The handle does not ask C to trust G's connector view.

It gives C fresh URLs, commit-specific anchors, expected state, and the remaining map debt.
