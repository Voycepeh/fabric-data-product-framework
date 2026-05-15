# `02_ex_<agreement>_<topic>`

Exploration notebook flow used to profile source data and draft advisory AI outputs for human review.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/02_ex_agreement_topic.ipynb">Open template notebook</a>

> `02_ex` proposes evidence and AI-assisted suggestions.

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
      <td data-label="Function / class"><a href="../../api/reference/setup_notebook/"><code>setup_notebook</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Purpose">Run consolidated FabricOps startup for exploration and pipeline notebooks.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../api/reference/load_config/"><code>load_config</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Purpose">Validate and return a user-supplied framework configuration.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../api/reference/get_path/"><code>get_path</code></a></td>
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
      <td data-label="Function / class"><a href="../../api/reference/read_lakehouse_table/"><code>read_lakehouse_table</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Purpose">Read a Delta table from a Fabric lakehouse.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../api/reference/read_warehouse_table/"><code>read_warehouse_table</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Purpose">Read a table from a Microsoft Fabric warehouse.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../api/reference/profile_dataframe/"><code>profile_dataframe</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Purpose">Build canonical DQ-ready profiling rows from a Spark DataFrame.</td>
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
      <td data-label="Function / class"><a href="../../api/reference/draft_dq_rules/"><code>draft_dq_rules</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Purpose">Draft candidate DQ rules from metadata profiles or raw DataFrame fallback.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../api/reference/review_dq_rules/"><code>review_dq_rules</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Purpose">Review AI-suggested DQ rules sequentially with explicit approve/reject decisions.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../api/reference/write_dq_rules/"><code>write_dq_rules</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Purpose">Validate, build, and persist approved DQ rules.</td>
    </tr>
  </tbody>
</table>

## Segment 4: Human review and write approved DQ rules

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
      <td data-label="Function / class"><a href="../../api/reference/write_dq_rules/"><code>write_dq_rules</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Purpose">Validate, build, and persist approved DQ rules.</td>
    </tr>
  </tbody>
</table>

## Optional lineage notes

