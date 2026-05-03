# RFC-CDP-012 — Identify Protocol

Author: Kevin “Andie” Williams  
Status: Draft v0.3  
Series: Constitutional Decision Plane (CDP)  
Date: March 17, 2026

## Abstract
Defines how humans, institutions, and synthetic actors are identified in CDP.

## 1. Purpose
The Identify Protocol answers:
- how humans, institutions, and synthetic actors are identified;
- how delegation and scope are represented;
- how identity links to authority.

## 2. Actor Types
At minimum:
- `human`
- `institution`
- `synthetic`

## 3. Required Properties
An identity SHOULD include:
- stable actor identifier;
- actor type;
- display label;
- trust source;
- authority grants;
- delegation relationships;
- revocation status.

## 4. Delegation
If authority may be delegated, policy MUST define:
- who may delegate;
- to whom;
- for what scope;
- until when;
- how revocation behaves.

## 5. Principle
No anonymous authority. Anonymous participation MAY exist only under explicit policy and without silent escalation into unverified power.
