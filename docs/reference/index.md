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

## Find a callable

Search the callable catalogue by function name, module, starter path, or purpose. Site-wide search is still available from the top right.

<div class="callable-finder" data-callable-finder>
  <label class="callable-finder-label" for="callable-finder-input">Search callables</label>
  <input id="callable-finder-input" class="callable-finder-input" type="search" placeholder="Search callables" aria-describedby="callable-finder-help callable-finder-status callable-finder-examples" autocomplete="off">
  <p id="callable-finder-help" class="callable-finder-help">Search by function name, module, or what the function does.</p>
  <p id="callable-finder-examples" class="callable-finder-examples">Try: <code>csv</code> · <code>data_quality</code> · <code>quarantine</code></p>
  <p id="callable-finder-status" class="callable-finder-status" aria-live="polite">Showing all callables.</p>
  <p class="callable-finder-empty" data-callable-finder-empty hidden>No callables match your search.</p>
</div>

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
    <tr data-callable-row="true" data-callable-name="add_audit_columns" data-callable-module="technical_audit_columns" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Add run tracking and audit columns for ingestion workflows.">
      <td data-label="Function / class"><a href="./step-06b-runtime-standards/add_audit_columns/"><code>add_audit_columns</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Add run tracking and audit columns for ingestion workflows.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="add_datetime_features" data-callable-module="technical_audit_columns" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Add localized datetime feature columns derived from a UTC datetime column.">
      <td data-label="Function / class"><a href="./step-06b-runtime-standards/add_datetime_features/"><code>add_datetime_features</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Add localized datetime feature columns derived from a UTC datetime column.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="add_hash_columns" data-callable-module="technical_audit_columns" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Add business key and row-level SHA256 hash columns.">
      <td data-label="Function / class"><a href="./step-06b-runtime-standards/add_hash_columns/"><code>add_hash_columns</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Add business key and row-level SHA256 hash columns.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="assert_dq_passed" data-callable-module="data_quality" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Raise when any error-severity DQ rule failed after results are logged.">
      <td data-label="Function / class"><a href="./step-06d-controlled-outputs/assert_dq_passed/"><code>assert_dq_passed</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Raise when any error-severity DQ rule failed after results are logged.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="assert_notebook_name_valid" data-callable-module="runtime_context" data-callable-starter-path="02_ex, 03_pc" data-callable-importance="Essential" data-callable-purpose="Raise :class:`NotebookNamingError` when a notebook name is invalid.">
      <td data-label="Function / class"><a href="./step-01-governance-context/assert_notebook_name_valid/"><code>assert_notebook_name_valid</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Starter path">02_ex, 03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Raise :class:`NotebookNamingError` when a notebook name is invalid.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="bootstrap_fabric_env" data-callable-module="environment_config" data-callable-starter-path="00_env_config" data-callable-importance="Essential" data-callable-purpose="Bootstrap 00_env_config environment readiness by resolving required targets and collecting runtime/AI check results.">
      <td data-label="Function / class"><a href="./step-02b-notebook-startup-checks/bootstrap_fabric_env/"><code>bootstrap_fabric_env</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Bootstrap 00_env_config environment readiness by resolving required targets and collecting runtime/AI check results.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="build_ai_quality_context" data-callable-module="data_profiling" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Build deterministic AI-ready context from standard metadata profile rows.">
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/build_ai_quality_context/"><code>build_ai_quality_context</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build deterministic AI-ready context from standard metadata profile rows.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="build_contract_column_records" data-callable-module="data_contracts" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Build normalized contract-column metadata records for persistence.">
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/build_contract_column_records/"><code>build_contract_column_records</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build normalized contract-column metadata records for persistence.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="build_contract_header_record" data-callable-module="data_contracts" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Build one header row for FABRICOPS_CONTRACTS.">
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/build_contract_header_record/"><code>build_contract_header_record</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build one header row for FABRICOPS_CONTRACTS.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="build_contract_records" data-callable-module="data_contracts" data-callable-starter-path="03_pc" data-callable-importance="Essential" data-callable-purpose="Build grouped contract header, column, and rule metadata payloads.">
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/build_contract_records/"><code>build_contract_records</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build grouped contract header, column, and rule metadata payloads.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="build_contract_rule_records" data-callable-module="data_contracts" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Build quality-rule metadata records from a validated contract.">
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/build_contract_rule_records/"><code>build_contract_rule_records</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build quality-rule metadata records from a validated contract.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="build_contract_summary" data-callable-module="data_contracts" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Build a concise contract summary for reviews and handover.">
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/build_contract_summary/"><code>build_contract_summary</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build a concise contract summary for reviews and handover.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="build_dataset_run_record" data-callable-module="data_product_metadata" data-callable-starter-path="03_pc" data-callable-importance="Essential" data-callable-purpose="Build a dataset-run metadata record for operational tracking.">
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/build_dataset_run_record/"><code>build_dataset_run_record</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build a dataset-run metadata record for operational tracking.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="build_dq_rule_candidate_prompt" data-callable-module="data_quality" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Build the DQ-candidate prompt used in AI-assisted quality drafting.">
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/build_dq_rule_candidate_prompt/"><code>build_dq_rule_candidate_prompt</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build the DQ-candidate prompt used in AI-assisted quality drafting.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="build_governance_candidate_prompt" data-callable-module="data_governance" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Build the governance-candidate prompt for AI-assisted classification drafts.">
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/build_governance_candidate_prompt/"><code>build_governance_candidate_prompt</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build the governance-candidate prompt for AI-assisted classification drafts.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="build_governance_classification_records" data-callable-module="data_governance" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Build metadata-ready governance classification records from column suggestions.">
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/build_governance_classification_records/"><code>build_governance_classification_records</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build metadata-ready governance classification records from column suggestions.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="build_handover_summary_prompt" data-callable-module="handover_documentation" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Build the handover-summary prompt for AI-assisted run handoff drafting.">
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/build_handover_summary_prompt/"><code>build_handover_summary_prompt</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build the handover-summary prompt for AI-assisted run handoff drafting.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="build_lineage_from_notebook_code" data-callable-module="data_lineage" data-callable-starter-path="02_ex" data-callable-importance="Optional" data-callable-purpose="Scan, optionally enrich, and validate lineage from notebook source code.">
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/build_lineage_from_notebook_code/"><code>build_lineage_from_notebook_code</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">02_ex</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Scan, optionally enrich, and validate lineage from notebook source code.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="build_lineage_handover_markdown" data-callable-module="data_lineage" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Create a concise markdown handover summary from lineage execution results.">
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/build_lineage_handover_markdown/"><code>build_lineage_handover_markdown</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Create a concise markdown handover summary from lineage execution results.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="build_lineage_record_from_steps" data-callable-module="data_lineage" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Create metadata-ready lineage records from validated lineage steps.">
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/build_lineage_record_from_steps/"><code>build_lineage_record_from_steps</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Create metadata-ready lineage records from validated lineage steps.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="build_lineage_records" data-callable-module="data_lineage" data-callable-starter-path="03_pc" data-callable-importance="Optional" data-callable-purpose="Build compact lineage records for downstream metadata sinks.">
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/build_lineage_records/"><code>build_lineage_records</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build compact lineage records for downstream metadata sinks.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="build_manual_dq_rule_prompt_package" data-callable-module="data_quality" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Build copy/paste prompt package for manual DQ candidate generation.">
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/build_manual_dq_rule_prompt_package/"><code>build_manual_dq_rule_prompt_package</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build copy/paste prompt package for manual DQ candidate generation.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="build_manual_governance_prompt_package" data-callable-module="data_governance" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Build copy/paste prompt package for manual governance suggestion generation.">
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/build_manual_governance_prompt_package/"><code>build_manual_governance_prompt_package</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build copy/paste prompt package for manual governance suggestion generation.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="build_manual_handover_prompt_package" data-callable-module="handover_documentation" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Build copy/paste prompt package for manual handover summary generation.">
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/build_manual_handover_prompt_package/"><code>build_manual_handover_prompt_package</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build copy/paste prompt package for manual handover summary generation.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="build_quality_result_records" data-callable-module="data_product_metadata" data-callable-starter-path="03_pc" data-callable-importance="Essential" data-callable-purpose="Convert quality-rule execution output into metadata evidence records.">
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/build_quality_result_records/"><code>build_quality_result_records</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert quality-rule execution output into metadata evidence records.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="build_run_summary" data-callable-module="handover_documentation" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Build a handover-friendly summary for one data product run.">
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/build_run_summary/"><code>build_run_summary</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build a handover-friendly summary for one data product run.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="build_runtime_context" data-callable-module="runtime_context" data-callable-starter-path="02_ex, 03_pc" data-callable-importance="Essential" data-callable-purpose="Build a standard runtime context dictionary for Fabric notebooks.">
      <td data-label="Function / class"><a href="./step-01-governance-context/build_runtime_context/"><code>build_runtime_context</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Starter path">02_ex, 03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build a standard runtime context dictionary for Fabric notebooks.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="build_schema_drift_records" data-callable-module="data_product_metadata" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Convert schema drift results into metadata records for audit trails.">
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/build_schema_drift_records/"><code>build_schema_drift_records</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert schema drift results into metadata records for audit trails.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="build_schema_snapshot_records" data-callable-module="data_product_metadata" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Convert a schema snapshot into row-wise metadata records.">
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/build_schema_snapshot_records/"><code>build_schema_snapshot_records</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert a schema snapshot into row-wise metadata records.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="check_fabric_ai_functions_available" data-callable-module="environment_config" data-callable-starter-path="00_env_config" data-callable-importance="Essential" data-callable-purpose="Check whether Fabric AI Functions are available in the current runtime.">
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/check_fabric_ai_functions_available/"><code>check_fabric_ai_functions_available</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Check whether Fabric AI Functions are available in the current runtime.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="check_partition_drift" data-callable-module="data_drift" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Check partition-level drift using keys, partitions, and optional watermark baselines.">
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/check_partition_drift/"><code>check_partition_drift</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Check partition-level drift using keys, partitions, and optional watermark baselines.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="check_profile_drift" data-callable-module="data_drift" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Compare profile metrics against a baseline profile and drift thresholds.">
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/check_profile_drift/"><code>check_profile_drift</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Compare profile metrics against a baseline profile and drift thresholds.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="check_schema_drift" data-callable-module="data_drift" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Compare a current dataframe schema against a baseline schema snapshot.">
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/check_schema_drift/"><code>check_schema_drift</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Compare a current dataframe schema against a baseline schema snapshot.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="classify_column" data-callable-module="data_governance" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Classify one column using term matching, metadata cues, and business context.">
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/classify_column/"><code>classify_column</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Classify one column using term matching, metadata cues, and business context.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="classify_columns" data-callable-module="data_governance" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Classify multiple columns and return normalized governance suggestions.">
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/classify_columns/"><code>classify_columns</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Classify multiple columns and return normalized governance suggestions.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="configure_fabric_ai_functions" data-callable-module="environment_config" data-callable-starter-path="00_env_config" data-callable-importance="Essential" data-callable-purpose="Apply optional default Fabric AI Function configuration.">
      <td data-label="Function / class"><a href="./step-01-governance-context/configure_fabric_ai_functions/"><code>configure_fabric_ai_functions</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Apply optional default Fabric AI Function configuration.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="contract_records_to_spark" data-callable-module="data_contracts" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Convert record dictionaries into a Spark DataFrame when Spark is available.">
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/contract_records_to_spark/"><code>contract_records_to_spark</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert record dictionaries into a Spark DataFrame when Spark is available.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="create_ai_prompt_config" data-callable-module="environment_config" data-callable-starter-path="00_env_config" data-callable-importance="Essential" data-callable-purpose="Create the AI prompt-template configuration used by FabricOps.">
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/create_ai_prompt_config/"><code>create_ai_prompt_config</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create the AI prompt-template configuration used by FabricOps.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="create_framework_config" data-callable-module="environment_config" data-callable-starter-path="00_env_config" data-callable-importance="Essential" data-callable-purpose="Create the top-level FabricOps framework configuration contract.">
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/create_framework_config/"><code>create_framework_config</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create the top-level FabricOps framework configuration contract.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="create_governance_config" data-callable-module="environment_config" data-callable-starter-path="00_env_config" data-callable-importance="Essential" data-callable-purpose="Create governance policy defaults for FabricOps runtime checks.">
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/create_governance_config/"><code>create_governance_config</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create governance policy defaults for FabricOps runtime checks.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="create_lineage_config" data-callable-module="environment_config" data-callable-starter-path="00_env_config" data-callable-importance="Essential" data-callable-purpose="Create lineage capture defaults for FabricOps handover traceability.">
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/create_lineage_config/"><code>create_lineage_config</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create lineage capture defaults for FabricOps handover traceability.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="create_notebook_runtime_config" data-callable-module="environment_config" data-callable-starter-path="00_env_config" data-callable-importance="Essential" data-callable-purpose="Create notebook naming-policy configuration for runtime guards.">
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/create_notebook_runtime_config/"><code>create_notebook_runtime_config</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create notebook naming-policy configuration for runtime guards.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="create_path_config" data-callable-module="environment_config" data-callable-starter-path="00_env_config" data-callable-importance="Essential" data-callable-purpose="Create environment-to-target routing used by Fabric IO helpers.">
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/create_path_config/"><code>create_path_config</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create environment-to-target routing used by Fabric IO helpers.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="create_quality_config" data-callable-module="environment_config" data-callable-starter-path="00_env_config" data-callable-importance="Essential" data-callable-purpose="Create the default quality policy used during FabricOps checks.">
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/create_quality_config/"><code>create_quality_config</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Create the default quality policy used during FabricOps checks.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE" data-callable-module="data_quality" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Default prompt template used to draft candidate DQ rules.">
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE/"><code>DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Default prompt template used to draft candidate DQ rules.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="default_technical_columns" data-callable-module="technical_audit_columns" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Return framework-generated and legacy technical column names to ignore.">
      <td data-label="Function / class"><a href="./step-06b-runtime-standards/default_technical_columns/"><code>default_technical_columns</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Return framework-generated and legacy technical column names to ignore.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="enrich_lineage_steps_with_ai" data-callable-module="data_lineage" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Optionally enrich deterministic lineage steps using an AI helper callable.">
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/enrich_lineage_steps_with_ai/"><code>enrich_lineage_steps_with_ai</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Optionally enrich deterministic lineage steps using an AI helper callable.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="extract_business_keys" data-callable-module="data_contracts" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Extract business-key column names from a normalized contract.">
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/extract_business_keys/"><code>extract_business_keys</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract business-key column names from a normalized contract.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="extract_classifications" data-callable-module="data_contracts" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Extract column classification mappings from a normalized contract.">
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/extract_classifications/"><code>extract_classifications</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract column classification mappings from a normalized contract.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="extract_optional_columns" data-callable-module="data_contracts" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Extract optional column names from a normalized contract.">
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/extract_optional_columns/"><code>extract_optional_columns</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract optional column names from a normalized contract.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="extract_quality_rules" data-callable-module="data_contracts" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Extract raw quality-rule definitions from a normalized contract.">
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/extract_quality_rules/"><code>extract_quality_rules</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract raw quality-rule definitions from a normalized contract.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="extract_required_columns" data-callable-module="data_contracts" data-callable-starter-path="03_pc" data-callable-importance="Essential" data-callable-purpose="Extract required column names from a normalized contract.">
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/extract_required_columns/"><code>extract_required_columns</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Extract required column names from a normalized contract.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="fallback_copilot_lineage_prompt" data-callable-module="data_lineage" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Build a fallback Copilot prompt for manual lineage enrichment.">
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/fallback_copilot_lineage_prompt/"><code>fallback_copilot_lineage_prompt</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build a fallback Copilot prompt for manual lineage enrichment.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="generate_dq_rule_candidates_with_fabric_ai" data-callable-module="data_quality" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Append AI-suggested DQ rule candidates to a profiling DataFrame.">
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/generate_dq_rule_candidates_with_fabric_ai/"><code>generate_dq_rule_candidates_with_fabric_ai</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Append AI-suggested DQ rule candidates to a profiling DataFrame.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="generate_governance_candidates_with_fabric_ai" data-callable-module="data_governance" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Execute Fabric AI Functions to append governance suggestions to a DataFrame.">
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/generate_governance_candidates_with_fabric_ai/"><code>generate_governance_candidates_with_fabric_ai</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Execute Fabric AI Functions to append governance suggestions to a DataFrame.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="generate_handover_summary_with_fabric_ai" data-callable-module="handover_documentation" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Execute Fabric AI Functions to append handover summary suggestions.">
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/generate_handover_summary_with_fabric_ai/"><code>generate_handover_summary_with_fabric_ai</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Execute Fabric AI Functions to append handover summary suggestions.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="generate_metadata_profile" data-callable-module="data_profiling" data-callable-starter-path="02_ex" data-callable-importance="Essential" data-callable-purpose="Generate standard metadata profile rows for a Spark/Fabric DataFrame.">
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/generate_metadata_profile/"><code>generate_metadata_profile</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Starter path">02_ex</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Generate standard metadata profile rows for a Spark/Fabric DataFrame.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="generate_run_id" data-callable-module="runtime_context" data-callable-starter-path="03_pc" data-callable-importance="Essential" data-callable-purpose="Generate a notebook-safe run identifier.">
      <td data-label="Function / class"><a href="./step-01-governance-context/generate_run_id/"><code>generate_run_id</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Generate a notebook-safe run identifier.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="get_default_dq_rule_templates" data-callable-module="data_quality" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Return editable example data quality rules.">
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/get_default_dq_rule_templates/"><code>get_default_dq_rule_templates</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Return editable example data quality rules.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="get_executable_quality_rules" data-callable-module="data_contracts" data-callable-starter-path="03_pc" data-callable-importance="Essential" data-callable-purpose="Return normalized quality rules ready for pipeline enforcement.">
      <td data-label="Function / class"><a href="./step-06c-pipeline-controls/get_executable_quality_rules/"><code>get_executable_quality_rules</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Return normalized quality rules ready for pipeline enforcement.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="get_path" data-callable-module="environment_config" data-callable-starter-path="00_env_config, 02_ex, 03_pc" data-callable-importance="Essential" data-callable-purpose="Resolve a configured Fabric path for an environment and target.">
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/get_path/"><code>get_path</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config, 02_ex, 03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Resolve a configured Fabric path for an environment and target.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="Housepath" data-callable-module="fabric_input_output" data-callable-starter-path="00_env_config" data-callable-importance="Essential" data-callable-purpose="Fabric lakehouse or warehouse connection details.">
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/Housepath/"><code>Housepath</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Fabric lakehouse or warehouse connection details.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="lakehouse_csv_read" data-callable-module="fabric_input_output" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Read a CSV file from a Fabric lakehouse Files path.">
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/lakehouse_csv_read/"><code>lakehouse_csv_read</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a CSV file from a Fabric lakehouse Files path.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="lakehouse_excel_read_as_spark" data-callable-module="fabric_input_output" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Read an Excel file from a Fabric lakehouse Files path.">
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/lakehouse_excel_read_as_spark/"><code>lakehouse_excel_read_as_spark</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read an Excel file from a Fabric lakehouse Files path.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="lakehouse_parquet_read_as_spark" data-callable-module="fabric_input_output" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Read a Parquet file from a Fabric lakehouse Files path.">
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/lakehouse_parquet_read_as_spark/"><code>lakehouse_parquet_read_as_spark</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a Parquet file from a Fabric lakehouse Files path.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="lakehouse_table_read" data-callable-module="fabric_input_output" data-callable-starter-path="02_ex, 03_pc" data-callable-importance="Essential" data-callable-purpose="Read a Delta table from a Fabric lakehouse.">
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/lakehouse_table_read/"><code>lakehouse_table_read</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">02_ex, 03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a Delta table from a Fabric lakehouse.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="lakehouse_table_write" data-callable-module="fabric_input_output" data-callable-starter-path="03_pc" data-callable-importance="Essential" data-callable-purpose="Write a Spark DataFrame to a Fabric lakehouse Delta table.">
      <td data-label="Function / class"><a href="./step-06d-controlled-outputs/lakehouse_table_write/"><code>lakehouse_table_write</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Write a Spark DataFrame to a Fabric lakehouse Delta table.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="load_contract_from_lakehouse" data-callable-module="data_contracts" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Load one contract by ID/version from Fabric metadata storage.">
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/load_contract_from_lakehouse/"><code>load_contract_from_lakehouse</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Load one contract by ID/version from Fabric metadata storage.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="load_data_contract" data-callable-module="data_contracts" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Load and normalize a data product contract from file path or dictionary.">
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/load_data_contract/"><code>load_data_contract</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Load and normalize a data product contract from file path or dictionary.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="load_fabric_config" data-callable-module="environment_config" data-callable-starter-path="00_env_config, 02_ex, 03_pc" data-callable-importance="Essential" data-callable-purpose="Validate and return a user-supplied framework configuration.">
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/load_fabric_config/"><code>load_fabric_config</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config, 02_ex, 03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate and return a user-supplied framework configuration.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="load_latest_approved_contract" data-callable-module="data_contracts" data-callable-starter-path="03_pc" data-callable-importance="Essential" data-callable-purpose="Load the latest approved contract for a dataset/object pair.">
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/load_latest_approved_contract/"><code>load_latest_approved_contract</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Load the latest approved contract for a dataset/object pair.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="normalize_contract_dict" data-callable-module="data_contracts" data-callable-starter-path="02_ex" data-callable-importance="Essential" data-callable-purpose="Normalize a notebook-authored contract dictionary to a stable shape.">
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/normalize_contract_dict/"><code>normalize_contract_dict</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">02_ex</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Normalize a notebook-authored contract dictionary to a stable shape.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="parse_manual_ai_json_response" data-callable-module="handover_documentation" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Parse manual AI JSON output into Python objects.">
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/parse_manual_ai_json_response/"><code>parse_manual_ai_json_response</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Parse manual AI JSON output into Python objects.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="plot_lineage_steps" data-callable-module="data_lineage" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Render lineage steps as a directed graph figure.">
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/plot_lineage_steps/"><code>plot_lineage_steps</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Render lineage steps as a directed graph figure.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="profile_dataframe" data-callable-module="data_profiling" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Build a lightweight profile for pandas or Spark-like DataFrames.">
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/profile_dataframe/"><code>profile_dataframe</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Build a lightweight profile for pandas or Spark-like DataFrames.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="profile_dataframe_to_metadata" data-callable-module="data_profiling" data-callable-starter-path="02_ex" data-callable-importance="Essential" data-callable-purpose="Profile a Spark/Fabric DataFrame into metadata-compatible metadata rows.">
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/profile_dataframe_to_metadata/"><code>profile_dataframe_to_metadata</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Starter path">02_ex</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Profile a Spark/Fabric DataFrame into metadata-compatible metadata rows.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="profile_metadata_to_records" data-callable-module="data_profiling" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Convert Spark metadata profile rows into JSON-friendly dictionaries.">
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/profile_metadata_to_records/"><code>profile_metadata_to_records</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Convert Spark metadata profile rows into JSON-friendly dictionaries.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="render_run_summary_markdown" data-callable-module="handover_documentation" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Render a run summary dictionary into Markdown for handover notes.">
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/render_run_summary_markdown/"><code>render_run_summary_markdown</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Render a run summary dictionary into Markdown for handover notes.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="run_config_smoke_tests" data-callable-module="environment_config" data-callable-starter-path="00_env_config" data-callable-importance="Essential" data-callable-purpose="Run 00_env_config smoke checks for Spark, runtime context, configured paths, notebook naming, and optional AI/IO imports.">
      <td data-label="Function / class"><a href="./step-02b-notebook-startup-checks/run_config_smoke_tests/"><code>run_config_smoke_tests</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Run 00_env_config smoke checks for Spark, runtime context, configured paths, notebook naming, and optional AI/IO imports.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="run_data_product" data-callable-module="data_quality" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Run the starter kit workflow end-to-end for a data product outcome.">
      <td data-label="Function / class"><a href="./step-06a-transformation-logic/run_data_product/"><code>run_data_product</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Run the starter kit workflow end-to-end for a data product outcome.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="run_dq_rules" data-callable-module="data_quality" data-callable-starter-path="03_pc" data-callable-importance="Essential" data-callable-purpose="Run notebook-facing DQ rules and return a Spark DataFrame result.">
      <td data-label="Function / class"><a href="./step-06c-pipeline-controls/run_dq_rules/"><code>run_dq_rules</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Run notebook-facing DQ rules and return a Spark DataFrame result.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="run_quality_rules" data-callable-module="data_quality" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Execute quality rules against a dataframe and return structured results.">
      <td data-label="Function / class"><a href="./step-06c-pipeline-controls/run_quality_rules/"><code>run_quality_rules</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Execute quality rules against a dataframe and return structured results.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="scan_notebook_cells" data-callable-module="data_lineage" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Scan multiple notebook cells and append cell references to lineage steps.">
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/scan_notebook_cells/"><code>scan_notebook_cells</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Scan multiple notebook cells and append cell references to lineage steps.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="scan_notebook_lineage" data-callable-module="data_lineage" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Extract deterministic lineage steps from notebook code using AST parsing.">
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/scan_notebook_lineage/"><code>scan_notebook_lineage</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Extract deterministic lineage steps from notebook code using AST parsing.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="seed_minimal_sample_source_table" data-callable-module="fabric_input_output" data-callable-starter-path="02_ex" data-callable-importance="Optional" data-callable-purpose="Create and persist deterministic demo rows into a sample source table.">
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/seed_minimal_sample_source_table/"><code>seed_minimal_sample_source_table</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">02_ex</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Create and persist deterministic demo rows into a sample source table.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="split_valid_and_quarantine" data-callable-module="data_quality" data-callable-starter-path="03_pc" data-callable-importance="Optional" data-callable-purpose="Split a Spark DataFrame into pass/quarantine outputs for row-level DQ rules.">
      <td data-label="Function / class"><a href="./step-06c-pipeline-controls/split_valid_and_quarantine/"><code>split_valid_and_quarantine</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Split a Spark DataFrame into pass/quarantine outputs for row-level DQ rules.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="suggest_accepted_value_mapping_prompt" data-callable-module="data_quality" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Build a constrained prompt for accepted-value mapping suggestions.">
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/suggest_accepted_value_mapping_prompt/"><code>suggest_accepted_value_mapping_prompt</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build a constrained prompt for accepted-value mapping suggestions.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="suggest_closest_accepted_value" data-callable-module="data_quality" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Suggest a deterministic closest accepted value using ``difflib``.">
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/suggest_closest_accepted_value/"><code>suggest_closest_accepted_value</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Suggest a deterministic closest accepted value using ``difflib``.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="suggest_dq_rules_prompt" data-callable-module="data_quality" data-callable-starter-path="02_ex" data-callable-importance="Optional" data-callable-purpose="Build a prompt for candidate DQ rule suggestions.">
      <td data-label="Function / class"><a href="./step-08-ai-assisted-dq-suggestions/suggest_dq_rules_prompt/"><code>suggest_dq_rules_prompt</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">02_ex</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Build a prompt for candidate DQ rule suggestions.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="summarize_drift_results" data-callable-module="data_drift" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Summarize schema, partition, and profile drift outcomes into one decision.">
      <td data-label="Function / class"><a href="./step-04-ingest-profile-store/summarize_drift_results/"><code>summarize_drift_results</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Summarize schema, partition, and profile drift outcomes into one decision.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="summarize_governance_classifications" data-callable-module="data_governance" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Summarize governance classification outputs into review-friendly counts.">
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/summarize_governance_classifications/"><code>summarize_governance_classifications</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Summarize governance classification outputs into review-friendly counts.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="validate_contract_dict" data-callable-module="data_contracts" data-callable-starter-path="02_ex" data-callable-importance="Essential" data-callable-purpose="Validate a contract dictionary and return error strings without raising.">
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/validate_contract_dict/"><code>validate_contract_dict</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">02_ex</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate a contract dictionary and return error strings without raising.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="validate_dq_rules" data-callable-module="data_quality" data-callable-starter-path="03_pc" data-callable-importance="Essential" data-callable-purpose="Validate notebook-facing DQ rules.">
      <td data-label="Function / class"><a href="./step-06c-pipeline-controls/validate_dq_rules/"><code>validate_dq_rules</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate notebook-facing DQ rules.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="validate_framework_config" data-callable-module="environment_config" data-callable-starter-path="00_env_config" data-callable-importance="Essential" data-callable-purpose="Validate and normalize framework configuration input.">
      <td data-label="Function / class"><a href="./step-02a-shared-runtime-config/validate_framework_config/"><code>validate_framework_config</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Starter path">00_env_config</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate and normalize framework configuration input.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="validate_lineage_steps" data-callable-module="data_lineage" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Validate lineage step structure and flag records requiring human review.">
      <td data-label="Function / class"><a href="./step-10-lineage-handover-documentation/validate_lineage_steps/"><code>validate_lineage_steps</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Validate lineage step structure and flag records requiring human review.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="validate_notebook_name" data-callable-module="runtime_context" data-callable-starter-path="02_ex, 03_pc" data-callable-importance="Essential" data-callable-purpose="Validate notebook names against the framework workspace notebook model.">
      <td data-label="Function / class"><a href="./step-01-governance-context/validate_notebook_name/"><code>validate_notebook_name</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/runtime_context/" title="Open runtime_context module page" aria-label="Open runtime_context module page">runtime_context</a></td>
      <td data-label="Starter path">02_ex, 03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate notebook names against the framework workspace notebook model.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="warehouse_read" data-callable-module="fabric_input_output" data-callable-starter-path="02_ex, 03_pc" data-callable-importance="Essential" data-callable-purpose="Read a table from a Microsoft Fabric warehouse.">
      <td data-label="Function / class"><a href="./step-03-source-contract-ingestion-pattern/warehouse_read/"><code>warehouse_read</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">02_ex, 03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Read a table from a Microsoft Fabric warehouse.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="warehouse_write" data-callable-module="fabric_input_output" data-callable-starter-path="03_pc" data-callable-importance="Essential" data-callable-purpose="Write a Spark DataFrame to a Microsoft Fabric warehouse table.">
      <td data-label="Function / class"><a href="./step-06d-controlled-outputs/warehouse_write/"><code>warehouse_write</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Starter path">03_pc</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Write a Spark DataFrame to a Microsoft Fabric warehouse table.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="write_contract_to_lakehouse" data-callable-module="data_contracts" data-callable-starter-path="02_ex" data-callable-importance="Essential" data-callable-purpose="Validate and persist contract records into Fabric metadata tables.">
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/write_contract_to_lakehouse/"><code>write_contract_to_lakehouse</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a></td>
      <td data-label="Starter path">02_ex</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Validate and persist contract records into Fabric metadata tables.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="write_governance_classifications" data-callable-module="data_governance" data-callable-starter-path="—" data-callable-importance="Optional" data-callable-purpose="Persist governance classifications to a metadata destination.">
      <td data-label="Function / class"><a href="./step-09-ai-assisted-classification/write_governance_classifications/"><code>write_governance_classifications</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Optional</td>
      <td data-label="Purpose">Persist governance classifications to a metadata destination.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="write_metadata_records" data-callable-module="data_product_metadata" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Write metadata records to a configured metadata sink.">
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/write_metadata_records/"><code>write_metadata_records</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Write metadata records to a configured metadata sink.</td>
    </tr>
    <tr data-callable-row="true" data-callable-name="write_multiple_metadata_outputs" data-callable-module="data_product_metadata" data-callable-starter-path="—" data-callable-importance="Essential" data-callable-purpose="Write multiple metadata payloads to their configured destinations.">
      <td data-label="Function / class"><a href="./step-07-output-profile-product-contract/write_multiple_metadata_outputs/"><code>write_multiple_metadata_outputs</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a></td>
      <td data-label="Starter path">—</td>
      <td data-label="Importance">Essential</td>
      <td data-label="Purpose">Write multiple metadata payloads to their configured destinations.</td>
    </tr>
  </tbody>
</table>

