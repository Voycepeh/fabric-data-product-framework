from pathlib import Path

from fabric_data_product_framework.handover import create_actual_data_mvp_template


def test_actual_data_mvp_assets_exist_and_contain_runner_calls(tmp_path: Path):
    notebook_path = Path("examples/fabric_actual_data_mvp/actual_data_mvp_template.py")
    contract_path = Path("contracts/examples/actual_data_mvp_contract.yml")
    guide_path = Path("docs/workflows/run-actual-data-mvp.md")

    assert notebook_path.exists()
    assert contract_path.exists()
    assert guide_path.exists()

    notebook_text = notebook_path.read_text(encoding="utf-8")
    contract_text = contract_path.read_text(encoding="utf-8")
    guide_text = guide_path.read_text(encoding="utf-8")

    assert "fw.load_data_contract" in notebook_text
    assert "fw.run_data_product" in notebook_text
    assert "fw.assert_data_product_passed" in notebook_text
    assert "def transform" in notebook_text
    assert "meta.classification_table" not in notebook_text
    assert "governance.classification_table" in notebook_text or 'getattr(governance, "classification_table"' in notebook_text

    assert "workspace" not in notebook_text.lower()
    assert "workspace" not in contract_text.lower()
    assert 'result.get("dq_workflow_summary")' not in notebook_text
    assert 'result.get("drift_summary")' not in notebook_text
    assert 'result.get("governance_summary")' not in notebook_text
    assert 'result.get("quarantine_summary")' not in notebook_text

    for section in ["dataset:", "runtime:", "source:", "target:", "quality:", "drift:", "governance:", "metadata:"]:
        assert section in contract_text

    assert "examples/fabric_actual_data_mvp/actual_data_mvp_template.py" in guide_text
    assert "contracts/examples/actual_data_mvp_contract.yml" in guide_text

    generated = tmp_path / "generated_actual_data_mvp.py"
    output = create_actual_data_mvp_template(str(generated))
    assert Path(output).exists()
    generated_text = generated.read_text(encoding="utf-8")
    assert "fw.load_data_contract" in generated_text
    assert "fw.run_data_product" in generated_text
    assert "fw.assert_data_product_passed" in generated_text
    assert 'result.get("dq_workflow_summary")' not in generated_text
    assert 'result.get("drift_summary")' not in generated_text
    assert 'result.get("governance_summary")' not in generated_text
    assert 'result.get("quarantine_summary")' not in generated_text


from fabric_data_product_framework.handover import create_pipeline_notebook_template


def test_pipeline_template_lineage_calls_are_namespaced_and_defined(tmp_path: Path):
    out = tmp_path / "pipeline_template.py"
    create_pipeline_notebook_template(str(out), dataset_name="orders")
    text = out.read_text(encoding="utf-8")
    assert "import fabric_data_product_framework as fw" in text
    assert "fw.build_lineage_from_notebook_code" in text
    assert "lineage_result.get(\"validation\", {})" in text
    assert "fw.build_lineage_record_from_steps" in text
    assert "fw.plot_lineage_steps" in text


def test_pipeline_template_no_undefined_dataset_or_run_vars(tmp_path: Path):
    out = tmp_path / "pipeline_template_defined_vars.py"
    create_pipeline_notebook_template(str(out), dataset_name="orders")
    text = out.read_text(encoding="utf-8")
    assert "DATASET_NAME" not in text
    assert "RUN_ID" not in text
    assert 'dataset_name = "orders"' in text
    assert "run_id = None" in text


def test_generated_actual_data_mvp_contains_ai_assisted_lineage_section(tmp_path: Path):
    generated = tmp_path / "generated_actual_data_mvp_lineage.py"
    create_actual_data_mvp_template(str(generated))
    text = generated.read_text(encoding="utf-8")
    assert "fw.build_lineage_from_notebook_code" in text
    assert "lineage_steps = lineage_result.get(\"steps\", [])" in text
    assert "lineage_result.get(\"validation\", {})" in text
    assert "fw.build_lineage_record_from_steps(" in text
    assert "fw.plot_lineage_steps(" in text
