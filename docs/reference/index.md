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
      <td data-label="Guided usage">Pipeline notebook flow for deterministic enforcement and controlled publishing.<br><a href="../notebook-structure/03-pipeline-contract/">View guided structure</a></td>
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

Use the finder below to look up public callable functions.

<div class="callable-finder" data-callable-finder>
  <label class="callable-finder-label" for="callable-finder-input">Search callable functions</label>
  <input id="callable-finder-input" class="callable-finder-input" type="search" placeholder="Search callable functions" aria-describedby="callable-finder-help callable-finder-status callable-finder-examples" autocomplete="off">
  <p id="callable-finder-help" class="callable-finder-help">Search by function name, module, role, starter path, or what the public function does.</p>
  <p id="callable-finder-examples" class="callable-finder-examples">Try: <span class="callable-finder-chip">csv</span> <span class="callable-finder-chip">data_quality</span> <span class="callable-finder-chip">quarantine</span></p>
  <p id="callable-finder-status" class="callable-finder-status" aria-live="polite">Showing all public callables.</p>
  <fieldset class="callable-role-filters">
    <legend>Role filters</legend>
    <label><input type="checkbox" data-role-filter="essential" checked> Essential</label>
    <p class="callable-role-note"><strong>Essential</strong>: Core functions used in the starter notebook flow.</p>
    <label><input type="checkbox" data-role-filter="optional" checked> Optional</label>
    <p class="callable-role-note"><strong>Optional</strong>: Extra helper functions for advanced or situational use.</p>
  </fieldset>
  <p class="callable-finder-empty" data-callable-finder-empty hidden>No callables match your search.</p>
</div>

## Function catalogue

## All public functions

<div class="reference-catalogue-list">
<article id="assert_dq_passed" class="reference-catalogue-item" data-callable-row="true" data-callable-name="assert_dq_passed" data-callable-module="data_quality" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Raise only after evidence materialization when error-severity rules fail.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/assert_dq_passed/"><code>assert_dq_passed</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Raise only after evidence materialization when error-severity rules fail.</p>
</article>
<article id="attach_rule_metadata_keys" class="reference-catalogue-item" data-callable-row="true" data-callable-name="attach_rule_metadata_keys" data-callable-module="data_quality" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Attach deterministic metadata keys to candidate DQ rules.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/attach_rule_metadata_keys/"><code>attach_rule_metadata_keys</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Attach deterministic metadata keys to candidate DQ rules.</p>
</article>
<article id="build_dq_review_rows" class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_dq_review_rows" data-callable-module="data_quality" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Build notebook-editable DQ review rows without changing rule taxonomy.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/build_dq_review_rows/"><code>build_dq_review_rows</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Build notebook-editable DQ review rows without changing rule taxonomy.</p>
</article>
<article id="build_dq_rule_deactivation_metadata_df" class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_dq_rule_deactivation_metadata_df" data-callable-module="data_quality" data-callable-starter-path="—" data-role="optional" data-callable-purpose="—">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/build_dq_rule_deactivation_metadata_df/"><code>build_dq_rule_deactivation_metadata_df</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">—</p>
</article>
<article id="build_dq_rule_key" class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_dq_rule_key" data-callable-module="data_product_metadata" data-callable-starter-path="—" data-role="optional" data-callable-purpose="—">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/build_dq_rule_key/"><code>build_dq_rule_key</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">—</p>
</article>
<article id="build_dq_rules_metadata_df" class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_dq_rules_metadata_df" data-callable-module="data_quality" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Build approved DQ metadata rows as a Spark DataFrame.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/build_dq_rules_metadata_df/"><code>build_dq_rules_metadata_df</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Build approved DQ metadata rows as a Spark DataFrame.</p>
</article>
<article id="build_governance_candidate_prompt" class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_governance_candidate_prompt" data-callable-module="ai" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Build the governance-candidate prompt for AI-assisted classification drafts.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/build_governance_candidate_prompt/"><code>build_governance_candidate_prompt</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Build the governance-candidate prompt for AI-assisted classification drafts.</p>
</article>
<article id="build_governance_context" class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_governance_context" data-callable-module="data_governance" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Build governance prompt context fields for notebook workflows.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/build_governance_context/"><code>build_governance_context</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Build governance prompt context fields for notebook workflows.</p>
</article>
<article id="build_handover_summary_prompt" class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_handover_summary_prompt" data-callable-module="ai" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Build the handover-summary prompt for AI-assisted run handoff drafting.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/build_handover_summary_prompt/"><code>build_handover_summary_prompt</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Build the handover-summary prompt for AI-assisted run handoff drafting.</p>
</article>
<article id="build_lineage_from_notebook_code" class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_lineage_from_notebook_code" data-callable-module="data_lineage" data-callable-starter-path="02_ex" data-role="essential" data-callable-purpose="Scan, optionally enrich, and validate lineage from notebook source code.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/build_lineage_from_notebook_code/"><code>build_lineage_from_notebook_code</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>02_ex</span></p>
  <p class="reference-catalogue-item-purpose">Scan, optionally enrich, and validate lineage from notebook source code.</p>
</article>
<article id="build_lineage_handover_markdown" class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_lineage_handover_markdown" data-callable-module="data_lineage" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Create a concise markdown handover summary from lineage execution results.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/build_lineage_handover_markdown/"><code>build_lineage_handover_markdown</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Create a concise markdown handover summary from lineage execution results.</p>
</article>
<article id="build_lineage_records" class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_lineage_records" data-callable-module="data_lineage" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Build compact lineage records for downstream metadata sinks.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/build_lineage_records/"><code>build_lineage_records</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Build compact lineage records for downstream metadata sinks.</p>
</article>
<article id="build_manual_governance_prompt_package" class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_manual_governance_prompt_package" data-callable-module="ai" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Build copy/paste prompt package for manual governance suggestion generation.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/build_manual_governance_prompt_package/"><code>build_manual_governance_prompt_package</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Build copy/paste prompt package for manual governance suggestion generation.</p>
</article>
<article id="build_manual_handover_prompt_package" class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_manual_handover_prompt_package" data-callable-module="ai" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Build copy/paste prompt package for manual handover summary generation.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/build_manual_handover_prompt_package/"><code>build_manual_handover_prompt_package</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Build copy/paste prompt package for manual handover summary generation.</p>
</article>
<article id="build_metadata_column_key" class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_metadata_column_key" data-callable-module="data_product_metadata" data-callable-starter-path="—" data-role="optional" data-callable-purpose="—">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/build_metadata_column_key/"><code>build_metadata_column_key</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">—</p>
</article>
<article id="build_metadata_table_key" class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_metadata_table_key" data-callable-module="data_product_metadata" data-callable-starter-path="—" data-role="optional" data-callable-purpose="—">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/build_metadata_table_key/"><code>build_metadata_table_key</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">—</p>
</article>
<article id="build_run_summary" class="reference-catalogue-item" data-callable-row="true" data-callable-name="build_run_summary" data-callable-module="run_summary" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Build a handover-friendly summary for one data product run.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/build_run_summary/"><code>build_run_summary</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/run_summary/" title="Open run_summary module page" aria-label="Open run_summary module page">run_summary</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Build a handover-friendly summary for one data product run.</p>
</article>
<article id="capture_column_business_context" class="reference-catalogue-item" data-callable-row="true" data-callable-name="capture_column_business_context" data-callable-module="business_context" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Display interactive approval widget.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/capture_column_business_context/"><code>capture_column_business_context</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/business_context/" title="Open business_context module page" aria-label="Open business_context module page">business_context</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Display interactive approval widget.</p>
</article>
<article id="check_partition_drift" class="reference-catalogue-item" data-callable-row="true" data-callable-name="check_partition_drift" data-callable-module="data_drift" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Check partition-level drift using keys, partitions, and optional watermark baselines.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/check_partition_drift/"><code>check_partition_drift</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Check partition-level drift using keys, partitions, and optional watermark baselines.</p>
</article>
<article id="check_profile_drift" class="reference-catalogue-item" data-callable-row="true" data-callable-name="check_profile_drift" data-callable-module="data_drift" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Compare profile metrics against a baseline profile and drift thresholds.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/check_profile_drift/"><code>check_profile_drift</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Compare profile metrics against a baseline profile and drift thresholds.</p>
</article>
<article id="check_schema_drift" class="reference-catalogue-item" data-callable-row="true" data-callable-name="check_schema_drift" data-callable-module="data_drift" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Compare a current dataframe schema against a baseline schema snapshot.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/check_schema_drift/"><code>check_schema_drift</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Compare a current dataframe schema against a baseline schema snapshot.</p>
</article>
<article id="draft_dq_rules" class="reference-catalogue-item" data-callable-row="true" data-callable-name="draft_dq_rules" data-callable-module="data_quality" data-callable-starter-path="02_ex" data-role="essential" data-callable-purpose="Draft candidate DQ rules from metadata profiles or raw DataFrame fallback.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/draft_dq_rules/"><code>draft_dq_rules</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>02_ex</span></p>
  <p class="reference-catalogue-item-purpose">Draft candidate DQ rules from metadata profiles or raw DataFrame fallback.</p>
</article>
<article id="enforce_dq_rules" class="reference-catalogue-item" data-callable-row="true" data-callable-name="enforce_dq_rules" data-callable-module="data_quality" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Run notebook-facing DQ rules and return a Spark DataFrame result.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/enforce_dq_rules/"><code>enforce_dq_rules</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Run notebook-facing DQ rules and return a Spark DataFrame result.</p>
</article>
<article id="extract_candidate_rules_from_responses" class="reference-catalogue-item" data-callable-row="true" data-callable-name="extract_candidate_rules_from_responses" data-callable-module="data_quality" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Extract candidate DQ rules from Spark/list AI responses.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/extract_candidate_rules_from_responses/"><code>extract_candidate_rules_from_responses</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Extract candidate DQ rules from Spark/list AI responses.</p>
</article>
<article id="extract_column_business_context_suggestions" class="reference-catalogue-item" data-callable-row="true" data-callable-name="extract_column_business_context_suggestions" data-callable-module="business_context" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Parse AI suggestion rows from Spark DataFrames or ``list[dict]`` payloads.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/extract_column_business_context_suggestions/"><code>extract_column_business_context_suggestions</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/business_context/" title="Open business_context module page" aria-label="Open business_context module page">business_context</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Parse AI suggestion rows from Spark DataFrames or ``list[dict]`` payloads.</p>
</article>
<article id="extract_pii_suggestions" class="reference-catalogue-item" data-callable-row="true" data-callable-name="extract_pii_suggestions" data-callable-module="data_governance" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Extract governance suggestions from Spark/list response payloads.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/extract_pii_suggestions/"><code>extract_pii_suggestions</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Extract governance suggestions from Spark/list response payloads.</p>
</article>
<article id="generate_governance_candidates_with_fabric_ai" class="reference-catalogue-item" data-callable-row="true" data-callable-name="generate_governance_candidates_with_fabric_ai" data-callable-module="ai" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Execute Fabric AI Functions to append governance suggestions to a DataFrame.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/generate_governance_candidates_with_fabric_ai/"><code>generate_governance_candidates_with_fabric_ai</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Execute Fabric AI Functions to append governance suggestions to a DataFrame.</p>
</article>
<article id="generate_handover_summary_with_fabric_ai" class="reference-catalogue-item" data-callable-row="true" data-callable-name="generate_handover_summary_with_fabric_ai" data-callable-module="ai" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Execute Fabric AI Functions to append handover summary suggestions.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/generate_handover_summary_with_fabric_ai/"><code>generate_handover_summary_with_fabric_ai</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Execute Fabric AI Functions to append handover summary suggestions.</p>
</article>
<article id="get_path" class="reference-catalogue-item" data-callable-row="true" data-callable-name="get_path" data-callable-module="environment_config" data-callable-starter-path="00_env_config, 02_ex, 03_pc" data-role="essential" data-callable-purpose="Resolve a configured Fabric path for an environment and target.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/get_path/"><code>get_path</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>00_env_config, 02_ex, 03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Resolve a configured Fabric path for an environment and target.</p>
</article>
<article id="lakehouse_csv_read" class="reference-catalogue-item" data-callable-row="true" data-callable-name="lakehouse_csv_read" data-callable-module="fabric_input_output" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Read a CSV file from a Fabric lakehouse Files path.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/lakehouse_csv_read/"><code>lakehouse_csv_read</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Read a CSV file from a Fabric lakehouse Files path.</p>
</article>
<article id="lakehouse_excel_read_as_spark" class="reference-catalogue-item" data-callable-row="true" data-callable-name="lakehouse_excel_read_as_spark" data-callable-module="fabric_input_output" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Read an Excel file from a Fabric lakehouse Files path.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/lakehouse_excel_read_as_spark/"><code>lakehouse_excel_read_as_spark</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Read an Excel file from a Fabric lakehouse Files path.</p>
</article>
<article id="lakehouse_parquet_read_as_spark" class="reference-catalogue-item" data-callable-row="true" data-callable-name="lakehouse_parquet_read_as_spark" data-callable-module="fabric_input_output" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Read a Parquet file from a Fabric lakehouse Files path.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/lakehouse_parquet_read_as_spark/"><code>lakehouse_parquet_read_as_spark</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Read a Parquet file from a Fabric lakehouse Files path.</p>
</article>
<article id="lakehouse_table_read" class="reference-catalogue-item" data-callable-row="true" data-callable-name="lakehouse_table_read" data-callable-module="fabric_input_output" data-callable-starter-path="02_ex, 03_pc" data-role="essential" data-callable-purpose="Read a Delta table from a Fabric lakehouse.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/lakehouse_table_read/"><code>lakehouse_table_read</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>02_ex, 03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Read a Delta table from a Fabric lakehouse.</p>
</article>
<article id="lakehouse_table_write" class="reference-catalogue-item" data-callable-row="true" data-callable-name="lakehouse_table_write" data-callable-module="fabric_input_output" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Write a Spark DataFrame to a Fabric lakehouse Delta table.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/lakehouse_table_write/"><code>lakehouse_table_write</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Write a Spark DataFrame to a Fabric lakehouse Delta table.</p>
</article>
<article id="load_fabric_config" class="reference-catalogue-item" data-callable-row="true" data-callable-name="load_fabric_config" data-callable-module="environment_config" data-callable-starter-path="00_env_config, 02_ex, 03_pc" data-role="essential" data-callable-purpose="Validate and return a user-supplied framework configuration.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/load_fabric_config/"><code>load_fabric_config</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>00_env_config, 02_ex, 03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Validate and return a user-supplied framework configuration.</p>
</article>
<article id="load_governance" class="reference-catalogue-item" data-callable-row="true" data-callable-name="load_governance" data-callable-module="data_governance" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Load approved governance metadata as read-only context.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/load_governance/"><code>load_governance</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Load approved governance metadata as read-only context.</p>
</article>
<article id="parse_manual_ai_json_response" class="reference-catalogue-item" data-callable-row="true" data-callable-name="parse_manual_ai_json_response" data-callable-module="ai" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Parse manual AI JSON output into Python objects.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/parse_manual_ai_json_response/"><code>parse_manual_ai_json_response</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/ai/" title="Open ai module page" aria-label="Open ai module page">ai</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Parse manual AI JSON output into Python objects.</p>
</article>
<article id="plot_lineage_steps" class="reference-catalogue-item" data-callable-row="true" data-callable-name="plot_lineage_steps" data-callable-module="data_lineage" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Render lineage steps as a directed graph figure.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/plot_lineage_steps/"><code>plot_lineage_steps</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Render lineage steps as a directed graph figure.</p>
</article>
<article id="prepare_business_context_profile_input" class="reference-catalogue-item" data-callable-row="true" data-callable-name="prepare_business_context_profile_input" data-callable-module="business_context" data-callable-starter-path="—" data-role="optional" data-callable-purpose="—">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/prepare_business_context_profile_input/"><code>prepare_business_context_profile_input</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/business_context/" title="Open business_context module page" aria-label="Open business_context module page">business_context</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">—</p>
</article>
<article id="prepare_governance_input" class="reference-catalogue-item" data-callable-row="true" data-callable-name="prepare_governance_input" data-callable-module="data_governance" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Join approved business context into profile rows for governance AI suggestions.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/prepare_governance_input/"><code>prepare_governance_input</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Join approved business context into profile rows for governance AI suggestions.</p>
</article>
<article id="profile_dataframe" class="reference-catalogue-item" data-callable-row="true" data-callable-name="profile_dataframe" data-callable-module="data_profiling" data-callable-starter-path="02_ex, 03_pc" data-role="essential" data-callable-purpose="Build canonical DQ-ready profiling rows from a Spark DataFrame.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/profile_dataframe/"><code>profile_dataframe</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_profiling/" title="Open data_profiling module page" aria-label="Open data_profiling module page">data_profiling</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>02_ex, 03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Build canonical DQ-ready profiling rows from a Spark DataFrame.</p>
</article>
<article id="render_run_summary_markdown" class="reference-catalogue-item" data-callable-row="true" data-callable-name="render_run_summary_markdown" data-callable-module="run_summary" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Render a run summary dictionary into Markdown for handover notes.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/render_run_summary_markdown/"><code>render_run_summary_markdown</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/run_summary/" title="Open run_summary module page" aria-label="Open run_summary module page">run_summary</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Render a run summary dictionary into Markdown for handover notes.</p>
</article>
<article id="review_dq_rule_deactivations" class="reference-catalogue-item" data-callable-row="true" data-callable-name="review_dq_rule_deactivations" data-callable-module="data_quality" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Review active DQ rules one at a time for governed deactivation actions.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/review_dq_rule_deactivations/"><code>review_dq_rule_deactivations</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Review active DQ rules one at a time for governed deactivation actions.</p>
</article>
<article id="review_dq_rules" class="reference-catalogue-item" data-callable-row="true" data-callable-name="review_dq_rules" data-callable-module="data_quality" data-callable-starter-path="02_ex" data-role="essential" data-callable-purpose="Review AI-suggested DQ rules sequentially with explicit approve/reject decisions.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/review_dq_rules/"><code>review_dq_rules</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>02_ex</span></p>
  <p class="reference-catalogue-item-purpose">Review AI-suggested DQ rules sequentially with explicit approve/reject decisions.</p>
</article>
<article id="review_governance" class="reference-catalogue-item" data-callable-row="true" data-callable-name="review_governance" data-callable-module="data_governance" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Display governance review widget and capture decisions.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/review_governance/"><code>review_governance</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Display governance review widget and capture decisions.</p>
</article>
<article id="scan_notebook_cells" class="reference-catalogue-item" data-callable-row="true" data-callable-name="scan_notebook_cells" data-callable-module="data_lineage" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Scan multiple notebook cells and append cell references to lineage steps.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/scan_notebook_cells/"><code>scan_notebook_cells</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Scan multiple notebook cells and append cell references to lineage steps.</p>
</article>
<article id="scan_notebook_lineage" class="reference-catalogue-item" data-callable-row="true" data-callable-name="scan_notebook_lineage" data-callable-module="data_lineage" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Extract deterministic lineage steps from notebook code using AST parsing.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/scan_notebook_lineage/"><code>scan_notebook_lineage</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Extract deterministic lineage steps from notebook code using AST parsing.</p>
</article>
<article id="seed_minimal_sample_source_table" class="reference-catalogue-item" data-callable-row="true" data-callable-name="seed_minimal_sample_source_table" data-callable-module="fabric_input_output" data-callable-starter-path="02_ex" data-role="optional" data-callable-purpose="Create and persist deterministic demo rows into a sample source table.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/seed_minimal_sample_source_table/"><code>seed_minimal_sample_source_table</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>02_ex</span></p>
  <p class="reference-catalogue-item-purpose">Create and persist deterministic demo rows into a sample source table.</p>
</article>
<article id="setup_fabricops_notebook" class="reference-catalogue-item" data-callable-row="true" data-callable-name="setup_fabricops_notebook" data-callable-module="environment_config" data-callable-starter-path="00_env_config, 02_ex, 03_pc" data-role="essential" data-callable-purpose="Run consolidated FabricOps startup for exploration and pipeline notebooks.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/setup_fabricops_notebook/"><code>setup_fabricops_notebook</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>00_env_config, 02_ex, 03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Run consolidated FabricOps startup for exploration and pipeline notebooks.</p>
</article>
<article id="standardize_output_columns" class="reference-catalogue-item" data-callable-row="true" data-callable-name="standardize_output_columns" data-callable-module="technical_columns" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Apply canonical technical/audit enrichment in one notebook-facing wrapper.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/standardize_output_columns/"><code>standardize_output_columns</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/technical_columns/" title="Open technical_columns module page" aria-label="Open technical_columns module page">technical_columns</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Apply canonical technical/audit enrichment in one notebook-facing wrapper.</p>
</article>
<article id="suggest_column_business_contexts" class="reference-catalogue-item" data-callable-row="true" data-callable-name="suggest_column_business_contexts" data-callable-module="business_context" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Run Fabric AI to draft column business context suggestions.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/suggest_column_business_contexts/"><code>suggest_column_business_contexts</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/business_context/" title="Open business_context module page" aria-label="Open business_context module page">business_context</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Run Fabric AI to draft column business context suggestions.</p>
</article>
<article id="suggest_dq_rules_with_fabric_ai" class="reference-catalogue-item" data-callable-row="true" data-callable-name="suggest_dq_rules_with_fabric_ai" data-callable-module="data_quality" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Run Fabric AI to draft DQ rules from prepared profile rows.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/suggest_dq_rules_with_fabric_ai/"><code>suggest_dq_rules_with_fabric_ai</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Run Fabric AI to draft DQ rules from prepared profile rows.</p>
</article>
<article id="suggest_pii_labels" class="reference-catalogue-item" data-callable-row="true" data-callable-name="suggest_pii_labels" data-callable-module="data_governance" data-callable-starter-path="—" data-role="essential" data-callable-purpose="Run Fabric AI personal-identifier suggestion prompt on prepared governance rows.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/suggest_pii_labels/"><code>suggest_pii_labels</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Run Fabric AI personal-identifier suggestion prompt on prepared governance rows.</p>
</article>
<article id="summarize_drift_results" class="reference-catalogue-item" data-callable-row="true" data-callable-name="summarize_drift_results" data-callable-module="data_drift" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Summarize schema, partition, and profile drift outcomes into one decision.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/summarize_drift_results/"><code>summarize_drift_results</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_drift/" title="Open data_drift module page" aria-label="Open data_drift module page">data_drift</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Summarize schema, partition, and profile drift outcomes into one decision.</p>
</article>
<article id="validate_dq_rules" class="reference-catalogue-item" data-callable-row="true" data-callable-name="validate_dq_rules" data-callable-module="data_quality" data-callable-starter-path="03_pc" data-role="optional" data-callable-purpose="Validate canonical DQ rules before enforcement.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/validate_dq_rules/"><code>validate_dq_rules</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Validate canonical DQ rules before enforcement.</p>
</article>
<article id="validate_lineage_steps" class="reference-catalogue-item" data-callable-row="true" data-callable-name="validate_lineage_steps" data-callable-module="data_lineage" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Validate lineage step structure and flag records requiring human review.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/validate_lineage_steps/"><code>validate_lineage_steps</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_lineage/" title="Open data_lineage module page" aria-label="Open data_lineage module page">data_lineage</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Validate lineage step structure and flag records requiring human review.</p>
</article>
<article id="warehouse_read" class="reference-catalogue-item" data-callable-row="true" data-callable-name="warehouse_read" data-callable-module="fabric_input_output" data-callable-starter-path="02_ex, 03_pc" data-role="essential" data-callable-purpose="Read a table from a Microsoft Fabric warehouse.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/warehouse_read/"><code>warehouse_read</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>02_ex, 03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Read a table from a Microsoft Fabric warehouse.</p>
</article>
<article id="warehouse_write" class="reference-catalogue-item" data-callable-row="true" data-callable-name="warehouse_write" data-callable-module="fabric_input_output" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Write a Spark DataFrame to a Microsoft Fabric warehouse table.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/warehouse_write/"><code>warehouse_write</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Write a Spark DataFrame to a Microsoft Fabric warehouse table.</p>
</article>
<article id="write_column_business_context" class="reference-catalogue-item" data-callable-row="true" data-callable-name="write_column_business_context" data-callable-module="data_product_metadata" data-callable-starter-path="—" data-role="optional" data-callable-purpose="—">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/write_column_business_context/"><code>write_column_business_context</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">—</p>
</article>
<article id="write_column_governance_context" class="reference-catalogue-item" data-callable-row="true" data-callable-name="write_column_governance_context" data-callable-module="data_product_metadata" data-callable-starter-path="—" data-role="optional" data-callable-purpose="—">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/write_column_governance_context/"><code>write_column_governance_context</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">—</p>
</article>
<article id="write_dq_rules" class="reference-catalogue-item" data-callable-row="true" data-callable-name="write_dq_rules" data-callable-module="data_quality" data-callable-starter-path="02_ex" data-role="essential" data-callable-purpose="Validate, build, and persist approved DQ rules.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/write_dq_rules/"><code>write_dq_rules</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_quality/" title="Open data_quality module page" aria-label="Open data_quality module page">data_quality</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>02_ex</span></p>
  <p class="reference-catalogue-item-purpose">Validate, build, and persist approved DQ rules.</p>
</article>
<article id="write_governance" class="reference-catalogue-item" data-callable-row="true" data-callable-name="write_governance" data-callable-module="data_governance" data-callable-starter-path="03_pc" data-role="essential" data-callable-purpose="Persist approved governance rows to metadata table.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/write_governance/"><code>write_governance</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_governance/" title="Open data_governance module page" aria-label="Open data_governance module page">data_governance</a> <span class="reference-catalogue-separator">·</span> <span>essential</span> <span class="reference-catalogue-separator">·</span> <span>03_pc</span></p>
  <p class="reference-catalogue-item-purpose">Persist approved governance rows to metadata table.</p>
</article>
<article id="write_metadata_rows" class="reference-catalogue-item" data-callable-row="true" data-callable-name="write_metadata_rows" data-callable-module="data_product_metadata" data-callable-starter-path="—" data-role="optional" data-callable-purpose="Write metadata rows to a lakehouse metadata table.">
  <h3 class="reference-catalogue-item-name"><a href="../api/reference/write_metadata_rows/"><code>write_metadata_rows</code></a></h3>
  <p class="reference-catalogue-item-meta"><a class="reference-module-link" href="../api/modules/data_product_metadata/" title="Open data_product_metadata module page" aria-label="Open data_product_metadata module page">data_product_metadata</a> <span class="reference-catalogue-separator">·</span> <span>optional</span> <span class="reference-catalogue-separator">·</span> <span>—</span></p>
  <p class="reference-catalogue-item-purpose">Write metadata rows to a lakehouse metadata table.</p>
</article>
</div>

