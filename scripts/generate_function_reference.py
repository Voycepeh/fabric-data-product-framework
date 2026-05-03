from __future__ import annotations

import ast
import re
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
    "summarize_profile": 4,
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
    "classify_columns": 12,
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
    is_public: bool
    is_deprecated: bool
    related_public: set[str]



def first_sentence(doc: str | None) -> str:
    if not doc:
        return ""
    line = doc.strip().splitlines()[0].strip()
    return line.split(".")[0].strip() + ("." if "." in line else "")



def is_dataclass_node(node: ast.ClassDef) -> bool:
    for deco in node.decorator_list:
        if isinstance(deco, ast.Name) and deco.id == "dataclass":
            return True
        if isinstance(deco, ast.Attribute) and deco.attr == "dataclass":
            return True
        if isinstance(deco, ast.Call):
            if isinstance(deco.func, ast.Name) and deco.func.id == "dataclass":
                return True
            if isinstance(deco.func, ast.Attribute) and deco.func.attr == "dataclass":
                return True
    return False



def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")



def parse_module(path: Path) -> dict[str, Any]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    symbols: dict[str, dict[str, Any]] = {}
    calls: dict[str, set[str]] = {}

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            symbols[node.name] = {
                "summary": first_sentence(ast.get_docstring(node)),
                "obj_type": "Function",
                "doc": ast.get_docstring(node) or "",
            }
            called = set()
            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Name):
                        called.add(child.func.id)
                    elif isinstance(child.func, ast.Attribute):
                        called.add(child.func.attr)
            calls[node.name] = called
        elif isinstance(node, ast.ClassDef):
            typ = "Dataclass" if is_dataclass_node(node) else "Class"
            symbols[node.name] = {
                "summary": first_sentence(ast.get_docstring(node)),
                "obj_type": typ,
                "doc": ast.get_docstring(node) or "",
            }

    names = set(symbols)
    used_by: dict[str, set[str]] = {name: set() for name in names}
    for caller, callees in calls.items():
        for callee in callees:
            if callee in names:
                used_by.setdefault(callee, set()).add(caller)

    return {"symbols": symbols, "calls": calls, "used_by": used_by}


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
            return [
                {
                    "step_number": item["step_number"],
                    "step_name": item["step_name"],
                    "canonical_modules": [m.replace(".py", "") for m in item.get("canonical_modules", [])],
                }
                for item in reg
            ]
    return []


def resolve_step(symbol: Symbol, step_modules: dict[int, list[str]]) -> int | None:
    if symbol.name in PUBLIC_CALLABLE_STEP_REGISTRY:
        return PUBLIC_CALLABLE_STEP_REGISTRY[symbol.name]
    for step, modules in step_modules.items():
        if symbol.module in modules:
            return step
    return None


def main() -> None:
    public = set(parse_public_exports())
    module_data = {p.stem: parse_module(p) for p in PKG_DIR.glob("*.py") if p.name != "__init__.py"}

    symbol_map: dict[str, Symbol] = {}
    for module, info in module_data.items():
        for name, meta in info["symbols"].items():
            symbol_map[f"{module}.{name}"] = Symbol(
                name=name,
                module=module,
                obj_type=meta["obj_type"],
                summary=meta["summary"],
                is_public=name in public,
                is_deprecated="deprecated" in meta["doc"].lower(),
                related_public=set(),
            )

    for module, info in module_data.items():
        for name in info["symbols"]:
            users = info["used_by"].get(name, set())
            related_public = {u for u in users if f"{module}.{u}" in symbol_map and symbol_map[f"{module}.{u}"].is_public}
            symbol_map[f"{module}.{name}"].related_public = related_public

    step_registry = parse_step_registry()
    step_modules = {s["step_number"]: s["canonical_modules"] for s in step_registry}
    step_titles = {s["step_number"]: s["step_name"] for s in step_registry}
    step_symbols: dict[int, list[Symbol]] = {s["step_number"]: [] for s in step_registry}
    other: list[Symbol] = []

    public_symbols = [s for s in symbol_map.values() if s.is_public]
    for symbol in public_symbols:
        step = resolve_step(symbol, step_modules)
        if step is None:
            other.append(symbol)
        else:
            step_symbols[step].append(symbol)

    MODULE_DIR.mkdir(parents=True, exist_ok=True)
    module_index_lines = [
        "# Module API Catalogue",
        "",
        "Generated module summaries with public exports and related internal helpers.",
        "",
        "| Module | Public callable count | Internal helper count | Main workflow step(s) | Description | Link |",
        "|---|---:|---:|---|---|---|",
    ]

    for module in sorted(module_data):
        info = module_data[module]
        module_md = MODULE_DIR / f"{module}.md"
        module_symbols = [s for s in symbol_map.values() if s.module == module]
        public_in_module = [s for s in module_symbols if s.is_public]
        related_helpers = [s for s in module_symbols if (not s.is_public and bool(s.related_public))]
        other_internal = [s for s in module_symbols if (not s.is_public and not s.related_public)]
        deprecated_count = sum(1 for s in module_symbols if s.is_deprecated)

        lines = [f"# `{module}` module", "", "## Module contents", ""]
        lines.append(f"- Public callables: {len(public_in_module)}")
        lines.append(f"- Related internal helpers: {len(related_helpers)}")
        lines.append(f"- Other internal objects: {len(other_internal)}")
        lines.append(f"- Deprecated objects: {deprecated_count}")
        if not public_in_module:
            lines.append("- **Internal module: no public exports from `__all__`.**")
        lines.extend(["", "| Name | Status | Type | Purpose | Used by / related public callable | API link |", "|---|---|---|---|---|---|"])

        for s in sorted(module_symbols, key=lambda x: x.name.lower()):
            if s.is_deprecated:
                status = "Deprecated"
            elif s.is_public:
                status = "Public"
            elif s.related_public:
                status = "Internal helper"
            else:
                status = "Internal"
            anchor = slug(s.name)
            related = ", ".join(f"[`{u}`](#{slug(u)})" for u in sorted(s.related_public)) if s.related_public else "—"
            lines.append(
                f"| [`{s.name}`](#{anchor}) | {status} | {s.obj_type} | {s.summary or '—'} | {related} | [Jump](#{anchor}) |"
            )

        lines.extend(["", "## Public callables from `__all__`", ""])
        if public_in_module:
            lines.extend(["| Callable | Type | Summary | Related helpers |", "|---|---|---|---|"])
            for s in sorted(public_in_module, key=lambda x: x.name.lower()):
                related = sorted([c for c in info["calls"].get(s.name, set()) if c in info["symbols"] and not c.startswith("__") and c != s.name and not symbol_map[f"{module}.{c}"].is_public])
                lines.append(f"| [`{s.name}`](#{slug(s.name)}) | {s.obj_type} | {s.summary or '—'} | {', '.join(f'[`{r}`](#{slug(r)})' for r in related) or '—'} |")
        else:
            lines.append("No public exports in this module.")

        lines.extend(["", "## Related internal helpers", ""])
        if related_helpers:
            lines.extend(["| Helper | Related public callables |", "|---|---|"])
            for helper in sorted(related_helpers, key=lambda x: x.name.lower()):
                users = ", ".join(f"[`{u}`](#{slug(u)})" for u in sorted(helper.related_public))
                lines.append(f"| [`{helper.name}`](#{slug(helper.name)}) | {users or '—'} |")
        else:
            lines.append("No related internal helpers detected.")

        lines.extend(["", "## Full module API", "", f"::: fabric_data_product_framework.{module}"])
        module_md.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

        module_steps = sorted({resolve_step(s, step_modules) for s in public_in_module if resolve_step(s, step_modules) is not None})
        step_labels = ", ".join(f"Step {n}" for n in module_steps) if module_steps else "Internal / not mapped"
        desc = next((s.summary for s in sorted(public_in_module, key=lambda x: x.name.lower()) if s.summary), "Internal utility module")
        label = f"`{module}`" if public_in_module else f"`{module}` (internal)"
        module_index_lines.append(
            f"| {label} | {len(public_in_module)} | {len(related_helpers)} | {step_labels} | {desc} | [Open]({module}.md) |"
        )

    (MODULE_DIR / "index.md").write_text("\n".join(module_index_lines) + "\n", encoding="utf-8", newline="\n")

    ref = ["# Callable Reference", "", "Generated step-first function catalogue sourced from `fabric_data_product_framework.__all__`.", ""]
    for step in sorted(step_titles):
        ref.append(f"## Step {step}: {step_titles[step]}")
        ref.append("")
        entries = sorted(step_symbols.get(step, []), key=lambda x: x.name.lower())
        if entries:
            ref.extend(["| Function / class | Module | Purpose | Related helpers | API link |", "|---|---|---|---|---|"])
            for s in entries:
                info = module_data[s.module]
                related = sorted([c for c in info["calls"].get(s.name, set()) if c in info["symbols"] and not symbol_map[f"{s.module}.{c}"].is_public])
                ref.append(
                    f"| [`{s.name}`](../api/modules/{s.module}.md#{slug(s.name)}) | [`{s.module}`](../api/modules/{s.module}.md) | {s.summary or '—'} | {', '.join(f'[`{r}`](../api/modules/{s.module}.md#{slug(r)})' for r in related) or '—'} | [API anchor](../api/modules/{s.module}.md#{slug(s.name)}) · [Module](../api/modules/{s.module}.md) |"
                )
        else:
            ref.append("No public callable currently mapped to this step.")
            if step in STEP_FALLBACK_NOTES:
                ref.extend(["", STEP_FALLBACK_NOTES[step]])
        ref.append("")
    if other:
        ref.extend(["## Other Utilities", ""])
        for s in sorted(other, key=lambda x: x.name.lower()):
            ref.append(f"- [`{s.name}`](../api/modules/{s.module}.md#{slug(s.name)}) ([`{s.module}`](../api/modules/{s.module}.md))")

    REFERENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    REFERENCE_PATH.write_text("\n".join(ref) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
