import pandas as pd

from fabric_data_product_framework.ai_quality_rules import (
    build_layman_rule_records,
    build_quality_rule_generation_prompt,
    build_quality_rule_prompt_context,
    normalize_quality_rule_candidate,
    parse_ai_quality_rule_candidates,
)
from fabric_data_product_framework.quarantine import (
    add_dq_failure_columns,
    split_valid_and_quarantine,
)
from fabric_data_product_framework.rule_compiler import compile_layman_rule_to_quality_rule


def test_prompt_context_and_prompt_instructions():
    profile = {"dataset_name": "sales", "table_name": "orders", "summary": {"row_count": 100, "distinct_count": 95}}
    context = build_quality_rule_prompt_context(profile)
    prompt = build_quality_rule_generation_prompt(profile)
    assert context["dataset_name"] == "sales"
    assert "summary" in str(context["profile"])
    assert "layman_rule" in prompt
    assert "JSON array only" in prompt


def test_parse_valid_array_markdown_fence_and_malformed_json():
    raw = '[{"rule_type":"not_null","column":"id"}]'
    parsed = parse_ai_quality_rule_candidates(raw)
    assert parsed["ok"] is True
    fenced = '```json\n[{"rule_type":"not_null","column":"id"}]\n```'
    parsed_fenced = parse_ai_quality_rule_candidates(fenced)
    assert parsed_fenced["ok"] is True
    bad = parse_ai_quality_rule_candidates("not-json")
    assert bad["ok"] is False


def test_normalize_defaults_and_candidate_status():
    normalized = normalize_quality_rule_candidate({"rule_type": "not_null", "column": "id"})
    assert normalized["approval_status"] == "candidate"
    assert normalized["severity"] == "warning"


def test_compiler_supported_and_skipped_cases():
    assert compile_layman_rule_to_quality_rule({"rule_type": "not_null", "column": "email", "layman_rule": "Email should not be blank."})["status"] == "compiled"
    assert compile_layman_rule_to_quality_rule({"rule_type": "unique", "column": "id"})["status"] == "compiled"
    assert compile_layman_rule_to_quality_rule({"rule_type": "accepted_values", "column": "status", "rule_config": {"accepted_values": ["Active", "Inactive"]}})["status"] == "compiled"
    assert compile_layman_rule_to_quality_rule({"rule_type": "range_check", "column": "score", "rule_config": {"min_value": 0, "max_value": 100}})["status"] == "compiled"
    assert compile_layman_rule_to_quality_rule({"rule_type": "regex_check", "column": "email", "rule_config": {"pattern": ".+@.+"}})["status"] == "compiled"
    assert compile_layman_rule_to_quality_rule({"rule_type": "freshness_check", "column": "updated_at", "rule_config": {"max_age_days": 7}})["status"] == "compiled"
    assert compile_layman_rule_to_quality_rule({"rule_type": "unsupported"})["status"] == "skipped"
    assert compile_layman_rule_to_quality_rule({"rule_type": "not_null"})["status"] == "skipped"


def test_pandas_quarantine_helpers():
    df = pd.DataFrame({"id": [1, None], "email": ["ok@example.com", "bad"]})
    rules = [
        {"rule_id": "DQ001", "rule_type": "not_null", "column": "id", "severity": "critical", "reason": "id required"},
        {"rule_id": "DQ002", "rule_type": "regex_check", "column": "email", "pattern": r"^[^@]+@[^@]+\.[^@]+$", "severity": "warning", "reason": "email format"},
    ]
    enriched = add_dq_failure_columns(df, rules, engine="pandas")
    assert len(enriched.loc[1, "dq_errors"]) >= 1
    assert len(enriched.loc[1, "dq_warnings"]) >= 1
    valid_df, quarantine_df = split_valid_and_quarantine(df, rules, engine="pandas")
    assert len(valid_df) == 1
    assert len(quarantine_df) == 1


def test_build_layman_records():
    rows = build_layman_rule_records([{"rule_id": "R1", "rule_type": "not_null", "layman_rule": "id required"}], "run1", "ds", "tbl")
    assert rows[0]["approval_status"] == "candidate"
