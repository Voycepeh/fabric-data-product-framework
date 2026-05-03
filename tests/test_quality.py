import importlib
import json
from datetime import datetime, timedelta, timezone

import pandas as pd
import pytest

from fabricops_kit.quality import (
    DataQualityError,
    assert_quality_gate,
    build_quality_result_records,
    run_quality_rules,
)


def _run(df, rule):
    return run_quality_rules(df, [rule], dataset_name="synthetic", table_name="orders", engine="pandas")


def test_not_null_passes_and_fails():
    assert _run(pd.DataFrame({"a": [1, 2]}), {"rule_id": "1", "rule_type": "not_null", "column": "a"})["results"][0]["status"] == "passed"
    assert _run(pd.DataFrame({"a": [1, None]}), {"rule_id": "1", "rule_type": "not_null", "column": "a"})["results"][0]["status"] == "failed"


def test_unique_and_unique_combination():
    r1 = _run(pd.DataFrame({"a": [1, 2, 2]}), {"rule_type": "unique", "column": "a"})
    assert r1["results"][0]["failed_count"] == 2
    r2 = _run(pd.DataFrame({"a": [1, 1], "b": [1, 2]}), {"rule_type": "unique_combination", "columns": ["a", "b"]})
    assert r2["results"][0]["status"] == "passed"


def test_accepted_values_range_regex():
    df = pd.DataFrame({"status": ["ok", "bad"], "amount": [5, 500], "email": ["a@b.com", "broken"]})
    assert _run(df, {"rule_type": "accepted_values", "column": "status", "accepted_values": ["ok"]})["results"][0]["failed_count"] == 1
    assert _run(df, {"rule_type": "range_check", "column": "amount", "min_value": 0, "max_value": 100})["results"][0]["failed_count"] == 1
    assert _run(df, {"rule_type": "regex_check", "column": "email", "pattern": r"^[^@]+@[^@]+\.[^@]+$"})["results"][0]["failed_count"] == 1


def test_row_count_rules_and_empty_dataframe():
    empty = pd.DataFrame({"a": []})
    assert _run(empty, {"rule_type": "row_count_min", "min_count": 1})["results"][0]["status"] == "failed"
    assert _run(empty, {"rule_type": "row_count_between", "min_count": 0, "max_count": 10})["results"][0]["status"] == "passed"


def test_freshness_passes_and_fails():
    fresh = pd.DataFrame({"updated_at": [datetime.now(timezone.utc) - timedelta(hours=1)]})
    stale = pd.DataFrame({"updated_at": [datetime.now(timezone.utc) - timedelta(days=5)]})
    assert _run(fresh, {"rule_type": "freshness_check", "column": "updated_at", "max_age_days": 2})["results"][0]["status"] == "passed"
    assert _run(stale, {"rule_type": "freshness_check", "column": "updated_at", "max_age_days": 2})["results"][0]["status"] == "failed"


def test_gate_behavior_and_assertion():
    df = pd.DataFrame({"a": [1, None]})
    blocking = run_quality_rules(df, [{"rule_type": "not_null", "column": "a", "severity": "critical"}], engine="pandas")
    assert blocking["status"] == "failed" and not blocking["can_continue"]
    with pytest.raises(DataQualityError):
        assert_quality_gate(blocking)

    warning = run_quality_rules(df, [{"rule_type": "not_null", "column": "a", "severity": "warning"}], engine="pandas")
    assert warning["status"] == "warning" and warning["can_continue"]


def test_records_json_safe_and_unsupported_and_missing_column():
    df = pd.DataFrame({"a": [1]})
    result = run_quality_rules(
        df,
        [
            {"rule_type": "unknown_type", "severity": "warning"},
            {"rule_type": "not_null", "column": "missing"},
        ],
        engine="pandas",
    )
    assert result["results"][0]["status"] == "skipped"
    assert result["results"][1]["status"] == "failed"
    rows = build_quality_result_records(result, run_id="run-1")
    json.dumps(rows)




def test_range_check_min_only_max_only_and_both():
    df = pd.DataFrame({"amount": [-1, 0, 5, 12, None]})
    min_only = _run(df, {"rule_type": "range_check", "column": "amount", "min_value": 0})
    assert min_only["results"][0]["failed_count"] == 1

    max_only = _run(df, {"rule_type": "range_check", "column": "amount", "max_value": 10})
    assert max_only["results"][0]["failed_count"] == 1

    both = _run(df, {"rule_type": "range_check", "column": "amount", "min_value": 0, "max_value": 10})
    assert both["results"][0]["failed_count"] == 2


def test_range_check_missing_min_and_max_is_invalid_rule():
    df = pd.DataFrame({"amount": [1, 2, 3]})
    result = _run(df, {"rule_type": "range_check", "column": "amount"})
    assert result["results"][0]["status"] == "failed"
    assert "requires at least one of min_value or max_value" in result["results"][0]["message"]

def test_import_without_pyspark_and_auto_detection_and_invalid_engine():
    module = importlib.import_module("fabricops_kit.quality")
    assert module is not None
    df = pd.DataFrame({"a": [1]})
    assert run_quality_rules(df, [], engine="auto")["engine"] == "pandas"
    with pytest.raises(ValueError):
        run_quality_rules(df, [], engine="duckdb")
