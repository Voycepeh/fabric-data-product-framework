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


def test_duplicate_names_not_marked_exported_in_wrong_module() -> None:
    generate_reference()
    payload = json.loads(CALLABLE_MAP_JSON_FILE.read_text(encoding="utf-8"))
    nodes = payload["nodes"]
    exported_lookup = {(n["module_name"], n["callable_name"]): n["exported"] for n in nodes}
    assert exported_lookup.get(("config", "load_config")) is True
    assert exported_lookup.get(("fabric_input_output", "load_config"), False) is False


def test_cross_module_private_helper_calls_flagged_distinctly() -> None:
    generate_reference()
    payload = json.loads(CALLABLE_MAP_JSON_FILE.read_text(encoding="utf-8"))
    edges = payload["edges"]
    assert any(e["edge_type"] == "cross_module" and e["callee_kind"] == "internal_helper" for e in edges)
    assert any(e["edge_type"] == "cross_module" and e["callee_kind"] == "public_export" for e in edges)
    assert any(e["edge_type"] == "cross_module" and e["callee_kind"] == "internal_callable" for e in edges)


def test_write_business_context_resolves_function_level_import_call() -> None:
    generate_reference()
    payload = json.loads(CALLABLE_MAP_JSON_FILE.read_text(encoding="utf-8"))
    assert any(
        edge["caller_qualified_name"] == "fabricops_kit.business_context.write_business_context"
        and edge["callee_qualified_name"] == "fabricops_kit.metadata.write_column_business_context"
        and edge["edge_type"] == "cross_module"
        for edge in payload["edges"]
    )


def test_callee_kind_values_are_restricted() -> None:
    generate_reference()
    payload = json.loads(CALLABLE_MAP_JSON_FILE.read_text(encoding="utf-8"))
    allowed = {"public_export", "internal_helper", "internal_callable", "unresolved"}
    assert {edge["callee_kind"] for edge in payload["edges"]}.issubset(allowed)
