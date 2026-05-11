import json
from pathlib import Path


def _code_cells(path: str) -> list[str]:
    nb = json.loads(Path(path).read_text(encoding="utf-8"))
    return ["".join(c.get("source", [])) for c in nb["cells"] if c.get("cell_type") == "code"]


def _all_code(path: str) -> str:
    return "\n".join(_code_cells(path))


def test_00_env_config_import_and_default_prompt_override_guard():
    cells = _code_cells("templates/notebooks/00_env_config.ipynb")
    import_block = cells[0]
    prompt_block = "\n".join(cells)
    assert "from fabricops_kit.environment_config import (" in import_block
    assert "create_ai_prompt_config" in import_block
    assert "AI_PROMPT_CONFIG = create_ai_prompt_config()" in prompt_block
    assert "if DQ_RULE_CANDIDATE_PROMPT_TEMPLATE_OVERRIDE is not None:" in prompt_block


def test_02_ex_contract_and_runtime_handoff_is_runnable():
    ex = _all_code("templates/notebooks/02_ex_agreement_topic.ipynb")
    assert "target_table=TARGET_TABLE" in ex
    for required in [
        '"contract_type": "source_input"',
        '"object_name": SOURCE_TABLE',
        '"version": "1.0.0"',
        '"status": "approved"',
        "SOURCE_INPUT_CONTRACT_APPROVED = normalize_contract_dict",
        "validate_contract_dict(SOURCE_INPUT_CONTRACT_APPROVED)",
        "write_contract_to_lakehouse(SOURCE_INPUT_CONTRACT_APPROVED",
    ]:
        assert required in ex


def test_02_ex_uses_widget_approved_rules_and_persists_metadata_table():
    ex = _all_code("templates/notebooks/02_ex_agreement_topic.ipynb")
    assert "import fabricops_kit.dq_review as dq_review" in ex
    assert "HUMAN_APPROVED_RULES = list(dq_review.APPROVED_RULES_FROM_WIDGET)" in ex
    assert "r.get('approval_status', 'approved') == 'approved'" not in ex
    assert "title='AI suggests (advisory), human reviews'" not in ex
    assert "if not HUMAN_APPROVED_RULES:" in ex
    assert 'raise ValueError("No approved DQ rules selected in widget.' in ex
    assert "approved_rules_metadata_df.write.mode('append').saveAsTable('METADATA_DQ_RULES')" in ex


def test_02_ex_and_03_pc_share_same_dq_table_key_convention():
    ex = _all_code("templates/notebooks/02_ex_agreement_topic.ipynb")
    pc = _all_code("templates/notebooks/03_pc_agreement_source_to_target.ipynb")
    assert 'DQ_TABLE_NAME = TARGET_TABLE' in ex
    assert 'DQ_TABLE_NAME = TARGET_TABLE' in pc
    assert 'build_dq_rule_history(' in ex and 'table_name=DQ_TABLE_NAME' in ex
    assert 'load_active_dq_rules(metadata_dq_rules, table_name=DQ_TABLE_NAME)' in pc


def test_03_pc_deterministic_only_and_valid_run_dq_signature():
    pc = _all_code("templates/notebooks/03_pc_agreement_source_to_target.ipynb")
    assert "run_dq_rules(df_standard, table_name=DQ_TABLE_NAME, rules=rules)" in pc
    assert "fail_on_error=False" not in pc
    assert "suggest_dq_rules" not in pc
    assert "extract_dq_rules" not in pc


def test_docs_match_signature_and_key_convention():
    text = Path("docs/data-quality-rules-system.md").read_text(encoding="utf-8")
    assert "fail_on_error=False" not in text
    assert "DQ_TABLE_NAME = TARGET_TABLE" in text
    assert "APPROVED_RULES_FROM_WIDGET" in text


def test_sample_csv_fixture_removed():
    assert not Path("samples/end_to_end/minimal_source.csv").exists()
