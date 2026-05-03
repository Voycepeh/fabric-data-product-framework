from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PKG_DIR = ROOT / "src" / "fabric_data_product_framework"
INIT_PATH = PKG_DIR / "__init__.py"
REFERENCE_PATH = ROOT / "docs" / "reference" / "index.md"
MODULE_DIR = ROOT / "docs" / "api" / "modules"

STEP_FALLBACK_NOTES = {
    5: "No public callable is currently exported for this step. Use notebook prompts for AI-assisted rule drafting.",
}

PUBLIC_CALLABLE_STEP_REGISTRY = {
    "validate_notebook_name": 1,
    "assert_notebook_name_valid": 1,
    "build_runtime_context": 1,
    "generate_run_id": 1,
    "Housepath": 2,
    "load_fabric_config": 2,
    "get_path": 2,
    "lakehouse_table_read": 3,
    "lakehouse_csv_read": 3,
    "lakehouse_excel_read_as_spark": 3,
    "lakehouse_parquet_read_as_spark": 3,
    "warehouse_read": 3,
    "profile_dataframe": 4,
    "profile_dataframe_to_metadata": 4,
    "profile_metadata_to_records": 4,
    "build_ai_quality_context": 4,
    "build_dataset_run_record": 11,
    "build_schema_snapshot_records": 11,
    "build_schema_drift_records": 11,
    "build_quality_result_records": 11,
    "write_metadata_records": 11,
    "write_multiple_metadata_outputs": 11,
    "run_quality_rules": 7,
    "load_data_contract": 7,
    "check_schema_drift": 8,
    "check_profile_drift": 8,
    "check_partition_drift": 8,
    "summarize_drift_results": 8,
    "default_technical_columns": 10,
    "add_datetime_features": 10,
    "add_audit_columns": 10,
    "add_hash_columns": 10,
    "lakehouse_table_write": 11,
    "warehouse_write": 11,
    "classify_column": 12,
    "classify_columns": 12,
    "build_governance_classification_records": 12,
    "write_governance_classifications": 12,
    "summarize_governance_classifications": 12,
    "build_lineage_records": 13,
    "generate_mermaid_lineage": 13,
    "build_transformation_summary_markdown": 13,
    "LineageRecorder": 13,
    "build_run_summary": 13,
    "render_run_summary_markdown": 13,
}


@dataclass
class Symbol:
    name: str
    module: str
    obj_type: str
    summary: str


def first_sentence(doc: str | None) -> str:
    if not doc:
        return ""
    line = doc.strip().splitlines()[0].strip()
    return line.split(".")[0].strip() + ("." if "." in line else "")


def is_deprecated(doc: str | None) -> bool:
    return "deprecated" in (doc or "").lower()


def slug(name: str) -> str:
    return name.replace("_", "-").lower()


def parse_module(path: Path) -> dict[str, Any]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    functions: dict[str, dict[str, Any]] = {}
    classes: dict[str, dict[str, Any]] = {}
    constants: dict[str, dict[str, Any]] = {}
    calls: dict[str, set[str]] = {}
    used_by: dict[str, set[str]] = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            doc = ast.get_docstring(node)
            functions[node.name] = {"summary": first_sentence(doc), "deprecated": is_deprecated(doc)}
            called = set()
            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Name):
                        called.add(child.func.id)
                    elif isinstance(child.func, ast.Attribute):
                        called.add(child.func.attr)
            calls[node.name] = called
        elif isinstance(node, ast.ClassDef):
            doc = ast.get_docstring(node)
            is_dc = any(isinstance(d, ast.Name) and d.id == "dataclass" for d in node.decorator_list)
            classes[node.name] = {"summary": first_sentence(doc), "deprecated": is_deprecated(doc), "is_dataclass": is_dc}
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id.isupper():
                    constants[t.id] = {"summary": "Module-level constant or registry.", "deprecated": False}
    names = set(functions) | set(classes)
    for caller, callees in calls.items():
        for callee in names:
            if callee in callees:
                used_by.setdefault(callee, set()).add(caller)
    return {"functions": functions, "classes": classes, "constants": constants, "calls": calls, "used_by": used_by}


def parse_public_exports() -> list[str]:
    tree = ast.parse(INIT_PATH.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets):
            if isinstance(node.value, ast.List):
                return [elt.value for elt in node.value.elts if isinstance(elt, ast.Constant) and isinstance(elt.value, str)]
    raise RuntimeError("Could not parse __all__ from __init__.py")


def parse_step_registry() -> list[dict[str, Any]]:
    tree = ast.parse((PKG_DIR / "handover.py").read_text(encoding="utf-8"))
    for node in tree.body:
        is_assign = isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "MVP_STEP_REGISTRY" for t in node.targets)
        is_annassign = isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "MVP_STEP_REGISTRY"
        if is_assign or is_annassign:
            if node.value is None:
                continue
            reg = ast.literal_eval(node.value)
            return [{"step_number": i["step_number"], "step_name": i["step_name"], "canonical_modules": [m.replace('.py', '') for m in i.get("canonical_modules", [])]} for i in reg]
    return []


def resolve_step(symbol: Symbol, step_modules: dict[int, list[str]]) -> int | None:
    if symbol.name in PUBLIC_CALLABLE_STEP_REGISTRY:
        return PUBLIC_CALLABLE_STEP_REGISTRY[symbol.name]
    for step, modules in step_modules.items():
        if symbol.module in modules:
            return step
    return None


def main() -> None:
    public = parse_public_exports()
    module_data = {p.stem: parse_module(p) for p in PKG_DIR.glob("*.py") if p.name != "__init__.py"}
    symbol_map: dict[str, Symbol] = {}
    for name in public:
        for module, info in module_data.items():
            if name in info["functions"]:
                symbol_map[name] = Symbol(name, module, "Function", info["functions"][name]["summary"])
                break
            if name in info["classes"]:
                t = "Dataclass" if info["classes"][name]["is_dataclass"] else "Class"
                symbol_map[name] = Symbol(name, module, t, info["classes"][name]["summary"])
                break

    step_registry = parse_step_registry()
    step_modules = {s["step_number"]: s["canonical_modules"] for s in step_registry}
    step_titles = {s["step_number"]: s["step_name"] for s in step_registry}

    MODULE_DIR.mkdir(parents=True, exist_ok=True)
    module_index_lines = ["# Module API Catalogue", "", "Generated module summaries with public exports and related internal helpers.", "", "| Module | Public callable count | Internal helper count | Main workflow step(s) | Description | Link |", "|---|---:|---:|---|---|---|"]

    for module in sorted(module_data):
        info = module_data[module]
        public_in_module = [s for s in symbol_map.values() if s.module == module]
        public_names = {s.name for s in public_in_module}
        function_names = set(info["functions"])
        class_names = set(info["classes"])
        related_helpers = sorted(n for n in (function_names | class_names) if n not in public_names and info["used_by"].get(n) and any(u in public_names for u in info["used_by"][n]))
        other_internal = sorted(n for n in (function_names | class_names) if n not in public_names and n not in related_helpers)
        deprecated_count = sum(1 for n in function_names if info["functions"][n]["deprecated"]) + sum(1 for n in class_names if info["classes"][n]["deprecated"])
        is_internal_only = not public_in_module
        lines = [f"# `{module}` module" + (" (internal)" if is_internal_only else ""), "", f"Public callables: {len(public_in_module)}  ", f"Related internal helpers: {len(related_helpers)}  ", f"Other internal objects: {len(other_internal)}  ", f"Deprecated objects: {deprecated_count}", ""]
        if is_internal_only:
            lines.extend(["Internal module: no public exports from `__all__`.", ""])
        lines.extend(["## Module contents", "", "| Name | Status | Type | Purpose | Used by / related public callable | API link |", "|---|---|---|---|---|---|"])

        for name in sorted(function_names | class_names):
            if name in info["functions"]:
                meta = info["functions"][name]
                typ = "Function"
            else:
                meta = info["classes"][name]
                typ = "Dataclass" if meta["is_dataclass"] else "Class"
            if meta["deprecated"]:
                status = "Deprecated"
            elif name in public_names:
                status = "Public"
            elif name in related_helpers:
                status = "Internal helper"
            else:
                status = "Internal"
            rel = sorted(u for u in info["used_by"].get(name, set()) if u in public_names)
            anchor = slug(name)
            lines.append(f"| [{name}](#{anchor}) | {status} | {typ} | {meta['summary'] or '—'} | {', '.join(f'`{r}`' for r in rel) or '—'} | [API](#{anchor}) |")

        lines.extend(["", "## Public callables from `__all__`", ""])
        if public_in_module:
            lines.extend(["| Callable | Type | Summary | Related helpers |", "|---|---|---|---|"])
            for s in sorted(public_in_module, key=lambda x: x.name.lower()):
                related = sorted([c for c in info["calls"].get(s.name, set()) if c in function_names and c.startswith("_")])
                lines.append(f"| `{s.name}` | {s.obj_type} | {s.summary or '—'} | {', '.join(f'`{r}` (internal)' for r in related) or '—'} |")
        else:
            lines.append("No public exports in this module.")
        lines.extend(["", "## Related internal helpers", ""])
        if related_helpers:
            lines.extend(["| Helper | Related public callables |", "|---|---|"])
            for helper in related_helpers:
                users = sorted([u for u in info["used_by"].get(helper, set()) if u in public_names])
                lines.append(f"| `{helper}` | {', '.join(f'`{u}`' for u in users) or '—'} |")
        else:
            lines.append("No module-level related internal helpers detected.")
        lines.extend(["", "## Full module API", ""])
        if is_internal_only:
            lines.append("This module is internal-only and is intentionally excluded from full public API rendering.")
        else:
            lines.append(f"::: fabric_data_product_framework.{module}")
        (MODULE_DIR / f"{module}.md").write_text("\n".join(lines)+"\n", encoding="utf-8", newline="\n")

        steps = sorted({resolve_step(s, step_modules) for s in public_in_module if resolve_step(s, step_modules) is not None})
        step_text = ", ".join(f"{n}: {step_titles.get(n,'') }" for n in steps) or "—"
        desc = "Internal module with no public exports." if is_internal_only else "Module containing public callable implementations."
        module_index_lines.append(f"| `{module}` | {len(public_in_module)} | {len(related_helpers)} | {step_text} | {desc} | [Open]({module}.md) |")

    (MODULE_DIR / "index.md").write_text("\n".join(module_index_lines)+"\n", encoding="utf-8", newline="\n")

    ref = ["# Callable Reference", "", "Generated step-first function catalogue sourced from `fabric_data_product_framework.__all__`.", ""]
    step_symbols: dict[int, list[Symbol]] = {s["step_number"]: [] for s in step_registry}
    other: list[Symbol] = []
    for symbol in symbol_map.values():
        step = resolve_step(symbol, step_modules)
        (other if step is None else step_symbols[step]).append(symbol)

    for step in sorted(step_titles):
        ref += [f"## Step {step}: {step_titles[step]}", ""]
        entries = sorted(step_symbols.get(step, []), key=lambda x: x.name.lower())
        if entries:
            ref += ["| Function / class | Module | Purpose | Related helpers | API link |", "|---|---|---|---|---|"]
            for s in entries:
                info = module_data[s.module]
                related = sorted([c for c in info["calls"].get(s.name, set()) if c in info["functions"] and c.startswith("_")])
                ref.append(f"| [`{s.name}`](../api/modules/{s.module}.md#{slug(s.name)}) | [`{s.module}`](../api/modules/{s.module}.md) | {s.summary or '—'} | {', '.join(f'`{r}` (internal)' for r in related) or '—'} | [function API](../api/modules/{s.module}.md#{slug(s.name)}) |")
        else:
            ref.append("No public callable currently mapped to this step.")
            if step in STEP_FALLBACK_NOTES:
                ref += ["", STEP_FALLBACK_NOTES[step]]
        ref.append("")
    if other:
        ref += ["## Other Utilities", ""]
        for s in sorted(other, key=lambda x: x.name.lower()):
            ref.append(f"- [`{s.name}`](../api/modules/{s.module}.md#{slug(s.name)}) ([`{s.module}`](../api/modules/{s.module}.md))")

    REFERENCE_PATH.write_text("\n".join(ref)+"\n", encoding="utf-8", newline="\n")

if __name__ == "__main__":
    main()
