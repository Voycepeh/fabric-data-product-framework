import json

from fabric_data_product_framework.lineage import (
    LineageRecorder,
    build_lineage_prompt_context,
    build_lineage_records,
    build_transformation_summary_markdown,
    generate_mermaid_lineage,
    get_fabric_copilot_lineage_prompt,
    build_lineage_record_from_steps,
    plot_lineage_networkx,
    validate_lineage_steps,
)


def _sample_step(step_id: str = "T001") -> dict:
    return {
        "step_id": step_id,
        "step_name": "Filter active records",
        "input_name": "df_source",
        "output_name": "df_active",
        "description": "Keep only active records.",
        "reason": "Inactive records are excluded from reporting.",
        "transformation_type": "filter",
        "columns_used": ["status"],
        "columns_created": [],
        "business_impact": "Improves reporting relevance.",
        "notes": "Synthetic example.",
    }


def test_lineage_recorder_initializes_with_context() -> None:
    recorder = LineageRecorder("sales_dataset", run_id="run-001", source_tables=["src.sales"], target_table="curated.sales")
    summary = recorder.build_summary()
    assert summary["dataset_name"] == "sales_dataset"
    assert summary["run_id"] == "run-001"
    assert summary["source_tables"] == ["src.sales"]
    assert summary["target_table"] == "curated.sales"


def test_add_step_returns_json_safe_record() -> None:
    recorder = LineageRecorder("sales_dataset")
    step = recorder.add_step(**_sample_step())
    assert step["step_id"] == "T001"
    json.dumps(step)


def test_to_records_returns_all_steps() -> None:
    recorder = LineageRecorder("sales_dataset")
    recorder.add_step(**_sample_step("T001"))
    recorder.add_step(**_sample_step("T002"))
    assert len(recorder.to_records()) == 2


def test_build_summary_contains_rollups() -> None:
    recorder = LineageRecorder("sales_dataset", source_tables=["src.sales"], target_table="curated.sales")
    recorder.add_step(**_sample_step("T001"))
    recorder.add_step(**{**_sample_step("T002"), "columns_created": ["reporting_date"], "transformation_type": "derive_column"})
    summary = recorder.build_summary()
    assert summary["step_count"] == 2
    assert "status" in summary["columns_used"]
    assert "reporting_date" in summary["columns_created"]


def test_build_lineage_records_returns_row_per_step() -> None:
    steps = [_sample_step("T001"), _sample_step("T002")]
    records = build_lineage_records(dataset_name="sales_dataset", run_id="run-001", source_tables=["src.sales"], target_table="curated.sales", transformation_steps=steps)
    assert len(records) == 2
    assert records[0]["run_id"] == "run-001"


def test_generate_mermaid_lineage_returns_flowchart() -> None:
    mermaid = generate_mermaid_lineage(source_tables=["source.sales"], target_table="target.sales", transformation_steps=[_sample_step()])
    assert mermaid.startswith("flowchart LR")
    assert "-->" in mermaid


def test_generate_mermaid_lineage_uses_safe_node_ids() -> None:
    mermaid = generate_mermaid_lineage(source_tables=["source table.with spaces"], target_table="target-table", transformation_steps=[{**_sample_step(), "step_id": "T-001/#"}])
    assert " " not in [line.strip().split("[")[0] for line in mermaid.splitlines() if "[\"" in line]


def test_transformation_summary_markdown_includes_steps_and_reasons() -> None:
    recorder = LineageRecorder("sales_dataset", run_id="run-001", source_tables=["src.sales"], target_table="curated.sales")
    recorder.add_step(**_sample_step())
    markdown = build_transformation_summary_markdown(recorder.build_summary(), include_mermaid=False)
    assert "Transformation Summary" in markdown
    assert "Reason:" in markdown


def test_transformation_summary_markdown_includes_mermaid_block() -> None:
    recorder = LineageRecorder("sales_dataset", source_tables=["src.sales"], target_table="curated.sales")
    recorder.add_step(**_sample_step())
    markdown = build_transformation_summary_markdown(recorder.build_summary(), include_mermaid=True)
    assert "```mermaid" in markdown


def test_lineage_prompt_context_contains_instruction() -> None:
    context = build_lineage_prompt_context(dataset_name="sales_dataset", source_tables=["src.sales"], target_table="curated.sales", transformation_steps=[_sample_step()], eda_notes="Null checks passed.")
    assert "Do not invent transformations" in context


def test_empty_transformation_steps_do_not_crash() -> None:
    recorder = LineageRecorder("sales_dataset", source_tables=["src.sales"], target_table="curated.sales")
    summary = recorder.build_summary()
    markdown = build_transformation_summary_markdown(summary)
    mermaid = generate_mermaid_lineage(source_tables=["src.sales"], target_table="curated.sales", transformation_steps=[])
    assert summary["step_count"] == 0
    assert "No transformation steps recorded" in markdown
    assert mermaid.startswith("flowchart")


def test_lineage_outputs_are_json_serializable() -> None:
    recorder = LineageRecorder("sales_dataset", run_id="run-001", source_tables=["src.sales"], target_table="curated.sales")
    recorder.add_step(**_sample_step())
    summary = recorder.build_summary()
    records = build_lineage_records(dataset_name="sales_dataset", run_id="run-001", source_tables=["src.sales"], target_table="curated.sales", transformation_steps=recorder.to_records())
    context = build_lineage_prompt_context(dataset_name="sales_dataset", source_tables=["src.sales"], target_table="curated.sales", transformation_steps=recorder.to_records())
    json.dumps(summary)
    json.dumps(records)
    json.dumps(context)


def test_validate_lineage_steps_accepts_valid_steps() -> None:
    steps = [{"source": "raw_orders", "target": "clean_orders", "transformation": "Clean required columns and standardize amount", "reason": "Prepare source for validation and analytics", "source_type": "dataframe", "target_type": "dataframe", "confidence": "high", "notes": ""}]
    out = validate_lineage_steps(steps)
    assert out["is_valid"] is True
    assert out["review_required"] is False


def test_validate_lineage_steps_rejects_missing_fields() -> None:
    out = validate_lineage_steps([{"source": "raw_orders", "source_type": "dataframe", "target_type": "dataframe", "confidence": "high", "reason": "x"}])
    assert out["is_valid"] is False
    assert out["errors"]


def test_validate_lineage_steps_flags_low_confidence_review() -> None:
    out = validate_lineage_steps([{"source": "raw_orders", "target": "clean_orders", "transformation": "Filter", "reason": "Prepare", "source_type": "dataframe", "target_type": "dataframe", "confidence": "low"}])
    assert out["is_valid"] is True
    assert out["review_required"] is True
    assert out["warnings"]


def test_validate_lineage_steps_flags_unknown_type_review() -> None:
    out = validate_lineage_steps([{"source": "raw_orders", "target": "clean_orders", "transformation": "Filter", "reason": "Prepare", "source_type": "unknown", "target_type": "dataframe", "confidence": "high"}])
    assert out["review_required"] is True


def test_build_lineage_record_from_steps_uses_custom_dataset() -> None:
    steps = [{"source": "a", "target": "b", "transformation": "join", "reason": "analytics", "source_type": "dataframe", "target_type": "dataframe", "confidence": "high"}]
    rows = build_lineage_record_from_steps("custom_dataset", steps, run_id="run-001")
    assert rows[0]["dataset_name"] == "custom_dataset"
    assert "framework_smoke_orders" not in str(rows)


def test_get_fabric_copilot_lineage_prompt_contains_required_terms() -> None:
    prompt = get_fabric_copilot_lineage_prompt()
    for term in ["Fabric notebook", "scan the entire", "lineage_steps", "Spark", "Pandas", "DataFrame", "markdown", "comments", "reads", "writes", "joins", "filters", "withColumn", "groupBy", "confidence", "Needs human review", "matplotlib", "networkx", "avoid Mermaid", "human"]:
        assert term in prompt


def test_plot_lineage_networkx_returns_graph() -> None:
    steps = [{"source": "raw_orders", "target": "clean_orders", "transformation": "filter", "reason": "analytics", "source_type": "dataframe", "target_type": "dataframe", "confidence": "high"}]
    try:
        g, _, _ = plot_lineage_networkx(steps)
        assert g.number_of_nodes() == 2
        assert g.number_of_edges() == 1
    except ImportError as ex:
        assert "matplotlib" in str(ex) or "networkx" in str(ex)
