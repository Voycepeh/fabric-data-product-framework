# Fabric Data Product Framework

## What this is
A reusable Microsoft Fabric notebook framework for turning raw or source data into governed, quality-checked, handover-ready data products.

It abstracts the repeatable 80% of pipeline work so teams can focus on the dataset-specific 20%: business meaning, transformation logic, and data nuance.

## Why this exists
This framework is designed to make Fabric data products easier to:
- build
- review
- govern
- operate
- hand over

It is especially intended for teams where people may know Python or data analysis, but may not yet know Fabric engineering best practices.

## Operating model

| Actor | Owns |
|---|---|
| Functional People | Purpose, definitions, usage, caveats, governance approval, handover acceptance |
| Technical People | Source declaration, EDA, transformation logic, contracts, DQ rules, exception review |
| AI | Drafting, summarising, recommending, explaining, candidate rules, lineage and handover narrative |
| Framework | Profiling, metadata logging, drift checks, DQ execution, validation, write pattern, handover export |

Functional people define meaning. Technical people turn meaning into data products. AI accelerates documentation and reasoning. The framework makes the process repeatable, validated, and handover-ready.

## Lifecycle at a glance

| Step | Stage | Primary actor | Where it happens |
|---:|---|---|---|
| 1 | Dataset purpose and steward agreement | Functional People | Governance doc / metadata table |
| 2 | Business metadata entry | Functional People | Metadata table / form |
| 3 | Governance labeling and usage controls | Functional People | Governance doc / metadata table |
| 4 | Data contract draft | Technical People | Contract file / notebook |
| 5 | Notebook parameters and source declaration | Technical People | Main pipeline notebook |
| 6 | Source profiling | Framework | Profiling notebook / utility |
| 7 | Source metadata logging | Framework | Metadata table |
| 8 | EDA notes and data nuance explanation | Technical People | Separate EDA notebook |
| 9 | Schema drift, data drift, and incremental safety checks | Framework | Checks notebook / reusable gate |
| 10 | Transformation pipeline | Technical People | Main pipeline notebook |
| 11 | Technical columns and write pattern | Framework | Main pipeline notebook |
| 12 | Output profiling | Framework | Profiling utility / metadata table |
| 13 | DQ rules and contract validation | Technical People + Framework | Checks notebook / pipeline gate |
| 14 | Lineage and transformation summary | Framework + AI + Technical People | Handover notebook |
| 15 | Handover package and AI context export | Framework + AI, accepted by Functional People | Handover notebook |

## Quick start
1. Define purpose, steward, usage, and business metadata.
2. Draft governance labels and data contract expectations.
3. Configure the notebook parameters and declared sources.
4. Run source profiling and metadata logging.
5. Complete the separate EDA notes notebook.
6. Build the transformation pipeline.
7. Run drift, incremental, DQ, and contract checks.
8. Export lineage, run summary, AI context, and handover package.

## More documentation
- [Lifecycle operating model](docs/lifecycle-operating-model.md)
- [Notebook structure](docs/notebook-structure.md)
- [AI in the loop](docs/ai-in-the-loop.md)
- [Functional responsibilities](docs/functional-responsibilities.md)
- [Technical responsibilities](docs/technical-responsibilities.md)
- [Framework responsibilities](docs/framework-responsibilities.md)
- [Handover package](docs/handover-package.md)
A reusable Microsoft Fabric notebook framework for turning raw data into documented, quality-checked, governed, AI-ready data products.

## What this framework is for

This framework helps Python-proficient data practitioners deliver consistent Fabric data products without first mastering every Fabric engineering best practice. It provides a practical notebook lifecycle, reusable templates, and metadata outputs that support onboarding, review, and handover.

## Core idea

**AI proposes. Humans approve. Pipelines enforce. Documentation updates automatically.**

## Core lifecycle

Use this lifecycle as the default operating model for each dataset.

| Step | Lifecycle stage | Purpose | Current support |
|---|---|---|---|
| 1 | Dataset purpose and steward agreement | Define business purpose, scope, steward, and expected usage. | Notebook template section; human-authored, AI-assisted. |
| 2 | Notebook parameters and environment setup | Set runtime parameters, paths, target tables, and execution mode. | Fabric notebook setup pattern with parameters, paths, runtime imports, and naming convention check. |
| 3 | Source declaration | Register declared sources, keys, refresh expectations, and ingestion intent. | Source table and lakehouse variables; source registry is planned. |
| 4 | Source profiling | Profile input shape, nulls, distributions, and basic quality indicators. | Implemented profiling utility and Fabric metadata logging pattern. |
| 5 | Schema drift, data drift, and incremental safety checks | Compare current vs baseline structure and behavior before transforms; verify incremental boundaries. | Schema drift and incremental safety utilities implemented. Data drift checks planned. |
| 6 | EDA notes and data nuance explanation | Capture observed quirks, caveats, and business-relevant interpretation notes. | Notebook documentation pattern. Findings are frozen after development so they do not become recurring pipeline logic. |
| 7 | Transformation pipeline | Apply business logic from raw/bronze to curated outputs with reproducible steps. | Notebook section pattern for dataset-specific business logic designed to run end-to-end. |
| 8 | Technical columns and write pattern | Apply audit columns, watermark/version columns, partition/write rules, and persistence pattern. | Fabric notebook pattern for audit columns, datetime standardization, and lakehouse writes. |
| 9 | Output profiling | Re-profile final output to confirm expected shape and characteristics. | Implemented profiling utility and Fabric output metadata logging pattern. |
| 10 | Data quality rules | Run required checks (completeness, validity, consistency, thresholds) and capture pass/fail details. | Planned rule execution and pipeline gate. |
| 11 | Governance labeling | Apply sensitivity/classification labels and usage controls in documented form. | Planned governance metadata and label validation. |
| 12 | Data contracts | Validate and publish dataset contract expectations for schema, semantics, and constraints. | Contract schema validation implemented. Runtime enforcement planned. |
| 13 | Lineage and transformation summary | Record lineage and summarize how each output is derived. | AI-assisted lineage prompt/template proven. Automated extraction planned. |
| 14 | Run summary and AI context export | Produce run summary and package curated context for assisted documentation and handover. | Planned handover package. |
| 15 | Business metadata layer | Capture business definitions, metric meaning, known caveats, owner notes, and usage examples so the data product is understandable after handover. | Planned handover artefact; AI-assisted drafting with human steward review. |

## Lifecycle ownership model

The framework separates lifecycle work into five teachable streams:

- **Governance documents**
- **Pipeline engineering artefacts**
- **Automated checks**
- **Human data understanding**
- **Handover documents**

This helps teams see who owns decisions, where AI helps, and what the framework automates.

## AI in the loop, human accountable

The framework uses AI in the loop to reduce documentation and metadata burden, but accountability remains with humans. AI can draft, summarize, recommend, and explain. Humans approve purpose, business rules, governance decisions, data contracts, and business meaning. The framework then makes the approved decisions executable through repeatable profiling, validation, logging, and pipeline gates.

## Human, AI, and framework responsibilities

```mermaid
flowchart TD

subgraph G["Governance / Data Ownership"]
    G1["1. Dataset purpose and steward agreement<br/><br/>Human accountable<br/>AI assisted drafting<br/>Output: approved purpose, scope, usage, owner, steward"]
    G11["11. Governance labeling<br/><br/>Human accountable<br/>AI can recommend labels<br/>Output: sensitivity label, classification, usage controls"]
    G12["12. Data contracts<br/><br/>Human accountable, engineering enforced<br/>AI can draft contract expectations<br/>Output: schema, semantics, constraints, refresh expectations"]
end

subgraph E["Pipeline Engineering / Transformation Implementation"]
    E2["2. Notebook parameters and environment setup<br/><br/>Framework automated<br/>Human configures dataset-specific values<br/>Output: parameters, paths, imports, naming checks"]
    E3["3. Source declaration<br/><br/>Human declares source intent<br/>Framework records metadata<br/>Output: sources, keys, refresh pattern, ingestion intent"]
    E4["4. Source profiling<br/><br/>Framework automated<br/>AI can summarize profile<br/>Output: input profile metadata"]
    E7["7. Transformation pipeline<br/><br/>Human authors business logic<br/>AI can explain and refactor<br/>Output: reproducible transformation code"]
    E8["8. Technical columns and write pattern<br/><br/>Framework automated<br/>Human selects write mode where needed<br/>Output: audit columns, partitions, watermark/version fields"]
    E9["9. Output profiling<br/><br/>Framework automated<br/>AI can summarize output changes<br/>Output: output profile metadata"]
end

subgraph C["Automated Checks / Pipeline Gates"]
    C5["5. Schema drift, data drift, and incremental safety checks<br/><br/>Framework automated gate<br/>Human reviews exceptions<br/>Output: pass/fail drift and incremental safety result"]
    C10["10. Data quality rules<br/><br/>Framework executes checks<br/>Human approves rules<br/>AI can suggest candidate rules<br/>Output: completeness, validity, consistency, threshold results"]
end

subgraph H["Human Data Understanding"]
    H6["6. EDA notes and data nuance explanation<br/><br/>Human owned<br/>AI assisted summarisation<br/>Output: frozen quirks, caveats, assumptions, and transformation rationale"]
end

subgraph O["Handover / Operational Readiness"]
    O13["13. Lineage and transformation summary<br/><br/>Framework captures lineage<br/>AI drafts explanation<br/>Human reviews<br/>Output: source-to-output lineage and transformation explanation"]
    O14["14. Run summary and AI context export<br/><br/>Framework packages run metadata<br/>AI prepares context<br/>Output: run summary, profile summary, quality results, contract status, governance status"]
    O15["15. Business metadata layer<br/><br/>Human accountable<br/>AI can draft definitions<br/>Output: business definitions, metric meaning, owner notes, known caveats, usage examples"]
end

G1 --> E2
E2 --> E3
E3 --> E4
E4 --> C5
C5 --> H6
H6 --> E7
E7 --> E8
E8 --> E9
E9 --> C10
C10 --> G11
G11 --> G12
G12 --> O13
O13 --> O14
O14 --> O15

C5 -. "If drift or incremental risk found" .-> H6
C10 -. "If quality rule fails" .-> H6
G12 -. "If contract expectation changes" .-> E3
O15 -. "If handover exposes missing context" .-> H6
```

## Responsibility matrix

| Stream | Steps | Human responsibility | AI responsibility | Framework responsibility | Main artefacts |
|---|---:|---|---|---|---|
| Governance / data ownership | 1, 11, 12 | Approve purpose, usage, steward, labels, contracts | Draft purpose, suggest labels, draft contract expectations | Store and validate metadata | Purpose agreement, labels, data contract |
| Pipeline engineering / transformation | 2, 3, 4, 7, 8, 9 | Configure dataset-specific values and author business logic | Explain/refactor logic, summarize profiling | Run setup, profiling, technical columns, write pattern | Notebook config, source registry, profiles, transformation code |
| Automated checks / gates | 5, 10 | Approve exceptions and thresholds | Suggest candidate checks and explain failures | Execute drift, incremental, and DQ gates | Check results, pass/fail logs |
| Human data understanding | 6 | Interpret data nuances and business caveats | Summarize findings and convert notes into documentation | Preserve notes as non-runtime documentation | EDA notes, assumptions, caveats |
| Handover / operational readiness | 13, 14, 15 | Review and accept handover context | Generate lineage narrative, run summary, business metadata drafts | Export run context and metadata package | Lineage, run summary, AI context export, business metadata layer |

## What the framework currently standardizes or supports

### Implemented in this repo

1. Dataset contract schema validation
2. DataFrame profiling utility
3. Schema snapshot and schema drift comparison
4. Engine-aware dataframe API pattern for pandas, Spark, and auto mode
5. Safe public examples and documentation structure

### Proven in the Fabric notebook pattern

1. Dataset purpose and approved usage section
2. Notebook parameters and environment setup
3. Naming convention check
4. Source table declaration
5. Source profiling written to metadata table
6. EDA notes and frozen data nuance explanation
7. Core transformation section designed for run-all execution
8. Technical audit columns
9. Datetime standardization such as timezone conversion, date, time, and time block columns
10. Lakehouse write pattern
11. Output profiling written to metadata table
12. AI-assisted lineage prompt/template

### Planned next

1. Data drift checks
2. Incremental partition safety checks
3. Data quality rule execution
4. Governance labeling checks
5. Runtime data contract enforcement
6. Automated lineage summary
7. Run summary
8. AI context export

## What belongs in GitHub vs Fabric

### GitHub (source of truth)

- Templates and reusable framework code
- Contracts, examples, tests, and documentation
- Review history and change control

### Fabric (execution environment)

- Notebook and pipeline execution
- Lakehouse reads/writes and operational runs
- Metadata tables, monitoring, and runtime outputs

## Repository status

This repository is in an **early scaffold** stage. The current focus is standards, lifecycle consistency, and safe public templates.

## Public repo safety note

Do not commit real organisational data, secrets, tenant details, internal table names, workspace names, screenshots, or production metadata.

## Short examples

For deeper examples, see [docs/architecture.md](docs/architecture.md), [docs/schema-drift.md](docs/schema-drift.md), and [docs/metadata-model.md](docs/metadata-model.md).

### Contract validation

```python
from fabric_data_product_framework.config import load_and_validate_dataset_contract

contract, errors = load_and_validate_dataset_contract(
    "examples/configs/sample_dataset_contract.yaml"
)
```

### DataFrame profiling

```python
import pandas as pd
from fabric_data_product_framework.profiling import (
    flatten_profile_for_metadata,
    profile_dataframe,
)

df = pd.DataFrame({"customer_id": [1, 2, 3], "amount": [10.5, 20.0, 30.0]})
profile = profile_dataframe(df, dataset_name="synthetic_orders")

source_profile = profile_dataframe(df_source, dataset_name="synthetic_orders", engine="spark")
profile_rows = flatten_profile_for_metadata(
    source_profile,
    table_name="source.synthetic_orders",
    run_id=ctx["run_id"],
    table_stage="source",
)
```


### Technical columns

```python
from fabric_data_product_framework.technical_columns import add_standard_technical_columns

df_output = add_standard_technical_columns(
    df_output,
    run_id=ctx["run_id"],
    environment=ctx["environment"],
    source_table=ctx["source_table"],
    watermark_column="updated_at",
    business_keys=["customer_id"],
    engine="spark",
)
```

### Schema drift check

```python
from fabric_data_product_framework.drift import compare_schema_snapshots

result = compare_schema_snapshots(baseline_snapshot, current_snapshot)
```

### Incremental safety check

```python
from fabric_data_product_framework.incremental import (
    assert_incremental_safe,
    build_partition_snapshot,
    compare_partition_snapshots,
)

current_partition_snapshots = build_partition_snapshot(
    df_source,
    dataset_name="synthetic_orders",
    table_name="source.synthetic_orders",
    partition_column="business_date",
    business_keys=["customer_id", "order_id"],
    watermark_column="updated_at",
    engine="spark",
)

safety_result = compare_partition_snapshots(
    previous_partition_snapshots,
    current_partition_snapshots,
)

assert_incremental_safe(safety_result)
```

### Data quality gate

```python
from fabric_data_product_framework.quality import (
    assert_quality_gate,
    run_quality_rules,
)

quality_result = run_quality_rules(
    df_output,
    contract.get("quality_rules", []),
    dataset_name=ctx["dataset_name"],
    table_name=ctx["target_table"],
    engine="spark",
)

assert_quality_gate(quality_result)
```

### Notebook runtime helper

```python
from fabric_data_product_framework.runtime import (
    build_runtime_context,
    assert_notebook_name_valid,
)

ctx = build_runtime_context(
    dataset_name="synthetic_orders",
    environment="dev",
    source_table="source.synthetic_orders",
    target_table="product.synthetic_orders",
    notebook_name="source_to_product_synthetic_orders",
)

assert_notebook_name_valid(
    ctx["notebook_name"],
    allowed_prefixes=["source_to_product_", "bronze_to_silver_", "silver_to_gold_"],
)
```

## Execution engines

The framework exposes engine-aware dataframe APIs with `engine="auto" | "pandas" | "spark"`.

- **pandas**: local and synthetic workloads
- **spark**: Fabric/lakehouse-scale workloads
- **auto**: runtime engine detection

See [docs/engine-model.md](docs/engine-model.md) for engine behavior and API usage.

## First runnable notebook MVP

After PR 14, you can copy `templates/notebooks/fabric_data_product_mvp.py` into a Fabric notebook to run a full MVP flow from contract validation to metadata outputs.

Wire only three adapters to start testing in your environment:

- `fabric_reader`
- `fabric_table_writer`
- `metadata_writer`

The template is intentionally adapter-based and does not depend on a specific workspace setup or Fabric-only SDK imports.

## Callable Function Reference
See [src/README.md](src/README.md) for callable API references.
