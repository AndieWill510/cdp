# CDP Simple Swimlane Diagram

**Status:** Draft  
**Category:** Architecture Documentation / Diagram  
**Date:** 2026-05-03  
**Related:** `docs/diagrams/cdp-data-flow-diagram.md`, `README.md`  

---

## 1. Purpose

This document provides a simple UML-style swimlane diagram for the Constitutional Decision Plane (CDP).

The goal is to show responsibility boundaries across human, AI, governance, execution, audit, and repair lanes without the full detail of the data flow diagram.

This is documentation, not an RFC.

---

## 2. Swimlane Diagram

```mermaid
flowchart TB
    %% Mermaid does not have native UML swimlanes, so each subgraph is used as a lane.

    subgraph L1[Human / Affected Party]
        H1[Submit intent or request]
        H2[Provide evidence or context]
        H3[Raise challenge, appeal, or harm claim]
        H4[Review decision, appeal, or repair record]
    end

    subgraph L2[AI Agent / Source System]
        A1[Generate proposed action]
        A2[Attach evidence bundle]
        A3[Declare assumptions and uncertainty]
        A4[Wait for authorization]
    end

    subgraph L3[CDP Governance Plane]
        G1[Create decision envelope]
        G2[Identify standing and authority]
        G3[Nemawashi / clarify context]
        G4[Propose]
        G5[Challenge]
        G6[Test]
        G7[Adjudicate]
        G8[Legitimize]
    end

    subgraph L4[Execution Control Plane]
        E1[Apply maturity gate]
        E2[Queue for review if required]
        E3[Check presence grant]
        E4[Authorize execution]
        E5[Execute action]
        E6[Rollback or compensate if needed]
    end

    subgraph L5[Audit / Record Plane]
        R1[Append event log]
        R2[Create decision record]
        R3[Create appeal or repair record]
        R4[Provide replay / audit view]
        R5[Emit learning signals]
    end

    subgraph L6[Repair Plane]
        P1[Intake appeal or harm claim]
        P2[Conduct affected-party review]
        P3[Determine breach]
        P4[Create repair agenda]
        P5[Commit remedy]
        P6[Verify repair]
    end

    %% Main happy path
    H1 --> H2 --> G1
    A1 --> A2 --> A3 --> G1
    G1 --> G2 --> G3 --> G4 --> G5 --> G6 --> G7 --> G8
    G8 --> E1 --> E2 --> E3 --> E4 --> E5
    E5 --> R1 --> R2 --> R4 --> H4

    %% Waiting / authority path
    A4 -. waits on .-> E4
    E2 -. requires review .-> G5

    %% Challenge and repair paths
    H3 --> P1
    G5 -. contested .-> P1
    G8 -. legitimacy failure .-> P1
    E5 -. harm or exceeded authority .-> P1
    E6 --> P1

    P1 --> P2 --> P3
    P3 -- breach found --> P4 --> P5 --> P6 --> R3
    P3 -- no breach found --> R3
    R3 --> R4 --> H4

    %% Learning path
    R2 --> R5
    R3 --> R5
    R5 -. updates context .-> G3
    R5 -. updates gates .-> E1
```

---

## 3. Lane Responsibilities

| Lane | Responsibility |
|---|---|
| Human / Affected Party | Submit requests, supply context, challenge decisions, raise harm claims, review outcomes. |
| AI Agent / Source System | Generate proposals, attach evidence, disclose assumptions, wait for authorization. |
| CDP Governance Plane | Wrap decisions, establish standing, deliberate, test, adjudicate, and legitimize. |
| Execution Control Plane | Gate, queue, authorize, execute, rollback, and compensate. |
| Audit / Record Plane | Preserve events, decisions, appeals, repair records, replay views, and learning signals. |
| Repair Plane | Intake appeals, review harms, determine breaches, create repair agendas, verify remedies. |

---

## 4. Design Notes

- This is intentionally simpler than `cdp-data-flow-diagram.md`.
- Each Mermaid subgraph functions as a UML-style swimlane.
- This diagram emphasizes responsibility boundaries rather than full protocol detail.
- Challenge, appeal, rollback, compensation, and repair are first-class paths rather than exceptions.
- Learning is downstream of decision and repair records; it does not replace repair.
