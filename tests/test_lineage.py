from fabricops_kit.data_lineage import build_lineage_handover_markdown, build_lineage_records


def test_build_lineage_records() -> None:
    rows = build_lineage_records(
        dataset_name="ds",
        run_id="r1",
        source_tables=["src.orders"],
        target_table="prd.orders_clean",
        transformation_steps=[{"step": "filter", "detail": "amount > 0"}],
    )
    assert rows
    assert rows[0]["dataset_name"] == "ds"
    assert rows[0]["target_table"] == "prd.orders_clean"


def test_build_lineage_handover_markdown() -> None:
    md = build_lineage_handover_markdown({"records": [{"source_table": "src.orders", "target_table": "prd.orders_clean"}]})
    assert "prd.orders_clean" in md
