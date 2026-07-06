# Demo Visualization Outputs

Status: demo planning note v0.1  
Audience: implementers, product demo builders, corporate attorneys, Trust & Safety reviewers  
Related docs:

- `docs/product-demo-scenarios-roadmap.md`
- `docs/self-canonicalizing-ingestion.md`
- `docs/identifier-registry.md`
- `docs/control-plane-as-decision-registry.md`
- `db/ddl/001-decision-registry-kernel.sql`

---

## 1. Core idea

Visualization outputs should be derived artifacts.

They should not be hand-built dashboard art.

Every visualization should come from a stable query or projection, serialized into a small JSON artifact, and then rendered into one or more presentation formats.

```text
CDP projections -> visualization data specs -> rendered outputs
```

The same scenario should be able to produce:

```text
JSON chart specs
Markdown report tables
PNG/SVG static charts
HTML dashboard panels
PowerPoint slide assets
PDF-ready attorney review exhibits
```

without changing the underlying scenario data.

---

## 2. Visualization pipeline

For each scenario, the demo runner should perform this sequence:

```text
1. Load messy source workbook
2. Self-canonicalize rows
3. Validate identifiers/classes/decisions
4. Insert or stage canonical rows
5. Query projections / in-memory equivalents
6. Produce visualization data specs
7. Render selected output formats
8. Package review artifacts
```

The visualization boundary is between steps 5 and 6.

The database or in-memory model answers:

```text
What are the rollups, findings, edges, and review rows?
```

The visualization layer answers:

```text
How should those results be shown to attorneys, safety reviewers, and demo viewers?
```

Keep those separate.

---

## 3. Canonical visualization artifacts

Each scenario should produce a `visualizations/` directory.

Recommended structure:

```text
out/demo/<scenario_slug>/visualizations/
  class_rollup.chart.json
  human_review_burden.chart.json
  permission_source_distribution.chart.json
  governance_findings.summary.json
  parent_child_edges.graph.json
  decision_register.table.json
```

Optional rendered outputs:

```text
out/demo/<scenario_slug>/visualizations/png/
  class_rollup.png
  human_review_burden.png
  permission_source_distribution.png
  parent_child_lineage.png

out/demo/<scenario_slug>/visualizations/svg/
  class_rollup.svg
  human_review_burden.svg
  permission_source_distribution.svg
  parent_child_lineage.svg

out/demo/<scenario_slug>/dashboard.html
out/demo/<scenario_slug>/attorney_review_report.md
out/demo/<scenario_slug>/trust_safety_review_report.md
```

The JSON specs are the durable source of truth for visual output tests.

PNG, SVG, HTML, and slides are render targets.

---

## 4. Visualization types

### 4.1 Decision volume by class

Question:

```text
What kinds of decisions happened?
```

Data source:

```text
cdp_projection.decision_class_rollup
```

Canonical artifact:

```text
class_rollup.chart.json
```

Recommended chart:

```text
bar chart
```

Minimum data:

```json
{
  "chart_type": "bar",
  "title": "Decision volume by class",
  "x_key": "decision_class_id",
  "series": [
    {"data_key": "decision_count", "label": "Decision count"}
  ],
  "data": [
    {"decision_class_id": "claim_approval", "decision_count": 4}
  ]
}
```

---

### 4.2 Human review burden

Question:

```text
Which decision classes required human review?
```

Data source:

```text
cdp_projection.decision_class_rollup
```

Canonical artifact:

```text
human_review_burden.chart.json
```

Recommended chart:

```text
grouped or stacked bar chart
```

Minimum data:

```json
{
  "chart_type": "bar",
  "title": "Human review burden by decision class",
  "x_key": "decision_class_id",
  "series": [
    {"data_key": "decision_count", "label": "All decisions"},
    {"data_key": "human_required_count", "label": "Human review required"}
  ],
  "data": [
    {
      "decision_class_id": "claim_approval",
      "decision_count": 4,
      "human_required_count": 3
    }
  ]
}
```

---

### 4.3 Permission-source distribution

Question:

```text
What allowed these decisions to happen?
```

Data source:

```text
cdp_projection.decision_registry_flat
```

Canonical artifact:

```text
permission_source_distribution.chart.json
```

Recommended chart:

```text
bar chart
```

Minimum data:

```json
{
  "chart_type": "bar",
  "title": "Permission-source distribution",
  "x_key": "permission_source_type",
  "series": [
    {"data_key": "decision_count", "label": "Decision count"}
  ],
  "data": [
    {"permission_source_type": "policy_rule", "decision_count": 7},
    {"permission_source_type": "human_approval", "decision_count": 3}
  ]
}
```

---

### 4.4 Governance findings summary

Question:

```text
Where is governance weak or incomplete?
```

Data sources:

```text
cdp_core.identifier_registry
cdp_projection.decision_registry_flat
cdp_projection.decision_class_rollup
```

Canonical artifact:

```text
governance_findings.summary.json
```

Recommended output:

```text
count cards + findings table
```

Minimum data:

```json
{
  "title": "Governance findings",
  "counts": {
    "missing_identifier_count": 0,
    "mistyped_identifier_count": 0,
    "packed_field_count": 0,
    "unknown_permission_count": 1,
    "deprecated_identifier_count": 0,
    "human_approval_missing_count": 0
  },
  "findings": [
    {
      "severity": "warning",
      "finding_type": "unknown_permission_source",
      "decision_id": "dec_003",
      "message": "Decision used an unknown permission source."
    }
  ]
}
```

---

### 4.5 Parent-child lineage

Question:

```text
Which decisions descended from which prior decisions?
```

Data source:

```text
cdp_projection.decision_parent_child_edges
```

Canonical artifact:

```text
parent_child_edges.graph.json
```

Recommended output:

```text
edge list first, graph render later
```

Minimum data:

```json
{
  "graph_type": "directed_edges",
  "title": "Decision lineage",
  "nodes": [
    {"id": "dec_001", "label": "dec_001", "class_id": "claim_intake"},
    {"id": "dec_003", "label": "dec_003", "class_id": "human_review_escalation"}
  ],
  "edges": [
    {
      "source": "dec_001",
      "target": "dec_003",
      "relation": "escalates_from"
    }
  ]
}
```

Important: lineages should render from atomic IDs and relation types, never from prose.

---

### 4.6 Attorney Decision Register

Question:

```text
Can a reviewer inspect every material decision?
```

Data source:

```text
cdp_projection.decision_registry_flat
```

Canonical artifact:

```text
decision_register.table.json
```

Recommended output:

```text
table / spreadsheet / Markdown / PDF-ready exhibit
```

Minimum data:

```json
{
  "table_name": "Attorney Decision Register",
  "columns": [
    "decision_id",
    "created",
    "decision_class_id",
    "plain_english_decision",
    "permission_source_type",
    "permission_source_id",
    "human_required",
    "human_approver_id",
    "parent_decision_id",
    "parent_relation_type"
  ],
  "rows": []
}
```

---

## 5. Rendering strategy

Use three levels of rendering.

### Level 1: Data specs only

This is the first build target.

For each scenario, generate JSON files under:

```text
out/demo/<scenario_slug>/visualizations/
```

These can be unit tested easily.

No rendering dependencies required.

### Level 2: Markdown reports

Render tables and summary counts into:

```text
attorney_review_report.md
trust_safety_review_report.md
governance_findings.md
```

This is the best near-term demo surface because it is readable in GitHub and easy to diff.

### Level 3: Static visual outputs

Render JSON specs to:

```text
PNG
SVG
HTML
PPTX
PDF
```

These can be added after the data specs are stable.

Do not start with a dashboard framework.

Start with deterministic data specs and Markdown.

---

## 6. Suggested renderer sequence

### First renderer: Markdown

Why:

- no heavy dependencies;
- GitHub-readable;
- easy to review;
- easy to diff;
- good for attorney-facing reports.

### Second renderer: HTML

Why:

- interactive enough for demos;
- can render charts from JSON specs;
- easy to screenshot;
- usable in local browser.

### Third renderer: PNG/SVG

Why:

- useful for reports and slides;
- stable static artifacts;
- good for executive review.

### Fourth renderer: PowerPoint

Why:

- corporate demo distribution;
- sales/product narrative;
- executive readout.

PowerPoint should be a final packaging target, not the canonical visualization source.

---

## 7. Demo runner output contract

A future demo runner should produce:

```text
out/demo/<scenario_slug>/
  canonical_identifier_registry.csv
  canonical_decision_classes.csv
  canonical_decisions.csv
  ingestion_report.json
  governance_findings.md
  attorney_review_report.md
  trust_safety_review_report.md
  visualizations/
    class_rollup.chart.json
    human_review_burden.chart.json
    permission_source_distribution.chart.json
    governance_findings.summary.json
    parent_child_edges.graph.json
    decision_register.table.json
```

Optional rendered files:

```text
  dashboard.html
  visualizations/png/*.png
  visualizations/svg/*.svg
  slides/<scenario_slug>_demo.pptx
```

---

## 8. Unit-test approach

Tests should verify the data specs before testing rendered images.

Recommended tests:

```text
test_class_rollup_chart_spec_matches_expected
test_human_review_burden_chart_spec_matches_expected
test_permission_source_distribution_spec_matches_expected
test_parent_child_graph_spec_matches_expected
test_attorney_decision_register_table_matches_expected
test_governance_findings_summary_matches_expected
```

Later, renderer smoke tests can verify:

```text
Markdown files are created
HTML dashboard is created
PNG files are created
SVG files are created
```

Avoid pixel-perfect image tests unless there is a strong reason.

Test the data specs, not the pixels.

---

## 9. Visualization acceptance criteria

A scenario visualization pass is acceptable when:

1. all visualization JSON specs are generated;
2. every spec is derived from canonical scenario rows or database projections;
3. no chart requires parsing prose;
4. no chart is manually edited;
5. every chart can be regenerated from the same scenario pack;
6. attorney-facing tables include plain-English decision surfaces;
7. safety-facing outputs include findings, escalations, exceptions, and repairs;
8. parent-child lineage uses explicit `parent_decision_id` and `parent_relation_type`;
9. unknown/deprecated identifiers are visible as findings;
10. Markdown reports can be generated without a dashboard framework.

---

## 10. What to build next

After scenario packs exist, build in this order:

1. `scripts/run_demo_scenario.py`
2. in-memory projection helpers for scenario fixtures;
3. JSON visualization-spec generators;
4. Markdown report renderer;
5. expected JSON fixtures for each scenario;
6. unit tests comparing actual specs to expected specs;
7. optional HTML dashboard renderer;
8. optional PNG/SVG renderers;
9. optional PowerPoint packager.

The first useful product slice is not a dashboard.

The first useful product slice is:

```text
scenario workbook -> canonical data -> validated decisions -> JSON visualization specs -> Markdown review packet
```

That gives the demo durable evidence and a reviewable artifact before adding visual polish.

---

## 11. Design rule

Projections are truth.

Visualization specs are contracts.

Rendered charts are outputs.

Do not let a chart become the source of truth.

Do not hand-edit visualization outputs.

Do not parse prose to build charts.

Do not make attorneys clean data before seeing the review packet.
