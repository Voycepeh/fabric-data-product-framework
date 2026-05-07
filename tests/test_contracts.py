import json

from fabricops_kit.contracts import (
    build_contract_column_records,
    build_contract_header_record,
    build_contract_records,
    build_contract_rule_records,
    build_contract_summary,
    extract_business_keys,
    extract_classifications,
    extract_quality_rules,
    extract_required_columns,
    normalize_contract_dict,
    validate_contract_dict,
)


def _valid_contract():
    return {
        "contract_id": "student_events_source_input_v1",
        "contract_type": "source_input",
        "dataset_name": "student_events",
        "object_name": "raw_student_events",
        "version": "1.0.0",
        "status": "approved",
        "required_columns": ["student_id", "event_id"],
        "optional_columns": ["event_description"],
        "business_keys": ["event_id"],
        "classifications": {"student_id": "confidential", "event_id": "internal"},
        "quality_rules": [{"rule_id": "event_id_not_null", "rule_type": "not_null", "column": "event_id", "severity": "critical"}],
    }


def test_normalize_contract_dict_fills_defaults():
    normalized = normalize_contract_dict({"contract_id": "c1"})
    assert normalized["required_columns"] == []
    assert normalized["classifications"] == {}
    assert normalized["quality_rules"] == []


def test_validate_contract_dict_valid_contract():
    assert validate_contract_dict(_valid_contract()) == []


def test_validate_contract_dict_missing_fields():
    errors = validate_contract_dict({"contract_type": "source_input", "dataset_name": "x", "version": "1", "status": "draft"})
    assert any("contract_id" in err for err in errors)
    assert any("object_name" in err for err in errors)


def test_build_contract_header_record_includes_contract_json():
    row = build_contract_header_record(_valid_contract())
    parsed = json.loads(row["contract_json"])
    assert parsed["contract_id"] == "student_events_source_input_v1"


def test_build_contract_column_records_required_and_business_keys():
    rows = build_contract_column_records(_valid_contract())
    event_id = next(r for r in rows if r["column_name"] == "event_id")
    optional = next(r for r in rows if r["column_name"] == "event_description")
    assert event_id["required"] is True
    assert event_id["business_key"] is True
    assert optional["required"] is False


def test_build_contract_rule_records_stores_rule_json():
    rows = build_contract_rule_records(_valid_contract())
    assert rows[0]["rule_id"] == "event_id_not_null"
    assert json.loads(rows[0]["rule_json"])["rule_type"] == "not_null"


def test_build_contract_records_groups_outputs():
    records = build_contract_records(_valid_contract())
    assert set(records.keys()) == {"contracts", "columns", "rules"}


def test_extractors_and_summary():
    contract = _valid_contract()
    assert extract_required_columns(contract) == ["student_id", "event_id"]
    assert extract_business_keys(contract) == ["event_id"]
    assert extract_classifications(contract) == {"student_id": "confidential", "event_id": "internal"}
    assert extract_quality_rules(contract)[0]["rule_id"] == "event_id_not_null"
    summary = build_contract_summary(contract)
    assert summary["required_column_count"] == 2
    assert summary["quality_rule_count"] == 1
