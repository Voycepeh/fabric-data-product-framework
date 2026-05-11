# `03_pc_<agreement>_<pipeline>`

Pipeline-contract notebook flow for deterministic enforcement and controlled publishing.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/03_pc_agreement_source_to_target.ipynb">Open template notebook</a>

> `03_pc` is deterministic pipeline enforcement.

## Segment 1: Load shared config and runtime context

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
      <td data-label="Function / class"><a href="../../reference/step-02a-shared-runtime-config/load_fabric_config/"><code>load_fabric_config</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Purpose">Validate and return a user-supplied framework configuration.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-01-governance-context/validate_notebook_name/"><code>validate_notebook_name</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Purpose">Validate notebook names against the framework workspace notebook model.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-01-governance-context/assert_notebook_name_valid/"><code>assert_notebook_name_valid</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Purpose">Raise :class:`NotebookNamingError` when a notebook name is invalid.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-01-governance-context/generate_run_id/"><code>generate_run_id</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Purpose">Generate a notebook-safe run identifier.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-01-governance-context/build_runtime_context/"><code>build_runtime_context</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Purpose">Build a standard runtime context dictionary for Fabric notebooks.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-02a-shared-runtime-config/get_path/"><code>get_path</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Purpose">Resolve a configured Fabric path for an environment and target.</td>
    </tr>
  </tbody>
</table>

## Segment 2: Load approved contract and source data

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
      <td data-label="Function / class"><a href="../../reference/step-03-source-contract-ingestion-pattern/load_latest_approved_contract/"><code>load_latest_approved_contract</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Purpose">Load the latest approved contract for a dataset/object pair.</td>
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
  </tbody>
</table>

## Segment 3: Validate columns, transform, and compile rules

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
      <td data-label="Function / class"><a href="../../reference/step-03-source-contract-ingestion-pattern/extract_required_columns/"><code>extract_required_columns</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Purpose">Extract required column names from a normalized contract.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-06c-pipeline-controls/get_executable_quality_rules/"><code>get_executable_quality_rules</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Purpose">Return normalized quality rules ready for pipeline enforcement.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-06c-pipeline-controls/validate_dq_rules/"><code>validate_dq_rules</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Purpose">Validate canonical DQ rules before enforcement.</td>
    </tr>
  </tbody>
</table>

## Segment 4: Run DQ, split outputs, and publish

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
      <td data-label="Function / class"><a href="../../reference/step-06c-pipeline-controls/enforce_dq_rules/"><code>enforce_dq_rules</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Purpose">Run notebook-facing DQ rules and return a Spark DataFrame result.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-06d-controlled-outputs/assert_dq_passed/"><code>assert_dq_passed</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Purpose">Raise only after evidence materialization when error-severity rules fail.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-06d-controlled-outputs/lakehouse_table_write/"><code>lakehouse_table_write</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Purpose">Write a Spark DataFrame to a Fabric lakehouse Delta table.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-06d-controlled-outputs/warehouse_write/"><code>warehouse_write</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Purpose">Write a Spark DataFrame to a Microsoft Fabric warehouse table.</td>
    </tr>
  </tbody>
</table>

## Optional metadata / lineage / handover evidence

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
      <td data-label="Function / class"><a href="../../reference/step-07-output-profile-product-contract/build_dataset_run_record/"><code>build_dataset_run_record</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Purpose">Build a dataset-run metadata record for operational tracking.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-07-output-profile-product-contract/build_quality_result_records/"><code>build_quality_result_records</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Purpose">Convert quality-rule execution output into metadata evidence records.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-07-output-profile-product-contract/build_contract_records/"><code>build_contract_records</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Purpose">Build grouped contract header, column, and rule metadata payloads.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-10-lineage-handover-documentation/build_lineage_records/"><code>build_lineage_records</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Purpose">Build compact lineage records for downstream metadata sinks.</td>
    </tr>
  </tbody>
</table>

