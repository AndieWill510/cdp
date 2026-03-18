flowchart TD

%% Core lifecycle
P[Propose<br/>RFC-002] --> C[Challenge<br/>RFC-003]
C --> T[Test<br/>RFC-004]
T --> A[Adjudicate<br/>RFC-005]
A --> L[Legitimize<br/>RFC-006]
L --> E[Execute<br/>RFC-007]
E --> R[Record<br/>RFC-008]
R --> N[Learn<br/>RFC-009]

%% Feedback loops
C --> P
T --> P
A --> P
N --> P

%% Nemawashi (pre-alignment)
NM[Nemawashi<br/>RFC-010] -.-> P
NM -.-> C

%% Identity & Trust
ID[Identify<br/>RFC-012] --> P
ID --> C
ID --> T
ID --> A
ID --> L
ID --> E

AT[Attest<br/>RFC-011] --> P
AT --> C
AT --> T
AT --> A
AT --> L
AT --> E
AT --> R

%% Schemas (data layer)
DS[Decision Schema<br/>RFC-013] --- P
ES[Envelope Schema<br/>RFC-014] --- P
PS[Payload Schemas<br/>RFC-015] --- P

%% APIs
GA[Governance API<br/>RFC-016] --> P
DA[Deliberation API<br/>RFC-017] --> C

%% State machines
GSM[Governance State Machine<br/>RFC-018] --> P
GSM --> A
GSM --> L

XSM[Execution State Machine<br/>RFC-019] --> E
XSM --> R
