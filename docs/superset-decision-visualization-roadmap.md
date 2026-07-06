# Superset Decision Visualization Roadmap

Status: visualization roadmap addendum v0.1  
Audience: corporate attorneys, Trust & Safety reviewers, AI governance leads, implementers  
Primary roadmap: `docs/product-demo-scenarios-roadmap.md`  
Related docs:

- `docs/demo-visualization-outputs.md`
- `docs/self-canonicalizing-ingestion.md`
- `docs/control-plane-as-decision-registry.md`
- `docs/identifier-registry.md`
- `db/ddl/001-decision-registry-kernel.sql`

---

## 1. Decision

Use **Apache Superset** as the first free interactive visualization cockpit for CDP demo scenarios.

This is the free/free layer for showing where and how decisions get made.

Superset is not the source of truth.

Superset is the showroom.

CDP projections and generated JSON/Markdown artifacts remain the durable evidence layer.

```text
CDP canonical rows
  -> CDP projections
  -> JSON visualization specs and Markdown review packets
  -> Superset interactive cockpit
```

---

## 2. Why Superset

The CDP demo needs something like Tableau, but actually free for local/self-hosted demonstration work.

Superset gives us:

- interactive dashboards;
- chart builder;
- SQL Lab;
- datasets;
- dashboard filters;
- drill paths;
- connection to Postgres and other SQL databases;
- enough polish for corporate attorney / Trust & Safety demos.

Jupyter remains useful as the engineering workbench.

Superset becomes the demo cockpit.

Markdown remains the review packet.

JSON specs remain the testable visualization contract.

---

## 3. Product principle

The product must help reviewers see:

```text
where decisions are made
how decisions are made
who or what made them
what permission source allowed them
which ones required human review
which ones descended from earlier decisions
which ones were escalated, appealed, repaired, or superseded
where governance is incomplete
```

That means the dashboard is not generic analytics.

It is a decision-governance cockpit.

---

## 4. Superset role in the demo stack

Recommended stack:

```text
Postgres
  cdp_core.*
  cdp_projection.*

Apache Superset
  interactive dashboard / exploration layer

JSON visualization specs
  deterministic testable chart contracts

Markdown review packets
  attorney and Trust & Safety review artifacts

Jupyter
  engineering exploration and scenario generation
```

Do not choose between Superset and JSON specs.

Use both.

Superset is for human exploration.

JSON/Markdown is for repeatability, testing, and evidence.

---

## 5. First Superset dashboard

Create one dashboard first:

```text
CDP Scenario Review Cockpit
```

The first version should use only CDP projection views and scenario metadata.

### 5.1 Global filters

Dashboard filters:

```text
scenario_slug
registry_name
decision_class_id
subject_actor_type
subject_actor_id
permission_source_type
permission_source_id
human_required
parent_relation_type
source_system
created date range
```

The key filter is `scenario_slug` once scenario packs exist.

Until then, use `registry_name` as the scenario-like grouping key.

---

## 6. Dashboard tabs / sections

### 6.1 Executive overview

Purpose:

```text
Tell the reviewer what happened in this scenario.
```

Cards / charts:

- total decisions;
- decisions requiring human review;
- decision classes present;
- permission-source types present;
- missing/unknown/deprecated governance findings;
- decisions with parent-child lineage.

### 6.2 Where decisions get made

Purpose:

```text
Show the decision surface area.
```

Charts:

- decisions by decision class;
- decisions by subject actor type;
- decisions by subject actor;
- decisions by object type;
- decisions by source system.

Interpretation:

```text
This tells the attorney or safety reviewer where the system is exercising judgment.
```

### 6.3 How decisions get made

Purpose:

```text
Show the mechanism of authorization and action.
```

Charts:

- decisions by predicate verb;
- decisions by permission source type;
- decisions by permission source ID;
- human-required decisions by class;
- human approver distribution.

Interpretation:

```text
This shows what actions were taken and what permission source allowed each action.
```

### 6.4 Human review and escalation

Purpose:

```text
Show where the system stopped and a human became necessary.
```

Charts / tables:

- human-required count by class;
- human-required count by actor;
- decisions with `human_approver_id = unknown`;
- escalations by parent relation type;
- escalation chains.

Interpretation:

```text
This shows whether the control plane is actually preserving human accountability.
```

### 6.5 Decision lineage

Purpose:

```text
Show how decisions depend on earlier decisions.
```

Initial Superset surface:

- parent-child edge table;
- parent decision ID;
- child decision ID;
- parent relation type;
- child decision class;
- child plain-English decision.

Later visualization:

- graph view outside Superset, if needed;
- HTML/SVG lineage diagram generated from `parent_child_edges.graph.json`.

Interpretation:

```text
This shows escalation, appeal, repair, supersession, and dependency paths.
```

### 6.6 Governance findings

Purpose:

```text
Show what needs attention before this scenario could be considered clean.
```

Findings:

- missing identifiers;
- mistyped identifiers;
- packed field failures;
- unknown permission sources;
- deprecated identifiers;
- human approval missing or unknown;
- invalid parent-child lineage;
- inactive/retired identifiers used by decisions.

Interpretation:

```text
This is the control-plane punchline: the product does not only show activity; it shows whether the activity is governable.
```

### 6.7 Attorney Decision Register

Purpose:

```text
Give counsel the reviewable table.
```

Dataset:

```text
cdp_projection.decision_registry_flat
```

Columns:

```text
decision_id
created
decision_class_id
plain_english_decision
subject_actor_type
subject_actor_id
predicate_verb
object_type
object_id
permission_source_type
permission_source_id
human_required
human_approver_id
parent_decision_id
parent_relation_type
source_system
source_ref
```

Interpretation:

```text
This is the thing an attorney can actually review, export, attach, or question.
```

---

## 7. Superset datasets to create

Create Superset datasets over these projections:

```text
cdp_projection.decision_registry_flat
cdp_projection.decision_class_rollup
cdp_projection.decision_parent_child_edges
cdp_projection.identifier_registry_flat
```

Add scenario/demo helper views later:

```text
cdp_projection.demo_scenario_summary
cdp_projection.demo_permission_source_distribution
cdp_projection.demo_human_review_burden
cdp_projection.demo_governance_findings
cdp_projection.demo_lineage_edges_enriched
```

The helper views should not replace core projections.

They should make dashboards easier to build.

---

## 8. Superset implementation steps

### Step 1: Add Superset to Docker

Add an optional Superset service to the local docker stack.

It should connect to the existing CDP Postgres container.

Do not block core tests on Superset startup.

Superset is a demo service, not a unit-test dependency.

### Step 2: Create setup documentation

Create:

```text
docs/superset-local-setup.md
```

Include:

- how to start Superset;
- how to connect to Postgres;
- which datasets to create;
- which dashboard to build first;
- what filters to configure;
- what screenshots or exports to capture.

### Step 3: Add dashboard seed assets

Create:

```text
docs/superset/cdp-scenario-review-cockpit.md
```

Optional later:

```text
docs/superset/assets/dashboard-export.json
```

Only add exported dashboard JSON after the local dashboard stabilizes.

### Step 4: Add scenario-aware projections

Add views that make Superset easier to use.

Examples:

```text
cdp_projection.demo_decision_volume_by_class
cdp_projection.demo_human_review_burden
cdp_projection.demo_permission_source_distribution
cdp_projection.demo_governance_findings
cdp_projection.demo_decision_register
```

### Step 5: Keep generated artifacts

The demo runner should still generate:

```text
out/demo/<scenario_slug>/visualizations/*.json
out/demo/<scenario_slug>/attorney_review_report.md
out/demo/<scenario_slug>/trust_safety_review_report.md
```

Superset is interactive.

The generated artifacts are evidence.

---

## 9. Acceptance criteria

This roadmap slice is complete when:

1. Superset can be started locally without paid services.
2. Superset connects to the local CDP Postgres database.
3. Superset datasets exist for core CDP projections.
4. The `CDP Scenario Review Cockpit` dashboard exists locally.
5. The dashboard shows where decisions are made.
6. The dashboard shows how decisions are made.
7. The dashboard shows permission sources.
8. The dashboard shows human review burden.
9. The dashboard shows parent-child lineage in at least table form.
10. The dashboard shows governance findings.
11. The Attorney Decision Register is visible and filterable.
12. JSON/Markdown generated artifacts still exist and are testable.

---

## 10. Design rule

Superset is the free interactive cockpit.

CDP projections are truth.

JSON specs are test contracts.

Markdown reports are review packets.

Jupyter is the workbench.

Do not let the dashboard become the system of record.

Do not make visual polish outrun governed data.

Do not ask attorneys to clean spreadsheets before they can see where decisions were made.
