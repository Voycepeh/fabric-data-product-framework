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
| 2. Ask AI for candidates | Exploration notebook (`02_ex`) | `suggest_dq_rules` runs the canonical prompt template to propose advisory rule candidates. | AI response text/JSON |
| 3. Parse AI candidates | Exploration notebook (`02_ex`) | `extract_dq_rules` turns responses into candidate rule records scoped to a table key. | Candidate rule rows |
| 4. Human review and selection | Human + widget in `02_ex` | `review_dq_rules` presents candidates; humans approve the subset worth enforcing. | Approved rule list |
| 5. Persist governed history | Exploration notebook (`02_ex`) | `build_dq_rule_history` appends approval decisions to metadata history. | Metadata rule history |
| 6. Load and enforce active rules | Pipeline notebook (`03_pc`) | `load_active_dq_rules` loads approved active rules; `run_dq_rules` evaluates them deterministically. | DQ evaluation result |
| 7. Produce evidence and gate pipeline | Pipeline notebook (`03_pc`) | `split_dq_rows` writes valid/quarantine/evidence splits; `assert_dq_passed` enforces fail-or-continue policy. | Quarantine + evidence + pass/fail gate |

Use one shared metadata key across notebooks (for example `DQ_TABLE_NAME = TARGET_TABLE`) so exploration writes and pipeline enforcement reads the same governed rule set.

## Canonical config and prompt template

The workflow uses a single canonical prompt source: `CONFIG.ai_prompt_config.dq_rule_candidate_template`.

```python
# Canonical configuration usage in notebook code
DQ_TABLE_NAME = TARGET_TABLE
PROMPT_TEMPLATE = CONFIG.ai_prompt_config.dq_rule_candidate_template
```

```text
# Canonical DQ candidate prompt pattern (conceptual form)
You are a data quality assistant.
Given profiling evidence for table: {table_name}
Suggest candidate DQ rules that are specific, testable, and implementation-ready.
Return structured rule candidates with fields such as:
- rule_name
- rule_description
- rule_type
- rule_expression
- severity
- rationale_from_profile

Important:
- Treat output as advisory only.
- Do not auto-approve rules.
- Favor precise thresholds grounded in observed profile evidence.
```

## Sample data used in the workflow

Use a small, teachable dataset with intentional quality issues so AI suggestions and human review are easy to demonstrate.

```python
sample_rows = [
    {"order_id": 1001, "customer_id": "C001", "order_total": 120.50, "country_code": "SG", "order_date": "2025-01-10"},
    {"order_id": 1002, "customer_id": "C002", "order_total": -9.99,  "country_code": "US", "order_date": "2025-01-11"},  # invalid negative total
    {"order_id": 1003, "customer_id": None,   "order_total": 42.00,  "country_code": "XX", "order_date": "2025-01-12"},  # missing customer, invalid country
    {"order_id": 1003, "customer_id": "C004", "order_total": 87.25,  "country_code": "SG", "order_date": "2025-01-13"},  # duplicate order_id
    {"order_id": 1005, "customer_id": "C005", "order_total": 65.00,  "country_code": "SG", "order_date": None},          # missing order_date
]
```

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
import fabricops_kit.data_quality_review as dq_review
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

## Fabric notebook screenshot slots (placeholders for later upload)

> Replace these placeholder images with real Fabric notebook screenshots when available.

### Step 1-3: Profiling and AI candidate generation (`02_ex`)

![Placeholder: profiling and AI candidate generation](assets/dq-step-1-3-placeholder.png)

### Step 4-5: Human review and approval persistence (`02_ex`)

![Placeholder: human review and metadata persistence](assets/dq-step-4-5-placeholder.png)

### Step 6: Pipeline rule enforcement (`03_pc`)

![Placeholder: pipeline DQ rule enforcement](assets/dq-step-6-placeholder.png)

### Step 7: Quarantine evidence and pipeline gating (`03_pc`)

![Placeholder: quarantine evidence and gate](assets/dq-step-7-placeholder.png)

## Notes

- AI output is advisory; approved metadata is the control point.
- Deterministic pipeline behavior comes from enforcing only approved active rules.
- Quarantine is evidence-first: one source row can produce multiple failure-evidence rows when multiple rules fail.
