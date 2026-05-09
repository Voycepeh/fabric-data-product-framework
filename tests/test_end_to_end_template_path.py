from pathlib import Path
from runpy import run_path

from fabricops_kit.data_contracts import get_executable_quality_rules, normalize_contract_dict, validate_contract_dict
from fabricops_kit.data_quality import validate_dq_rules


def test_sample_assets_exist():
    assert Path("samples/end_to_end/minimal_source.csv").exists()
    assert Path("samples/end_to_end/minimal_source_contract.py").exists()


def test_contract_fixture_validates_and_rules_compile():
    raw = run_path("samples/end_to_end/minimal_source_contract.py")["MINIMAL_SOURCE_CONTRACT"]
    contract = normalize_contract_dict(raw)
    assert validate_contract_dict(contract) == []
    rules = get_executable_quality_rules(contract)
    assert rules
    validate_dq_rules(rules)


def test_03_pc_core_flow_markers_present():
    pc = Path("templates/notebooks/03_pc_agreement_source_to_target.ipynb").read_text(encoding="utf-8")
    assert "rules = get_executable_quality_rules(contract)" in pc
    assert "split_valid_and_quarantine" in pc
    assert 'f\"{TARGET_TABLE}_QUARANTINE\"' in pc
    assert "Optional: metadata evidence for audit/handover" in pc


def test_02_ex_core_flow_markers_present():
    ex = Path("templates/notebooks/02_ex_agreement_topic.ipynb").read_text(encoding="utf-8")
    assert "suggest_dq_rules_prompt" in ex
    assert "validate_contract_dict" in ex
    assert "minimal_source_contract.py" in ex


def test_docs_do_not_reference_yaml_contract():
    docs_text = Path("templates/notebooks/README.md").read_text(encoding="utf-8") + "\n" + Path("docs/recipes/index.md").read_text(encoding="utf-8")
    assert "minimal_source_contract.yml" not in docs_text
    assert "YAML" not in docs_text
