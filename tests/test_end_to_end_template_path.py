from pathlib import Path


def test_sample_assets_exist():
    assert Path("samples/end_to_end/minimal_source.csv").exists()


def test_02_ex_contains_approved_contract_handoff_flow():
    ex = Path("templates/notebooks/02_ex_agreement_topic.ipynb").read_text(encoding="utf-8")
    assert "HUMAN_APPROVED_RULES" in ex
    assert ("write_contract_to_lakehouse" in ex) or ("contracts.json" in ex)


def test_03_pc_contract_loading_and_dq_flow_markers_present():
    pc = Path("templates/notebooks/03_pc_agreement_source_to_target.ipynb").read_text(encoding="utf-8")
    assert "load_latest_approved_contract" in pc
    assert "rules = get_executable_quality_rules(contract)" in pc
    assert "split_valid_and_quarantine" in pc
    assert "minimal_source_contract.py" not in pc


def test_docs_explain_02_ex_creates_contract_for_03_pc():
    sample_readme = Path("samples/end_to_end/README.md").read_text(encoding="utf-8")
    assert "Run `02_ex_agreement_topic`" in sample_readme
    assert "creates the approved contract" in sample_readme
    assert "loads the approved contract from metadata" in sample_readme
