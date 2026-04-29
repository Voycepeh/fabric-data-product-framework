# Fabric MVP notebook walkthrough (synthetic)

This walkthrough shows how to test the MVP template safely with synthetic settings.

## 1) Create a synthetic dataset contract

Create a contract YAML with synthetic dataset metadata and expected schema. Keep names public-safe and generic.

## 2) Configure notebook parameters

In the template, set:
- `DATASET_CONTRACT_PATH`
- `NOTEBOOK_NAME`
- `WORKSPACE`, `LAKEHOUSE`, `SOURCE_TABLE`, `TARGET_TABLE`
- `ENVIRONMENT`, `DRY_RUN`, `PROFILE_ONLY`

## 3) Run source profiling

Run the notebook through source read, schema snapshot, and profile generation. Confirm row counts and inferred semantic types look reasonable.

## 4) Run transformation

Implement your logic inside:
- `# USER TRANSFORMATION START`
- `# USER TRANSFORMATION END`

For first-run testing, keep `df_output = df_source`.

## 5) Add technical columns

The template applies:
- `add_pipeline_run_id`
- `add_loaded_at`

You can extend this later with extra technical columns when needed.

## 6) Write output

Switch off `DRY_RUN` and confirm `fabric_table_writer` writes to your target table identifier.

## 7) Write metadata logs

Wire `metadata_writer` and confirm metadata outputs append to mapped metadata tables:
- dataset runs
- column profiles
- schema snapshots
- schema drift results

## 8) Review run summary

Review the printed run summary for:
- `run_id`
- dataset name
- source/output row counts
- mode flags

This gives a lightweight handover-friendly checkpoint before expanding to incremental or quality-rule stages.
