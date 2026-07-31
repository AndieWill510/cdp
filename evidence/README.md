# Evidence Layer

Status: Draft v0.1

## Purpose

The repository has three layers that describe what CDP *should* do and one
gap: nothing describes what CDP has actually been shown to do. This directory
is that fourth layer.

The guiding rule is:

> **We only claim what we can substantiate.**

Every claim in this directory must be backed by a verifiable artifact —
something a third party could re-run or re-read and reach the same
conclusion. If a claim cannot be tied to such an artifact, it does not belong
here.

## The four layers

| Layer | Location | Answers | Kind of claim |
|---|---|---|---|
| RFCs | `rfc/`, `rfcs/` | What is CDP supposed to be? | Constitutional specification |
| Architecture | `docs/` (diagrams, design notes) | How do the specified pieces compose? | Composition / design |
| Implementation | `cdp/`, `src/cdp_control_plane/`, `prototype/` | What code exists? | Executable artifact |
| **Evidence** | `evidence/` | What has actually been demonstrated? | Verified fact |

These layers are ordered by decreasing distance from proof. An RFC can
describe a protocol that no code implements. Code can exist that no test
exercises. Only this layer is restricted to claims that have already been
checked against reality.

**Normative documents are never evidence.** An RFC saying a protocol must
exist is not evidence the protocol exists. An architecture diagram showing
how a component would compose with others is not evidence it does. A module
sitting in `cdp/` with no test importing it is not evidence it works —
unexercised code is E1 at best, never higher.

## What counts as an artifact

A claim in this directory must cite one or more of:

- GitHub Actions run output (a workflow run, job, and conclusion that can be
  looked up by ID or URL)
- `pytest` output (a specific run, log file, or CI job — not "the tests
  probably pass")
- Runtime logs (from a running process, container, or service)
- API transcripts (an actual request/response pair, not a schema)
- Integration test results (tests that exercise more than one component
  together, e.g. a live API against a live database)
- Reproducible demonstrations (steps anyone can follow to get the same
  result)

A claim that cannot cite one of these is not evidence. Write "No evidence
currently available" instead of inferring capability from adjacent RFC or
architecture text.

## Evidence levels

Every governance step, protocol, or capability documented in this layer is
assigned exactly one level, based on the *strongest* artifact currently
available for it:

| Level | Meaning | What must exist |
|---|---|---|
| E0 | Specified only | An RFC and/or architecture document. No code. |
| E1 | Implemented | Code exists in a canonical implementation path (`cdp/`). No test exercises it. |
| E2 | Structurally tested | A test exercises the code without a live dependency (no database, no running server) — e.g. schema/DDL shape checks, pure-function unit tests. |
| E3 | Runtime tested | A test exercises the code against a live dependency running locally (e.g. a real Postgres instance), but not through the full stack (no live API call). |
| E4 | Integration tested | A test exercises the code through the full stack as a caller would use it — e.g. an HTTP request against a running API server backed by a live database — and this is confirmed to run and pass in CI, not just locally. |
| E5 | Production demonstrated | The capability has been observed operating in a production deployment, not just CI or a developer's machine. |

Levels are not cumulative credentials — a capability is E4 only if an E4-type
artifact exists *now*, not because it once passed at that level and may have
regressed since (see [`003-known-gaps.md`](003-known-gaps.md) for how
regressions and drift are tracked).

## What an evidence level does not claim

An evidence level answers one question: *has this been demonstrated to
work, at least once, by an artifact of this kind?* It does not answer two
other questions that are easy to conflate with it:

- **Is the test suite behind that level thorough?** E4 means an
  integration test exercised the capability through the full stack and
  passed in CI. It does not mean the test suite has no blind spots, edge
  cases, or fragile assumptions. A capability's evidence level and its test
  suite's health are separate claims, tracked in separate columns: the
  level lives in `000-current-state.md`/`001-test-matrix.md`'s
  Static/Runtime/API/Integration Tests columns, and the health assessment
  lives in `001-test-matrix.md`'s dedicated **Test Suite Health** column
  (Healthy / Known gaps / Not exercised in CI / N/A), with specifics cited
  in that row's Notes.
- **Has this been proven in production?** E4 evidence in this repository
  currently only ever means "proven in CI" — a provisioned service
  container and a freshly started process inside a GitHub Actions run, not
  a live deployment. E5 (Production demonstrated) is the only level that
  answers the production question, and as of this writing no capability in
  `000-current-state.md` has reached it. Do not read E4 as "battle-tested."

Concretely, these are three independent claims, and a capability's rating
on one says nothing about its rating on the others:

| Claim | Example |
|---|---|
| Capability evidence level | Challenge workflow: E4 |
| Test suite health | Challenge test suite: no known blind spots, vs. "has known gaps around concurrent adjudication" |
| Production experience | Challenge: E0 — never run outside CI/local Docker |

A concrete case from this repository's own history: a test-suite
reorganization moved files without updating their file-relative path
computations, and CI caught two resulting bugs (repo-root and fixture
lookups resolving to the wrong directory). Neither bug touched the
governance logic those tests exercise — the *capability's* evidence level
was unaffected — but it was a real, if temporary, gap in test-suite health
that a passing local run had not revealed. Recording only the capability's
E-level would have missed that story entirely; it belongs in the
test-suite-health dimension, not the capability dimension.

## Documents in this layer

- [`000-current-state.md`](000-current-state.md) — evidence level for every
  governance step, cited to artifacts.
- [`001-test-matrix.md`](001-test-matrix.md) — which test types exist for
  which governance step.
- [`002-demonstrated-capabilities.md`](002-demonstrated-capabilities.md) —
  narrative description of capabilities that have cleared at least E2,
  evidence-first.
- [`003-known-gaps.md`](003-known-gaps.md) — capabilities the constitution
  expects that have no implementation or test evidence yet, described
  without proposing fixes.

## Maintenance rule

Whenever a pull request materially changes repository capability — a new
governance step is implemented, a test is added or removed, a CI job starts
or stops covering something, a route is added or dropped — the relevant
document(s) in this layer must be updated in the same PR. The Evidence layer
reflects the repository's **demonstrated** state, not its intended state. A
stale evidence document is worse than no evidence document, because it looks
authoritative while being wrong.
