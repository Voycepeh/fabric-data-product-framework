from __future__ import annotations

import ast
from pathlib import Path

import pytest

from scripts.generate_function_reference import main as generate_reference

ROOT = Path(__file__).resolve().parents[1]
INIT_FILE = ROOT / "src" / "fabricops_kit" / "__init__.py"
REFERENCE_FILE = ROOT / "docs" / "reference" / "index.md"
MODULE_INDEX_FILE = ROOT / "docs" / "api" / "modules" / "index.md"
DOCS_METADATA_FILE = ROOT / "src" / "fabricops_kit" / "docs_metadata.py"


def public_exports() -> list[str]:
    tree = ast.parse(INIT_FILE.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets):
            return [elt.value for elt in node.value.elts if isinstance(elt, ast.Constant)]
    raise AssertionError("__all__ missing")


def public_symbol_docs() -> list[dict[str, object]]:
    tree = ast.parse(DOCS_METADATA_FILE.read_text(encoding="utf-8"))
    for node in tree.body:
        is_assign = isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "PUBLIC_SYMBOL_DOCS" for t in node.targets)
        is_annassign = isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "PUBLIC_SYMBOL_DOCS"
        if (is_assign or is_annassign) and node.value is not None:
            return ast.literal_eval(node.value)
    raise AssertionError("PUBLIC_SYMBOL_DOCS missing")


def section(content: str, title: str) -> str:
    marker = f"## {title}"
    start = content.find(marker)
    if start < 0:
        return ""
    rest = content[start + len(marker) :]
    next_idx = rest.find("\n## ")
    return rest if next_idx < 0 else rest[:next_idx]


def test_reference_generator_runs_without_fabric_runtime() -> None:
    generate_reference()
    assert REFERENCE_FILE.exists()


def test_every_public_export_is_listed_and_linked() -> None:
    generate_reference()
    content = REFERENCE_FILE.read_text(encoding="utf-8")
    for name in public_exports():
        assert f"`{name}`" in content
        assert "module overview" not in content
        assert "api-chip-link" in content


def test_every_public_callable_has_docstring_first_sentence() -> None:
    missing: list[str] = []
    package_dir = ROOT / "src" / "fabricops_kit"
    module_trees = {p.stem: ast.parse(p.read_text(encoding="utf-8")) for p in package_dir.glob("*.py")}
    symbols = {row["symbol_name"]: row["module"] for row in public_symbol_docs()}
    for name in public_exports():
        module = symbols[name]
        tree = module_trees[module]
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name == name:
                first_line = ((ast.get_docstring(node) or "").strip().splitlines() or [""])[0].strip()
                if not first_line:
                    missing.append(name)
                break
    assert missing == []


def test_step_specific_callable_placement() -> None:
    generate_reference()
    content = REFERENCE_FILE.read_text(encoding="utf-8")
    step1 = section(content, "Step 1: Define purpose, approved usage & governance ownership")
    step2 = section(content, "Step 2: Configure runtime, environment & path rules")
    step3 = section(content, "Step 3: Declare source contract & ingest source data")
    step6 = section(content, "Step 6: Build production transformation & write target output")
    step7 = section(content, "Step 7: Validate output & persist target metadata")

    assert "`lakehouse_table_read`" in step3
    assert "`lakehouse_table_read`" not in step1
    assert "`add_audit_columns`" in step6
    assert "`add_datetime_features`" in step6
    assert "`add_hash_columns`" in step6
    assert "`default_technical_columns`" in step6
    assert "`lakehouse_table_write`" in step7
    assert "`warehouse_write`" in step7
    assert "`warehouse_write`" not in step1
    assert "`get_path`" in step2


def test_metadata_driven_summary_override_is_applied() -> None:
    generate_reference()
    content = REFERENCE_FILE.read_text(encoding="utf-8")
    assert "Run the starter kit workflow end-to-end for a data product outcome." in content


def test_reference_links_are_site_friendly_and_correctly_routed() -> None:
    generate_reference()
    content = REFERENCE_FILE.read_text(encoding="utf-8")
    assert "./step-02-runtime-environment-path-rules/get_path/" in content
    assert "./step-02-runtime-environment-path-rules/load_fabric_config/" in content
    assert "./step-04-source-validation-metadata/profile_metadata_to_records/" in content
    assert "./step-02-runtime-environment-path-rules/get_path.md" not in content
    assert "./step-02-runtime-environment-path-rules/load_fabric_config.md" not in content
    assert "./step-04-source-validation-metadata/profile_metadata_to_records.md" not in content


def test_docs_metadata_matches_public_exports() -> None:
    exports = set(public_exports())
    metadata_symbols = {row["symbol_name"] for row in public_symbol_docs()}
    assert exports - metadata_symbols == set()
    assert metadata_symbols - exports == set()


def test_build_quality_result_records_metadata_module_matches_exported_symbol_module() -> None:
    metadata_row = next(row for row in public_symbol_docs() if row["symbol_name"] == "build_quality_result_records")
    assert metadata_row["module"] == "metadata"


def test_invalid_workflow_step_fails_loudly(monkeypatch) -> None:
    from scripts import generate_function_reference as gen

    bad = dict(gen.parse_docs_metadata())
    target = next(iter(bad))
    bad[target] = dict(bad[target])
    bad[target]["workflow_step"] = 99
    monkeypatch.setattr(gen, "parse_docs_metadata", lambda: bad)
    with pytest.raises(RuntimeError, match="Invalid workflow_step"):
        gen.main()


def test_generated_docs_are_multiline_readable() -> None:
    generate_reference()
    docs_files = [REFERENCE_FILE, *(ROOT / "docs" / "api" / "modules").glob("*.md")]
    for doc in docs_files:
        text = doc.read_text(encoding="utf-8")
        assert text.count("\n") > 5, f"{doc} appears to be a single-line/generated-compressed file"


def test_no_public_looking_module_page_for_internal_only_modules() -> None:
    generate_reference()
    for module_doc in (ROOT / "docs" / "api" / "modules").glob("*.md"):
        text = module_doc.read_text(encoding="utf-8")
        if "No public exports in this module." in text:
            assert "(internal)" in text
            assert "Not intended as a primary user-facing API surface." in text


def test_all_exports_appear_exactly_once_in_reference() -> None:
    generate_reference()
    text = REFERENCE_FILE.read_text(encoding="utf-8")
    for name in public_exports():
        assert text.count(f"`{name}`") == 1


def test_reference_lists_all_exported_callables() -> None:
    generate_reference()
    content = REFERENCE_FILE.read_text(encoding="utf-8")
    missing = [name for name in public_exports() if f"`{name}`" not in content]
    assert missing == []
    assert "## Other exported callables" in content
    assert "| Function / class | Module | Importance | Purpose |" in content


def test_public_callables_are_exported_or_private() -> None:
    exported = set(public_exports())
    package_dir = ROOT / "src" / "fabricops_kit"
    public_modules = {row["module"] for row in public_symbol_docs()}
    public_missing: list[str] = []
    for module_path in package_dir.glob("*.py"):
        mod_name = module_path.stem
        if mod_name.startswith("_") or mod_name in {"__init__", "schemas"} or mod_name not in public_modules:
            continue
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        module_all: set[str] = set()
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets):
                if isinstance(node.value, ast.List):
                    module_all = {
                        elt.value for elt in node.value.elts if isinstance(elt, ast.Constant) and isinstance(elt.value, str)
                    }
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_") and module_all and node.name in module_all:
                if node.name not in exported:
                    public_missing.append(f"fabricops_kit.{mod_name}.{node.name}")
    assert public_missing == []


def test_workflow_step_none_moves_symbol_to_other_exported_callables(monkeypatch) -> None:
    from scripts import generate_function_reference as gen

    bad = dict(gen.parse_docs_metadata())
    target = "lakehouse_table_read"
    bad[target] = dict(bad[target])
    bad[target]["workflow_step"] = None
    monkeypatch.setattr(gen, "parse_docs_metadata", lambda: bad)
    gen.main()
    content = REFERENCE_FILE.read_text(encoding="utf-8")
    assert "## Other exported callables" in content
    other = section(content, "Other exported callables")
    assert "`lakehouse_table_read`" in other


def test_handover_uses_single_canonical_registry_symbol() -> None:
    handover = (ROOT / "src" / "fabricops_kit" / "handover.py").read_text(encoding="utf-8")
    assert "MVP_STEP_REGISTRY" in handover
    assert handover.count("def get_mvp_step_registry(") >= 1


def test_generated_docs_use_lf_newlines() -> None:
    generate_reference()
    docs_files = [REFERENCE_FILE, MODULE_INDEX_FILE, *((ROOT / "docs" / "api" / "modules").glob("*.md"))]
    for doc in docs_files:
        raw = doc.read_bytes()
        assert b"\r\n" not in raw, f"{doc} contains CRLF newlines"
