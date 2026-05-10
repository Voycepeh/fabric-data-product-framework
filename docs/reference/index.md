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
      <td data-label="Notebook"><code>00_env_config</code></td>
      <td data-label="Guided usage">Shared environment bootstrap and validation before exploration or pipeline notebooks run.</td>
      <td data-label="Full template"><a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/00_env_config.ipynb">Open notebook</a></td>
    </tr>
    <tr>
      <td data-label="Notebook"><code>02_ex_&lt;agreement&gt;_&lt;topic&gt;</code></td>
      <td data-label="Guided usage">Exploration notebook flow used to profile source data and draft advisory AI outputs for human review.</td>
      <td data-label="Full template"><a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/02_ex_agreement_topic.ipynb">Open notebook</a></td>
    </tr>
    <tr>
      <td data-label="Notebook"><code>03_pc_&lt;agreement&gt;_&lt;pipeline&gt;</code></td>
      <td data-label="Guided usage">Pipeline-contract notebook flow for deterministic enforcement and controlled publishing.</td>
      <td data-label="Full template"><a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/03_pc_agreement_source_to_target.ipynb">Open notebook</a></td>
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
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/Housepath/"><code>Housepath</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Fabric lakehouse or warehouse connection details.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/create_path_config/"><code>create_path_config</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create environment-to-target routing used by Fabric IO helpers.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/create_notebook_runtime_config/"><code>create_notebook_runtime_config</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create notebook naming-policy configuration for runtime guards.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/validate_framework_config/"><code>validate_framework_config</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate and normalize framework configuration input.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/load_fabric_config/"><code>load_fabric_config</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate and return a user-supplied framework configuration.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/get_path/"><code>get_path</code></a></td>
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
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/create_ai_prompt_config/"><code>create_ai_prompt_config</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create the AI prompt-template configuration used by FabricOps.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/create_governance_config/"><code>create_governance_config</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create governance policy defaults for FabricOps runtime checks.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/create_quality_config/"><code>create_quality_config</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create the default quality policy used during FabricOps checks.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/create_lineage_config/"><code>create_lineage_config</code></a></td>
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
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/create_framework_config/"><code>create_framework_config</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create the top-level FabricOps framework configuration contract.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/validate_framework_config/"><code>validate_framework_config</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate and normalize framework configuration input.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/load_fabric_config/"><code>load_fabric_config</code></a></td>
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
      <td data-label="Function / class"><a href="./step-02b-notebook-startup-checks/run_config_smoke_tests/"><code>run_config_smoke_tests</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Run 00_env_config smoke checks for Spark, runtime context, configured paths, notebook naming, and optional AI/IO imports.</td>
      <td data-label="Related helpers"><a href="./internal/config/_check_spark_session.md"><code>_check_spark_session</code></a> (internal), <a href="./internal/config/_get_fabric_runtime_metadata.md"><code>_get_fabric_runtime_metadata</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02b-notebook-startup-checks/bootstrap_fabric_env/"><code>bootstrap_fabric_env</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Bootstrap 00_env_config environment readiness by resolving required targets and collecting runtime/AI check results.</td>
      <td data-label="Related helpers"><a href="./internal/config/_get_fabric_runtime_metadata.md"><code>_get_fabric_runtime_metadata</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/check_fabric_ai_functions_available/"><code>check_fabric_ai_functions_available</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Check whether Fabric AI Functions are available in the current runtime.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-01-governance-context/configure_fabric_ai_functions/"><code>configure_fabric_ai_functions</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Apply optional default Fabric AI Function configuration.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/get_path/"><code>get_path</code></a></td>
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
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/load_fabric_config/"><code>load_fabric_config</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate and return a user-supplied framework configuration.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-01-governance-context/validate_notebook_name/"><code>validate_notebook_name</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate notebook names against the framework workspace notebook model.</td>
      <td data-label="Related helpers"><a href="./internal/runtime/_infer_notebook_name_from_runtime.md"><code>_infer_notebook_name_from_runtime</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-01-governance-context/assert_notebook_name_valid/"><code>assert_notebook_name_valid</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Raise :class:`NotebookNamingError` when a notebook name is invalid.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-01-governance-context/build_runtime_context/"><code>build_runtime_context</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build a standard runtime context dictionary for Fabric notebooks.</td>
      <td data-label="Related helpers"><a href="./internal/runtime/_infer_notebook_name_from_runtime.md"><code>_infer_notebook_name_from_runtime</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/get_path/"><code>get_path</code></a></td>
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
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/lakehouse_table_read/"><code>lakehouse_table_read</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a Delta table from a Fabric lakehouse.</td>
      <td data-label="Related helpers"><a href="./internal/fabric_io/_get_spark.md"><code>_get_spark</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/warehouse_read/"><code>warehouse_read</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a table from a Microsoft Fabric warehouse.</td>
      <td data-label="Related helpers"><a href="./internal/fabric_io/_get_spark.md"><code>_get_spark</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/generate_metadata_profile/"><code>generate_metadata_profile</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Generate standard metadata profile rows for a Spark/Fabric DataFrame.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/profile_dataframe_to_metadata/"><code>profile_dataframe_to_metadata</code></a></td>
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
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/suggest_dq_rules_prompt/"><code>suggest_dq_rules_prompt</code></a></td>
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
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/normalize_contract_dict/"><code>normalize_contract_dict</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Normalize a notebook-authored contract dictionary to a stable shape.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/validate_contract_dict/"><code>validate_contract_dict</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate a contract dictionary and return error strings without raising.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/write_contract_to_lakehouse/"><code>write_contract_to_lakehouse</code></a></td>
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
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/build_lineage_from_notebook_code/"><code>build_lineage_from_notebook_code</code></a></td>
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
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/load_fabric_config/"><code>load_fabric_config</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate and return a user-supplied framework configuration.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-01-governance-context/validate_notebook_name/"><code>validate_notebook_name</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate notebook names against the framework workspace notebook model.</td>
      <td data-label="Related helpers"><a href="./internal/runtime/_infer_notebook_name_from_runtime.md"><code>_infer_notebook_name_from_runtime</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-01-governance-context/assert_notebook_name_valid/"><code>assert_notebook_name_valid</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Raise :class:`NotebookNamingError` when a notebook name is invalid.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-01-governance-context/generate_run_id/"><code>generate_run_id</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Generate a notebook-safe run identifier.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-01-governance-context/build_runtime_context/"><code>build_runtime_context</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build a standard runtime context dictionary for Fabric notebooks.</td>
      <td data-label="Related helpers"><a href="./internal/runtime/_infer_notebook_name_from_runtime.md"><code>_infer_notebook_name_from_runtime</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/get_path/"><code>get_path</code></a></td>
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
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/load_latest_approved_contract/"><code>load_latest_approved_contract</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Load the latest approved contract for a dataset/object pair.</td>
      <td data-label="Related helpers"><a href="./internal/contracts/_select_latest.md"><code>_select_latest</code></a> (internal), <a href="./internal/contracts/_to_records.md"><code>_to_records</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/lakehouse_table_read/"><code>lakehouse_table_read</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a Delta table from a Fabric lakehouse.</td>
      <td data-label="Related helpers"><a href="./internal/fabric_io/_get_spark.md"><code>_get_spark</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/warehouse_read/"><code>warehouse_read</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a table from a Microsoft Fabric warehouse.</td>
      <td data-label="Related helpers"><a href="./internal/fabric_io/_get_spark.md"><code>_get_spark</code></a> (internal)</td>
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
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/extract_required_columns/"><code>extract_required_columns</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract required column names from a normalized contract.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-06c-pipeline-controls/get_executable_quality_rules/"><code>get_executable_quality_rules</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Return normalized quality rules ready for pipeline enforcement.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-06c-pipeline-controls/validate_dq_rules/"><code>validate_dq_rules</code></a></td>
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
      <td data-label="Function / class"><a href="./step-06c-pipeline-controls/run_dq_rules/"><code>run_dq_rules</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Run notebook-facing DQ rules and return a Spark DataFrame result.</td>
      <td data-label="Related helpers"><a href="./internal/dq/_to_quality_rule.md"><code>_to_quality_rule</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-06c-pipeline-controls/split_valid_and_quarantine/"><code>split_valid_and_quarantine</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Split a Spark DataFrame into pass/quarantine outputs for row-level DQ rules.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-06d-controlled-outputs/lakehouse_table_write/"><code>lakehouse_table_write</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Write a Spark DataFrame to a Fabric lakehouse Delta table.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-06d-controlled-outputs/warehouse_write/"><code>warehouse_write</code></a></td>
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
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/build_dataset_run_record/"><code>build_dataset_run_record</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build a dataset-run metadata record for operational tracking.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/build_quality_result_records/"><code>build_quality_result_records</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert quality-rule execution output into metadata evidence records.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/build_contract_records/"><code>build_contract_records</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build grouped contract header, column, and rule metadata payloads.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/build_lineage_records/"><code>build_lineage_records</code></a></td>
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
      <td data-label="Function / class"><a href="./step-06b-runtime-standards/add_audit_columns/"><code>add_audit_columns</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Add run tracking and audit columns for ingestion workflows.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-06b-runtime-standards/add_datetime_features/"><code>add_datetime_features</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Add localized datetime feature columns derived from a UTC datetime column.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-06b-runtime-standards/add_hash_columns/"><code>add_hash_columns</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Add business key and row-level SHA256 hash columns.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-06d-controlled-outputs/assert_dq_passed/"><code>assert_dq_passed</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Raise when any error-severity DQ rule failed after results are logged.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-01-governance-context/assert_notebook_name_valid/"><code>assert_notebook_name_valid</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Starter path">02_ex, 03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Raise :class:`NotebookNamingError` when a notebook name is invalid.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02b-notebook-startup-checks/bootstrap_fabric_env/"><code>bootstrap_fabric_env</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Bootstrap 00_env_config environment readiness by resolving required targets and collecting runtime/AI check results.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/build_ai_quality_context/"><code>build_ai_quality_context</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build deterministic AI-ready context from standard metadata profile rows.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/build_contract_column_records/"><code>build_contract_column_records</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build normalized contract-column metadata records for persistence.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/build_contract_header_record/"><code>build_contract_header_record</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build one header row for FABRICOPS_CONTRACTS.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/build_contract_records/"><code>build_contract_records</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build grouped contract header, column, and rule metadata payloads.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/build_contract_rule_records/"><code>build_contract_rule_records</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build quality-rule metadata records from a validated contract.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/build_contract_summary/"><code>build_contract_summary</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build a concise contract summary for reviews and handover.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/build_dataset_run_record/"><code>build_dataset_run_record</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build a dataset-run metadata record for operational tracking.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/build_dq_rule_candidate_prompt/"><code>build_dq_rule_candidate_prompt</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build the DQ-candidate prompt used in AI-assisted quality drafting.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/build_governance_candidate_prompt/"><code>build_governance_candidate_prompt</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build the governance-candidate prompt for AI-assisted classification drafts.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/build_governance_classification_records/"><code>build_governance_classification_records</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build metadata-ready governance classification records from column suggestions.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/build_handover_summary_prompt/"><code>build_handover_summary_prompt</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build the handover-summary prompt for AI-assisted run handoff drafting.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/build_lineage_from_notebook_code/"><code>build_lineage_from_notebook_code</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">02_ex</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Scan, optionally enrich, and validate lineage from notebook source code.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/build_lineage_handover_markdown/"><code>build_lineage_handover_markdown</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Create a concise markdown handover summary from lineage execution results.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/build_lineage_record_from_steps/"><code>build_lineage_record_from_steps</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Create metadata-ready lineage records from validated lineage steps.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/build_lineage_records/"><code>build_lineage_records</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build compact lineage records for downstream metadata sinks.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/build_manual_dq_rule_prompt_package/"><code>build_manual_dq_rule_prompt_package</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build copy/paste prompt package for manual DQ candidate generation.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/build_manual_governance_prompt_package/"><code>build_manual_governance_prompt_package</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build copy/paste prompt package for manual governance suggestion generation.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/build_manual_handover_prompt_package/"><code>build_manual_handover_prompt_package</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build copy/paste prompt package for manual handover summary generation.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/build_quality_result_records/"><code>build_quality_result_records</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert quality-rule execution output into metadata evidence records.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/build_run_summary/"><code>build_run_summary</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build a handover-friendly summary for one data product run.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-01-governance-context/build_runtime_context/"><code>build_runtime_context</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Starter path">02_ex, 03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build a standard runtime context dictionary for Fabric notebooks.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/build_schema_drift_records/"><code>build_schema_drift_records</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert schema drift results into metadata records for audit trails.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/build_schema_snapshot_records/"><code>build_schema_snapshot_records</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert a schema snapshot into row-wise metadata records.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/check_fabric_ai_functions_available/"><code>check_fabric_ai_functions_available</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Check whether Fabric AI Functions are available in the current runtime.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/check_partition_drift/"><code>check_partition_drift</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Check partition-level drift using keys, partitions, and optional watermark baselines.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/check_profile_drift/"><code>check_profile_drift</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Compare profile metrics against a baseline profile and drift thresholds.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/check_schema_drift/"><code>check_schema_drift</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Compare a current dataframe schema against a baseline schema snapshot.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/classify_column/"><code>classify_column</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Classify one column using term matching, metadata cues, and business context.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/classify_columns/"><code>classify_columns</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Classify multiple columns and return normalized governance suggestions.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-01-governance-context/configure_fabric_ai_functions/"><code>configure_fabric_ai_functions</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Apply optional default Fabric AI Function configuration.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/contract_records_to_spark/"><code>contract_records_to_spark</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert record dictionaries into a Spark DataFrame when Spark is available.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/create_ai_prompt_config/"><code>create_ai_prompt_config</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create the AI prompt-template configuration used by FabricOps.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/create_framework_config/"><code>create_framework_config</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create the top-level FabricOps framework configuration contract.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/create_governance_config/"><code>create_governance_config</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create governance policy defaults for FabricOps runtime checks.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/create_lineage_config/"><code>create_lineage_config</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create lineage capture defaults for FabricOps handover traceability.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/create_notebook_runtime_config/"><code>create_notebook_runtime_config</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create notebook naming-policy configuration for runtime guards.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/create_path_config/"><code>create_path_config</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create environment-to-target routing used by Fabric IO helpers.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/create_quality_config/"><code>create_quality_config</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create the default quality policy used during FabricOps checks.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE/"><code>DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Default prompt template used to draft candidate DQ rules.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-06b-runtime-standards/default_technical_columns/"><code>default_technical_columns</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Return framework-generated and legacy technical column names to ignore.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/enrich_lineage_steps_with_ai/"><code>enrich_lineage_steps_with_ai</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Optionally enrich deterministic lineage steps using an AI helper callable.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/extract_business_keys/"><code>extract_business_keys</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract business-key column names from a normalized contract.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/extract_classifications/"><code>extract_classifications</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract column classification mappings from a normalized contract.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/extract_optional_columns/"><code>extract_optional_columns</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract optional column names from a normalized contract.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/extract_quality_rules/"><code>extract_quality_rules</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract raw quality-rule definitions from a normalized contract.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/extract_required_columns/"><code>extract_required_columns</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract required column names from a normalized contract.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/fallback_copilot_lineage_prompt/"><code>fallback_copilot_lineage_prompt</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build a fallback Copilot prompt for manual lineage enrichment.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/generate_dq_rule_candidates_with_fabric_ai/"><code>generate_dq_rule_candidates_with_fabric_ai</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Append AI-suggested DQ rule candidates to a profiling DataFrame.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/generate_governance_candidates_with_fabric_ai/"><code>generate_governance_candidates_with_fabric_ai</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Execute Fabric AI Functions to append governance suggestions to a DataFrame.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/generate_handover_summary_with_fabric_ai/"><code>generate_handover_summary_with_fabric_ai</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Execute Fabric AI Functions to append handover summary suggestions.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/generate_metadata_profile/"><code>generate_metadata_profile</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Starter path">02_ex</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Generate standard metadata profile rows for a Spark/Fabric DataFrame.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-01-governance-context/generate_run_id/"><code>generate_run_id</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Generate a notebook-safe run identifier.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/get_default_dq_rule_templates/"><code>get_default_dq_rule_templates</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Return editable example data quality rules.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-06c-pipeline-controls/get_executable_quality_rules/"><code>get_executable_quality_rules</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Return normalized quality rules ready for pipeline enforcement.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/get_path/"><code>get_path</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config, 02_ex, 03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Resolve a configured Fabric path for an environment and target.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/Housepath/"><code>Housepath</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Fabric lakehouse or warehouse connection details.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/lakehouse_csv_read/"><code>lakehouse_csv_read</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a CSV file from a Fabric lakehouse Files path.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/lakehouse_excel_read_as_spark/"><code>lakehouse_excel_read_as_spark</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read an Excel file from a Fabric lakehouse Files path.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/lakehouse_parquet_read_as_spark/"><code>lakehouse_parquet_read_as_spark</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a Parquet file from a Fabric lakehouse Files path.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/lakehouse_table_read/"><code>lakehouse_table_read</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">02_ex, 03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a Delta table from a Fabric lakehouse.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-06d-controlled-outputs/lakehouse_table_write/"><code>lakehouse_table_write</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Write a Spark DataFrame to a Fabric lakehouse Delta table.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/load_contract_from_lakehouse/"><code>load_contract_from_lakehouse</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Load one contract by ID/version from Fabric metadata storage.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/load_data_contract/"><code>load_data_contract</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Load and normalize a data product contract from file path or dictionary.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/load_fabric_config/"><code>load_fabric_config</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config, 02_ex, 03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate and return a user-supplied framework configuration.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/load_latest_approved_contract/"><code>load_latest_approved_contract</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Load the latest approved contract for a dataset/object pair.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/normalize_contract_dict/"><code>normalize_contract_dict</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">02_ex</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Normalize a notebook-authored contract dictionary to a stable shape.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/parse_manual_ai_json_response/"><code>parse_manual_ai_json_response</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Parse manual AI JSON output into Python objects.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/plot_lineage_steps/"><code>plot_lineage_steps</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Render lineage steps as a directed graph figure.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/profile_dataframe/"><code>profile_dataframe</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build a lightweight profile for pandas or Spark-like DataFrames.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/profile_dataframe_to_metadata/"><code>profile_dataframe_to_metadata</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Starter path">02_ex</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Profile a Spark/Fabric DataFrame into metadata-compatible metadata rows.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/profile_metadata_to_records/"><code>profile_metadata_to_records</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert Spark metadata profile rows into JSON-friendly dictionaries.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/render_run_summary_markdown/"><code>render_run_summary_markdown</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Render a run summary dictionary into Markdown for handover notes.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02b-notebook-startup-checks/run_config_smoke_tests/"><code>run_config_smoke_tests</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Run 00_env_config smoke checks for Spark, runtime context, configured paths, notebook naming, and optional AI/IO imports.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-06a-transformation-logic/run_data_product/"><code>run_data_product</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Run the starter kit workflow end-to-end for a data product outcome.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-06c-pipeline-controls/run_dq_rules/"><code>run_dq_rules</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Run notebook-facing DQ rules and return a Spark DataFrame result.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-06c-pipeline-controls/run_quality_rules/"><code>run_quality_rules</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Execute quality rules against a dataframe and return structured results.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/scan_notebook_cells/"><code>scan_notebook_cells</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Scan multiple notebook cells and append cell references to lineage steps.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/scan_notebook_lineage/"><code>scan_notebook_lineage</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Extract deterministic lineage steps from notebook code using AST parsing.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-06c-pipeline-controls/split_valid_and_quarantine/"><code>split_valid_and_quarantine</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Split a Spark DataFrame into pass/quarantine outputs for row-level DQ rules.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/suggest_accepted_value_mapping_prompt/"><code>suggest_accepted_value_mapping_prompt</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build a constrained prompt for accepted-value mapping suggestions.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/suggest_closest_accepted_value/"><code>suggest_closest_accepted_value</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Suggest a deterministic closest accepted value using ``difflib``.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/suggest_dq_rules_prompt/"><code>suggest_dq_rules_prompt</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">02_ex</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build a prompt for candidate DQ rule suggestions.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/summarize_drift_results/"><code>summarize_drift_results</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Summarize schema, partition, and profile drift outcomes into one decision.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/summarize_governance_classifications/"><code>summarize_governance_classifications</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Summarize governance classification outputs into review-friendly counts.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/validate_contract_dict/"><code>validate_contract_dict</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">02_ex</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate a contract dictionary and return error strings without raising.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-06c-pipeline-controls/validate_dq_rules/"><code>validate_dq_rules</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate notebook-facing DQ rules.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/validate_framework_config/"><code>validate_framework_config</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate and normalize framework configuration input.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/validate_lineage_steps/"><code>validate_lineage_steps</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Validate lineage step structure and flag records requiring human review.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-01-governance-context/validate_notebook_name/"><code>validate_notebook_name</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Starter path">02_ex, 03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate notebook names against the framework workspace notebook model.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/warehouse_read/"><code>warehouse_read</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">02_ex, 03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a table from a Microsoft Fabric warehouse.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-06d-controlled-outputs/warehouse_write/"><code>warehouse_write</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Write a Spark DataFrame to a Microsoft Fabric warehouse table.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/write_contract_to_lakehouse/"><code>write_contract_to_lakehouse</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">02_ex</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate and persist contract records into Fabric metadata tables.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/write_governance_classifications/"><code>write_governance_classifications</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Persist governance classifications to a metadata destination.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/write_metadata_records/"><code>write_metadata_records</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Write metadata records to a configured metadata sink.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/write_multiple_metadata_outputs/"><code>write_multiple_metadata_outputs</code></a></td>
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
      <td data-label="Function / class"><a href="./step-06b-runtime-standards/add_audit_columns/"><code>add_audit_columns</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Add run tracking and audit columns for ingestion workflows.</td>
      <td data-label="Related helpers"><a href="./internal/technical_columns/_assert_columns_exist.md"><code>_assert_columns_exist</code></a> (internal), <a href="./internal/technical_columns/_bucket_values_pandas.md"><code>_bucket_values_pandas</code></a> (internal), <a href="./internal/technical_columns/_get_fabric_runtime_context.md"><code>_get_fabric_runtime_context</code></a> (internal), <a href="./internal/technical_columns/_resolve_engine.md"><code>_resolve_engine</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-06b-runtime-standards/add_datetime_features/"><code>add_datetime_features</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Add localized datetime feature columns derived from a UTC datetime column.</td>
      <td data-label="Related helpers"><a href="./internal/technical_columns/_assert_columns_exist.md"><code>_assert_columns_exist</code></a> (internal), <a href="./internal/technical_columns/_resolve_engine.md"><code>_resolve_engine</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-06b-runtime-standards/add_hash_columns/"><code>add_hash_columns</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Add business key and row-level SHA256 hash columns.</td>
      <td data-label="Related helpers"><a href="./internal/technical_columns/_assert_columns_exist.md"><code>_assert_columns_exist</code></a> (internal), <a href="./internal/technical_columns/_hash_row.md"><code>_hash_row</code></a> (internal), <a href="./internal/technical_columns/_non_technical_columns.md"><code>_non_technical_columns</code></a> (internal), <a href="./internal/technical_columns/_resolve_engine.md"><code>_resolve_engine</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-06d-controlled-outputs/assert_dq_passed/"><code>assert_dq_passed</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Raise when any error-severity DQ rule failed after results are logged.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/build_ai_quality_context/"><code>build_ai_quality_context</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build deterministic AI-ready context from standard metadata profile rows.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/build_contract_column_records/"><code>build_contract_column_records</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build normalized contract-column metadata records for persistence.</td>
      <td data-label="Related helpers"><a href="./internal/contracts/_now_utc_iso.md"><code>_now_utc_iso</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/build_contract_header_record/"><code>build_contract_header_record</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build one header row for FABRICOPS_CONTRACTS.</td>
      <td data-label="Related helpers"><a href="./internal/contracts/_now_utc_iso.md"><code>_now_utc_iso</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/build_contract_rule_records/"><code>build_contract_rule_records</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build quality-rule metadata records from a validated contract.</td>
      <td data-label="Related helpers"><a href="./internal/contracts/_now_utc_iso.md"><code>_now_utc_iso</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/build_contract_summary/"><code>build_contract_summary</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build a concise contract summary for reviews and handover.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/build_dq_rule_candidate_prompt/"><code>build_dq_rule_candidate_prompt</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build the DQ-candidate prompt used in AI-assisted quality drafting.</td>
      <td data-label="Related helpers"><a href="./internal/ai/_resolve_prompt_template.md"><code>_resolve_prompt_template</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/build_governance_candidate_prompt/"><code>build_governance_candidate_prompt</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build the governance-candidate prompt for AI-assisted classification drafts.</td>
      <td data-label="Related helpers"><a href="./internal/ai/_resolve_prompt_template.md"><code>_resolve_prompt_template</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/build_governance_classification_records/"><code>build_governance_classification_records</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build metadata-ready governance classification records from column suggestions.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/build_handover_summary_prompt/"><code>build_handover_summary_prompt</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build the handover-summary prompt for AI-assisted run handoff drafting.</td>
      <td data-label="Related helpers"><a href="./internal/ai/_resolve_prompt_template.md"><code>_resolve_prompt_template</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/build_lineage_handover_markdown/"><code>build_lineage_handover_markdown</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Create a concise markdown handover summary from lineage execution results.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/build_lineage_record_from_steps/"><code>build_lineage_record_from_steps</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Create metadata-ready lineage records from validated lineage steps.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/build_manual_dq_rule_prompt_package/"><code>build_manual_dq_rule_prompt_package</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build copy/paste prompt package for manual DQ candidate generation.</td>
      <td data-label="Related helpers"><a href="./internal/ai/_compact_sample_rows.md"><code>_compact_sample_rows</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/build_manual_governance_prompt_package/"><code>build_manual_governance_prompt_package</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build copy/paste prompt package for manual governance suggestion generation.</td>
      <td data-label="Related helpers"><a href="./internal/ai/_compact_sample_rows.md"><code>_compact_sample_rows</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/build_manual_handover_prompt_package/"><code>build_manual_handover_prompt_package</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build copy/paste prompt package for manual handover summary generation.</td>
      <td data-label="Related helpers"><a href="./internal/ai/_compact_sample_rows.md"><code>_compact_sample_rows</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/build_run_summary/"><code>build_run_summary</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build a handover-friendly summary for one data product run.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/build_schema_drift_records/"><code>build_schema_drift_records</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert schema drift results into metadata records for audit trails.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/build_schema_snapshot_records/"><code>build_schema_snapshot_records</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert a schema snapshot into row-wise metadata records.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/check_partition_drift/"><code>check_partition_drift</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Check partition-level drift using keys, partitions, and optional watermark baselines.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/check_profile_drift/"><code>check_profile_drift</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Compare profile metrics against a baseline profile and drift thresholds.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/check_schema_drift/"><code>check_schema_drift</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Compare a current dataframe schema against a baseline schema snapshot.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/classify_column/"><code>classify_column</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Classify one column using term matching, metadata cues, and business context.</td>
      <td data-label="Related helpers"><a href="./internal/governance/_match_terms.md"><code>_match_terms</code></a> (internal), <a href="./internal/governance/_phrase_in_text.md"><code>_phrase_in_text</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/classify_columns/"><code>classify_columns</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Classify multiple columns and return normalized governance suggestions.</td>
      <td data-label="Related helpers"><a href="./internal/governance/_column_name.md"><code>_column_name</code></a> (internal), <a href="./internal/governance/_normalize_columns.md"><code>_normalize_columns</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/contract_records_to_spark/"><code>contract_records_to_spark</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert record dictionaries into a Spark DataFrame when Spark is available.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE/"><code>DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Default prompt template used to draft candidate DQ rules.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-06b-runtime-standards/default_technical_columns/"><code>default_technical_columns</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Return framework-generated and legacy technical column names to ignore.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/enrich_lineage_steps_with_ai/"><code>enrich_lineage_steps_with_ai</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Optionally enrich deterministic lineage steps using an AI helper callable.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/extract_business_keys/"><code>extract_business_keys</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract business-key column names from a normalized contract.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/extract_classifications/"><code>extract_classifications</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract column classification mappings from a normalized contract.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/extract_optional_columns/"><code>extract_optional_columns</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract optional column names from a normalized contract.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/extract_quality_rules/"><code>extract_quality_rules</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract raw quality-rule definitions from a normalized contract.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/fallback_copilot_lineage_prompt/"><code>fallback_copilot_lineage_prompt</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build a fallback Copilot prompt for manual lineage enrichment.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/generate_dq_rule_candidates_with_fabric_ai/"><code>generate_dq_rule_candidates_with_fabric_ai</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Append AI-suggested DQ rule candidates to a profiling DataFrame.</td>
      <td data-label="Related helpers"><a href="./internal/ai/_require_fabric_ai_dataframe.md"><code>_require_fabric_ai_dataframe</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/generate_governance_candidates_with_fabric_ai/"><code>generate_governance_candidates_with_fabric_ai</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Execute Fabric AI Functions to append governance suggestions to a DataFrame.</td>
      <td data-label="Related helpers"><a href="./internal/ai/_require_fabric_ai_dataframe.md"><code>_require_fabric_ai_dataframe</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/generate_handover_summary_with_fabric_ai/"><code>generate_handover_summary_with_fabric_ai</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Execute Fabric AI Functions to append handover summary suggestions.</td>
      <td data-label="Related helpers"><a href="./internal/ai/_require_fabric_ai_dataframe.md"><code>_require_fabric_ai_dataframe</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/get_default_dq_rule_templates/"><code>get_default_dq_rule_templates</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Return editable example data quality rules.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/lakehouse_csv_read/"><code>lakehouse_csv_read</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a CSV file from a Fabric lakehouse Files path.</td>
      <td data-label="Related helpers"><a href="./internal/fabric_io/_get_spark.md"><code>_get_spark</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/lakehouse_excel_read_as_spark/"><code>lakehouse_excel_read_as_spark</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read an Excel file from a Fabric lakehouse Files path.</td>
      <td data-label="Related helpers"><a href="./internal/fabric_io/_get_spark.md"><code>_get_spark</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/lakehouse_parquet_read_as_spark/"><code>lakehouse_parquet_read_as_spark</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a Parquet file from a Fabric lakehouse Files path.</td>
      <td data-label="Related helpers"><a href="./internal/fabric_io/_convert_single_parquet_ns_to_us.md"><code>_convert_single_parquet_ns_to_us</code></a> (internal), <a href="./internal/fabric_io/_get_spark.md"><code>_get_spark</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/load_contract_from_lakehouse/"><code>load_contract_from_lakehouse</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Load one contract by ID/version from Fabric metadata storage.</td>
      <td data-label="Related helpers"><a href="./internal/contracts/_select_latest.md"><code>_select_latest</code></a> (internal), <a href="./internal/contracts/_to_records.md"><code>_to_records</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/load_data_contract/"><code>load_data_contract</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Load and normalize a data product contract from file path or dictionary.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/parse_manual_ai_json_response/"><code>parse_manual_ai_json_response</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Parse manual AI JSON output into Python objects.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/plot_lineage_steps/"><code>plot_lineage_steps</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Render lineage steps as a directed graph figure.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/profile_dataframe/"><code>profile_dataframe</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build a lightweight profile for pandas or Spark-like DataFrames.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/profile_metadata_to_records/"><code>profile_metadata_to_records</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert Spark metadata profile rows into JSON-friendly dictionaries.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/render_run_summary_markdown/"><code>render_run_summary_markdown</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Render a run summary dictionary into Markdown for handover notes.</td>
      <td data-label="Related helpers"><a href="./internal/run_summary/_status_of.md"><code>_status_of</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-06a-transformation-logic/run_data_product/"><code>run_data_product</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Run the starter kit workflow end-to-end for a data product outcome.</td>
      <td data-label="Related helpers"><a href="./internal/quality/_effective_contract_dict.md"><code>_effective_contract_dict</code></a> (internal), <a href="./internal/quality/_refresh_mode.md"><code>_refresh_mode</code></a> (internal), <a href="./internal/quality/_runtime_validation_contract.md"><code>_runtime_validation_contract</code></a> (internal), <a href="./internal/quality/_write_dataframe_to_table.md"><code>_write_dataframe_to_table</code></a> (internal), <a href="./internal/quality/_write_records_spark.md"><code>_write_records_spark</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-06c-pipeline-controls/run_quality_rules/"><code>run_quality_rules</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Execute quality rules against a dataframe and return structured results.</td>
      <td data-label="Related helpers"><a href="./internal/quality/_normalize_severity.md"><code>_normalize_severity</code></a> (internal), <a href="./internal/quality/_now_iso.md"><code>_now_iso</code></a> (internal), <a href="./internal/quality/_pandas_rule.md"><code>_pandas_rule</code></a> (internal), <a href="./internal/quality/_resolve_engine.md"><code>_resolve_engine</code></a> (internal), <a href="./internal/quality/_result_from_counts.md"><code>_result_from_counts</code></a> (internal), <a href="./internal/quality/_spark_rule.md"><code>_spark_rule</code></a> (internal), <a href="./internal/quality/_to_jsonable.md"><code>_to_jsonable</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/scan_notebook_cells/"><code>scan_notebook_cells</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Scan multiple notebook cells and append cell references to lineage steps.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/scan_notebook_lineage/"><code>scan_notebook_lineage</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Extract deterministic lineage steps from notebook code using AST parsing.</td>
      <td data-label="Related helpers"><a href="./internal/lineage/_call_name.md"><code>_call_name</code></a> (internal), <a href="./internal/lineage/_flatten_chain.md"><code>_flatten_chain</code></a> (internal), <a href="./internal/lineage/_name.md"><code>_name</code></a> (internal), <a href="./internal/lineage/_resolve_write_target.md"><code>_resolve_write_target</code></a> (internal), <a href="./internal/lineage/_step.md"><code>_step</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/suggest_accepted_value_mapping_prompt/"><code>suggest_accepted_value_mapping_prompt</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build a constrained prompt for accepted-value mapping suggestions.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/suggest_closest_accepted_value/"><code>suggest_closest_accepted_value</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Suggest a deterministic closest accepted value using ``difflib``.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/summarize_drift_results/"><code>summarize_drift_results</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Summarize schema, partition, and profile drift outcomes into one decision.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/summarize_governance_classifications/"><code>summarize_governance_classifications</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Summarize governance classification outputs into review-friendly counts.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/validate_lineage_steps/"><code>validate_lineage_steps</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Validate lineage step structure and flag records requiring human review.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/write_governance_classifications/"><code>write_governance_classifications</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Persist governance classifications to a metadata destination.</td>
      <td data-label="Related helpers"><a href="./internal/governance/_spark_create_governance_metadata_dataframe.md"><code>_spark_create_governance_metadata_dataframe</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/write_metadata_records/"><code>write_metadata_records</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Write metadata records to a configured metadata sink.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/write_multiple_metadata_outputs/"><code>write_multiple_metadata_outputs</code></a></td>
      <td data-label="Module"><a class="api-chip api-chip-module api-chip-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Write multiple metadata payloads to their configured destinations.</td>
      <td data-label="Related helpers">—</td>
    </tr>
  </tbody>
</table>

