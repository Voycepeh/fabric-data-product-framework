from __future__ import annotations

import ast
import json
from pathlib import Path

from scripts.generate_function_reference import main as generate_reference

ROOT = Path(__file__).resolve().parents[1]
INIT_FILE = ROOT / "src" / "fabricops_kit" / "__init__.py"
CALLABLE_MAP_FILE = ROOT / "docs" / "reference" / "callable-map.md"
CALLABLE_MAP_JSON_FILE = ROOT / "docs" / "reference" / "callable-map.json"


def public_exports() -> list[str]:
    tree = ast.parse(INIT_FILE.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets):
            return [elt.value for elt in node.value.elts if isinstance(elt, ast.Constant)]
    raise AssertionError("__all__ missing")


def test_callable_map_outputs_are_generated() -> None:
    generate_reference()
    assert CALLABLE_MAP_FILE.exists()
    assert CALLABLE_MAP_JSON_FILE.exists()


def test_callable_map_markdown_sections_present() -> None:
    generate_reference()
    content = CALLABLE_MAP_FILE.read_text(encoding="utf-8")
    assert "# Callable Map" in content
    assert "Public callable chains" in content
    assert "Internal helper index" in content
    assert "Cross-module FabricOps calls" in content
    assert "Module dependency summary" in content


def test_callable_map_json_shape_and_nodes() -> None:
    generate_reference()
    payload = json.loads(CALLABLE_MAP_JSON_FILE.read_text(encoding="utf-8"))
    assert isinstance(payload["nodes"], list)
    assert isinstance(payload["edges"], list)
    assert isinstance(payload["module_summary"], list)
    exported_nodes = {n["callable_name"] for n in payload["nodes"] if n.get("exported")}
    for symbol in public_exports():
        assert symbol in exported_nodes


def test_callable_map_contains_internal_helpers_and_unresolved_edges() -> None:
    generate_reference()
    payload = json.loads(CALLABLE_MAP_JSON_FILE.read_text(encoding="utf-8"))
    assert any(node["callable_name"].startswith("_") for node in payload["nodes"])
    unresolved = [edge for edge in payload["edges"] if edge["edge_type"] == "unresolved"]
    assert isinstance(unresolved, list)
