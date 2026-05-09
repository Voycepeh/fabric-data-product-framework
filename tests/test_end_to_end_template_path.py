from pathlib import Path
from runpy import run_path

import pytest

from fabricops_kit.data_contracts import build_contract_records, get_executable_quality_rules, normalize_contract_dict, validate_contract_dict
from fabricops_kit.data_quality import split_valid_and_quarantine, validate_dq_rules


def test_sample_assets_exist():
    assert Path("samples/end_to_end/minimal_source.csv").exists()
    assert Path("samples/end_to_end/minimal_source_contract.py").exists()


def test_contract_and_rule_path():
    raw = run_path("samples/end_to_end/minimal_source_contract.py")["MINIMAL_SOURCE_CONTRACT"]
    contract = normalize_contract_dict(raw)
    assert contract["status"] == "approved"
    assert validate_contract_dict(contract) == []
    rules = get_executable_quality_rules(contract)
    assert rules
    validate_dq_rules(rules)
    rule_types = {r.get("rule_type") for r in rules}
    assert {"not_null", "unique_key", "accepted_values", "value_range", "regex_format"}.issubset(rule_types)


def test_build_contract_records_with_sample_contract():
    contract = normalize_contract_dict(run_path("samples/end_to_end/minimal_source_contract.py")["MINIMAL_SOURCE_CONTRACT"])
    records = build_contract_records(contract)
    assert records["contracts"]
    assert records["columns"]
    assert records["rules"]
    email_col = next(r for r in records["columns"] if r["column_name"] == "email")
    assert email_col["logical_type"] == "email"
    assert email_col["physical_type"] == "string"


def test_split_valid_and_quarantine_unique_key_support():
    pytest.importorskip("pyspark", reason="pyspark is required for Spark quarantine split tests")
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.master("local[1]").appName("test-unique-key-quarantine").getOrCreate()
    try:
        df = spark.createDataFrame(
            [("C001",), ("C001",), ("C002",)],
            ["customer_id"],
        )
        rules = [
            {
                "rule_id": "r_customer_unique",
                "rule_type": "unique_key",
                "columns": ["customer_id"],
                "severity": "warning",
                "description": "Customer ID should be unique per extract.",
            }
        ]
        df_valid, df_quarantine = split_valid_and_quarantine(df, rules)
        assert df_valid.count() == 1
        assert df_quarantine.count() == 2
        assert "dq_failed_rule_ids" in df_quarantine.columns
    finally:
        spark.stop()


def test_notebook_templates_contain_required_flow():
    pc = Path("templates/notebooks/03_pc_agreement_source_to_target.ipynb").read_text(encoding="utf-8")
    ex = Path("templates/notebooks/02_ex_agreement_topic.ipynb").read_text(encoding="utf-8")

    assert "run_path(\"samples/end_to_end/minimal_source_contract.py\")" in pc
    assert "rules = get_executable_quality_rules(contract)" in pc
    assert 'rules = DQ_RULES.get(TARGET_TABLE, [])' not in pc
    assert "split_valid_and_quarantine" in pc
    assert 'f\"{TARGET_TABLE}_QUARANTINE\"' in pc
    assert "build_dataset_run_record" in pc
    assert "build_quality_result_records" in pc
    assert ("build_contract_records" in pc) or ("write_contract_to_lakehouse" in pc)
    assert ("build_lineage_records" in pc) or ("build_lineage_record_from_steps" in pc)
    assert 'NOTEBOOK_CODE_FOR_LINEAGE = """' not in pc
    assert "suggest_dq_rules_prompt" in ex
    assert "validate_contract_dict" in ex
