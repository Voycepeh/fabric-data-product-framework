from pathlib import Path

from fabric_data_product_framework.template_generator import create_actual_data_mvp_template


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
