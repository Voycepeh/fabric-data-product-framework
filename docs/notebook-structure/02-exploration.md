# `02_ex_<agreement>_<topic>`

Exploration notebook flow used to profile source data and draft advisory AI outputs for human review.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/02_ex_agreement_topic.ipynb">Open template notebook</a>

> `02_ex` is AI-assisted exploration and human review.

## Segment 1: Load shared config and runtime

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
      <td data-label="Function / class"><a href="../reference/step-02a-shared-runtime-config/load_fabric_config/"><code>load_fabric_config</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate and return a user-supplied framework configuration.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../reference/step-01-governance-context/validate_notebook_name/"><code>validate_notebook_name</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate notebook names against the framework workspace notebook model.</td>
      <td data-label="Related helpers"><a href="../reference/internal/runtime/_infer_notebook_name_from_runtime.md"><code>_infer_notebook_name_from_runtime</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../reference/step-01-governance-context/assert_notebook_name_valid/"><code>assert_notebook_name_valid</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Raise :class:`NotebookNamingError` when a notebook name is invalid.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../reference/step-01-governance-context/build_runtime_context/"><code>build_runtime_context</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build a standard runtime context dictionary for Fabric notebooks.</td>
      <td data-label="Related helpers"><a href="../reference/internal/runtime/_infer_notebook_name_from_runtime.md"><code>_infer_notebook_name_from_runtime</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../reference/step-02a-shared-runtime-config/get_path/"><code>get_path</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Resolve a configured Fabric path for an environment and target.</td>
      <td data-label="Related helpers">—</td>
    </tr>
  </tbody>
</table>

## Segment 2: Profile source and capture evidence

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
      <td data-label="Function / class"><a href="../reference/step-04-ingest-profile-store/seed_minimal_sample_source_table/"><code>seed_minimal_sample_source_table</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Create and persist deterministic demo rows into a sample source table.</td>
      <td data-label="Related helpers"><a href="../reference/internal/fabric_io/_get_spark.md"><code>_get_spark</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../reference/step-03-source-contract-ingestion-pattern/lakehouse_table_read/"><code>lakehouse_table_read</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a Delta table from a Fabric lakehouse.</td>
      <td data-label="Related helpers"><a href="../reference/internal/fabric_io/_get_spark.md"><code>_get_spark</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../reference/step-03-source-contract-ingestion-pattern/warehouse_read/"><code>warehouse_read</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a table from a Microsoft Fabric warehouse.</td>
      <td data-label="Related helpers"><a href="../reference/internal/fabric_io/_get_spark.md"><code>_get_spark</code></a> (internal)</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../reference/step-04-ingest-profile-store/generate_metadata_profile/"><code>generate_metadata_profile</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Generate standard metadata profile rows for a Spark/Fabric DataFrame.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../reference/step-04-ingest-profile-store/profile_dataframe_to_metadata/"><code>profile_dataframe_to_metadata</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Profile a Spark/Fabric DataFrame into metadata-compatible metadata rows.</td>
      <td data-label="Related helpers">—</td>
    </tr>
  </tbody>
</table>

## Segment 3: AI-assisted drafting (advisory only)

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
      <td data-label="Function / class"><a href="../reference/step-08-ai-assisted-dq-suggestions/suggest_dq_rules_prompt/"><code>suggest_dq_rules_prompt</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build a prompt for candidate DQ rule suggestions.</td>
      <td data-label="Related helpers">—</td>
    </tr>
  </tbody>
</table>

## Segment 4: Human approval and contract write

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
      <td data-label="Function / class"><a href="../reference/step-03-source-contract-ingestion-pattern/normalize_contract_dict/"><code>normalize_contract_dict</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Normalize a notebook-authored contract dictionary to a stable shape.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../reference/step-03-source-contract-ingestion-pattern/validate_contract_dict/"><code>validate_contract_dict</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate a contract dictionary and return error strings without raising.</td>
      <td data-label="Related helpers">—</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../reference/step-07-output-profile-product-contract/write_contract_to_lakehouse/"><code>write_contract_to_lakehouse</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate and persist contract records into Fabric metadata tables.</td>
      <td data-label="Related helpers">—</td>
    </tr>
  </tbody>
</table>

## Optional lineage notes

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
      <td data-label="Function / class"><a href="../reference/step-10-lineage-handover-documentation/build_lineage_from_notebook_code/"><code>build_lineage_from_notebook_code</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Scan, optionally enrich, and validate lineage from notebook source code.</td>
      <td data-label="Related helpers">—</td>
    </tr>
  </tbody>
</table>

