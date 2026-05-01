# Full metadata chaining recipe

## Purpose
Chain profiling, DQ, governance, drift checks, and lineage outputs so one run produces reusable handover-ready metadata artifacts.

## When to use it
- End-to-end MVP runs.
- Preparing artifacts for operations handover.
- Demonstrating full framework value in a single notebook.

## Required inputs
- Source DataFrame (or Spark DataFrame) and target transformation DataFrame.
- DQ rule candidates/approved rules.
- Prior snapshot/profile baseline for drift comparisons.

## Copy-paste code
```python
from fabric_data_product_framework.profiling import run_profile_workflow
from fabric_data_product_framework.dq import run_dq_workflow
from fabric_data_product_framework.governance import classify_columns, build_governance_classification_records
from fabric_data_product_framework.drift_checkers import check_schema_drift, check_profile_drift, summarize_drift_results
from fabric_data_product_framework.lineage import (
    build_lineage_records,
    generate_mermaid_lineage,
    build_transformation_summary_markdown,
)

profile = run_profile_workflow(df=transformed_df)
dq = run_dq_workflow(df=transformed_df, dq_rules=approved_rules)

classifications = classify_columns(columns=transformed_df.columns)
governance_records = build_governance_classification_records(classifications)

schema_drift = check_schema_drift(
    current_columns=list(transformed_df.columns),
    previous_columns=baseline_columns,
)
profile_drift = check_profile_drift(current_profile=profile, previous_profile=baseline_profile)
drift_summary = summarize_drift_results([schema_drift, profile_drift])

lineage_steps = [
    {"step": "source ingest", "input": "source_df", "output": "bronze_df"},
    {"step": "transform", "input": "bronze_df", "output": "transformed_df"},
    {"step": "quality", "input": "transformed_df", "output": "dq_result"},
]
lineage_records = build_lineage_records(lineage_steps)
lineage_mermaid = generate_mermaid_lineage(lineage_records)
summary_md = build_transformation_summary_markdown(lineage_steps)

artifacts = {
    "profile": profile,
    "dq": dq,
    "governance": governance_records,
    "drift": drift_summary,
    "lineage_mermaid": lineage_mermaid,
    "transformation_summary_markdown": summary_md,
}
print(artifacts)
```

## Expected output
- Unified artifact dictionary for profile, DQ, governance, drift, and lineage.
- Markdown summary and Mermaid lineage ready for handover docs.
- Reusable metadata outputs for subsequent contract baselines.

## Common failures
- Missing baseline profile/columns for drift checks.
- Unapproved or malformed DQ rules.
- Step records missing fields required for lineage build.

## Related function groups
See [src/README.md](../../src/README.md) sections: Profiling, Data quality, Governance classification, Drift checks and snapshots, and Lineage.
