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
    import fabricops_kit as fdpf

    missing: list[str] = []
    for name in public_exports():
        obj = getattr(fdpf, name)
        doc = getattr(obj, "__doc__", None)
        first_line = (doc or "").strip().splitlines()[0].strip() if doc else ""
        if not first_line:
            missing.append(name)
    assert missing == []


def test_step_specific_callable_placement() -> None:
    generate_reference()
    content = REFERENCE_FILE.read_text(encoding="utf-8")
    step1 = section(content, "Step 1: Package and runtime setup")
    step2 = section(content, "Step 2: Fabric config and paths")
    step3 = section(content, "Step 3: Pull source data")
    step10 = section(content, "Step 10: Standard technical columns")
    step11 = section(content, "Step 11: Output write, output profiling, and metadata logging")

    assert "`lakehouse_table_read`" in step3
    assert "`lakehouse_table_read`" not in step1
    assert "`add_audit_columns`" in step10
    assert "`add_datetime_features`" in step10
    assert "`add_hash_columns`" in step10
    assert "`default_technical_columns`" in step10
    assert "`lakehouse_table_write`" in step11
    assert "`warehouse_write`" in step11
    assert "`warehouse_write`" not in step1
    assert "`get_path`" in step2


def test_metadata_driven_summary_override_is_applied() -> None:
    generate_reference()
    content = REFERENCE_FILE.read_text(encoding="utf-8")
    assert "Run the framework pipeline end-to-end for a data product." in content


def test_reference_links_are_site_friendly_and_correctly_routed() -> None:
    generate_reference()
    content = REFERENCE_FILE.read_text(encoding="utf-8")
    assert "./step-02-runtime-configuration/get_path/" in content
    assert "./step-02-runtime-configuration/load_fabric_config/" in content
    assert "./step-04-source-ingestion-read-helpers/profile_metadata_to_records/" in content
    assert "./step-02-runtime-configuration/get_path.md" not in content
    assert "./step-02-runtime-configuration/load_fabric_config.md" not in content
    assert "./step-04-source-ingestion-read-helpers/profile_metadata_to_records.md" not in content


def test_docs_metadata_matches_public_exports() -> None:
    exports = set(public_exports())
    metadata_symbols = {row["symbol_name"] for row in public_symbol_docs()}
    assert exports - metadata_symbols == set()
    assert metadata_symbols - exports == set()


def test_build_quality_result_records_metadata_module_matches_exported_symbol_module() -> None:
    import fabricops_kit as fdpf

    metadata_row = next(row for row in public_symbol_docs() if row["symbol_name"] == "build_quality_result_records")
    exported_module = getattr(fdpf.build_quality_result_records, "__module__", "").split(".")[-1]
    assert metadata_row["module"] == exported_module


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
            assert "intentionally excluded from full public API rendering" in text


def test_all_exports_appear_exactly_once_in_reference() -> None:
    generate_reference()
    text = REFERENCE_FILE.read_text(encoding="utf-8")
    for name in public_exports():
        assert text.count(f"`{name}`") == 1


def test_handover_uses_single_canonical_registry_symbol() -> None:
    handover = (ROOT / "src" / "fabricops_kit" / "handover.py").read_text(encoding="utf-8")
    assert "MVP_STEP_REGISTRY" in handover
    assert "LEGACY_MVP_STEPS" in handover
    assert handover.count("def get_mvp_step_registry(") == 1


def test_generated_docs_use_lf_newlines() -> None:
    generate_reference()
    docs_files = [REFERENCE_FILE, MODULE_INDEX_FILE, *((ROOT / "docs" / "api" / "modules").glob("*.md"))]
    for doc in docs_files:
        raw = doc.read_bytes()
        assert b"\r\n" not in raw, f"{doc} contains CRLF newlines"
