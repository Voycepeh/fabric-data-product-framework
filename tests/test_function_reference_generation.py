from __future__ import annotations

import ast
from pathlib import Path

from scripts.generate_function_reference import main as generate_reference

ROOT = Path(__file__).resolve().parents[1]
INIT_FILE = ROOT / "src" / "fabricops_kit" / "__init__.py"
REFERENCE_FILE = ROOT / "docs" / "reference" / "index.md"
DOCS_METADATA_FILE = ROOT / "src" / "fabricops_kit" / "docs_metadata.py"


def public_exports() -> list[str]:
    tree = ast.parse(INIT_FILE.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets):
            return [elt.value for elt in node.value.elts if isinstance(elt, ast.Constant)]
    raise AssertionError("__all__ missing")


def metadata_literal(name: str) -> list[dict[str, object]]:
    tree = ast.parse(DOCS_METADATA_FILE.read_text(encoding="utf-8"))
    for node in tree.body:
        is_assign = isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets)
        is_annassign = isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == name
        if (is_assign or is_annassign) and node.value is not None:
            return ast.literal_eval(node.value)
    raise AssertionError(f"{name} missing")


def notebook_source_text(path: str) -> str:
    import json

    notebook = json.loads((ROOT / path).read_text(encoding="utf-8"))
    return "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"] if cell.get("cell_type") == "code")


def markdown_section(content: str, heading: str) -> str:
    start_token = f"## {heading}\n"
    start = content.find(start_token)
    if start < 0:
        return ""
    rest = content[start + len(start_token) :]
    next_idx = rest.find("\n## ")
    return rest if next_idx < 0 else rest[:next_idx]


def test_reference_generator_runs_without_fabric_runtime() -> None:
    generate_reference()
    assert REFERENCE_FILE.exists()


def test_every_public_export_is_listed_exactly_once_in_all_functions_table() -> None:
    generate_reference()
    content = REFERENCE_FILE.read_text(encoding="utf-8")
    all_functions = markdown_section(content, "All public functions")
    assert all_functions
    for name in public_exports():
        assert all_functions.count(f"<code>{name}</code>") == 1


def test_reference_contains_template_first_starter_sections_and_segments() -> None:
    generate_reference()
    content = REFERENCE_FILE.read_text(encoding="utf-8")
    assert "## Starter path functions" in content
    assert "### `00_env_config`" in content
    assert "### `02_ex_<agreement>_<topic>`" in content
    assert "### `03_pc_<agreement>_<pipeline>`" in content
    assert "#### Segment 1: Load shared config and runtime" in content
    assert "#### Segment 2: Profile source and capture evidence" in content
    assert "#### Segment 3: AI-assisted drafting (advisory only)" in content
    assert "#### Segment 4: Human approval and contract write" in content
    assert "#### Segment 1: Load shared config and runtime context" in content
    assert "#### Segment 2: Load approved contract and source data" in content
    assert "#### Segment 3: Validate columns, transform, and compile rules" in content
    assert "#### Segment 4: Run DQ, split outputs, and publish" in content
    assert "#### Optional metadata / lineage / handover evidence" in content


def test_template_used_functions_appear_in_expected_starter_segments() -> None:
    generate_reference()
    content = REFERENCE_FILE.read_text(encoding="utf-8")
    assert "#### Segment 2: Profile source and capture evidence" in content and "<code>generate_metadata_profile</code>" in content
    assert "#### Segment 3: AI-assisted drafting (advisory only)" in content and "<code>suggest_dq_rules_prompt</code>" in content
    assert "#### Segment 4: Run DQ, split outputs, and publish" in content and "<code>run_dq_rules</code>" in content


def test_reference_no_longer_contains_old_step_headings() -> None:
    generate_reference()
    content = REFERENCE_FILE.read_text(encoding="utf-8")
    assert "## Lifecycle flow" not in content
    assert "## Callable map by workflow step" not in content
    assert "## Step 1:" not in content
    assert "## Step 2A:" not in content


def test_all_public_functions_table_contains_starter_path_column() -> None:
    generate_reference()
    content = REFERENCE_FILE.read_text(encoding="utf-8")
    assert "## All public functions" in content
    assert '<table class="reference-catalogue-table">' in content
    assert 'data-label="Starter path"' in content
    assert '<a href="./step-02a-shared-runtime-config/load_fabric_config/"><code>load_fabric_config</code></a>' in content
    assert "data-callable-row" in content
    assert "data-callable-name=" in content
    assert "data-callable-purpose=" in content


def test_reference_includes_callable_finder_block() -> None:
    generate_reference()
    content = REFERENCE_FILE.read_text(encoding="utf-8")
    assert "## Find a callable" in content
    assert 'data-callable-finder' in content
    assert 'id="callable-finder-input"' in content
    assert 'data-callable-finder-empty' in content
    assert content.index("## Find a callable") < content.index("## All public functions")
    assert content.index("## Find a callable") > content.index("## Starter path functions")


def test_function_reference_tables_use_compact_module_links() -> None:
    generate_reference()
    content = REFERENCE_FILE.read_text(encoding="utf-8")
    assert 'class="reference-module-link"' in content
    assert '<table class="reference-function-table">' in content
    assert '<table class="reference-catalogue-table">' in content
    assert 'api-chip api-chip-module api-chip-link' not in content


def test_non_starter_callable_still_appears_in_complete_catalogue() -> None:
    generate_reference()
    content = REFERENCE_FILE.read_text(encoding="utf-8")
    assert "## Additional public functions" in content
    assert "<code>run_data_product</code>" in content


def test_reference_tables_include_mobile_friendly_classes_and_data_labels() -> None:
    generate_reference()
    content = REFERENCE_FILE.read_text(encoding="utf-8")
    assert '<table class="reference-template-table">' in content
    assert '<table class="reference-function-table">' in content
    assert 'data-label="Function / class"' in content
    assert 'data-label="Purpose"' in content


def test_reference_html_tables_use_anchor_links_not_markdown_links() -> None:
    generate_reference()
    content = REFERENCE_FILE.read_text(encoding="utf-8")
    assert '<td data-label="Full template"><a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/00_env_config.ipynb">Open notebook</a></td>' in content
    assert '<td data-label="Function / class"><a href="./step-02a-shared-runtime-config/Housepath/"><code>Housepath</code></a></td>' in content
    assert '<a href="./internal/config/_check_spark_session.md"><code>_check_spark_session</code></a> (internal)' in content
    assert "[`Open notebook`](" not in content
    assert "<code>`00_env_config`</code>" not in content


def test_docs_metadata_matches_public_exports() -> None:
    exports = set(public_exports())
    metadata_symbols = {row["symbol_name"] for row in metadata_literal("PUBLIC_SYMBOL_DOCS")}
    assert exports == metadata_symbols


def test_reference_file_is_in_sync_with_generator() -> None:
    before = REFERENCE_FILE.read_text(encoding="utf-8")
    generate_reference()
    after = REFERENCE_FILE.read_text(encoding="utf-8")
    assert after == before


def test_generated_docs_are_multiline_readable_and_lf_safe() -> None:
    generate_reference()
    text = REFERENCE_FILE.read_text(encoding="utf-8")
    assert text.count("\n") > 20
    assert "\r\n" not in text


def test_template_flow_symbols_are_exported() -> None:
    exports = set(public_exports())
    template_docs = metadata_literal("TEMPLATE_FLOW_DOCS")
    for notebook in template_docs:
        for segment in notebook["segments"]:
            for symbol in segment["symbols"]:
                assert symbol in exports


def test_template_flow_registry_matches_expected_symbol_sets() -> None:
    template_docs = metadata_literal("TEMPLATE_FLOW_DOCS")
    symbols_by_notebook: dict[str, set[str]] = {}
    for notebook in template_docs:
        symbols = symbols_by_notebook.setdefault(notebook["notebook_key"], set())
        for segment in notebook["segments"]:
            symbols.update(segment["symbols"])

    expected = {
        "00_env_config": {
            "Housepath",
            "create_path_config",
            "create_notebook_runtime_config",
            "create_ai_prompt_config",
            "create_governance_config",
            "create_quality_config",
            "create_lineage_config",
            "create_framework_config",
            "validate_framework_config",
            "load_fabric_config",
            "run_config_smoke_tests",
            "bootstrap_fabric_env",
            "check_fabric_ai_functions_available",
            "configure_fabric_ai_functions",
            "get_path",
        },
        "02_ex": {
            "load_fabric_config",
            "validate_notebook_name",
            "assert_notebook_name_valid",
            "build_runtime_context",
            "get_path",
            "lakehouse_table_read",
            "warehouse_read",
            "generate_metadata_profile",
            "profile_dataframe_to_metadata",
            "suggest_dq_rules_prompt",
            "normalize_contract_dict",
            "validate_contract_dict",
            "write_contract_to_lakehouse",
            "build_lineage_from_notebook_code",
        },
        "03_pc": {
            "load_fabric_config",
            "validate_notebook_name",
            "assert_notebook_name_valid",
            "generate_run_id",
            "build_runtime_context",
            "get_path",
            "load_latest_approved_contract",
            "lakehouse_table_read",
            "warehouse_read",
            "extract_required_columns",
            "get_executable_quality_rules",
            "validate_dq_rules",
            "run_dq_rules",
            "split_valid_and_quarantine",
            "lakehouse_table_write",
            "warehouse_write",
            "build_dataset_run_record",
            "build_quality_result_records",
            "build_contract_records",
            "build_lineage_records",
        },
    }
    assert symbols_by_notebook == expected


def test_every_starter_flow_symbol_is_used_in_its_template_notebook() -> None:
    template_docs = metadata_literal("TEMPLATE_FLOW_DOCS")
    for notebook in template_docs:
        code = notebook_source_text(notebook["template_path"])
        for segment in notebook["segments"]:
            for symbol in segment["symbols"]:
                assert symbol in code, f"{symbol} is listed for {notebook['notebook_key']} but not used in notebook code"
