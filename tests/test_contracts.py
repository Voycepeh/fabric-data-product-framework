import json
from datetime import datetime, timedelta, timezone

import pandas as pd
import pytest

from fabric_data_product_framework import contracts


def _contract(expected_freshness: str = "2 days"):
    return {
        "dataset": {"name": "sales", "purpose": "testing"},
        "source": {"table": "bronze.sales"},
        "target": {"table": "silver.sales"},
        "refresh": {"watermark_column": "updated_at"},
        "keys": {"business_keys": ["id"]},
        "contracts": {
            "upstream": {"expected_columns": ["id", "updated_at"], "expected_freshness": expected_freshness},
            "downstream": {"guaranteed_columns": ["id", "updated_at", "value"]},
        },
    }


def test_required_columns_and_extra():
    df = pd.DataFrame({"id": [1], "updated_at": ["2026-01-01"], "x": [1]})
    res = contracts.validate_required_columns(df, ["id", "updated_at"], engine="auto")
    assert res["status"] == "passed"
    assert res["extra"] == ["x"]


def test_required_columns_missing_fails():
    df = pd.DataFrame({"id": [1]})
    res = contracts.validate_required_columns(df, ["id", "updated_at"], engine="pandas")
    assert res["status"] == "failed"


def test_grain_checks_and_duplicate_counts_are_consistent():
    ok = pd.DataFrame({"id": [1, 2]})
    triple_dup = pd.DataFrame({"id": [1, 1, 1]})
    miss = pd.DataFrame({"other": [1]})
    assert contracts.validate_grain(ok, ["id"], engine="auto")["status"] == "passed"
    result = contracts.validate_grain(triple_dup, ["id"], engine="auto")
    assert result["status"] == "failed"
    assert result["duplicate_key_count"] == 1
    assert result["duplicate_row_count"] == 3
    assert result["duplicate_count"] == 3
    assert contracts.validate_grain(miss, ["id"], engine="auto")["status"] == "failed"


def test_freshness_pass_and_fail_and_hour_based_contract_support():
    fresh = pd.DataFrame({"updated_at": [datetime.now(timezone.utc)]})
    stale = pd.DataFrame({"updated_at": [datetime.now(timezone.utc) - timedelta(days=10)]})
    assert contracts.validate_freshness(fresh, "updated_at", max_age_days=2, engine="pandas")["status"] == "passed"
    assert contracts.validate_freshness(stale, "updated_at", max_age_days=2, engine="pandas")["status"] == "failed"

    src = pd.DataFrame({"id": [1], "updated_at": [datetime.now(timezone.utc) - timedelta(hours=24)]})
    # 25 hours should pass and 23 hours should fail for the same data point.
    assert contracts.validate_upstream_contract(src, _contract("25 hours"), engine="auto")["status"] == "passed"
    assert contracts.validate_upstream_contract(src, _contract("23 hours"), engine="auto")["status"] == "failed"


def test_upstream_downstream_runtime_and_assert_and_records():
    c = _contract()
    src = pd.DataFrame({"id": [1], "updated_at": [datetime.now(timezone.utc)]})
    out = pd.DataFrame({"id": [1], "updated_at": [datetime.now(timezone.utc)], "value": [10]})
    up = contracts.validate_upstream_contract(src, c, engine="auto")
    down = contracts.validate_downstream_contract(out, c, engine="auto")
    assert up["contract_type"] == "upstream"
    assert down["contract_type"] == "downstream"
    combined = contracts.validate_runtime_contracts(source_df=src, output_df=out, contract=c, engine="auto")
    contracts.assert_contracts_valid(combined)
    rows = contracts.build_contract_validation_records(combined, run_id="r1")
    assert rows and rows[0]["run_id"] == "r1"
    json.dumps(rows)


def test_assert_raises_on_blocking_failure():
    c = _contract()
    src = pd.DataFrame({"id": [1]})
    result = contracts.validate_runtime_contracts(source_df=src, contract=c, engine="auto")
    with pytest.raises(contracts.ContractValidationError):
        contracts.assert_contracts_valid(result)


def test_invalid_engine_and_lazy_import():
    df = pd.DataFrame({"id": [1]})
    with pytest.raises(ValueError):
        contracts.validate_required_columns(df, ["id"], engine="duckdb")
    assert "pyspark" not in contracts.__dict__
