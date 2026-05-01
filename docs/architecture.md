# Architecture Overview

This page describes framework components and runtime flow. For process sequencing, use the [canonical 13-step MVP lifecycle](lifecycle-operating-model.md).

## Core architecture positions

- **GitHub source of truth:** code, templates, contracts, docs, and version history are managed in GitHub.
- **Python package / wheel:** reusable framework utilities are packaged and installed into Fabric Environments.
- **Fabric notebook execution:** practitioners run the MVP notebook template with project-specific parameters.
- **Lakehouse / warehouse outputs:** transformed business outputs are written to target data stores.
- **Metadata tables:** profiling, drift, DQ, governance, lineage, and run summaries are persisted for observability and handover.
- **Dataset and pipeline contracts:** contract-first checks validate expected structure and operating rules.
- **AI/Copilot assistant:** AI consumes structured context and proposes DQ rules, labels, lineage, and documentation artifacts for human approval.

## System flow

```mermaid
flowchart LR
    GH[GitHub Repository\nCode + Docs + Contracts] --> PKG[Python Package / Wheel]
    PKG --> FAB[Microsoft Fabric\nNotebook Execution]
    FAB --> OUT[Lakehouse / Warehouse\nData Outputs]
    FAB --> META[Metadata Tables\nProfiles + Drift + DQ + Governance + Lineage + Run Summary]
    FAB --> CONTRACTS[Dataset Contracts / Pipeline Contracts\nValidation Results]
    META --> AI[AI/Copilot\nConsumes Structured Context]
    CONTRACTS --> AI
    AI --> PROP[Proposed DQ, Labels, Lineage,\nTransformation Summaries, Handover Notes]
    PROP --> HUMAN[Human Review + Approval]
    HUMAN --> HANDOVER[Handover Artifacts]
```

## Metadata model reference

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
