# Quality API Reference

## Module purpose
`fabric_data_product_framework.quality` executes normalized DQ rules and returns enforceable pass/fail gate outcomes.

## Core public callables
- `run_quality_rules(df, rules, dataset_name="unknown", table_name="unknown", engine="auto")`
- `assert_quality_gate(result, fail_on="critical")`
- `build_quality_result_records(result, run_id=...)`

## Typical chaining
1. compile/load approved rules.
2. run `run_quality_rules`.
3. call `assert_quality_gate` before output writes.
4. persist records with `build_quality_result_records`.
