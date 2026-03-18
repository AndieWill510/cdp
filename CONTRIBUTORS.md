# Contributing to CDP

CDP is not a typical application project.

It is a **protocol system**—a constitutional layer for decision-making.

Contributions are welcome.  
But correctness, clarity, and discipline matter more than speed.

---

## Principles

All contributions MUST align with the following:

### 1. Decisions Are First-Class

CDP governs decisions, not just data or APIs.

Every change must preserve:
- contestability
- auditability
- legitimacy
- replayability

---

### 2. Protocol > Implementation

The protocol is the product.

- RFCs are canonical
- Code is a reference implementation

If code and RFC diverge, the RFC wins.

---

### 3. No Silent Authority

All authority must be:

- explicit
- verifiable
- constrained

No hidden privilege. No implicit trust.

---

### 4. Adversarial Integrity

CDP assumes:

> Systems improve under challenge.

Design for:
- disagreement
- falsification
- audit

Not convenience.

---

### 5. Determinism Over Cleverness

Prefer:
- explicit state transitions
- clear schemas
- traceable behavior

Avoid:
- implicit magic
- hidden side effects
- ambiguous flows

---

## Contribution Types

We welcome contributions in:

### Protocol Design
- RFC proposals
- protocol refinements
- schema evolution

### Implementation
- state machine correctness
- API behavior
- persistence models

### Simulation
- adversarial scenarios
- governance stress tests
- failure modeling

### Documentation
- diagrams
- examples
- clarity improvements

---

## RFC Process

Significant changes MUST go through RFCs.

### Steps:
1. Open draft in `/rfc`
2. Describe:
   - problem
   - proposed change
   - invariants affected
3. Expect challenge
4. Revise
5. Reach rough consensus
6. Merge

---

## Code Standards

- Python: typed, explicit, readable
- No hidden side effects
- State transitions must be:
  - explicit
  - validated
  - logged

Every mutation MUST:
- pass through a protocol
- produce a record
- be replayable

---

## What Not To Do

Do NOT:

- bypass the state machine
- mutate state outside protocol flows
- introduce implicit authority
- weaken auditability
- optimize away traceability

If it makes the system less explainable, it is wrong.

---

## Testing Philosophy

We test for:

- correctness under challenge
- invalid transitions
- adversarial inputs
- replay consistency

Not just “happy paths.”

---

## Tone

Be direct. Be precise. Be respectful.

Disagreement is expected.  
Ambiguity is not.

---

## Final Note

CDP is infrastructure for decisions.

Bad infrastructure fails silently.  
Good infrastructure makes failure visible.

We are building the latter.
