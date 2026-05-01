# Local-safe smoke recipe

## Purpose
Quick local smoke test of profiling, quality checks, governance classification input shaping, drift checks, and lineage record generation without Fabric-only dependencies.

## When to use it
- First-time repo validation.
- CI-style sanity checks.
- Teaching the framework workflow with small in-memory pandas data.

## Required inputs
- Python environment with project dependencies.
- A small pandas DataFrame.
- A minimal quality rule list.

## Copy-paste code
```python
import pandas as pd
from fabric_data_product_framework.profiling import profile_dataframe, summarize_profile
from fabric_data_product_framework.quality import run_quality_rules
from fabric_data_product_framework.governance_classifier import classify_columns
from fabric_data_product_framework.drift_checkers import check_profile_drift, summarize_drift_results
from fabric_data_product_framework.lineage import build_lineage_records, generate_mermaid_lineage

source_df = pd.DataFrame(
    [
        {"order_id": 1, "customer_email": "a@example.com", "amount": 10.5},
        {"order_id": 2, "customer_email": "b@example.com", "amount": 11.0},
    ]
)

profile = profile_dataframe(source_df, dataset_name="orders_local", engine="pandas")
print(summarize_profile(profile))

rules = [
    {"rule_id": "not_null_order_id", "rule_type": "not_null", "column": "order_id", "severity": "critical"},
    {"rule_id": "amount_non_negative", "rule_type": "range_check", "column": "amount", "min_value": 0, "severity": "warning"},
]
quality_result = run_quality_rules(source_df, rules, dataset_name="orders_local", table_name="local.orders", engine="pandas")

classifications = classify_columns(
    profile=profile,
    dataset_name="orders_local",
    table_name="local.orders",
)

profile_drift = check_profile_drift(current_profile=profile, baseline_profile=profile)
drift_summary = summarize_drift_results(profile_drift_result=profile_drift)

lineage_records = build_lineage_records(
    dataset_name="orders_local",
    run_id="local-smoke-001",
    source_tables=["local.orders_raw"],
    target_table="local.orders",
    transformation_steps=[
        {"step_id": "1", "step_name": "ingest", "input_name": "orders_raw", "output_name": "orders_local", "transformation_type": "ingest"},
        {"step_id": "2", "step_name": "quality", "input_name": "orders_local", "output_name": "quality_result", "transformation_type": "quality"},
    ],
)
mermaid = generate_mermaid_lineage(
    source_tables=["local.orders_raw"],
    target_table="local.orders",
    transformation_steps=[
        {"step_id": "1", "step_name": "ingest"},
        {"step_id": "2", "step_name": "quality"},
    ],
)

print(quality_result["status"])
print(classifications)
print(drift_summary)
print(mermaid)
```

## Expected output
- Profile dictionary plus human-readable profile summary.
- Quality status (`passed`/`failed`) and per-rule outcomes.
- Governance classification suggestions.
- Profile drift summary dictionary.
- Lineage records and Mermaid diagram text.

## Common failures
- Import errors: ensure `PYTHONPATH=src`.
- Rule payload errors: each rule must include valid `rule_type` keys supported by `run_quality_rules`.
- Governance input mismatch: pass `profile=...` (not raw column list).

## Related function groups
See [src/README.md](../../src/README.md) sections: Profiling, Data quality workflow, Governance classification, Drift checks and snapshots, and Lineage and transformation summaries.
