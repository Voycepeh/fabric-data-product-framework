# `03_pc_<agreement>_<pipeline>`

Pipeline notebook flow for deterministic enforcement and controlled publishing.

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
      <td data-label="Function / class"><a href="../../reference/setup_fabricops_notebook/"><code>setup_fabricops_notebook</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Purpose">Run consolidated FabricOps startup for exploration and pipeline notebooks.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/load_fabric_config/"><code>load_fabric_config</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Purpose">Validate and return a user-supplied framework configuration.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/get_path/"><code>get_path</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Purpose">Resolve a configured Fabric path for an environment and target.</td>
    </tr>
  </tbody>
</table>

## Segment 2: Load source data and validate required columns

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
      <td data-label="Function / class"><a href="../../reference/lakehouse_table_read/"><code>lakehouse_table_read</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Purpose">Read a Delta table from a Fabric lakehouse.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/warehouse_read/"><code>warehouse_read</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Purpose">Read a table from a Microsoft Fabric warehouse.</td>
    </tr>
  </tbody>
</table>

## Segment 3: Transform and apply runtime standards

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
      <td data-label="Function / class"><a href="../../reference/standardize_output_columns/"><code>standardize_output_columns</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/technical_columns/" title="Open technical_columns module page" aria-label="Open technical_columns module page">technical_columns</a></td>
      <td data-label="Purpose">Apply canonical technical/audit enrichment in one notebook-facing wrapper.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/validate_dq_rules/"><code>validate_dq_rules</code></a></td>
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
      <td data-label="Function / class"><a href="../../reference/enforce_dq_rules/"><code>enforce_dq_rules</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Purpose">Run notebook-facing DQ rules and return a Spark DataFrame result.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/assert_dq_passed/"><code>assert_dq_passed</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Purpose">Raise only after evidence materialization when error-severity rules fail.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/lakehouse_table_write/"><code>lakehouse_table_write</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Purpose">Write a Spark DataFrame to a Fabric lakehouse Delta table.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/warehouse_write/"><code>warehouse_write</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Purpose">Write a Spark DataFrame to a Microsoft Fabric warehouse table.</td>
    </tr>
  </tbody>
</table>

## Optional profiling, drift, governance, lineage, and handover

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
      <td data-label="Function / class"><a href="../../reference/profile_dataframe/"><code>profile_dataframe</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Purpose">Build canonical DQ-ready profiling rows from a Spark DataFrame.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/check_schema_drift/"><code>check_schema_drift</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Purpose">Compare a current dataframe schema against a baseline schema snapshot.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/check_partition_drift/"><code>check_partition_drift</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Purpose">Check partition-level drift using keys, partitions, and optional watermark baselines.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/check_profile_drift/"><code>check_profile_drift</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Purpose">Compare profile metrics against a baseline profile and drift thresholds.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/summarize_drift_results/"><code>summarize_drift_results</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Purpose">Summarize schema, partition, and profile drift outcomes into one decision.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/classify_columns/"><code>classify_columns</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Purpose">Classify multiple columns and return normalized governance suggestions.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/build_governance_classification_records/"><code>build_governance_classification_records</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Purpose">Build metadata-ready governance classification records from column suggestions.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/write_governance_classifications/"><code>write_governance_classifications</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Purpose">Persist governance classifications to a metadata destination.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/summarize_governance_classifications/"><code>summarize_governance_classifications</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Purpose">Summarize governance classification outputs into review-friendly counts.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/build_lineage_records/"><code>build_lineage_records</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Purpose">Build compact lineage records for downstream metadata sinks.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/build_lineage_handover_markdown/"><code>build_lineage_handover_markdown</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Purpose">Create a concise markdown handover summary from lineage execution results.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/build_run_summary/"><code>build_run_summary</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/run_summary/" title="Open run_summary module page" aria-label="Open run_summary module page">run_summary</a></td>
      <td data-label="Purpose">Build a handover-friendly summary for one data product run.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/render_run_summary_markdown/"><code>render_run_summary_markdown</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/run_summary/" title="Open run_summary module page" aria-label="Open run_summary module page">run_summary</a></td>
      <td data-label="Purpose">Render a run summary dictionary into Markdown for handover notes.</td>
    </tr>
  </tbody>
</table>

