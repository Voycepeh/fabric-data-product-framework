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
    7: "No public callable is currently exported for this step. Use notebook prompts and human review as defined in the MVP runbook.",
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
    internal = {n for n in names if n.startswith("_")}
    for caller, callees in calls.items():
        for callee in names:
            if callee in callees:
                used_by.setdefault(callee, set()).add(caller)
    return {"functions": functions, "classes": classes, "calls": calls, "used_by": used_by, "internal": internal}


def parse_public_exports() -> list[str]:
    tree = ast.parse(INIT_PATH.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            if any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets):
                if isinstance(node.value, ast.List):
                    return [elt.value for elt in node.value.elts if isinstance(elt, ast.Constant) and isinstance(elt.value, str)]
    raise RuntimeError("Could not parse __all__ from __init__.py")


def parse_step_registry() -> list[dict[str, Any]]:
    path = PKG_DIR / "handover.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        is_registry_assign = isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "MVP_STEP_REGISTRY" for t in node.targets
        )
        is_registry_annassign = isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "MVP_STEP_REGISTRY"
        if is_registry_assign or is_registry_annassign:
            value = node.value
            if value is None:
                continue
            reg = ast.literal_eval(value)
            out: list[dict[str, Any]] = []
            for item in reg:
                out.append({
                    "step_number": item["step_number"],
                    "step_name": item["step_name"],
                    "canonical_modules": [m.replace(".py", "") for m in item.get("canonical_modules", [])],
                })
            return out
    return []


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
    step_modules = {step["step_number"]: step["canonical_modules"] for step in step_registry}
    step_titles = {step["step_number"]: step["step_name"] for step in step_registry}
    step_symbols: dict[int, list[Symbol]] = {step["step_number"]: [] for step in step_registry}
    other: list[Symbol] = []
    for s in symbol_map.values():
        placed = False
        for step, modules in step_modules.items():
            if s.module in modules:
                step_symbols[step].append(s)
                placed = True
                break
        if not placed:
            other.append(s)

    MODULE_DIR.mkdir(parents=True, exist_ok=True)
    module_index_lines = ["# Module API Catalogue", "", "Generated module summaries with public exports and related internal helpers.", ""]
    for module in sorted(module_data):
        info = module_data[module]
        module_md = MODULE_DIR / f"{module}.md"
        public_in_module = [s for s in symbol_map.values() if s.module == module]
        lines = [f"# `{module}` module", ""]
        lines.append("## Public callables from `__all__`")
        lines.append("")
        if public_in_module:
            lines.append("| Callable | Type | Summary | Related helpers |")
            lines.append("|---|---|---|---|")
            for s in sorted(public_in_module, key=lambda x: x.name.lower()):
                related = sorted([c for c in info["calls"].get(s.name, set()) if c in info["functions"] and c.startswith("_")])
                lines.append(f"| `{s.name}` | {s.obj_type} | {s.summary or '—'} | {', '.join(f'`{r}` (internal)' for r in related) or '—'} |")
        else:
            lines.append("No public exports in this module.")
        lines.append("\n## Internal helpers (module-level)\n")
        internal_fns = sorted([f for f in info["functions"] if f.startswith("_")])
        if internal_fns:
            lines.append("| Helper | Related public callables |")
            lines.append("|---|---|")
            for helper in internal_fns:
                users = sorted([u for u in info["used_by"].get(helper, set()) if u in {p.name for p in public_in_module}])
                lines.append(f"| `{helper}` | {', '.join(f'`{u}`' for u in users) or '—'} |")
        else:
            lines.append("No module-level internal helpers detected.")
        lines.append("\n## Full module API\n")
        lines.append(f"::: fabric_data_product_framework.{module}")
        module_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
        module_index_lines.append(f"- [`{module}`]({module}.md)")

    (MODULE_DIR / "index.md").write_text("\n".join(module_index_lines) + "\n", encoding="utf-8")

    ref = ["# Callable Reference", "", "Generated step-first function catalogue sourced from `fabric_data_product_framework.__all__`.", ""]
    for step in sorted(step_titles):
        ref.append(f"## Step {step}: {step_titles[step]}")
        ref.append("")
        entries = sorted(step_symbols.get(step, []), key=lambda x: x.name.lower())
        if entries:
            ref.append("| Function / class | Module | Purpose | Related helpers | API link |")
            ref.append("|---|---|---|---|---|")
            for s in entries:
                info = module_data[s.module]
                related = sorted([c for c in info["calls"].get(s.name, set()) if c in info["functions"] and c.startswith("_")])
                api_link = f"[module API](../api/modules/{s.module}.md)"
                ref.append(f"| `{s.name}` | `{s.module}` | {s.summary or '—'} | {', '.join(f'`{r}` (internal)' for r in related) or '—'} | {api_link} |")
        else:
            ref.append("No public callable currently mapped to this step.")
            if step in STEP_FALLBACK_NOTES:
                ref.append("")
                ref.append(STEP_FALLBACK_NOTES[step])
        ref.append("")
    if other:
        ref.append("## Other Utilities\n")
        for s in sorted(other, key=lambda x: x.name.lower()):
            ref.append(f"- `{s.name}` (`{s.module}`) → [module API](../api/modules/{s.module}.md)")
    REFERENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    REFERENCE_PATH.write_text("\n".join(ref) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
