# Profile to DQ to governance to lineage to handover

## Purpose

Use this recipe for a full metadata-first execution path that produces
handover-ready artifacts.

## Required inputs

- Spark session `spark`.
- Spark DataFrame `transformed_df`.
- Quality contract dictionary.
- Optional baseline profile for drift checks.

## Example

```python
from fabric_data_product_framework.quality import run_dq_workflow
from fabric_data_product_framework.drift import (
    check_profile_drift,
    summarize_drift_results,
)
from fabric_data_product_framework.governance import (
    build_governance_classification_records,
    classify_columns,
)
from fabric_data_product_framework.lineage import (
    build_lineage_records,
    build_transformation_summary_markdown,
    generate_mermaid_lineage,
)
from fabric_data_product_framework.profiling import profile_dataframe

dataset_name = "sales_orders"
table_name = "silver_sales_orders"
run_id = "fabric-run-001"

profile = profile_dataframe(
    transformed_df,
    dataset_name=dataset_name,
    engine="spark",
)

dq_result = run_dq_workflow(
    spark,
    transformed_df,
    quality_contract,
    dataset_name=dataset_name,
    table_name=table_name,
)

classifications = classify_columns(
    profile=profile,
    dataset_name=dataset_name,
    table_name=table_name,
    run_id=run_id,
)

governance_records = build_governance_classification_records(
    classifications,
    dataset_name=dataset_name,
    table_name=table_name,
    run_id=run_id,
)

profile_drift = check_profile_drift(
    current_profile=profile,
    baseline_profile=baseline_profile,
)

drift_summary = summarize_drift_results(
    profile_drift_result=profile_drift,
)

steps = [
    {
        "step_id": "1",
        "step_name": "ingest",
        "input_name": "bronze_sales_orders",
        "output_name": "transformed_df",
        "transformation_type": "transform",
        "description": "Normalize and enrich orders",
    },
    {
        "step_id": "2",
        "step_name": "quality",
        "input_name": "transformed_df",
        "output_name": "dq_result",
        "transformation_type": "quality",
        "description": "Apply quality contract rules",
    },
]

lineage_records = build_lineage_records(
    dataset_name=dataset_name,
    run_id=run_id,
    source_tables=["bronze_sales_orders"],
    target_table=table_name,
    transformation_steps=steps,
)

lineage_mermaid = generate_mermaid_lineage(
    source_tables=["bronze_sales_orders"],
    target_table=table_name,
    transformation_steps=steps,
)

summary = {
    "dataset_name": dataset_name,
    "run_id": run_id,
    "source_tables": ["bronze_sales_orders"],
    "target_table": table_name,
    "step_count": len(steps),
    "steps": steps,
    "columns_used": ["order_id", "customer_id", "amount"],
    "columns_created": ["order_total", "dq_status"],
}

summary_md = build_transformation_summary_markdown(summary)

artifacts = {
    "profile": profile,
    "dq": dq_result,
    "governance": governance_records,
    "drift": drift_summary,
    "lineage_records": lineage_records,
    "lineage_mermaid": lineage_mermaid,
    "transformation_summary_markdown": summary_md,
}

print(artifacts)
```

## Expected output

- Profile output for transformed data.
- DQ workflow results and status.
- Governance records and drift summary.
- Lineage records and Mermaid lineage text.
- Markdown transformation summary.

## Common failures

- Spark session missing.
- Invalid or incomplete quality contract.
- Missing baseline profile when drift comparison is enabled.
