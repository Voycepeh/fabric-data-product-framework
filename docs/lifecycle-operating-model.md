# Lifecycle Operating Model

This page defines the single end-to-end workflow for FabricOps Starter Kit.

## Operating roles

- **Human-led steps** define intent, approve business thresholds, and make release decisions.
- **Framework-assisted deterministic checks** execute reusable validation, profiling, drift, and metadata routines.
- **AI-assisted steps** propose rule candidates, summaries, and classifications that humans review.

## 13-step end-to-end workflow

```mermaid
flowchart TD
    A[1 Define data product intent\nHuman-led] --> B[2 Configure runtime and environment\nFramework-assisted]
    B --> C[3 Declare and read source data\nFramework-assisted]
    C --> D[4 Profile source metadata\nFramework-assisted]
    D --> E[5 Generate/define quality checks\nAI-assisted + Human-led]
    E --> F[6 Review quality and governance intent\nHuman-led]
    F --> G[7 Apply quality checks\nFramework-assisted]
    G --> H[8 Detect schema/profile/partition drift\nFramework-assisted]
    H --> I[9 Execute transformations\nHuman-led + Framework-assisted]
    I --> J[10 Add technical columns and write prep\nFramework-assisted]
    J --> K[11 Write outputs and profile outputs\nFramework-assisted]
    K --> L[12 Generate governance metadata and lineage\nAI-assisted + Framework-assisted]
    L --> M[13 Produce handover and final validation\nHuman-led + Framework-assisted]

    classDef human fill:#fef3c7,stroke:#92400e,color:#111827;
    classDef framework fill:#dbeafe,stroke:#1d4ed8,color:#111827;
    classDef ai fill:#dcfce7,stroke:#166534,color:#111827;

    class A,F,I,M human;
    class B,C,D,G,H,J,K framework;
    class E,L ai;
```

## Practical use

Use [Quick Start](quick-start.md) to execute the workflow and [Reference](reference/index.md) to locate callable functions by step.
