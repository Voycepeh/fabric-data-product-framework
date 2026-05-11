# AI-Assisted Data Quality

## Purpose

FabricOps uses metadata-managed DQ rules where AI assists with suggestions, humans approve, metadata stores decisions, and deterministic pipelines enforce approved active rules.

## End-to-end flow

| Stage | Notebook | What happens |
|---|---|---|
| 1. Profile | `02_ex` | Profile source data with `profile_for_dq` |
| 2. Suggest | `02_ex` | Generate advisory candidates with `suggest_dq_rules` using `CONFIG.ai_prompt_config.dq_rule_candidate_template` |
| 3. Review | Human + `02_ex` | Extract/review candidates with `extract_dq_rules` and `review_dq_rules` |
| 4. Approve + store | `02_ex` | Append approved rules to metadata with `build_dq_rule_history` |
| 5. Enforce | `03_pc` | Load approved active rules with `load_active_dq_rules`, run `run_dq_rules` |
| 6. Quarantine evidence | `03_pc` | Split with `split_dq_rows` into valid rows, quarantine rows, and failure evidence |
| 7. Fail/continue | `03_pc` | Call `assert_dq_passed` after evidence is produced |

## Exploration-side workflow (`02_ex`)

```python
profile_rows = profile_for_dq(df_source, table_name=TARGET_TABLE)
responses = suggest_dq_rules(
    profile_rows,
    prompt_template=CONFIG.ai_prompt_config.dq_rule_candidate_template,
    output_col="ai_response",
)
candidate_rules = extract_dq_rules(responses, table_name=TARGET_TABLE)
review_dq_rules(candidate_rules, table_name=TARGET_TABLE)
approved = [r for r in candidate_rules if r.get("approval_status") == "approved"]
approved_history = build_dq_rule_history(
    spark=spark,
    table_name=TARGET_TABLE,
    approved_rules=approved,
    action_by="notebook_user",
)
```

AI output remains advisory. Human approval is required before rules enter active metadata.

## Pipeline-side workflow (`03_pc`)

```python
rules = load_active_dq_rules(spark.table("METADATA_DQ_RULES"), table_name=TARGET_TABLE)
dq_result = run_dq_rules(df_standard, table_name=TARGET_TABLE, rules=rules, fail_on_error=False)

df_valid, df_quarantine, dq_failure_evidence = split_dq_rows(df_standard, rules, dq_run_id=RUN_ID)

# Evidence first, then fail when required.
assert_dq_passed(dq_result)
```

Quarantine is an evidence stream: one quarantined source row can map to multiple failure-evidence rows via IDs when multiple rules fail. Most true fixes happen upstream/source-side.
