# RFC-CDP-066 — Control Tower and Workflow Observability Protocol

Author: Kevin “Andie” Williams / AIITL contribution  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: May 15, 2026  
Depends On: RFC-CDP-001, RFC-CDP-010, RFC-CDP-020, RFC-CDP-021, RFC-CDP-040, RFC-CDP-041, RFC-CDP-042, RFC-CDP-043, RFC-CDP-044, RFC-CDP-045, RFC-CDP-046, RFC-CDP-047, RFC-CDP-048, RFC-CDP-060, RFC-CDP-061, RFC-CDP-062, RFC-CDP-063, RFC-CDP-064, RFC-CDP-065  
Updates: RFC-CDP-010, RFC-CDP-047, RFC-CDP-048, RFC-CDP-061, RFC-CDP-062, RFC-CDP-063, RFC-CDP-064, RFC-CDP-065

---

## Abstract

This RFC defines the **Control Tower and Workflow Observability Protocol** for the Constitutional Decision Plane (CDP).

CDP introduces governed workflows for proposals, challenges, tests, adjudications, legitimations, executions, records, learning, witness review, surface integrity, canonical record adequacy, semantic synthesis, appeals, and repair. These workflows may be valid in isolation but overwhelming in operation without visual analytics, graph awareness, queue visibility, bottleneck detection, and stuck-flow monitoring.

This RFC defines a control-tower layer for CDP: a visual and operational observability plane that helps humans and AIITL systems understand what is happening, where work is stuck, what is blocked, what is aging, what is looping, what lacks authority, what lacks witness testimony, what lacks adjudication, what lacks repair, and what is at risk of silent legitimacy failure.

The core principle is:

> A governed workflow that cannot be observed will eventually become an ungoverned workflow.

The protocol does not require a graph database, but it requires graph-aware representations of workflow state, dependencies, queues, transitions, blockers, and human accountability.

---

## 1. Purpose

This RFC answers:

- how CDP operators know what is happening across the control plane;
- how stuck decisions, challenges, adjudications, witnesses, surfaces, repairs, and executions are detected;
- how visual analytics support legitimacy rather than merely operational efficiency;
- how workflow states, queues, dependencies, and blockers are represented;
- how graph-style analysis can reveal hidden bottlenecks, loops, orphaned records, or silent drift;
- how AIITL may assist in workflow observability without becoming final authority;
- how operational dashboards, alerts, and visual surfaces remain accountable and challengeable;
- how workflow observability feeds Record, Learn, Repair, and governance improvement.

---

## 2. Core Principle

A valid process can still disappear inside its own machinery.

A decision may be proposed, challenged, witnessed, tested, adjudicated, legitimated, executed, recorded, appealed, repaired, and learned from. But if the control plane cannot show where the decision is, what it depends on, who owns the next action, why it is blocked, how long it has aged, and what legitimacy risk is accumulating, then the governance system becomes operationally illegible.

CDP MUST therefore distinguish:

- process definition from process visibility;
- database state from operational awareness;
- queue depth from legitimacy risk;
- workflow completion from meaningful resolution;
- dashboard display from governed observation;
- stuck work from low-priority work;
- delay from denial;
- review from indefinite limbo;
- visualization from adjudication;
- observability from authority.

A control plane must show its own traffic.

---

## 3. Relationship to Existing RFCs

### 3.1 RFC-CDP-010 Reference Architecture

The Reference Architecture defines CDP as layered governance infrastructure.

This RFC adds an explicit operational observability layer across those governance workflows.

### 3.2 RFC-CDP-020 Decision Object Schema

Decision Objects preserve decision state, authority, lifecycle status, linked artifacts, and metadata.

This RFC defines how Decision Objects participate in visual and graph-aware workflow observability.

### 3.3 RFC-CDP-021 Envelope Schema

Envelopes carry message context, actor, authority, lineage, payload type, attestation, and integrity material.

This RFC defines observability expectations for envelope lineage, routing, blocking, and dependency relationships.

### 3.4 RFC-CDP-040 through RFC-CDP-048 Lifecycle Protocols

The lifecycle protocols define Nemawashi, Propose, Challenge, Test, Adjudicate, Legitimize, Execute, Record, and Learn.

This RFC defines how operators observe work moving across those protocols and detect when work is stalled, looping, or improperly bypassing required steps.

### 3.5 RFC-CDP-061 Schema Drift and Context Preservation

Workflow observability SHOULD surface schema drift signals when objects accumulate mismatched states, missing context, stale authority, or incompatible interpretations.

### 3.6 RFC-CDP-062 Interpretive Witness and Synoptic Review Protocol

Witness Records may be pending, missing, divergent, insufficient, or blocked.

This RFC defines how witness workflow state becomes visible.

### 3.7 RFC-CDP-063 Human-Readable Surface Integrity Protocol

Human-readable surfaces may be draft, under review, challenged, published, superseded, repaired, or retracted.

This RFC defines how surface lifecycle state appears in the control tower.

### 3.8 RFC-CDP-064 Canonical Record Adequacy Protocol

Adequacy reviews may block downstream witness, surface, adjudication, execution, or repair.

This RFC defines how adequacy blockers are visualized and monitored.

### 3.9 RFC-CDP-065 Semantic Layer and Meta-Review Protocol

Semantic synthesis may reveal corpus-level patterns, bottlenecks, recurring drift, or repeated stuck states.

This RFC defines how semantic and operational observability feed each other.

---

## 4. Terminology

### 4.1 Control Tower

A **Control Tower** is the operational observability layer that presents the state, flow, dependencies, queues, blockers, aging, risk, and ownership of CDP-governed work.

A Control Tower is not merely a dashboard. It is a governed situational-awareness surface for decision legitimacy.

### 4.2 Workflow Observability

**Workflow Observability** is the ability to understand the current and historical state of CDP workflows, including where work is, where it came from, what it depends on, who owns it, what is blocked, what is aging, and what legitimacy risks are accumulating.

### 4.3 Workflow Node

A **Workflow Node** is a governed object or process unit visible in the Control Tower.

Examples include:

- Decision Object;
- Proposal;
- Challenge;
- Test;
- Adjudication;
- Legitimation;
- Execution request;
- Record action;
- Learn action;
- Witness Record;
- Surface Integrity Review;
- Adequacy Review;
- Semantic Synthesis;
- Appeal;
- Repair action;
- authority grant;
- evidence artifact;
- human task;
- AIITL task.

### 4.4 Workflow Edge

A **Workflow Edge** is a relationship between Workflow Nodes.

Examples include:

- depends on;
- blocks;
- updates;
- supersedes;
- challenges;
- adjudicates;
- legitimates;
- executes;
- records;
- repairs;
- witnesses;
- grounds;
- derives from;
- routes to;
- owns;
- waits for.

### 4.5 Stuck State

A **Stuck State** occurs when a Workflow Node remains in a non-terminal state beyond expected time, lacks an owner, lacks a required dependency, loops repeatedly, waits on unavailable context, or cannot progress without explicit challenge, adjudication, repair, or human intervention.

### 4.6 Bottleneck

A **Bottleneck** is a recurring concentration of pending, blocked, aging, or failed workflow items at a node, role, protocol step, queue, dependency, or authority boundary.

### 4.7 Work-in-Progress Inventory

**Work-in-Progress Inventory** is the current set of non-terminal CDP objects, tasks, queues, and reviews requiring action, monitoring, expiry, adjudication, or repair.

### 4.8 Legitimacy Risk Indicator

A **Legitimacy Risk Indicator** is a signal that delay, missing context, blocked authority, unresolved divergence, surface defect, record inadequacy, or repair failure may undermine legitimacy.

### 4.9 Traffic Pattern

A **Traffic Pattern** is an observed flow of objects through CDP lifecycle states over time.

Traffic patterns may reveal normal flow, delay, rework, bypass, escalation, oscillation, abandonment, or silent accumulation.

### 4.10 Visual Analytics Surface

A **Visual Analytics Surface** is a human-facing display that represents CDP workflow state, graph relationships, risks, queues, maps, timelines, bottlenecks, or metrics.

Visual Analytics Surfaces are Human-Readable Surfaces and SHOULD conform to RFC-CDP-063.

---

## 5. Protocol Overview

The Control Tower and Workflow Observability Protocol follows this sequence:

```text
Workflow Event / State Change
  → Observability Record
  → Graph / Dependency Update
  → Queue and Aging Update
  → Bottleneck / Stuck-State Detection
  → Visual Analytics Surface
  → Alert / Challenge / Escalation / Repair
  → Record / Learn
```

A CDP implementation MAY store workflow state in a relational control-plane database, event store, document store, graph database, or hybrid architecture.

The protocol does not require a graph database.

The protocol DOES require graph-aware questions to be answerable.

---

## 6. Required Observability Questions

A CDP Control Tower SHOULD answer, at minimum:

- What decisions are currently active?
- What state is each decision in?
- What is waiting for human review?
- What is waiting for AIITL witness work?
- What is waiting for adjudication?
- What is waiting for authority proof?
- What is waiting for evidence?
- What is waiting for record adequacy?
- What is waiting for surface integrity review?
- What is waiting for repair?
- What is blocked?
- What is aging past expected thresholds?
- What has no owner?
- What has no next action?
- What is looping between states?
- What has bypassed required states?
- What was challenged but not adjudicated?
- What was adjudicated but not legitimated?
- What was legitimated but not executed?
- What was executed but not recorded?
- What was recorded but not learned from?
- What was surfaced to humans but later challenged?
- What is accumulating legitimacy risk?

A system that cannot answer these questions is not fully observable.

---

## 7. Workflow State Model

A CDP implementation SHOULD expose workflow states for governed objects.

Recommended generic states include:

- `new`;
- `queued`;
- `assigned`;
- `in_progress`;
- `waiting_on_dependency`;
- `waiting_on_human`;
- `waiting_on_aiitl`;
- `waiting_on_authority`;
- `waiting_on_evidence`;
- `waiting_on_adjudication`;
- `waiting_on_repair`;
- `blocked`;
- `challenged`;
- `escalated`;
- `approved`;
- `rejected`;
- `deferred`;
- `executed`;
- `recorded`;
- `learned`;
- `repaired`;
- `superseded`;
- `closed`;
- `archived`.

Protocol-specific RFCs MAY define specialized states, but Control Tower views SHOULD normalize them into a common observability model.

---

## 8. Workflow Node Requirements

A Workflow Node SHOULD include:

- node identifier;
- node type;
- associated canonical record;
- lifecycle state;
- owner;
- accountable role;
- created timestamp;
- updated timestamp;
- due timestamp or expected aging threshold;
- priority or impact level;
- risk level;
- current blockers;
- required next action;
- dependencies;
- downstream dependents;
- challenge status;
- adjudication status;
- repair status where applicable;
- links to evidence, Witness Records, surfaces, adequacy reviews, semantic reviews, or repair records.

A Workflow Node with no owner and no terminal state SHOULD be treated as an observability defect.

---

## 9. Workflow Edge Requirements

Workflow Edges SHOULD preserve relationships between nodes.

Recommended edge types include:

- `depends_on`;
- `blocks`;
- `blocked_by`;
- `routes_to`;
- `assigned_to`;
- `owned_by`;
- `challenges`;
- `adjudicates`;
- `legitimates`;
- `executes`;
- `records`;
- `learns_from`;
- `repairs`;
- `supersedes`;
- `derives_from`;
- `grounds`;
- `witnesses`;
- `surfaces`;
- `caveats`;
- `appeals`.

A CDP implementation SHOULD be able to traverse these relationships to identify impact, dependency chains, blocked downstream actions, and orphaned work.

---

## 10. Stuck-State Detection

A CDP implementation SHOULD detect stuck states.

Stuck-state signals include:

- state age exceeds threshold;
- no owner assigned;
- next action missing;
- dependency missing;
- required Witness Record absent;
- required adjudication absent;
- required authority proof absent;
- required evidence absent;
- required adequacy review absent;
- required surface review absent;
- challenge remains unresolved;
- repair action remains unassigned;
- state oscillates repeatedly;
- object returns to the same reviewer repeatedly;
- queue grows without throughput;
- execution completed but record is missing;
- surface published but challenge path missing;
- learning action created but never closed.

Stuck-state detection SHOULD produce an observable event.

For high-impact decisions, stuck-state detection MAY create a challenge, escalation, or repair candidate.

---

## 11. Bottleneck Detection

A CDP implementation SHOULD detect bottlenecks across workflows.

Bottlenecks may occur at:

- a protocol step;
- an adjudication queue;
- a human reviewer;
- an AIITL witness process;
- an authority approval role;
- evidence retrieval;
- adequacy review;
- surface integrity review;
- repair review;
- execution gate;
- record finalization;
- learning closure.

Bottleneck indicators include:

- growing queue depth;
- rising median age;
- rising tail age;
- repeated rework;
- high challenge rate;
- low adjudication throughput;
- frequent missing authority;
- frequent missing evidence;
- repeated record inadequacy;
- repeated surface defects;
- repair backlog;
- abandoned learning actions.

Bottleneck reports SHOULD distinguish operational delay from legitimacy risk.

---

## 12. Visual Analytics Requirements

A CDP Control Tower SHOULD provide Visual Analytics Surfaces appropriate to operator needs.

Useful views include:

- lifecycle kanban;
- queue depth by protocol step;
- aging heatmap;
- stuck item list;
- dependency graph;
- decision lineage graph;
- challenge/adjudication map;
- witness divergence map;
- surface defect dashboard;
- adequacy blocker dashboard;
- semantic drift trend view;
- repair backlog view;
- authority bottleneck map;
- execution gate view;
- record/learn closure view;
- SLA or threshold breach view;
- role ownership view;
- affected-party impact queue.

A Visual Analytics Surface SHOULD remain traceable to underlying records.

A visualization MUST NOT become an unchallengeable source of truth.

---

## 13. Graph-Aware Analysis

CDP SHOULD support graph-aware analysis even when stored in a relational database.

Graph-aware questions include:

- What downstream actions are blocked by this challenge?
- What decisions depend on this authority grant?
- What surfaces were generated from this inadequate record?
- What witnesses disagree on this policy basis?
- What execution requests bypassed adjudication?
- What repairs relate to this decision class?
- What records share the same stale policy version?
- What bottleneck is common across these delayed cases?
- What human reviewer is overloaded?
- What AIITL witness process repeatedly creates testimony-insufficient outputs?
- What challenge types predict later repair?
- What surface defects correlate with appeals?

Implementations MAY answer these questions through SQL, graph databases, materialized views, search indexes, semantic indexes, or analytics pipelines.

The requirement is queryability, not a specific storage engine.

---

## 14. Alerting and Escalation

A CDP implementation SHOULD support alerts for workflow observability events.

Alert types include:

- stuck decision;
- aging challenge;
- overdue adjudication;
- missing authority;
- missing evidence;
- missing Witness Record;
- missing surface review;
- missing adequacy review;
- execution without record;
- publication without challenge path;
- repair backlog threshold;
- repeated drift pattern;
- owner missing;
- dependency chain blocked;
- high-impact item approaching deadline.

Alerts SHOULD include:

- object identifier;
- state;
- owner;
- age;
- blocker;
- impact level;
- required next action;
- escalation path;
- supporting links.

Alert fatigue SHOULD be treated as an observability defect.

---

## 15. Legitimacy Risk Indicators

CDP observability SHOULD include legitimacy risk indicators, not merely operational metrics.

Examples include:

- unresolved challenge age;
- adjudication backlog for high-impact cases;
- execution actions lacking record closure;
- surfaces published from inadequate records;
- witness divergence unresolved past threshold;
- decisions with stale authority;
- decisions with no affected-party review where required;
- repair actions overdue;
- repeated refusal-to-conclude events;
- repeated semantic drift findings;
- high number of open appeals per decision class;
- high number of surface corrections after publication.

Legitimacy risk indicators SHOULD be interpreted carefully. They are signals, not final judgments.

---

## 16. AIITL Role in Observability

AIITL systems MAY assist with Control Tower observability by:

- summarizing workflow state;
- identifying stuck states;
- detecting bottleneck patterns;
- explaining dependency chains;
- suggesting escalation paths;
- comparing current traffic to historical patterns;
- identifying missing owners;
- identifying missing records;
- detecting surface drift;
- detecting semantic drift;
- generating human-readable operational briefings.

AIITL MUST NOT silently convert observability into authority.

AIITL recommendations SHOULD remain reviewable, traceable, and challengeable.

---

## 17. Control Tower Surface Integrity

Control Tower dashboards and visualizations are Human-Readable Surfaces.

They SHOULD conform to RFC-CDP-063.

A Control Tower surface SHOULD disclose:

- data freshness;
- included workflows;
- excluded workflows;
- filter criteria;
- aggregation logic;
- known gaps;
- confidence limits;
- threshold definitions;
- owner of the visualization;
- how to inspect underlying records;
- how to challenge the visualization.

A dashboard that hides stale data, missing queues, or excluded workflows may create false operational confidence.

---

## 18. Record Requirements

A CDP implementation SHOULD record:

- workflow state changes;
- queue entries;
- owner assignments;
- dependency changes;
- blocker declarations;
- stuck-state detections;
- bottleneck detections;
- alerts;
- escalations;
- visualization snapshots where material;
- dashboard definitions;
- threshold definitions;
- challenge records arising from observability;
- repair or learning actions arising from observability.

The record MUST preserve enough information for a future reviewer to reconstruct why an item was considered stuck, blocked, escalated, or at legitimacy risk.

---

## 19. Learning Closure

Workflow observability SHOULD feed the Learn Protocol when:

- recurring stuck states appear;
- bottlenecks persist;
- adjudication queues age beyond thresholds;
- repairs repeatedly fail to close;
- records are repeatedly inadequate;
- surfaces repeatedly fail review;
- witnesses repeatedly diverge without resolution;
- execution repeatedly waits on the same authority boundary;
- dashboards repeatedly mislead operators;
- alert fatigue prevents response;
- graph analysis reveals hidden dependency failure.

Learning closure MAY require:

- workflow redesign;
- state model revision;
- authority delegation revision;
- staffing or ownership change;
- queue threshold revision;
- dashboard redesign;
- alert tuning;
- schema revision;
- surface protocol revision;
- witness protocol revision;
- execution gate revision;
- repair process revision.

---

## 20. Security and Safety Considerations

### 20.1 Dashboard Theater

A dashboard may create a false sense of control while hiding real blockers or legitimacy risk.

CDP MUST distinguish display from observability.

### 20.2 Metric Capture

Teams may optimize dashboard metrics while neglecting legitimacy, affected-party impact, repair, or truth.

Control Tower metrics SHOULD include qualitative and legitimacy-aware signals.

### 20.3 Hidden Queues

Work may move into unofficial spreadsheets, chats, inboxes, or side processes that the Control Tower cannot see.

Hidden queues are governance risk.

### 20.4 Surveillance Risk

Workflow observability may become worker surveillance if misused.

CDP SHOULD monitor process health without reducing humans to throughput metrics.

### 20.5 Automation Bias

AIITL-generated alerts or summaries may appear authoritative.

Operators SHOULD treat observability outputs as decision support, not final adjudication.

### 20.6 Stuckness as Harm

Delay may become denial.

For rights-affecting, safety-sensitive, care-related, or repair-sensitive workflows, prolonged stuckness SHOULD be treated as potential harm, not merely backlog.

---

## 21. Implementation Notes

A simple implementation MAY begin with:

1. a control-plane database table for workflow nodes;
2. a table for workflow edges or dependencies;
3. normalized lifecycle states;
4. owner and next-action fields;
5. created, updated, and due timestamps;
6. stuck-state SQL views;
7. queue depth and aging dashboards;
8. manual escalation for high-impact stuck items.

A mature implementation MAY include:

- graph database or graph projection;
- event-sourced workflow history;
- materialized observability views;
- visual dependency maps;
- bottleneck detection;
- anomaly detection;
- AIITL operational summaries;
- legitimacy risk scoring;
- affected-party impact queues;
- dashboard challenge workflows;
- repair-linked stuckness monitoring;
- semantic drift analytics.

---

## 22. Non-Goals

This RFC does not require:

- a specific graph database;
- a specific visualization tool;
- real-time monitoring for every low-impact workflow;
- automated escalation for every delay;
- replacing human management;
- reducing legitimacy to metrics;
- exposing sensitive workflow data to unauthorized viewers;
- treating dashboards as final adjudication.

This protocol governs workflow observability. It does not replace Challenge, Adjudicate, Legitimize, Execute, Record, Learn, Witness, Surface Integrity, Adequacy Review, Semantic Review, Appeal, or Repair.

---

## 23. Summary

CDP creates governed workflows.

Governed workflows create traffic.

Traffic creates queues, blockers, aging, loops, hidden dependencies, and legitimacy risk.

Without a Control Tower, CDP may become procedurally correct but operationally blind.

The Control Tower and Workflow Observability Protocol requires CDP systems to show where work is, what it depends on, who owns it, how long it has waited, why it is blocked, what is at risk, and what requires escalation.

The control plane database may store the truth.

But visual analytics make the truth operationally legible.

A graph database is optional.

Graph-aware thinking is not.

A governed workflow that cannot be observed will eventually become an ungoverned workflow.
