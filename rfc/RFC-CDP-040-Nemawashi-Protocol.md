# RFC-CDP-010 — Nemawashi Protocol

Author: Kevin “Andie” Williams  
Status: Draft v0.3  
Series: Constitutional Decision Plane (CDP)  
Date: March 17, 2026

## Abstract
Defines pre-formal and continuous alignment within CDP.

## 1. Purpose
The Nemawashi Protocol answers:
- how pre-formal and continuous alignment works;
- how stakeholders are surfaced;
- how tone, readiness, and friction are managed before and throughout deliberation.

## 2. Authority
Actors invoking this protocol MUST possess `ALIGN` authority or an equivalent facilitation authority defined by policy.

## 3. Semantics
Nemawashi is not legitimacy.
Nemawashi is social preparation for deliberation.

It MAY:
- surface stakeholders;
- uncover hidden objections early;
- improve proposal quality;
- reduce avoidable friction.

It MUST NOT:
- replace Challenge;
- silently resolve formal objections;
- confer legitimacy.

## 4. Recommended Payload
```json
{
  "stakeholders": ["actor_id"],
  "positions": [
    {
      "actor_id": "string",
      "stance": "support | oppose | neutral",
      "notes": "string"
    }
  ],
  "alignment_status": "low | medium | high",
  "open_issues": ["string"],
  "engagements": ["string"],
  "metadata": {}
}
```

## 5. Invariant
Deliberation MUST be socially prepared, not just logically executed.
