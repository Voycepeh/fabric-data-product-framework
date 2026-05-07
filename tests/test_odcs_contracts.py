from pathlib import Path

import pytest

from fabricops_kit.contracts import (
    extract_business_keys,
    extract_classifications,
    extract_optional_columns,
    extract_required_columns,
    load_odcs_contract,
    map_odcs_quality_rules_to_fabricops_rules,
    validate_odcs_contract,
)


EXAMPLE_PATH = Path("templates/contracts/odcs_source_input_contract_example.yaml")


def test_load_odcs_contract_loads_example_yaml():
    contract = load_odcs_contract(EXAMPLE_PATH)
    assert contract["kind"] == "DataContract"


def test_validate_odcs_contract_passes_for_example():
    contract = load_odcs_contract(EXAMPLE_PATH)
    assert validate_odcs_contract(contract) == []


def test_extract_required_and_optional_columns():
    contract = load_odcs_contract(EXAMPLE_PATH)
    assert extract_required_columns(contract, "raw_student_events") == ["student_id", "event_id", "event_timestamp", "event_type"]
    assert extract_optional_columns(contract, "raw_student_events") == ["event_description"]


def test_extract_business_keys_and_classifications():
    contract = load_odcs_contract(EXAMPLE_PATH)
    assert extract_business_keys(contract, "raw_student_events") == ["event_id"]
    classifications = extract_classifications(contract, "raw_student_events")
    assert classifications["student_id"] == "confidential"
    assert classifications["event_id"] == "internal"


def test_map_quality_rules_and_skip_unsupported_rule():
    contract = load_odcs_contract(EXAMPLE_PATH)
    contract["quality"].append({"name": "raw_sql", "type": "sql", "rule": "sql", "object": "raw_student_events"})
    mapped = map_odcs_quality_rules_to_fabricops_rules(contract, "raw_student_events")
    rule_types = [r.get("rule_type") for r in mapped if not r.get("skipped")]
    assert "not_null" in rule_types
    assert "unique" in rule_types
    assert "accepted_values" in rule_types
    assert "row_count_min" in rule_types
    assert any(item.get("skipped") for item in mapped)


def test_missing_object_raises_clear_error():
    contract = load_odcs_contract(EXAMPLE_PATH)
    with pytest.raises(ValueError, match="not found"):
        extract_required_columns(contract, "missing_table")


def test_invalid_contract_returns_validation_errors():
    bad_contract = {"kind": "WrongKind", "schema": {}}
    errors = validate_odcs_contract(bad_contract)
    assert any("kind must be DataContract" in err for err in errors)
    assert any("apiVersion is required" in err for err in errors)
    assert any("schema must be a list" in err for err in errors)
