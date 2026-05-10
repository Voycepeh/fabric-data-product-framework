from pathlib import Path


def test_sample_csv_fixture_removed():
    assert not Path("samples/end_to_end/minimal_source.csv").exists()


def test_seed_helper_is_available_and_notebook_uses_it():
    io_text = Path("src/fabricops_kit/fabric_io.py").read_text(encoding="utf-8")
    ex = Path("templates/notebooks/02_ex_agreement_topic.ipynb").read_text(encoding="utf-8")
    assert "def seed_minimal_sample_source_table" in io_text
    assert "seed_minimal_sample_source_table" in ex
    assert "minimal_source.csv" not in ex


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
    assert "minimal_source.csv" not in pc


def test_docs_explain_02_ex_creates_contract_for_03_pc():
    sample_readme = Path("samples/end_to_end/README.md").read_text(encoding="utf-8")
    assert "Run `02_ex_agreement_topic`" in sample_readme
    assert "creates the approved source-input contract" in sample_readme
    assert "reads the same `minimal_source` table" in sample_readme


def test_seed_helper_rows_and_columns_defined():
    io_text = Path("src/fabricops_kit/fabric_io.py").read_text(encoding="utf-8")
    for expected in ["customer_id", "country", "amount", "is_active", "1001", "1004"]:
        assert expected in io_text
