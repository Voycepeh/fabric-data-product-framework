"""Generate workflow-aligned API reference pages from public surface (__all__)."""
from __future__ import annotations

import ast
from pathlib import Path

import mkdocs_gen_files

PACKAGE = "fabricops_kit"
PKG_DIR = Path(__file__).resolve().parents[1] / "src" / PACKAGE
INIT_PATH = PKG_DIR / "__init__.py"
DOCS_METADATA_PATH = PKG_DIR / "docs_metadata.py"


def _read_literal(path: Path, name: str):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        is_assign = isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets)
        is_ann = isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == name
        if (is_assign or is_ann) and node.value is not None:
            return ast.literal_eval(node.value)
    raise RuntimeError(f"Missing literal {name} in {path}")


def _public_symbols() -> list[str]:
    return list(_read_literal(INIT_PATH, "__all__"))


def _symbol_module_index() -> dict[str, str]:
    mapping: dict[str, str] = {}
    for module_path in sorted(PKG_DIR.glob("*.py")):
        if module_path.name in {"__init__.py", "docs_metadata.py"}:
            continue
        module = module_path.stem
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                mapping[node.name] = module
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        mapping[target.id] = module
    return mapping


PUBLIC_SYMBOLS = _public_symbols()
PUBLIC_SYMBOL_DOCS = _read_literal(DOCS_METADATA_PATH, "PUBLIC_SYMBOL_DOCS")
WORKFLOW_STEPS = _read_literal(DOCS_METADATA_PATH, "WORKFLOW_STEP_DOCS")
module_index = _symbol_module_index()

workflow_step_by_symbol = {row["symbol_name"]: row["workflow_step"] for row in PUBLIC_SYMBOL_DOCS if row.get("kind") == "function"}
symbols_by_step: dict[str, list[tuple[str, str]]] = {str(step["number"]): [] for step in WORKFLOW_STEPS}
for symbol in PUBLIC_SYMBOLS:
    if workflow_step_by_symbol.get(symbol) is None:
        continue
    module_name = module_index.get(symbol)
    if module_name is None:
        raise RuntimeError(f"Unable to resolve source module for symbol '{symbol}'")
    dotted_path = f"{PACKAGE}.{module_name}.{symbol}"
    step_key = str(workflow_step_by_symbol[symbol])
    symbols_by_step[step_key].append((symbol, dotted_path))

for items in symbols_by_step.values():
    items.sort(key=lambda item: item[0].lower())


def _load_internal_helpers() -> dict[str, list[str]]:
    """Return module -> sorted internal helper names for package modules."""
    module_helpers: dict[str, list[str]] = {}
    for module_path in sorted(PKG_DIR.glob("*.py")):
        if module_path.name in {"__init__.py", "docs_metadata.py"}:
            continue
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        helpers = sorted(
            node.name
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name.startswith("_")
        )
        if helpers:
            module_helpers[module_path.stem] = helpers
    return module_helpers


internal_helpers_by_module = _load_internal_helpers()

for step in WORKFLOW_STEPS:
    step_number = str(step["number"])
    step_slug = step["slug"]
    for symbol, dotted_path in symbols_by_step.get(step_number, []):
        doc_path = f"reference/{step_slug}/{symbol}.md"
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            fd.write(f"# `{symbol}`\n\n")
            fd.write('<div class="api-status-block">\n')
            fd.write('  <span class="api-chip api-chip-public">Public callable</span>\n')
            fd.write('</div>\n\n')
            fd.write(f"::: {dotted_path}\n")
            fd.write("    options:\n")
            fd.write("      show_root_heading: false\n")
            fd.write("      show_source: true\n")
            fd.write("      docstring_style: numpy\n")
            fd.write("      docstring_section_style: table\n")

for module_name, helpers in internal_helpers_by_module.items():
    for helper_name in helpers:
        doc_path = f"reference/internal/{module_name}/{helper_name}.md"
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            fd.write(f"# `{helper_name}`\n\n")
            fd.write('<div class="api-status-block">\n')
            fd.write('  <span class="api-chip api-chip-internal">Internal helper</span>\n')
            fd.write('  <div class="api-chip-subtitle">This page documents an internal implementation helper, not a primary public API.</div>\n')
            fd.write('</div>\n\n')
            fd.write(f"::: {PACKAGE}.{module_name}.{helper_name}\n")
            fd.write("    options:\n")
            fd.write("      show_root_heading: false\n")
            fd.write("      show_source: true\n")
            fd.write("      docstring_style: numpy\n")
            fd.write("      docstring_section_style: table\n")

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as fd:
    fd.write("- [Reference Home](index.md)\n")
    for step in WORKFLOW_STEPS:
        step_number = str(step["number"])
        step_slug = step["slug"]
        step_title = step["title"]
        fd.write(f"- Step {step_number}: {step_title}\n")
        for symbol, _ in symbols_by_step.get(step_number, []):
            fd.write(f"  - [{symbol}]({step_slug}/{symbol}.md)\n")
    if internal_helpers_by_module:
        fd.write("- Internal Helpers\n")
        for module_name, helpers in sorted(internal_helpers_by_module.items()):
            fd.write(f"  - {module_name}\n")
            for helper_name in helpers:
                fd.write(f"    - [{helper_name}](internal/{module_name}/{helper_name}.md)\n")
