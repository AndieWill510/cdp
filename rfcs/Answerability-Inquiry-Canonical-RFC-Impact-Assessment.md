# Impact of the Answerability Inquiry on Canonical CDP RFCs

**Status:** Working document  
**Authority:** Informational only  
**Repository basis:** Canonical RFC inventory in `rfc/` on `main`  
**Purpose:** Determine which existing RFCs require amendment, clarification, or no immediate change in light of the ConstantC answerability inquiry.

---

## 1. Scope and Method

This assessment is grounded in the canonical `rfc/` directory of `AndieWill510/cdp`, not in remembered numbering or reconstructed titles.

The canonical inventory was inspected first. The following RFCs were then reviewed as the direct constitutional surface of the inquiry:

- RFC-CDP-001 — Vision, Scope, and Principles
- RFC-CDP-002 — Anti-Premature-Certainty Principle
- RFC-CDP-032 — Authority and Delegation Model
- RFC-CDP-033 — Standing and Recusal Model
- RFC-CDP-042 — Challenge Protocol
- RFC-CDP-045 — Legitimize Protocol
- RFC-CDP-070 — Appeals and Contestability Model
- RFC-CDP-074 — Sovereignty Claims and Authority Pluralism

This is a constitutional impact assessment, not a blanket rewrite proposal. It does not amend any RFC.

Assessment categories:

- **No immediate change** — the inquiry does not presently require amendment.
- **Clarification recommended** — mechanics remain intact, but rationale or terminology should be strengthened.
- **Amendment recommended** — the present constitutional formulation should be revised.
- **Further review required** — possible impact exists, but no amendment should be proposed until the canonical text is examined directly.

---

## 2. Findings from the Answerability Inquiry

The inquiry supports the following working conclusions:

1. **Procedure does not create legitimacy by itself.** Procedure may preserve, test, evidence, or operationalize legitimacy, but procedural completion alone is insufficient.
2. **Authority does not legitimate itself.** The capacity to act, delegate, approve, or enforce does not by itself establish a rightful claim to govern.
3. **Consequence-bearing relationships generate claims of answerability.** When an institution, actor, or system materially affects another, the affected party has a claim to demand reasons, contest the act, preserve dissent, and seek repair.
4. **Standing is not merely conferred by the framework.** CDP may recognize and protect standing, but it should not imply that affected-party standing exists only because CDP declares it.
5. **Challenge is a maintenance function of legitimacy.** Challenge does not itself create legitimacy; it prevents legitimacy from becoming insulated from answerability.
6. **Legitimacy must remain answerable after conferral.** Legitimation is not an irreversible ceremonial state. Appeals, affected-party review, authority conflict, repair, and learning may reopen or qualify it.
7. **The descriptive, normative, procedural, and testing layers should remain distinct.** RFCs should not slide from observable conditions to moral obligation without naming the bridge.

These remain working constitutional conclusions until separately adopted through CDP governance.

---

## 3. RFC Impact Assessment

## RFC-CDP-001 — Vision, Scope, and Principles

**Assessment:** Amendment recommended.

RFC-CDP-001 already rejects speed, access, hierarchy, institutional legibility, and procedural appearance as substitutes for legitimacy. It also protects constitutional standing, affected-party claims, contestability, repair, and sovereignty.

The gap is foundational rather than mechanical. The RFC states that constitutional standing is a precondition of legitimacy, but it does not yet explain why affected parties possess that standing beyond CDP's own declaration.

Recommended amendment:

- add answerability as an explicit constitutional principle;
- state that CDP recognizes and protects answerability arising from consequence-bearing relationships;
- distinguish legitimacy from procedural conformance;
- clarify that CDP does not manufacture affected-party claims through institutional recognition;
- add a boundary between descriptive premises, normative commitments, and procedural enforcement.

No lifecycle change is presently recommended.

---

## RFC-CDP-002 — Anti-Premature-Certainty Principle

**Assessment:** Clarification recommended.

RFC-CDP-002 is strongly aligned with the inquiry. It already requires visible uncertainty, alternatives, challenge, stakeholder impact, reversibility, repair paths, and falsifiable tests. It also distinguishes field presence from genuine inquiry.

Recommended clarification:

- identify unanswerable finality as a form of certainty capture;
- state that a procedurally complete decision may still exhibit certainty performance when affected-party questions or normative premises cannot receive a substantive response;
- preserve the current falsifiability and gate mechanics.

No structural amendment is presently required.

---

## RFC-CDP-032 — Authority and Delegation Model

**Assessment:** Clarification recommended.

RFC-CDP-032 already states that authority is not ambient access and that legitimacy does not arise merely because power can act. It distinguishes institutional authority, affected-party authority, and sovereignty authority.

Recommended clarification:

- state expressly that valid authority remains answerable to those materially affected within its scope;
- add answerability failure as a possible authority-decay or suspension condition where policy permits;
- distinguish the source of an authority grant from the continuing legitimacy of its exercise;
- clarify that delegation transfers bounded capacity, not immunity from contestation.

The authority object and delegation mechanics need not change in this pass.

---

## RFC-CDP-033 — Standing and Recusal Model

**Assessment:** Amendment recommended. This is the most direct impact.

Section 11.1 currently resolves the constitutional-root problem by declaring that constitutional standing is granted by the CDP framework, requires no granter, is axiomatic within CDP, and stops the regress there.

That formulation is operationally useful but philosophically incomplete. It risks implying that affected-party standing exists because CDP confers it. The answerability inquiry supports a different relationship:

- consequence-bearing relationships give rise to claims of answerability;
- affected-party standing is CDP's recognition and protection of those claims;
- CDP does not create the underlying affected-party relationship;
- the framework may define procedural scope, stage, evidence, and contestability without claiming authorship of the underlying claim.

Recommended amendment:

- revise Section 11.1 so that constitutional standing is **recognized and protected by CDP**, not ontologically created by it;
- retain the rule that no actor inside the governed system may revoke constitutional standing;
- preserve preliminary standing based on a claim of potential material impact;
- distinguish the underlying standing claim from its procedural expression in CDP;
- preserve recusal, stage specificity, functional standing, and contestability mechanics.

This amendment should be drafted before any downstream RFC changes that depend on RFC-CDP-033's constitutional root.

---

## RFC-CDP-042 — Challenge Protocol

**Assessment:** Clarification recommended.

RFC-CDP-042 already says that challenge is mandatory, silence is not agreement, affected-party challenge standing must be protected, and challenge prevents legitimacy theater.

The inquiry does not require a mechanical change.

Recommended clarification:

- describe Challenge as an institutional answerability mechanism;
- state that challenge preserves the decision's obligation to respond to material reasons, evidence, affected-party claims, and authority disputes;
- avoid implying that the existence of challenge alone makes a decision legitimate.

The current final principle — “Challenge does not create legitimacy. Challenge prevents legitimacy theater.” — should remain.

---

## RFC-CDP-045 — Legitimize Protocol

**Assessment:** Amendment recommended.

RFC-CDP-045 is already careful: it distinguishes integrity, sufficiency, legitimacy, correctness, and hierarchy; requires governed evidence; blocks unresolved challenges and affected-party claims; and denies that hierarchy alone confers legitimacy.

The remaining gap is definitional. Legitimacy is presently defined principally as a valid process performed by actors with valid standing and authority, with required conditions addressed. The answerability inquiry indicates that this is necessary but not sufficient.

Recommended amendment:

- add **answerability** to the Necessary-Not-Sufficient Axiom;
- define answerability as the maintained capacity and obligation to provide reasons, receive contestation, preserve unresolved claims, and enter appeal or repair where required;
- state that procedural validity is necessary but not sufficient for legitimacy;
- add an `answerability_basis_ref` or equivalent only after the concept has a canonical schema and protocol owner;
- clarify that legitimacy may later be qualified, suspended, reopened, or shown defective through appeal, affected-party review, authority conflict, or repair evidence.

No schema field should be added casually. First amend the constitutional definition; then determine whether an implementation field is actually needed.

---

## RFC-CDP-070 — Appeals and Contestability Model

**Assessment:** No immediate change; rationale strengthened.

RFC-CDP-070 already operationalizes continuing answerability. Appeal initiation is a constitutional right of entry, institutional permission is not required, silence does not close an appeal, and unresolved appeal blocks closure.

The inquiry strengthens the explanation for these rules but does not presently require their mechanics to change.

A future editorial revision may state that appeal is not an exception to legitimacy but one of the means by which legitimacy remains answerable after decision and execution.

---

## RFC-CDP-074 — Sovereignty Claims and Authority Pluralism

**Assessment:** No immediate change; strong alignment.

RFC-CDP-074 already rejects institutional legibility as the source of all legitimacy, preserves authority that originates outside the institution, prevents authority downgrading, and blocks illegitimate closure where material authority conflict remains unresolved.

This RFC provides an important limit on any answerability amendment: CDP must not turn answerability into a claim that every authority is answerable exclusively to the institution running CDP. Answerability must remain compatible with authority pluralism, restricted knowledge, delegated scope, and sovereignty.

No immediate amendment is recommended.

---

## 4. Direct Amendment Order

The recommended order is:

1. **RFC-CDP-033** — repair the constitutional root of standing.
2. **RFC-CDP-001** — add answerability to the constitutional frame and distinguish recognition from creation.
3. **RFC-CDP-045** — revise the definition of legitimacy after the foundational terms are settled.
4. **RFC-CDP-032** — clarify continuing answerability of exercised authority.
5. **RFC-CDP-042 and RFC-CDP-002** — make limited rationale clarifications only.

RFC-CDP-070 and RFC-CDP-074 should be used as consistency checks during drafting.

---

## 5. RFCs Requiring Targeted Follow-Up Review

Before amendments are finalized, the following canonical RFCs should be reviewed for dependency effects:

- RFC-CDP-024 — Proposal Sufficiency Gate
- RFC-CDP-044 — Adjudicate Protocol
- RFC-CDP-047 — Record Protocol
- RFC-CDP-048 — Learn Protocol
- RFC-CDP-060 — Covenant Protocol and AIITL
- RFC-CDP-062 — Interpretive Witness and Synoptic Review Protocol
- RFC-CDP-064 — Canonical Record Adequacy Protocol
- RFC-CDP-065 — Semantic Layer and Meta-Review Protocol
- RFC-CDP-073 — Affected-Party Review and Anti-Erasure
- RFC-CDP-076 — Repair Efficacy and Verification
- RFC-CDP-090 — Governance State Machine
- RFC-CDP-092 — Repair State Machine

These are not classified here as requiring amendment. They are listed because they may consume, preserve, test, or operationalize any later canonical definition of answerability.

---

## 6. Questions That Must Remain Open

- What exact normative bridge connects material consequence to an obligation of answerability?
- Is answerability a constitutional primitive, a property of legitimate authority, or both?
- What limits answerability where confidentiality, cultural protocol, safety, or restricted knowledge applies?
- What constitutes a substantive answer rather than procedural acknowledgment?
- When does failure of answerability suspend legitimacy, and when does it instead trigger challenge, appeal, or repair?
- Can an authority remain legitimate while a particular act is unanswerable?
- How should answerability operate across plural or conflicting authority systems?

No RFC should pretend these questions are resolved until the project has actually resolved them.

---

## 7. Current Recommendation

Do not rewrite the lifecycle.

Do not add a new protocol or schema merely because the philosophical vocabulary has improved.

First amend the constitutional root in RFC-CDP-033, then the frame in RFC-CDP-001, and then the definition of legitimacy in RFC-CDP-045. Preserve the existing procedural machinery unless a concrete inconsistency emerges during amendment drafting.

The principal change is not that CDP needs more procedure.

It is that CDP should state more precisely why its existing protections are owed.