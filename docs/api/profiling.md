# Profiling API Reference

## Module purpose
`fabric_data_product_framework.profiling` produces JSON-safe table and column profiles for pandas and Spark.

## Core public callables
- `profile_dataframe(df, dataset_name="unknown", sample_size=5, top_n=5, engine="auto")`
- `profile_column(series, sample_size=5, top_n=5)`
- `flatten_profile_for_metadata(profile, table_name, run_id, table_stage, exclude_columns=None)`
- `summarize_profile(profile)`

## Typical chaining
1. `profile_dataframe` on source data.
2. `flatten_profile_for_metadata` for metadata writes.
3. use profile for DQ candidate generation and governance classification.
