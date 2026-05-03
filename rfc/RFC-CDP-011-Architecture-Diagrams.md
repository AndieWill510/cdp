# RFC-CDP-011 — Architecture Diagrams

Author: Kevin “Andie” Williams  
Status: Draft v0.1  
Series: Constitutional Decision Plane (CDP)  
Date: May 3, 2026  
Depends On: RFC-CDP-001, RFC-CDP-010

## Abstract

This RFC provides simple Mermaid architecture diagrams for the Constitutional Decision Plane (CDP).

The diagrams are explanatory. They do not replace the normative architecture in RFC-CDP-010. If a diagram and normative prose conflict, the prose controls.

## 1. Purpose

This document gives readers a compact visual map of CDP:

- a conceptual plane diagram;
- a logical component diagram;
- an execution and remedy control path.

The diagrams are stored as Mermaid text so they remain versionable, reviewable, and editable in source form.

## 2. Conceptual Architecture

```mermaid
flowchart TB
    CF["Constitutional Frame<br/>Vision • Scope • Principles • Invariants"]

    subgraph DP["Decision Plane"]
        N["Nemawashi"]
        P["Propose"]
        C["Challenge"]
        T["Test"]
        A["Adjudicate"]
        L["Legitimize"]
        EX0["Execute"]
        R["Record"]
        LN["Learn"]
        N --> P --> C --> T --> A --> L --> EX0 --> R --> LN
    end

    subgraph ERP["Execution and Remedy Plane"]
        MG["Maturity Gate"]
        QR["Queue / Review"]
        PG["Presence Grant"]
        EX["Bounded Execution"]
        KS["Kill Switch"]
        RB["Rollback / Mitigation"]
        CP["Compensation"]
        RM["Remedy"]
        SR["Sufficiency Review"]
        RH["Residual Harm"]
        ER["Record / Learn"]
        MG --> QR --> PG --> EX
        EX --> KS --> RB --> CP --> RM --> SR --> RH --> ER
    end

    subgraph CVP["Covenant Plane"]
        CE["Covenant Established"]
        WT["Witness"]
        SD["Schema Drift"]
        BI["Boundary Issue"]
        CR["Covenant Repair"]
        CE --> WT --> SD --> CR
        WT --> BI --> CR
    end

    subgraph RRP["Repair / Reparations / Rematriation / Sovereignty Plane"]
        BR["Breach Record"]
        RA["Repair Agenda"]
        RP["Repair Points"]
        AP["Affected-Party Review"]
        SC["Sovereignty Claims"]
        IR["Institutional Response"]
        RC["Repair Commitment"]
        RO["Return Obligation"]
        CEV["Completion Evidence"]
        BR --> RA --> RP
        RP --> AP
        RP --> SC
        AP --> IR --> RC --> RO --> CEV
    end

    CF --> DP
    CF --> ERP
    CF --> CVP
    CF --> RRP

    DP <--> ERP
    DP <--> CVP
    DP <--> RRP
    ERP <--> RRP
    CVP <--> RRP
```

## 3. Logical Reference Architecture

```mermaid
flowchart LR
    U["Clients / Operators / Institutions / Affected Parties / AIITL Agents"]

    API["CDP Service Surface"]
    ID["Identity"]
    AT["Attestation"]
    AR["Authority Resolver"]
    PE["Policy Engine"]
    PL["Protocol Layer"]
    DK["Decision Kernel"]
    EC["Execution Control"]
    RC["Remedy Control"]
    CV["Covenant Manager"]
    RP["Repair Manager"]
    SM["State Machines"]
    RW["Record Writer"]
    LE["Learning Engine"]

    DS[("Decision Store")]
    RS[("Record Store")]
    AS[("Artifact Store")]
    TS[("Trust / Authority Store")]
    QS[("Queues / Review Routing")]
    VS[("Search / Precedent Store")]

    EX["Executors / Target Systems"]
    HR["Human / Quorum / Affected-Party Review"]
    OB["Audit / Replay / Observability"]

    U --> API
    API --> ID
    API --> AT
    API --> PL

    ID --> TS
    AT --> TS
    PL --> AR
    AR --> PE
    AR --> TS

    PL --> DK
    DK --> DS
    DK --> SM
    DK --> RW

    PL --> EC
    PL --> RC
    PL --> CV
    PL --> RP

    EC --> QS
    EC --> EX
    EC --> RW

    RC --> HR
    RC --> RP
    RC --> RW

    CV --> RW
    CV --> SM

    RP --> HR
    RP --> RW
    RP --> SM

    RW --> RS
    RW --> AS

    DS --> LE
    RS --> LE
    AS --> LE
    LE --> VS
    LE --> PE

    RS --> OB
    DS --> OB
    TS --> OB
    QS --> OB
```

## 4. Execution and Remedy Control Path

```mermaid
flowchart LR
    LEG["Legitimate Decision"]
    MG["Maturity Gate"]
    Q["Queue / Review"]
    PG["Presence Grant"]
    EX["Execute"]
    EM["Emergency Override"]
    KS["Kill Switch"]
    RB["Rollback"]
    MT["Mitigation"]
    CP["Compensation Claim"]
    RM["Remedy Determination"]
    RA["Resource Authorization"]
    RD["Remedy Delivery"]
    SR["Sufficiency Review"]
    RH["Residual Harm"]
    REC["Record"]
    LEARN["Learn"]

    LEG --> MG --> Q --> PG --> EX
    EX --> EM
    EX --> KS
    KS --> RB
    KS --> MT
    RB --> CP
    MT --> CP
    CP --> RM --> RA --> RD --> SR --> RH --> REC --> LEARN
```

## 5. Summary

These diagrams provide a source-controlled visual reading guide for CDP.

They are intentionally simple. The architecture remains governed by RFC-CDP-010 and the protocol-specific RFCs.
