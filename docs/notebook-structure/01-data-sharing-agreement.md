# `01_data_sharing_agreement_<agreement>`

This is the governance-owned control-plane notebook for one data sharing agreement. It defines the agreement, reviews metadata evidence, approves business context and classification/PII metadata, and makes approved metadata available to `02_ex` and `03_pc`.

- Keep `agreement_id` stable for the same agreement.
- Keep `save_to_metadata=False` while testing.
- Set `save_to_metadata=True` only when ready to write approved metadata.
- `02_ex` and `03_pc` reuse approved metadata from this notebook.
- DQ enforcement remains in `03_pc`.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/01_data_agreement_template.ipynb">Open template notebook</a>

## 01 Runtime bootstrap and imports

- `%run 00_env_config` must stay as its own standalone cell.
- Imports load governance, metadata, business context, DQ visibility, and notebook traceability helpers.
- Widget display is handled inside helper functions.
- Avoid importing `display` directly in the notebook except local aliases for custom HTML rendering.

## 02 Define and save agreement metadata

Governance defines agreement identity, approved usage, business context, ownership, permissions, restrictions, classification, sensitivity, PII posture, and related notebook links. This step builds `governance_prompt_context` and `agreement_context_metadata`, writes `METADATA_DATA_AGREEMENT` only when `save_to_metadata=True`, and registers the notebook to `METADATA_NOTEBOOK_REGISTRY` only when `save_to_metadata=True`.

<table class="reference-function-table notebook-structure-function-table">
  <thead><tr><th>Function / class</th><th>Module</th><th>Purpose</th></tr></thead>
  <tbody>
    <tr><td><a href="../../api/reference/build_governance_context/"><code>build_governance_context</code></a></td><td><a class="reference-module-link" href="../../api/modules/data_governance/">data_governance</a></td><td>Build agreement governance prompt context for downstream AI-assisted review steps.</td></tr>
    <tr><td><a href="../../api/reference/write_metadata_rows/"><code>write_metadata_rows</code></a></td><td><a class="reference-module-link" href="../../api/modules/data_product_metadata/">data_product_metadata</a></td><td>Persist agreement-level metadata rows when metadata writes are enabled.</td></tr>
    <tr><td><a href="../../api/reference/register_current_notebook/"><code>register_current_notebook</code></a></td><td><a class="reference-module-link" href="../../api/modules/data_product_metadata/">data_product_metadata</a></td><td>Register notebook traceability rows for agreement-level discoverability.</td></tr>
    <tr><td><a href="../../api/reference/step-02a-shared-runtime-config/get_path/"><code>get_path</code></a></td><td><a class="reference-module-link" href="../../api/modules/config/">config</a></td><td>Resolve canonical metadata table paths for reads and writes.</td></tr>
  </tbody>
</table>

## 03 Load existing metadata evidence and linked notebooks

This is the read-only evidence and traceability section. It loads `METADATA_PROFILE_ROWS`, `METADATA_DQ_RULES`, `METADATA_COLUMN_CONTEXT`, `METADATA_COLUMN_GOVERNANCE`, `METADATA_DATA_AGREEMENT`, and `METADATA_NOTEBOOK_REGISTRY`. Notebook links come from `METADATA_NOTEBOOK_REGISTRY` first, while `related_notebook_links` is fallback only.

<table class="reference-function-table notebook-structure-function-table">
  <thead><tr><th>Function / class</th><th>Module</th><th>Purpose</th></tr></thead>
  <tbody>
    <tr><td><a href="../../api/reference/load_notebook_registry/"><code>load_notebook_registry</code></a></td><td><a class="reference-module-link" href="../../api/modules/data_product_metadata/">data_product_metadata</a></td><td>Load notebook registration rows used to render linked notebook traceability first.</td></tr>
    <tr><td><a href="../../api/reference/load_governance/"><code>load_governance</code></a></td><td><a class="reference-module-link" href="../../api/modules/data_governance/">data_governance</a></td><td>Load approved governance metadata as read-only evidence context.</td></tr>
  </tbody>
</table>

## 04 Review and save column business context

This step uses existing profile rows as evidence. AI suggests column business context, a human reviewer approves or rejects suggestions using the widget, and approved rows write to `METADATA_COLUMN_CONTEXT` only when `save_to_metadata=True`.

<table class="reference-function-table notebook-structure-function-table">
  <thead><tr><th>Function / class</th><th>Module</th><th>Purpose</th></tr></thead>
  <tbody>
    <tr><td><a href="../../api/reference/prepare_business_context_profile_input/"><code>prepare_business_context_profile_input</code></a></td><td><a class="reference-module-link" href="../../api/modules/business_context/">business_context</a></td><td>Prepare profile evidence rows for business-context prompting.</td></tr>
    <tr><td><a href="../../api/reference/suggest_column_business_contexts/"><code>suggest_column_business_contexts</code></a></td><td><a class="reference-module-link" href="../../api/modules/business_context/">business_context</a></td><td>Generate AI-assisted column business-context suggestions.</td></tr>
    <tr><td><a href="../../api/reference/extract_column_business_context_suggestions/"><code>extract_column_business_context_suggestions</code></a></td><td><a class="reference-module-link" href="../../api/modules/business_context/">business_context</a></td><td>Extract review-ready business-context suggestion rows.</td></tr>
    <tr><td><a href="../../api/reference/capture_column_business_context/"><code>capture_column_business_context</code></a></td><td><a class="reference-module-link" href="../../api/modules/business_context/">business_context</a></td><td>Capture human approvals/rejections through the review widget.</td></tr>
    <tr><td><a href="../../api/reference/write_column_business_context/"><code>write_column_business_context</code></a></td><td><a class="reference-module-link" href="../../api/modules/data_product_metadata/">data_product_metadata</a></td><td>Write approved business-context rows when metadata writes are enabled.</td></tr>
  </tbody>
</table>

## 05 Review and save classification / sensitivity / PII

This step uses approved business context as input. AI suggests classification, sensitivity, and PII labels, then a human reviewer approves or rejects through the governance widget. Approved rows write to `METADATA_COLUMN_GOVERNANCE` only when `save_to_metadata=True`.

<table class="reference-function-table notebook-structure-function-table">
  <thead><tr><th>Function / class</th><th>Module</th><th>Purpose</th></tr></thead>
  <tbody>
    <tr><td><a href="../../api/reference/prepare_governance_input/"><code>prepare_governance_input</code></a></td><td><a class="reference-module-link" href="../../api/modules/data_governance/">data_governance</a></td><td>Join approved business-context evidence into governance prompt inputs.</td></tr>
    <tr><td><a href="../../api/reference/suggest_pii_labels/"><code>suggest_pii_labels</code></a></td><td><a class="reference-module-link" href="../../api/modules/data_governance/">data_governance</a></td><td>Generate AI-assisted classification, sensitivity, and PII suggestions.</td></tr>
    <tr><td><a href="../../api/reference/extract_pii_suggestions/"><code>extract_pii_suggestions</code></a></td><td><a class="reference-module-link" href="../../api/modules/data_governance/">data_governance</a></td><td>Extract structured governance review candidates from AI output.</td></tr>
    <tr><td><a href="../../api/reference/review_governance/"><code>review_governance</code></a></td><td><a class="reference-module-link" href="../../api/modules/data_governance/">data_governance</a></td><td>Run the governance widget to capture human approval decisions.</td></tr>
    <tr><td><a href="../../api/reference/write_governance/"><code>write_governance</code></a></td><td><a class="reference-module-link" href="../../api/modules/data_governance/">data_governance</a></td><td>Persist approved governance rows when metadata writes are enabled.</td></tr>
  </tbody>
</table>

## 06 View existing DQ rules

This section is read-only DQ visibility only. There is no DQ enforcement in this notebook; `03_pc` enforces approved DQ rules.

<table class="reference-function-table notebook-structure-function-table">
  <thead><tr><th>Function / class</th><th>Module</th><th>Purpose</th></tr></thead>
  <tbody>
    <tr><td><a href="../../api/reference/load_approved_dq_rules/"><code>load_approved_dq_rules</code></a></td><td><a class="reference-module-link" href="../../api/modules/data_quality/">data_quality</a></td><td>Load approved DQ rules for governance-side visibility.</td></tr>
  </tbody>
</table>
