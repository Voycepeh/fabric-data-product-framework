# Fabric dry run recipe

## Purpose
Run a Fabric-notebook-native dry run that exercises Lakehouse IO, profiling, DQ, and governance outputs before production writes.

## When to use it
- Validating Environment setup in Microsoft Fabric.
- Confirming path wiring and table naming conventions.
- Dry-running transformations with non-production sample tables.

## Required inputs
- Fabric notebook attached to a Lakehouse.
- Config loaded via `load_fabric_config`.
- Source table name and target dry-run table name.

## Copy-paste code
```python
from fabric_data_product_framework.fabric_notebook import (
    load_fabric_config,
    lakehouse_table_read,
    lakehouse_table_write,
    check_naming_convention,
)
from fabric_data_product_framework.profiling import run_profile_workflow
from fabric_data_product_framework.dq import run_dq_workflow
from fabric_data_product_framework.governance import classify_columns, summarize_governance_classifications

cfg = load_fabric_config()
source_table = "bronze_sales_orders"
target_table = "silver_sales_orders_dry_run"

check_naming_convention(target_table)
df = lakehouse_table_read(source_table, config=cfg)

profile = run_profile_workflow(df=df)
rules = [
    {"rule_id": "not_null_order_id", "column": "order_id", "expectation": "not_null"},
]
dq = run_dq_workflow(df=df, dq_rules=rules)

classifications = classify_columns(columns=df.columns)
classification_summary = summarize_governance_classifications(classifications)

# dry-run write target (change mode/location as needed)
lakehouse_table_write(df, target_table, mode="overwrite", config=cfg)

print(profile)
print(dq)
print(classification_summary)
```

## Expected output
- Source table reads successfully from Lakehouse.
- Profile + DQ results are printed for review.
- Governance classification summary appears.
- Dry-run target table is written to the configured Lakehouse path.

## Common failures
- Lakehouse not attached to notebook session.
- Config path mismatch in `load_fabric_config`.
- Naming policy rejection from `check_naming_convention`.

## Related function groups
See [src/README.md](../../src/README.md) sections: Fabric notebook runtime, Profiling, Data quality, and Governance classification.
