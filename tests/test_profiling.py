import json

import pandas as pd

from fabric_data_product_framework.profiling import (
    profile_column,
    profile_dataframe,
    summarize_profile,
    to_jsonable,
)


def test_profile_dataframe_counts_and_duplicates():
    df = pd.DataFrame({"a": [1, 1, 2], "b": ["x", "x", "y"]})
    prof = profile_dataframe(df, dataset_name="synthetic")
    assert prof["dataset_name"] == "synthetic"
    assert prof["row_count"] == 3
    assert prof["column_count"] == 2
    assert prof["duplicate_row_count"] == 1


def test_profile_column_null_and_distinct():
    s = pd.Series([1, None, 1, 2], name="x")
    prof = profile_column(s)
    assert prof["null_count"] == 1
    assert prof["distinct_count"] == 2


def test_numeric_column_stats():
    s = pd.Series([10.0, 20.0, 30.0], name="amount")
    prof = profile_column(s)
    assert prof["min_value"] == 10.0
    assert prof["max_value"] == 30.0
    assert prof["mean_value"] == 20.0
    assert prof["median_value"] == 20.0
    assert prof["std_value"] is not None


def test_date_column_min_max():
    s = pd.Series(pd.to_datetime(["2024-01-01", "2024-01-03"]), name="event_date")
    prof = profile_column(s)
    assert prof["min_value"].startswith("2024-01-01")
    assert prof["max_value"].startswith("2024-01-03")


def test_categorical_top_values():
    s = pd.Series(["A", "A", "B", "C"], name="segment")
    prof = profile_column(s, top_n=2)
    assert len(prof["top_values"]) == 2
    assert prof["top_values"][0]["value"] == "A"


def test_semantic_inference_rules():
    email_prof = profile_column(pd.Series(["a@example.com", "b@example.com"], name="email"))
    id_prof = profile_column(pd.Series(["c1", "c2"], name="customer_id"))
    amount_prof = profile_column(pd.Series([10.5, 20.5], name="amount"))

    assert email_prof["inferred_semantic_type"] == "email"
    assert id_prof["inferred_semantic_type"] == "identifier"
    assert amount_prof["inferred_semantic_type"] == "amount"


def test_profile_is_json_serializable():
    df = pd.DataFrame({"customer_id": [1, 2], "created_at": pd.to_datetime(["2024-01-01", "2024-01-02"])})
    prof = profile_dataframe(df)
    json.dumps(prof)


def test_summarize_profile_keys():
    df = pd.DataFrame({"customer_id": [1, 2, 2], "email": ["a@example.com", None, "b@example.com"]})
    prof = profile_dataframe(df)
    summary = summarize_profile(prof)
    expected = {
        "dataset_name",
        "row_count",
        "column_count",
        "duplicate_row_count",
        "columns_with_nulls",
        "likely_identifier_columns",
        "likely_date_columns",
        "likely_sensitive_columns",
        "generated_at",
    }
    assert expected.issubset(summary.keys())


def test_empty_dataframe_does_not_crash():
    df = pd.DataFrame()
    prof = profile_dataframe(df, dataset_name="empty")
    assert prof["dataset_name"] == "empty"
    assert prof["row_count"] == 0
    assert prof["column_count"] == 0
    assert prof["columns"] == []


def test_to_jsonable_list_with_timestamp():
    out = to_jsonable([1, None, pd.Timestamp("2024-01-01")])
    assert out == [1, None, "2024-01-01T00:00:00"]


def test_to_jsonable_nested_dict_with_pd_na_and_nan():
    out = to_jsonable({"a": pd.NA, "b": [1, float("nan")]})
    assert out == {"a": None, "b": [1, None]}


def test_profile_column_mixed_object_values_is_json_serializable():
    s = pd.Series([1, "x", pd.Timestamp("2024-01-01"), None], name="mixed_obj", dtype="object")
    prof = profile_column(s)
    json.dumps(prof)
