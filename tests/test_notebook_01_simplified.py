from __future__ import annotations

import ast
import json
from pathlib import Path

NOTEBOOK_PATH = Path("templates/notebooks/01_data_agreement_template.ipynb")


def _code_cells() -> list[str]:
    payload = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    return ["".join(cell.get("source", [])) for cell in payload.get("cells", []) if cell.get("cell_type") == "code"]


def test_notebook_01_has_valid_python_code_cells() -> None:
    for code in _code_cells():
        if code.lstrip().startswith("%"):
            continue
        ast.parse(code)


def test_notebook_01_uses_public_imports_only() -> None:
    private_symbols: list[str] = []
    for code in _code_cells():
        if code.lstrip().startswith("%"):
            continue
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == "fabricops_kit":
                for alias in node.names:
                    if alias.name.startswith("_"):
                        private_symbols.append(alias.name)
    assert private_symbols == []


def test_notebook_01_does_not_use_legacy_placeholders_or_widgets() -> None:
    combined = "\n".join(_code_cells())
    assert "FABRIC_CONFIG" not in combined
    assert "metadata_store = #" not in combined
    assert "notebookutils.widgets" not in combined


def test_notebook_01_agreement_fields_are_lightweight() -> None:
    combined = "\n".join(_code_cells())
    assert 'agreement_id = "r002_sales_demo"' in combined
    assert 'expiry_date = "2026-12-31"' in combined
    assert "classification" not in combined
    assert "sensitivity" not in combined
    assert "pii" not in combined


def test_notebook_01_uses_supported_setup_notebook_signature() -> None:
    combined = "\n".join(_code_cells())
    assert "CONFIG = setup_notebook(" not in combined
    assert "setup_notebook(spark, env_name=env_name)" not in combined
    assert "BOOTSTRAP_01 = setup_notebook(" in combined
    assert "config=CONFIG" in combined
    assert "env=env_name" in combined
    assert 'required_targets=["metadata"]' in combined
    assert 'notebook_name="01_data_agreement_template"' in combined


def test_notebook_01_restores_table_column_governance_workflow() -> None:
    combined = "\n".join(_code_cells())
    assert 'dataset_name = "r002_sales_demo"' in combined
    assert 'table_name = "sales_orders"' in combined
    assert 'read_lakehouse_table(CONFIG, env_name, "metadata", "METADATA_PROFILE_ROWS")' in combined
    assert "prepare_business_context_profile_input(" in combined
    assert "draft_business_context(" in combined
    assert "review_business_context(" in combined
    assert "write_business_context(" in combined
    assert "prepare_governance_input(" in combined
    assert "draft_governance(" in combined
    assert "review_governance(" in combined
    assert "write_governance(" in combined


def test_notebook_01_widget_launch_and_save_are_split_cells() -> None:
    code_cells = _code_cells()
    for code in code_cells:
        assert not ("review_business_context(" in code and "get_reviewed_business_context_rows(" in code)
        assert not ("review_governance(" in code and "write_governance(" in code)


def test_notebook_01_guards_empty_profile_rows_before_create_dataframe() -> None:
    combined = "\n".join(_code_cells())
    assert "if profile_rows:" in combined
    assert "if prepared_rows:" in combined


def test_notebook_01_metadata_access_uses_configured_routing_only() -> None:
    combined = "\n".join(_code_cells())
    assert 'spark.table("METADATA_' not in combined
    assert 'spark.sql(' not in combined
    assert 'read_lakehouse_table(CONFIG, env_name, "metadata", "METADATA_PROFILE_ROWS")' in combined
    assert 'read_lakehouse_table(CONFIG, env_name, "metadata", "METADATA_DQ_RULES")' in combined
