from pathlib import Path

from fabricops_kit.data_contracts import get_executable_quality_rules, normalize_contract_dict, validate_contract_dict
from fabricops_kit.data_quality import validate_dq_rules


def _simple_yaml_load(text: str) -> dict:
    data = {}
    for line in text.splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip()
    return data


def test_sample_assets_exist():
    assert Path("samples/end_to_end/minimal_source.csv").exists()
    assert Path("samples/end_to_end/minimal_source_contract.yml").exists()


def test_contract_and_rule_path():
    import yaml

    raw = yaml.safe_load(Path("samples/end_to_end/minimal_source_contract.yml").read_text(encoding="utf-8"))
    contract = normalize_contract_dict(raw)
    assert contract["status"] == "approved"
    assert validate_contract_dict(contract) == []
    rules = get_executable_quality_rules(contract)
    assert rules
    validate_dq_rules(rules)
    rule_types = {r.get("rule_type") for r in rules}
    assert {"not_null", "unique_key", "accepted_values", "value_range", "regex_format"}.issubset(rule_types)


def test_notebook_templates_contain_required_flow():
    pc = Path("templates/notebooks/03_pc_agreement_source_to_target.ipynb").read_text(encoding="utf-8")
    ex = Path("templates/notebooks/02_ex_agreement_topic.ipynb").read_text(encoding="utf-8")

    assert "rules = get_executable_quality_rules(contract)" in pc
    assert 'rules = DQ_RULES.get(TARGET_TABLE, [])' not in pc
    assert "split_valid_and_quarantine" in pc
    assert 'f"{TARGET_TABLE}_QUARANTINE"' in pc
    assert "build_dataset_run_record" in pc
    assert "build_quality_result_records" in pc
    assert ("build_contract_records" in pc) or ("write_contract_to_lakehouse" in pc)
    assert ("build_lineage_records" in pc) or ("build_lineage_record_from_steps" in pc)
    assert 'NOTEBOOK_CODE_FOR_LINEAGE = """' not in pc
    assert "suggest_dq_rules_prompt" in ex
    assert "validate_contract_dict" in ex
