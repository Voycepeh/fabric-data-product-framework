import pandas as pd

from fabricops_kit.dq import (
    build_layman_rule_records,
    build_quality_rule_generation_prompt,
    build_quality_rule_prompt_context,
    parse_ai_quality_rule_candidates,
)
from fabricops_kit.dq import add_dq_failure_columns, split_valid_and_quarantine
from fabricops_kit.dq import compile_layman_rules_to_quality_rules


def test_prompt_context_and_prompt_instructions():
    profile = {"dataset_name": "sales", "table_name": "orders", "summary": {"row_count": 100}}
    context = build_quality_rule_prompt_context(profile)
    prompt = build_quality_rule_generation_prompt(profile)
    assert context["dataset_name"] == "sales"
    assert "layman_rule" in prompt


def test_parse_preserves_unsupported_and_incomplete_suggestions():
    raw = '[{"rule_type":"not_null","column":"id"},{"rule_type":"unsupported_rule","column":"x"},{"rule_type":"not_null"}]'
    parsed = parse_ai_quality_rule_candidates(raw)
    assert len(parsed["candidates"]) == 3
    assert parsed["candidates"][1]["can_compile"] is False
    assert parsed["candidates"][2]["can_compile"] is False
    assert len(parsed["warnings"]) >= 2


def test_build_layman_records_stores_unsupported_with_can_compile_false():
    parsed = parse_ai_quality_rule_candidates('[{"rule_type":"unsupported_rule","layman_rule":"Human rule"}]')
    rows = build_layman_rule_records(parsed["candidates"], "run1", "ds", "tbl")
    assert rows[0]["can_compile"] is False
    assert rows[0]["candidate_json"]["rule_type"] == "unsupported_rule"


def test_compiler_returns_skipped_record_for_unsupported():
    out = compile_layman_rules_to_quality_rules([{"rule_type": "unsupported_rule", "layman_rule": "desc"}])
    rec = out["records"][0]
    assert rec["status"] == "skipped"
    assert rec["compiler_warning"] is True
    assert rec["layman_rule"] == "desc"


def test_pandas_quarantine_unique_and_unique_combination():
    df = pd.DataFrame({"id": [1, 1, 2], "a": ["x", "x", "x"], "b": [1, 1, 2]})
    rules = [
        {"rule_id": "U1", "rule_type": "unique", "column": "id", "severity": "critical", "reason": "id unique"},
        {"rule_id": "U2", "rule_type": "unique_combination", "columns": ["a", "b"], "severity": "warning", "reason": "combo unique"},
    ]
    enriched = add_dq_failure_columns(df, rules, engine="pandas")
    assert len(enriched.loc[0, "dq_errors"]) >= 1
    assert len(enriched.loc[0, "dq_warnings"]) >= 1
    valid_df, quarantine_df = split_valid_and_quarantine(df, rules, engine="pandas")
    assert len(quarantine_df) == 2
    assert len(valid_df) == 1


def test_parse_fenced_malformed_and_non_array():
    fenced = '''```json
[{"rule_type":"not_null","column":"id"}]
```'''
    ok = parse_ai_quality_rule_candidates(fenced)
    assert ok["ok"] is True

    malformed = parse_ai_quality_rule_candidates('{bad')
    assert malformed["ok"] is False

    non_array = parse_ai_quality_rule_candidates('{"rule_type":"not_null"}')
    assert non_array["ok"] is False


def test_normalization_defaults():
    parsed = parse_ai_quality_rule_candidates('[{"rule_type":"not_null","column":"id","columns":"k"}]')
    c = parsed["candidates"][0]
    assert c["approval_status"] == "candidate"
    assert c["severity"] == "warning"
    assert c["confidence"] == "medium"
    assert c["rule_config"] == {}
    assert isinstance(c["columns"], list)
