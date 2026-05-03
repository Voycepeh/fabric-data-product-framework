from __future__ import annotations

import ast
from pathlib import Path

from scripts.generate_function_reference import main as generate_reference


ROOT = Path(__file__).resolve().parents[1]
INIT_FILE = ROOT / "src" / "fabric_data_product_framework" / "__init__.py"
REFERENCE_FILE = ROOT / "docs" / "reference" / "index.md"


def public_exports() -> list[str]:
    tree = ast.parse(INIT_FILE.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets):
            return [elt.value for elt in node.value.elts if isinstance(elt, ast.Constant)]
    raise AssertionError("__all__ missing")


def test_reference_generator_runs_without_fabric_runtime() -> None:
    generate_reference()
    assert REFERENCE_FILE.exists()


def test_every_public_export_is_listed_and_linked() -> None:
    generate_reference()
    content = REFERENCE_FILE.read_text(encoding="utf-8")
    for name in public_exports():
        assert f"`{name}`" in content
        assert "module API" in content


def test_every_public_callable_has_docstring_first_sentence() -> None:
    import fabric_data_product_framework as fdpf

    missing: list[str] = []
    for name in public_exports():
        obj = getattr(fdpf, name)
        doc = getattr(obj, "__doc__", None)
        first_line = (doc or "").strip().splitlines()[0].strip() if doc else ""
        if not first_line:
            missing.append(name)
    assert missing == []
