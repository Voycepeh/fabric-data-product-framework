# Local-safe smoke recipe

## Purpose
Quick local smoke test of profiling, DQ, contract validation, drift, and lineage without Fabric-only dependencies.

## When to use it
- First-time repo validation.
- CI-style sanity checks.
- Teaching the framework workflow with small in-memory data.

## Required inputs
- Python environment with project dependencies.
- A small pandas DataFrame.
- Optional: lightweight DQ rules list.

## Copy-paste code
```python
import pandas as pd
from fabric_data_product_framework.profiling import run_profile_workflow
from fabric_data_product_framework.dq import run_dq_workflow
from fabric_data_product_framework.governance import classify_columns
from fabric_data_product_framework.drift_checkers import check_schema_drift, check_profile_drift, summarize_drift_results
from fabric_data_product_framework.lineage import build_lineage_records, generate_mermaid_lineage

source_df = pd.DataFrame(
    [
        {"order_id": 1, "customer_email": "a@example.com", "amount": 10.5},
        {"order_id": 2, "customer_email": "b@example.com", "amount": 11.0},
    ]
)

profile_result = run_profile_workflow(df=source_df)

rules = [
    {"rule_id": "not_null_order_id", "column": "order_id", "expectation": "not_null"},
    {"rule_id": "non_negative_amount", "column": "amount", "expectation": "ge", "value": 0},
]
dq_result = run_dq_workflow(df=source_df, dq_rules=rules)

governance = classify_columns(columns=list(source_df.columns))

schema_drift = check_schema_drift(
    current_columns=list(source_df.columns),
    previous_columns=["order_id", "customer_email", "amount"],
)
profile_drift = check_profile_drift(current_profile=profile_result, previous_profile=profile_result)
print(summarize_drift_results([schema_drift, profile_drift]))

lineage_records = build_lineage_records([
    {"step": "read source", "input": "local_df", "output": "source_df"},
    {"step": "dq", "input": "source_df", "output": "dq_result"},
])
print(generate_mermaid_lineage(lineage_records))
print(dq_result)
print(governance)
```

## Expected output
- Profile metadata object is returned.
- DQ summary with pass/fail counts.
- Governance classification suggestions for each column.
- Drift summary showing no unexpected change for the baseline.
- Mermaid lineage text output.

## Common failures
- Import errors: install project dependencies and ensure `PYTHONPATH=src`.
- Rule schema mismatch: normalize rules with `normalize_dq_rules` if needed.
- Empty drift baseline: provide previous snapshots/structures.

## Related function groups
See [src/README.md](../../src/README.md) sections: Data quality, Governance classification, Drift checks, and Lineage.
