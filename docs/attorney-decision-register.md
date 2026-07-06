# Attorney-Facing Decision Register for Agentic AI

Status: Demo design note  
Scope: Attorney-readable output from an agentic AI decision system  
Audience: Attorneys, compliance reviewers, first-year engineers, product owners  

---

## 1. Purpose

This document defines the simplest useful output an attorney can request from an agentic AI system:

> A Decision Register: one row per material AI decision, recommendation, or action.

The goal is not to expose model internals, hidden reasoning, chain-of-thought, every prompt token, or every intermediate retrieval.

The goal is to produce a practical, reviewable record that a first-year attorney can understand and a first-year engineer can build without needing to understand the full CDP architecture.

---

## 2. Plain-English answer

### Is it reasonable?

Yes, if the attorney is asking for:

> A list of material decisions or actions made, recommended, blocked, or executed by the agentic AI, with enough context to understand what happened, what it affected, what rule or permission allowed it, and where the supporting record lives.

No, if the attorney is asking for:

> Everything the model thought, every hidden inference, every token-level internal state, or a perfect explanation of why a neural model generated a particular sentence.

That is not a reasonable operational output.

### Is it achievable?

Yes, if the system is designed to log decisions at the agent boundary, tool boundary, policy-check boundary, and human-approval boundary.

Maybe, if partial logs already exist.

No, not reliably, if the system was never instrumented and someone is trying to reconstruct decisions after the fact from chat transcripts, application logs, or vibes in a trench coat.

The practical rule:

> Do not ask the AI to remember what it did. Log what the system allowed it to do while it is doing it.

---

## 3. The smallest useful definition of “decision”

For attorney-facing output, a “decision” means any AI-made or AI-recommended event that materially changes, recommends, blocks, permits, denies, records, or escalates something.

A decision is material when it does at least one of these:

1. approves, denies, scores, ranks, flags, blocks, or escalates a person, claim, request, transaction, case, account, payment, service, access right, or workflow step;
2. sends or causes an external communication;
3. writes, updates, deletes, or commits a business record;
4. calls a tool or system that changes state;
5. accesses restricted data or uses a privileged permission;
6. creates an output that a person or system is expected to rely on;
7. bypasses, overrides, or requests an exception to a normal rule;
8. recommends an action that a human later approves, rejects, or modifies.

Not every model response is a material decision.

Not every token is a material decision.

Not every retrieved document is a material decision.

Not every draft sentence is a material decision.

---

## 4. The attorney should ask for this

The attorney-friendly request should be:

> Please produce the Decision Register for this agentic AI system for the relevant time period. For each material AI decision, recommendation, or action, include what was decided, what was affected, when it happened, what rule or permission allowed it, whether a human approved it, what evidence or inputs it relied on, what system action occurred, and where the audit record can be found.

This avoids the trap of asking for metaphysical authority.

It asks for records.

---

## 5. The engineer should produce this

The engineer-friendly output is a CSV, spreadsheet, database view, or API response with one row per material decision.

### Minimal Decision Register columns

| Column | Plain-English meaning | Example |
|---|---|---|
| `decision_id` | Unique ID for this decision row | `dec-2026-000123` |
| `timestamp` | When it happened | `2026-07-06T18:42:11Z` |
| `agent_name` | Which AI/agent made or recommended it | `claims-review-agent` |
| `agent_version` | Which version/config was active | `v0.3.1` |
| `matter_id` | Case, claim, request, ticket, account, or workflow ID | `claim-9981` |
| `decision_type` | Kind of decision | `recommend_approval` |
| `plain_english_decision` | What happened in normal language | `The agent recommended approving the claim.` |
| `affected_object_type` | What kind of thing was affected | `claim` |
| `affected_object_id` | The specific thing affected | `claim-9981` |
| `action_taken` | What the system actually did | `recommendation_created` |
| `final_status` | Proposed, approved, denied, executed, blocked, escalated, etc. | `human_approved` |
| `permission_source_type` | What kind of permission allowed this | `policy_rule` |
| `permission_source_id` | The policy, role, approval, or config ID | `policy-claims-approval-v2` |
| `human_required` | Was a human required before execution? | `yes` |
| `human_approver_id` | Who approved, if applicable | `user-442` |
| `evidence_refs` | IDs/links to evidence or inputs used | `rec-88; rec-91` |
| `policy_refs` | IDs/links to policies or rules applied | `policy-claims-approval-v2` |
| `tool_used` | Tool/API/system used, if any | `claims_api.recommend` |
| `audit_record_ref` | Link or ID to detailed record | `audit-evt-55291` |
| `exception_flag` | Did it require an exception or override? | `no` |
| `notes` | Short human-readable note | `Confidence below auto-execute threshold; routed to human.` |

This is the whole magic trick.

A lawyer can read it.

An engineer can build it.

CDP can govern it.

---

## 6. Avoid the governance nightmare phrase

The phrase “under whose authority” can become a governance nightmare because it mixes legal authority, system permissions, business delegation, identity, role-based access, human approval, and model behavior into one overloaded question.

Use these simpler questions instead:

1. What did the AI decide, recommend, or do?
2. What thing or person did it affect?
3. Was it allowed to do that automatically?
4. If yes, what policy, role, configuration, or prior approval allowed it?
5. If no, who approved it before it took effect?
6. What evidence or inputs did it rely on?
7. Where is the detailed audit record?

For the register, replace “authority” with two simpler fields:

```text
permission_source_type
permission_source_id
```

Then, if needed, add:

```text
human_required
human_approver_id
```

This is less philosophically satisfying but much more reviewable.

---

## 7. Controlled values for permission source

For the first demo, use a small dropdown list.

```text
policy_rule
human_approval
system_role
workflow_configuration
tool_permission
prior_decision
emergency_exception
unknown
```

Definitions:

| Value | Meaning |
|---|---|
| `policy_rule` | A named policy or rule allowed the decision or recommendation |
| `human_approval` | A human approved the decision before it took effect |
| `system_role` | The agent had a configured role that allowed this operation |
| `workflow_configuration` | The workflow allowed this step under configured conditions |
| `tool_permission` | A tool/API permission allowed the action |
| `prior_decision` | A previous recorded decision authorized this one |
| `emergency_exception` | An exception path was used |
| `unknown` | The system cannot show the permission source |

`unknown` is allowed as a value, but it should be embarrassing.

It is not a failure of syntax.

It is a governance finding.

---

## 8. The simple CSV shape

A first demo can produce a CSV like this:

```csv
decision_id,timestamp,agent_name,agent_version,matter_id,decision_type,plain_english_decision,affected_object_type,affected_object_id,action_taken,final_status,permission_source_type,permission_source_id,human_required,human_approver_id,evidence_refs,policy_refs,tool_used,audit_record_ref,exception_flag,notes
dec-001,2026-07-06T18:42:11Z,claims-review-agent,v0.3.1,claim-9981,recommend_approval,The agent recommended approving the claim.,claim,claim-9981,recommendation_created,human_approved,policy_rule,policy-claims-approval-v2,yes,user-442,rec-88;rec-91,policy-claims-approval-v2,claims_api.recommend,audit-evt-55291,no,Confidence below auto-execute threshold; routed to human.
dec-002,2026-07-06T18:44:09Z,access-agent,v0.1.9,access-7731,deny_access,The agent denied the access request because identity verification failed.,access_request,access-7731,access_denied,executed,workflow_configuration,workflow-access-v1,no,,rec-idv-404,policy-access-v1,access_api.deny,audit-evt-55292,no,Auto-denial allowed only for failed identity verification.
dec-003,2026-07-06T18:45:33Z,claims-review-agent,v0.3.1,claim-9982,escalate_review,The agent escalated the claim for human review.,claim,claim-9982,review_task_created,escalated,policy_rule,policy-claims-approval-v2,yes,,rec-94;rec-95,policy-claims-approval-v2,workflow.create_task,audit-evt-55293,no,High-dollar claim exceeded auto-review threshold.
```

---

## 9. Minimal JSON version

For API use, the same output can be JSON:

```json
{
  "decision_id": "dec-001",
  "timestamp": "2026-07-06T18:42:11Z",
  "agent_name": "claims-review-agent",
  "agent_version": "v0.3.1",
  "matter_id": "claim-9981",
  "decision_type": "recommend_approval",
  "plain_english_decision": "The agent recommended approving the claim.",
  "affected_object": {
    "type": "claim",
    "id": "claim-9981"
  },
  "action_taken": "recommendation_created",
  "final_status": "human_approved",
  "permission": {
    "source_type": "policy_rule",
    "source_id": "policy-claims-approval-v2",
    "human_required": true,
    "human_approver_id": "user-442"
  },
  "references": {
    "evidence_refs": ["rec-88", "rec-91"],
    "policy_refs": ["policy-claims-approval-v2"],
    "audit_record_ref": "audit-evt-55291"
  },
  "tool_used": "claims_api.recommend",
  "exception_flag": false,
  "notes": "Confidence below auto-execute threshold; routed to human."
}
```

---

## 10. What the attorney should not ask for

Do not ask for:

- “all thoughts of the AI”;
- hidden chain-of-thought;
- token-level internals;
- every retrieved chunk unless retrieval itself is material to the dispute;
- every prompt draft;
- every non-material intermediate step;
- a post-hoc explanation invented after the fact;
- an answer to “why did the neural network really do this?” stated with false certainty.

Ask for:

- material decisions;
- material recommendations;
- material actions;
- state-changing tool calls;
- human approvals;
- permission sources;
- evidence references;
- policy references;
- audit records.

That is discoverable in practice if the system was designed responsibly.

---

## 11. What the engineer should not build

Do not build this by asking the model after the fact:

```text
Please summarize all decisions you made today.
```

That is not an audit system.

That is a confession booth made of fog.

Instead, instrument the wrapper around the AI system:

1. log when the agent proposes a material decision;
2. log when the agent calls a tool;
3. log when the system checks policy or permission;
4. log when a human approves, rejects, edits, or escalates;
5. log what actually happened;
6. emit a Decision Register row from those logs.

---

## 12. Minimal implementation path

A first-year engineer can implement the first version with four event types:

```text
decision.proposed
permission.checked
human.reviewed
action.executed
```

Then generate a register row by joining events on `decision_id` or `matter_id`.

### Required event fields

```text
event_id
event_type
timestamp
decision_id
agent_name
agent_version
matter_id
actor_id
actor_type
payload_json
audit_record_ref
```

### Example event sequence

```jsonl
{"event_type":"decision.proposed","decision_id":"dec-001","timestamp":"2026-07-06T18:42:11Z","agent_name":"claims-review-agent","agent_version":"v0.3.1","matter_id":"claim-9981","payload_json":{"decision_type":"recommend_approval","plain_english_decision":"The agent recommended approving the claim.","affected_object_type":"claim","affected_object_id":"claim-9981","evidence_refs":["rec-88","rec-91"]}}
{"event_type":"permission.checked","decision_id":"dec-001","timestamp":"2026-07-06T18:42:12Z","payload_json":{"permission_source_type":"policy_rule","permission_source_id":"policy-claims-approval-v2","human_required":true}}
{"event_type":"human.reviewed","decision_id":"dec-001","timestamp":"2026-07-06T18:43:50Z","actor_id":"user-442","actor_type":"human","payload_json":{"review_result":"approved"}}
{"event_type":"action.executed","decision_id":"dec-001","timestamp":"2026-07-06T18:44:01Z","payload_json":{"action_taken":"recommendation_created","final_status":"human_approved","tool_used":"claims_api.recommend","audit_record_ref":"audit-evt-55291"}}
```

---

## 13. Reasonable vs achievable matrix

| Attorney request | Reasonable? | Achievable? | Notes |
|---|---:|---:|---|
| “Give me all material AI decisions for this period.” | Yes | Yes, if instrumented | Best request |
| “Show what the AI recommended and what a human approved.” | Yes | Yes | Very useful |
| “Show every state-changing tool call.” | Yes | Yes | Should be mandatory for agentic systems |
| “Show what policy or permission allowed each action.” | Yes | Yes, if policy checks are logged | Use permission fields, not metaphysics |
| “Show all evidence references used by each decision.” | Yes | Usually | Depends on retrieval/logging quality |
| “Show the AI’s hidden reasoning.” | Usually no | No | Do not design around this |
| “Explain exactly why the model generated each word.” | No | No | False certainty risk |
| “Reconstruct last year’s decisions from partial logs.” | Sometimes | Maybe | Depends on log quality |
| “Prove no unlogged decisions occurred.” | Reasonable as control objective | Hard | Requires instrumentation, access controls, and negative-control evidence |

---

## 14. CDP relationship

The Attorney-Facing Decision Register is not the full CDP record.

It is a review surface.

CDP can use the Decision Register as a projection from deeper governed records, lifecycle envelopes, wire messages, tool events, approval records, and audit logs.

A lawyer does not need to read the whole governed path to ask the first useful question:

> What did the AI materially decide, recommend, or do?

The Decision Register answers that question first.

Then CDP can answer the deeper questions:

- Was the decision admitted properly?
- Was standing valid?
- Was the authority claim sufficient?
- Were challenges available?
- Was evidence preserved?
- Was human approval required?
- Was execution blocked until legitimacy was established?
- Can the decision be replayed?
- Can it be appealed or repaired?

The Decision Register is the front desk.

CDP is the courthouse, docket, evidence room, appeal path, and repair ledger behind it.

---

## 15. Design posture

Do not start with ontology.

Start with the register.

One row per material decision.

Plain English first.

Stable IDs second.

Permission source third.

Evidence and audit references fourth.

Deeper governance fifth.

The output should be boring enough to subpoena, simple enough to explain, and structured enough to govern.
