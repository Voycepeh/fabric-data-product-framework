"""Generate workflow-aligned API reference pages from public surface (__all__)."""
from __future__ import annotations

import ast
import importlib
from pathlib import Path

import mkdocs_gen_files
from fabricops_kit.docs_metadata import PUBLIC_SYMBOL_DOCS, WORKFLOW_STEP_DOCS

PACKAGE = "fabricops_kit"
pkg = importlib.import_module(PACKAGE)

PUBLIC_SYMBOLS = list(getattr(pkg, "__all__", []))

WORKFLOW_STEPS = WORKFLOW_STEP_DOCS
workflow_step_by_symbol = {row["symbol_name"]: row["workflow_step"] for row in PUBLIC_SYMBOL_DOCS}
symbols_by_step: dict[str, list[tuple[str, str]]] = {str(step["number"]): [] for step in WORKFLOW_STEPS}
for symbol in PUBLIC_SYMBOLS:
    if workflow_step_by_symbol.get(symbol) is None:
        continue
    obj = getattr(pkg, symbol)
    module_name = getattr(obj, "__module__", PACKAGE)
    dotted_path = f"{module_name}.{symbol}"
    step_key = str(workflow_step_by_symbol[symbol])
    symbols_by_step[step_key].append((symbol, dotted_path))

for items in symbols_by_step.values():
    items.sort(key=lambda item: item[0].lower())


def _load_internal_helpers() -> dict[str, list[str]]:
    """Return module -> sorted internal helper names for package modules."""
    package_root = Path(__file__).resolve().parents[1] / "src" / PACKAGE
    module_helpers: dict[str, list[str]] = {}
    for module_path in sorted(package_root.glob("*.py")):
        if module_path.name == "__init__.py":
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
            fd.write("<div class=\"api-status-block\">\n")
            fd.write("  <span class=\"api-chip api-chip-public\">Public callable</span>\n")
            fd.write("</div>\n\n")
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
            fd.write("<div class=\"api-status-block\">\n")
            fd.write("  <span class=\"api-chip api-chip-internal\">Internal helper</span>\n")
            fd.write("  <div class=\"api-chip-subtitle\">This page documents an internal implementation helper, not a primary public API.</div>\n")
            fd.write("</div>\n\n")
            fd.write(f"::: {PACKAGE}.{module_name}.{helper_name}\n")
            fd.write("    options:\n")
            fd.write("      show_root_heading: false\n")
            fd.write("      show_source: true\n")
            fd.write("      docstring_style: numpy\n")
            fd.write("      docstring_section_style: table\n")

# NOTE:
# `docs/reference/index.md` is intentionally maintained by hand as the
# Function Reference landing page and must never be generated here.

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
