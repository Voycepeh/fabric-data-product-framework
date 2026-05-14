# `01_data_sharing_agreement_<agreement>`

Governance-owned agreement source of truth used across environments, with a working review-and-approval flow.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/01_data_agreement_template.ipynb">Open template notebook</a>

## Segment 1: Define agreement metadata and bootstrap runtime

Set agreement-level governance context (`agreement_id`, approved usage, ownership, restrictions, classification/sensitivity/PII posture), then bootstrap runtime with `00_env_config` for metadata path resolution.

## Segment 2: Fetch profile and existing governance/DQ metadata

Load existing agreement/table metadata (profile rows, DQ rules, column context, column governance, agreement rows) with safe fallbacks when a metadata table is not created yet.

## Segment 3: Review and approve column business context

Use profile metadata to generate business-context suggestions and run the human approval widget.

<table class="reference-function-table notebook-structure-function-table">
  <thead><tr><th>Function / class</th><th>Module</th><th>Purpose</th></tr></thead>
  <tbody>
    <tr><td><a href="../../api/reference/prepare_business_context_profile_input/"><code>prepare_business_context_profile_input</code></a></td><td><a class="reference-module-link" href="../../api/modules/business_context/">business_context</a></td><td>Prepare profile rows for column business-context prompting.</td></tr>
    <tr><td><a href="../../api/reference/suggest_column_business_contexts/"><code>suggest_column_business_contexts</code></a></td><td><a class="reference-module-link" href="../../api/modules/business_context/">business_context</a></td><td>Generate AI-assisted business-context suggestions.</td></tr>
    <tr><td><a href="../../api/reference/extract_column_business_context_suggestions/"><code>extract_column_business_context_suggestions</code></a></td><td><a class="reference-module-link" href="../../api/modules/business_context/">business_context</a></td><td>Parse suggestion payloads into review rows.</td></tr>
    <tr><td><a href="../../api/reference/capture_column_business_context/"><code>capture_column_business_context</code></a></td><td><a class="reference-module-link" href="../../api/modules/business_context/">business_context</a></td><td>Run human-in-the-loop approval widget for business context.</td></tr>
    <tr><td><a href="../../api/reference/write_column_business_context/"><code>write_column_business_context</code></a></td><td><a class="reference-module-link" href="../../api/modules/data_product_metadata/">data_product_metadata</a></td><td>Persist approved business context rows.</td></tr>
  </tbody>
</table>

## Segment 4: Review classification / sensitivity / PII and write approved governance

Use approved business context as input for governance suggestions, run the governance review widget, and write approved rows only after human approval.

<table class="reference-function-table notebook-structure-function-table">
  <tbody>
    <tr><td><a href="../../api/reference/build_governance_context/"><code>build_governance_context</code></a></td><td><a class="reference-module-link" href="../../api/modules/data_governance/">data_governance</a></td><td>Build agreement governance prompt context.</td></tr>
    <tr><td><a href="../../api/reference/prepare_governance_input/"><code>prepare_governance_input</code></a></td><td><a class="reference-module-link" href="../../api/modules/data_governance/">data_governance</a></td><td>Join approved business context into governance prompt rows.</td></tr>
    <tr><td><a href="../../api/reference/suggest_pii_labels/"><code>suggest_pii_labels</code></a></td><td><a class="reference-module-link" href="../../api/modules/data_governance/">data_governance</a></td><td>Generate AI-assisted PII/classification suggestions.</td></tr>
    <tr><td><a href="../../api/reference/extract_pii_suggestions/"><code>extract_pii_suggestions</code></a></td><td><a class="reference-module-link" href="../../api/modules/data_governance/">data_governance</a></td><td>Extract structured governance review suggestions.</td></tr>
    <tr><td><a href="../../api/reference/review_governance/"><code>review_governance</code></a></td><td><a class="reference-module-link" href="../../api/modules/data_governance/">data_governance</a></td><td>Capture human governance approvals and rejections.</td></tr>
    <tr><td><a href="../../api/reference/write_governance/"><code>write_governance</code></a></td><td><a class="reference-module-link" href="../../api/modules/data_governance/">data_governance</a></td><td>Persist approved governance rows with agreement context.</td></tr>
    <tr><td><a href="../../api/reference/load_governance/"><code>load_governance</code></a></td><td><a class="reference-module-link" href="../../api/modules/data_governance/">data_governance</a></td><td>Load approved governance metadata as downstream read-only context.</td></tr>
  </tbody>
</table>

## Segment 5: DQ visibility and notebook registry links across environments/workspaces

Display existing approved DQ rules for governance visibility (read-only; no enforcement), and render clickable notebook registry links for one `agreement_id` across environments/workspaces.

<table class="reference-function-table notebook-structure-function-table">
  <tbody>
    <tr><td><a href="../../api/reference/load_approved_dq_rules/"><code>load_approved_dq_rules</code></a></td><td><a class="reference-module-link" href="../../api/modules/data_quality/">data_quality</a></td><td>Load active approved DQ rules for read-only governance visibility.</td></tr>
    <tr><td><a href="../../api/reference/write_metadata_rows/"><code>write_metadata_rows</code></a></td><td><a class="reference-module-link" href="../../api/modules/data_product_metadata/">data_product_metadata</a></td><td>Persist agreement-level metadata records.</td></tr>
    <tr><td><a href="../../api/reference/step-02a-shared-runtime-config/get_path/"><code>get_path</code></a></td><td><a class="reference-module-link" href="../../api/modules/config/">config</a></td><td>Resolve metadata path for read/write operations.</td></tr>
  </tbody>
</table>


## Agreement and notebook registration flow

- Notebook `01` creates and saves agreement metadata into `METADATA_DATA_AGREEMENT`.
- Notebooks `02_ex` and `03_pc` use a widget to select an existing agreement from `METADATA_DATA_AGREEMENT`; users do not need to type `agreement_id`.
- Notebooks `01`, `02_ex`, and `03_pc` self-register to `METADATA_NOTEBOOK_REGISTRY`.
- Notebook `01` fetches clickable notebook links from `METADATA_NOTEBOOK_REGISTRY` for the selected agreement.
- `related_notebook_links` remains a fallback/manual bridge when registry rows are not available.
