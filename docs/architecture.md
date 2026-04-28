# Architecture Overview

## Core Architecture Positions

- **GitHub as source of truth:** code, configs, templates, docs, and version history live in GitHub.
- **Fabric as execution environment:** notebook runs, orchestration, and table writes happen in Fabric.
- **Lakehouse metadata tables as framework output:** profiling, drift, quality, lineage, and run summaries are persisted for observability.
- **Notebook template as practitioner interface:** teams use a standard notebook lifecycle with room for domain-specific logic.
- **YAML config as dataset contract:** declarative config defines expectations and controls.
- **Python package as reusable engine:** shared helpers eventually power common lifecycle steps.
- **Power BI as observability layer:** dashboards summarize run health and framework outputs.
- **AI/Copilot as assistant using exported context:** AI consumes structured run context; humans approve final outputs.

## High-level architecture

```mermaid
flowchart LR
    GH[GitHub Repository\nCode + Docs + YAML Contracts] --> FB[Microsoft Fabric\nNotebook Execution]
    PKG[Python Package\nReusable Framework Engine] --> FB
    FB --> LH[Lakehouse Data Tables]
    FB --> MH[Lakehouse Metadata Tables]
    MH --> PBI[Power BI Observability]
    MH --> AI[AI/Copilot Assistant\nContext Consumer]
    AI --> HUM[Human Review + Approval]
```

## Notebook lifecycle

```mermaid
flowchart TD
    A[1. Dataset Purpose + Steward] --> B[2. Parameters + Environment]
    B --> C[3. Source Declaration]
    C --> D[4. Source Profiling]
    D --> E[5. Drift + Incremental Safety]
    E --> F[6. EDA Notes]
    F --> G[7. Transformation Logic]
    G --> H[8. Technical Columns]
    H --> I[9. Output Write]
    I --> J[10. Output Profiling]
    J --> K[11. Data Quality Rules]
    K --> L[12. Governance Labels]
    L --> M[13. Data Contracts]
    M --> N[14. Lineage Summary]
    N --> O[15. Run Summary]
    O --> P[16. AI Context Export]
```

## Metadata outputs

```mermaid
erDiagram
    metadata_dataset_runs ||--o{ metadata_source_profiles : has
    metadata_dataset_runs ||--o{ metadata_column_profiles : has
    metadata_dataset_runs ||--o{ metadata_schema_snapshots : records
    metadata_schema_snapshots ||--o{ metadata_schema_drift_results : compared_to
    metadata_dataset_runs ||--o{ metadata_partition_snapshots : records
    metadata_partition_snapshots ||--o{ metadata_data_drift_results : compared_to
    metadata_dataset_runs ||--o{ metadata_transformation_steps : logs
    metadata_dataset_runs ||--o{ metadata_lineage : captures
    metadata_dataset_runs ||--o{ metadata_dq_results : validates
    metadata_dataset_runs ||--o{ metadata_governance_labels : tags
    metadata_dataset_runs ||--o{ metadata_contract_validation_results : checks
```
