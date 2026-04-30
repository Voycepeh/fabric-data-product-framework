import json

from fabric_data_product_framework.governance_classifier import (
    build_governance_classification_records,
    classify_column,
    classify_columns,
    summarize_governance_classifications,
    write_governance_classifications,
)


def test_classify_column_contact_email():
    r = classify_column("customer_email")
    assert r["suggested_classification"] == "contact"


def test_classify_column_identifier_staff_id():
    r = classify_column("staff_id")
    assert r["suggested_classification"] == "identifier"


def test_classify_column_personal_data_name():
    r = classify_column("full_name")
    assert r["suggested_classification"] == "personal_data"


def test_classify_column_financial_salary():
    r = classify_column("base_salary")
    assert r["suggested_classification"] == "financial"


def test_classify_column_health_diagnosis():
    r = classify_column("diagnosis_code")
    assert r["suggested_classification"] == "health"


def test_classify_column_sensitive_free_text_comments():
    r = classify_column("comments", profile={"avg_length": 200})
    assert r["suggested_classification"] == "sensitive_free_text"
    assert r["confidence"] >= 0.8


def test_classify_column_unknown_fallback():
    r = classify_column("x1")
    assert r["suggested_classification"] == "unknown"


def test_custom_rules_override_defaults():
    r = classify_column(
        "employee_id",
        rules=[
            {
                "rule_id": "custom_emp",
                "classification": "identifier",
                "action": "restrict_access",
                "patterns": ["employee_id"],
                "confidence": 0.99,
                "reason": "custom",
            }
        ],
    )
    assert r["confidence"] == 0.99
    assert "custom_emp" in r["evidence"]["matched_rule_ids"]


def test_classify_columns_profile_dict_columns():
    p = {"columns": [{"column_name": "email", "data_type": "string"}, {"column_name": "salary", "data_type": "double"}]}
    rows = classify_columns(p)
    assert len(rows) == 2


def test_classify_columns_flattened_records_shape():
    p = [{"COLUMN_NAME": "staff_id", "data_type": "string"}, {"name": "notes", "dtype": "string"}]
    rows = classify_columns(p)
    assert {r["column_name"] for r in rows} == {"staff_id", "notes"}


def test_build_records_json_safe():
    c = [classify_column("email")]
    rows = build_governance_classification_records(c, dataset_name="d", table_name="t", run_id="r1")
    assert rows[0]["status"] == "suggested"
    assert json.loads(rows[0]["evidence_json"]) is not None
    assert json.loads(rows[0]["classification_json"])["column_name"] == "email"


def test_summarize_counts():
    rows = [classify_column("email"), classify_column("staff_id"), classify_column("x")]
    s = summarize_governance_classifications(rows)
    assert s["total_columns"] == 3
    assert s["unknown_count"] == 1
    assert s["review_required_count"] >= 2


def test_write_governance_classifications_with_fake_spark():
    captured = {}

    class FakeWriter:
        def __init__(self):
            self.mode_name = None

        def mode(self, m):
            self.mode_name = m
            return self

        def saveAsTable(self, t):
            captured["table"] = t

    class FakeDF:
        def __init__(self):
            self.write = FakeWriter()

    class FakeSpark:
        def createDataFrame(self, rows):
            captured["rows"] = rows
            return FakeDF()

    recs = write_governance_classifications(
        spark=FakeSpark(),
        classifications=[classify_column("email")],
        table_name="fw_metadata.governance_classifications",
        dataset_name="d",
        source_table="s",
    )
    assert recs
    assert captured["table"] == "fw_metadata.governance_classifications"
    assert captured["rows"][0]["column_name"] == "email"
