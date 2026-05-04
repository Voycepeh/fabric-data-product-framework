from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PKG_DIR = ROOT / "src" / "fabricops_kit"
PACKAGE_NAME = "fabricops_kit"
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
    importance: str = "Optional"
    purpose: str = ""


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


def public_reference_link(symbol: str, docs_metadata: dict[str, dict[str, Any]], step_slugs: dict[int, str]) -> str:
    """Return docs-relative link target for a public callable reference page."""
    if symbol not in docs_metadata:
        raise RuntimeError(f"Missing PUBLIC_SYMBOL_DOCS entry for exported symbol: {symbol}")
    step = docs_metadata[symbol].get("workflow_step")
    if step is None:
        raise RuntimeError(f"Missing workflow_step metadata for exported symbol: {symbol}")
    step_slug = step_slugs.get(step)
    if not step_slug:
        raise RuntimeError(f"Missing WORKFLOW_STEP_DOCS slug mapping for workflow step {step} ({symbol})")
    return f"../../reference/{step_slug}/{symbol}.md"


def main() -> None:
    public = parse_public_exports()
    module_data = {p.stem: parse_module(p) for p in PKG_DIR.glob("*.py") if p.name != "__init__.py"}

    step_registry = parse_step_registry()
    docs_metadata = parse_docs_metadata()
    step_docs = parse_workflow_step_docs()
    step_titles = {s["step_number"]: s["step_name"] for s in step_registry}
    step_slugs = {int(step["number"]): step["slug"] for step in step_docs}
    step_symbols: dict[int, list[Symbol]] = {s["step_number"]: [] for s in step_registry}
    mapped_symbols: set[str] = set()

    missing_metadata = sorted(name for name in public if name not in docs_metadata)
    if missing_metadata:
        raise RuntimeError("Missing PUBLIC_SYMBOL_DOCS entries for exported symbols: " + ", ".join(missing_metadata))

    unknown_metadata = sorted(name for name in docs_metadata if name not in public)
    if unknown_metadata:
        raise RuntimeError("PUBLIC_SYMBOL_DOCS contains symbols not exported in __all__: " + ", ".join(unknown_metadata))

    symbol_map: dict[str, Symbol] = {}
    for name in public:
        preferred_module = docs_metadata[name]["module"]
        modules_to_check = [preferred_module] + [m for m in module_data if m != preferred_module]
        for module in modules_to_check:
            info = module_data[module]
            if name in info["functions"]:
                symbol_map[name] = Symbol(name, module, "function", info["functions"][name])
                break
            if name in info["classes"]:
                symbol_map[name] = Symbol(name, module, "class", info["classes"][name])
                break
        if name not in symbol_map:
            raise RuntimeError(f"Could not resolve exported symbol {name} to a module-level function/class.")

    for symbol in symbol_map.values():
        meta = docs_metadata[symbol.name]
        if meta["module"] != symbol.module:
            raise RuntimeError(
                f"Metadata module mismatch for {symbol.name}: expected {symbol.module}, found {meta['module']}"
            )
        if meta["kind"] != symbol.obj_type:
            raise RuntimeError(f"Metadata kind mismatch for {symbol.name}: expected {symbol.obj_type}, found {meta['kind']}")
        step = meta.get("workflow_step")
        if step is not None and step not in step_symbols:
            raise RuntimeError(f"Invalid workflow_step {step} for {symbol.name}; expected one of {sorted(step_symbols)}")
        symbol.summary = meta.get("summary_override") or symbol.summary
        symbol.purpose = meta.get("purpose") or symbol.summary or "—"
        symbol.importance = meta.get("importance") or ("Essential" if step is not None and int(step) <= 7 else "Optional")
        if symbol.importance not in {"Essential", "Optional"}:
            raise RuntimeError(f"Invalid importance {symbol.importance!r} for {symbol.name}; expected Essential or Optional")
        if step is not None:
            step_symbols[step].append(symbol)
            mapped_symbols.add(symbol.name)

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
                workflow_step = docs_metadata[s.name].get("workflow_step")
                callable_link = (
                    public_reference_link(s.name, docs_metadata, step_slugs)
                    if workflow_step is not None
                    else f"../modules/{module}/#{s.name}"
                )
                lines.append(
                    f"| [`{s.name}`]({callable_link}) | {s.obj_type} | {s.summary or '—'} | "
                    f"{', '.join(f'[`{r}`]({internal_helper_link(module, r)}) (internal)' for r in related) or '—'} |"
                )
        else:
            lines.append("No public exports in this module.")
        lines.extend(["", "## Internal helpers", ""])
        internal_fns = sorted([f for f in info["functions"] if f.startswith("_")])
        if internal_fns:
            lines.extend(["| Helper | Related public callables |", "|---|---|"])
            for helper in internal_fns:
                users = sorted([u for u in info["used_by"].get(helper, set()) if u in {p.name for p in public_in_module}])
                users_links = ", ".join(f"[`{u}`]({public_reference_link(u, docs_metadata, step_slugs)})" for u in users) or "—"
                lines.append(f"| [`{helper}`]({internal_helper_link(module, helper)}) | {users_links} |")
        else:
            lines.append("No module-level internal helpers detected.")

        if public_in_module:
            for s in sorted(public_in_module, key=lambda x: x.name.lower()):
                workflow_step = docs_metadata[s.name].get("workflow_step")
                expected_target = (
                    public_reference_link(s.name, docs_metadata, step_slugs)
                    if workflow_step is not None
                    else f"../modules/{module}/#{s.name}"
                )
                expected_link = f"[`{s.name}`]({expected_target})"
                if not any(expected_link in line for line in lines):
                    raise RuntimeError(f"Missing callable table link for {module}.{s.name}")
                if f"../../reference/{module}/{s.name}.md" in "\n".join(lines):
                    raise RuntimeError(
                        f"Found deprecated module-path public link for {module}.{s.name}; expected workflow-step slug path."
                    )
        for helper in internal_fns:
            expected_helper_link = f"[`{helper}`]({internal_helper_link(module, helper)})"
            if not any(expected_helper_link in line for line in lines):
                raise RuntimeError(f"Missing internal helper link for {module}.{helper}")
        if any("## Public callable details" in line for line in lines):
            raise RuntimeError(f"Public callable details section should not be rendered for {module}")
        if any("## Full module API" in line for line in lines):
            raise RuntimeError(f"Full module API section should not be rendered for {module}")
        if any(line.strip().startswith("::: fabricops_kit.") for line in lines):
            raise RuntimeError(f"Mkdocstrings directives should not be rendered on module page for {module}")
        module_md.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        if not is_internal_only:
            module_index_lines.append(f"- [`{module}`]({module}.md)")
        else:
            module_index_lines.append(f"- [`{module}`]({module}.md) *(internal-only)*")

    (MODULE_DIR / "index.md").write_text("\n".join(module_index_lines) + "\n", encoding="utf-8", newline="\n")

    ref = ["# Callable Functions", "", "Generated step-first catalogue of callable functions sourced from `fabricops_kit.__all__`.", ""]
    ref.extend(["## Modules", "", "| Module |", "|---|"])
    for module in sorted(module_data):
        ref.append(
            f"| <a class=\"api-chip api-chip-module api-chip-link\" href=\"../api/modules/{module}/\" title=\"Open {module} module page\" aria-label=\"Open {module} module page\">{module}</a> |"
        )
    ref.append("")
    for step in sorted(step_titles):
        ref.append(f"## Step {step}: {step_titles[step]}")
        ref.append("")
        entries = sorted(step_symbols.get(step, []), key=lambda x: x.name.lower())
        if entries:
            ref.extend(["| Function / class | Module | Importance | Purpose | Related helpers |", "|---|---|---|---|---|"])
            for s in entries:
                info = module_data[s.module]
                related = sorted([c for c in info["calls"].get(s.name, set()) if c in info["functions"] and c.startswith("_")])
                step_slug = step_slugs.get(step)
                symbol_link = f"./{step_slug}/{s.name}/" if step_slug else f"../api/modules/{s.module}/#{s.name}"
                ref.append(
                    f"| [`{s.name}`]({symbol_link}) | <a class=\"api-chip api-chip-module api-chip-link\" href=\"../api/modules/{s.module}/\" title=\"Open {s.module} module page\" aria-label=\"Open {s.module} module page\">{s.module}</a> | {s.importance} | {s.purpose or '—'} | "
                    f"{', '.join(f'[`{r}`](./internal/{s.module}/{r}.md) (internal)' for r in related) or '—'} |"
                )
        else:
            ref.append("No public callable currently mapped to this step.")
            if step in STEP_FALLBACK_NOTES:
                ref.extend(["", STEP_FALLBACK_NOTES[step]])
        ref.append("")
    unmapped = sorted((set(symbol_map) - mapped_symbols), key=str.lower)
    ref.extend(
        [
            "## Other exported callables",
            "",
            "These callables are exported by `fabricops_kit.__all__` but are not currently mapped to a lifecycle step. They are listed here so the public reference remains complete.",
            "",
        ]
    )
    if unmapped:
        ref.extend(["| Function / class | Module | Importance | Purpose | Related helpers |", "|---|---|---|---|---|"])
        for name in unmapped:
            s = symbol_map[name]
            info = module_data[s.module]
            related = sorted([c for c in info["calls"].get(s.name, set()) if c in info["functions"] and c.startswith("_")])
            ref.append(
                f"| [`{s.name}`](../api/modules/{s.module}/) | <a class=\"api-chip api-chip-module api-chip-link\" href=\"../api/modules/{s.module}/\" title=\"Open {s.module} module page\" aria-label=\"Open {s.module} module page\">{s.module}</a> | {s.importance} | {s.purpose or s.summary or '—'} | "
                f"{', '.join(f'[`{r}`](./internal/{s.module}/{r}.md) (internal)' for r in related) or '—'} |"
            )
    else:
        ref.append("No unmapped exported callables.")
    ref.append("")
    REFERENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    REFERENCE_PATH.write_text("\n".join(ref) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
