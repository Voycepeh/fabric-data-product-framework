# Fabric Manual Validation Guide

This guide captures the tested MVP manual flow for Microsoft Fabric using only synthetic data.

## 1) Upload and unpack framework package

1. Build/export the framework zip locally.
2. Upload the zip into Lakehouse **Files**.
3. In a Fabric notebook cell:

```python
import os
import sys
import zipfile

zip_path = "/lakehouse/default/Files/fabricops-kit.zip"
package_dir = "/lakehouse/default/Files/fabricops-kit"

os.makedirs(package_dir, exist_ok=True)
with zipfile.ZipFile(zip_path, "r") as zf:
    zf.extractall(package_dir)

sys.path.append(package_dir)
```

## 2) Import recommended modules

```python
import fabricops_kit.profiling as profiling
import fabricops_kit.technical_columns as tech
import fabricops_kit.runtime as runtime
```

## 3) Create synthetic Spark input dataframe

```python
run_id = "fabric-manual-test-001"

df_source = spark.createDataFrame(
    [
        (1, "2026-04-28T10:00:00Z", 100.0),
        (2, "2026-04-28T10:30:00Z", 80.5),
        (3, "2026-04-28T11:00:00Z", 42.0),
    ],
    ["customer_id", "updated_at", "amount"],
)
```

## 4) Profile source and flatten metadata rows

```python
source_profile = profiling.profile_dataframe(
    df_source,
    dataset_name="sample_framework_input",
    engine="spark",
)

# Correct signature:
# flatten_profile_for_metadata(profile, table_name, run_id, table_stage, exclude_columns=None)
source_profile_rows = profiling.flatten_profile_for_metadata(
    source_profile,
    table_name="sample_framework_input",
    run_id=run_id,
    table_stage="source",
)
```

## 5) Add standard technical columns

```python
# Correct signature:
# add_standard_technical_columns(df, run_id=..., business_keys=[...], source_system=..., source_table=..., engine="spark")
df_output = tech.add_standard_technical_columns(
    df_source,
    run_id=run_id,
    business_keys=["customer_id"],
    source_system="manual",
    source_table="sample_framework_input",
    engine="spark",
)
```

## 6) Write Delta output with saveAsTable and read back

```python
output_table = "sample_framework_output"

df_output.write.mode("overwrite").format("delta").saveAsTable(output_table)

df_output_readback = spark.read.table(output_table)
```

## 7) Profile output and flatten metadata rows

```python
output_profile = profiling.profile_dataframe(
    df_output_readback,
    dataset_name="sample_framework_output",
    engine="spark",
)

output_profile_rows = profiling.flatten_profile_for_metadata(
    output_profile,
    table_name="sample_framework_output",
    run_id=run_id,
    table_stage="output",
)
```

## 8) Validate input/output row counts

```python
input_count = df_source.count()
output_count = df_output_readback.count()

assert input_count == output_count, f"Row count mismatch: {input_count} != {output_count}"
```
