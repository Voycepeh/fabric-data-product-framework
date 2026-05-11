# `02_ex_<agreement>_<topic>`

Exploration notebook flow used to profile source data and draft advisory AI outputs for human review.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/02_ex_agreement_topic.ipynb">Open template notebook</a>

> `02_ex` is AI-assisted exploration and human review.

## Segment 1: Load shared config and runtime

<table class="reference-function-table notebook-structure-function-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-02b-notebook-startup-checks/setup_fabricops_notebook/"><code>setup_fabricops_notebook</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Purpose">Run consolidated FabricOps startup for exploration and pipeline notebooks.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-02a-shared-runtime-config/load_fabric_config/"><code>load_fabric_config</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Purpose">Validate and return a user-supplied framework configuration.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-02a-shared-runtime-config/get_path/"><code>get_path</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Purpose">Resolve a configured Fabric path for an environment and target.</td>
    </tr>
  </tbody>
</table>

## Segment 2: Profile source and capture evidence

<table class="reference-function-table notebook-structure-function-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-04-ingest-profile-store/seed_minimal_sample_source_table/"><code>seed_minimal_sample_source_table</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Purpose">Create and persist deterministic demo rows into a sample source table.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-03-source-contract-ingestion-pattern/lakehouse_table_read/"><code>lakehouse_table_read</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Purpose">Read a Delta table from a Fabric lakehouse.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-03-source-contract-ingestion-pattern/warehouse_read/"><code>warehouse_read</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Purpose">Read a table from a Microsoft Fabric warehouse.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-04-ingest-profile-store/generate_metadata_profile/"><code>generate_metadata_profile</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Purpose">Generate standard metadata profile rows for a Spark/Fabric DataFrame.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-04-ingest-profile-store/profile_dataframe_to_metadata/"><code>profile_dataframe_to_metadata</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Purpose">Profile a Spark/Fabric DataFrame into metadata-compatible metadata rows.</td>
    </tr>
  </tbody>
</table>

## Segment 3: AI-assisted drafting (advisory only)

<table class="reference-function-table notebook-structure-function-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-08-ai-assisted-dq-suggestions/draft_dq_rules/"><code>draft_dq_rules</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Purpose">Draft candidate DQ rules from metadata profiles or raw DataFrame fallback.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-08-ai-assisted-dq-suggestions/review_dq_rules/"><code>review_dq_rules</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Purpose">Review AI-suggested DQ rules sequentially with explicit approve/reject decisions.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-08-ai-assisted-dq-suggestions/write_dq_rules/"><code>write_dq_rules</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Purpose">Validate, build, and persist approved DQ rules.</td>
    </tr>
  </tbody>
</table>

## Segment 4: Human approval and contract write

<table class="reference-function-table notebook-structure-function-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-03-source-contract-ingestion-pattern/normalize_contract_dict/"><code>normalize_contract_dict</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Purpose">Normalize a notebook-authored contract dictionary to a stable shape.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-03-source-contract-ingestion-pattern/validate_contract_dict/"><code>validate_contract_dict</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Purpose">Validate a contract dictionary and return error strings without raising.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-07-output-profile-product-contract/write_contract_to_lakehouse/"><code>write_contract_to_lakehouse</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Purpose">Validate and persist contract records into Fabric metadata tables.</td>
    </tr>
  </tbody>
</table>

## Optional lineage notes

<table class="reference-function-table notebook-structure-function-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-10-lineage-handover-documentation/build_lineage_from_notebook_code/"><code>build_lineage_from_notebook_code</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Purpose">Scan, optionally enrich, and validate lineage from notebook source code.</td>
    </tr>
  </tbody>
</table>

