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
      <td data-label="Guided usage">Shared environment bootstrap and validation before exploration or pipeline notebooks run.<br><a href="../notebook-structure/00-env-config/">View guided structure</a></td>
      <td data-label="Full template"><a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/00_env_config.ipynb">Open notebook</a></td>
    </tr>
    <tr>
      <td data-label="Notebook"><code>02_ex_&lt;agreement&gt;_&lt;topic&gt;</code></td>
      <td data-label="Guided usage">Exploration notebook flow used to profile source data and draft advisory AI outputs for human review.<br><a href="../notebook-structure/02-exploration/">View guided structure</a></td>
      <td data-label="Full template"><a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/02_ex_agreement_topic.ipynb">Open notebook</a></td>
    </tr>
    <tr>
      <td data-label="Notebook"><code>03_pc_&lt;agreement&gt;_&lt;pipeline&gt;</code></td>
      <td data-label="Guided usage">Pipeline-contract notebook flow for deterministic enforcement and controlled publishing.<br><a href="../notebook-structure/03-pipeline-contract/">View guided structure</a></td>
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

Use the finder below to look up public callables.

<div class="callable-finder" data-callable-finder>
  <label class="callable-finder-label" for="callable-finder-input">Search callables</label>
  <input id="callable-finder-input" class="callable-finder-input" type="search" placeholder="Search callables" aria-describedby="callable-finder-help callable-finder-status callable-finder-examples" autocomplete="off">
  <p id="callable-finder-help" class="callable-finder-help">Search by function name, module, or what the function does.</p>
  <p id="callable-finder-examples" class="callable-finder-examples">Try: <span class="callable-finder-chip">csv</span> <span class="callable-finder-chip">data_quality</span> <span class="callable-finder-chip">quarantine</span></p>
  <p id="callable-finder-status" class="callable-finder-status" aria-live="polite">Showing all callables.</p>
  <fieldset class="callable-role-filters">
    <legend>Role filters</legend>
    <label><input type="checkbox" data-role-filter="essential" checked> Essential</label>
    <label><input type="checkbox" data-role-filter="optional" checked> Optional</label>
    <label><input type="checkbox" data-role-filter="internal"> Internal</label>
  </fieldset>
  <p class="callable-finder-empty" data-callable-finder-empty hidden>No callables match your search.</p>
</div>

## Function catalogue

## All public functions

<div class="reference-catalogue-list">
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="add_audit_columns" data-callable-module="technical_audit_columns" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Add run tracking and audit columns for ingestion workflows.">
  <h3 class="reference-catalogue-item-name"><a href="./step-06b-runtime-standards/add_audit_columns/"><code>add_audit_columns</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Add run tracking and audit columns for ingestion workflows.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="add_datetime_features" data-callable-module="technical_audit_columns" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Add localized datetime feature columns derived from a UTC datetime column.">
  <h3 class="reference-catalogue-item-name"><a href="./step-06b-runtime-standards/add_datetime_features/"><code>add_datetime_features</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Add localized datetime feature columns derived from a UTC datetime column.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="add_hash_columns" data-callable-module="technical_audit_columns" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Add business key and row-level SHA256 hash columns.">
  <h3 class="reference-catalogue-item-name"><a href="./step-06b-runtime-standards/add_hash_columns/"><code>add_hash_columns</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Add business key and row-level SHA256 hash columns.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="assert_dq_passed" data-callable-module="data_quality" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Raise only after evidence materialization when error-severity rules fail.">
  <h3 class="reference-catalogue-item-name"><a href="./step-06d-controlled-outputs/assert_dq_passed/"><code>assert_dq_passed</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Raise only after evidence materialization when error-severity rules fail.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_ai_quality_context" data-callable-module="data_profiling" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Build deterministic AI-ready context from standard metadata profile rows.">
  <h3 class="reference-catalogue-item-name"><a href="./step-04-ingest-profile-store/build_ai_quality_context/"><code>build_ai_quality_context</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Build deterministic AI-ready context from standard metadata profile rows.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_contract_summary" data-callable-module="data_contracts" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Build a concise contract summary for reviews and handover.">
  <h3 class="reference-catalogue-item-name"><a href="./step-07-output-profile-product-contract/build_contract_summary/"><code>build_contract_summary</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Build a concise contract summary for reviews and handover.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_dataset_run_record" data-callable-module="data_product_metadata" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Build a dataset-run metadata record for operational tracking.">
  <h3 class="reference-catalogue-item-name"><a href="./step-07-output-profile-product-contract/build_dataset_run_record/"><code>build_dataset_run_record</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Build a dataset-run metadata record for operational tracking.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_governance_candidate_prompt" data-callable-module="ai" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Build the governance-candidate prompt for AI-assisted classification drafts.">
  <h3 class="reference-catalogue-item-name"><a href="./step-09-ai-assisted-classification/build_governance_candidate_prompt/"><code>build_governance_candidate_prompt</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Build the governance-candidate prompt for AI-assisted classification drafts.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_governance_classification_records" data-callable-module="data_governance" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Build metadata-ready governance classification records from column suggestions.">
  <h3 class="reference-catalogue-item-name"><a href="./step-09-ai-assisted-classification/build_governance_classification_records/"><code>build_governance_classification_records</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Build metadata-ready governance classification records from column suggestions.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_handover_summary_prompt" data-callable-module="ai" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Build the handover-summary prompt for AI-assisted run handoff drafting.">
  <h3 class="reference-catalogue-item-name"><a href="./step-10-lineage-handover-documentation/build_handover_summary_prompt/"><code>build_handover_summary_prompt</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Build the handover-summary prompt for AI-assisted run handoff drafting.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_lineage_from_notebook_code" data-callable-module="data_lineage" data-callable-starter-path="02_ex" data-role="essential" data-callable-purpose="Scan, optionally enrich, and validate lineage from notebook source code.">
  <h3 class="reference-catalogue-item-name"><a href="./step-10-lineage-handover-documentation/build_lineage_from_notebook_code/"><code>build_lineage_from_notebook_code</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>02_ex</span></p>
  <p class="reference-catalogue-item-purpose">Scan, optionally enrich, and validate lineage from notebook source code.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_lineage_handover_markdown" data-callable-module="data_lineage" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Create a concise markdown handover summary from lineage execution results.">
  <h3 class="reference-catalogue-item-name"><a href="./step-10-lineage-handover-documentation/build_lineage_handover_markdown/"><code>build_lineage_handover_markdown</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Create a concise markdown handover summary from lineage execution results.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_lineage_records" data-callable-module="data_lineage" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Build compact lineage records for downstream metadata sinks.">
  <h3 class="reference-catalogue-item-name"><a href="./step-10-lineage-handover-documentation/build_lineage_records/"><code>build_lineage_records</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Build compact lineage records for downstream metadata sinks.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_manual_governance_prompt_package" data-callable-module="ai" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Build copy/paste prompt package for manual governance suggestion generation.">
  <h3 class="reference-catalogue-item-name"><a href="./step-09-ai-assisted-classification/build_manual_governance_prompt_package/"><code>build_manual_governance_prompt_package</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Build copy/paste prompt package for manual governance suggestion generation.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_manual_handover_prompt_package" data-callable-module="ai" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Build copy/paste prompt package for manual handover summary generation.">
  <h3 class="reference-catalogue-item-name"><a href="./step-10-lineage-handover-documentation/build_manual_handover_prompt_package/"><code>build_manual_handover_prompt_package</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Build copy/paste prompt package for manual handover summary generation.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_quality_result_records" data-callable-module="data_product_metadata" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Convert quality-rule execution output into metadata evidence records.">
  <h3 class="reference-catalogue-item-name"><a href="./step-07-output-profile-product-contract/build_quality_result_records/"><code>build_quality_result_records</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Convert quality-rule execution output into metadata evidence records.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_run_summary" data-callable-module="handover_documentation" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Build a handover-friendly summary for one data product run.">
  <h3 class="reference-catalogue-item-name"><a href="./step-10-lineage-handover-documentation/build_run_summary/"><code>build_run_summary</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Build a handover-friendly summary for one data product run.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_schema_drift_records" data-callable-module="data_product_metadata" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Convert schema drift results into metadata records for audit trails.">
  <h3 class="reference-catalogue-item-name"><a href="./step-04-ingest-profile-store/build_schema_drift_records/"><code>build_schema_drift_records</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Convert schema drift results into metadata records for audit trails.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_schema_snapshot_records" data-callable-module="data_product_metadata" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Convert a schema snapshot into row-wise metadata records.">
  <h3 class="reference-catalogue-item-name"><a href="./step-04-ingest-profile-store/build_schema_snapshot_records/"><code>build_schema_snapshot_records</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Convert a schema snapshot into row-wise metadata records.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="check_partition_drift" data-callable-module="data_drift" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Check partition-level drift using keys, partitions, and optional watermark baselines.">
  <h3 class="reference-catalogue-item-name"><a href="./step-04-ingest-profile-store/check_partition_drift/"><code>check_partition_drift</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Check partition-level drift using keys, partitions, and optional watermark baselines.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="check_profile_drift" data-callable-module="data_drift" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Compare profile metrics against a baseline profile and drift thresholds.">
  <h3 class="reference-catalogue-item-name"><a href="./step-04-ingest-profile-store/check_profile_drift/"><code>check_profile_drift</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Compare profile metrics against a baseline profile and drift thresholds.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="check_schema_drift" data-callable-module="data_drift" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Compare a current dataframe schema against a baseline schema snapshot.">
  <h3 class="reference-catalogue-item-name"><a href="./step-04-ingest-profile-store/check_schema_drift/"><code>check_schema_drift</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Compare a current dataframe schema against a baseline schema snapshot.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="classify_column" data-callable-module="data_governance" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Classify one column using term matching, metadata cues, and business context.">
  <h3 class="reference-catalogue-item-name"><a href="./step-09-ai-assisted-classification/classify_column/"><code>classify_column</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Classify one column using term matching, metadata cues, and business context.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="classify_columns" data-callable-module="data_governance" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Classify multiple columns and return normalized governance suggestions.">
  <h3 class="reference-catalogue-item-name"><a href="./step-09-ai-assisted-classification/classify_columns/"><code>classify_columns</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Classify multiple columns and return normalized governance suggestions.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="configure_fabric_ai_functions" data-callable-module="environment_config" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Apply optional default Fabric AI Function configuration.">
  <h3 class="reference-catalogue-item-name"><a href="./step-01-governance-context/configure_fabric_ai_functions/"><code>configure_fabric_ai_functions</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Apply optional default Fabric AI Function configuration.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="default_technical_columns" data-callable-module="technical_audit_columns" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Return framework-generated and legacy technical column names to ignore.">
  <h3 class="reference-catalogue-item-name"><a href="./step-06b-runtime-standards/default_technical_columns/"><code>default_technical_columns</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/technical_audit_columns/" title="Open technical_audit_columns module page" aria-label="Open technical_audit_columns module page">technical_audit_columns</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Return framework-generated and legacy technical column names to ignore.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="DQEnforcementResult" data-callable-module="data_quality" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Structured DQ enforcement output for notebook-first usage.">
  <h3 class="reference-catalogue-item-name"><a href="./step-06c-pipeline-controls/DQEnforcementResult/"><code>DQEnforcementResult</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Structured DQ enforcement output for notebook-first usage.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="draft_dq_rules" data-callable-module="data_quality" data-callable-starter-path="02_ex" data-role="essential" data-callable-purpose="Draft candidate DQ rules from metadata profiles or raw DataFrame fallback.">
  <h3 class="reference-catalogue-item-name"><a href="./step-08-ai-assisted-dq-suggestions/draft_dq_rules/"><code>draft_dq_rules</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>02_ex</span></p>
  <p class="reference-catalogue-item-purpose">Draft candidate DQ rules from metadata profiles or raw DataFrame fallback.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="enforce_dq_rules" data-callable-module="data_quality" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Run notebook-facing DQ rules and return a Spark DataFrame result.">
  <h3 class="reference-catalogue-item-name"><a href="./step-06c-pipeline-controls/enforce_dq_rules/"><code>enforce_dq_rules</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Run notebook-facing DQ rules and return a Spark DataFrame result.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="extract_business_keys" data-callable-module="data_contracts" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Extract business-key column names from a normalized contract.">
  <h3 class="reference-catalogue-item-name"><a href="./step-03-source-contract-ingestion-pattern/extract_business_keys/"><code>extract_business_keys</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Extract business-key column names from a normalized contract.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="extract_classifications" data-callable-module="data_contracts" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Extract column classification mappings from a normalized contract.">
  <h3 class="reference-catalogue-item-name"><a href="./step-03-source-contract-ingestion-pattern/extract_classifications/"><code>extract_classifications</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Extract column classification mappings from a normalized contract.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="extract_optional_columns" data-callable-module="data_contracts" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Extract optional column names from a normalized contract.">
  <h3 class="reference-catalogue-item-name"><a href="./step-03-source-contract-ingestion-pattern/extract_optional_columns/"><code>extract_optional_columns</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Extract optional column names from a normalized contract.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="extract_quality_rules" data-callable-module="data_contracts" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Extract raw quality-rule definitions from a normalized contract.">
  <h3 class="reference-catalogue-item-name"><a href="./step-03-source-contract-ingestion-pattern/extract_quality_rules/"><code>extract_quality_rules</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Extract raw quality-rule definitions from a normalized contract.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="extract_required_columns" data-callable-module="data_contracts" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Extract required column names from a normalized contract.">
  <h3 class="reference-catalogue-item-name"><a href="./step-03-source-contract-ingestion-pattern/extract_required_columns/"><code>extract_required_columns</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Extract required column names from a normalized contract.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="generate_governance_candidates_with_fabric_ai" data-callable-module="ai" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Execute Fabric AI Functions to append governance suggestions to a DataFrame.">
  <h3 class="reference-catalogue-item-name"><a href="./step-09-ai-assisted-classification/generate_governance_candidates_with_fabric_ai/"><code>generate_governance_candidates_with_fabric_ai</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Execute Fabric AI Functions to append governance suggestions to a DataFrame.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="generate_handover_summary_with_fabric_ai" data-callable-module="ai" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Execute Fabric AI Functions to append handover summary suggestions.">
  <h3 class="reference-catalogue-item-name"><a href="./step-10-lineage-handover-documentation/generate_handover_summary_with_fabric_ai/"><code>generate_handover_summary_with_fabric_ai</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Execute Fabric AI Functions to append handover summary suggestions.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="generate_metadata_profile" data-callable-module="data_profiling" data-callable-starter-path="02_ex" data-role="essential" data-callable-purpose="Generate standard metadata profile rows for a Spark/Fabric DataFrame.">
  <h3 class="reference-catalogue-item-name"><a href="./step-04-ingest-profile-store/generate_metadata_profile/"><code>generate_metadata_profile</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>02_ex</span></p>
  <p class="reference-catalogue-item-purpose">Generate standard metadata profile rows for a Spark/Fabric DataFrame.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="get_executable_quality_rules" data-callable-module="data_contracts" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Return normalized quality rules ready for pipeline enforcement.">
  <h3 class="reference-catalogue-item-name"><a href="./step-06c-pipeline-controls/get_executable_quality_rules/"><code>get_executable_quality_rules</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Return normalized quality rules ready for pipeline enforcement.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="get_path" data-callable-module="environment_config" data-callable-starter-path="00_env_config, 02_ex, 03_pc" data-role="essential" data-callable-purpose="Resolve a configured Fabric path for an environment and target.">
  <h3 class="reference-catalogue-item-name"><a href="./step-02a-shared-runtime-config/get_path/"><code>get_path</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>00_env_config, 02_ex, 03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Resolve a configured Fabric path for an environment and target.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="Housepath" data-callable-module="fabric_input_output" data-callable-starter-path="00_env_config" data-role="essential" data-callable-purpose="Fabric lakehouse or warehouse connection details.">
  <h3 class="reference-catalogue-item-name"><a href="./step-02a-shared-runtime-config/Housepath/"><code>Housepath</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>00_env_config</span></p>
  <p class="reference-catalogue-item-purpose">Fabric lakehouse or warehouse connection details.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="lakehouse_csv_read" data-callable-module="fabric_input_output" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Read a CSV file from a Fabric lakehouse Files path.">
  <h3 class="reference-catalogue-item-name"><a href="./step-03-source-contract-ingestion-pattern/lakehouse_csv_read/"><code>lakehouse_csv_read</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Read a CSV file from a Fabric lakehouse Files path.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="lakehouse_excel_read_as_spark" data-callable-module="fabric_input_output" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Read an Excel file from a Fabric lakehouse Files path.">
  <h3 class="reference-catalogue-item-name"><a href="./step-03-source-contract-ingestion-pattern/lakehouse_excel_read_as_spark/"><code>lakehouse_excel_read_as_spark</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Read an Excel file from a Fabric lakehouse Files path.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="lakehouse_parquet_read_as_spark" data-callable-module="fabric_input_output" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Read a Parquet file from a Fabric lakehouse Files path.">
  <h3 class="reference-catalogue-item-name"><a href="./step-03-source-contract-ingestion-pattern/lakehouse_parquet_read_as_spark/"><code>lakehouse_parquet_read_as_spark</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Read a Parquet file from a Fabric lakehouse Files path.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="lakehouse_table_read" data-callable-module="fabric_input_output" data-callable-starter-path="02_ex, 03_pc" data-role="essential" data-callable-purpose="Read a Delta table from a Fabric lakehouse.">
  <h3 class="reference-catalogue-item-name"><a href="./step-03-source-contract-ingestion-pattern/lakehouse_table_read/"><code>lakehouse_table_read</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>02_ex, 03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Read a Delta table from a Fabric lakehouse.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="lakehouse_table_write" data-callable-module="fabric_input_output" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Write a Spark DataFrame to a Fabric lakehouse Delta table.">
  <h3 class="reference-catalogue-item-name"><a href="./step-06d-controlled-outputs/lakehouse_table_write/"><code>lakehouse_table_write</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Write a Spark DataFrame to a Fabric lakehouse Delta table.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="load_contract_from_lakehouse" data-callable-module="data_contracts" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Load one contract by ID/version from Fabric metadata storage.">
  <h3 class="reference-catalogue-item-name"><a href="./step-03-source-contract-ingestion-pattern/load_contract_from_lakehouse/"><code>load_contract_from_lakehouse</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Load one contract by ID/version from Fabric metadata storage.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="load_fabric_config" data-callable-module="environment_config" data-callable-starter-path="00_env_config, 02_ex, 03_pc" data-role="essential" data-callable-purpose="Validate and return a user-supplied framework configuration.">
  <h3 class="reference-catalogue-item-name"><a href="./step-02a-shared-runtime-config/load_fabric_config/"><code>load_fabric_config</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>00_env_config, 02_ex, 03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Validate and return a user-supplied framework configuration.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="load_latest_approved_contract" data-callable-module="data_contracts" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Load the latest approved contract for a dataset/object pair.">
  <h3 class="reference-catalogue-item-name"><a href="./step-03-source-contract-ingestion-pattern/load_latest_approved_contract/"><code>load_latest_approved_contract</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Load the latest approved contract for a dataset/object pair.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="normalize_contract_dict" data-callable-module="data_contracts" data-callable-starter-path="02_ex" data-role="essential" data-callable-purpose="Normalize a notebook-authored contract dictionary to a stable shape.">
  <h3 class="reference-catalogue-item-name"><a href="./step-03-source-contract-ingestion-pattern/normalize_contract_dict/"><code>normalize_contract_dict</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>02_ex</span></p>
  <p class="reference-catalogue-item-purpose">Normalize a notebook-authored contract dictionary to a stable shape.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="parse_manual_ai_json_response" data-callable-module="ai" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Parse manual AI JSON output into Python objects.">
  <h3 class="reference-catalogue-item-name"><a href="./step-10-lineage-handover-documentation/parse_manual_ai_json_response/"><code>parse_manual_ai_json_response</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Parse manual AI JSON output into Python objects.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="plot_lineage_steps" data-callable-module="data_lineage" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Render lineage steps as a directed graph figure.">
  <h3 class="reference-catalogue-item-name"><a href="./step-10-lineage-handover-documentation/plot_lineage_steps/"><code>plot_lineage_steps</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Render lineage steps as a directed graph figure.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="profile_dataframe" data-callable-module="data_profiling" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Build a lightweight profile from a PySpark DataFrame.">
  <h3 class="reference-catalogue-item-name"><a href="./step-04-ingest-profile-store/profile_dataframe/"><code>profile_dataframe</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Build a lightweight profile from a PySpark DataFrame.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="profile_dataframe_to_metadata" data-callable-module="data_profiling" data-callable-starter-path="02_ex" data-role="essential" data-callable-purpose="Profile a Spark/Fabric DataFrame into metadata-compatible metadata rows.">
  <h3 class="reference-catalogue-item-name"><a href="./step-04-ingest-profile-store/profile_dataframe_to_metadata/"><code>profile_dataframe_to_metadata</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>02_ex</span></p>
  <p class="reference-catalogue-item-purpose">Profile a Spark/Fabric DataFrame into metadata-compatible metadata rows.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="profile_metadata_to_records" data-callable-module="data_profiling" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Convert Spark metadata profile rows into JSON-friendly dictionaries.">
  <h3 class="reference-catalogue-item-name"><a href="./step-04-ingest-profile-store/profile_metadata_to_records/"><code>profile_metadata_to_records</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Convert Spark metadata profile rows into JSON-friendly dictionaries.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="render_run_summary_markdown" data-callable-module="handover_documentation" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Render a run summary dictionary into Markdown for handover notes.">
  <h3 class="reference-catalogue-item-name"><a href="./step-10-lineage-handover-documentation/render_run_summary_markdown/"><code>render_run_summary_markdown</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/handover_documentation/" title="Open handover_documentation module page" aria-label="Open handover_documentation module page">handover_documentation</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Render a run summary dictionary into Markdown for handover notes.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="review_dq_rule_deactivations" data-callable-module="notebook_review" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Review active DQ rules one at a time for governed deactivation actions.">
  <h3 class="reference-catalogue-item-name"><a href="./step-08-ai-assisted-dq-suggestions/review_dq_rule_deactivations/"><code>review_dq_rule_deactivations</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/notebook_review/" title="Open notebook_review module page" aria-label="Open notebook_review module page">notebook_review</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Review active DQ rules one at a time for governed deactivation actions.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="review_dq_rules" data-callable-module="data_quality" data-callable-starter-path="02_ex" data-role="essential" data-callable-purpose="Review AI-suggested DQ rules sequentially with explicit approve/reject decisions.">
  <h3 class="reference-catalogue-item-name"><a href="./step-08-ai-assisted-dq-suggestions/review_dq_rules/"><code>review_dq_rules</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>02_ex</span></p>
  <p class="reference-catalogue-item-purpose">Review AI-suggested DQ rules sequentially with explicit approve/reject decisions.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="scan_notebook_cells" data-callable-module="data_lineage" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Scan multiple notebook cells and append cell references to lineage steps.">
  <h3 class="reference-catalogue-item-name"><a href="./step-10-lineage-handover-documentation/scan_notebook_cells/"><code>scan_notebook_cells</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Scan multiple notebook cells and append cell references to lineage steps.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="scan_notebook_lineage" data-callable-module="data_lineage" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Extract deterministic lineage steps from notebook code using AST parsing.">
  <h3 class="reference-catalogue-item-name"><a href="./step-10-lineage-handover-documentation/scan_notebook_lineage/"><code>scan_notebook_lineage</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Extract deterministic lineage steps from notebook code using AST parsing.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="seed_minimal_sample_source_table" data-callable-module="fabric_input_output" data-callable-starter-path="02_ex" data-role="optional" data-callable-purpose="Create and persist deterministic demo rows into a sample source table.">
  <h3 class="reference-catalogue-item-name"><a href="./step-04-ingest-profile-store/seed_minimal_sample_source_table/"><code>seed_minimal_sample_source_table</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>02_ex</span></p>
  <p class="reference-catalogue-item-purpose">Create and persist deterministic demo rows into a sample source table.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="setup_fabricops_notebook" data-callable-module="environment_config" data-callable-starter-path="00_env_config, 02_ex, 03_pc" data-role="essential" data-callable-purpose="Run consolidated FabricOps startup for exploration and pipeline notebooks.">
  <h3 class="reference-catalogue-item-name"><a href="./step-02b-notebook-startup-checks/setup_fabricops_notebook/"><code>setup_fabricops_notebook</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>00_env_config, 02_ex, 03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Run consolidated FabricOps startup for exploration and pipeline notebooks.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="summarize_drift_results" data-callable-module="data_drift" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Summarize schema, partition, and profile drift outcomes into one decision.">
  <h3 class="reference-catalogue-item-name"><a href="./step-04-ingest-profile-store/summarize_drift_results/"><code>summarize_drift_results</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Summarize schema, partition, and profile drift outcomes into one decision.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="summarize_governance_classifications" data-callable-module="data_governance" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Summarize governance classification outputs into review-friendly counts.">
  <h3 class="reference-catalogue-item-name"><a href="./step-09-ai-assisted-classification/summarize_governance_classifications/"><code>summarize_governance_classifications</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Summarize governance classification outputs into review-friendly counts.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="validate_contract_dict" data-callable-module="data_contracts" data-callable-starter-path="02_ex" data-role="essential" data-callable-purpose="Validate a contract dictionary and return error strings without raising.">
  <h3 class="reference-catalogue-item-name"><a href="./step-03-source-contract-ingestion-pattern/validate_contract_dict/"><code>validate_contract_dict</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>02_ex</span></p>
  <p class="reference-catalogue-item-purpose">Validate a contract dictionary and return error strings without raising.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="validate_dq_rules" data-callable-module="data_quality" data-callable-starter-path="03_pc" data-role="optional" data-callable-purpose="Validate canonical DQ rules before enforcement.">
  <h3 class="reference-catalogue-item-name"><a href="./step-06c-pipeline-controls/validate_dq_rules/"><code>validate_dq_rules</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Validate canonical DQ rules before enforcement.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="validate_lineage_steps" data-callable-module="data_lineage" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Validate lineage step structure and flag records requiring human review.">
  <h3 class="reference-catalogue-item-name"><a href="./step-10-lineage-handover-documentation/validate_lineage_steps/"><code>validate_lineage_steps</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Validate lineage step structure and flag records requiring human review.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="warehouse_read" data-callable-module="fabric_input_output" data-callable-starter-path="02_ex, 03_pc" data-role="essential" data-callable-purpose="Read a table from a Microsoft Fabric warehouse.">
  <h3 class="reference-catalogue-item-name"><a href="./step-03-source-contract-ingestion-pattern/warehouse_read/"><code>warehouse_read</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>02_ex, 03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Read a table from a Microsoft Fabric warehouse.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="warehouse_write" data-callable-module="fabric_input_output" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Write a Spark DataFrame to a Microsoft Fabric warehouse table.">
  <h3 class="reference-catalogue-item-name"><a href="./step-06d-controlled-outputs/warehouse_write/"><code>warehouse_write</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Write a Spark DataFrame to a Microsoft Fabric warehouse table.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="write_contract_to_lakehouse" data-callable-module="data_contracts" data-callable-starter-path="02_ex" data-role="essential" data-callable-purpose="Validate and persist contract records into Fabric metadata tables.">
  <h3 class="reference-catalogue-item-name"><a href="./step-07-output-profile-product-contract/write_contract_to_lakehouse/"><code>write_contract_to_lakehouse</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_contracts/" title="Open data_contracts module page" aria-label="Open data_contracts module page">data_contracts</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>02_ex</span></p>
  <p class="reference-catalogue-item-purpose">Validate and persist contract records into Fabric metadata tables.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="write_dq_rules" data-callable-module="data_quality" data-callable-starter-path="02_ex" data-role="essential" data-callable-purpose="Validate, build, and persist approved DQ rules.">
  <h3 class="reference-catalogue-item-name"><a href="./step-08-ai-assisted-dq-suggestions/write_dq_rules/"><code>write_dq_rules</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>02_ex</span></p>
  <p class="reference-catalogue-item-purpose">Validate, build, and persist approved DQ rules.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="write_governance_classifications" data-callable-module="data_governance" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Persist governance classifications to a metadata destination.">
  <h3 class="reference-catalogue-item-name"><a href="./step-09-ai-assisted-classification/write_governance_classifications/"><code>write_governance_classifications</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Persist governance classifications to a metadata destination.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="write_metadata_records" data-callable-module="data_product_metadata" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Write metadata records to a configured metadata sink.">
  <h3 class="reference-catalogue-item-name"><a href="./step-07-output-profile-product-contract/write_metadata_records/"><code>write_metadata_records</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Write metadata records to a configured metadata sink.</p>
</article>
<article class="reference-catalogue-item" data-callable-row="true" data-callable-name="write_multiple_metadata_outputs" data-callable-module="data_product_metadata" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Write multiple metadata payloads to their configured destinations.">
  <h3 class="reference-catalogue-item-name"><a href="./step-07-output-profile-product-contract/write_multiple_metadata_outputs/"><code>write_multiple_metadata_outputs</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Write multiple metadata payloads to their configured destinations.</p>
</article>
</div>

