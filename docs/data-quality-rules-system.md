# AI-Assisted Data Quality

## Purpose

FabricOps uses an AI-in-the-loop workflow for data quality (DQ):

- AI suggests candidate rules from profiling evidence.
- Humans review and explicitly approve/reject each candidate.
- Metadata records those decisions as governed rule history.
- Pipeline notebooks enforce only approved, active rules deterministically.

![AI-assisted data quality rule flow](assets/DQ-with-ai.png)

## Run the example end to end

Want to try the workflow immediately? Import the example one-notebook demo into Fabric, install the matching `fabricops_kit` wheel, and run the full flow from profiling to approved-rule enforcement and quarantine handling.

- [Example one-notebook DQ demo](https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/examples/notebooks/FabricOps_AI_DQ_Source_of_Truth_Widget_Metadata_Flow.ipynb)
- Matching wheel release: Coming with the tested release asset.

## Main workflow

The core execution path is a 7-step workflow aligned to the visual flow: **AI suggests, humans approve, pipelines enforce, and results split into accepted vs. quarantined outputs**.

| Step | Where | What happens | Output |
|---|---|---|---|
| 1. Source data | Input dataframe or source table | Start from the raw dataframe or source table. | Source dataframe |
| 2a. Load profiled data and approved rules | Exploration notebook (`02_ex`) + metadata | Load existing profile evidence and currently approved active DQ rules when available. | Reusable profile + active-rule context |
| 2b. Profile data (if needed) | Exploration notebook (`02_ex`) | Profile or refresh evidence only when profile metadata is missing or stale for the current dataset/question. | Current profile evidence metadata |
| 3. AI suggests DQ rules | Exploration notebook (`02_ex`) | Generate candidate value-level DQ rules from profile evidence and business context. | Candidate DQ rules |
| 4. Human review and approval | Analyst/engineer + DQ review widget in `02_ex` | Review, edit, approve, or reject suggested rules. | Reviewed decisions + approved rules |
| 5. Store approved rules | Exploration notebook (`02_ex`) + metadata | Persist approved rules as governed metadata history. | Approved DQ metadata |
| 6. Pipeline applies approved rules | Pipeline notebook (`03_pc`) | Load only approved active rules and enforce them deterministically. | DQ enforcement result |
| 7. Split results | Pipeline notebook (`03_pc`) | Split enforcement output into accepted rows and quarantined failed rows with reasons. | Accepted rows + quarantined rows |

Use one shared metadata key across notebooks (for example `DQ_TABLE_NAME = TARGET_TABLE`) so exploration writes and pipeline enforcement reads the same governed rule set.

## Outputs

- **Accepted rows**: valid rows continue to downstream pipeline steps.
- **Quarantined rows**: failed rows are isolated with explicit failure reasons for triage and remediation.

## Optional feedback loop

Feedback and learning are **not** a numbered execution step. As an optional continuous-improvement loop, AI suggestions, human decisions, and approved-rule history can be captured as reusable metadata to improve future rule suggestions, prompts, and evaluation.

## Expandable rule set

Start with a compact set of high-value value-level rules so the workflow stays understandable and practical. Then add rule types over time as needed. The same shared approval-and-enforcement engine remains in place, so the workflow stays consistent while coverage expands.

## Canonical config and real framework prompt

The workflow uses a single canonical prompt source: `CONFIG.ai_prompt_config.dq_rule_candidate_template`.

```python
DQ_TABLE_NAME = TARGET_TABLE
PROMPT_TEMPLATE = CONFIG.ai_prompt_config.dq_rule_candidate_template
```

```text
You are helping draft candidate FabricOps data quality rules for a pipeline contract notebook.

These suggestions are advisory only.
A human analyst or engineer must approve them before enforcement.

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
   rule_id, rule_type, columns, lower_bound or upper_bound, severity, description

5. regex_format
   Use when a string column should match a known format such as email, code, phone, postal code, or ID.
   Required fields:
   rule_id, rule_type, columns, regex_pattern, severity, description

Heuristics:
- Suggest not_null when null_count is 0 or when the column name looks mandatory, such as id, key, date, code, status, amount, or name.
- Suggest unique_key only when distinct_count is close to row_count and the column name looks like an identifier or business key.
- Suggest accepted_values when distinct_count is small and the observed values look like business categories.
- Suggest value_range only when lower_bound and upper_bound are available and the range is business meaningful.
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
For value_range, include lower_bound and/or upper_bound.
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

## Implementation example behind the workflow

```python
# 0) Shared key and canonical prompt config
DQ_TABLE_NAME = TARGET_TABLE
PROMPT_TEMPLATE = CONFIG.ai_prompt_config.dq_rule_candidate_template

# 1) Create or load profile metadata (02_ex)
profile_rows = profile_dataframe_to_metadata(df_source, table_name=DQ_TABLE_NAME)
# or: profile_rows = spark.table("METADATA_PROFILE_TABLE")

# 2) Optional: load existing approved active rules (02_ex)
dq_metadata_table = FABRIC_CONFIG.review_workflow_config.dq_approved_table
existing_dq_df = read_lakehouse_table(metadata_path, dq_metadata_table)
approved_active_rules = load_dq_rules(existing_dq_df, table_name=DQ_TABLE_NAME)

# 3) Ask AI for candidate rules from profile metadata when needed (02_ex)
candidate_rules = draft_dq_rules(
    profile_df=profile_rows,
    table_name=DQ_TABLE_NAME,
    business_context=BUSINESS_CONTEXT,
    prompt_template=PROMPT_TEMPLATE,
    output_col="ai_response",
)

# 4) Launch human review widget (02_ex)
run_dq_rule_review_widget(
    candidate_rules,
    table_name=DQ_TABLE_NAME,
)
# 4) After analyst/engineer interaction, collect current widget state (02_ex)
review = get_dq_review_results(
    table_name=DQ_TABLE_NAME,
    environment_name=ENV_NAME,
    dataset_name=DATASET_NAME,
)
approved = review["approved_rules"]
if not approved:
    raise ValueError("No approved DQ rules selected in widget.")

# 5) Persist analyst / engineer DQ approval history (02_ex)
write_dq_rules(
    approved,
    table_name=DQ_TABLE_NAME,
    metadata_path=metadata_path,
    action_by="notebook_user",
)

# Optional feedback loop: review active rules for deactivation (02_ex)
deactivation_reviews = review_dq_rule_deactivations(
    approved_active_rules,
    table_name=DQ_TABLE_NAME,
)
deactivation_df = _build_dq_rule_deactivation_metadata_df(
    deactivation_reviews,
    table_name=DQ_TABLE_NAME,
)

# 6) Pipeline loads active approved rules only (03_pc)
approved_for_pipeline = load_dq_rules(
    read_lakehouse_table(metadata_path, dq_metadata_table),
    table_name=DQ_TABLE_NAME,
)

# 7) Pipeline enforces approved active rules deterministically (03_pc)
dq = enforce_dq(
    df_standard,
    table_name=DQ_TABLE_NAME,
    rules=approved_for_pipeline,
    dq_run_id=RUN_ID,
)

# 7) Split outputs
_ = dq.valid_rows
_ = dq.quarantine_rows
_ = dq.failure_rows

# Final explicit gate
assert_dq_passed(dq.rule_results)
```

## Screenshot slots

Fabric notebook screenshots for steps 1-7 will be added once uploaded to `docs/assets/`.

## Notes

- AI output is advisory; approved metadata is the control point.
- Deterministic pipeline behavior comes from enforcing only approved active rules.
- Quarantine is evidence-first: one source row can produce multiple failure-evidence rows when multiple rules fail.


Existing active rules can be reviewed for deactivation using the existing `review_dq_rule_deactivations` helper. Deactivations must include an explicit action reason and should be persisted as append-only inactive metadata rows.
