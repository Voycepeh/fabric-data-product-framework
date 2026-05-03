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
REFERENCE_STEP_SLUGS = {
    1: "step-01-purpose-setup",
    2: "step-02-runtime-configuration",
    3: "step-03-source-declaration-paths",
    4: "step-04-source-ingestion-read-helpers",
    5: "step-05-source-profiling-metadata",
    6: "step-06-drift-checks",
    7: "step-07-ai-rule-generation-review",
    8: "step-08-quality-rule-execution",
    9: "step-09-core-transformation-business-logic",
    10: "step-10-technical-columns-write-prep",
    11: "step-11-output-write-metadata-logging",
    12: "step-12-governance-classification",
    13: "step-13-lineage-summary-handover",
}

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
    "scan_notebook_lineage": 12,
    "scan_notebook_cells": 12,
    "enrich_lineage_steps_with_ai": 12,
    "fallback_copilot_lineage_prompt": 12,
    "validate_lineage_steps": 12,
    "build_lineage_record_from_steps": 12,
    "build_lineage_from_notebook_code": 12,
    "build_lineage_handover_markdown": 12,
    "plot_lineage_steps": 12,
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


def parse_module(path: Path) -> dict[str, Any]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    functions: dict[str, str] = {}
    classes: dict[str, str] = {}
    calls: dict[str, set[str]] = {}
    used_by: dict[str, set[str]] = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            functions[node.name] = first_sentence(ast.get_docstring(node))
            called = set()
            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Name):
                        called.add(child.func.id)
                    elif isinstance(child.func, ast.Attribute):
                        called.add(child.func.attr)
            calls[node.name] = called
        elif isinstance(node, ast.ClassDef):
            classes[node.name] = first_sentence(ast.get_docstring(node))
    names = set(functions) | set(classes)
    for caller, callees in calls.items():
        for callee in names:
            if callee in callees:
                used_by.setdefault(callee, set()).add(caller)
    return {"functions": functions, "classes": classes, "calls": calls, "used_by": used_by}


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
    public = parse_public_exports()
    module_data = {p.stem: parse_module(p) for p in PKG_DIR.glob("*.py") if p.name != "__init__.py"}

    symbol_map: dict[str, Symbol] = {}
    for name in public:
        for module, info in module_data.items():
            if name in info["functions"]:
                symbol_map[name] = Symbol(name, module, "function", info["functions"][name])
                break
            if name in info["classes"]:
                symbol_map[name] = Symbol(name, module, "class", info["classes"][name])
                break

    step_registry = parse_step_registry()
    step_modules = {s["step_number"]: s["canonical_modules"] for s in step_registry}
    step_titles = {s["step_number"]: s["step_name"] for s in step_registry}
    step_symbols: dict[int, list[Symbol]] = {s["step_number"]: [] for s in step_registry}
    other: list[Symbol] = []

    for symbol in symbol_map.values():
        step = resolve_step(symbol, step_modules)
        if step is None:
            other.append(symbol)
        else:
            step_symbols[step].append(symbol)

    MODULE_DIR.mkdir(parents=True, exist_ok=True)
    module_index_lines = ["# Module API Catalogue", "", "Generated module summaries with public exports and related internal helpers.", ""]
    for module in sorted(module_data):
        info = module_data[module]
        module_md = MODULE_DIR / f"{module}.md"
        public_in_module = [s for s in symbol_map.values() if s.module == module]
        is_internal_only = not public_in_module
        title = f"# `{module}` module" if not is_internal_only else f"# `{module}` module (internal)"
        status_banner = (
            "!!! warning \"Internal-only module\"\n"
            "    Not intended as a primary user-facing API surface."
            if is_internal_only
            else "!!! info \"Module overview\"\n"
            "    This page summarizes public callables and related internal helpers."
        )
        lines = [title, "", status_banner, "", "## Public callables from `__all__`", ""]
        if public_in_module:
            lines.extend(["| Callable | Type | Summary | Related helpers |", "|---|---|---|---|"])
            for s in sorted(public_in_module, key=lambda x: x.name.lower()):
                related = sorted([c for c in info["calls"].get(s.name, set()) if c in info["functions"] and c.startswith("_")])
                lines.append(
                    f"| [`{s.name}`](#{s.name}) | {s.obj_type} | {s.summary or '—'} | "
                    f"{', '.join(f'`{r}` (internal)' for r in related) or '—'} |"
                )
        else:
            lines.append("No public exports in this module.")
        lines.extend(["", "## Internal helpers (module-level)", ""])
        internal_fns = sorted([f for f in info["functions"] if f.startswith("_")])
        if internal_fns:
            lines.extend(["| Helper | Related public callables |", "|---|---|"])
            for helper in internal_fns:
                users = sorted([u for u in info["used_by"].get(helper, set()) if u in {p.name for p in public_in_module}])
                lines.append(f"| `{helper}` | {', '.join(f'`{u}`' for u in users) or '—'} |")
        else:
            lines.append("No module-level internal helpers detected.")
        if not is_internal_only:
            lines.extend(["", "## Full module API", "", f"::: fabric_data_product_framework.{module}"])
        else:
            lines.extend(["", "## Full module API", "", "This module is internal-only and is intentionally excluded from full public API rendering."])
        module_md.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        if not is_internal_only:
            module_index_lines.append(f"- [`{module}`]({module}.md)")
        else:
            module_index_lines.append(f"- [`{module}`]({module}.md) *(internal-only)*")

    (MODULE_DIR / "index.md").write_text("\n".join(module_index_lines) + "\n", encoding="utf-8", newline="\n")

    ref = ["# Callable Reference", "", "Generated step-first function catalogue sourced from `fabric_data_product_framework.__all__`.", ""]
    for step in sorted(step_titles):
        ref.append(f"## Step {step}: {step_titles[step]}")
        ref.append("")
        entries = sorted(step_symbols.get(step, []), key=lambda x: x.name.lower())
        if entries:
            ref.extend(["| Function / class | Module | Purpose | Related helpers | Module page |", "|---|---|---|---|---|"])
            for s in entries:
                info = module_data[s.module]
                related = sorted([c for c in info["calls"].get(s.name, set()) if c in info["functions"] and c.startswith("_")])
                step_slug = REFERENCE_STEP_SLUGS.get(step)
                symbol_link = f"./{step_slug}/{s.name}.md" if step_slug else f"../api/modules/{s.module}.md#{s.name}"
                ref.append(
                    f"| [`{s.name}`]({symbol_link}) | `{s.module}` | {s.summary or '—'} | "
                    f"{', '.join(f'`{r}` (internal)' for r in related) or '—'} | "
                    f"[module overview](../api/modules/{s.module}.md) |"
                )
        else:
            ref.append("No public callable currently mapped to this step.")
            if step in STEP_FALLBACK_NOTES:
                ref.extend(["", STEP_FALLBACK_NOTES[step]])
        ref.append("")
    if other:
        ref.extend(["## Other Utilities", ""])
        for s in sorted(other, key=lambda x: x.name.lower()):
            ref.append(f"- [`{s.name}`](./other-utilities/{s.name}.md) (`{s.module}`) → [module overview](../api/modules/{s.module}.md)")

    REFERENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    REFERENCE_PATH.write_text("\n".join(ref) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
