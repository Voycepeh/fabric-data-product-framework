# Run actual-data MVP in Fabric

## 1) Purpose
Use one contract + one transform function to run the full framework flow on a real Fabric table.

- Notebook template: `examples/fabric_actual_data_mvp/actual_data_mvp_template.py`
- Contract example: `contracts/examples/actual_data_mvp_contract.yml`

## 2) Prerequisites
- Fabric Spark notebook environment.
- Framework package available in your notebook runtime.
- Existing source and target tables you are allowed to use.

## 3) What you must edit
- Contract path, source table, target table.
- Key column, watermark column, partition column.
- Dataset/business metadata fields (owner, approved usage, agreement id).
- `transform(df, ctx)` business logic.

## 4) What the framework does automatically
- Contract normalization and validation.
- Source/output profiling and metadata writes.
- DQ workflow (contract rules, optional candidate generation, quality gate).
- Drift checks (schema, partition/data, profile where configured).
- Governance classification suggestions.
- Quarantine split/summary.
- Runtime contract checks, lineage records, run summary, and gated target write.

## 5) How to run in Fabric
1. Open/copy `examples/fabric_actual_data_mvp/actual_data_mvp_template.py` into a Fabric notebook.
2. Update the contract placeholders.
3. Implement your dataset-specific logic inside `transform`.
4. Run all cells.

## 6) How to interpret result sections
- `status` / `written`: overall gate result and final write outcome.
- `run_summary`: high-level run metadata and gate rollup.
- `dq_workflow`: DQ rule generation, loaded rules, quality result, and gate result.
- `drift.summary`: schema/data drift rollup.
- `governance.summary`: column classification suggestion rollup.
- `quarantine`: quarantine status, row count, and write status.

## 7) Common first-run behavior
- Drift checks can report `no_baseline`; first run should not fail solely due to missing baseline snapshots.
- DQ candidate generation produces reviewable suggestions; they are not auto-approved blocking rules.
- Governance classification outputs reviewable suggestions and does not apply Purview labels.

## 8) Troubleshooting
- If target is not written, inspect gate sections in `result` and quality severity thresholds.
- Validate contract table names/columns match the source table schema.
- Freeze/skip exploratory preview cells before production scheduling.
- Keep `fw.assert_data_product_passed(result)` so failed gates fail scheduled pipelines.
- Final target writes only happen when blocking gates pass.
