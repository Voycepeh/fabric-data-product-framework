from pathlib import Path

import pytest

from fabric_data_product_framework.data_contract import (
    assert_data_product_passed,
    build_runtime_context_from_contract,
    load_data_contract,
    validate_data_contract_shape,
)


def _valid_contract():
    return {
        "dataset": {"name": "orders", "description": "desc", "owner": "owner", "approved_usage": "analytics"},
        "environment": {"name": "dev", "metadata_schema": "meta"},
        "source": {"table": "bronze.orders", "format": "delta"},
        "target": {"table": "silver.orders", "mode": "append", "format": "delta"},
        "keys": {"business_keys": ["order_id"], "watermark_column": "updated_at", "partition_column": "order_date"},
        "schema": {"required_source_columns": ["order_id"], "required_output_columns": ["order_id"]},
        "quality": {"rules": []},
        "drift": {"schema_policy": {}, "incremental_policy": {}},
        "metadata": {
            "source_profile_table": "meta.source_profile",
            "output_profile_table": "meta.output_profile",
            "schema_snapshot_table": "meta.schema_snapshot",
            "partition_snapshot_table": "meta.partition_snapshot",
            "quality_result_table": "meta.quality_result",
            "quarantine_table": "meta.quarantine",
            "contract_validation_table": "meta.contract_validation",
            "lineage_table": "meta.lineage",
            "run_summary_table": "meta.run_summary",
            "dataset_runs_table": "meta.dataset_runs",
        },
    }


def test_validate_data_contract_shape_passes_for_complete_contract():
    assert validate_data_contract_shape(_valid_contract()) == []


def test_validate_data_contract_shape_reports_missing_sections():
    contract = _valid_contract()
    del contract["metadata"]
    errors = validate_data_contract_shape(contract)
    assert "Missing required section: metadata" in errors


def test_load_data_contract_accepts_dict_and_path(tmp_path: Path):
    contract = _valid_contract()
    loaded_dict = load_data_contract(contract)
    assert loaded_dict["dataset"]["name"] == "orders"

    contract_file = tmp_path / "contract.yml"
    contract_file.write_text("dataset:\n  name: orders\n", encoding="utf-8")
    loaded_path = load_data_contract(contract_file)
    assert loaded_path["dataset"]["name"] == "orders"


def test_build_runtime_context_from_contract_uses_contract_fields():
    ctx = build_runtime_context_from_contract(_valid_contract(), overrides={"run_id": "run_123"})
    assert ctx["dataset_name"] == "orders"
    assert ctx["environment"] == "dev"
    assert ctx["run_id"] == "run_123"


def test_assert_data_product_passed_raises_for_failed_status():
    with pytest.raises(RuntimeError):
        assert_data_product_passed({"status": "failed"})
