# Lifecycle Operating Model

Canonical order for the MVP workflow in this metadata-first, AI-in-the-loop, Fabric-first framework.

```mermaid
flowchart TD
    A[1 Define data product\nHuman led] --> B[2 Setup config and environment\nFramework led]
    B --> C[3 Declare source and ingest data\nFramework led]
    C --> D[4 Profile source and capture metadata\nFramework led]
    D --> E[5 Explore data\nHuman led]
    E --> F[6 Explain transformation logic\nHuman led]
    F --> G[7 Build transformation pipeline\nFramework led]
    G --> H[8 AI generate DQ rules\nAI assisted]
    H --> I[9 Human review DQ rules\nHuman led]
    I --> J[10 AI suggest sensitivity labels\nAI assisted]
    J --> K[11 Human review and governance gate\nHuman led]
    K --> L[12 AI generated lineage and transformation summary\nAI assisted]
    L --> M[13 Handover framework pack\nFramework led]

    D -. source profile .-> H
    D -. profile evidence .-> J
    F -. transformation rationale .-> L
    G -. transformation summary .-> L

    M --> N[Handover includes:\nDQ, governance, lineage, profile, run summary, caveats]

    classDef human fill:#fef3c7,stroke:#92400e,color:#111827;
    classDef framework fill:#dbeafe,stroke:#1d4ed8,color:#111827;
    classDef ai fill:#dcfce7,stroke:#166534,color:#111827;

    class A,E,F,I,K human;
    class B,C,D,G,M framework;
    class H,J,L ai;
```

AI proposes. Humans approve. The framework validates, logs, and produces handover artifacts.
