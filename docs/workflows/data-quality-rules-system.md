# Data quality rules system

FabricOps Starter Kit supports a lightweight, config-driven data quality (DQ) pattern:

1. **Store approved rules in config** (for example, `DQ_RULES` in `00_env_config`).
2. **Use AI to suggest candidate rules** from profile metadata.
3. **Human review and approval** required before any enforcement.
4. **Pipeline contract notebook enforces approved rules** with `run_dq_rules`.
5. **Persist results** via the generic `lakehouse_table_write` pattern.

## Supported rule types

| Rule type | Purpose | Required extra fields |
|---|---|---|
| `not_null` | Check selected columns are not null. | None |
| `unique_key` | Check selected column combination is unique. | None |
| `accepted_values` | Check one column is in allowed values. | `allowed_values` |
| `value_range` | Check one column is between min and max values. | `min_value`, `max_value` |
| `regex_format` | Check one string column matches regex. | `regex_pattern` |
| `row_count_between` | Check table row count is in bounds. | `min_rows`, `max_rows` |
| `schema_required_columns` | Check expected columns exist. | None |
| `schema_data_type` | Check selected columns match expected types. | `expected_types` |

## Template usage snippets

```python
# 00_env_config
DQ_RULES = get_default_dq_rule_templates()
```

```python
# pipeline contract notebook
# candidate-only AI suggestions must be reviewed before being copied into DQ_RULES
prompt = suggest_dq_rules_prompt(df_profile, "EMAIL_LOGS", business_context="Describe what this table is used for.")

# enforce approved rules with fail-after-logging
result = run_dq_rules(df_message_log, "EMAIL_LOGS", DQ_RULES["EMAIL_LOGS"], fail_on_error=False)
dq_results_path = get_path(ENV_NAME, "metadata", config=CONFIG)
write_dq_results(result, dq_results_path, table_name="DQ_RESULTS")
assert_dq_passed(result)
```


## Editable AI prompt template

Set `DQ_RULE_SUGGESTION_PROMPT_TEMPLATE` in `templates/notebooks/00_config.py` to customize how AI suggests rule candidates without changing package code.

```python
prompt = suggest_dq_rules_prompt(
    df_profile,
    "EMAIL_LOGS",
    business_context="Outbound email monitoring",
    prompt_template=DQ_RULE_SUGGESTION_PROMPT_TEMPLATE,
)
```
