# AI-Assisted Data Quality

## Purpose

FabricOps uses an AI-in-the-loop workflow for data quality (DQ):

- AI suggests candidate rules from profiling evidence.
- Humans review and explicitly approve/reject each candidate.
- Metadata records those decisions as governed rule history.
- Pipeline notebooks enforce only approved, active rules deterministically.

![AI-assisted data quality rule flow](assets/DQ-with-ai.png)

## 7-step workflow (exploration to governed enforcement)

| Step | Where | What happens | Output |
|---|---|---|---|
| 1. Profile source data | Exploration notebook (`02_ex`) | `profile_for_dq` computes profile evidence used for rule ideation. | Structured profiling rows |
| 2. Ask AI for candidates | Exploration notebook (`02_ex`) | `suggest_dq_rules` runs the canonical framework prompt to propose advisory rule candidates. | AI response text/JSON |
| 3. Parse AI candidates | Exploration notebook (`02_ex`) | `extract_dq_rules` turns responses into candidate rule records scoped to a table key. | Candidate rule rows |
| 4. Human review and selection | Human + widget in `02_ex` | `review_dq_rules` presents candidates; humans approve the subset worth enforcing. | Approved rule list |
| 5. Persist governed history | Exploration notebook (`02_ex`) | `build_dq_rule_history` appends approval decisions to metadata history. | Metadata rule history |
| 6. Load and enforce active rules | Pipeline notebook (`03_pc`) | `load_active_dq_rules` loads approved active rules; `run_dq_rules` evaluates them deterministically. | DQ evaluation result |
| 7. Produce evidence and gate pipeline | Pipeline notebook (`03_pc`) | `split_dq_rows` writes valid/quarantine/evidence splits; `assert_dq_passed` enforces fail-or-continue policy. | Quarantine + evidence + pass/fail gate |

Use one shared metadata key across notebooks (for example `DQ_TABLE_NAME = TARGET_TABLE`) so exploration writes and pipeline enforcement reads the same governed rule set.

## Canonical config and real framework prompt

The workflow uses a single canonical prompt source: `CONFIG.ai_prompt_config.dq_rule_candidate_template`.

```python
DQ_TABLE_NAME = TARGET_TABLE
PROMPT_TEMPLATE = CONFIG.ai_prompt_config.dq_rule_candidate_template
```

```text
You are helping draft candidate FabricOps data quality rules for a pipeline contract notebook.

These suggestions are advisory only.
A human engineer, data steward, or governance reviewer must approve them before enforcement.

Use only these FabricOps rule_type values:

1. not_null
   Use when a column must be populated.
   Required fields:
   rule_id, rule_type, columns, severity, description

2. unique_key
   Use when one or more columns define the business grain and must be unique.
   Required fields:
   rule_id, rule_type, columns, severity, description

3. accepted_values
   Use when a column should only contain known business values.
   Required fields:
   rule_id, rule_type, columns, allowed_values, severity, description

4. value_range
   Use when a numeric, date, or timestamp column should stay within a sensible range.
   Required fields:
   rule_id, rule_type, columns, min_value or max_value, severity, description

5. regex_format
   Use when a string column should match a known format such as email, code, phone, postal code, or ID.
   Required fields:
   rule_id, rule_type, columns, regex_pattern, severity, description

Heuristics:
- Suggest not_null when null_count is 0 or when the column name looks mandatory, such as id, key, date, code, status, amount, or name.
- Suggest unique_key only when distinct_count is close to row_count and the column name looks like an identifier or business key.
- Suggest accepted_values when distinct_count is small and the observed values look like business categories.
- Suggest value_range only when min_value and max_value are available and the range is business meaningful.
- Suggest regex_format only for clear format columns such as email, phone, postal_code, programme_code, course_code, invoice_number, or staff_id.
- Use severity="error" only for rules that should block the pipeline.
- Use severity="warning" for rules that should be reviewed but should not block the pipeline.
- Do not suggest unsupported rule types.
- Do not return Great Expectations, Deequ, DQX, SQL, or pseudocode syntax.

Return only a Python dictionary named DQ_RULES using this shape:

DQ_RULES = {
    "{table_name}": [
        {
            "rule_id": "lower_snake_case_rule_id",
            "rule_type": "one_supported_rule_type",
            "columns": ["column_name"],
            "severity": "error_or_warning",
            "description": "Plain business explanation."
        }
    ]
}

For accepted_values, include allowed_values.
For value_range, include min_value and/or max_value.
For regex_format, include regex_pattern.

Table name:
{table_name}

Column profile row:
Column name: {column_name}
Data type: {data_type}
Row count: {row_count}
Null count: {null_count}
Null percent: {null_percent}
Distinct count: {distinct_count}
Distinct percent: {distinct_percent}
Minimum value: {min_value}
Maximum value: {max_value}
Observed values sample: {observed_values_sample}
```

## Sample data used in the one-notebook demo

The self-contained demo notebook uses an email-log sample with deliberate issues for review and enforcement walkthroughs.

```python
sample_rows = [
    {"message_id": "m001", "status": "Delivered", "sender_email": "alice@example.com", "event_count": 1},
    {"message_id": "m002", "status": "Failed", "sender_email": "bob@example.com", "event_count": 2},
    {"message_id": None, "status": "Delivered", "sender_email": "bad-email", "event_count": -1},
    {"message_id": "m002", "status": "Resolved", "sender_email": "carol@example.com", "event_count": 1},
]
```

Issues intentionally included:
- `message_id` null value
- duplicate `message_id` (`m002`)
- invalid email format (`bad-email`)
- negative `event_count`

## End-to-end example aligned to all 7 steps

```python
# 0) Shared key and canonical prompt config
DQ_TABLE_NAME = TARGET_TABLE
PROMPT_TEMPLATE = CONFIG.ai_prompt_config.dq_rule_candidate_template

# 1) Profile source data (02_ex)
profile_rows = profile_for_dq(df_source, table_name=DQ_TABLE_NAME)

# 2) Ask AI for rule candidates (02_ex)
responses = suggest_dq_rules(
    profile_rows,
    prompt_template=PROMPT_TEMPLATE,
    output_col="ai_response",
)

# 3) Parse candidate rules (02_ex)
candidate_rules = extract_dq_rules(responses, table_name=DQ_TABLE_NAME)

# 4) Human review + explicit approval (02_ex)
import fabricops_kit.dq_review as dq_review
review_dq_rules(candidate_rules, table_name=DQ_TABLE_NAME)
approved = list(dq_review.APPROVED_RULES_FROM_WIDGET)
if not approved:
    raise ValueError("No approved DQ rules selected in widget.")

# 5) Persist governed approval history (02_ex)
approved_history = build_dq_rule_history(
    spark=spark,
    table_name=DQ_TABLE_NAME,
    approved_rules=approved,
    action_by="notebook_user",
)

# 6) Pipeline loads and enforces active approved rules (03_pc)
rules = load_active_dq_rules(spark.table("METADATA_DQ_RULES"), table_name=DQ_TABLE_NAME)
dq_result = run_dq_rules(df_standard, table_name=DQ_TABLE_NAME, rules=rules)

# 7) Evidence + gate (03_pc)
df_valid, df_quarantine, dq_failure_evidence = split_dq_rows(
    df_standard,
    rules,
    dq_run_id=RUN_ID,
)
assert_dq_passed(dq_result)
```

## Screenshot slots

Fabric notebook screenshots for steps 1-7 will be added once uploaded to `docs/assets/`.

## Notes

- AI output is advisory; approved metadata is the control point.
- Deterministic pipeline behavior comes from enforcing only approved active rules.
- Quarantine is evidence-first: one source row can produce multiple failure-evidence rows when multiple rules fail.
