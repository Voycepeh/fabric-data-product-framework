import pandas as pd

from fabric_data_product_framework.profiling import (
    build_ai_quality_context,
    default_technical_columns,
    flatten_profile_for_metadata,
    get_profiled_columns,
    is_min_max_supported_type,
    profile_metadata_to_records,
    profile_dataframe,
    summarize_profile,
)


class FakeDTypesDataFrame:
    def __init__(self, dtypes):
        self.dtypes = dtypes


class FakeRow(dict):
    def asDict(self):
        return dict(self)


class FakeProfileDF:
    def __init__(self, rows):
        self._rows = rows

    def collect(self):
        return self._rows


def test_default_technical_columns_contains_required_values():
    cols = set(default_technical_columns())
    for required in {"pipeline_ts", "_pipeline_run_id", "loaded_at", "run_ingest_id", "ingest_run_id"}:
        assert required in cols


def test_get_profiled_columns_excludes_default_and_custom():
    df = FakeDTypesDataFrame([
        ("id", "int"),
        ("pipeline_ts", "timestamp"),
        ("status", "string"),
        ("custom_tech", "string"),
    ])
    assert get_profiled_columns(df, exclude_columns={"custom_tech"}) == ["id", "status"]


def test_is_min_max_supported_type():
    assert is_min_max_supported_type("int")
    assert is_min_max_supported_type("timestamp")
    assert is_min_max_supported_type("string")
    assert not is_min_max_supported_type("array<string>")
    assert not is_min_max_supported_type("struct<a:int>")


def test_profile_metadata_to_records_collects_as_dict_rows():
    profile_df = FakeProfileDF([FakeRow(COLUMN_NAME="id", ROW_COUNT=3), FakeRow(COLUMN_NAME="status", ROW_COUNT=3)])
    rows = profile_metadata_to_records(profile_df)
    assert rows[0]["COLUMN_NAME"] == "id"
    assert rows[1]["COLUMN_NAME"] == "status"


def test_build_ai_quality_context_returns_expected_sections():
    profile_df = FakeProfileDF([
        FakeRow(COLUMN_NAME="order_id", DATA_TYPE="string", ROW_COUNT=100, NULL_COUNT=0, NULL_PERCENT=0.0, DISTINCT_COUNT=100, DISTINCT_PERCENT=100.0, MIN_VALUE="1", MAX_VALUE="100"),
        FakeRow(COLUMN_NAME="order_status", DATA_TYPE="string", ROW_COUNT=100, NULL_COUNT=2, NULL_PERCENT=2.0, DISTINCT_COUNT=3, DISTINCT_PERCENT=3.0, MIN_VALUE="OPEN", MAX_VALUE="CLOSED"),
        FakeRow(COLUMN_NAME="event_timestamp", DATA_TYPE="timestamp", ROW_COUNT=100, NULL_COUNT=0, NULL_PERCENT=0.0, DISTINCT_COUNT=95, DISTINCT_PERCENT=95.0, MIN_VALUE="2026-01-01", MAX_VALUE="2026-01-31"),
    ])
    context = build_ai_quality_context(profile_df, dataset_name="orders", table_name="orders_clean")
    assert context["dataset_name"] == "orders"
    assert context["table_name"] == "orders_clean"
    assert context["row_count"] == 100
    assert len(context["column_profiles"]) == 3
    assert context["column_count"] == 3
    assert "order_status" in context["columns_with_nulls"]
    hints = {(h["column"], h["hint"]) for h in context["candidate_rule_hints"]}
    assert ("order_id", "UNIQUE_CANDIDATE") in hints
    assert ("order_status", "ACCEPTED_VALUES_CANDIDATE") in hints
    assert ("event_timestamp", "DATE_RANGE_CANDIDATE") in hints


def test_legacy_profile_dataframe_supports_pandas():
    pdf = pd.DataFrame([{"id": 1, "status": "OPEN"}, {"id": 2, "status": "CLOSED"}])
    profile = profile_dataframe(pdf, dataset_name="orders")
    assert profile["dataset_name"] == "orders"
    assert profile["engine"] == "pandas"
    assert profile["row_count"] == 2

    profile_auto = profile_dataframe(
        pdf,
        dataset_name="orders",
        engine="auto",
    )
    assert profile_auto["engine"] == "pandas"
    assert profile_auto["row_count"] == 2
    try:
        summarize_profile({})
    except NotImplementedError as exc:
        assert "build_ai_quality_context" in str(exc)
    else:
        raise AssertionError("Expected NotImplementedError")


def test_flatten_profile_for_metadata_preserves_falsey_lowercase_values():
    profile = {
        "row_count": 2,
        "generated_at": "2026-01-01T00:00:00",
        "columns": [
            {
                "column_name": "amount",
                "data_type": "int64",
                "null_count": 0,
                "null_pct": 0.0,
                "distinct_count": 1,
                "distinct_pct": 50.0,
                "min_value": 0,
                "max_value": 0,
            }
        ],
    }
    rows = flatten_profile_for_metadata(profile, "orders", "r1", "source")
    assert len(rows) == 1
    assert rows[0]["null_count"] == 0
    assert rows[0]["null_pct"] == 0.0
    assert rows[0]["min_value"] == 0
    assert rows[0]["max_value"] == 0


def test_flatten_profile_for_metadata_supports_uppercase_and_exclude_columns():
    profile = {
        "row_count": 3,
        "columns": [
            {
                "COLUMN_NAME": "id",
                "DATA_TYPE": "int",
                "NULL_COUNT": 0,
                "NULL_PERCENT": 0.0,
                "DISTINCT_COUNT": 3,
                "DISTINCT_PERCENT": 100.0,
                "MIN_VALUE": 1,
                "MAX_VALUE": 3,
            },
            {"COLUMN_NAME": "ignore_me", "DATA_TYPE": "string"},
        ],
    }
    rows = flatten_profile_for_metadata(profile, "orders", "r2", "output", exclude_columns={"ignore_me"})
    assert len(rows) == 1
    assert rows[0]["column_name"] == "id"
    assert rows[0]["null_count"] == 0
    assert rows[0]["null_pct"] == 0.0
    assert rows[0]["min_value"] == 1
    assert rows[0]["max_value"] == 3
