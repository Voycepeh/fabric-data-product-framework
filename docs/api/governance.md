# Governance API Reference

## Module purpose
`fabric_data_product_framework.governance_classifier` provides deterministic, review-first column classification suggestions.

## Core public callables
- `classify_column(column_name, data_type=None, profile=None, metadata=None, business_context=None, rules=None)`
- `classify_columns(profile, metadata=None, business_context=None, rules=None, dataset_name=None, table_name=None, run_id=None)`
- `write_governance_classifications(...)`
- `summarize_governance_classifications(classifications)`

## Typical chaining
1. run profiling.
2. classify columns with `classify_columns`.
3. persist review records.
4. include summary in run handover.
