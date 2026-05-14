# `02_ex_<agreement>_<topic>`

Exploration and proposal notebook for analyst/data scientist-led investigation of source data before governance approval and production enforcement.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/02_ex_agreement_topic.ipynb">Open template notebook</a>

## Purpose

`02_ex` is where analysts and data scientists perform agreement-aware exploration before production enforcement.

`02_ex` starts from `00_env_config` and should reuse shared configuration/runtime validation instead of redefining notebook setup.

`02_ex` first explores existing metadata context (approved DQ state, governance/classification context, and prior notebook evidence), then explores the dataset itself.

`02_ex` captures findings in markdown and uses the DQ widget flow to suggest, review, approve, and deactivate DQ rules.

`02_ex` should not manually define final DQ rules in the findings section.

## Ownership

- Primary owner: Analyst / Data Scientist
- Typical collaborators: Data steward, governance owner, data engineer

## Naming convention

- Notebook pattern: `02_ex_<agreement>_<topic>`
- `<agreement>` maps to the governance agreement notebook (`01_data_sharing_agreement_<agreement>`)
- `<topic>` describes the exploration question/domain focus

## What belongs in `02_ex`

- Agreement selection and agreement context
- Source data profiling and discovery
- Source quirk investigation and analyst observations
- Exploratory analysis
- Exploratory transform ideas (investigation only)
- AI-assisted DQ candidate drafting (advisory)
- DQ widget-based analyst/engineer review and approval
- Read-only metadata exploration
- Read-only review of approved DQ rules, governance/classification metadata, and notebook registry/prior evidence
- Findings and handoff notes

## What does not belong in `02_ex`

- Governance approval authority
- Production enforcement
- Final deterministic production transformation contract
- Manual final DQ rule writing outside the DQ widget flow
- Scheduled, run-all-safe behavior

`02_ex` does **not** approve governance controls and does **not** enforce approved DQ rules in production. Governance covers usage, ownership, sensitivity/classification, and restrictions; DQ rule approval is owned by analysts/engineers through the review flow.

## Recommended notebook flow

1. **Introduction and scope**
   - Set `agreement_id`, `topic`, and `table_name`.
   - These are the only required top-level placeholders.
2. **Agreement context**
   - Explain that the notebook operates within a selected data agreement.
   - Approved usage, ownership, and business context come from the agreement metadata where available.
3. **Configuration and imports**
   - Run `%run 00_env_config` in its own standalone cell.
   - Import all helper functions used below in one setup cell.
   - Resolve `metadata_path` using `get_path(ENV_NAME, "metadata", config=FABRIC_CONFIG)`.
   - Resolve DQ metadata table using `FABRIC_CONFIG.review_workflow_config.dq_approved_table`.
   - Do not call `setup_fabricops_notebook` again inside `02_ex`.
4. **Metadata exploration**
   - Select agreement using the agreement helper/widget flow.
   - Register the current notebook against the selected agreement.
   - Read existing approved DQ rules as read-only context.
   - Read governance/classification metadata as read-only context.
   - Read notebook registry/prior evidence as read-only context.
   - This section should not profile source data and should not write DQ rules.
5. **Dataset exploration**
   - Choose one source-loading pattern.
   - Load from lakehouse table, warehouse table, CSV, or parquet using existing helper functions.
   - Display schema and sample records.
   - Run `profile_dataframe`.
   - Add focused exploratory checks in an empty analyst code block.
   - Keep exploratory transform logic here only as investigation; final repeatable logic belongs in `03_pc`.
6. **Findings**
   - Record findings in markdown, not structured proposal rows.
   - Use small subtitles:
     - Key findings
     - Source quirks
     - Business context notes
     - Classification / sensitivity notes
     - Suggested pipeline transform notes
     - Open questions
     - Handoff notes
   - Do not create `proposal_rows`.
   - Do not create `proposal_df`.
   - Do not manually define final DQ rules here.
   - Handoff notes should say:
     - Approved DQ rules from section 07 are consumed by `03_pc`.
     - Governance/classification updates follow the data agreement workflow.
     - Production transformations and deterministic enforcement belong in `03_pc`.
7. **AI-assisted DQ flow**
   - Load existing approved/active DQ rules.
   - Generate AI candidate rules when needed using `draft_dq_rules`.
   - Review/edit/approve/reject candidates using `run_dq_rule_review_widget`.
   - Collect widget results using `get_dq_rule_review_results`.
   - Persist only approved rules using `write_dq_rules`.
   - Review existing active rules for deactivation using `review_dq_rule_deactivations`.
   - Persist deactivation metadata using `build_dq_rule_deactivation_metadata_df`.
   - Do not write AI candidate rules directly to metadata.

**Principle:** “`02_ex` is exploratory and analyst-driven; deterministic production logic and enforcement belong in `03_pc`.”

## AI boundary

- AI suggestions are advisory until reviewed.
- DQ approval is analyst/engineer-owned through the DQ widget flow.
- Governance/classification approval follows the data agreement workflow.
- `03_pc` enforces active approved DQ metadata only.

## Handoff boundaries

- DQ rules approved through the section 07 widget flow are consumed by `03_pc`.
- Governance/classification changes identified during exploration should follow the data agreement workflow.
- Production transformations and deterministic enforcement belong in `03_pc`.
- `02_ex` should remain exploratory and analyst-driven.

## Examples

- Select an agreement, inspect existing DQ/governance context, then profile a source table.
- Use profile evidence and business context to draft DQ candidates, review them in the DQ widget, and persist only approved rules.
- Record source quirks and suggested transform notes in the Findings section.
- Identify classification/sensitivity observations for the data agreement workflow.

## Cross-links

- [Canonical notebook structure](../notebook-structure.md)
- [01 data sharing agreement role](../notebook-structure.md#notebook-roles-and-responsibilities)
- [03 pipeline contract notebook](03-pipeline-contract.md)
- [Data quality rules system](../data-quality-rules-system.md)
- [Metadata and contracts](../metadata-and-contracts.md)
