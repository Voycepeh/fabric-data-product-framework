from pathlib import Path

FULL_MODULE_FILES = [
    "environment_config.py",
    "runtime_context.py",
    "fabric_input_output.py",
    "data_profiling.py",
    "data_contracts.py",
    "data_quality.py",
    "data_drift.py",
    "data_governance.py",
    "data_product_metadata.py",
    "data_lineage.py",
    "handover_documentation.py",
    "technical_audit_columns.py",
]


def test_full_module_files_exist() -> None:
    root = Path("src/fabricops_kit")
    for module_file in FULL_MODULE_FILES:
        assert (root / module_file).exists()


def test_data_quality_alias_functions_declared() -> None:
    text = Path("src/fabricops_kit/data_quality.py").read_text(encoding="utf-8")
    assert "def run_data_quality_rules" in text
    assert "def validate_data_quality_rules" in text
