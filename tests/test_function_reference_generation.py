from __future__ import annotations

import ast
import re
from pathlib import Path

from scripts.generate_function_reference import main as generate_reference

ROOT = Path(__file__).resolve().parents[1]
INIT_FILE = ROOT / "src" / "fabric_data_product_framework" / "__init__.py"
REFERENCE_FILE = ROOT / "docs" / "reference" / "index.md"
MODULE_DIR = ROOT / "docs" / "api" / "modules"


def public_exports() -> list[str]:
    tree = ast.parse(INIT_FILE.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets):
            return [elt.value for elt in node.value.elts if isinstance(elt, ast.Constant)]
    raise AssertionError("__all__ missing")


def parse_module_symbols(module_path: Path) -> tuple[set[str], set[str]]:
    tree = ast.parse(module_path.read_text(encoding="utf-8"))
    functions, classes = set(), set()
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            functions.add(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.add(node.name)
    return functions, classes


def test_reference_generator_runs_without_fabric_runtime() -> None:
    generate_reference()
    assert REFERENCE_FILE.exists()


def test_module_pages_include_module_contents_and_deterministic_anchor_links() -> None:
    generate_reference()
    for doc in MODULE_DIR.glob("*.md"):
        if doc.name == "index.md":
            continue
        content = doc.read_text(encoding="utf-8")
        assert "## Module contents" in content
        section = content.split("## Module contents", 1)[1].split("## Public callables from `__all__`", 1)[0]
        rows = [line for line in section.splitlines() if line.startswith("| [`")]
        for row in rows:
            assert re.search(r"\| \[`[^`]+`\]\(#[a-z0-9\-]+\) \|", row)
            assert re.search(r"\| \[Jump\]\(#[a-z0-9\-]+\) \|$", row)


def test_public_and_related_internal_helpers_are_listed_in_module_contents() -> None:
    generate_reference()
    exports = set(public_exports())
    for src in (ROOT / "src" / "fabric_data_product_framework").glob("*.py"):
        if src.name == "__init__.py":
            continue
        module = src.stem
        doc = (MODULE_DIR / f"{module}.md").read_text(encoding="utf-8")
        functions, classes = parse_module_symbols(src)
        module_public = sorted((functions | classes) & exports)
        for name in module_public:
            assert f"[`{name}`](#" in doc


def test_modules_index_is_table_with_internal_labeling() -> None:
    generate_reference()
    content = (MODULE_DIR / "index.md").read_text(encoding="utf-8")
    assert "| Module | Public callable count | Internal helper count |" in content
    assert "|---|---:|---:|" in content
    assert "(internal)" in content


def test_zero_public_export_module_is_clearly_internal() -> None:
    generate_reference()
    exports = set(public_exports())
    for src in (ROOT / "src" / "fabric_data_product_framework").glob("*.py"):
        if src.name == "__init__.py":
            continue
        functions, classes = parse_module_symbols(src)
        if not ((functions | classes) & exports):
            content = (MODULE_DIR / f"{src.stem}.md").read_text(encoding="utf-8")
            assert "Internal module: no public exports from `__all__`." in content


def test_reference_rows_link_to_module_and_function_anchor() -> None:
    generate_reference()
    content = REFERENCE_FILE.read_text(encoding="utf-8")
    for name in public_exports():
        assert f"[`{name}`](../api/modules/" in content
        assert "[API anchor](../api/modules/" in content
        assert "· [Module](../api/modules/" in content


def test_generated_docs_are_multiline_readable() -> None:
    generate_reference()
    docs_files = [REFERENCE_FILE, *MODULE_DIR.glob("*.md")]
    for doc in docs_files:
        text = doc.read_text(encoding="utf-8")
        assert text.count("\n") > 5, f"{doc} appears to be a single-line/generated-compressed file"
