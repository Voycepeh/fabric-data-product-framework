import pandas as pd

from fabric_data_product_framework.data_contract import run_data_product
from fabric_data_product_framework.dq import (
    build_dq_rule_records,
    generate_dq_rule_candidates_with_fabric_ai,
    load_dq_rules,
    normalize_dq_rule,
    normalize_dq_rules,
    run_dq_rules,
    run_dq_workflow,
    store_dq_rules,
)


class _FakeWriter:
    def __init__(self, spark, df):
        self.spark = spark
        self.df = df
        self._mode = "append"

    def mode(self, mode):
        self._mode = mode
        return self

    def saveAsTable(self, table):
        self.spark.tables[table] = self.df.copy()


class _FakeSparkDF:
    def __init__(self, spark, df):
        self.spark = spark
        self._df = df

    @property
    def write(self):
        return _FakeWriter(self.spark, self._df)


class _FakeSpark:
    def __init__(self, source_df):
        self.source_df = source_df
        self.tables = {}
        self.writes = []

    def table(self, name):
        if name in self.tables:
            return self.tables[name].copy()
        return self.source_df.copy()

    def createDataFrame(self, rows):
        if isinstance(rows, pd.DataFrame):
            return _FakeSparkDF(self, rows)
        return _FakeSparkDF(self, pd.DataFrame(rows))




class _FakeAI:
    def __init__(self, response):
        self.response = response

    def generate_response(self, **_kwargs):
        return self.response


def test_generate_dq_rule_candidates_with_fabric_ai_success(monkeypatch):
    response = '[{"rule_id":"ai1","column":"order_id","rule_type":"not_null","severity":"critical","layman_rule":"order id required","rule_config":{}}]'

    monkeypatch.setattr(pd.DataFrame, "ai", property(lambda self: _FakeAI(response)), raising=False)
    out = generate_dq_rule_candidates_with_fabric_ai(profile={"columns": []}, dataset_name="orders", table_name="silver.orders")
    assert out
    assert out[0]["rule_id"] == "ai1"
    assert out[0]["status"] == "candidate"


def test_generate_dq_rule_candidates_with_fabric_ai_missing_extension(monkeypatch):
    monkeypatch.setattr(pd.DataFrame, "ai", property(lambda self: None), raising=False)
    try:
        generate_dq_rule_candidates_with_fabric_ai(profile={"columns": []})
        assert False, "Expected RuntimeError"
    except RuntimeError as exc:
        assert "Fabric Runtime 1.3+" in str(exc)

def test_normalize_dq_rule_aliases():
    out = normalize_dq_rule({"id": "x", "rule_type": "not_empty", "field": "a", "allowed_values": ["x"], "min": 1})
    assert out["rule_id"] == "x"
    assert out["rule_type"] == "not_null"
    assert out["column"] == "a"
    assert out["accepted_values"] == ["x"]
    assert out["min_value"] == 1


def test_normalize_dq_rules_safe_none_empty():
    assert normalize_dq_rules(None) == []
    assert normalize_dq_rules([]) == []


def test_build_dq_rule_records_has_lifecycle_and_json():
    rows = build_dq_rule_records([{"rule_id": "r1", "rule_type": "not_null", "column": "order_id"}], "orders", "silver.orders", run_id="run1")
    assert rows[0]["rule_id"] == "r1"
    assert rows[0]["status"] == "candidate"
    assert "rule_json" in rows[0]
    assert "created_at" in rows[0]


def test_run_dq_rules_executes_quality_runner():
    df = pd.DataFrame([{"order_id": 1}, {"order_id": None}])
    result = run_dq_rules(df, [{"rule_id": "r1", "rule_type": "not_null", "column": "order_id", "severity": "critical"}], "orders", "silver.orders", engine="pandas")
    assert result["summary"]["total_rules"] == 1


def test_critical_unsupported_rule_fails_closed():
    df = pd.DataFrame([{"order_id": 1}])
    result = run_dq_rules(df, [{"rule_id": "bad", "rule_type": "typo_rule", "severity": "critical"}], "orders", "silver.orders", engine="pandas", fail_on="none")
    assert result["can_continue"] is False


def test_warning_unsupported_rule_does_not_block():
    df = pd.DataFrame([{"order_id": 1}])
    result = run_dq_rules(df, [{"rule_id": "warn", "rule_type": "typo_rule", "severity": "warning"}], "orders", "silver.orders", engine="pandas", fail_on="none")
    assert result["can_continue"] is True


def test_run_dq_workflow_uses_explicit_rules():
    df = pd.DataFrame([{"order_id": 1}, {"order_id": None}])
    spark = _FakeSpark(df)
    qc = {"rules": [{"rule_id": "r1", "rule_type": "not_null", "column": "order_id", "severity": "critical"}], "fail_on": "critical"}
    out = run_dq_workflow(spark, df, qc, "orders", "silver.orders", engine="pandas")
    assert out["enforceable_rule_count"] == 1


def test_run_dq_workflow_loads_store_rules():
    df = pd.DataFrame([{"order_id": 1}])
    spark = _FakeSpark(df)
    spark.tables["meta.dq_rules"] = pd.DataFrame([
        {"dataset_name": "orders", "table_name": "silver.orders", "status": "approved", "rule_json": '{"rule_id":"store1","rule_type":"not_null","column":"order_id","severity":"critical"}'}
    ])
    qc = {"rules": [], "use_rule_store": True, "rule_store_table": "meta.dq_rules", "rule_status": "approved", "fail_on": "critical"}
    out = run_dq_workflow(spark, df, qc, "orders", "silver.orders", engine="pandas")
    assert len(out["loaded_rules"]) == 1


def test_run_dq_workflow_stores_candidates_when_enabled():
    df = pd.DataFrame([{"order_id": 1}])
    spark = _FakeSpark(df)
    profile = {"row_count": 1, "columns": [{"column_name": "order_id", "null_count": 0, "distinct_count": 1}]}
    qc = {"rules": [], "generate_candidates": True, "rule_store_table": "meta.dq_rules", "fail_on": "critical"}
    out = run_dq_workflow(spark, df, qc, "orders", "silver.orders", profile=profile, engine="pandas")
    assert out["stored_candidate_records"]




def test_run_dq_workflow_fabric_ai_stores_candidates_not_enforced(monkeypatch):
    df = pd.DataFrame([{"order_id": 1}])
    spark = _FakeSpark(df)
    response = '[{"rule_id":"ai_not_null","column":"order_id","rule_type":"not_null","severity":"warning","layman_rule":"rule","rule_config":{}}]'

    monkeypatch.setattr(pd.DataFrame, "ai", property(lambda self: _FakeAI(response)), raising=False)
    qc = {"rules": [], "generate_candidates": True, "candidate_generation_method": "fabric_ai", "rule_store_table": "meta.dq_rules", "fail_on": "critical"}
    out = run_dq_workflow(spark, df, qc, "orders", "silver.orders", profile={"columns": []}, engine="pandas")
    assert out["stored_candidate_records"]
    assert out["enforceable_rule_count"] == 0

def test_run_data_product_accepts_direct_quality_rules():
    source_df = pd.DataFrame([{"order_id": 1, "updated_at": "2026-01-01T00:00:00Z", "order_date": "2026-01-01"}])
    spark = _FakeSpark(source_df)
    contract = {
        "dataset": {"name": "orders", "description": "d", "owner": "o", "approved_usage": "a"},
        "source": {"table": "bronze.orders"},
        "target": {"table": "silver.orders"},
        "metadata": {"source_profile_table": "m.sp", "output_profile_table": "m.op", "schema_snapshot_table": "m.ss", "partition_snapshot_table": "m.ps", "quality_result_table": "m.qr", "quarantine_table": "m.qq", "contract_validation_table": "m.cv", "lineage_table": "m.li", "run_summary_table": "m.rs", "dataset_runs_table": "m.dr"},
        "quality": {"rules": [{"rule_id": "r1", "rule_type": "not_null", "column": "order_id", "severity": "critical"}]},
        "keys": {"business_keys": ["order_id"]},
    }
    result = run_data_product(spark=spark, contract=contract, source_df=source_df)
    assert "quality_result" in result




def test_run_dq_workflow_fails_closed_on_unsupported_critical_rule():
    df = pd.DataFrame([{"order_id": 1}])
    spark = _FakeSpark(df)
    qc = {"rules": [{"rule_id": "bad", "rule_type": "typo_rule", "severity": "critical"}], "fail_on": "critical"}
    out = run_dq_workflow(spark, df, qc, "orders", "silver.orders", engine="pandas")
    assert out["quality_result"]["can_continue"] is False
    assert out["gate_passed"] is False


def test_run_data_product_fails_closed_on_unsupported_critical_rule():
    source_df = pd.DataFrame([{"order_id": 1, "updated_at": "2026-01-01T00:00:00Z", "order_date": "2026-01-01"}])
    spark = _FakeSpark(source_df)
    contract = {
        "dataset": {"name": "orders", "description": "d", "owner": "o", "approved_usage": "a"},
        "source": {"table": "bronze.orders"},
        "target": {"table": "silver.orders"},
        "metadata": {"source_profile_table": "m.sp", "output_profile_table": "m.op", "schema_snapshot_table": "m.ss", "partition_snapshot_table": "m.ps", "quality_result_table": "m.qr", "quarantine_table": "m.qq", "contract_validation_table": "m.cv", "lineage_table": "m.li", "run_summary_table": "m.rs", "dataset_runs_table": "m.dr"},
        "quality": {"rules": [{"rule_id": "bad", "rule_type": "typo_rule", "severity": "critical"}], "fail_on": "critical"},
        "keys": {"business_keys": ["order_id"]},
    }
    result = run_data_product(spark=spark, contract=contract, source_df=source_df)
    assert result["status"] == "failed"

def test_store_and_load_dq_rules_roundtrip():
    df = pd.DataFrame([{"x": 1}])
    spark = _FakeSpark(df)
    store_dq_rules(spark, [{"rule_id": "r1", "rule_type": "not_null", "column": "x"}], "meta.dq_rules", dataset_name="orders", source_table="silver.orders")
    loaded = load_dq_rules(spark, "meta.dq_rules", dataset_name="orders", source_table="silver.orders", status="candidate")
    assert loaded[0]["rule_id"] == "r1"


def test_store_and_load_dq_rules_roundtrip_approved_status():
    df = pd.DataFrame([{"x": 1}])
    spark = _FakeSpark(df)
    store_dq_rules(spark, [{"rule_id": "r2", "rule_type": "not_null", "column": "x"}], "meta.dq_rules", dataset_name="orders", source_table="silver.orders", status="approved")
    loaded = load_dq_rules(spark, "meta.dq_rules", dataset_name="orders", source_table="silver.orders", status="approved")
    assert loaded[0]["rule_id"] == "r2"
    assert loaded[0]["status"] == "approved"
