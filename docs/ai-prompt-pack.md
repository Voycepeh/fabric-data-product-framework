# AI Prompt Pack (Reusable Templates)

> All AI suggestions are advisory only and must be reviewed and approved by humans before use.

## 1) EDA summary generation
**Template:**
"Summarize exploratory findings for dataset `{dataset_id}` using the profile metrics below. Highlight anomalies, possible root causes, and open questions. Keep recommendations practical and note confidence levels.\n\nProfile context:\n{profile_context}" 

## 2) Data quality rule suggestion
**Template:**
"Given dataset purpose `{dataset_purpose}` and column profile metrics `{column_profiles}`, propose candidate data quality rules with severity (`info`, `warning`, `error`) and rationale. Return as a review-ready table." 

## 3) Governance label suggestion
**Template:**
"Suggest governance labels for dataset `{dataset_id}` and columns `{column_list}` based on these notes `{domain_notes}`. Include a short reason for each label and mark uncertain labels for human review." 

## 4) Transformation explanation
**Template:**
"Explain this transformation pipeline in plain language for maintainers and downstream analysts.\n\nTransformation steps:\n{transformation_steps}\n\nInclude assumptions, risks, and validation checks." 

## 5) Data contract drafting
**Template:**
"Draft a data contract section for dataset `{dataset_id}` including expected freshness, schema expectations, key constraints, nullability assumptions, and downstream commitments. Use this context: `{contract_context}`." 

## 6) Incremental refresh safety review
**Template:**
"Review this incremental refresh plan for safety issues.\n\nWatermark: `{watermark_column}`\nPartition column: `{partition_column}`\nLast successful max watermark: `{last_max}`\nCurrent observed max watermark: `{current_max}`\nPolicy: `{incremental_policy}`\n\nIdentify rollback risks, gap/overlap risks, and checks to run before write." 

## 7) Run summary drafting
**Template:**
"Draft a concise run summary for run `{run_id}` using these inputs: status `{status}`, quality results `{dq_results}`, drift results `{drift_results}`, lineage notes `{lineage_notes}`, and exceptions `{exceptions}`. Include explicit human approval checkpoints." 

## Human review checklist

Before accepting AI-generated text:
- Verify technical correctness against notebook outputs.
- Confirm governance labels match policy.
- Remove speculative claims without evidence.
- Ensure no sensitive or real organizational identifiers are included.
- Record approver name/role in run notes.
