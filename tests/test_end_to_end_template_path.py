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
    assert "DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE" in import_block
    assert "DEFAULT_GOVERNANCE_CANDIDATE_TEMPLATE" in import_block
    assert "DEFAULT_HANDOVER_SUMMARY_TEMPLATE" in import_block
    assert "BUSINESS_CONTEXT_PROMPT_TEMPLATE = DEFAULT_BUSINESS_CONTEXT_PROMPT_TEMPLATE" in prompt_block
    assert "DQ_RULE_SUGGESTION_PROMPT_TEMPLATE = DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE" in prompt_block
    assert "GOVERNANCE_PERSONAL_IDENTIFIER_PROMPT_TEMPLATE = DEFAULT_GOVERNANCE_PERSONAL_IDENTIFIER_PROMPT_TEMPLATE" in prompt_block
    assert "GOVERNANCE_CANDIDATE_PROMPT_TEMPLATE = DEFAULT_GOVERNANCE_CANDIDATE_TEMPLATE" in prompt_block
    assert "GOVERNANCE_REVIEW_PROMPT_TEMPLATE = DEFAULT_GOVERNANCE_REVIEW_TEMPLATE" in prompt_block
    assert "HANDOVER_SUMMARY_PROMPT_TEMPLATE = DEFAULT_HANDOVER_SUMMARY_TEMPLATE" in prompt_block
    assert "ReviewWorkflowConfig" in import_block
    assert "REVIEW_WORKFLOW_CONFIG = ReviewWorkflowConfig(" in prompt_block
    assert "review_workflow_config=REVIEW_WORKFLOW_CONFIG" in prompt_block
    assert "AI_PROMPTS = {" not in prompt_block
    assert "notebook_runtime_config=RUNTIME_CONFIG" in prompt_block
    assert "\n    runtime_config=RUNTIME_CONFIG," not in prompt_block
    assert "NotebookRuntimeConfig(\n    allowed_notebook_prefixes=NOTEBOOK_PREFIXES,\n    validation_mode=VALIDATION_MODE" not in prompt_block
    assert "setup_notebook(\n    config=CONFIG,\n    env=ENV," in prompt_block
    assert "validation_mode=VALIDATION_MODE" not in prompt_block
    assert "check_naming_convention(\n    allowed_prefixes=NOTEBOOK_PREFIXES,\n    fail_on_error=(VALIDATION_MODE == \"strict\"),\n)" in prompt_block
    assert "Suggest governance labels as JSON. Profile: {profile}" not in prompt_block
    assert "Summarize run handover details as markdown. Context: {context}" not in prompt_block


def test_00_env_config_is_environment_only_and_imports_package_helpers():
    text = Path("templates/notebooks/00_env_config.ipynb").read_text(encoding="utf-8")
    for token in ["AGREEMENT_ID", "SOURCE_LAYER", "TARGET_LAYER"]:
        assert token not in text
    for token in [
        "from fabricops_kit.fabric_input_output import (",
        "from fabricops_kit.config import (",
        "setup_notebook(",
        "load_config(CONFIG)",
    ]:
        assert token in text
    for token in [
        "def get_path",
        "def validate_environment",
        "def validate_target",
        "def clean_datetime_columns",
        "def add_system_technical_columns",
        "def initialize_fabricops_runtime",
        "class RuntimeContext",
    ]:
        assert token not in text


def test_02_ex_dq_only_handoff_is_runnable():
    ex = _all_code("templates/notebooks/02_ex_agreement_topic.ipynb")
    assert "DQ_TABLE_NAME = TARGET_TABLE" in ex
    for required in [
        "HUMAN_APPROVED_RULES = list(data_quality.APPROVED_RULES_FROM_WIDGET)",
        "write_dq_rules(",
        "table_name=DQ_TABLE_NAME",
        "Optional: use this section when this workflow is needed.",
        "build_governance_classification_records",
    ]:
        assert required in ex


def test_02_ex_uses_widget_approved_rules_and_persists_metadata_table():
    ex = _all_code("templates/notebooks/02_ex_agreement_topic.ipynb")
    assert "import fabricops_kit.data_quality as data_quality" in ex
    assert "HUMAN_APPROVED_RULES = list(data_quality.APPROVED_RULES_FROM_WIDGET)" in ex
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
    assert "enforce_dq(" in pc
    assert "table_name=DQ_TABLE_NAME" in pc
    assert "metadata_df=metadata_dq_rules" in pc
    assert "dq_run_id=RUN_ID" in pc


def test_03_pc_deterministic_only_and_valid_run_dq_signature():
    pc = _all_code("templates/notebooks/03_pc_agreement_source_to_target.ipynb")
    assert "RUN_OPTIONAL_ADVANCED_EVIDENCE = False" in pc
    assert 'REQUIRED_SOURCE_COLUMNS = ["customer_id", "event_ts", "status", "amount"]' in pc
    assert 'missing = sorted(set(REQUIRED_SOURCE_COLUMNS) - set(df_source.columns))' in pc
    assert 'metadata_dq_rules = spark.table("METADATA_DQ_RULES")' in pc
    assert "enforce_dq(" in pc
    assert "table_name=DQ_TABLE_NAME" in pc
    assert "metadata_df=metadata_dq_rules" in pc
    assert "dq_run_id=RUN_ID" in pc
    assert "df_valid = dq.valid_rows" in pc
    assert "assert_dq_passed(dq.rule_results)" in pc
    assert "fail_on_error=False" not in pc
    assert "suggest_dq_rules" not in pc
    assert "extract_dq_rules" not in pc


def test_03_pc_output_write_occurs_after_dq_assertion():
    pc = _all_code("templates/notebooks/03_pc_agreement_source_to_target.ipynb")
    assert pc.index("df_valid = dq.valid_rows") < pc.index("write_lakehouse_table(df_valid")
    assert pc.index("assert_dq_passed(dq.rule_results)") < pc.index("write_lakehouse_table(df_valid")


def test_03_pc_optional_advanced_evidence_is_guarded():
    pc = _all_code("templates/notebooks/03_pc_agreement_source_to_target.ipynb")
    assert "if RUN_OPTIONAL_ADVANCED_EVIDENCE:" in pc
    assert "prepare_drift_baselines(" in pc


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
        "read_lakehouse_csv",  # ingestion variant; lakehouse table path is primary in current templates
        "read_lakehouse_excel",  # ingestion variant
        "read_lakehouse_parquet",  # ingestion variant
    }
    missing = essentials - present - allowed_missing
    assert missing == set(), f"Missing essential callables in templates: {sorted(missing)}"


def test_01_data_agreement_template_exists_and_contains_required_context_fields():
    text = Path("templates/notebooks/01_data_agreement_template.ipynb").read_text(encoding="utf-8")
    for token in [
        "AGREEMENT_ID",
        "APPROVED_USAGE",
        "BUSINESS_CONTEXT",
        "ReviewWorkflowConfig",
        "METADATA_DATA_AGREEMENT",
    ]:
        assert token in text


def test_01_data_agreement_template_has_no_dq_enforcement_or_column_widget_execution():
    text = Path("templates/notebooks/01_data_agreement_template.ipynb").read_text(encoding="utf-8")
    forbidden = [
        "enforce_dq(",
        "run_dq_rules(",
        "capture_column_business_context(",
        "review_dq_rules(",
        "review_column_governance_context(",
    ]
    for token in forbidden:
        assert token not in text


def test_00_env_config_keeps_review_workflow_defaults_generic():
    text = Path("templates/notebooks/00_env_config.ipynb").read_text(encoding="utf-8")
    assert "BUSINESS_CONTEXT_PROMPT_TEMPLATE" in text
    assert "GOVERNANCE_REVIEW_PROMPT_TEMPLATE" in text
    assert "Customer analytics and governed reporting" not in text


def test_02_ex_template_references_01_agreement_and_business_context_helpers():
    text = Path("templates/notebooks/02_ex_agreement_topic.ipynb").read_text(encoding="utf-8")
    for token in [
        "%run 01_data_agreement_template",
        "BUSINESS_CONTEXT",
        "prepare_business_context_profile_input",
        "suggest_column_business_contexts",
        "extract_column_business_context_suggestions",
        "capture_column_business_context",
        "COLUMN_BUSINESS_CONTEXT_FROM_WIDGET",
        "prepare_dq_profile_input",
        "prepare_governance_profile_input",
        "suggest_personal_identifier_classifications",
        "review_column_governance_context",
    ]:
        assert token in text


def test_03_pc_template_has_no_ai_suggestion_or_business_context_widget_calls():
    text = Path("templates/notebooks/03_pc_agreement_source_to_target.ipynb").read_text(encoding="utf-8")
    for token in ["suggest_column_business_contexts", "suggest_personal_identifier_classifications", "capture_column_business_context"]:
        assert token not in text


def test_templates_readme_documents_all_four_layers():
    text = Path("templates/notebooks/README.md").read_text(encoding="utf-8")
    for token in ["00_env_config", "01_data_agreement_template", "02_ex_*", "03_pc_*"]:
        assert token in text
