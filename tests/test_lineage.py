from fabric_data_product_framework.lineage import (
    build_lineage_from_notebook_code,
    build_lineage_record_from_steps,
    enrich_lineage_steps_with_ai,
    plot_lineage_steps,
    scan_notebook_cells,
    scan_notebook_lineage,
    validate_lineage_steps,
)


def test_scan_read_transform_write_deterministic() -> None:
    code = """
df = lakehouse_table_read('orders')
clean = df.filter(df.amount > 0).select('id','amount')
lakehouse_table_write(clean, lh_out, 'orders_clean')
"""
    one = scan_notebook_lineage(code)
    two = scan_notebook_lineage(code)
    assert one == two
    assert any(s["operation_types"] == ["read"] for s in one)
    assert any("filter" in s["operation_types"] for s in one)
    assert any(s["operation_types"] == ["write"] for s in one)
    assert any(s["target"] == "orders_clean" for s in one if s["operation_types"] == ["write"])


def test_scan_join_and_cells() -> None:
    cells = ["a = lakehouse_table_read('a')", "b = lakehouse_table_read('b')\nout = a.join(b, 'id')"]
    steps = scan_notebook_cells(cells)
    assert any("join" in s["operation_types"] for s in steps)
    assert any("cell:1" in s["code_refs"] for s in steps)


def test_validation_rules() -> None:
    valid = [{"source":"a","target":"b","transformation":"filter","reason":"prep","source_type":"dataframe","target_type":"unknown","confidence":"low"}]
    out = validate_lineage_steps(valid)
    assert out["is_valid"] is True
    assert out["review_required"] is True
    bad = validate_lineage_steps([{"source":"a"}])
    assert bad["is_valid"] is False
    malformed = validate_lineage_steps(["oops", None])
    assert malformed["is_valid"] is False


def test_orchestration_and_fallback() -> None:
    code = "df = lakehouse_table_read('x')\nout = df.dropna()"
    result = build_lineage_from_notebook_code(code, use_ai=False)
    assert result["steps"]
    assert result["ai_used"] is False
    enriched = enrich_lineage_steps_with_ai(result["steps"], ai_helper=None)
    assert enriched["fallback_prompt"]


def test_plot_lineage_steps() -> None:
    steps = [{"source":"a","target":"b","transformation":"join","reason":"x","source_type":"dataframe","target_type":"dataframe","confidence":"high"}]
    try:
        fig = plot_lineage_steps(steps)
        assert fig is not None
    except ModuleNotFoundError as ex:
        assert "matplotlib" in str(ex) or "networkx" in str(ex)


def test_build_lineage_record_from_steps() -> None:
    steps = [{"source":"a","target":"b","transformation":"join","reason":"x","source_type":"dataframe","target_type":"dataframe","confidence":"high"}]
    rows = build_lineage_record_from_steps("ds", steps)
    assert rows[0]["dataset_name"] == "ds"
