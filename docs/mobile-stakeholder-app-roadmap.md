# Mobile Stakeholder App Roadmap

Status: product roadmap track v0.1  
Audience: product builders, Swift/iOS implementers, corporate attorneys, Trust & Safety reviewers, AI governance teams  
Related docs / artifacts:

- `docs/product-demo-scenarios-roadmap.md`
- `docs/superset-decision-visualization-roadmap.md`
- `docs/nemawashi-workflow-rules-engine.md`
- `docs/decision-lifecycle-review-flow.md`
- `rfc/RFC-CDP-023-Decision-Lifecycle-Envelope.md`
- `db/ddl/001-decision-registry-kernel.sql`
- `db/ddl/003-nemawashi-workflow-rules.sql`
- `tests/test_nemawashi_workflow_rules_ddl.py`

---

## 1. Product decision

Build the first stakeholder-facing mobile app as a native iPhone app.

Recommended stack:

```text
Swift + SwiftUI first.
FastAPI/Postgres backend.
OpenAPI-generated Swift client.
SwiftData only for local cache and offline drafts.
APNs push notifications for tasks, blockers, challenges, and consultation updates.
```

Superset remains the free interactive dashboard/admin/demo cockpit.

The iPhone app is the stakeholder action cockpit.

```text
Superset:
  show where and how decisions are made across scenarios

Mobile app:
  tell the right stakeholder what needs attention and let them respond
```

---

## 2. Why native iPhone first

CDP's mobile product job is not generic analytics.

The mobile product job is:

```text
Tell the right stakeholder:
  You have a decision to review.
  Here is what happened.
  Here is why you matter.
  Here is what blocks advancement.
  Here are your governed response options.
```

That needs clarity, trust, accessibility, security, notifications, offline-safe drafts, and a polished native feel.

SwiftUI is the best first path for an iPhone-first stakeholder app.

React Native / Expo and Flutter remain credible alternatives if the goal changes to rapid cross-platform delivery.

Current decision:

```text
SwiftUI now.
Cross-platform later only if the product need becomes unavoidable.
```

---

## 3. Role in the CDP product stack

Recommended stack:

```text
iPhone app
  SwiftUI
  Observation / app state
  async/await networking
  OpenAPI-generated API client
  Keychain token storage
  SwiftData local cache / offline drafts
  APNs push notifications

Backend
  FastAPI
  Postgres
  CDP core tables
  Workflow/rules tables
  Auth/RBAC
  WebSocket or polling for live-ish updates

Admin / demo / analytics
  Superset
  Markdown review packets
  JSON visualization specs
```

Do not let the mobile app talk directly to Postgres.

The app talks to a governed API.

---

## 4. First app concept

Working name:

```text
CDP Stakeholder Cockpit
```

The app should feel like a secure review inbox, not a dashboard port.

Primary user stories:

```text
As a stakeholder, I can see decisions waiting on me.
As a privacy counsel, I can see why I was pulled into a restricted-data decision.
As a data owner, I can respond to an access request before it advances.
As a reviewer, I can see blockers and required responses.
As a participant, I can object, clarify, approve, recuse, or provide evidence.
As an adjudicator, I can see unresolved challenges and context.
```

---

## 5. First screens

### 5.1 Inbox

Purpose:

```text
Show the stakeholder what needs attention.
```

Sections:

```text
My pending reviews
Blocking tasks
Due soon
Unread consultation threads
Open objections
Waiting on me
```

Primary data source:

```text
cdp_projection.workflow_task_queue
cdp_projection.nemawashi_blockers
cdp_projection.communication_thread_flat
```

---

### 5.2 Decision Card

Purpose:

```text
Show what happened and why the stakeholder is being asked to participate.
```

Fields:

```text
decision_id
decision_class_id
plain-English decision
subject actor
predicate/action
object
permission source
human_required
lifecycle_stage
workflow_status
blocked / not blocked
```

Primary data source:

```text
cdp_projection.decision_registry_flat
cdp_projection.workflow_task_queue
cdp_projection.nemawashi_blockers
```

---

### 5.3 Nemawashi Stakeholders

Purpose:

```text
Show who has been identified and what role each stakeholder has.
```

Stakeholders:

```text
data owner
system owner
privacy counsel
security reviewer
legal reviewer
safety reviewer
human approver
affected party proxy
witness
observer
```

Primary data source:

```text
cdp_projection.nemawashi_stakeholder_map_flat
```

---

### 5.4 Thread

Purpose:

```text
Give stakeholders a governed communication surface.
```

Thread types:

```text
nemawashi_consultation
clarification
challenge_discussion
adjudication_discussion
execution_review
repair_discussion
```

Message types:

```text
comment
objection
clarification_request
clarification_response
boundary_statement
evidence_pointer
standing_statement
approval
recusal
```

Primary data source:

```text
cdp_core.communication_thread
cdp_core.communication_participant
cdp_core.communication_message
cdp_projection.communication_thread_flat
```

---

### 5.5 Action Sheet

Purpose:

```text
Constrain stakeholder responses to governed actions.
```

Actions:

```text
Acknowledge
Request clarification
Object
Approve participation
Recuse
Provide evidence
Raise challenge
Approve / reject review task
```

Important rule:

```text
The app should not offer arbitrary state mutation.
It should offer governed response actions that create records, messages, tasks, findings, or challenges.
```

---

### 5.6 Blockers

Purpose:

```text
Show why a decision cannot advance.
```

Blocker types:

```text
missing stakeholder
required stakeholder response incomplete
blocking workflow task
rule-blocked transition
open challenge
missing human reviewer
unresolved affected-party claim
```

Primary data source:

```text
cdp_projection.nemawashi_blockers
cdp_projection.rule_evaluation_findings
```

---

### 5.7 Decision Lineage

Purpose:

```text
Show how this decision depends on earlier decisions.
```

Lineage types:

```text
child_of
depends_on
derived_from
escalates_from
approves
denies
appeal_of
repair_of
supersedes
```

Primary data source:

```text
cdp_projection.decision_parent_child_edges
```

---

## 6. API boundary

The iPhone app should call a governed API, never Postgres directly.

First API shape:

```text
GET  /me/tasks
GET  /me/threads
GET  /decisions/{decision_id}
GET  /decisions/{decision_id}/stakeholders
GET  /decisions/{decision_id}/blockers
GET  /decisions/{decision_id}/threads
GET  /threads/{thread_id}/messages
POST /threads/{thread_id}/messages
POST /decisions/{decision_id}/actions/acknowledge
POST /decisions/{decision_id}/actions/object
POST /decisions/{decision_id}/actions/request-clarification
POST /decisions/{decision_id}/actions/provide-evidence
POST /decisions/{decision_id}/actions/recuse
POST /decisions/{decision_id}/actions/raise-challenge
POST /tasks/{task_id}/complete
POST /tasks/{task_id}/waive
```

The API should return DTOs aligned to app screens, not raw table rows.

---

## 7. Suggested Swift project structure

```text
CDPMobile/
  App/
    CDPMobileApp.swift
    AppState.swift
    AuthState.swift

  API/
    CDPClient.swift
    DTOs/
    Generated/
      OpenAPIClient.swift

  Features/
    Inbox/
    DecisionDetail/
    Stakeholders/
    Threads/
    Blockers/
    Actions/
    Lineage/

  Models/
    DecisionSummary.swift
    WorkflowTask.swift
    Stakeholder.swift
    CommunicationThread.swift
    CommunicationMessage.swift
    Blocker.swift

  LocalStore/
    DraftMessage.swift
    CachedDecision.swift

  Design/
    CDPTheme.swift
    StatusBadges.swift
```

State style:

```text
SwiftUI views
  -> feature view models / observable state
  -> CDPClient
  -> governed backend API
  -> Postgres/CDP projections
```

---

## 8. Mapping from CDP projections to screens

```text
cdp_projection.workflow_task_queue
  -> Inbox
  -> Task detail
  -> Due soon
  -> Blocking task cards

cdp_projection.decision_registry_flat
  -> Decision Card
  -> Decision summary
  -> Permission-source display

cdp_projection.nemawashi_stakeholder_map_flat
  -> Stakeholder Map
  -> Participation status
  -> Missing-role warnings

cdp_projection.nemawashi_blockers
  -> Blockers screen
  -> Decision advancement warning

cdp_projection.communication_thread_flat
  -> Thread list
  -> Unread/open thread cards

cdp_core.communication_message
  -> Thread body
  -> Objections / clarifications / evidence pointers

cdp_projection.rule_evaluation_findings
  -> Why this task exists
  -> Why this transition is blocked
  -> What rule created the work

cdp_projection.decision_parent_child_edges
  -> Decision lineage
```

---

## 9. First build slice

The first mobile slice should be small and powerful:

```text
Login
  -> Task Inbox
  -> Decision Detail
  -> Stakeholder Map
  -> Consultation Thread
  -> Post objection / clarification / approval / recusal
```

Minimum backend support:

```text
/me/tasks
/decisions/{decision_id}
/decisions/{decision_id}/stakeholders
/decisions/{decision_id}/blockers
/decisions/{decision_id}/threads
/threads/{thread_id}/messages
POST /threads/{thread_id}/messages
POST /tasks/{task_id}/complete
```

Minimum database support:

```text
001-decision-registry-kernel.sql
003-nemawashi-workflow-rules.sql
```

Minimum scenario support:

```text
restricted_data_access
```

---

## 10. First demo story

Use restricted data access.

Demo flow:

```text
1. A restricted-data access decision is registered.
2. CDP creates a workflow instance.
3. CDP identifies required stakeholder roles.
4. CDP creates a blocking human-review task.
5. CDP opens a Nemawashi consultation thread.
6. Privacy counsel receives the task on iPhone.
7. Privacy counsel opens the decision card.
8. The app shows why privacy counsel matters.
9. The app shows a missing data-owner blocker.
10. Privacy counsel posts an objection.
11. The objection is recorded in the thread.
12. The workflow remains blocked until the blocker is resolved or waived.
```

Product punchline:

```text
CDP does not merely visualize that a decision happened.
It routes the decision to the right people and captures governed participation before the decision advances.
```

---

## 11. Push notifications

Push notifications should be used for governed work, not spam.

Notification types:

```text
new_task_assigned
blocking_task_due_soon
new_consultation_message
stakeholder_response_required
challenge_raised
adjudication_required
execution_blocked
repair_required
```

Notification rule:

```text
A notification is not participation.
An acknowledgment is not consent.
No response is not legitimacy unless a protocol explicitly says so.
```

---

## 12. Offline and local cache

Use local persistence for convenience, not authority.

SwiftData may store:

```text
cached task summaries
cached decision summaries
cached stakeholder maps
draft messages
draft evidence pointers
last-read thread state
```

SwiftData must not become authority for:

```text
standing
adjudication
legitimacy
execution approval
repair closure
workflow transition
```

The backend remains the authority.

---

## 13. Security / trust baseline

Mobile baseline:

```text
OAuth/OIDC login
short-lived access tokens
refresh-token handling
Keychain storage
server-side authorization checks
per-decision access control
per-thread participant checks
redaction-aware DTOs
push notification content minimization
local cache clearing on logout
```

Security rule:

```text
The app may display governed state.
The backend decides whether the user can see or change it.
```

---

## 14. Alternatives and when to reconsider

### SwiftUI

Best when:

```text
iPhone-first product
polished native UX
secure stakeholder workflow
push notifications
accessibility
offline drafts/local cache
```

Current recommendation:

```text
Use SwiftUI first.
```

### Expo / React Native

Best when:

```text
iOS + Android quickly
TypeScript team
shared app logic across platforms
faster prototype cycles
```

Reconsider if:

```text
Android becomes immediately required
web/mobile code sharing becomes more important than iPhone polish
```

### Flutter

Best when:

```text
highly custom cross-platform UI
Dart is acceptable
multiple platforms from one codebase
```

Reconsider if:

```text
brand-heavy custom UI becomes more important than native Apple integration
```

---

## 15. Acceptance criteria

The first mobile roadmap slice is complete when:

1. SwiftUI app scaffold exists.
2. App can authenticate against a local/dev backend.
3. App can load `/me/tasks`.
4. App can show a task inbox from `workflow_task_queue`.
5. App can show a decision card.
6. App can show stakeholders for a decision.
7. App can show blockers.
8. App can show consultation threads.
9. App can post a governed message.
10. App can complete or respond to a workflow task.
11. App does not connect directly to Postgres.
12. App does not offer arbitrary state mutation.
13. Backend enforces per-decision authorization.
14. Local cache is non-authoritative.
15. Push notifications are scoped to governed work.

---

## 16. Design rules

Superset is the dashboard cockpit.

The mobile app is the stakeholder action cockpit.

Jupyter is the engineering workbench.

The backend is the governance authority.

The mobile app is not the system of record.

The mobile app should not talk directly to Postgres.

The app should not ask stakeholders to understand the whole control plane before acting.

The app should answer:

```text
Why am I here?
What decision needs attention?
What blocks it?
What can I do?
What will my response become in the governed record?
```
