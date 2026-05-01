# Full metadata chaining recipe

## Purpose
Chain profiling, contract-driven DQ workflow, governance, drift summaries, and lineage records to produce handover-ready artifacts.

## When to use it
- End-to-end MVP run demos.
- Metadata artifact generation for operations handover.
- Validating notebook lifecycle outputs in one execution path.

## Required inputs
- Spark DataFrame `transformed_df`.
- Spark session `spark`.
- Quality contract object/dict.
- Baseline profile dictionary for drift comparison.

## Copy-paste code
```python
from fabric_data_product_framework.profiling import profile_dataframe
from fabric_data_product_framework.dq import run_dq_workflow
from fabric_data_product_framework.governance_classifier import classify_columns, build_governance_classification_records
from fabric_data_product_framework.drift_checkers import check_profile_drift, summarize_drift_results
from fabric_data_product_framework.lineage import build_lineage_records, generate_mermaid_lineage, build_transformation_summary_markdown

dataset_name = "sales_orders"
table_name = "silver_sales_orders"
run_id = "fabric-run-001"

profile = profile_dataframe(transformed_df, dataset_name=dataset_name, engine="spark")

dq_result = run_dq_workflow(
    spark,
    transformed_df,
    quality_contract,
    dataset_name=dataset_name,
    table_name=table_name,
    run_id=run_id
)

classifications = classify_columns(profile=profile, dataset_name=dataset_name, table_name=table_name, run_id=run_id)
governance_records = build_governance_classification_records(
    classifications,
    dataset_name=dataset_name,
    table_name=table_name,
    run_id=run_id,
)

profile_drift = check_profile_drift(current_profile=profile, baseline_profile=baseline_profile)
drift_summary = summarize_drift_results(profile_drift_result=profile_drift)

steps = [
    {"step_id": "1", "step_name": "ingest", "input_name": "bronze_sales_orders", "output_name": "transformed_df", "transformation_type": "transform", "description": "Normalize and enrich orders"},
    {"step_id": "2", "step_name": "quality", "input_name": "transformed_df", "output_name": "dq_result", "transformation_type": "quality", "description": "Apply quality contract rules"},
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
- DQ workflow result with gate status and per-rule records.
- Governance records and profile drift summary.
- Lineage records plus Mermaid and markdown transformation summary artifacts.

## Common failures
- Missing `spark` session for DQ workflow.
- `quality_contract` omitted required rule details.
- `baseline_profile` not available for drift comparison.

## Related function groups
See [src/README.md](../../src/README.md) sections: Profiling, Data quality workflow, Governance classification, Drift checks and snapshots, and Lineage and transformation summaries.
