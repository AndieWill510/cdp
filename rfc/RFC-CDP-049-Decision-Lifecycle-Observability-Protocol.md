# RFC-CDP-049 — Decision Lifecycle Observability Protocol

Author: Kevin “Andie” Williams / AIITL contribution  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: May 15, 2026  
Depends On: RFC-CDP-001, RFC-CDP-010, RFC-CDP-020, RFC-CDP-021, RFC-CDP-040, RFC-CDP-041, RFC-CDP-042, RFC-CDP-043, RFC-CDP-044, RFC-CDP-045, RFC-CDP-046, RFC-CDP-047, RFC-CDP-048  
Updates: RFC-CDP-040, RFC-CDP-041, RFC-CDP-042, RFC-CDP-043, RFC-CDP-044, RFC-CDP-045, RFC-CDP-046, RFC-CDP-047, RFC-CDP-048

---

## Abstract

This RFC defines the **Decision Lifecycle Observability Protocol** for the Constitutional Decision Plane (CDP).

The CDP decision lifecycle spans Nemawashi, Propose, Challenge, Test, Adjudicate, Legitimize, Execute, Record, and Learn. These steps define a constitutional flow for decisions, but the flow itself must be observable. A decision can be procedurally valid in theory while becoming stuck, bypassed, orphaned, overloaded, stale, or invisible in practice.

This RFC defines how CDP implementations observe the main decision lifecycle as a governed flow. It specifies lifecycle states, transition visibility, stuck-state detection, bypass detection, ownership, aging, bottlenecks, alerts, graph-aware dependency questions, and learning closure for decision-flow operations.

The core principle is:

> The decision lifecycle must be observable as constitutional flow, not merely stored as lifecycle state.

---

## 1. Purpose

This RFC answers:

- how CDP operators know where a decision is in the lifecycle;
- how decisions stuck in Nemawashi, Propose, Challenge, Test, Adjudicate, Legitimize, Execute, Record, or Learn are detected;
- how required lifecycle steps are monitored for bypass, delay, rework, and closure;
- how workflow state differs from constitutional progress;
- how owners, dependencies, blockers, and next actions are represented;
- how the lifecycle can be visualized as traffic rather than static records;
- how lifecycle observability protects legitimacy, not merely efficiency;
- how lifecycle bottlenecks feed Record and Learn.

---

## 2. Core Principle

A decision lifecycle that cannot be observed cannot be governed.

It is not enough for CDP to define proper stages. CDP must show whether decisions are actually moving through those stages, where they are stuck, what they are waiting on, whether required steps were skipped, and whether learning has closed the loop.

CDP MUST therefore distinguish:

- lifecycle definition from lifecycle execution;
- lifecycle state from lifecycle progress;
- stored transition from visible transition;
- completed step from adequate step;
- delay from deliberation;
- rework from circularity;
- queue from limbo;
- bypass from legitimate exception;
- execution from closure;
- record from learning.

A constitutional flow must be visible enough to challenge.

---

## 3. Relationship to Existing RFCs

### 3.1 RFC-CDP-040 Nemawashi Protocol

Nemawashi prepares decision context, alignment, stakeholder awareness, and pre-proposal sensemaking.

This RFC defines how Nemawashi activity becomes visible enough to prevent informal alignment from becoming hidden governance.

### 3.2 RFC-CDP-041 Propose Protocol

Propose creates a decision candidate.

This RFC defines how proposals are tracked from creation through challenge, test, adjudication, legitimation, execution, record, and learn.

### 3.3 RFC-CDP-042 Challenge Protocol

Challenge introduces contestability.

This RFC defines how open challenges are monitored for ownership, aging, dependency, adjudication readiness, and closure.

### 3.4 RFC-CDP-043 Test Protocol

Test evaluates assumptions, claims, risks, evidence, or expected outcomes.

This RFC defines visibility into required tests, pending tests, failed tests, bypassed tests, and test results awaiting adjudication.

### 3.5 RFC-CDP-044 Adjudicate Protocol

Adjudicate resolves conflicts, challenges, test results, and competing claims.

This RFC defines how adjudication queues, blockers, age, owner, and decision readiness are observed.

### 3.6 RFC-CDP-045 Legitimize Protocol

Legitimize determines whether a decision is valid, authorized, and ready to proceed.

This RFC defines how legitimacy status is monitored and how stale, skipped, or incomplete legitimation is detected.

### 3.7 RFC-CDP-046 Execute Protocol

Execute carries decisions into action.

This RFC defines how execution readiness, blocked execution, unauthorized execution, and execution-without-record are detected.

### 3.8 RFC-CDP-047 Record Protocol

Record preserves governed acts and artifacts.

This RFC defines how missing, stale, or incomplete records are detected as lifecycle observability defects.

### 3.9 RFC-CDP-048 Learn Protocol

Learn closes the loop between decisions, outcomes, repair, and future improvement.

This RFC defines how learning actions are tracked, aged, closed, and escalated when they remain unresolved.

---

## 4. Terminology

### 4.1 Decision Lifecycle

The **Decision Lifecycle** is the governed flow from Nemawashi through Learn.

Recommended lifecycle sequence:

```text
Nemawashi → Propose → Challenge → Test → Adjudicate → Legitimize → Execute → Record → Learn
```

### 4.2 Lifecycle Observability

**Lifecycle Observability** is the ability to understand the current and historical movement of a decision through the lifecycle, including state, ownership, blockers, dependencies, aging, exceptions, bypasses, and closure.

### 4.3 Lifecycle Node

A **Lifecycle Node** is a decision object, lifecycle step, task, review, challenge, test, adjudication, legitimation, execution, record, or learning action visible in the lifecycle flow.

### 4.4 Lifecycle Edge

A **Lifecycle Edge** is a relationship or transition between Lifecycle Nodes.

Examples include:

- prepares;
- proposes;
- challenges;
- tests;
- adjudicates;
- legitimates;
- executes;
- records;
- learns from;
- blocks;
- depends on;
- supersedes;
- returns to;
- escalates to.

### 4.5 Lifecycle State

A **Lifecycle State** is the current process state of a decision or lifecycle node.

### 4.6 Lifecycle Progress

**Lifecycle Progress** is the meaningful movement of a decision toward legitimate closure.

A state change does not always indicate progress. A decision may move between states while remaining unresolved, looping, or procedurally hollow.

### 4.7 Stuck Decision

A **Stuck Decision** is a decision that remains in a non-terminal lifecycle state beyond an expected threshold, lacks ownership, lacks required context, lacks required authority, lacks required next action, or cannot progress without explicit intervention.

### 4.8 Bypassed Step

A **Bypassed Step** is a lifecycle step skipped without recorded authority, exception, or justification.

Bypass may be legitimate in low-impact or emergency contexts, but the bypass itself SHOULD be visible and reviewable.

### 4.9 Lifecycle Control View

A **Lifecycle Control View** is a visual or analytic surface that presents decision lifecycle traffic, queues, states, blockers, transitions, aging, and risk.

Lifecycle Control Views are Human-Readable Surfaces and SHOULD comply with RFC-CDP-063 when applicable.

### 4.10 Lifecycle Closure

**Lifecycle Closure** is the condition in which a decision has reached an appropriate terminal state and required recording, learning, repair, or appeal obligations are either completed, waived, deferred, or explicitly transferred.

---

## 5. Protocol Overview

The Decision Lifecycle Observability Protocol follows this sequence:

```text
Lifecycle Event
  → State / Transition Record
  → Owner and Dependency Update
  → Aging and Bypass Check
  → Stuck-State / Bottleneck Detection
  → Lifecycle Control View
  → Alert / Challenge / Escalation
  → Record / Learn
```

A CDP implementation MAY store lifecycle state in a relational database, event store, document store, graph database, or hybrid system.

The protocol does not require a graph database.

The protocol DOES require graph-aware lifecycle questions to be answerable.

---

## 6. Required Lifecycle Observability Questions

A CDP implementation SHOULD answer, at minimum:

- What decisions are in Nemawashi?
- What Nemawashi items have not produced proposals?
- What proposals are open?
- What proposals have no challenge window?
- What challenges are open?
- What challenges are unassigned?
- What challenges are overdue for adjudication?
- What tests are required?
- What tests are pending?
- What tests failed but have not been adjudicated?
- What decisions are waiting for adjudication?
- What adjudications are overdue?
- What decisions are waiting for legitimation?
- What legitimations are stale or incomplete?
- What executions are blocked?
- What executions occurred without required legitimation?
- What executions occurred without a record?
- What decisions were recorded but never learned from?
- What learning actions are open?
- What decisions are looping between states?
- What steps were bypassed?
- What exceptions were recorded?
- What decisions have no owner?
- What decisions have no next action?
- What decisions are approaching deadline or harm threshold?

---

## 7. Lifecycle State Model

A CDP implementation SHOULD normalize lifecycle states across the main decision flow.

Recommended states include:

- `nemawashi_active`;
- `nemawashi_complete`;
- `proposal_draft`;
- `proposal_submitted`;
- `challenge_window_open`;
- `challenge_pending`;
- `test_required`;
- `test_in_progress`;
- `test_complete`;
- `adjudication_required`;
- `adjudication_in_progress`;
- `adjudicated`;
- `legitimation_required`;
- `legitimation_in_progress`;
- `legitimated`;
- `execution_ready`;
- `execution_blocked`;
- `executed`;
- `record_required`;
- `recorded`;
- `learning_required`;
- `learning_in_progress`;
- `learned`;
- `deferred`;
- `rejected`;
- `superseded`;
- `closed`;
- `reopened`.

Lifecycle states SHOULD be accompanied by owner, timestamp, next action, and blocker information.

---

## 8. Lifecycle Node Requirements

A Lifecycle Node SHOULD include:

- node identifier;
- decision identifier;
- lifecycle step;
- lifecycle state;
- owner;
- accountable role;
- created timestamp;
- updated timestamp;
- expected completion threshold;
- priority or impact level;
- authority requirements;
- evidence requirements;
- current blockers;
- required next action;
- dependencies;
- downstream dependents;
- exception status;
- challenge status;
- adjudication status;
- legitimation status;
- execution status;
- record status;
- learning status.

A non-terminal Lifecycle Node with no owner SHOULD be treated as a lifecycle observability defect.

---

## 9. Lifecycle Edge Requirements

Lifecycle Edges SHOULD preserve how work moves and depends across the lifecycle.

Recommended edge types include:

- `prepared_by`;
- `proposed_by`;
- `challenged_by`;
- `tested_by`;
- `adjudicated_by`;
- `legitimated_by`;
- `executed_by`;
- `recorded_by`;
- `learned_by`;
- `blocked_by`;
- `depends_on`;
- `returns_to`;
- `supersedes`;
- `bypasses`;
- `escalates_to`;
- `reopens`;
- `closes`.

Lifecycle Edges SHOULD support traversal from any decision to its current blockers, past transitions, bypasses, and downstream obligations.

---

## 10. Stuck-State Detection

A CDP implementation SHOULD detect stuck decisions.

Stuck-state signals include:

- Nemawashi remains active without proposal decision;
- proposal remains draft past threshold;
- proposal has no owner;
- challenge window remains open indefinitely;
- challenge remains unassigned;
- test required but not started;
- test complete but not adjudicated;
- adjudication required but not scheduled;
- adjudication in progress past threshold;
- legitimation required but not performed;
- legitimation becomes stale before execution;
- execution ready but blocked without reason;
- execution performed but record missing;
- record created but learning action missing;
- learning action remains open past threshold;
- decision repeatedly returns to the same prior state;
- decision has no required next action;
- decision waits on authority with no authority owner;
- decision waits on evidence with no evidence owner.

Stuck-state detection SHOULD produce an observable event and MAY create a challenge or escalation candidate.

---

## 11. Bypass Detection

A CDP implementation SHOULD detect lifecycle bypass.

Bypass signals include:

- proposal skipped before execution;
- challenge window omitted where required;
- test skipped despite requirement;
- adjudication skipped after challenge;
- legitimation skipped before execution;
- execution performed before required authority;
- record omitted after execution;
- learn omitted after outcome;
- emergency exception invoked without recorded basis;
- low-impact shortcut used for high-impact decision.

A bypass MAY be valid if authorized, scoped, and recorded.

An unrecorded bypass SHOULD be treated as a legitimacy risk indicator.

---

## 12. Bottleneck Detection

A CDP implementation SHOULD detect bottlenecks across the lifecycle.

Bottlenecks may occur at:

- Nemawashi intake;
- proposal drafting;
- challenge assignment;
- testing capacity;
- adjudication queue;
- legitimacy review;
- execution gate;
- record finalization;
- learning closure;
- authority approval;
- evidence retrieval;
- human reviewer load;
- AIITL support process.

Bottleneck indicators include:

- rising queue depth;
- rising median age;
- rising tail age;
- repeated rework;
- repeated bypass requests;
- high challenge-to-adjudication delay;
- low learning closure rate;
- recurring missing authority;
- recurring missing evidence;
- high reopen rate;
- repeated failed tests without resolution.

Bottleneck reports SHOULD distinguish operational load from legitimacy failure.

---

## 13. Lifecycle Control Views

A CDP implementation SHOULD provide lifecycle control views.

Useful views include:

- lifecycle traffic map;
- decision kanban by lifecycle state;
- aging heatmap;
- stuck decision list;
- bypass report;
- challenge-to-adjudication queue;
- test completion dashboard;
- legitimation freshness report;
- execution readiness view;
- execution-without-record exception report;
- record-to-learn closure view;
- owner workload view;
- decision dependency graph;
- authority blocker map;
- evidence blocker map;
- high-impact decision watchlist.

Lifecycle Control Views SHOULD be traceable to underlying lifecycle records.

A visualization MUST NOT become an unchallengeable source of truth.

---

## 14. Graph-Aware Lifecycle Analysis

CDP SHOULD support graph-aware lifecycle analysis even when stored in relational tables.

Graph-aware questions include:

- What challenges block this decision?
- What tests depend on this evidence artifact?
- What adjudications depend on this challenge?
- What executions depend on this legitimation?
- What records are missing after execution?
- What learning actions came from this decision class?
- What decisions share the same authority blocker?
- What proposals repeatedly return to Nemawashi?
- What adjudication outcomes lead to repeated rework?
- What high-impact decisions bypassed testing?
- What decisions are downstream of a stale policy version?

Implementations MAY answer these questions through SQL, graph databases, materialized views, event streams, search indexes, or analytics pipelines.

The requirement is lifecycle queryability, not a specific storage engine.

---

## 15. Alerts and Escalation

A CDP implementation SHOULD support alerts for lifecycle observability events.

Alert types include:

- overdue proposal;
- unassigned challenge;
- overdue test;
- overdue adjudication;
- stale legitimation;
- blocked execution;
- execution without record;
- record without learning closure;
- missing owner;
- missing authority;
- missing evidence;
- repeated lifecycle loop;
- unrecorded bypass;
- high-impact decision approaching deadline;
- decision stuck beyond harm threshold.

Alerts SHOULD include:

- decision identifier;
- lifecycle state;
- owner;
- age;
- blocker;
- impact level;
- required next action;
- escalation path;
- supporting links.

Alert fatigue SHOULD be treated as a lifecycle observability defect.

---

## 16. Legitimacy Risk Indicators

Lifecycle observability SHOULD include legitimacy risk indicators.

Examples include:

- prolonged challenge age;
- adjudication backlog for high-impact decisions;
- repeated test bypass;
- execution without fresh legitimation;
- execution without record;
- low learning closure rate;
- decisions reopened after surface publication;
- repeated missing authority;
- repeated missing evidence;
- high bypass rate in a decision class;
- high stuckness in rights-affecting decisions.

Legitimacy risk indicators are signals, not final judgments.

They SHOULD trigger review, not automatic condemnation.

---

## 17. AIITL Role in Lifecycle Observability

AIITL systems MAY assist with lifecycle observability by:

- summarizing decision traffic;
- identifying stuck states;
- detecting bypass patterns;
- explaining dependency chains;
- suggesting escalation paths;
- identifying missing owners;
- identifying missing next actions;
- comparing current lifecycle flow to historical patterns;
- identifying legitimacy risk indicators;
- generating human-readable lifecycle briefings.

AIITL MUST NOT silently convert observability into authority.

AIITL recommendations SHOULD remain reviewable, traceable, and challengeable.

---

## 18. Record Requirements

A CDP implementation SHOULD record:

- lifecycle state changes;
- lifecycle transitions;
- owner assignments;
- blocker declarations;
- dependency changes;
- bypass events;
- exception justifications;
- stuck-state detections;
- bottleneck detections;
- alerts;
- escalations;
- lifecycle control view definitions;
- challenge records arising from observability;
- learning actions arising from observability.

The record MUST preserve enough information for a future reviewer to reconstruct why a decision was considered stuck, bypassed, blocked, escalated, or at legitimacy risk.

---

## 19. Learning Closure

Lifecycle observability SHOULD feed the Learn Protocol when:

- decisions repeatedly get stuck in the same lifecycle step;
- challenges repeatedly age past threshold;
- adjudication queues become persistent bottlenecks;
- legitimation repeatedly goes stale before execution;
- execution repeatedly lacks record closure;
- learning actions repeatedly fail to close;
- bypasses become routine;
- alerts become noisy or ignored;
- graph analysis reveals hidden dependency failure.

Learning closure MAY require:

- lifecycle state model revision;
- protocol revision;
- queue threshold revision;
- authority delegation revision;
- staffing or ownership change;
- test automation;
- adjudication process redesign;
- execution gate revision;
- record automation;
- learning closure enforcement;
- dashboard redesign.

---

## 20. Relationship to RFC-CDP-066

RFC-CDP-049 governs observability for the core decision lifecycle:

```text
Nemawashi → Propose → Challenge → Test → Adjudicate → Legitimize → Execute → Record → Learn
```

RFC-CDP-066 generalizes observability across the broader CDP control tower, including witness records, surface integrity, canonical record adequacy, semantic synthesis, repair, appeals, and cross-workflow control-plane traffic.

In operational terms:

- RFC-CDP-049 is the runway tower for the decision lifecycle.
- RFC-CDP-066 is air traffic control for the whole airport.

Implementations SHOULD allow RFC-CDP-049 lifecycle observability data to feed RFC-CDP-066 Control Tower views.

---

## 21. Security and Safety Considerations

### 21.1 Lifecycle Theater

A decision may appear to move through lifecycle states while failing to satisfy the purpose of those states.

CDP SHOULD distinguish state transitions from constitutional progress.

### 21.2 Hidden Informality

Nemawashi and informal review may become hidden governance if not made visible enough for accountability.

Lifecycle observability SHOULD preserve informal preparation without over-bureaucratizing it.

### 21.3 Delay as Denial

In rights-affecting, safety-sensitive, care-related, or repair-sensitive workflows, prolonged delay may become denial.

Stuckness SHOULD be treated as potential harm where consequence accumulates.

### 21.4 Metric Capture

Teams may optimize lifecycle metrics while undermining legitimacy.

Metrics SHOULD support governance, not replace judgment.

### 21.5 Surveillance Risk

Lifecycle observability may become worker surveillance if misused.

CDP SHOULD monitor process health without reducing humans to throughput metrics.

### 21.6 Automation Bias

AIITL-generated lifecycle summaries may appear authoritative.

Operators SHOULD treat observability outputs as decision support, not final adjudication.

---

## 22. Implementation Notes

A simple implementation MAY begin with:

1. a lifecycle_state field on Decision Objects;
2. lifecycle transition records;
3. owner and next_action fields;
4. created, updated, and due timestamps;
5. stuck-state SQL views;
6. bypass event records;
7. queue depth and aging dashboards;
8. manual escalation for high-impact stuck decisions.

A mature implementation MAY include:

- event-sourced lifecycle history;
- graph projections of decision dependencies;
- lifecycle bottleneck detection;
- AIITL-generated operational summaries;
- legitimacy risk indicators;
- affected-party harm thresholds;
- automated bypass detection;
- lifecycle replay;
- lifecycle simulation;
- control tower integration under RFC-CDP-066.

---

## 23. Non-Goals

This RFC does not require:

- a specific database engine;
- a specific graph database;
- real-time monitoring for every low-impact decision;
- automated escalation for every delay;
- replacing human judgment;
- treating lifecycle metrics as legitimacy;
- exposing sensitive decision details to unauthorized viewers;
- eliminating informal Nemawashi.

This protocol governs observability of the main decision lifecycle. It does not replace Nemawashi, Propose, Challenge, Test, Adjudicate, Legitimize, Execute, Record, Learn, Control Tower observability, Witness Review, Surface Integrity, Adequacy Review, Semantic Review, Appeal, or Repair.

---

## 24. Summary

CDP defines a constitutional decision lifecycle.

But a lifecycle that cannot be observed becomes a maze.

The Decision Lifecycle Observability Protocol requires CDP systems to show where a decision is, where it came from, what it waits on, who owns it, what step was bypassed, what is aging, what is blocked, what is looping, and whether learning has closed.

The decision lifecycle must be observable as constitutional flow, not merely stored as lifecycle state.

That is how CDP prevents legitimate process from becoming invisible delay, silent bypass, or procedural fog.
