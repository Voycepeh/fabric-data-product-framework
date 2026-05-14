from fabricops_kit.data_contracts import generate_handover_contract, export_handover_contract


def test_generate_handover_contract_filters_and_counts(tmp_path):
    package = generate_handover_contract(
        contracts=[{"contract_id": "c1", "dataset_name": "orders", "approval_status": "approved"}],
        contract_columns=[{"dataset_name": "orders", "table_name": "curated.orders", "column_name": "order_id", "status": "approved"}],
        contract_rules=[{"dataset_name": "orders", "table_name": "curated.orders", "rule_id": "r1", "status": "approved"}],
        quality_results=[{"dataset_name": "orders", "table_name": "curated.orders", "status": "passed"}],
        lineage_records=[{"dataset_name": "orders", "source": "raw.orders", "target": "curated.orders"}],
        dataset_name="orders",
        table_name="curated.orders",
        include_prompt=True,
    )
    assert package["summary"]["contract_count"] == 1
    assert package["summary"]["column_count"] == 1
    assert "handover_summary_prompt" in package

    out = tmp_path / "handover.json"
    written = export_handover_contract(package, str(out), format="json")
    assert written.endswith("handover.json")
    assert out.exists()
