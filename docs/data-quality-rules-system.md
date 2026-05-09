# Data Quality Rules System

## Purpose

FabricOps uses data quality (DQ) rules as approved expectations attached to the data product being produced. AI can suggest candidate rules from profile metadata, but humans approve those rules before `03_pc` pipeline notebooks enforce them.

![AI-assisted data quality rule flow](assets/DQ-with-ai.png)

## End-to-end flow

| Stage | Notebook | What happens |
|---|---|---|
| 1. Profile | `02_ex` | Create or load sample/source data and profile it |
| 2. Suggest | `02_ex` | Use `ai.response`-style generation (`DataFrame.ai.generate_response`) with the default DQ prompt to suggest candidate rules |
| 3. Review | Human | Steward/engineer edits, accepts, or rejects suggested rules |
| 4. Enforce | `03_pc` | Approved rules are encoded in config/metadata and enforced |
| 5. Quarantine | `03_pc` | Failed rows are retained, pass rows continue |
| 6. Monitor | Metadata tables | DQ results and run evidence are written |

## Flow 1: `02_ex` profiles data and asks AI for candidate rules

```python
from pyspark.sql import Row
from fabricops_kit import (
    profile_dataframe_to_metadata,
    suggest_dq_rules_prompt,
    DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE,
)

df_email_logs = spark.createDataFrame([
    Row(EVENT_ID="E001", STATUS="Delivered", SENDER_EMAIL="a@nus.edu.sg"),
    Row(EVENT_ID="E002", STATUS="Resolved", SENDER_EMAIL="b@nus.edu.sg"),
    Row(EVENT_ID=None, STATUS="Unknown", SENDER_EMAIL=None),
])

# Real FabricOps profiling helper for metadata-style profiling rows
# (TABLE_NAME, COLUMN_NAME, NULL_PERCENT, DISTINCT_COUNT, ...)
df_profile = profile_dataframe_to_metadata(df_email_logs, table_name="EMAIL_LOGS")
```

Use the project default prompt template exactly (from `fabricops_kit.dq`):

```python
prompt = suggest_dq_rules_prompt(
    profile_df=df_profile,
    table_name="EMAIL_LOGS",
    business_context="Campus email event analytics table.",
    output_format="python_config",
    prompt_template=DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE,
)
```

Default prompt template currently used:

```text
You are helping draft candidate data quality rules for table '{table_name}'.
IMPORTANT: AI output is advisory only. A human must review and approve every suggestion before copying into DQ_RULES in 00_config.py.

Business context:
{business_context}

Profile metadata:
{profile_json}

Supported rule types (use only these):
- not_null
- unique_key
- accepted_values
- value_range
- regex_format
- accepted_values_ref
- string_length_between

Hard constraints:
- Return only Python dictionary output named DQ_RULES.
- Do not include Great Expectations, Deequ, DQX, SQL, pseudocode, markdown, or explanatory text.
- Do not invent unsupported rule types.

Output format: {output_format}
Required shape: DQ_RULES = {"TABLE_NAME": [<rule dictionaries>]}
```

In Fabric runtime, AI generation is typically done with DataFrame AI Functions:

```python
# Fabric runtime example for row-level AI suggestions
# (profile rows + prompt template -> ai_dq_rule_candidate output column)
df_profile_ai = df_profile.ai.generate_response(
    prompt=prompt,
    is_prompt_template=False,
    output_col="ai_dq_rule_candidate",
    error_col="ai_dq_rule_error",
    response_format="json_object",
    concurrency=20,
)
```

You can then normalize AI output into candidate metadata columns for review:

| COLUMN_NAME | NULL_PERCENT | DISTINCT_COUNT | suggested_rule_type | suggested_severity | approval_status |
|---|---:|---:|---|---|---|
| EVENT_ID | 33.3 | 2 | not_null | error | pending_review |
| STATUS | 0.0 | 3 | accepted_values | warning | pending_review |
| SENDER_EMAIL | 33.3 | 2 | not_null | warning | pending_review |

This is still candidate metadata. Nothing is enforced until human review and approval.

## Flow 2: `03_pc` enforces approved rules and quarantines failed rows

`03_pc` is the pipeline contract notebook. It should be run-all-safe and should not call AI for enforcement.

```python
from fabricops_kit import (
    run_dq_rules,
    assert_dq_passed,
    split_valid_and_quarantine,
    lakehouse_table_write,
)

DQ_RULES = {
    "EMAIL_LOGS": [
        {
            "rule_id": "EMAIL_LOGS_EVENT_ID_NOT_NULL",
            "rule_type": "not_null",
            "columns": ["EVENT_ID"],
            "severity": "error",
            "description": "EVENT_ID must be present for every row.",
            "approval_status": "approved",
            "approved_by": "data_steward",
        },
        {
            "rule_id": "EMAIL_LOGS_STATUS_ALLOWED",
            "rule_type": "accepted_values",
            "columns": ["STATUS"],
            "allowed_values": ["Delivered", "Resolved"],
            "severity": "warning",
            "description": "STATUS should use approved lifecycle values.",
            "approval_status": "approved",
            "approved_by": "data_steward",
        },
    ]
}

approved_rules = [r for r in DQ_RULES["EMAIL_LOGS"] if r.get("approval_status") == "approved"]

dq_result = run_dq_rules(
    df_email_logs,
    "EMAIL_LOGS",
    approved_rules,
    fail_on_error=False,
)

# Real helper available in fabricops_kit.quality
# Returns (valid_df, quarantine_df) based on row-level rule coverage.
df_pass, df_quarantine = split_valid_and_quarantine(df_email_logs, approved_rules, engine="auto")

lakehouse_table_write(df_pass, lh_out, "EMAIL_LOGS", mode="append")
lakehouse_table_write(df_quarantine, lh_meta, "EMAIL_LOGS_DQ_QUARANTINE", mode="append")
lakehouse_table_write(dq_result, lh_meta, "DQ_RESULTS", mode="append")
assert_dq_passed(dq_result)
```

### Approval process

- AI creates suggestions in `02_ex`.
- Steward/engineer reviews suggestions and approves only usable rules.
- Approved rules are copied into config or approved-rule metadata.
- `03_pc` loads only approved rules.
- `03_pc` writes DQ evidence before failing or continuing.
- `error` severity can fail after logging.
- `warning` severity can continue, but evidence is still written.

## Flow 3: accepted values and AI-assisted mapping suggestions

Accepted-values rules are exact checks. If the source value is not exactly in the approved list, the row fails the rule.

```python
allowed_universities = [
    "National University of Singapore",
    "Nanyang Technological University",
]

dq_rule = {
    "rule_id": "ORG_NAME_ACCEPTED_VALUES",
    "rule_type": "accepted_values",
    "columns": ["ORG_NAME"],
    "allowed_values": allowed_universities,
    "severity": "warning",
    "description": "ORG_NAME must use canonical approved names.",
}
```

Example input values:

- `nus`
- `National University of Singapore`
- `NUS`
- `NTU`

`nus` fails the strict accepted-values check because matching is exact.

AI can assist with candidate mapping suggestions (not auto-correction):

1. Use `ai.similarity` (or equivalent Fabric AI similarity scoring) to find closest approved value.
2. Use `ai.response`/`generate_response` with a constrained prompt.
3. Store the output as candidate mapping metadata.
4. Human approves mapping before production use.

Prompt example:

```text
You are helping standardize organization names for a governed Fabric data pipeline.

Task:
Suggest a mapping from the invalid source value to one approved canonical value.

Rules:
- Only choose from the approved values provided.
- Do not invent new canonical values.
- If confidence is low, return "needs_review".
- Return JSON only with:
  source_value,
  suggested_value,
  confidence,
  reason.

Invalid source value:
{source_value}

Approved values:
{approved_values}
```

Example candidate output:

| source_value | suggested_value | confidence | approval_status |
|---|---|---:|---|
| nus | National University of Singapore | 0.95 | pending_review |

AI suggestion does not mutate production data automatically.

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

## What this page is not

- Not the full DQ architecture: see [Data quality architecture](architecture/data-quality-architecture.md).
- Not the notebook role source of truth: see [Notebook Structure](notebook-structure.md).
- Not a replacement for steward approval.
- Not a complete function index: see [Function Reference](reference/index.md) and module docs under `docs/api/modules/quality.md`.
