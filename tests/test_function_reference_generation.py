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


def test_reference_generator_runs_without_fabric_runtime() -> None:
    generate_reference()
    assert REFERENCE_FILE.exists()


def test_every_public_export_is_listed_exactly_once_in_all_functions_table() -> None:
    generate_reference()
    content = REFERENCE_FILE.read_text(encoding="utf-8")
    for name in public_exports():
        assert content.count(f"`{name}`") == 1


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
    assert "#### Segment 2: Profile source and capture evidence" in content and "`generate_metadata_profile`" in content
    assert "#### Segment 3: AI-assisted drafting (advisory only)" in content and "`build_manual_dq_rule_prompt_package`" in content
    assert "#### Segment 4: Run DQ, split outputs, and publish" in content and "`run_dq_rules`" in content


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
    assert "| Function / class | Module | Starter path | Importance | Purpose |" in content
    assert "| [`load_fabric_config`]" in content


def test_non_starter_callable_still_appears_in_complete_catalogue() -> None:
    generate_reference()
    content = REFERENCE_FILE.read_text(encoding="utf-8")
    assert "## Additional public functions" in content
    assert "`run_data_product`" in content


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
