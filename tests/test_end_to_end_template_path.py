from pathlib import Path


def test_sample_csv_fixture_removed():
    assert not Path("samples/end_to_end/minimal_source.csv").exists()


def test_seed_helper_is_available_and_notebook_uses_it():
    io_text = Path("src/fabricops_kit/fabric_io.py").read_text(encoding="utf-8")
    ex = Path("templates/notebooks/02_ex_agreement_topic.ipynb").read_text(encoding="utf-8")
    assert "def seed_minimal_sample_source_table" in io_text
    assert "seed_minimal_sample_source_table" in ex
    assert "minimal_source.csv" not in ex


def test_03_pc_reads_seeded_source_without_reseeding():
    pc = Path("templates/notebooks/03_pc_agreement_source_to_target.ipynb").read_text(encoding="utf-8")
    assert "seed_minimal_sample_source_table" not in pc
    assert "lakehouse_table_read(source_path, SOURCE_TABLE)" in pc


def test_02_ex_uses_framework_ai_dq_functions_only():
    ex = Path("templates/notebooks/02_ex_agreement_topic.ipynb").read_text(encoding="utf-8")
    for required in [
        "profile_for_dq",
        "suggest_dq_rules",
        "extract_dq_rules",
        "review_dq_rules",
        "build_dq_rule_history",
    ]:
        assert required in ex
    for forbidden in [
        "run_dq_rules",
        "split_dq_rows",
        "assert_dq_passed",
        "get_default_dq_rule_templates",
        "suggest_dq_rules_prompt",
        "split_valid_and_quarantine",
    ]:
        assert forbidden not in ex


def test_03_pc_uses_framework_deterministic_dq_functions_only():
    pc = Path("templates/notebooks/03_pc_agreement_source_to_target.ipynb").read_text(encoding="utf-8")
    for required in [
        "load_active_dq_rules",
        "run_dq_rules",
        "split_dq_rows",
        "assert_dq_passed",
    ]:
        assert required in pc
    for forbidden in [
        "suggest_dq_rules",
        "extract_dq_rules",
        "get_default_dq_rule_templates",
        "suggest_dq_rules_prompt",
        "split_valid_and_quarantine",
        "data_quality import",
    ]:
        assert forbidden not in pc


def test_docs_explain_02_ex_creates_contract_for_03_pc():
    readme_path = Path("samples/end_to_end/README.md")
    if not readme_path.exists():
        return
    sample_readme = readme_path.read_text(encoding="utf-8")
    assert "Run `02_ex_agreement_topic`" in sample_readme
    assert "creates the approved source-input contract" in sample_readme
    assert "reads the same `minimal_source` table" in sample_readme


def test_seed_helper_rows_and_columns_defined():
    io_text = Path("src/fabricops_kit/fabric_io.py").read_text(encoding="utf-8")
    for expected in ["customer_id", "event_ts", "status", "amount", "email", "country_code", "user1001@example.com", "user1004@example.com"]:
        assert expected in io_text
