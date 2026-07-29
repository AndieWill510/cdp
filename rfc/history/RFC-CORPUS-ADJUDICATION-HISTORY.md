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

## Session 026 answerability convergence

- Two independent efforts corrected the same constitutional root at the same time: the assumption that CDP grants constitutional standing, replaced by the principle that consequence-bearing relationships create answerability, which CDP recognizes and protects.
- One effort integrated the correction directly into RFC-CDP-001 (§5.1 Answerability Before Legitimacy), RFC-CDP-033 (§11, recognition rather than grant, the Answerability Test), and RFC-CDP-045 (§7, the Answerability Gate and constitutional-vs-procedural legitimacy), landing via PR #28.
- A second, unrelated effort landed directly on `main` (commits `8d224fa`, `dec4553`, `703e4dc`) while PR #28 was in progress on a separate branch, proposing the same correction as a standalone `RFC-CDP-003-Answerability-Principle.md` plus a staged amendment package (`rfcs/Answerability-Constitutional-Spine-Amendments.md`) and its planning basis (`rfcs/Answerability-Inquiry-Canonical-RFC-Impact-Assessment.md`).
- This was treated as a governance event, not a fault on either side: the repository briefly held two independently valid proposals for the same constitutional concept.
- Adjudication converged on the PR #28 formulation, which had already been reviewed and refined (recognition-authority requirements, existence contestability, the answerable-to/answerable-for distinction, and the RFC-CDP-045 claim-classification and status-combination redesign). `RFC-CDP-003-Answerability-Principle.md` and the staged amendment package were retired as superseded. The impact-assessment document was archived to `rfc/history/Answerability-Inquiry-Canonical-RFC-Impact-Assessment.md` as a design-history record: its recommended amendment order (RFC-CDP-033, then RFC-CDP-001, then RFC-CDP-045) matched the order the surviving integration actually followed.
- `RFC-CDP-003` was never added to the manifest or a band index, so no promotion bookkeeping needed reversal; band-index status drift for RFC-CDP-001, RFC-CDP-033, and RFC-CDP-045 was corrected in the same pass.
