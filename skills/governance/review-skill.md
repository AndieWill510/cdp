---
name: review-skill
description: Review an existing CDP skill for clarity, safety, evidence quality, and real-world usefulness before changing it.
inputs:
  - path to the skill under review
  - one or more completed task reports or concrete friction observations
outputs:
  - evidence-backed review
  - explicit keep, revise, split, merge, or retire recommendation
---

# Goal

Determine whether a skill helps humans and agents perform recurring work reliably without hiding uncertainty, weakening safeguards, or creating unnecessary process.

## Preconditions

- Read `AGENTS.md` and `skills/README.md`.
- Read the complete skill under review.
- Gather concrete evidence from at least one attempted use when available.
- Distinguish a failure of the skill from a failure of its underlying script, tool, environment, or implementation.

## Procedure

1. State the skill's intended capability in one sentence.
2. Identify the evidence used for this review:
   - task reports
   - commands and logs
   - user or contributor friction
   - repeated omissions or errors
3. Check the skill against these dimensions:
   - **Legibility:** Can a new contributor understand what to do and why?
   - **Executability:** Are commands, files, and expected results concrete?
   - **Safety:** Are destructive or irreversible actions bounded?
   - **Contestability:** Can a contributor stop, question, or challenge the procedure?
   - **Evidence:** Does success require proof rather than assertion?
   - **Scope:** Is the skill small enough to compose and broad enough to reuse?
   - **Portability:** Can humans and multiple capable agents follow it?
   - **Honesty:** Does it require uncertainty and blockers to be reported?
4. Identify schema drift between the written skill and actual repository behavior.
5. Classify each finding as:
   - defect
   - ambiguity
   - missing safeguard
   - obsolete instruction
   - overfitting
   - useful extension
6. Recommend exactly one disposition:
   - keep unchanged
   - revise
   - split
   - merge
   - deprecate
   - retire
7. When recommending a change, describe the smallest coherent patch and the evidence that would validate it.

## Success Criteria

- The review cites concrete evidence rather than aesthetic preference alone.
- The recommendation is explicit and proportionate.
- Safety and governance are not weakened for convenience.
- Any proposed change includes a validation method.

## Never

- Do not rewrite a skill merely because wording could be more elegant.
- Do not infer repeated friction from a single unexplained failure.
- Do not let the same agent silently propose, approve, and validate a consequential safety reduction.
- Do not remove stop conditions, human review, or evidence requirements without explicit authorization.

## Report

Report:

- skill reviewed
- evidence examined
- what worked
- defects or friction found
- schema drift found
- recommended disposition
- proposed smallest patch
- validation required
- dissent or unresolved uncertainty
