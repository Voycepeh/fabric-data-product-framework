# Callable Function Reference

This page lists the main callable functions intended to be imported from `fabric_data_product_framework`.


## Execution scope quick reference

| Area | Local safe | Fabric runtime required |
|---|---|---|
| Contract/config/runtime helpers | Yes | No |
| Profiling/quality/drift logic | Yes (pandas/samples) | Optional for Spark-scale validation |
| Fabric adapters (`fabric.py`) | Adapter validation only | Yes (actual Lakehouse IO) |
| AI helper modules | Yes (prompt/parse/compile) | Yes for real Fabric AI calls |

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
| `write_profile_metadata_rows` | Write flattened profile rows to Spark metadata tables via JSON normalization. | Fabric-safe profile metadata writes without manual schema handling. |
| `profile_and_write_metadata` | Profile a dataframe and write metadata in one call. | Simplify source/output profiling notebooks. |
| `profile_table_and_write_metadata` | Read a table, profile it, and write metadata in one call. | One-call Fabric smoke-test profiling flow. |
| `summarize_profile` | Create a compact high-level profile summary. | Build quick observability summaries. |

`write_profile_metadata_rows`, `profile_and_write_metadata`, and `profile_table_and_write_metadata` are Spark/Fabric convenience helpers for `saveAsTable` metadata sinks. For generic/custom sinks, use `metadata.write_metadata_records` with an injected writer adapter.

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

## Contract-driven DQ workflow

Functions from `src/fabric_data_product_framework/dq.py`.

| Function | Purpose | Typical use |
|---|---|---|
| `generate_dq_rule_candidates` | Build conservative deterministic candidate rules from profile/metadata/business context. | Suggest profile-based candidate rules prior to human approval. |
| `generate_dq_rule_candidates_with_fabric_ai` | Optionally call Microsoft Fabric `pandas.ai.generate_response` to propose candidate rules. | Use Fabric Runtime 1.3+ AI functions for AI-assisted candidate suggestions. |
| `normalize_dq_rule` | Normalize rule aliases and defaults into executable DQ shape. | Clean AI-authored or hand-authored rules. |
| `normalize_dq_rules` | Normalize a rule list safely (including `None`). | Prepare contract/store rule inputs for execution. |
| `build_dq_rule_records` | Build rule-store metadata records with lifecycle fields and JSON payload. | Persist candidate/approved rules in metadata tables. |
| `store_dq_rules` | Write normalized rule records to a Spark table. | Save candidate/approved rules for reuse. |
| `load_dq_rules` | Load and parse rules from Spark table with status filters. | Fetch approved/active rules for contract runs. |
| `run_dq_rules` | Execute normalized rules with fail-closed unsupported critical behavior. | Enforce DQ gate safely for direct rule lists. |
| `run_dq_workflow` | Run contract-driven DQ flow (explicit rules, approved rule-store rules, candidate generation/storage, execution, gate). | Use from `run_data_product` and notebook orchestration. |

Generated DQ candidates are stored for human review and are **not enforced** unless they are explicitly included in contract rules or loaded via enforceable rule-store status (for example, `approved`). `run_dq_workflow` defaults to `candidate_generation_method=profile`; set `candidate_generation_method=fabric_ai` to use optional Fabric AI candidate generation (Fabric Runtime 1.3+ with AI functions configured).

Fabric notebook setup for AI mode:

```python
%pip install openai pydantic
```

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


## AI-assisted data quality rules

Functions from `src/fabric_data_product_framework/ai_quality_rules.py`, `src/fabric_data_product_framework/rule_compiler.py`, and `src/fabric_data_product_framework/quarantine.py`.

| Function | Purpose | Typical use |
|---|---|---|
| `build_quality_rule_prompt_context` | Build JSON-safe context from profile/contract/business context. | Build evidence-rich notebook prompt inputs. |
| `build_quality_rule_generation_prompt` | Build strict provider-neutral prompt instructions for AI rule generation. | Send to notebook-layer Fabric AI response call. |
| `parse_ai_quality_rule_candidates` | Parse AI response (JSON array) safely, including fenced JSON text. | Validate and extract candidate rules before review. |
| `normalize_quality_rule_candidate` | Normalize rule candidate shape/defaults. | Standardize AI payloads for storage/compilation. |
| `validate_ai_quality_rule_candidate` | Validate candidate against supported framework rule patterns. | Gate candidate compilation and approvals. |
| `build_layman_rule_records` | Flatten layman candidates into metadata-ready records. | Persist approval-candidate history. |
| `compile_layman_rule_to_quality_rule` | Compile one candidate to executable `run_quality_rules` rule format. | Convert approved candidate to technical rule. |
| `compile_layman_rules_to_quality_rules` | Compile many candidates and preserve skipped warnings. | Batch conversion with traceable compiler outcomes. |
| `build_rule_registry_records` | Build registry rows for compiled executable rules. | Persist rule definitions in technical rule registry. |
| `add_dq_failure_columns` | Add row-level `dq_errors`/`dq_warnings` columns for supported rule checks. | Annotate records before quarantine split. |
| `split_valid_and_quarantine` | Split valid vs quarantine rows using `dq_errors`. | Route good rows forward and isolate failing rows. |
| `build_quarantine_summary_records` | Build summary rows for quarantine counts. | Feed monitoring/dashboard tables. |

See `docs/workflows/ai-generated-dq-rules.md` for the full Fabric workflow and handover pattern.


## AI-assisted transformation summaries

Functions from `src/fabric_data_product_framework/ai_lineage_summary.py`.

| Function | Purpose | Typical use |
|---|---|---|
| `build_transformation_summary_prompt_context` | Build compact context from lineage summary and optional runtime/code/business inputs. | Prepare evidence package for notebook-layer AI summarisation. |
| `build_transformation_summary_generation_prompt` | Build strict prompt requiring JSON-array summaries per step. | Send to Fabric AI response API from notebook code. |
| `parse_ai_transformation_summaries` | Parse and validate AI summary candidates from JSON or fenced JSON. | Convert raw AI output to safe candidate objects. |
| `normalize_transformation_summary_candidate` | Normalize defaults and preserve unknown fields under metadata. | Standardize candidates before review/storage. |
| `build_transformation_summary_records` | Flatten candidates into metadata-ready records. | Persist reviewed summaries for handover/lineage tables. |

See `docs/workflows/ai-transformation-summary.md` for the full workflow pattern.

## Fabric notebook compatibility helpers

The framework now includes legacy-compatible Fabric notebook helpers in `fabric_notebook.py`, preserving deployed helper names (for example `get_path`, `lakehouse_table_read`, `lakehouse_table_write`, `clean_datetime_columns`, `add_system_technical_columns`, and `ODI_METADATA_LOGGER`) to minimize notebook migration effort.

## Notebook template generator

Use `create_pipeline_notebook_template(...)` from `template_generator.py` to generate a cell-separated `.py` notebook template (`# %%` and `# %% [markdown]`) that follows the framework workflow and Copilot-friendly section-by-section authoring pattern.

For Fabric house config loading guidance, see `docs/workflows/fabric-config.md`.

## Contract-first orchestration

Functions from `src/fabric_data_product_framework/data_contract.py`.

| Function | Purpose | Typical use |
|---|---|---|
| `load_data_contract` | Load a contract from YAML path or in-memory dict. | Notebook entrypoint for contract-first runs. |
| `validate_data_contract_shape` | Validate required MVP contract sections/keys for orchestration. | Fail early when contract shape is incomplete. |
| `build_runtime_context_from_contract` | Build run context (dataset/env/source/target/run_id) from contract with optional overrides. | Use before executing contract-driven steps. |
| `run_data_product` | Orchestrate source read, profiling, snapshots, transform, technical columns, quality, quarantine, contract checks, lineage, summary, and gated write. | Main contract runner API. |
| `assert_data_product_passed` | Raise if run result is not passed. | Simple post-run gate in notebooks/pipelines. |

```python
import fabric_data_product_framework as fw

contract = fw.load_data_contract("contracts/framework_mvp_orders.yml")
result = fw.run_data_product(
    spark=spark,
    contract=contract,
    transform=transform_orders,
)
fw.assert_data_product_passed(result)
```

`run_data_product` assumes Spark/Fabric-compatible table access (`spark.table`, `saveAsTable`) and metadata sink tables declared under `contract["metadata"]`.

This runner treats the pipeline as one contract execution unit (not a manual checklist of utility calls).

Minimal MVP contract shape:

```yaml
dataset:
  name: orders
  description: Orders product
  owner: data.team@example.com
  approved_usage: analytics
environment:
  name: dev
  metadata_schema: meta
refresh:
  mode: full
source:
  table: bronze.orders
  format: delta
target:
  table: silver.orders
  mode: append
  format: delta
keys:
  business_keys: [order_id]
  watermark_column: updated_at
  partition_column: order_date
schema:
  required_source_columns: [order_id, updated_at]
  required_output_columns: [order_id, updated_at]
quality:
  rules: []
drift:
  schema_policy: {}
  incremental_policy: {}
metadata:
  source_profile_table: meta.source_profile
  output_profile_table: meta.output_profile
  schema_snapshot_table: meta.schema_snapshot
  partition_snapshot_table: meta.partition_snapshot
  quality_result_table: meta.quality_result
  quarantine_table: meta.quarantine
  contract_validation_table: meta.contract_validation
  lineage_table: meta.lineage
  run_summary_table: meta.run_summary
  dataset_runs_table: meta.dataset_runs
```



Use `full` for normal full rebuild datasets. Use `incremental` only when the dataset has partition/watermark logic and requires historical partition safety checks.


## Contract-first data product runner

Functions from `src/fabric_data_product_framework/data_contract.py`.

| Function | Purpose | Typical use |
|---|---|---|
| `load_data_contract` | Load YAML/dict input and normalize it into typed data product contract sections. | Keep one editable contract file while preserving Python/YAML friendliness. |
| `normalize_data_product_contract` | Normalize loose/legacy contract dictionaries into sectioned typed objects. | Support backward-compatible migration from older `upstream_contract`/`downstream_contract` keys. |
| `run_data_product` | Execute the contract-first runner using normalized source/target/quality/drift/metadata/runtime sections internally. | Run data products while keeping the user-facing API unchanged. |
| `data_product_contract_to_dict` | Serialize normalized contract objects back to plain dictionaries. | Logging, testing, JSON/YAML export prep. |

Note: users edit a single contract, and the framework normalizes it into typed sections that `run_data_product` consumes internally.

Normalized contract snippet:

```yaml
dataset:
  name: orders
source:
  table: raw.orders
target:
  table: curated.orders
  required_columns: [order_id, updated_at]
metadata:
  source_profile_table: meta.source_profile
  output_profile_table: meta.output_profile
  schema_snapshot_table: meta.schema_snapshot
  partition_snapshot_table: meta.partition_snapshot
  quality_result_table: meta.quality_result
  quarantine_table: meta.quarantine
  contract_validation_table: meta.contract_validation
  lineage_table: meta.lineage
  run_summary_table: meta.run_summary
  dataset_runs_table: meta.dataset_runs
```

Legacy mapping note: `upstream_contract.table_name`/`required_columns` and `downstream_contract.table_name`/`required_columns` are mapped to normalized `source.*` and `target.*` fields.

```python
import fabric_data_product_framework as fw

contract = fw.load_data_contract("contracts/examples/normalized_data_product_contract.yml")
result = fw.run_data_product(spark=spark, contract=contract, transform=transform_orders)
```
