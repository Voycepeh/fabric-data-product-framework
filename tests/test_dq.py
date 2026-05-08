from pathlib import Path
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


def test_public_api_exports():
    from fabricops_kit import (
        get_default_dq_rule_templates,
        validate_dq_rules as _validate,
        run_dq_rules as _run,
        write_dq_results as _write,
        suggest_dq_rules_prompt as _suggest,
        assert_dq_passed as _assert,
    )
    assert callable(get_default_dq_rule_templates)
    assert callable(_validate) and callable(_run) and callable(_write) and callable(_suggest) and callable(_assert)


def test_schema_data_type_missing_expected_type_key():
    with pytest.raises(ValueError, match="expected_types missing columns"):
        validate_dq_rules([{
            "rule_id": "t", "rule_type": "schema_data_type", "columns": ["id", "x"],
            "expected_types": {"id": "bigint"}, "severity": "warning", "description": "d"
        }])


def test_fail_log_then_assert_pattern(spark_session):
    from fabricops_kit.dq import assert_dq_passed
    df = spark_session.createDataFrame([{"id": None}])
    rules = [{"rule_id": "r1", "rule_type": "not_null", "columns": ["id"], "severity": "error", "description": "id required"}]
    result = run_dq_rules(df, "EMAIL_LOGS", rules, fail_on_error=False)
    assert result.count() == 1
    with pytest.raises(ValueError):
        assert_dq_passed(result)


def test_not_null_rejects_multiple_columns():
    with pytest.raises(ValueError, match="exactly one column"):
        validate_dq_rules([{
            "rule_id": "r1", "rule_type": "not_null", "columns": ["id", "status"],
            "severity": "error", "description": "id and status required"
        }])


def test_run_dq_rules_rejects_quality_rule_shape(spark_session):
    df = spark_session.createDataFrame([{"id": 1}])
    with pytest.raises(ValueError, match="missing required field 'columns'"):
        run_dq_rules(df, "EMAIL_LOGS", [{
            "rule_id": "legacy", "rule_type": "not_null", "column": "id",
            "severity": "error", "reason": "legacy shape"
        }], fail_on_error=False)


def test_dq_collect_rows_converted_to_dicts_for_quality_records(spark_session):
    from fabricops_kit import build_quality_result_records

    df = spark_session.createDataFrame([{"id": 1}])
    rules = [{"rule_id": "r1", "rule_type": "not_null", "columns": ["id"], "severity": "error", "description": "id required"}]
    dq_result = run_dq_rules(df, "EMAIL_LOGS", rules, fail_on_error=False)
    dq_result_records = [r.asDict(recursive=True) for r in dq_result.collect()]
    payload = {"results": dq_result_records, "can_continue": True}
    quality_records = build_quality_result_records(payload, run_id="r", dataset_name="d", table_name="t", table_stage="source")
    assert isinstance(dq_result_records[0], dict)
    assert isinstance(quality_records, list)


def test_notebook_templates_reference_defined_dq_names():
    import json
    for path in [
        "templates/notebooks/02_ex_agreement_topic.ipynb",
        "templates/notebooks/03_pc_agreement_source_to_target.ipynb",
    ]:
        nb = json.loads(Path(path).read_text())
        joined = "\n".join("".join(c.get("source", [])) for c in nb.get("cells", []) if c.get("cell_type") == "code")
        assert "lh_out" not in joined
    pc = json.loads(Path("templates/notebooks/03_pc_agreement_source_to_target.ipynb").read_text())
    code = "\n".join("".join(c.get("source", [])) for c in pc["cells"] if c.get("cell_type") == "code")
    assert "run_quality_rules(" not in code
    assert "contract.source.business_keys" not in code
    assert "contract.target.required_columns" not in code
    assert "get_executable_quality_rules(contract)" not in code
    assert 'dq_results_path = get_path(ENV_NAME, "metadata", config=CONFIG)' in code

    ex = json.loads(Path("templates/notebooks/02_ex_agreement_topic.ipynb").read_text())
    ex_code = "\n".join("".join(c.get("source", [])) for c in ex["cells"] if c.get("cell_type") == "code")
    assert "classification_candidates = classify_columns(" in ex_code
