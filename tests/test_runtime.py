import json

import pytest

from fabric_data_product_framework.runtime import (
    NotebookNamingError,
    assert_notebook_name_valid,
    build_runtime_context,
    generate_run_id,
    validate_notebook_name,
)


def test_validate_notebook_name_allows_expected_prefix():
    errors = validate_notebook_name(
        "source_to_product_synthetic_orders",
        allowed_prefixes=["source_to_product_", "bronze_to_silver_"],
    )
    assert errors == []


def test_validate_notebook_name_rejects_disallowed_prefix():
    errors = validate_notebook_name(
        "adhoc_orders_pipeline",
        allowed_prefixes=["source_to_product_", "bronze_to_silver_"],
    )
    assert errors
    assert "must start with one of" in errors[0]


def test_assert_notebook_name_valid_raises_for_invalid_name():
    with pytest.raises(NotebookNamingError):
        assert_notebook_name_valid("Bad Name", allowed_prefixes=["source_to_product_"])


def test_generate_run_id_returns_unique_values():
    one = generate_run_id()
    two = generate_run_id()
    assert one != two
    assert one.startswith("run_")


def test_build_runtime_context_returns_expected_json_safe_keys():
    context = build_runtime_context(
        dataset_name="synthetic_orders",
        environment="dev",
        source_table="source.synthetic_orders",
        target_table="product.synthetic_orders",
        notebook_name="source_to_product_synthetic_orders",
        run_id="run_20260101T000000Z_deadbeef",
    )

    assert set(context.keys()) == {
        "dataset_name",
        "environment",
        "source_table",
        "target_table",
        "notebook_name",
        "run_id",
        "started_at_utc",
    }
    json.dumps(context)


def test_build_runtime_context_generates_run_id_using_dataset_prefix():
    context = build_runtime_context(
        dataset_name="Synthetic Orders",
        environment="dev",
        source_table="source.synthetic_orders",
        target_table="product.synthetic_orders",
    )
    assert context["run_id"].startswith("synthetic_orders_")
