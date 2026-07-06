# Identifier Registry and Config Lookup Split

Status: design note v0.5  
Scope: no-floating-ID registry, generic config lookup, and decision-registry validation  
Related DDL: `db/ddl/001-decision-registry-kernel.sql`  

---

## 1. Core correction

The normalized Decision Registry fixed one problem:

```text
Do not pack facts into columns.
```

But normalization revealed another problem:

```text
Do not let atomic IDs float without a registry.
```

A column like:

```text
subject_actor_id = claims_review_agent
```

is better than:

```text
subject = agent:claims_review_agent
```

But `claims_review_agent` still needs to be registered somewhere.

Otherwise the database has atomic strings, but not controlled identifiers.

The fix is a separate table:

```text
cdp_core.identifier_registry
```

---

## 2. Naming decision

Do not call this table `z_config_lookup`.

That name implies a miscellaneous bag of configuration values.

The control plane needs something more disciplined:

```text
cdp_core.identifier_registry
```

The naming split is:

```text
cdp_core.decision_registry
  The decisions.

cdp_core.decision_class_registry
  The decision classes/categories.

cdp_core.identifier_registry
  The registered IDs that decisions are allowed to reference.

cdp_core.config_lookup
  Generic miscellaneous config, not governance-critical identity.
```

The decision registry is the ledger.

The decision class registry is the taxonomy.

The identifier registry is the no-floating-ID authority.

The config lookup is the miscellaneous knob drawer.

---

## 3. Why config lookup is still useful

A generic config lookup is still useful for non-governance runtime settings:

```text
feature flags
batch sizes
timeouts
default display settings
local demo switches
```

That table can be generic and intentionally boring:

```text
cdp_core.config_lookup
```

But it must not become the authority for decision actors, objects, verbs, permission sources, or parent relation types.

Those are governance-bearing identifiers.

They belong in:

```text
cdp_core.identifier_registry
```

---

## 4. What the identifier registry does

The identifier registry registers the identifiers used by the decision registry.

It answers:

```text
Is this ID known?
What registry does it belong to?
What type is it?
Is it active or deprecated?
What label should humans see?
Does it have a parent identifier?
```

Every non-decision ID used by `cdp_core.decision_registry` should be either:

1. a self-reference inside `decision_registry`;
2. a reference to `decision_class_registry`;
3. or a registered identifier in `identifier_registry`.

No floating IDs.

---

## 5. Table shape

The table is:

```text
cdp_core.identifier_registry
```

Core columns:

```text
registry_name
identifier_id
identifier_type_registry_name
identifier_type_id
parent_registry_name
parent_identifier_id
display_label
description
status
created
updated_at
```

The unique key is:

```text
(registry_name, identifier_id)
```

This lets the same string appear safely in different registries.

Example:

```text
registry_name = actor
identifier_id = user_442
```

and:

```text
registry_name = permission_source
identifier_id = user_442
```

can both exist, but they mean different registered things.

---

## 6. Registry of registries

The identifier registry also registers the registries themselves.

This is the small recursive move that prevents mystery namespaces.

Example registry rows:

```text
registry_name | identifier_id
registry      | actor
registry      | actor_type
registry      | object
registry      | object_type
registry      | predicate_verb
registry      | permission_source
registry      | permission_source_type
registry      | parent_relation_type
registry      | source_system
registry      | lookup_kind
```

So the system can answer:

```text
Is actor a known registry?
Is permission_source_type a known registry?
Is parent_relation_type a known registry?
```

without hardcoding every namespace in application code.

---

## 7. Lookup kinds

The registry also has a minimal `lookup_kind` registry.

Examples:

```text
registry
enum_value
identifier
business_object
actor
policy
system
source_system
```

These are used to type registry rows and controlled values.

For example:

```text
registry_name = actor_type
identifier_id = agent
identifier_type_registry_name = lookup_kind
identifier_type_id = enum_value
```

means:

```text
agent is an enum value in the actor_type registry.
```

---

## 8. Example registered identifiers

Actor type:

```text
registry_name = actor_type
identifier_id = agent
identifier_type_registry_name = lookup_kind
identifier_type_id = enum_value
display_label = Agent
```

Actor:

```text
registry_name = actor
identifier_id = claims_review_agent
identifier_type_registry_name = actor_type
identifier_type_id = agent
display_label = Claims Review Agent
```

Object type:

```text
registry_name = object_type
identifier_id = claim
identifier_type_registry_name = lookup_kind
identifier_type_id = business_object
display_label = Claim
```

Object:

```text
registry_name = object
identifier_id = claim_9981
identifier_type_registry_name = object_type
identifier_type_id = claim
display_label = Claim 9981
```

Permission source type:

```text
registry_name = permission_source_type
identifier_id = policy_rule
identifier_type_registry_name = lookup_kind
identifier_type_id = enum_value
display_label = Policy Rule
```

Permission source:

```text
registry_name = permission_source
identifier_id = policy_claims_approval_v2
identifier_type_registry_name = permission_source_type
identifier_type_id = policy_rule
display_label = Claims Approval Policy v2
```

---

## 9. Decision-registry validation

The DDL includes a trigger:

```text
trg_validate_decision_registry_identifiers
```

on:

```text
cdp_core.decision_registry
```

The trigger rejects decision rows when referenced identifiers are missing or mistyped.

It validates:

```text
parent_relation_type      -> identifier_registry(parent_relation_type)
subject_actor_type        -> identifier_registry(actor_type)
subject_actor_id          -> identifier_registry(actor) typed by actor_type
predicate_verb            -> identifier_registry(predicate_verb)
object_type               -> identifier_registry(object_type)
object_id                 -> identifier_registry(object) typed by object_type
permission_source_type    -> identifier_registry(permission_source_type)
permission_source_id      -> identifier_registry(permission_source) typed by permission_source_type
human_approver_id         -> identifier_registry(actor) typed by human, unless none or unknown
source_system             -> identifier_registry(source_system)
```

This preserves normal form without accepting loose strings.

---

## 10. What is not registered here

The identifier registry does not store decisions.

Decisions belong in:

```text
cdp_core.decision_registry
```

Decision classes belong in:

```text
cdp_core.decision_class_registry
```

The identifier registry stores the valid nouns and controlled values that decisions may reference.

That boundary matters.

Bad:

```text
Store decisions inside identifier_registry.
```

Better:

```text
Store decisions in decision_registry.
Store allowed referenced IDs in identifier_registry.
```

---

## 11. Loading order

For spreadsheet or fixture ingestion, the safe order is:

```text
1. identifier_registry seed rows
2. decision_class_registry rows
3. additional identifier_registry rows for actors, objects, policies, tools, etc.
4. decision_registry rows
5. projection queries
```

If a decision references a new object such as:

```text
claim_9999
```

then `claim_9999` must be inserted into `identifier_registry` before the decision row is inserted.

No floating IDs.

---

## 12. Why not hardcode only CHECK constraints?

Some values are stable controlled vocabularies, and CHECK constraints are useful for early demo discipline.

But CHECK constraints alone do not solve the general problem.

For example:

```text
subject_actor_id
object_id
permission_source_id
human_approver_id
```

can vary from demo to demo, matter to matter, and system to system.

They need a registry, not a hardcoded enum.

The current DDL uses both:

- CHECK constraints for basic shape and a few core finite enums;
- identifier-registry validation for no-floating-ID enforcement.

That is acceptable for the demo.

Later profiles may move more controlled values out of CHECK constraints and into registry-only enforcement.

---

## 13. Design rule

Use `decision_registry` for decisions.

Use `decision_class_registry` for decision classes.

Use `identifier_registry` for referenced IDs.

Use `config_lookup` for miscellaneous config.

Use views to derive compatibility strings.

Do not store packed strings as authoritative data.

Do not let IDs float.

Do not make config lookup carry governance authority.
