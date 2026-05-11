from fabricops_kit import data_quality as dq


class _Spark:
    pass


def test_write_dq_rules_writes_history_payload(monkeypatch):
    written = {}

    monkeypatch.setattr(dq.SparkSession, "getActiveSession", staticmethod(lambda: _Spark()))

    def _fake_build(spark, table_name, approved_rules, **kwargs):
        assert table_name == "T"
        assert approved_rules == [{"rule_id": "r1", "rule_type": "not_null", "columns": ["c"], "severity": "error", "description": "d"}]
        return "history_df"

    def _fake_write(df, metadata_path, tablename, mode="append"):
        written["df"] = df
        written["metadata_path"] = metadata_path
        written["tablename"] = tablename
        written["mode"] = mode

    monkeypatch.setattr(dq, "build_dq_rule_history", _fake_build)
    monkeypatch.setattr(dq, "lakehouse_table_write", _fake_write)

    out = dq.write_dq_rules(
        [{"rule_id": "r1", "rule_type": "not_null", "columns": ["c"], "severity": "error", "description": "d"}],
        table_name="T",
        metadata_path="LH",
    )
    assert out == "history_df"
    assert written == {"df": "history_df", "metadata_path": "LH", "tablename": "METADATA_DQ_RULES", "mode": "append"}
