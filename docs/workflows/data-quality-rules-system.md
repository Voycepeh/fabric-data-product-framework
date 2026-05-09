# Data Quality Rules System

## Purpose

Use this page as a practical guide for moving from candidate DQ ideas to approved, enforced checks in FabricOps.

For architecture context, see [Data quality architecture](../architecture/data-quality-architecture.md).

## The 5 step flow

1. **Profile source data in `02_ex`.**
2. **Use AI to suggest candidate rules** from profiling and business context.
3. **Human reviews and approves/edits/rejects** candidates before promotion.
4. **Store approved rules** in configuration or metadata tables.
5. **`03_pc` enforces approved rules** and writes DQ results plus quarantine evidence.

## Supported rule types

| Rule type | Purpose | Required extra fields |
|---|---|---|
| `not_null` | Check selected columns are not null. | None |
| `unique_key` | Check selected column combination is unique. | None |
| `accepted_values` | Check one column is in allowed values. | `allowed_values` |
| `value_range` | Check one column is within bounds. | `min_value`, `max_value` |
| `regex_format` | Check one string column against a regex pattern. | `regex_pattern` |
| `accepted_values_ref` | Check one column against values in a reference table column. | `reference_table`, `reference_column` |
| `string_length_between` | Check one string column length is within bounds. | `min_length`, `max_length` |

## Minimal notebook usage

```python
# 02_ex: AI suggestion only
prompt = suggest_dq_rules_prompt(df_profile, "CUSTOMERS", business_context="Customer master quality checks")
```

```python
# 03_pc: approved enforcement only
result = run_dq_rules(df_customers, "CUSTOMERS", DQ_RULES["CUSTOMERS"], fail_on_error=False)
lakehouse_table_write(result, dq_results_path, "DQ_RESULTS", mode="append")
assert_dq_passed(result)
```

## Quarantine pattern

- Evaluate approved rules on the pipeline input DataFrame.
- Split pass/fail rows using deterministic rule outcomes.
- Write pass rows to curated output.
- Write fail rows to quarantine with rule id/type/severity and run timestamp.

## Related pages

- [Data quality architecture](../architecture/data-quality-architecture.md)
- [Contract model](../metadata-and-contracts/contract-model.md)
- [Notebook Structure](../notebook-structure.md)
