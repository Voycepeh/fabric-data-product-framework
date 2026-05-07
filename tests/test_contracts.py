import json

from fabricops_kit import contracts


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
    normalized = contracts.normalize_contract_dict({"contract_id": "c1"})
    assert normalized["required_columns"] == []
    assert normalized["classifications"] == {}
    assert normalized["quality_rules"] == []


def test_validate_contract_dict_valid_contract():
    assert contracts.validate_contract_dict(_valid_contract()) == []


def test_validate_contract_dict_missing_fields():
    errors = contracts.validate_contract_dict({"contract_type": "source_input", "dataset_name": "x", "version": "1", "status": "draft"})
    assert any("contract_id" in err for err in errors)
    assert any("object_name" in err for err in errors)


def test_validate_contract_dict_rejects_string_required_columns():
    invalid = _valid_contract()
    invalid["required_columns"] = "event_id"
    errors = contracts.validate_contract_dict(invalid)
    assert any("required_columns must be a list" in err for err in errors)


def test_build_contract_header_record_includes_contract_json_and_preserves_approved_at():
    contract = _valid_contract()
    contract["approved_at_utc"] = "2026-01-01T00:00:00+00:00"
    row = contracts.build_contract_header_record(contract)
    parsed = json.loads(row["contract_json"])
    assert parsed["contract_id"] == "student_events_source_input_v1"
    assert row["approved_at_utc"] == "2026-01-01T00:00:00+00:00"


def test_build_contract_column_records_required_and_business_keys():
    rows = contracts.build_contract_column_records(_valid_contract())
    event_id = next(r for r in rows if r["column_name"] == "event_id")
    optional = next(r for r in rows if r["column_name"] == "event_description")
    assert event_id["required"] is True
    assert event_id["business_key"] is True
    assert optional["required"] is False


def test_build_contract_rule_records_stores_rule_json():
    rows = contracts.build_contract_rule_records(_valid_contract())
    assert rows[0]["rule_id"] == "event_id_not_null"
    assert json.loads(rows[0]["rule_json"])["rule_type"] == "not_null"


def test_build_contract_records_groups_outputs():
    records = contracts.build_contract_records(_valid_contract())
    assert set(records.keys()) == {"contracts", "columns", "rules"}


def test_extractors_and_summary():
    contract = _valid_contract()
    assert contracts.extract_required_columns(contract) == ["student_id", "event_id"]
    assert contracts.extract_business_keys(contract) == ["event_id"]
    assert contracts.extract_classifications(contract) == {"student_id": "confidential", "event_id": "internal"}
    assert contracts.extract_quality_rules(contract)[0]["rule_id"] == "event_id_not_null"
    summary = contracts.build_contract_summary(contract)
    assert summary["required_column_count"] == 2
    assert summary["quality_rule_count"] == 1


def test_write_contract_to_lakehouse_uses_df_and_expected_signature(monkeypatch):
    calls = []

    monkeypatch.setattr(contracts, "contract_records_to_spark", lambda rows, schema_name=None: {"rows": rows})

    def fake_write(df, metadata_path, table_name, mode="append"):
        calls.append((df, metadata_path, table_name, mode))

    monkeypatch.setattr(contracts, "lakehouse_table_write", fake_write)
    metadata_path = object()
    contracts.write_contract_to_lakehouse(_valid_contract(), metadata_path, mode="append")

    assert len(calls) == 3
    assert [c[2] for c in calls] == ["FABRICOPS_CONTRACTS", "FABRICOPS_CONTRACT_COLUMNS", "FABRICOPS_CONTRACT_RULES"]
    assert all(c[1] is metadata_path for c in calls)


class _Row:
    def __init__(self, data):
        self._data = data

    def asDict(self, recursive=True):
        return dict(self._data)


class _SparkLikeFrame:
    def __init__(self, rows):
        self._rows = rows

    def collect(self):
        return [_Row(r) for r in self._rows]


def test_load_latest_approved_contract_from_spark_like_rows(monkeypatch):
    contract = _valid_contract()
    row = contracts.build_contract_header_record(contract)

    monkeypatch.setattr(contracts, "lakehouse_table_read", lambda metadata_path, table_name: _SparkLikeFrame([row]))

    loaded = contracts.load_latest_approved_contract(object(), "student_events", "raw_student_events", "source_input")
    assert loaded["contract_id"] == contract["contract_id"]


def test_load_latest_approved_contract_from_record_list(monkeypatch):
    contract = _valid_contract()
    row = contracts.build_contract_header_record(contract)

    monkeypatch.setattr(contracts, "lakehouse_table_read", lambda metadata_path, table_name: [row])

    loaded = contracts.load_latest_approved_contract(object(), "student_events", "raw_student_events", "source_input")
    assert loaded["version"] == "1.0.0"


def test_no_metadata_path_table_usage_regression(monkeypatch):
    class MetadataPath:
        def table(self, *_args, **_kwargs):
            raise AssertionError("metadata_path.table should not be called")

    contract = _valid_contract()
    row = contracts.build_contract_header_record(contract)

    monkeypatch.setattr(contracts, "contract_records_to_spark", lambda rows, schema_name=None: rows)
    monkeypatch.setattr(contracts, "lakehouse_table_write", lambda df, metadata_path, table_name, mode="append": None)
    monkeypatch.setattr(contracts, "lakehouse_table_read", lambda metadata_path, table_name: [row])

    metadata_path = MetadataPath()
    contracts.write_contract_to_lakehouse(contract, metadata_path)
    loaded = contracts.load_contract_from_lakehouse(metadata_path, contract_id=contract["contract_id"], version=contract["version"])
    assert loaded["contract_id"] == contract["contract_id"]
