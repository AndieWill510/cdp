# Session 002 Appendix: Turn 006 — Constitutional Root Challenge Memo

```text
SESSION: 002-standing-and-recusal
DATE: 2026-05-17
AUTHOR: Claude / Sonnet (claude-sonnet-4-6)
ROLE: challenger / constitutional architect
STATUS: promoted-with-rfc-patch
PURPOSE: Resolve the open constitutional root question in RFC-CDP-033 Section 11. Who grants standing to the standing-granter?
```

## Note

This appendix preserves Turn 006 for Session 002.

The corresponding canonical RFC patch was applied to:

```text
rfc/RFC-CDP-033-Standing-and-Recusal-Model.md
```

The RFC was advanced from Draft v0.1 to Draft v0.2.

---

## The Failure Mode This Section Prevents

The failure mode is **legitimacy by infinite delegation**.

Actor A grants standing to Actor B. Actor B adjudicates. Someone challenges whether Actor A had authority to grant standing. Actor A points to Actor C. Actor C points to Actor D. The chain either loops or disappears into institutional fog.

The result: the governance process appeared legitimate at every visible step, but the root of its authority was circular, unexamined, or laundered through enough layers that no one is accountable for it.

This is the vertical cousin of authority capture.

CDP must resolve the vertical question as clearly as it resolves the horizontal one.

---

## Summary of Constitutional Root Resolution

The answer has three tiers:

1. **Constitutional Standing** — granted by the CDP framework itself as a precondition of legitimate governance.
2. **Delegated Standing** — granted by recognized actors or institutions, traceable to constitutional standing or RFC-CDP-032 authority.
3. **Emergent Standing** — temporary standing arising from emergency, repair, appeal, or other contingent circumstances.

The regress stops at Tier 1.

Constitutional standing requires no granter. It is axiomatic within CDP.

If CDP cannot guarantee standing to affected parties, evidence custodians, and record-keepers, it has no legitimate claim to govern consequential decisions.

---

## Standing Types Preserved from Turn 006

| Standing Type | Granted By |
|---|---|
| Constitutional | CDP framework itself |
| Affected-Party | CDP framework, structurally |
| Evidence-Custodian | CDP framework, functionally |
| Record-Keeper | CDP framework, by role |
| Delegated | Recognized actor or institution |
| Emergency | CDP framework conditionally; requires human authorization |
| Repair | CDP framework upon breach recognition |
| Appeal | CDP framework upon contestation |

---

## Contestability Rule Preserved from Turn 006

Constitutional standing cannot be contested as to existence. Scope and stage may be challenged.

Delegated standing is fully contestable on grounds of invalid authority chain, expired delegation, undisclosed conflict, role incompatibility, or improper recusal determination.

Standing contests must be raised before or during the relevant stage.

Post-execution standing contests belong to the Appeal and Repair planes.

An uncontested standing determination becomes stable for that decision, while remaining subject to appeal.

---

## Applied RFC Patch Summary

`RFC-CDP-033-Standing-and-Recusal-Model.md` was updated to Draft v0.2 with:

- Section 11 replaced by Standing Types and Constitutional Root;
- constitutional standing made axiomatic;
- standing type taxonomy added;
- constitutional standing protection added;
- denial of constitutional standing named as a governance breach;
- contestability boundaries added;
- Repair-plane dependencies added to the RFC header.

Commit message used:

```text
CDP: Turn 006 — constitutional root resolved — RFC-CDP-033 Section 11 patch — Draft v0.2
```

---

## Next Load-Bearing Check

Does `RFC-CDP-001-Vision-Scope-Principles.md` currently support the claim that constitutional standing is axiomatic?

If it does not, the Standing model is floating above a gap in the vision RFC.
