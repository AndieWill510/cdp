# RFC-CDP-023 v0.8 Amendment — Computational Context References

Author: Kevin “Andie” Williams  
Status: Staged amendment — pending integration into RFC-CDP-023  
Series: Constitutional Decision Plane (CDP)  
Date: July 24, 2026  
Updates: RFC-CDP-023 v0.7  
Depends On: RFC-CDP-021, RFC-CDP-022, RFC-CDP-033, RFC-CDP-047, RFC-CDP-048, RFC-CDP-074

## Integration notice

This file is a normative staged amendment for integration into `rfc/RFC-CDP-023-Decision-Lifecycle-Envelope.md` as Draft v0.8.

It exists separately because the connected write surface available during this change could read only truncated portions of the 694-line RFC and required whole-file replacement for edits. Replacing the canonical RFC from an incomplete read would create an unacceptable risk of silent content loss.

The amendment therefore preserves the exact intended change without pretending that the canonical file was safely rewritten.

## 1. Amendment purpose

RFC-CDP-023 already defines the Decision Lifecycle Envelope as the governed path index for a complete CDP decision.

A new `decision_environment` object is not required.

The confirmed gap is narrower: the envelope currently indexes procedural, evidentiary, standing, execution, covenant, appeal, repair, and learning artifacts, but does not provide a first-class reference family for the computational substrate that materially shaped a decision.

Draft v0.8 adds **computational context references** without turning the envelope into a warehouse.

The envelope indexes governed computational-context records. It does not embed model weights, prompts, retrieved documents, memory contents, tool outputs, or proprietary runtime configuration directly.

## 2. New failure mode

Add the following failure mode to RFC-CDP-023 §1:

8. **Computational substrate invisibility** — a model, harness, tool chain, retrieval configuration, supplied context, or execution constraint materially shapes a governed decision, but the Decision Lifecycle Envelope contains no governed reference identifying that substrate.

Computational substrate invisibility prevents meaningful reconstruction of why the same apparent case and policy produced a different result. It also allows computational change to be mistaken for principled precedent development.

This failure mode is distinct from model-family authority capture under RFC-CDP-033. Independence and reproducibility may overlap, but neither substitutes for the other.

## 3. Minimum viable schema amendment

Add the following top-level control surface after `repair_control` and before `stage_record_refs` in RFC-CDP-023 §4:

```yaml
  # Computational context control surface
  computational_context:
    context_status: <unreviewed|complete|partial|unavailable|not_applicable>
    computational_context_refs: [<ref>]
    model_identity_refs: [<ref>]
    harness_config_refs: [<ref>]
    tool_chain_refs: [<ref>]
    retrieval_config_refs: [<ref>]
    supplied_context_refs: [<ref>]
    execution_environment_refs: [<ref>]
    reconstruction_limit_refs: [<ref>]
```

All reference-list fields are required even when empty.

An empty list means no governed references of that family are currently indexed.

An absent list is ambiguous and non-compliant once the v0.8 schema is claimed.

`context_status: complete` is a positive claim that the implementation has indexed every computational-context reference required by its applicable profile for meaningful reconstruction.

`context_status: unavailable` means the relevant computational context cannot currently be reconstructed and MUST be accompanied by at least one `reconstruction_limit_ref`.

`context_status: not_applicable` MUST NOT be used merely because the decision was human-mediated. Human decisions may still depend on software, retrieval, scoring, simulation, or generated analysis.

## 4. Reference family semantics

### 4.1 computational_context_refs

`computational_context_refs` points to governed records that describe the computational substrate relevant to the decision as a whole.

It MAY include an aggregate manifest record whose content hash covers the narrower reference families below.

### 4.2 model_identity_refs

`model_identity_refs` points to governed records identifying models that materially generated, evaluated, ranked, transformed, summarized, or recommended decision content.

A model identity record SHOULD preserve, where available and permitted:

- provider or operator;
- model family;
- model identifier;
- model or deployment version;
- inference profile or material runtime parameters;
- deployment or endpoint identity;
- effective time window;
- content hash or attestation reference;
- known nondeterminism or reproducibility limits.

A marketing name alone is not sufficient when a more precise deployment identifier is available.

### 4.3 harness_config_refs

`harness_config_refs` points to governed records identifying the orchestration surrounding a model or computational service.

This may include:

- system or policy instruction set version;
- routing and delegation configuration;
- memory and context assembly rules;
- safety and output-gating configuration;
- tool-selection policy;
- retry, sampling, fallback, and escalation behavior;
- applicable schema and parser versions.

The referenced record SHOULD avoid embedding protected prompt content when a content-addressed or sealed reference can preserve integrity without disclosure.

### 4.4 tool_chain_refs

`tool_chain_refs` points to governed records identifying tools, services, connectors, transformations, validators, and execution components that materially shaped the result.

A tool-chain reference SHOULD preserve ordering or dependency relationships when sequence affects the result.

### 4.5 retrieval_config_refs

`retrieval_config_refs` points to governed records identifying retrieval sources and configuration, including:

- index or corpus identity;
- snapshot, effective date, or content-hash boundary;
- query or retrieval policy version;
- ranking, filtering, and cutoff configuration;
- access-control or jurisdictional filters;
- known source omissions or availability failures.

Retrieved evidence itself remains governed through evidence references. This family records how evidence became reachable.

### 4.6 supplied_context_refs

`supplied_context_refs` points to governed records identifying memory, conversation context, examples, prior decisions, instructions, or other supplied material that materially conditioned computation.

This reference family MUST preserve privacy and minimization requirements. A sealed, redacted, hashed, or access-controlled record MAY be used when direct content exposure would be unsafe.

### 4.7 execution_environment_refs

`execution_environment_refs` points to governed records identifying material runtime constraints, including:

- software and dependency versions;
- jurisdiction or region;
- time, cost, latency, or token limits;
- security, privacy, and access restrictions;
- deterministic or nondeterministic execution settings;
- fallback conditions;
- degraded or partial-service state.

### 4.8 reconstruction_limit_refs

`reconstruction_limit_refs` points to governed records explaining why exact or meaningful reconstruction is limited.

Examples include:

- retired or inaccessible model deployment;
- unavailable proprietary service version;
- mutable external source without snapshot;
- irrecoverable retrieved content;
- missing harness or prompt attestation;
- nondeterministic tool behavior;
- privacy or legal restriction preventing replay.

A reconstruction-limit record is not proof that reconstruction is impossible. It is a contestable claim about the current limit.

## 5. Governed path manifest and hash amendment

Computational-context references MUST be included in the governed path manifest when they materially shaped the decision.

The governed path manifest SHOULD preserve:

```yaml
computational_context_manifest:
  context_status: <enum>
  computational_context_refs: [<registered-ref>]
  model_identity_refs: [<registered-ref>]
  harness_config_refs: [<registered-ref>]
  tool_chain_refs: [<registered-ref>]
  retrieval_config_refs: [<registered-ref>]
  supplied_context_refs: [<registered-ref>]
  execution_environment_refs: [<registered-ref>]
  reconstruction_limit_refs: [<registered-ref>]
```

Each registered reference included in the manifest MUST preserve the registration-time content hash or equivalent integrity marker required by RFC-CDP-023.

Changing a model alias, harness configuration, retrieval source, tool version, supplied-context record, or execution-environment record without producing a new governed reference and updated manifest constitutes silent reference mutation.

## 6. Applicability rule

Computational-context references are required when a computational system materially:

- generated or transformed a proposal;
- selected, retrieved, ranked, filtered, or summarized evidence;
- generated a challenge or test;
- recommended or performed adjudication;
- evaluated legitimacy;
- determined or constrained execution;
- generated a Record or Learn artifact;
- affected a material outcome through routing, memory, tool access, or runtime configuration.

A computational system that only transported opaque content without inspecting or transforming it MAY be classified as not material, subject to implementation-profile rules.

Materiality decisions SHOULD be contestable and SHOULD identify the authority making the classification.

## 7. Replay relationship

Computational-context preservation supports two distinct operations:

- **historical reconstruction or replay** — attempt to reproduce the original procedure under the original governed path and computational context;
- **re-adjudication** — decide under the current governed path and computational context while identifying changed conditions.

The envelope indexes what was used and what can be reconstructed. It does not guarantee deterministic replay.

A replay result does not prove that the original decision was legitimate or correct.

An inability to replay does not by itself invalidate the original decision, but the reconstruction limit may affect reliance, auditability, appeal, precedent weight, or required repair.

## 8. Authority pluralism boundary

Computational-context comparison MUST NOT classify all divergent outcomes as drift.

RFC-CDP-074 permits legitimate divergence where distinct, concurrently valid authorities, jurisdictions, sovereignty claims, treaty relationships, or normative orders apply.

The Decision Lifecycle Envelope SHOULD preserve the applicable authority references through existing standing, authority, boundary, appeal, repair, and governed-stage references.

Learn artifacts SHOULD use the `authority_pluralism_exclusion` category defined by RFC-CDP-048 when divergence is attributable to distinct valid authorities rather than a changed computational or procedural substrate.

Authority pluralism is not policy drift merely because two authorities do not produce the same outcome.

The exclusion MUST NOT be used to hide arbitrary inconsistency within the same authority.

## 9. Relationship to RFC-CDP-048

RFC-CDP-023 preserves the governed references needed to explain the computational context.

RFC-CDP-048 classifies what changed and whether the change explains a different outcome.

The relationship is:

- RFC-CDP-023: **what governed path and computational context existed?**
- RFC-CDP-048: **what variance occurred, and what should be learned or ratified?**

The envelope is the index.

The Learn artifact is the governed interpretation of variance.

Neither is a substitute for adjudication.

## 10. Integration checklist

When integrating this amendment into RFC-CDP-023:

1. bump status from Draft v0.7 to Draft v0.8;
2. set `Date: July 24, 2026`;
3. set `Updates: RFC-CDP-023 v0.7`;
4. add the Draft v0.8 abstract paragraph;
5. add computational substrate invisibility as failure mode 8;
6. add the `computational_context` control surface to the minimum viable schema;
7. add the reference-family semantics as a new numbered section;
8. require inclusion in the governed path manifest and hash when material;
9. add replay and authority-pluralism boundaries;
10. update conformance language and examples so absent computational-context lists remain distinguishable from empty lists.

## 11. Principle

A governed path that remembers every procedural step but forgets what computed the result is not yet replayable enough to explain its own drift.

Record the substrate without mistaking the substrate for authority.

Preserve variance without mistaking legitimate pluralism for error.