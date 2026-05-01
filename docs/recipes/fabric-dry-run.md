# Fabric dry run recipe

## Purpose
Run a Fabric-native dry run for Lakehouse read/write, profiling, contract-driven DQ workflow, and governance outputs.

## When to use it
- Validating Fabric Environment + Lakehouse path setup.
- Confirming dry-run transformations before production write paths.
- Executing DQ with a Spark session and quality contract.

## Required inputs
- Fabric notebook with active `spark` session.
- Fabric config file (for example `Files/configs/fabric_houses.yml`).
- A source table and dry-run target table.
- A quality contract object/dict.

## Copy-paste code
```python
from fabric_data_product_framework.fabric_notebook import load_fabric_config, get_path, lakehouse_table_read, lakehouse_table_write
from fabric_data_product_framework.profiling import profile_dataframe
from fabric_data_product_framework.dq import run_dq_workflow
from fabric_data_product_framework.governance_classifier import classify_columns, summarize_governance_classifications

cfg = load_fabric_config("Files/configs/fabric_houses.yml")
lh = get_path(env="Sandbox", target="Source", config=cfg)

source_table = "bronze_sales_orders"
target_table = "silver_sales_orders_dry_run"

df = lakehouse_table_read(lh, source_table, spark_session=spark)
profile = profile_dataframe(df, dataset_name="sales_orders", engine="spark")

quality_contract = {
    "rules": [
        {"rule_id": "order_id_not_null", "rule_type": "not_null", "column": "order_id", "severity": "critical"}
    ],
    "use_rule_store": False,
    "generate_candidates": False,
    "fail_on": "critical",
}

dq_result = run_dq_workflow(
    spark,
    df,
    quality_contract,
    dataset_name="sales_orders",
    table_name=source_table,
    profile=profile,
    engine="spark",
)

classifications = classify_columns(profile=profile, dataset_name="sales_orders", table_name=source_table)
summary = summarize_governance_classifications(classifications)

lakehouse_table_write(df, lh, target_table, mode="overwrite")

print(dq_result["status"])
print(summary)
```

## Expected output
- Delta table read succeeds from configured Lakehouse path.
- Profile and contract-driven DQ workflow results are produced.
- Governance classification summary is printed.
- Dry-run target table is written to `lh.root/Tables/<target_table>`.

## Common failures
- Config not found: check the `load_fabric_config(...)` file path.
- Spark session missing: run in Fabric notebook or pass `spark_session` explicitly.
- Invalid quality contract fields or unsupported rule types.

## Related function groups
See [src/README.md](../../src/README.md) sections: Fabric notebook runtime, Profiling, Data quality workflow, and Governance classification.
