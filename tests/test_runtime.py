import json

import pytest

from fabricops_kit.runtime import (
    NotebookNamingError,
    assert_notebook_name_valid,
    build_runtime_context,
    generate_run_id,
    validate_notebook_name,
)


def test_validate_notebook_name_allows_finalized_model_names():
    errors = validate_notebook_name("03_pc_email_metadata_source_to_unified")
    assert errors == []


def test_validate_notebook_name_rejects_non_model_name():
    errors = validate_notebook_name("adhoc_orders_pipeline")
    assert errors
    assert "must follow one of" in errors[0]


def test_assert_notebook_name_valid_raises_for_invalid_name():
    with pytest.raises(NotebookNamingError):
        assert_notebook_name_valid("Bad Name")


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
        notebook_name="03_pc_synthetic_orders_source_to_product",
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


def test_validate_notebook_name_reads_prefixes_from_framework_config():
    from fabricops_kit.config import (
        AIPromptConfig,
        FrameworkConfig,
        GovernanceConfig,
        LineageConfig,
        NotebookRuntimeConfig,
        PathConfig,
        QualityConfig,
    )
    from fabricops_kit.fabric_io import Housepath

    config = FrameworkConfig(
        path_config=PathConfig({"Sandbox": {"Source": Housepath("w", "h", "n", "abfss://x")}}),
        notebook_runtime_config=NotebookRuntimeConfig(["custom_"]),
        ai_prompt_config=AIPromptConfig(dq_rule_candidate_template="a", governance_candidate_template="b", handover_summary_template="c"),
        quality_config=QualityConfig(),
        governance_config=GovernanceConfig(),
        lineage_config=LineageConfig(),
    )

    assert validate_notebook_name("custom_pipeline", config=config) == []
    assert validate_notebook_name("03_pc_email_metadata_source_to_unified", config=config)
