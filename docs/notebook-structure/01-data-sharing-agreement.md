# `01_data_sharing_agreement_<agreement>`

Governance-owned agreement source of truth used across environments.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/01_data_agreement_template.ipynb">Open template notebook</a>

## Segment 1: Define agreement purpose and approved usage

Capture the agreement intent, approved usage boundaries, and high-level context that downstream notebooks consume as read-only guidance.

## Segment 2: Capture ownership, permissions, restrictions, and business context

Record owner and steward accountability, business context, and approved access constraints for the agreement.

## Segment 3: Review AI-assisted classification / sensitivity / PII suggestions

AI suggestions are optional and advisory. Human reviewers decide whether suggestions are accepted, edited, or rejected.

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
      <td data-label="Function / class"><a href="../../api/reference/build_governance_context/"><code>build_governance_context</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_governance/">data_governance</a></td>
      <td data-label="Purpose">Build governance prompt context fields for notebook workflows.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../api/reference/prepare_governance_input/"><code>prepare_governance_input</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_governance/">data_governance</a></td>
      <td data-label="Purpose">Join approved business context into profile rows for governance AI suggestions.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../api/reference/suggest_pii_labels/"><code>suggest_pii_labels</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_governance/">data_governance</a></td>
      <td data-label="Purpose">Run Fabric AI personal-identifier suggestion prompt on prepared governance rows.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../api/reference/extract_pii_suggestions/"><code>extract_pii_suggestions</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_governance/">data_governance</a></td>
      <td data-label="Purpose">Extract governance suggestions from Spark/list response payloads.</td>
    </tr>
  </tbody>
</table>

## Segment 4: Human approval and metadata write-back

Human approval is mandatory before metadata write-back. This notebook defines governance metadata; it does not enforce DQ rules.

<table class="reference-function-table notebook-structure-function-table">
  <tbody>
    <tr>
      <td data-label="Function / class"><a href="../../api/reference/review_governance/"><code>review_governance</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_governance/">data_governance</a></td>
      <td data-label="Purpose">Display governance review widget and capture decisions.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../api/reference/write_governance/"><code>write_governance</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_governance/">data_governance</a></td>
      <td data-label="Purpose">Persist approved governance rows to metadata table.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../api/reference/write_metadata_rows/"><code>write_metadata_rows</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_product_metadata/">data_product_metadata</a></td>
      <td data-label="Purpose">Write agreement-level metadata rows to a metadata table.</td>
    </tr>
  </tbody>
</table>

## Segment 5: Provide read-only context for 02_ex and 03_pc notebooks

Downstream notebooks load approved governance context as read-only input and should not redefine agreement truth locally.

<table class="reference-function-table notebook-structure-function-table">
  <tbody>
    <tr>
      <td data-label="Function / class"><a href="../../api/reference/load_governance/"><code>load_governance</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/data_governance/">data_governance</a></td>
      <td data-label="Purpose">Load approved governance metadata as read-only context.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../api/reference/step-02a-shared-runtime-config/get_path/"><code>get_path</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/config/">config</a></td>
      <td data-label="Purpose">Resolve configured metadata paths for runtime reads and writes.</td>
    </tr>
  </tbody>
</table>
