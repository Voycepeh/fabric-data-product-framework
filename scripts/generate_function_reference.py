from __future__ import annotations

import ast
import importlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PKG_DIR = ROOT / "src" / "fabric_data_product_framework"
PACKAGE_NAME = "fabric_data_product_framework"
INIT_PATH = PKG_DIR / "__init__.py"
DOCS_METADATA_PATH = PKG_DIR / "docs_metadata.py"
REFERENCE_PATH = ROOT / "docs" / "reference" / "index.md"
MODULE_DIR = ROOT / "docs" / "api" / "modules"
STEP_FALLBACK_NOTES = {
    5: "No public callable is currently exported for this step. Use notebook prompts for AI-assisted rule drafting.",
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


def parse_docs_metadata() -> dict[str, dict[str, Any]]:
    tree = ast.parse(DOCS_METADATA_PATH.read_text(encoding="utf-8"))
    for node in tree.body:
        is_assign = isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "PUBLIC_SYMBOL_DOCS" for t in node.targets
        )
        is_annassign = (
            isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "PUBLIC_SYMBOL_DOCS"
        )
        if (is_assign or is_annassign) and node.value is not None:
            rows = ast.literal_eval(node.value)
            return {row["symbol_name"]: row for row in rows}
    raise RuntimeError("Could not parse PUBLIC_SYMBOL_DOCS from docs_metadata.py")


def parse_workflow_step_docs() -> list[dict[str, Any]]:
    tree = ast.parse(DOCS_METADATA_PATH.read_text(encoding="utf-8"))
    for node in tree.body:
        is_assign = isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "WORKFLOW_STEP_DOCS" for t in node.targets
        )
        is_annassign = isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "WORKFLOW_STEP_DOCS"
        if (is_assign or is_annassign) and node.value is not None:
            return ast.literal_eval(node.value)
    raise RuntimeError("Could not parse WORKFLOW_STEP_DOCS from docs_metadata.py")


def internal_helper_link(module: str, helper: str) -> str:
    """Return docs-relative link target for an internal helper page."""
    return f"../../reference/internal/{module}/{helper}.md"


def main() -> None:
    public = parse_public_exports()
    module_data = {p.stem: parse_module(p) for p in PKG_DIR.glob("*.py") if p.name != "__init__.py"}
    pkg = importlib.import_module(PACKAGE_NAME)

    symbol_map: dict[str, Symbol] = {}
    for name in public:
        obj = getattr(pkg, name)
        obj_module = getattr(obj, "__module__", PACKAGE_NAME).split(".")[-1]
        for module, info in module_data.items():
            if module != obj_module:
                continue
            if name in info["functions"]:
                symbol_map[name] = Symbol(name, module, "function", info["functions"][name])
                break
            if name in info["classes"]:
                symbol_map[name] = Symbol(name, module, "class", info["classes"][name])
                break

    step_registry = parse_step_registry()
    docs_metadata = parse_docs_metadata()
    step_docs = parse_workflow_step_docs()
    step_titles = {s["step_number"]: s["step_name"] for s in step_registry}
    step_slugs = {int(step["number"]): step["slug"] for step in step_docs}
    step_symbols: dict[int, list[Symbol]] = {s["step_number"]: [] for s in step_registry}

    missing_metadata = sorted(name for name in public if name not in docs_metadata)
    if missing_metadata:
        raise RuntimeError("Missing PUBLIC_SYMBOL_DOCS entries for exported symbols: " + ", ".join(missing_metadata))

    unknown_metadata = sorted(name for name in docs_metadata if name not in public)
    if unknown_metadata:
        raise RuntimeError("PUBLIC_SYMBOL_DOCS contains symbols not exported in __all__: " + ", ".join(unknown_metadata))

    for symbol in symbol_map.values():
        meta = docs_metadata[symbol.name]
        if meta["module"] != symbol.module:
            raise RuntimeError(
                f"Metadata module mismatch for {symbol.name}: expected {symbol.module}, found {meta['module']}"
            )
        if meta["kind"] != symbol.obj_type:
            raise RuntimeError(f"Metadata kind mismatch for {symbol.name}: expected {symbol.obj_type}, found {meta['kind']}")
        step = meta["workflow_step"]
        if step not in step_symbols:
            raise RuntimeError(f"Invalid workflow_step {step} for {symbol.name}; expected one of {sorted(step_symbols)}")
        symbol.summary = meta.get("summary_override") or symbol.summary
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
            '<div class="api-status-block">\n'
            '  <span class="api-chip api-chip-internal">Internal-only module</span>\n'
            '  <div class="api-chip-subtitle">Not intended as a primary user-facing API surface.</div>\n'
            '</div>'
            if is_internal_only
            else '<div class="api-status-block">\n'
            '  <span class="api-chip api-chip-module">Module overview</span>\n'
            '</div>'
        )
        lines = [title, "", status_banner, "", "## Public callables from `__all__`", ""]
        if public_in_module:
            lines.extend(["| Callable | Type | Summary | Related helpers |", "|---|---|---|---|"])
            for s in sorted(public_in_module, key=lambda x: x.name.lower()):
                related = sorted([c for c in info["calls"].get(s.name, set()) if c in info["functions"] and c.startswith("_")])
                lines.append(
                    f"| [`{s.name}`](#{s.name}) | {s.obj_type} | {s.summary or '—'} | "
                    f"{', '.join(f'[`{r}`]({internal_helper_link(module, r)}) (internal)' for r in related) or '—'} |"
                )
        else:
            lines.append("No public exports in this module.")
        if public_in_module:
            lines.extend(["", "## Public callable details", ""])
            for s in sorted(public_in_module, key=lambda x: x.name.lower()):
                lines.extend([f"### {s.name}", "", f"::: fabric_data_product_framework.{module}.{s.name}", ""])

        internal_fns = sorted([f for f in info["functions"] if f.startswith("_")])
        if internal_fns and public_in_module:
            lines.extend(['??? note "Internal helpers (collapsed)"', "", "    Internal helpers are documented separately for maintainers:", ""])
            for helper in internal_fns:
                users = sorted([u for u in info["used_by"].get(helper, set()) if u in {p.name for p in public_in_module}])
                relation = f" (used by: {', '.join(f'`{u}`' for u in users)})" if users else ""
                lines.append(f"    - [`{helper}`]({internal_helper_link(module, helper)}){relation}")

        if public_in_module:
            for s in sorted(public_in_module, key=lambda x: x.name.lower()):
                expected_link = f"[`{s.name}`](#{s.name})"
                if not any(expected_link in line for line in lines):
                    raise RuntimeError(f"Missing callable table link for {module}.{s.name}")
                if not any(line.strip() == f"### {s.name}" for line in lines):
                    raise RuntimeError(f"Missing callable section anchor for {module}.{s.name}")
        if any("## Full module API" in line for line in lines):
            raise RuntimeError(f"Full module API section should not be rendered for {module}")
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
                step_slug = step_slugs.get(step)
                symbol_link = f"./{step_slug}/{s.name}/" if step_slug else f"../api/modules/{s.module}/#{s.name}"
                ref.append(
                    f"| [`{s.name}`]({symbol_link}) | `{s.module}` | {s.summary or '—'} | "
                    f"{', '.join(f'[`{r}`](./internal/{s.module}/{r}.md) (internal)' for r in related) or '—'} | "
                    f"[module overview](../api/modules/{s.module}/) |"
                )
        else:
            ref.append("No public callable currently mapped to this step.")
            if step in STEP_FALLBACK_NOTES:
                ref.extend(["", STEP_FALLBACK_NOTES[step]])
        ref.append("")
    REFERENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    REFERENCE_PATH.write_text("\n".join(ref) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
