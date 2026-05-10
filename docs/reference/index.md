# Function Reference

Use this page as an API lookup after you understand the notebook flow.

## Start from the templates

<table class="reference-template-table">
  <thead>
    <tr>
      <th>Notebook</th>
      <th>Guided usage</th>
      <th>Full template</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Notebook"><code>`00_env_config`</code></td>
      <td data-label="Guided usage">Shared environment bootstrap and validation before exploration or pipeline notebooks run.</td>
      <td data-label="Full template">[`Open notebook`](https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/00_env_config.ipynb)</td>
    </tr>
    <tr>
      <td data-label="Notebook"><code>`02_ex_<agreement>_<topic>`</code></td>
      <td data-label="Guided usage">Exploration notebook flow used to profile source data and draft advisory AI outputs for human review.</td>
      <td data-label="Full template">[`Open notebook`](https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/02_ex_agreement_topic.ipynb)</td>
    </tr>
    <tr>
      <td data-label="Notebook"><code>`03_pc_<agreement>_<pipeline>`</code></td>
      <td data-label="Guided usage">Pipeline-contract notebook flow for deterministic enforcement and controlled publishing.</td>
      <td data-label="Full template">[`Open notebook`](https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/03_pc_agreement_source_to_target.ipynb)</td>
    </tr>
  </tbody>
</table>

## What runs where

- `00_env_config` is shared setup.
- `02_ex` is AI-assisted exploration and human review.
- `03_pc` is deterministic pipeline enforcement.

AI functions are advisory. Approved contracts and pipeline notebooks are the enforcement point.

## Starter path functions

### `00_env_config`

Shared environment bootstrap and validation before exploration or pipeline notebooks run.

#### Segment 2: Define environment targets and notebook policy

<table class="reference-function-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Importance</th>
      <th>Purpose</th>
      <th>Related helpers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class">[`Housepath`](./step-02a-shared-runtime-config/Housepath/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Fabric lakehouse or warehouse connection details.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`create_path_config`](./step-02a-shared-runtime-config/create_path_config/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create environment-to-target routing used by Fabric IO helpers.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`create_notebook_runtime_config`](./step-02a-shared-runtime-config/create_notebook_runtime_config/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create notebook naming-policy configuration for runtime guards.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`validate_framework_config`](./step-02a-shared-runtime-config/validate_framework_config/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate and normalize framework configuration input.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`load_fabric_config`](./step-02a-shared-runtime-config/load_fabric_config/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate and return a user-supplied framework configuration.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`get_path`](./step-02a-shared-runtime-config/get_path/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Resolve a configured Fabric path for an environment and target.</td>
      <td data-label="Related helpers">—</td>
    </tr>
  </tbody>
</table>

#### Segment 3: Set AI, quality, governance, and lineage defaults

<table class="reference-function-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Importance</th>
      <th>Purpose</th>
      <th>Related helpers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class">[`create_ai_prompt_config`](./step-02a-shared-runtime-config/create_ai_prompt_config/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create the AI prompt-template configuration used by FabricOps.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`create_governance_config`](./step-02a-shared-runtime-config/create_governance_config/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create governance policy defaults for FabricOps runtime checks.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`create_quality_config`](./step-02a-shared-runtime-config/create_quality_config/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create the default quality policy used during FabricOps checks.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`create_lineage_config`](./step-02a-shared-runtime-config/create_lineage_config/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create lineage capture defaults for FabricOps handover traceability.</td>
      <td data-label="Related helpers">—</td>
    </tr>
  </tbody>
</table>

#### Segment 4: Assemble and validate framework config

<table class="reference-function-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Importance</th>
      <th>Purpose</th>
      <th>Related helpers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class">[`create_framework_config`](./step-02a-shared-runtime-config/create_framework_config/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create the top-level FabricOps framework configuration contract.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`validate_framework_config`](./step-02a-shared-runtime-config/validate_framework_config/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate and normalize framework configuration input.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`load_fabric_config`](./step-02a-shared-runtime-config/load_fabric_config/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate and return a user-supplied framework configuration.</td>
      <td data-label="Related helpers">—</td>
    </tr>
  </tbody>
</table>

#### Segment 5: Run startup checks and show resolved paths

<table class="reference-function-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Importance</th>
      <th>Purpose</th>
      <th>Related helpers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class">[`run_config_smoke_tests`](./step-02b-notebook-startup-checks/run_config_smoke_tests/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Run 00_env_config smoke checks for Spark, runtime context, configured paths, notebook naming, and optional AI/IO imports.</td>
      <td data-label="Related helpers">[`_check_spark_session`](./internal/config/_check_spark_session.md) (internal), [`_get_fabric_runtime_metadata`](./internal/config/_get_fabric_runtime_metadata.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`bootstrap_fabric_env`](./step-02b-notebook-startup-checks/bootstrap_fabric_env/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Bootstrap 00_env_config environment readiness by resolving required targets and collecting runtime/AI check results.</td>
      <td data-label="Related helpers">[`_get_fabric_runtime_metadata`](./internal/config/_get_fabric_runtime_metadata.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`check_fabric_ai_functions_available`](./step-02a-shared-runtime-config/check_fabric_ai_functions_available/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Check whether Fabric AI Functions are available in the current runtime.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`configure_fabric_ai_functions`](./step-01-governance-context/configure_fabric_ai_functions/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Apply optional default Fabric AI Function configuration.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`get_path`](./step-02a-shared-runtime-config/get_path/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Resolve a configured Fabric path for an environment and target.</td>
      <td data-label="Related helpers">—</td>
    </tr>
  </tbody>
</table>

### `02_ex_<agreement>_<topic>`

Exploration notebook flow used to profile source data and draft advisory AI outputs for human review.

#### Segment 1: Load shared config and runtime

<table class="reference-function-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Importance</th>
      <th>Purpose</th>
      <th>Related helpers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class">[`load_fabric_config`](./step-02a-shared-runtime-config/load_fabric_config/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate and return a user-supplied framework configuration.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`validate_notebook_name`](./step-01-governance-context/validate_notebook_name/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate notebook names against the framework workspace notebook model.</td>
      <td data-label="Related helpers">[`_infer_notebook_name_from_runtime`](./internal/runtime/_infer_notebook_name_from_runtime.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`assert_notebook_name_valid`](./step-01-governance-context/assert_notebook_name_valid/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Raise :class:`NotebookNamingError` when a notebook name is invalid.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_runtime_context`](./step-01-governance-context/build_runtime_context/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build a standard runtime context dictionary for Fabric notebooks.</td>
      <td data-label="Related helpers">[`_infer_notebook_name_from_runtime`](./internal/runtime/_infer_notebook_name_from_runtime.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`get_path`](./step-02a-shared-runtime-config/get_path/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Resolve a configured Fabric path for an environment and target.</td>
      <td data-label="Related helpers">—</td>
    </tr>
  </tbody>
</table>

#### Segment 2: Profile source and capture evidence

<table class="reference-function-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Importance</th>
      <th>Purpose</th>
      <th>Related helpers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class">[`lakehouse_table_read`](./step-03-source-contract-ingestion-pattern/lakehouse_table_read/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a Delta table from a Fabric lakehouse.</td>
      <td data-label="Related helpers">[`_get_spark`](./internal/fabric_io/_get_spark.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`warehouse_read`](./step-03-source-contract-ingestion-pattern/warehouse_read/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a table from a Microsoft Fabric warehouse.</td>
      <td data-label="Related helpers">[`_get_spark`](./internal/fabric_io/_get_spark.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`generate_metadata_profile`](./step-04-ingest-profile-store/generate_metadata_profile/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Generate standard metadata profile rows for a Spark/Fabric DataFrame.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`profile_dataframe_to_metadata`](./step-04-ingest-profile-store/profile_dataframe_to_metadata/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Profile a Spark/Fabric DataFrame into metadata-compatible metadata rows.</td>
      <td data-label="Related helpers">—</td>
    </tr>
  </tbody>
</table>

#### Segment 3: AI-assisted drafting (advisory only)

<table class="reference-function-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Importance</th>
      <th>Purpose</th>
      <th>Related helpers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class">[`suggest_dq_rules_prompt`](./step-08-ai-assisted-dq-suggestions/suggest_dq_rules_prompt/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build a prompt for candidate DQ rule suggestions.</td>
      <td data-label="Related helpers">—</td>
    </tr>
  </tbody>
</table>

#### Segment 4: Human approval and contract write

<table class="reference-function-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Importance</th>
      <th>Purpose</th>
      <th>Related helpers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class">[`normalize_contract_dict`](./step-03-source-contract-ingestion-pattern/normalize_contract_dict/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Normalize a notebook-authored contract dictionary to a stable shape.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`validate_contract_dict`](./step-03-source-contract-ingestion-pattern/validate_contract_dict/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate a contract dictionary and return error strings without raising.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`write_contract_to_lakehouse`](./step-07-output-profile-product-contract/write_contract_to_lakehouse/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate and persist contract records into Fabric metadata tables.</td>
      <td data-label="Related helpers">—</td>
    </tr>
  </tbody>
</table>

#### Optional lineage notes

<table class="reference-function-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Importance</th>
      <th>Purpose</th>
      <th>Related helpers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class">[`build_lineage_from_notebook_code`](./step-10-lineage-handover-documentation/build_lineage_from_notebook_code/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Scan, optionally enrich, and validate lineage from notebook source code.</td>
      <td data-label="Related helpers">—</td>
    </tr>
  </tbody>
</table>

### `03_pc_<agreement>_<pipeline>`

Pipeline-contract notebook flow for deterministic enforcement and controlled publishing.

#### Segment 1: Load shared config and runtime context

<table class="reference-function-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Importance</th>
      <th>Purpose</th>
      <th>Related helpers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class">[`load_fabric_config`](./step-02a-shared-runtime-config/load_fabric_config/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate and return a user-supplied framework configuration.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`validate_notebook_name`](./step-01-governance-context/validate_notebook_name/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate notebook names against the framework workspace notebook model.</td>
      <td data-label="Related helpers">[`_infer_notebook_name_from_runtime`](./internal/runtime/_infer_notebook_name_from_runtime.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`assert_notebook_name_valid`](./step-01-governance-context/assert_notebook_name_valid/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Raise :class:`NotebookNamingError` when a notebook name is invalid.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`generate_run_id`](./step-01-governance-context/generate_run_id/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Generate a notebook-safe run identifier.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_runtime_context`](./step-01-governance-context/build_runtime_context/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build a standard runtime context dictionary for Fabric notebooks.</td>
      <td data-label="Related helpers">[`_infer_notebook_name_from_runtime`](./internal/runtime/_infer_notebook_name_from_runtime.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`get_path`](./step-02a-shared-runtime-config/get_path/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Resolve a configured Fabric path for an environment and target.</td>
      <td data-label="Related helpers">—</td>
    </tr>
  </tbody>
</table>

#### Segment 2: Load approved contract and source data

<table class="reference-function-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Importance</th>
      <th>Purpose</th>
      <th>Related helpers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class">[`load_latest_approved_contract`](./step-03-source-contract-ingestion-pattern/load_latest_approved_contract/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Load the latest approved contract for a dataset/object pair.</td>
      <td data-label="Related helpers">[`_select_latest`](./internal/contracts/_select_latest.md) (internal), [`_to_records`](./internal/contracts/_to_records.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`lakehouse_table_read`](./step-03-source-contract-ingestion-pattern/lakehouse_table_read/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a Delta table from a Fabric lakehouse.</td>
      <td data-label="Related helpers">[`_get_spark`](./internal/fabric_io/_get_spark.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`warehouse_read`](./step-03-source-contract-ingestion-pattern/warehouse_read/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a table from a Microsoft Fabric warehouse.</td>
      <td data-label="Related helpers">[`_get_spark`](./internal/fabric_io/_get_spark.md) (internal)</td>
    </tr>
  </tbody>
</table>

#### Segment 3: Validate columns, transform, and compile rules

<table class="reference-function-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Importance</th>
      <th>Purpose</th>
      <th>Related helpers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class">[`extract_required_columns`](./step-03-source-contract-ingestion-pattern/extract_required_columns/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract required column names from a normalized contract.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`get_executable_quality_rules`](./step-06c-pipeline-controls/get_executable_quality_rules/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Return normalized quality rules ready for pipeline enforcement.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`validate_dq_rules`](./step-06c-pipeline-controls/validate_dq_rules/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate notebook-facing DQ rules.</td>
      <td data-label="Related helpers">—</td>
    </tr>
  </tbody>
</table>

#### Segment 4: Run DQ, split outputs, and publish

<table class="reference-function-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Importance</th>
      <th>Purpose</th>
      <th>Related helpers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class">[`run_dq_rules`](./step-06c-pipeline-controls/run_dq_rules/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Run notebook-facing DQ rules and return a Spark DataFrame result.</td>
      <td data-label="Related helpers">[`_to_quality_rule`](./internal/dq/_to_quality_rule.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`split_valid_and_quarantine`](./step-06c-pipeline-controls/split_valid_and_quarantine/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Split a Spark DataFrame into pass/quarantine outputs for row-level DQ rules.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`lakehouse_table_write`](./step-06d-controlled-outputs/lakehouse_table_write/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Write a Spark DataFrame to a Fabric lakehouse Delta table.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`warehouse_write`](./step-06d-controlled-outputs/warehouse_write/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Write a Spark DataFrame to a Microsoft Fabric warehouse table.</td>
      <td data-label="Related helpers">—</td>
    </tr>
  </tbody>
</table>

#### Optional metadata / lineage / handover evidence

<table class="reference-function-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Importance</th>
      <th>Purpose</th>
      <th>Related helpers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class">[`build_dataset_run_record`](./step-07-output-profile-product-contract/build_dataset_run_record/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build a dataset-run metadata record for operational tracking.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_quality_result_records`](./step-07-output-profile-product-contract/build_quality_result_records/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert quality-rule execution output into metadata evidence records.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_contract_records`](./step-07-output-profile-product-contract/build_contract_records/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build grouped contract header, column, and rule metadata payloads.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_lineage_records`](./step-10-lineage-handover-documentation/build_lineage_records/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build compact lineage records for downstream metadata sinks.</td>
      <td data-label="Related helpers">—</td>
    </tr>
  </tbody>
</table>

## All public functions

<table class="reference-catalogue-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Starter path</th>
      <th>Importance</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class">[`add_audit_columns`](./step-06b-runtime-standards/add_audit_columns/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Add run tracking and audit columns for ingestion workflows.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`add_datetime_features`](./step-06b-runtime-standards/add_datetime_features/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Add localized datetime feature columns derived from a UTC datetime column.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`add_hash_columns`](./step-06b-runtime-standards/add_hash_columns/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Add business key and row-level SHA256 hash columns.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`assert_dq_passed`](./step-06d-controlled-outputs/assert_dq_passed/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Raise when any error-severity DQ rule failed after results are logged.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`assert_notebook_name_valid`](./step-01-governance-context/assert_notebook_name_valid/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Starter path">02_ex, 03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Raise :class:`NotebookNamingError` when a notebook name is invalid.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`bootstrap_fabric_env`](./step-02b-notebook-startup-checks/bootstrap_fabric_env/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Bootstrap 00_env_config environment readiness by resolving required targets and collecting runtime/AI check results.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_ai_quality_context`](./step-04-ingest-profile-store/build_ai_quality_context/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build deterministic AI-ready context from standard metadata profile rows.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_contract_column_records`](./step-07-output-profile-product-contract/build_contract_column_records/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build normalized contract-column metadata records for persistence.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_contract_header_record`](./step-07-output-profile-product-contract/build_contract_header_record/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build one header row for FABRICOPS_CONTRACTS.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_contract_records`](./step-07-output-profile-product-contract/build_contract_records/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build grouped contract header, column, and rule metadata payloads.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_contract_rule_records`](./step-07-output-profile-product-contract/build_contract_rule_records/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build quality-rule metadata records from a validated contract.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_contract_summary`](./step-07-output-profile-product-contract/build_contract_summary/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build a concise contract summary for reviews and handover.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_dataset_run_record`](./step-07-output-profile-product-contract/build_dataset_run_record/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build a dataset-run metadata record for operational tracking.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_dq_rule_candidate_prompt`](./step-08-ai-assisted-dq-suggestions/build_dq_rule_candidate_prompt/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build the DQ-candidate prompt used in AI-assisted quality drafting.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_governance_candidate_prompt`](./step-09-ai-assisted-classification/build_governance_candidate_prompt/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build the governance-candidate prompt for AI-assisted classification drafts.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_governance_classification_records`](./step-09-ai-assisted-classification/build_governance_classification_records/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build metadata-ready governance classification records from column suggestions.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_handover_summary_prompt`](./step-10-lineage-handover-documentation/build_handover_summary_prompt/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build the handover-summary prompt for AI-assisted run handoff drafting.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_lineage_from_notebook_code`](./step-10-lineage-handover-documentation/build_lineage_from_notebook_code/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">02_ex</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Scan, optionally enrich, and validate lineage from notebook source code.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_lineage_handover_markdown`](./step-10-lineage-handover-documentation/build_lineage_handover_markdown/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Create a concise markdown handover summary from lineage execution results.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_lineage_record_from_steps`](./step-10-lineage-handover-documentation/build_lineage_record_from_steps/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Create metadata-ready lineage records from validated lineage steps.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_lineage_records`](./step-10-lineage-handover-documentation/build_lineage_records/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build compact lineage records for downstream metadata sinks.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_manual_dq_rule_prompt_package`](./step-08-ai-assisted-dq-suggestions/build_manual_dq_rule_prompt_package/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build copy/paste prompt package for manual DQ candidate generation.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_manual_governance_prompt_package`](./step-09-ai-assisted-classification/build_manual_governance_prompt_package/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build copy/paste prompt package for manual governance suggestion generation.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_manual_handover_prompt_package`](./step-10-lineage-handover-documentation/build_manual_handover_prompt_package/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build copy/paste prompt package for manual handover summary generation.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_quality_result_records`](./step-07-output-profile-product-contract/build_quality_result_records/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert quality-rule execution output into metadata evidence records.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_run_summary`](./step-10-lineage-handover-documentation/build_run_summary/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build a handover-friendly summary for one data product run.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_runtime_context`](./step-01-governance-context/build_runtime_context/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Starter path">02_ex, 03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build a standard runtime context dictionary for Fabric notebooks.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_schema_drift_records`](./step-04-ingest-profile-store/build_schema_drift_records/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert schema drift results into metadata records for audit trails.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_schema_snapshot_records`](./step-04-ingest-profile-store/build_schema_snapshot_records/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert a schema snapshot into row-wise metadata records.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`check_fabric_ai_functions_available`](./step-02a-shared-runtime-config/check_fabric_ai_functions_available/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Check whether Fabric AI Functions are available in the current runtime.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`check_partition_drift`](./step-04-ingest-profile-store/check_partition_drift/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Check partition-level drift using keys, partitions, and optional watermark baselines.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`check_profile_drift`](./step-04-ingest-profile-store/check_profile_drift/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Compare profile metrics against a baseline profile and drift thresholds.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`check_schema_drift`](./step-04-ingest-profile-store/check_schema_drift/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Compare a current dataframe schema against a baseline schema snapshot.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`classify_column`](./step-09-ai-assisted-classification/classify_column/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Classify one column using term matching, metadata cues, and business context.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`classify_columns`](./step-09-ai-assisted-classification/classify_columns/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Classify multiple columns and return normalized governance suggestions.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`configure_fabric_ai_functions`](./step-01-governance-context/configure_fabric_ai_functions/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Apply optional default Fabric AI Function configuration.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`contract_records_to_spark`](./step-07-output-profile-product-contract/contract_records_to_spark/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert record dictionaries into a Spark DataFrame when Spark is available.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`create_ai_prompt_config`](./step-02a-shared-runtime-config/create_ai_prompt_config/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create the AI prompt-template configuration used by FabricOps.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`create_framework_config`](./step-02a-shared-runtime-config/create_framework_config/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create the top-level FabricOps framework configuration contract.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`create_governance_config`](./step-02a-shared-runtime-config/create_governance_config/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create governance policy defaults for FabricOps runtime checks.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`create_lineage_config`](./step-02a-shared-runtime-config/create_lineage_config/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create lineage capture defaults for FabricOps handover traceability.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`create_notebook_runtime_config`](./step-02a-shared-runtime-config/create_notebook_runtime_config/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create notebook naming-policy configuration for runtime guards.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`create_path_config`](./step-02a-shared-runtime-config/create_path_config/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create environment-to-target routing used by Fabric IO helpers.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`create_quality_config`](./step-02a-shared-runtime-config/create_quality_config/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create the default quality policy used during FabricOps checks.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE`](./step-08-ai-assisted-dq-suggestions/DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Default prompt template used to draft candidate DQ rules.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`default_technical_columns`](./step-06b-runtime-standards/default_technical_columns/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Return framework-generated and legacy technical column names to ignore.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`enrich_lineage_steps_with_ai`](./step-10-lineage-handover-documentation/enrich_lineage_steps_with_ai/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Optionally enrich deterministic lineage steps using an AI helper callable.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`extract_business_keys`](./step-03-source-contract-ingestion-pattern/extract_business_keys/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract business-key column names from a normalized contract.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`extract_classifications`](./step-03-source-contract-ingestion-pattern/extract_classifications/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract column classification mappings from a normalized contract.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`extract_optional_columns`](./step-03-source-contract-ingestion-pattern/extract_optional_columns/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract optional column names from a normalized contract.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`extract_quality_rules`](./step-03-source-contract-ingestion-pattern/extract_quality_rules/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract raw quality-rule definitions from a normalized contract.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`extract_required_columns`](./step-03-source-contract-ingestion-pattern/extract_required_columns/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract required column names from a normalized contract.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`fallback_copilot_lineage_prompt`](./step-10-lineage-handover-documentation/fallback_copilot_lineage_prompt/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build a fallback Copilot prompt for manual lineage enrichment.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`generate_dq_rule_candidates_with_fabric_ai`](./step-08-ai-assisted-dq-suggestions/generate_dq_rule_candidates_with_fabric_ai/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Append AI-suggested DQ rule candidates to a profiling DataFrame.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`generate_governance_candidates_with_fabric_ai`](./step-09-ai-assisted-classification/generate_governance_candidates_with_fabric_ai/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Execute Fabric AI Functions to append governance suggestions to a DataFrame.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`generate_handover_summary_with_fabric_ai`](./step-10-lineage-handover-documentation/generate_handover_summary_with_fabric_ai/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Execute Fabric AI Functions to append handover summary suggestions.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`generate_metadata_profile`](./step-04-ingest-profile-store/generate_metadata_profile/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Starter path">02_ex</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Generate standard metadata profile rows for a Spark/Fabric DataFrame.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`generate_run_id`](./step-01-governance-context/generate_run_id/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Generate a notebook-safe run identifier.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`get_default_dq_rule_templates`](./step-08-ai-assisted-dq-suggestions/get_default_dq_rule_templates/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Return editable example data quality rules.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`get_executable_quality_rules`](./step-06c-pipeline-controls/get_executable_quality_rules/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Return normalized quality rules ready for pipeline enforcement.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`get_path`](./step-02a-shared-runtime-config/get_path/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config, 02_ex, 03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Resolve a configured Fabric path for an environment and target.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`Housepath`](./step-02a-shared-runtime-config/Housepath/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Fabric lakehouse or warehouse connection details.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`lakehouse_csv_read`](./step-03-source-contract-ingestion-pattern/lakehouse_csv_read/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a CSV file from a Fabric lakehouse Files path.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`lakehouse_excel_read_as_spark`](./step-03-source-contract-ingestion-pattern/lakehouse_excel_read_as_spark/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read an Excel file from a Fabric lakehouse Files path.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`lakehouse_parquet_read_as_spark`](./step-03-source-contract-ingestion-pattern/lakehouse_parquet_read_as_spark/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a Parquet file from a Fabric lakehouse Files path.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`lakehouse_table_read`](./step-03-source-contract-ingestion-pattern/lakehouse_table_read/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">02_ex, 03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a Delta table from a Fabric lakehouse.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`lakehouse_table_write`](./step-06d-controlled-outputs/lakehouse_table_write/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Write a Spark DataFrame to a Fabric lakehouse Delta table.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`load_contract_from_lakehouse`](./step-03-source-contract-ingestion-pattern/load_contract_from_lakehouse/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Load one contract by ID/version from Fabric metadata storage.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`load_data_contract`](./step-03-source-contract-ingestion-pattern/load_data_contract/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Load and normalize a data product contract from file path or dictionary.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`load_fabric_config`](./step-02a-shared-runtime-config/load_fabric_config/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config, 02_ex, 03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate and return a user-supplied framework configuration.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`load_latest_approved_contract`](./step-03-source-contract-ingestion-pattern/load_latest_approved_contract/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Load the latest approved contract for a dataset/object pair.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`normalize_contract_dict`](./step-03-source-contract-ingestion-pattern/normalize_contract_dict/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">02_ex</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Normalize a notebook-authored contract dictionary to a stable shape.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`parse_manual_ai_json_response`](./step-10-lineage-handover-documentation/parse_manual_ai_json_response/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Parse manual AI JSON output into Python objects.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`plot_lineage_steps`](./step-10-lineage-handover-documentation/plot_lineage_steps/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Render lineage steps as a directed graph figure.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`profile_dataframe`](./step-04-ingest-profile-store/profile_dataframe/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build a lightweight profile for pandas or Spark-like DataFrames.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`profile_dataframe_to_metadata`](./step-04-ingest-profile-store/profile_dataframe_to_metadata/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Starter path">02_ex</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Profile a Spark/Fabric DataFrame into metadata-compatible metadata rows.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`profile_metadata_to_records`](./step-04-ingest-profile-store/profile_metadata_to_records/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert Spark metadata profile rows into JSON-friendly dictionaries.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`render_run_summary_markdown`](./step-10-lineage-handover-documentation/render_run_summary_markdown/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Render a run summary dictionary into Markdown for handover notes.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`run_config_smoke_tests`](./step-02b-notebook-startup-checks/run_config_smoke_tests/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Run 00_env_config smoke checks for Spark, runtime context, configured paths, notebook naming, and optional AI/IO imports.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`run_data_product`](./step-06a-transformation-logic/run_data_product/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Run the starter kit workflow end-to-end for a data product outcome.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`run_dq_rules`](./step-06c-pipeline-controls/run_dq_rules/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Run notebook-facing DQ rules and return a Spark DataFrame result.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`run_quality_rules`](./step-06c-pipeline-controls/run_quality_rules/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Execute quality rules against a dataframe and return structured results.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`scan_notebook_cells`](./step-10-lineage-handover-documentation/scan_notebook_cells/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Scan multiple notebook cells and append cell references to lineage steps.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`scan_notebook_lineage`](./step-10-lineage-handover-documentation/scan_notebook_lineage/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Extract deterministic lineage steps from notebook code using AST parsing.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`split_valid_and_quarantine`](./step-06c-pipeline-controls/split_valid_and_quarantine/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Split a Spark DataFrame into pass/quarantine outputs for row-level DQ rules.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`suggest_accepted_value_mapping_prompt`](./step-08-ai-assisted-dq-suggestions/suggest_accepted_value_mapping_prompt/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build a constrained prompt for accepted-value mapping suggestions.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`suggest_closest_accepted_value`](./step-08-ai-assisted-dq-suggestions/suggest_closest_accepted_value/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Suggest a deterministic closest accepted value using ``difflib``.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`suggest_dq_rules_prompt`](./step-08-ai-assisted-dq-suggestions/suggest_dq_rules_prompt/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">02_ex</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build a prompt for candidate DQ rule suggestions.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`summarize_drift_results`](./step-04-ingest-profile-store/summarize_drift_results/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Summarize schema, partition, and profile drift outcomes into one decision.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`summarize_governance_classifications`](./step-09-ai-assisted-classification/summarize_governance_classifications/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Summarize governance classification outputs into review-friendly counts.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`validate_contract_dict`](./step-03-source-contract-ingestion-pattern/validate_contract_dict/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">02_ex</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate a contract dictionary and return error strings without raising.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`validate_dq_rules`](./step-06c-pipeline-controls/validate_dq_rules/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate notebook-facing DQ rules.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`validate_framework_config`](./step-02a-shared-runtime-config/validate_framework_config/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate and normalize framework configuration input.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`validate_lineage_steps`](./step-10-lineage-handover-documentation/validate_lineage_steps/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Validate lineage step structure and flag records requiring human review.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`validate_notebook_name`](./step-01-governance-context/validate_notebook_name/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Starter path">02_ex, 03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate notebook names against the framework workspace notebook model.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`warehouse_read`](./step-03-source-contract-ingestion-pattern/warehouse_read/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">02_ex, 03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a table from a Microsoft Fabric warehouse.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`warehouse_write`](./step-06d-controlled-outputs/warehouse_write/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Write a Spark DataFrame to a Microsoft Fabric warehouse table.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`write_contract_to_lakehouse`](./step-07-output-profile-product-contract/write_contract_to_lakehouse/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">02_ex</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate and persist contract records into Fabric metadata tables.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`write_governance_classifications`](./step-09-ai-assisted-classification/write_governance_classifications/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Persist governance classifications to a metadata destination.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`write_metadata_records`](./step-07-output-profile-product-contract/write_metadata_records/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Write metadata records to a configured metadata sink.</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`write_multiple_metadata_outputs`](./step-07-output-profile-product-contract/write_multiple_metadata_outputs/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Write multiple metadata payloads to their configured destinations.</td>
    </tr>
  </tbody>
</table>

## Additional public functions

These exported callables are part of the complete catalogue above and are not directly used in the minimal starter template path.

<table class="reference-function-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Importance</th>
      <th>Purpose</th>
      <th>Related helpers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class">[`add_audit_columns`](./step-06b-runtime-standards/add_audit_columns/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Add run tracking and audit columns for ingestion workflows.</td>
      <td data-label="Related helpers">[`_assert_columns_exist`](./internal/technical_columns/_assert_columns_exist.md) (internal), [`_bucket_values_pandas`](./internal/technical_columns/_bucket_values_pandas.md) (internal), [`_get_fabric_runtime_context`](./internal/technical_columns/_get_fabric_runtime_context.md) (internal), [`_resolve_engine`](./internal/technical_columns/_resolve_engine.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`add_datetime_features`](./step-06b-runtime-standards/add_datetime_features/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Add localized datetime feature columns derived from a UTC datetime column.</td>
      <td data-label="Related helpers">[`_assert_columns_exist`](./internal/technical_columns/_assert_columns_exist.md) (internal), [`_resolve_engine`](./internal/technical_columns/_resolve_engine.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`add_hash_columns`](./step-06b-runtime-standards/add_hash_columns/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Add business key and row-level SHA256 hash columns.</td>
      <td data-label="Related helpers">[`_assert_columns_exist`](./internal/technical_columns/_assert_columns_exist.md) (internal), [`_hash_row`](./internal/technical_columns/_hash_row.md) (internal), [`_non_technical_columns`](./internal/technical_columns/_non_technical_columns.md) (internal), [`_resolve_engine`](./internal/technical_columns/_resolve_engine.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`assert_dq_passed`](./step-06d-controlled-outputs/assert_dq_passed/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Raise when any error-severity DQ rule failed after results are logged.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_ai_quality_context`](./step-04-ingest-profile-store/build_ai_quality_context/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build deterministic AI-ready context from standard metadata profile rows.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_contract_column_records`](./step-07-output-profile-product-contract/build_contract_column_records/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build normalized contract-column metadata records for persistence.</td>
      <td data-label="Related helpers">[`_now_utc_iso`](./internal/contracts/_now_utc_iso.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_contract_header_record`](./step-07-output-profile-product-contract/build_contract_header_record/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build one header row for FABRICOPS_CONTRACTS.</td>
      <td data-label="Related helpers">[`_now_utc_iso`](./internal/contracts/_now_utc_iso.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_contract_rule_records`](./step-07-output-profile-product-contract/build_contract_rule_records/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build quality-rule metadata records from a validated contract.</td>
      <td data-label="Related helpers">[`_now_utc_iso`](./internal/contracts/_now_utc_iso.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_contract_summary`](./step-07-output-profile-product-contract/build_contract_summary/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build a concise contract summary for reviews and handover.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_dq_rule_candidate_prompt`](./step-08-ai-assisted-dq-suggestions/build_dq_rule_candidate_prompt/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build the DQ-candidate prompt used in AI-assisted quality drafting.</td>
      <td data-label="Related helpers">[`_resolve_prompt_template`](./internal/ai/_resolve_prompt_template.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_governance_candidate_prompt`](./step-09-ai-assisted-classification/build_governance_candidate_prompt/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build the governance-candidate prompt for AI-assisted classification drafts.</td>
      <td data-label="Related helpers">[`_resolve_prompt_template`](./internal/ai/_resolve_prompt_template.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_governance_classification_records`](./step-09-ai-assisted-classification/build_governance_classification_records/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build metadata-ready governance classification records from column suggestions.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_handover_summary_prompt`](./step-10-lineage-handover-documentation/build_handover_summary_prompt/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build the handover-summary prompt for AI-assisted run handoff drafting.</td>
      <td data-label="Related helpers">[`_resolve_prompt_template`](./internal/ai/_resolve_prompt_template.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_lineage_handover_markdown`](./step-10-lineage-handover-documentation/build_lineage_handover_markdown/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Create a concise markdown handover summary from lineage execution results.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_lineage_record_from_steps`](./step-10-lineage-handover-documentation/build_lineage_record_from_steps/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Create metadata-ready lineage records from validated lineage steps.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_manual_dq_rule_prompt_package`](./step-08-ai-assisted-dq-suggestions/build_manual_dq_rule_prompt_package/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build copy/paste prompt package for manual DQ candidate generation.</td>
      <td data-label="Related helpers">[`_compact_sample_rows`](./internal/ai/_compact_sample_rows.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_manual_governance_prompt_package`](./step-09-ai-assisted-classification/build_manual_governance_prompt_package/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build copy/paste prompt package for manual governance suggestion generation.</td>
      <td data-label="Related helpers">[`_compact_sample_rows`](./internal/ai/_compact_sample_rows.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_manual_handover_prompt_package`](./step-10-lineage-handover-documentation/build_manual_handover_prompt_package/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build copy/paste prompt package for manual handover summary generation.</td>
      <td data-label="Related helpers">[`_compact_sample_rows`](./internal/ai/_compact_sample_rows.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_run_summary`](./step-10-lineage-handover-documentation/build_run_summary/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build a handover-friendly summary for one data product run.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_schema_drift_records`](./step-04-ingest-profile-store/build_schema_drift_records/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert schema drift results into metadata records for audit trails.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`build_schema_snapshot_records`](./step-04-ingest-profile-store/build_schema_snapshot_records/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert a schema snapshot into row-wise metadata records.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`check_partition_drift`](./step-04-ingest-profile-store/check_partition_drift/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Check partition-level drift using keys, partitions, and optional watermark baselines.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`check_profile_drift`](./step-04-ingest-profile-store/check_profile_drift/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Compare profile metrics against a baseline profile and drift thresholds.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`check_schema_drift`](./step-04-ingest-profile-store/check_schema_drift/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Compare a current dataframe schema against a baseline schema snapshot.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`classify_column`](./step-09-ai-assisted-classification/classify_column/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Classify one column using term matching, metadata cues, and business context.</td>
      <td data-label="Related helpers">[`_match_terms`](./internal/governance/_match_terms.md) (internal), [`_phrase_in_text`](./internal/governance/_phrase_in_text.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`classify_columns`](./step-09-ai-assisted-classification/classify_columns/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Classify multiple columns and return normalized governance suggestions.</td>
      <td data-label="Related helpers">[`_column_name`](./internal/governance/_column_name.md) (internal), [`_normalize_columns`](./internal/governance/_normalize_columns.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`contract_records_to_spark`](./step-07-output-profile-product-contract/contract_records_to_spark/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert record dictionaries into a Spark DataFrame when Spark is available.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE`](./step-08-ai-assisted-dq-suggestions/DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Default prompt template used to draft candidate DQ rules.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`default_technical_columns`](./step-06b-runtime-standards/default_technical_columns/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Return framework-generated and legacy technical column names to ignore.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`enrich_lineage_steps_with_ai`](./step-10-lineage-handover-documentation/enrich_lineage_steps_with_ai/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Optionally enrich deterministic lineage steps using an AI helper callable.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`extract_business_keys`](./step-03-source-contract-ingestion-pattern/extract_business_keys/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract business-key column names from a normalized contract.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`extract_classifications`](./step-03-source-contract-ingestion-pattern/extract_classifications/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract column classification mappings from a normalized contract.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`extract_optional_columns`](./step-03-source-contract-ingestion-pattern/extract_optional_columns/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract optional column names from a normalized contract.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`extract_quality_rules`](./step-03-source-contract-ingestion-pattern/extract_quality_rules/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract raw quality-rule definitions from a normalized contract.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`fallback_copilot_lineage_prompt`](./step-10-lineage-handover-documentation/fallback_copilot_lineage_prompt/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build a fallback Copilot prompt for manual lineage enrichment.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`generate_dq_rule_candidates_with_fabric_ai`](./step-08-ai-assisted-dq-suggestions/generate_dq_rule_candidates_with_fabric_ai/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Append AI-suggested DQ rule candidates to a profiling DataFrame.</td>
      <td data-label="Related helpers">[`_require_fabric_ai_dataframe`](./internal/ai/_require_fabric_ai_dataframe.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`generate_governance_candidates_with_fabric_ai`](./step-09-ai-assisted-classification/generate_governance_candidates_with_fabric_ai/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Execute Fabric AI Functions to append governance suggestions to a DataFrame.</td>
      <td data-label="Related helpers">[`_require_fabric_ai_dataframe`](./internal/ai/_require_fabric_ai_dataframe.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`generate_handover_summary_with_fabric_ai`](./step-10-lineage-handover-documentation/generate_handover_summary_with_fabric_ai/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Execute Fabric AI Functions to append handover summary suggestions.</td>
      <td data-label="Related helpers">[`_require_fabric_ai_dataframe`](./internal/ai/_require_fabric_ai_dataframe.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`get_default_dq_rule_templates`](./step-08-ai-assisted-dq-suggestions/get_default_dq_rule_templates/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Return editable example data quality rules.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`lakehouse_csv_read`](./step-03-source-contract-ingestion-pattern/lakehouse_csv_read/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a CSV file from a Fabric lakehouse Files path.</td>
      <td data-label="Related helpers">[`_get_spark`](./internal/fabric_io/_get_spark.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`lakehouse_excel_read_as_spark`](./step-03-source-contract-ingestion-pattern/lakehouse_excel_read_as_spark/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read an Excel file from a Fabric lakehouse Files path.</td>
      <td data-label="Related helpers">[`_get_spark`](./internal/fabric_io/_get_spark.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`lakehouse_parquet_read_as_spark`](./step-03-source-contract-ingestion-pattern/lakehouse_parquet_read_as_spark/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a Parquet file from a Fabric lakehouse Files path.</td>
      <td data-label="Related helpers">[`_convert_single_parquet_ns_to_us`](./internal/fabric_io/_convert_single_parquet_ns_to_us.md) (internal), [`_get_spark`](./internal/fabric_io/_get_spark.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`load_contract_from_lakehouse`](./step-03-source-contract-ingestion-pattern/load_contract_from_lakehouse/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Load one contract by ID/version from Fabric metadata storage.</td>
      <td data-label="Related helpers">[`_select_latest`](./internal/contracts/_select_latest.md) (internal), [`_to_records`](./internal/contracts/_to_records.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`load_data_contract`](./step-03-source-contract-ingestion-pattern/load_data_contract/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Load and normalize a data product contract from file path or dictionary.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`parse_manual_ai_json_response`](./step-10-lineage-handover-documentation/parse_manual_ai_json_response/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Parse manual AI JSON output into Python objects.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`plot_lineage_steps`](./step-10-lineage-handover-documentation/plot_lineage_steps/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Render lineage steps as a directed graph figure.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`profile_dataframe`](./step-04-ingest-profile-store/profile_dataframe/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build a lightweight profile for pandas or Spark-like DataFrames.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`profile_metadata_to_records`](./step-04-ingest-profile-store/profile_metadata_to_records/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert Spark metadata profile rows into JSON-friendly dictionaries.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`render_run_summary_markdown`](./step-10-lineage-handover-documentation/render_run_summary_markdown/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Render a run summary dictionary into Markdown for handover notes.</td>
      <td data-label="Related helpers">[`_status_of`](./internal/run_summary/_status_of.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`run_data_product`](./step-06a-transformation-logic/run_data_product/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Run the starter kit workflow end-to-end for a data product outcome.</td>
      <td data-label="Related helpers">[`_effective_contract_dict`](./internal/quality/_effective_contract_dict.md) (internal), [`_refresh_mode`](./internal/quality/_refresh_mode.md) (internal), [`_runtime_validation_contract`](./internal/quality/_runtime_validation_contract.md) (internal), [`_write_dataframe_to_table`](./internal/quality/_write_dataframe_to_table.md) (internal), [`_write_records_spark`](./internal/quality/_write_records_spark.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`run_quality_rules`](./step-06c-pipeline-controls/run_quality_rules/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Execute quality rules against a dataframe and return structured results.</td>
      <td data-label="Related helpers">[`_normalize_severity`](./internal/quality/_normalize_severity.md) (internal), [`_now_iso`](./internal/quality/_now_iso.md) (internal), [`_pandas_rule`](./internal/quality/_pandas_rule.md) (internal), [`_resolve_engine`](./internal/quality/_resolve_engine.md) (internal), [`_result_from_counts`](./internal/quality/_result_from_counts.md) (internal), [`_spark_rule`](./internal/quality/_spark_rule.md) (internal), [`_to_jsonable`](./internal/quality/_to_jsonable.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`scan_notebook_cells`](./step-10-lineage-handover-documentation/scan_notebook_cells/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Scan multiple notebook cells and append cell references to lineage steps.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`scan_notebook_lineage`](./step-10-lineage-handover-documentation/scan_notebook_lineage/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Extract deterministic lineage steps from notebook code using AST parsing.</td>
      <td data-label="Related helpers">[`_call_name`](./internal/lineage/_call_name.md) (internal), [`_flatten_chain`](./internal/lineage/_flatten_chain.md) (internal), [`_name`](./internal/lineage/_name.md) (internal), [`_resolve_write_target`](./internal/lineage/_resolve_write_target.md) (internal), [`_step`](./internal/lineage/_step.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`suggest_accepted_value_mapping_prompt`](./step-08-ai-assisted-dq-suggestions/suggest_accepted_value_mapping_prompt/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build a constrained prompt for accepted-value mapping suggestions.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`suggest_closest_accepted_value`](./step-08-ai-assisted-dq-suggestions/suggest_closest_accepted_value/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Suggest a deterministic closest accepted value using ``difflib``.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`summarize_drift_results`](./step-04-ingest-profile-store/summarize_drift_results/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Summarize schema, partition, and profile drift outcomes into one decision.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`summarize_governance_classifications`](./step-09-ai-assisted-classification/summarize_governance_classifications/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Summarize governance classification outputs into review-friendly counts.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`validate_lineage_steps`](./step-10-lineage-handover-documentation/validate_lineage_steps/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Validate lineage step structure and flag records requiring human review.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`write_governance_classifications`](./step-09-ai-assisted-classification/write_governance_classifications/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Persist governance classifications to a metadata destination.</td>
      <td data-label="Related helpers">[`_spark_create_governance_metadata_dataframe`](./internal/governance/_spark_create_governance_metadata_dataframe.md) (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`write_metadata_records`](./step-07-output-profile-product-contract/write_metadata_records/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Write metadata records to a configured metadata sink.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class">[`write_multiple_metadata_outputs`](./step-07-output-profile-product-contract/write_multiple_metadata_outputs/)</td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Write multiple metadata payloads to their configured destinations.</td>
      <td data-label="Related helpers">—</td>
    </tr>
  </tbody>
</table>

