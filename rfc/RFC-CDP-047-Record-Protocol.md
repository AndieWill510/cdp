# RFC-CDP-008 — Record Protocol

Author: Kevin “Andie” Williams  
Status: Draft v0.3  
Series: Constitutional Decision Plane (CDP)  
Date: March 17, 2026

## Abstract
Defines the official record of a Decision lifecycle.

## 1. Purpose
The Record Protocol answers:
- what the official record is;
- what must be preserved;
- how provenance, transcript, evidence, and outcomes are attached;
- how replay and audit work.

## 2. Authority
Actors invoking this protocol MUST possess `RECORD` authority, or the implementation MUST provide an automatic trusted record service.

## 3. What MUST Be Preserved
- Decision versions;
- Envelopes and lineage;
- challenges, tests, adjudications, legitimations, and execution results;
- timestamps;
- actor references;
- artifact references;
- outcome summaries.

## 4. State Transitions
- `EXECUTED → RECORDED`
- `REJECTED → RECORDED`
- `FAILED → RECORDED`
- `ROLLED_BACK → RECORDED`

## 5. Replay Requirement
The record MUST support reconstruction of:
- who acted;
- when;
- under what authority;
- on which Decision version;
- with what result.

## 6. Recommended Payload
```json
{
  "record_ref": "string",
  "artifact_refs": ["string"],
  "transcript_refs": ["string"],
  "summary": "string",
  "outcome": "string",
  "metadata": {}
}
```

## 7. Principle
If an act cannot be reconstructed, it was not adequately governed.
