import json
from pathlib import Path


def _code_cells(path: str) -> list[str]:
    nb = json.loads(Path(path).read_text(encoding="utf-8"))
    return ["".join(c.get("source", [])) for c in nb["cells"] if c.get("cell_type") == "code"]


def _all_code(path: str) -> str:
    return "\n".join(_code_cells(path))


def test_sample_csv_fixture_removed():
    assert not Path("samples/end_to_end/minimal_source.csv").exists()


def test_00_env_config_imports_create_ai_prompt_config_from_environment_config_block():
    code_cells = _code_cells("templates/notebooks/00_env_config.ipynb")
    import_block = code_cells[0]
    assert "from fabricops_kit.environment_config import (" in import_block
    assert "create_ai_prompt_config" in import_block


def test_02_ex_runtime_imports_and_contract_handoff_symbols_present():
    ex = _all_code("templates/notebooks/02_ex_agreement_topic.ipynb")
    for required in [
        "validate_notebook_name",
        "assert_notebook_name_valid",
        "build_runtime_context",
        "seed_minimal_sample_source_table",
        "lakehouse_table_read",
        "warehouse_read",
        "normalize_contract_dict",
        "validate_contract_dict",
        "write_contract_to_lakehouse",
        "SOURCE_INPUT_CONTRACT_APPROVED",
        "validate_contract_dict(SOURCE_INPUT_CONTRACT_APPROVED)",
        "write_contract_to_lakehouse(SOURCE_INPUT_CONTRACT_APPROVED",
    ]:
        assert required in ex


def test_02_ex_uses_consistent_dq_table_key_and_pending_default_approval():
    ex = _all_code("templates/notebooks/02_ex_agreement_topic.ipynb")
    assert 'DQ_TABLE_NAME = TARGET_TABLE' in ex
    for required in [
        'profile_for_dq(df_source, table_name=DQ_TABLE_NAME)',
        'extract_dq_rules(responses, table_name=DQ_TABLE_NAME)',
        'review_dq_rules(CANDIDATE_DQ_RULES, table_name=DQ_TABLE_NAME',
        'build_dq_rule_history(',
        'table_name=DQ_TABLE_NAME',
        "r.get('approval_status', 'pending_review')",
    ]:
        assert required in ex
    assert "r.get('approval_status', 'approved') == 'approved'" not in ex


def test_02_ex_approved_contract_contains_required_fields():
    ex = _all_code("templates/notebooks/02_ex_agreement_topic.ipynb")
    for required in [
        '"contract_type": "source_input"',
        '"object_name": SOURCE_TABLE',
        '"version": "1.0.0"',
        '"status": "approved"',
        '"required_columns":',
        '"optional_columns":',
        '"business_keys":',
        '"classifications":',
        '"quality_rules": HUMAN_APPROVED_RULES',
        '"column_types":',
        '"approved_by":',
        '"approval_note":',
    ]:
        assert required in ex


def test_03_pc_uses_deterministic_only_dq_with_same_key_and_valid_signature():
    pc = _all_code("templates/notebooks/03_pc_agreement_source_to_target.ipynb")
    assert 'DQ_TABLE_NAME = TARGET_TABLE' in pc
    assert "load_active_dq_rules(metadata_dq_rules, table_name=DQ_TABLE_NAME)" in pc
    assert "run_dq_rules(df_standard, table_name=DQ_TABLE_NAME, rules=rules)" in pc
    assert "fail_on_error=False" not in pc
    for required in [
        "load_active_dq_rules",
        "run_dq_rules",
        "split_dq_rows",
        "assert_dq_passed",
    ]:
        assert required in pc
    for forbidden in ["suggest_dq_rules", "extract_dq_rules"]:
        assert forbidden not in pc


def test_docs_match_callable_signature_and_dq_key_convention():
    text = Path("docs/data-quality-rules-system.md").read_text(encoding="utf-8")
    assert "fail_on_error=False" not in text
    assert "DQ_TABLE_NAME = TARGET_TABLE" in text


def test_seed_helper_rows_and_columns_defined():
    io_text = Path("src/fabricops_kit/fabric_io.py").read_text(encoding="utf-8")
    for expected in ["customer_id", "event_ts", "status", "amount", "email", "country_code", "user1001@example.com", "user1004@example.com"]:
        assert expected in io_text
