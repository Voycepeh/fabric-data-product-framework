# DQ Workflow API Reference

## Module purpose
`fabric_data_product_framework.dq` handles candidate generation, rule normalization/storage, and orchestration around rule execution.

## Core public callables
- `generate_dq_rule_candidates(profile, metadata=None, business_context=None, dataset_name=None, table_name=None)`
- `normalize_dq_rule(rule)` / `normalize_dq_rules(rules)`
- `run_dq_rules(df, rules, dataset_name, table_name, engine="spark", fail_on="critical")`
- `run_dq_workflow(spark, df, quality_contract, dataset_name, table_name, run_id=None, profile=None, metadata=None, business_context=None, engine="spark")`

## Typical chaining
1. create or load candidate/approved rules.
2. normalize and persist rules.
3. execute with `run_dq_rules` or full `run_dq_workflow`.
4. feed outputs into run-summary and metadata tables.
