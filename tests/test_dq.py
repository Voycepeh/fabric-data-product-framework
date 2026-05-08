import pytest
from pyspark.sql import SparkSession

from fabricops_kit.dq import run_dq_rules, suggest_dq_rules_prompt, validate_dq_rules


@pytest.fixture(scope="module")
def spark_session():
    spark = SparkSession.builder.master("local[1]").appName("test-dq").getOrCreate()
    yield spark
    spark.stop()


def _rules():
    return [
        {"rule_id": "r1", "rule_type": "not_null", "columns": ["id"], "severity": "error", "description": "id required"},
        {"rule_id": "r2", "rule_type": "unique_key", "columns": ["id"], "severity": "error", "description": "id unique"},
        {"rule_id": "r3", "rule_type": "accepted_values", "columns": ["status"], "allowed_values": ["A", "B"], "severity": "warning", "description": "status"},
        {"rule_id": "r4", "rule_type": "value_range", "columns": ["amount"], "min_value": 0, "max_value": 10, "severity": "warning", "description": "range"},
        {"rule_id": "r5", "rule_type": "regex_format", "columns": ["email"], "regex_pattern": r"^[^@]+@[^@]+$", "severity": "warning", "description": "email"},
        {"rule_id": "r6", "rule_type": "row_count_between", "columns": ["id"], "min_rows": 1, "max_rows": 10, "severity": "warning", "description": "rows"},
        {"rule_id": "r7", "rule_type": "schema_required_columns", "columns": ["id", "status"], "severity": "error", "description": "schema"},
        {"rule_id": "r8", "rule_type": "schema_data_type", "columns": ["id"], "expected_types": {"id": "bigint"}, "severity": "warning", "description": "types"},
    ]


def test_validate_dq_rules_valid():
    assert validate_dq_rules(_rules())


def test_validate_dq_rules_invalid_missing_field():
    with pytest.raises(ValueError):
        validate_dq_rules([{"rule_id": "x"}])


def test_suggest_dq_rules_prompt():
    import pandas as pd

    profile = pd.DataFrame([{"column_name": "id", "null_count": 0}])
    prompt = suggest_dq_rules_prompt(profile, "EMAIL_LOGS", business_context="Tracks outbound emails")
    assert "suggestion-only" in prompt
    assert "DQ_RULES" in prompt
    assert "EMAIL_LOGS" in prompt


def test_run_dq_rules_with_spark(spark_session):
    df = spark_session.createDataFrame([
        {"id": 1, "status": "A", "amount": 4, "email": "a@x.com"},
        {"id": 1, "status": "C", "amount": 20, "email": "bad-email"},
    ])
    result = run_dq_rules(df, "EMAIL_LOGS", _rules(), fail_on_error=False)
    rows = {r["rule_id"]: r for r in result.collect()}
    assert rows["r1"]["status"] == "PASS"
    assert rows["r2"]["status"] == "FAIL"
    assert rows["r3"]["status"] == "FAIL"
    assert rows["r4"]["status"] == "FAIL"
    assert rows["r5"]["status"] == "FAIL"


def test_run_dq_rules_fail_on_error_raises(spark_session):
    df = spark_session.createDataFrame([{"id": None, "status": "A", "amount": 1, "email": "a@x.com"}])
    rules = [{"rule_id": "r1", "rule_type": "not_null", "columns": ["id"], "severity": "error", "description": "id required"}]
    with pytest.raises(ValueError):
        run_dq_rules(df, "EMAIL_LOGS", rules, fail_on_error=True)
