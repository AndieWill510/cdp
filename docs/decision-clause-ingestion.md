# Decision Clause Ingestion for the First CDP Demo

Status: Demo design note  
Scope: First decision-ingestion demo  
Repository: CDP — Constitutional Decision Plane  

---

## 1. Purpose

This document defines a simple ingestion grammar for the first CDP demo that ingests a series of decisions.

The goal is not to replace the CDP Decision Lifecycle Envelope, Wire Message Envelope, governed records, payload registry, or persistence model.

The goal is to provide a small, legible front door through which plain decisions can enter CDP without losing the governance surfaces CDP exists to protect.

A Decision Clause is the minimal grammatical unit CDP can ingest.

A Decision Envelope is the governed lifecycle index CDP uses to evaluate, challenge, legitimate, execute, record, and learn from that clause.

---

## 2. Core idea

A plain decision can be represented as a clause:

```text
Given / Because antecedent,
subject performs predicate on object,
under authority,
with rationale and references.
```

Or more compactly:

```text
Because/Given X, A does B to C under authority D.
```

The initial grammar is based on familiar parts of speech:

| Grammar part | CDP role | Question answered |
|---|---|---|
| Antecedent | condition, trigger, dependency, lineage, or rationale input | What came before or made this decision relevant? |
| Subject | actor or decision-maker | Who or what is acting, proposing, approving, rejecting, or recording? |
| Predicate | governed action | What is being done, proposed, blocked, approved, rejected, or executed? |
| Object | governed target | What is the action about or applied to? |
| Authority | standing / policy basis | Why is this actor allowed to make or propose this move? |
| Rationale | human-readable because-surface | Why does the decision claim to make sense? |
| Result | lifecycle/status surface | Where does this clause place the decision in CDP flow? |

For demo purposes, this grammar should be simple enough to ingest from JSONL, but structured enough to avoid becoming an opaque blob.

---

## 3. Important distinction: antecedent is not always rationale

The word `antecedent` is useful, but it should not collapse several different governance meanings into one untyped field.

An antecedent might be:

| Relation type | Example | Meaning |
|---|---|---|
| `condition` | `identity_verification_status == passed` | A condition that must be true |
| `trigger` | `risk_score > threshold` | A signal that caused review or action |
| `depends_on_decision` | `decision_id == dec-001` | A prior decision this one relies on |
| `depends_on_record` | `record_id == rec-123` | A governed record this clause relies on |
| `precedent` | `precedent_id == prec-045` | A prior governed outcome being reused |
| `rationale_input` | `policy_requirement == minimum_access_controls` | A reason surface, not necessarily a logical condition |
| `lineage` | `parent_decision_id == dec-root` | A causal or ancestry relationship |

Therefore the demo schema should use an array of typed antecedents rather than one untyped `because` field.

---

## 4. Minimal Decision Clause object

```json
{
  "decision_id": "dec-002",
  "clause_schema_version": "0.1",

  "antecedents": [
    {
      "relation_type": "depends_on_decision",
      "key": "decision_id",
      "operator": "equals",
      "value": "dec-001",
      "ref": "dec-001"
    }
  ],

  "subject": {
    "actor_id": "actor-review-board",
    "actor_type": "institution"
  },

  "predicate": {
    "verb": "approve",
    "modality": "may",
    "tense": "past",
    "polarity": "affirmative"
  },

  "object": {
    "object_type": "access_request",
    "object_id": "req-123"
  },

  "rationale": {
    "because": "The request satisfies the minimum access policy.",
    "evidence_refs": ["rec-policy-check-001"]
  },

  "authority": {
    "authority_basis": "policy:access-control:v1",
    "standing_status": "unreviewed"
  },

  "result": {
    "lifecycle_stage": "propose",
    "status": "admitted"
  }
}
```

---

## 5. JSON vs JSONL

Use both, but for different purposes.

Use JSON for one Decision Clause object.

Use JSONL for ingesting a series of decision events or decision clauses.

Example JSONL input:

```jsonl
{"event_type":"decision_clause.ingested","decision_id":"dec-001","subject":{"actor_id":"actor-intake","actor_type":"synthetic"},"predicate":{"verb":"submit","modality":"does","tense":"past","polarity":"affirmative"},"object":{"object_type":"access_request","object_id":"req-123"},"authority":{"authority_basis":"workflow:intake:v1","standing_status":"unreviewed"},"result":{"lifecycle_stage":"nemawashi","status":"formation"}}
{"event_type":"decision_clause.ingested","decision_id":"dec-002","antecedents":[{"relation_type":"depends_on_decision","key":"decision_id","operator":"equals","value":"dec-001","ref":"dec-001"}],"subject":{"actor_id":"actor-review-board","actor_type":"institution"},"predicate":{"verb":"approve","modality":"may","tense":"past","polarity":"affirmative"},"object":{"object_type":"access_request","object_id":"req-123"},"rationale":{"because":"The request satisfies the minimum access policy.","evidence_refs":["rec-policy-check-001"]},"authority":{"authority_basis":"policy:access-control:v1","standing_status":"unreviewed"},"result":{"lifecycle_stage":"propose","status":"admitted"}}
{"event_type":"decision_relation.linked","decision_id":"dec-002","relation_type":"depends_on_decision","related_decision_id":"dec-001"}
```

Each JSONL line should be independently parseable as JSON.

The persisted canonical object should be stored as JSONB or equivalent structured JSON, not as an opaque text CLOB.

---

## 6. What must not become opaque

The first demo may use JSON-first governed records.

However, governance-critical fields must be promoted into queryable columns or enforcement projections.

Do not bury these only inside predicate JSON:

- `decision_id`
- `subject_actor_id`
- `subject_actor_type`
- `predicate_verb`
- `predicate_modality`
- `predicate_polarity`
- `object_type`
- `object_id`
- `authority_basis`
- `standing_status`
- `lifecycle_stage`
- `status`
- `created_at`
- decision dependencies
- governed record references

The predicate can carry rich JSON, but it must not become a junk drawer.

If a field is needed for governance, enforcement, replay, challenge, or audit, it needs a queryable surface.

---

## 7. Recommended MVP persistence shape

### 7.1 `cdp_decision_clause`

Purpose: stores one ingested Decision Clause per row while preserving the original structured clause.

```text
cdp_decision_clause
- id
- decision_id
- clause_schema_version
- subject_actor_id
- subject_actor_type
- predicate_verb
- predicate_modality
- predicate_tense
- predicate_polarity
- object_type
- object_id
- authority_basis
- standing_status
- lifecycle_stage
- status
- clause_json JSONB
- created_at
- updated_at
```

### 7.2 `cdp_decision_relation`

Purpose: stores typed relationships between decisions, records, evidence, precedents, and lineage without burying them in opaque predicate payloads.

```text
cdp_decision_relation
- id
- decision_id
- relation_type
- related_decision_id
- related_record_id
- related_object_type
- related_object_id
- relation_json JSONB
- created_at
```

### 7.3 Why relations get their own table

A series of decisions becomes governable only if its relationships are joinable.

If `dec-002` depends on `dec-001`, that relationship must be available without parsing every full JSON payload.

This allows the demo to show:

- causal chains;
- dependency graphs;
- decision replay;
- challenge of prior assumptions;
- lineage-aware audit;
- later migration into full Decision Lifecycle Envelope references.

---

## 8. Relationship to CDP envelopes

A Decision Clause is not a Wire Message Envelope.

A Decision Clause is not a Decision Lifecycle Envelope.

A Decision Clause is an ingestion-friendly grammatical representation of a decision-like act.

The Wire Message Envelope remains the per-message protocol wrapper.

The Decision Lifecycle Envelope remains the per-decision governed path index.

The Decision Clause should be able to produce or update a Decision Lifecycle Envelope, but it should not pretend to contain the whole lifecycle.

Demo mapping:

| Decision Clause field | Wire / lifecycle surface |
|---|---|
| `decision_id` | `decision_id` |
| `subject.actor_id` | `actor_id`, `created_by`, standing records |
| `subject.actor_type` | `actor_type` |
| `predicate.verb` | protocol act / payload action |
| `object` | governed payload target |
| `antecedents` | lineage, precedent refs, stage refs, relation table |
| `rationale.evidence_refs` | governed record refs / evidence refs |
| `authority` | standing and authority control surface |
| `result.lifecycle_stage` | lifecycle stage |
| `result.status` | envelope status |

---

## 9. Demo behavior

The first demo should be able to ingest a JSONL file and show at least the following:

1. Decision clauses were parsed.
2. Required grammatical fields were validated.
3. Queryable columns were promoted.
4. Clause JSON was preserved.
5. Typed decision relations were extracted.
6. A simple chain of decisions can be reconstructed.
7. A clause can be mapped into a minimal lifecycle envelope surface.
8. The system can distinguish a human-readable rationale from a governed reference.

The demo does not need to fully adjudicate, legitimate, execute, repair, or learn.

The demo only needs to prove that plain decisions can enter CDP without losing the hooks required for those later stages.

---

## 10. Validation rules for v0.1

A Decision Clause is valid for demo ingestion when:

1. `decision_id` is present.
2. `subject.actor_id` is present.
3. `subject.actor_type` is present.
4. `predicate.verb` is present.
5. `object.object_type` and `object.object_id` are present, unless the predicate is explicitly objectless under a known allowed verb.
6. `authority.authority_basis` is present or explicitly marked `unknown`.
7. `authority.standing_status` is present.
8. `result.lifecycle_stage` is present.
9. `result.status` is present.
10. Every antecedent has a `relation_type`.

The parser should reject untyped antecedents.

The parser should accept empty antecedents.

An empty antecedent list means no antecedents were supplied.

An absent antecedent list means the input did not say whether antecedents exist.

That distinction matters.

---

## 11. Example natural-language round trip

Input sentence:

```text
Because the identity check passed, the review board approved access request req-123 under access-control policy v1.
```

Parsed Decision Clause:

```json
{
  "decision_id": "dec-002",
  "clause_schema_version": "0.1",
  "antecedents": [
    {
      "relation_type": "condition",
      "key": "identity_verification_status",
      "operator": "equals",
      "value": "passed",
      "ref": "rec-verification-123"
    }
  ],
  "subject": {
    "actor_id": "actor-review-board",
    "actor_type": "institution"
  },
  "predicate": {
    "verb": "approve",
    "modality": "may",
    "tense": "past",
    "polarity": "affirmative"
  },
  "object": {
    "object_type": "access_request",
    "object_id": "req-123"
  },
  "rationale": {
    "because": "The identity check passed.",
    "evidence_refs": ["rec-verification-123"]
  },
  "authority": {
    "authority_basis": "policy:access-control:v1",
    "standing_status": "unreviewed"
  },
  "result": {
    "lifecycle_stage": "propose",
    "status": "admitted"
  }
}
```

Important: the natural-language sentence is not the governed record.

It is a human-readable surface that helps produce the governed clause.

---

## 12. Non-goals

This document does not define:

- the final CDP canonical schema;
- the full Decision Lifecycle Envelope;
- the Wire Message Envelope;
- the governed record registry;
- full standing and recusal enforcement;
- full appeal or repair handling;
- a natural-language parser architecture;
- a complete ontology of all possible predicates.

Those belong elsewhere.

This document only defines the first-demo ingestion seam.

---

## 13. Design posture

Keep the demo small enough to build.

Keep the grammar legible enough to explain.

Keep the storage queryable enough to govern.

Keep the JSON rich enough to preserve nuance.

Keep the promoted columns strict enough to prevent schema drift.

A Decision Clause is the front door.

CDP is the house.
