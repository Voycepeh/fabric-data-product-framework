# Callable Function Reference

This page explains the main callable functions exposed by `fabric_data_product_framework`.
Read the root `README.md` and Fabric notebook template docs first.
This page is organized around how functions are typically chained in notebook workflows.
Detailed function-level documentation is progressively being standardized in docstrings and mirrored in `docs/api/` via the MkDocs-generated API reference site.

## Typical notebook chaining order

1. Runtime/config (`runtime.py`, `config.py`)
2. Source read and adapters (`fabric.py`, notebook readers)
3. Profiling (`profiling.py`)
4. DQ candidate generation/review/execution (`dq.py`, `quality.py`)
5. Drift and incremental safety (`drift.py`, `incremental.py`, `drift_checkers.py`)
6. Governance classification (`governance_classifier.py`)
7. Transformation and technical columns (`technical_columns.py`)
8. Lineage and transformation summary (`lineage.py`)
9. Run summary / handover (`run_summary.py`, `contracts.py`)
10. Contract-first one-call execution (`data_contract.py`)

## Execution scope quick reference

| Area | Local-safe | Fabric runtime required |
|---|---|---|
| Contract/config/runtime helpers | Yes | No |
| Profiling/quality/drift logic | Yes (small pandas samples) | Optional for Spark-scale runs |
| Fabric adapters (`fabric.py`) | Validation wrappers only | Yes for real Lakehouse IO |
| Metadata table writes | Optional with custom writer | Yes for Spark table sinks |

## Workflow-stage grouped function reference

### Runtime and config

| Function | What it does | Use when | Typical next step |
|---|---|---|---|
| `generate_run_id` | Builds normalized run IDs. | Starting a notebook run. | `build_runtime_context` |
| `build_runtime_context` | Creates JSON-safe runtime context. | Passing run metadata across steps. | Source read and profiling |
| `load_dataset_contract` | Loads YAML contract from disk. | Contract-first execution. | `validate_dataset_contract` |
| `load_and_validate_dataset_contract` | One-call load + validation. | Notebook entrypoint checks. | DQ/drift/contract gates |

### Fabric adapters and source access

| Function | What it does | Use when | Typical next step |
|---|---|---|---|
| `build_table_identifier` | Composes table identifier safely. | Building read/write target names. | `read_table` / `write_table` |
| `read_table` | Invokes injected table reader. | Notebook-specific Fabric table reads. | Profiling |
| `write_table` | Invokes injected table writer. | Persisting transformed outputs. | Run summary |

### Profiling

| Function | What it does | Use when | Typical next step |
|---|---|---|---|
| `profile_dataframe` | Profiles pandas or Spark dataframe. | Baseline source/output shape checks. | DQ candidate generation |
| `flatten_profile_for_metadata` | Flattens profile for metadata writes. | Storing profile records in tables/files. | Drift or governance checks |
| `summarize_profile` | Returns compact profile summary. | Quick notebook handover view. | Run summary |

### DQ candidate generation and execution

| Function | What it does | Use when | Typical next step |
|---|---|---|---|
| `generate_dq_rule_candidates` | Creates conservative candidate rules. | Bootstrapping DQ from profile data. | Human review / approval |
| `run_dq_rules` | Executes normalized DQ rules. | Running approved rules directly. | `assert_quality_gate` |
| `run_dq_workflow` | Runs end-to-end contract DQ flow. | Contract-driven notebook orchestration. | Drift / contracts validation |
| `run_quality_rules` | Evaluates core quality rules. | Quality checks without rule-store workflow. | `build_quality_result_records` |

### Drift and incremental safety

| Function | What it does | Use when | Typical next step |
|---|---|---|---|
| `check_schema_drift` | Compares current schema to baseline. | Pre-write schema safety gate. | `summarize_drift_results` |
| `check_partition_drift` | Compares partition snapshot changes. | Incremental safety checks. | `assert_incremental_safe` |
| `summarize_drift_results` | Combines drift outcomes to one status. | Notebook gating decision. | Governance / output write |

### Governance classification

| Function | What it does | Use when | Typical next step |
|---|---|---|---|
| `classify_columns` | Suggests governance classes by profile. | Sensitive-data review step. | `write_governance_classifications` |
| `summarize_governance_classifications` | Returns compact class/action counts. | Handover and audit summaries. | Run summary |

### Transformation support and technical columns

| Function | What it does | Use when | Typical next step |
|---|---|---|---|
| `add_standard_technical_columns` | Adds default framework technical metadata columns. | Before writing output datasets. | Lineage + write step |
| `add_business_key_hash` | Adds deterministic business key hash. | Incremental dedupe/change detection. | Contract/runtime validation |

### Lineage and summaries

| Function | What it does | Use when | Typical next step |
|---|---|---|---|
| `LineageRecorder` | Captures notebook transformation steps. | Tracking notable transformations. | `build_lineage_records` |
| `build_transformation_summary_markdown` | Renders concise lineage summary markdown. | Notebook handover section. | Run summary |

### Run summary and contract validation

| Function | What it does | Use when | Typical next step |
|---|---|---|---|
| `validate_runtime_contracts` | Checks source/output against contract expectations. | Pre-publish gate in notebook flow. | `assert_contracts_valid` |
| `build_run_summary` | Builds overall run outcome payload. | Final handover status generation. | `render_run_summary_markdown` |
| `build_run_summary_record` | Flattens run summary for metadata sink. | Persisting run-level audit record. | End of run |

### Contract-first orchestration

| Function | What it does | Use when | Typical next step |
|---|---|---|---|
| `run_data_product` | Executes contract-driven end-to-end workflow. | One-call orchestration path. | Review run summary + records |
| `normalize_data_product_contract` | Normalizes raw contract dictionaries into the typed contract object. | Pre-validating or inspecting contract structure before execution. | `run_data_product` |

### Template generation

| Function | What it does | Use when | Typical next step |
|---|---|---|---|
| `create_pipeline_notebook_template` | Produces a pipeline-oriented starter notebook template. | Bootstrapping standard pipeline notebook scaffolding. | Fill dataset-specific logic |
| `create_actual_data_mvp_template` | Produces an actual-data MVP notebook template. | Bootstrapping MVP-style Fabric notebook flows. | Connect source/target specifics and run checks |

## Minimal recipes

### Local smoke path

```python
from fabric_data_product_framework.runtime import build_runtime_context
from fabric_data_product_framework.profiling import profile_dataframe

ctx = build_runtime_context("orders", "local", "raw.orders", "silver.orders")
profile = profile_dataframe(df, dataset_name=ctx["dataset_name"], engine="pandas")
```

### Fabric dry-run path

```python
from fabric_data_product_framework.config import load_and_validate_dataset_contract

contract, errors = load_and_validate_dataset_contract("examples/configs/sample_dataset_contract.yaml")
if errors:
    raise ValueError(errors)
```

### Manual notebook path

```python
quality_result = run_quality_rules(df_output, rules=rules, engine="auto")
schema_result = check_schema_drift(df_output, dataset_name="orders", table_name="silver.orders")
summary = build_run_summary(runtime_context=ctx, quality_result=quality_result, schema_drift_result=schema_result)
```

### Contract-first one-call path

```python
from fabric_data_product_framework.data_contract import run_data_product
from fabric_data_product_framework.config import load_dataset_contract

contract = load_dataset_contract("examples/configs/sample_dataset_contract.yaml")
result = run_data_product(
    spark=spark,
    contract=contract,
    source_df=df,  # optional injection for controlled notebook/test runs
    write_target=False,  # optional dry-run behavior
    write_metadata=False,
)
print(result["run_summary"]["overall_status"])
```

## Advanced / legacy notes

- Use Fabric AI-assisted DQ candidate generation only when Fabric Runtime AI dependencies are available.
- Keep generated candidates in review-only mode until explicitly approved.
- The improved docstrings in core callable modules are intentionally structured to support future lightweight API doc generation.
