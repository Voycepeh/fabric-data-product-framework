import pandas as pd

from fabric_data_product_framework.quality import (
    build_quarantine_rule_coverage_records,
    build_quarantine_summary_records,
)
from fabric_data_product_framework.quality import (
    build_rule_registry_records,
    compile_layman_rules_to_quality_rules,
)


def test_compile_many_and_registry_records():
    candidates = [{"rule_id": "R1", "rule_type": "not_null", "column": "id"}, {"rule_id": "R2", "rule_type": "unsupported", "layman_rule": "x"}]
    out = compile_layman_rules_to_quality_rules(candidates)
    assert out["summary"]["compiled"] == 1
    assert out["summary"]["skipped"] == 1
    assert out["records"][1]["can_compile"] is False
    records = build_rule_registry_records(out["compiled_rules"], "run1", "ds", "tbl")
    assert records[0]["rule_id"] == "R1"


def test_build_quarantine_summary_records_pandas():
    df = pd.DataFrame({"a": [1, 2], "dq_errors": [["x"], []], "dq_warnings": [[], []]})
    qdf = df[df["dq_errors"].map(bool)].copy()
    rows = build_quarantine_summary_records(qdf, "run1", "ds", "tbl", engine="pandas")
    assert rows[0]["quarantine_row_count"] == 1


def test_aggregate_only_rules_exposed_in_coverage_records():
    rules = [{"rule_id": "A1", "rule_type": "row_count_min"}, {"rule_id": "A2", "rule_type": "freshness_check"}, {"rule_id": "A3", "rule_type": "unsupported"}]
    rows = build_quarantine_rule_coverage_records(rules, "run1", "ds", "tbl")
    statuses = {r["rule_id"]: r["coverage_status"] for r in rows}
    assert statuses["A1"] == "aggregate_only"
    assert statuses["A2"] == "aggregate_only"
    assert statuses["A3"] == "unsupported"
