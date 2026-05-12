import json
import ast
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
    assert "from fabricops_kit.config import (" in import_block
    assert "create_ai_prompt_config" not in import_block
    assert "AI_PROMPT_CONFIG = AIPromptConfig(" in prompt_block
    assert "DEFAULT_DQ_RULE_CANDIDATE_TEMPLATE" in import_block
    assert "DEFAULT_GOVERNANCE_CANDIDATE_TEMPLATE" in import_block
    assert "DEFAULT_HANDOVER_SUMMARY_TEMPLATE" in import_block
    assert "DQ_RULE_CANDIDATE_PROMPT_TEMPLATE = DEFAULT_DQ_RULE_CANDIDATE_TEMPLATE" in prompt_block
    assert "GOVERNANCE_CANDIDATE_PROMPT_TEMPLATE = DEFAULT_GOVERNANCE_CANDIDATE_TEMPLATE" in prompt_block
    assert "HANDOVER_SUMMARY_PROMPT_TEMPLATE = DEFAULT_HANDOVER_SUMMARY_TEMPLATE" in prompt_block
    assert "Suggest candidate DQ rules as JSON. Profile: {profile}" not in prompt_block
    assert "Suggest governance labels as JSON. Profile: {profile}" not in prompt_block
    assert "Summarize run handover details as markdown. Context: {context}" not in prompt_block


def test_02_ex_dq_only_handoff_is_runnable():
    ex = _all_code("templates/notebooks/02_ex_agreement_topic.ipynb")
    assert "DQ_TABLE_NAME = TARGET_TABLE" in ex
    for required in [
        "HUMAN_APPROVED_RULES = list(notebook_review.APPROVED_RULES_FROM_WIDGET)",
        "write_dq_rules(",
        "table_name=DQ_TABLE_NAME",
        "Optional: use this section when this workflow is needed.",
        "build_governance_classification_records",
    ]:
        assert required in ex


def test_02_ex_uses_widget_approved_rules_and_persists_metadata_table():
    ex = _all_code("templates/notebooks/02_ex_agreement_topic.ipynb")
    assert "import fabricops_kit.notebook_review as notebook_review" in ex
    assert "HUMAN_APPROVED_RULES = list(notebook_review.APPROVED_RULES_FROM_WIDGET)" in ex
    assert "r.get('approval_status', 'approved') == 'approved'" not in ex
    assert "title='AI suggests (advisory), human reviews'" not in ex
    assert "if not HUMAN_APPROVED_RULES:" in ex
    assert 'raise ValueError("No approved DQ rules selected in widget.' in ex
    assert "approved_rules_metadata_df = write_dq_rules(" in ex


def test_02_ex_and_03_pc_share_same_dq_table_key_convention():
    ex = _all_code("templates/notebooks/02_ex_agreement_topic.ipynb")
    pc = _all_code("templates/notebooks/03_pc_agreement_source_to_target.ipynb")
    assert 'DQ_TABLE_NAME = TARGET_TABLE' in ex
    assert 'DQ_TABLE_NAME = TARGET_TABLE' in pc
    assert 'write_dq_rules(' in ex and 'table_name=DQ_TABLE_NAME' in ex
    assert "enforce_dq_rules(" in pc
    assert "table_name=DQ_TABLE_NAME" in pc
    assert "metadata_df=metadata_dq_rules" in pc
    assert "dq_run_id=RUN_ID" in pc


def test_03_pc_deterministic_only_and_valid_run_dq_signature():
    pc = _all_code("templates/notebooks/03_pc_agreement_source_to_target.ipynb")
    assert 'REQUIRED_SOURCE_COLUMNS = ["customer_id", "event_ts", "status", "amount"]' in pc
    assert 'missing = sorted(set(REQUIRED_SOURCE_COLUMNS) - set(df_source.columns))' in pc
    assert 'metadata_dq_rules = spark.table("METADATA_DQ_RULES")' in pc
    assert "enforce_dq_rules(" in pc
    assert "table_name=DQ_TABLE_NAME" in pc
    assert "metadata_df=metadata_dq_rules" in pc
    assert "dq_run_id=RUN_ID" in pc
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


def test_no_removed_metadata_replacement_tokens_or_contract_imports():
    text = Path("templates/notebooks/02_ex_agreement_topic.ipynb").read_text(encoding="utf-8") + Path(
        "templates/notebooks/03_pc_agreement_source_to_target.ipynb"
    ).read_text(encoding="utf-8")
    forbidden = [
        "fabricops_kit.data_contracts",
        "SOURCE_INPUT_METADATA_DRAFT",
        "SOURCE_INPUT_METADATA_APPROVED",
        "approved_source_metadata",
        "source_metadata",
        "metadata_handover_id",
        "metadata_status",
        "handover_metadata",
    ]
    for token in forbidden:
        assert token not in text


def test_essential_callable_coverage_in_current_starter_notebooks():
    docs_metadata = Path("src/fabricops_kit/docs_metadata.py").read_text(encoding="utf-8")
    tree = ast.parse(docs_metadata)
    rows = []
    for node in tree.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "PUBLIC_SYMBOL_DOCS":
            rows = ast.literal_eval(node.value)
            break
    essentials = {row["symbol_name"] for row in rows if row["role"] == "essential"}

    notebooks_text = (
        Path("templates/notebooks/00_env_config.ipynb").read_text(encoding="utf-8")
        + Path("templates/notebooks/02_ex_agreement_topic.ipynb").read_text(encoding="utf-8")
        + Path("templates/notebooks/03_pc_agreement_source_to_target.ipynb").read_text(encoding="utf-8")
    )
    present = {name for name in essentials if name in notebooks_text}

    # Allowed missing until governance-context notebook (01_data_agreement) exists.
    allowed_missing = {
        "Housepath",  # type-level helper not always shown explicitly in starter notebooks
        "lakehouse_csv_read",  # ingestion variant; lakehouse table path is primary in current templates
        "lakehouse_excel_read_as_spark",  # ingestion variant
        "lakehouse_parquet_read_as_spark",  # ingestion variant
    }
    missing = essentials - present - allowed_missing
    assert missing == set(), f"Missing essential callables in templates: {sorted(missing)}"
