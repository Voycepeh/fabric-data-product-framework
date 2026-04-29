import pandas as pd

from fabric_data_product_framework.quarantine import build_quarantine_summary_records
from fabric_data_product_framework.rule_compiler import (
    build_rule_registry_records,
    compile_layman_rules_to_quality_rules,
)


def test_compile_many_and_registry_records():
    candidates = [
        {"rule_id": "R1", "rule_type": "not_null", "column": "id"},
        {"rule_id": "R2", "rule_type": "unsupported"},
    ]
    out = compile_layman_rules_to_quality_rules(candidates)
    assert out["summary"]["compiled"] == 1
    assert out["summary"]["skipped"] == 1
    records = build_rule_registry_records(out["compiled_rules"], "run1", "ds", "tbl")
    assert records[0]["rule_id"] == "R1"


def test_build_quarantine_summary_records_pandas():
    df = pd.DataFrame({"a": [1, 2], "dq_errors": [["x"], []], "dq_warnings": [[], []]})
    qdf = df[df["dq_errors"].map(bool)].copy()
    rows = build_quarantine_summary_records(qdf, "run1", "ds", "tbl", engine="pandas")
    assert rows[0]["quarantine_row_count"] == 1
