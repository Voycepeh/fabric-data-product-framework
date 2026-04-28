# Fabric Data Product Framework

Setting up our Data to be BI & AI ready.

A reusable Microsoft Fabric notebook framework for building documented, governed, quality-checked, drift-aware, AI-ready data products.


## AI-Assisted Fabric Framework

### Framework purpose
A reusable AI-assisted Microsoft Fabric framework that helps teams onboard data products consistently, improve data quality, detect schema/data drift, enforce contracts, and generate handover documentation.

### Problem
Data projects often depend too much on senior engineers' tacit knowledge. Junior engineers need to learn Fabric, PySpark, data quality, governance, pipeline design, documentation, and domain logic all at once.

### Framework answer
Standard templates plus AI-in-the-loop workflows turn senior engineering judgement into repeatable delivery patterns.

### Tagline
**AI proposes. Humans approve. Pipelines enforce. Documentation updates automatically.**

### Delivery flow
Requirement Gathering → Data Model & Dictionary → Data Generation → Data Verification → Handover

```mermaid
flowchart LR
    A[Requirement Gathering] --> B[Data Model & Dictionary]
    B --> C[Data Generation]
    C --> D[Data Verification]
    D --> E[Handover & Operations]

    AI[AI Assistant] -.-> A
    AI -.-> B
    AI -.-> C
    AI -.-> D
    AI -.-> E

    A --> A1[Business requirements<br/>Previous reports<br/>Workflow clarification<br/>Use cases]
    B --> B1[Table registry<br/>Column dictionary<br/>Keys & relationships<br/>Sensitivity labels]
    C --> C1[Notebook templates<br/>Pipeline templates<br/>Reusable PySpark patterns]
    D --> D1[Data quality rules<br/>Schema drift checks<br/>Data drift checks<br/>Contract validation]
    E --> E1[Runbook<br/>Test plan<br/>Known limitations<br/>Support notes]

    D1 --> F[Central Validation Log]
    E1 --> G[Generated Handover Pack]

    H[Human Reviewer] --> B
    H --> D
    H --> E

    F --> I[Monitoring Dashboard]
    G --> J[Junior Engineer Onboarding]
```

## Why this exists

Data teams often rebuild the same notebook patterns for profiling, quality checks, drift monitoring, governance notes, and lineage handoffs. This framework provides a consistent starting point so teams can focus on dataset-specific logic and business meaning instead of reinventing operational scaffolding.

## Who this is for

- Python-proficient data engineers, analytics engineers, and data scientists working in Microsoft Fabric
- Teams standardizing notebook-based data product delivery
- Organizations that want governed, explainable, and reusable dataset pipelines

## What problem it solves

- Reduces repeated engineering effort across dataset pipelines
- Introduces a shared lifecycle from source declaration to run summary
- Improves traceability with structured metadata outputs
- Supports AI-readiness with curated context export after human-reviewed runs

## What the framework standardizes

- Notebook section structure and execution flow
- Dataset contract configuration patterns (YAML)
- Profiling, drift, and quality metadata outputs
- Governance and lineage logging conventions
- Run summaries and AI context packaging

## Product positioning

- **Data First before AI First**
- **GitHub is the source of truth**
- **Fabric is the execution environment**
- **Not** a full data catalog
- **Not** a replacement for Microsoft Purview
- **Not** only a data quality library
- A reusable notebook framework for turning pipelines into trusted data products

## What the framework is trying to do

```mermaid
flowchart TD
    A[Define dataset purpose and ownership] --> B[Run notebook lifecycle in Fabric]
    B --> C[Profile sources and check drift/safety]
    C --> D[Apply transformations + technical columns]
    D --> E[Profile outputs and run quality checks]
    E --> F[Apply governance labels and contracts]
    F --> G[Write lineage + run summary metadata]
    G --> H[Export AI-ready context for assisted documentation]
    H --> I[Human review and approval]
```

## What belongs in GitHub vs what belongs in Fabric

### GitHub (source of truth)

- Framework code and reusable package modules
- Notebook templates and documentation
- Dataset contracts and configuration examples
- Tests, CI definitions, and release history

### Fabric (execution environment)

- Notebook execution, scheduling, and orchestration
- Lakehouse reads/writes and runtime outputs
- Metadata table persistence for runs, drift, quality, and lineage
- Workspace-level operational monitoring

## Core lifecycle

1. Dataset purpose and steward agreement
2. Notebook parameters and environment setup
3. Source declaration
4. Source profiling
5. Schema drift, data drift, and incremental safety checks
6. EDA notes and data nuance explanation
7. Transformation pipeline
8. Technical columns and write pattern
9. Output profiling
10. Data quality rules
11. Governance labeling
12. Data contracts
13. Lineage and transformation summary
14. Run summary and AI context export

## Repository status

This repository is in an **early scaffold** stage. The initial focus is product direction, standards, and safe public templates. Core execution engines are intentionally not implemented yet.

## Public repo safety note

Do not commit real organisational data, secrets, tenant information, internal table names, production metadata, real workspace names, or screenshots containing sensitive details.

## Dataset contract validation

Dataset contracts are now schema-validated using JSON Schema before runtime logic is implemented.

```python
from fabric_data_product_framework.config import load_and_validate_dataset_contract

contract, errors = load_and_validate_dataset_contract(
    "examples/configs/sample_dataset_contract.yaml"
)

if errors:
    for error in errors:
        print(error)
else:
    print("Dataset contract is valid.")
```



## DataFrame profiling example

```python
import pandas as pd
from fabric_data_product_framework.profiling import profile_dataframe, summarize_profile

df = pd.DataFrame({
    "customer_id": [1, 2, 3],
    "email": ["a@example.com", "b@example.com", None],
    "amount": [10.5, 20.0, 30.0],
})

profile = profile_dataframe(df, dataset_name="synthetic_orders")
summary = summarize_profile(profile)
```

Validation-to-gate flow:

```mermaid
flowchart LR
    A[Dataset contract YAML] --> B[Schema validation]
    B --> C[Profiling]
    B --> D[Schema drift checks]
    B --> E[Data drift checks]
    B --> F[Governance checks]
    B --> G[DQ execution]
    C --> H[Pipeline gate]
    D --> H
    E --> H
    F --> H
    G --> H
```

## Schema drift example

```python
import pandas as pd
from fabric_data_product_framework.drift import (
    build_schema_snapshot,
    compare_schema_snapshots,
    assert_no_blocking_schema_drift,
)

baseline_df = pd.DataFrame({
    "customer_id": [1, 2],
    "order_amount": [10.0, 20.0],
})

current_df = pd.DataFrame({
    "customer_id": [1, 2],
    "order_amount": [10.0, 20.0],
    "new_status": ["paid", "pending"],
})

baseline = build_schema_snapshot(baseline_df, dataset_name="synthetic_orders", table_name="source_orders")
current = build_schema_snapshot(current_df, dataset_name="synthetic_orders", table_name="source_orders")

result = compare_schema_snapshots(baseline, current)
assert_no_blocking_schema_drift(result)
```

