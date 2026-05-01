# Lifecycle Operating Model

Canonical lifecycle for a metadata-first, AI-in-the-loop, Fabric-first data product workflow.

## MVP lifecycle order

1. Define data product
2. Setup config and environment
3. Declare source and ingest data
4. Profile source and capture metadata
5. Explore data
6. Explain transformation logic
7. Build transformation pipeline
8. AI generate DQ rules from metadata, profile, and context
9. Human review DQ rules
10. AI suggest sensitivity labels
11. Human review and governance gate
12. AI generated lineage and transformation summary
13. Handover framework pack

## Mermaid flow

```mermaid
flowchart TD
    A[1 Define data product\n(Human led)] --> B[2 Setup config and environment\n(Framework led)]
    B --> C[3 Declare source and ingest data\n(Framework led)]
    C --> D[4 Profile source and capture metadata\n(Framework led)]
    D --> E[5 Explore data\n(Human led)]
    E --> F[6 Explain transformation logic\n(Human led)]
    F --> G[7 Build transformation pipeline\n(Framework led)]
    G --> H[8 AI generate DQ rules\n(AI assisted)]
    H --> I[9 Human review DQ rules\n(Human led)]
    I --> J[10 AI suggest sensitivity labels\n(AI assisted)]
    J --> K[11 Human review and governance gate\n(Human led)]
    K --> L[12 AI generated lineage and transformation summary\n(AI assisted)]
    L --> M[13 Handover framework pack\n(Framework led)]

    D -. profile metadata .-> H
    D -. profile + context .-> J
    F -. transformation rationale .-> L
    M --> N[Handover pack includes:\nDQ, governance, lineage, profile, run summary, caveats]
```

AI proposes. Humans approve. The framework executes validations, logs artifacts, and assembles handover outputs.
