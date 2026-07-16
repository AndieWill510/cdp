# RFC Corpus Adjudication History

**Status:** active provenance ledger  
**Date:** 2026-07-16

This ledger preserves readable corpus-level adjudication history without forcing the live Series Index to carry the full formation record.

Git history remains the complete source record for prior versions of `RFC-CDP-000-Series-Index.md`.

## Sessions 001–016

- **Session 001:** accepted the RFC Series Index / Map as the first canonical move; left Standing, envelope sequencing, Legitimize precision, Nemawashi governance, and schema-drift mechanisms unresolved.
- **Session 002:** promoted RFC-CDP-033 Standing and Recusal; updated RFC-CDP-001 to support constitutional standing.
- **Session 003:** split wire-message and decision-lifecycle envelope semantics into RFC-CDP-021 and RFC-CDP-023.
- **Session 004:** canonicalized governed-path hashing in RFC-CDP-023.
- **Session 005:** created RFC-CDP-070 Appeals and Contestability; made denial of constitutional standing a Repair-plane breach.
- **Session 006:** added repair controls and closure blocking to RFC-CDP-023.
- **Session 007:** advanced Anti-Premature Certainty and reserved the Proposal Sufficiency Gate.
- **Session 008:** created RFC-CDP-025 Persistence Model.
- **Session 009:** added standing enforcement projection and persistence controls.
- **Session 010:** created RFC-CDP-024 Proposal Sufficiency Gate.
- **Session 011:** defined the APC gate-result payload in RFC-CDP-022.
- **Session 012:** wired proposal-admission artifacts into RFC-CDP-023.
- **Session 013:** wired Propose to Proposal Sufficiency.
- **Session 014:** separated Formation Challenge from ordinary Challenge.
- **Session 015:** wired Legitimize to Proposal Sufficiency and APC evidence.
- **Session 016:** repaired canonical map drift and confirmed band placement.

## July 2026 constitutional reconciliation

- ConstantC and CDP independently converged on distinctions among Standing, Authority, Contestability, epistemic safety, and Sovereignty.
- The reconciliation bridge was recorded at `docs/constantc-cdp-standing-epistemic-safety-bridge.md`.
- RFC-CDP-034 Participation Integrity Attestation was promoted into the canonical `rfc/` lane.
- Participation Integrity was wired into Decision, Test, Adjudicate, Legitimize, Appeals, Record, Learn, and Anti-Erasure surfaces without creating a new lifecycle stage.
- Operational Reachability became one required dimension of Participation Integrity rather than the whole property.
- Sovereignty remained governed by RFC-CDP-032 and RFC-CDP-074 and must not be downgraded to stakeholder participation.

## Index architecture refactor

On 2026-07-16, the RFC map was split into:

- a compact constitutional Series Index;
- human-readable band indexes under `rfc/index/`;
- a machine-readable manifest;
- an automated integrity verifier;
- this dedicated adjudication ledger.

The purpose was to preserve provenance while preventing the navigation surface from becoming too large to update safely.
