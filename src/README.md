# Callable Function Reference

This page lists the main callable functions intended to be imported from `fabric_data_product_framework`.

## Runtime

Functions from `src/fabric_data_product_framework/runtime.py`.

| Function | Purpose | Typical use |
|---|---|---|
| `get_current_timestamp_utc` | Return current UTC timestamp in ISO format. | Stamp runtime metadata. |
| `generate_run_id` | Build a normalized run ID with timestamp + UUID suffix. | Generate pipeline run identifiers. |
| `normalize_name` | Normalize text to lowercase underscore-safe format. | Standardize dataset/notebook names. |
| `validate_notebook_name` | Return notebook naming violations as a list of messages. | Pre-check notebook naming conventions. |
| `assert_notebook_name_valid` | Raise if notebook naming is invalid. | Enforce naming in orchestration checks. |
| `build_runtime_context` | Build a JSON-safe runtime context dictionary. | Pass runtime details between notebook steps. |

```python
from fabric_data_product_framework.runtime import generate_run_id, build_runtime_context

run_id = generate_run_id("ingest")
ctx = build_runtime_context(
    dataset_name="orders",
    environment="dev",
    source_table="bronze.orders_raw",
    target_table="silver.orders",
    run_id=run_id,
)
```

## Config

Functions from `src/fabric_data_product_framework/config.py`.

| Function | Purpose | Typical use |
|---|---|---|
| `load_dataset_contract` | Load a dataset contract YAML file to a Python dictionary. | Read contract files before validation. |
| `validate_dataset_contract` | Validate contract content against the JSON schema and return errors. | Collect validation errors for reporting. |
| `assert_valid_dataset_contract` | Validate contract content and raise on failure. | Fail fast in pipeline entry checks. |
| `load_and_validate_dataset_contract` | Load + validate contract in one call; returns `(contract, errors)`. | One-step contract load/validation in notebooks or tests. |

```python
from fabric_data_product_framework.config import load_and_validate_dataset_contract

contract, errors = load_and_validate_dataset_contract("examples/configs/sample_dataset_contract.yaml")
```

## Profiling

Functions from `src/fabric_data_product_framework/profiling.py`.

| Function | Purpose | Typical use |
|---|---|---|
| `to_jsonable` | Convert values/structures to JSON-safe primitives. | Prepare profile or metadata outputs for serialization. |
| `infer_semantic_type` | Infer lightweight semantic type labels from column name/sample values. | Add semantic hints in profile outputs. |
| `profile_column` | Profile one pandas series. | Column-level diagnostics. |
| `profile_dataframe` | Profile a pandas or Spark dataframe. | Baseline source/output table profiling. |
| `flatten_profile_for_metadata` | Flatten profile output into metadata record rows. | Persist profile results in metadata tables/files. |
| `summarize_profile` | Create a compact high-level profile summary. | Build quick observability summaries. |

## Drift and incremental safety

Functions from `src/fabric_data_product_framework/drift.py` and `src/fabric_data_product_framework/incremental.py`.

| Function | Purpose | Typical use |
|---|---|---|
| `default_schema_drift_policy` | Return default drift policy settings. | Bootstrap drift checks with standard policy. |
| `detect_dataframe_engine` | Detect pandas vs Spark dataframe engine. | Auto-select engine behavior. |
| `build_schema_snapshot` | Build schema snapshot from a dataframe. | Capture baseline/current schema state. |
| `compare_schema_snapshots` | Compare baseline vs current schema snapshots. | Produce drift result (blocking/warning changes). |
| `assert_no_blocking_schema_drift` | Raise when schema comparison has blocking drift. | Gate transform/load steps. |
| `default_incremental_safety_policy` | Return default incremental safety policy settings. | Standardize incremental guardrails. |
| `build_partition_snapshot` | Build per-partition incremental snapshots. | Capture baseline/current partition state. |
| `compare_partition_snapshots` | Compare baseline/current partition snapshots. | Detect unsafe incremental changes. |
| `assert_incremental_safe` | Raise when incremental safety check fails. | Block unsafe writes. |
| `build_incremental_safety_records` | Flatten incremental comparison into record rows. | Persist safety results in metadata sinks. |

## Quality

Functions from `src/fabric_data_product_framework/quality.py`.

| Function | Purpose | Typical use |
|---|---|---|
| `run_quality_rules` | Execute supported data quality rules on pandas/Spark dataframes. | Evaluate quality before publish/load. |
| `assert_quality_gate` | Raise when quality result breaches configured fail threshold. | Enforce pass/fail quality gate. |
| `build_quality_result_records` | Flatten quality result payload into metadata record rows. | Persist quality outcomes for audits/dashboards. |

## Technical columns

Functions from `src/fabric_data_product_framework/technical_columns.py`.

| Function | Purpose | Typical use |
|---|---|---|
| `default_technical_columns` | Return framework technical column names. | Exclude technical fields from profiling/hash inputs. |
| `add_literal_column` | Add a constant-value column. | Add static metadata columns. |
| `add_pipeline_run_id` | Add pipeline run identifier column. | Stamp each row with run ID. |
| `add_pipeline_metadata` | Add run/pipeline/environment metadata columns. | Apply pipeline-level technical metadata. |
| `add_source_metadata` | Add source system/table/extract metadata columns. | Preserve source lineage attributes. |
| `add_loaded_at` | Add load timestamp column. | Audit ingestion/persistence time. |
| `add_watermark_value` | Copy watermark source column to standard technical column. | Keep incremental watermark in standard field. |
| `add_row_hash` | Add row-level SHA256 hash. | Change detection for row payloads. |
| `add_business_key_hash` | Add SHA256 hash from business key columns. | Incremental safety and dedupe support. |
| `add_datetime_parts` | Derive date/time helper columns from datetime input. | Build partitioning/reporting helper fields. |
| `add_standard_technical_columns` | Apply standard technical column bundle. | One-call technical enrichment before writes. |

## Runtime contract enforcement and run summary

Functions from `src/fabric_data_product_framework/contracts.py` and `src/fabric_data_product_framework/run_summary.py`.

| Function | Purpose | Typical use |
|---|---|---|
| `validate_runtime_contracts` | Validate runtime source/output data against upstream/downstream contract expectations. | Run after quality checks and before writing output. |
| `assert_contracts_valid` | Raise if runtime contract validation contains blocking errors. | Enforce fail-fast contract gate in notebook pipelines. |
| `build_contract_validation_records` | Flatten contract validation results into metadata-ready records. | Persist contract outcomes for audit and reporting. |
| `build_run_summary` | Build an execution summary payload from runtime context and optional check results. | Create concise handover summary after pipeline checks. |
| `render_run_summary_markdown` | Render a human-readable markdown summary from run summary payload. | Print notebook-friendly handover output. |
| `build_run_summary_record` | Flatten run summary to a single metadata-ready record. | Write summary to metadata tables/files. |

```python
from fabric_data_product_framework.contracts import (
    validate_runtime_contracts,
    assert_contracts_valid,
    build_contract_validation_records,
)
from fabric_data_product_framework.run_summary import (
    build_run_summary,
    render_run_summary_markdown,
    build_run_summary_record,
)

contract_result = validate_runtime_contracts(
    source_df=df_source,
    output_df=df_output,
    contract=contract,
    engine="auto",
)
assert_contracts_valid(contract_result)
contract_records = build_contract_validation_records(contract_result, run_id=ctx["run_id"])

summary = build_run_summary(
    runtime_context=ctx,
    contract=contract,
    source_profile=source_profile,
    output_profile=output_profile,
    quality_result=quality_result,
    contract_validation_result=contract_result,
)
print(render_run_summary_markdown(summary))
summary_record = build_run_summary_record(summary)
```


## Lineage

Functions and classes from `src/fabric_data_product_framework/lineage.py`.

| Function/Class | Purpose | Typical use |
|---|---|---|
| `TransformationStep` | Structured shape for a recorded transformation step. | Keep per-step lineage fields consistent and JSON-safe. |
| `LineageRecorder` | Notebook-friendly recorder for notable transformations. | Add steps during transformation logic and build summary outputs. |
| `build_lineage_records` | Flatten transformation steps into metadata-ready rows. | Persist lineage step records to metadata tables/files. |
| `generate_mermaid_lineage` | Build a Mermaid flowchart from sources, steps, and target. | Render quick lineage diagrams in handover docs/notebooks. |
| `build_transformation_summary_markdown` | Render concise markdown summary of transformations and business impact. | Print handover-friendly run lineage summaries. |
| `build_lineage_prompt_context` | Build prompt-ready markdown context for lineage review (no AI call). | Pass context to Copilot/AI tools while constraining invented details. |

```python
from fabric_data_product_framework.lineage import (
    LineageRecorder,
    build_transformation_summary_markdown,
)

lineage = LineageRecorder(
    dataset_name=ctx["dataset_name"],
    run_id=ctx["run_id"],
    source_tables=[ctx["source_table"]],
    target_table=ctx["target_table"],
)

lineage.add_step(
    step_id="T001",
    step_name="Apply business filter",
    input_name="df_source",
    output_name="df_filtered",
    description="Filter to records needed for reporting.",
    reason="The product table should only contain approved reporting records.",
    transformation_type="filter",
)

summary = lineage.build_summary()
print(build_transformation_summary_markdown(summary))
```

## Scaffold modules

These modules exist to reserve the framework structure, but do not expose public callable functions yet:

| Module | Planned purpose |
|---|---|
| `contracts.py` | Future contract-specific helpers |
| `governance.py` | Future governance label helpers |
| `ai_context.py` | Future AI context export helpers |

## Fabric adapters

Functions from `src/fabric_data_product_framework/fabric.py`.

| Function | Purpose | Typical use |
|---|---|---|
| `build_table_identifier` | Build `table`, `schema.table`, or `lakehouse.schema.table` identifiers. | Prepare table identifiers for read/write wrappers. |
| `read_table` | Read using an injected Fabric-compatible reader function. | Keep framework runtime-agnostic while integrating notebook readers. |
| `validate_write_mode` | Validate/normalize write mode (`append`, `overwrite`, `merge`). | Pre-check mode before writes. |
| `write_table` | Write using an injected Fabric-compatible writer function. | Keep framework runtime-agnostic while integrating notebook writers. |

## Source layout

This repository uses the standard Python `src/` layout.
All importable framework code lives in:

`src/fabric_data_product_framework/`

The main project overview is in the root `README.md`.
