"""Generate callable reference pages for MkDocs build."""
from __future__ import annotations

import ast
from pathlib import Path

import mkdocs_gen_files

PACKAGE = "fabricops_kit"
PKG_DIR = Path(__file__).resolve().parents[1] / "src" / PACKAGE
DOCS_METADATA_PATH = PKG_DIR / "docs_metadata.py"


def _read_literal(path: Path, name: str):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        is_assign = isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets)
        is_ann = isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == name
        if (is_assign or is_ann) and node.value is not None:
            return ast.literal_eval(node.value)
    raise RuntimeError(f"Missing literal {name} in {path}")


def _load_internal_helpers() -> dict[str, list[str]]:
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


public_symbol_docs = _read_literal(DOCS_METADATA_PATH, "PUBLIC_SYMBOL_DOCS")
internal_helpers_by_module = _load_internal_helpers()

for row in sorted(public_symbol_docs, key=lambda item: item["symbol_name"]):
    if row.get("kind") not in {"function", "class"}:
        continue
    symbol_name = row["symbol_name"]
    module_name = row["module"]
    doc_path = f"api/reference/{symbol_name}.md"
    with mkdocs_gen_files.open(doc_path, "w") as fd:
        fd.write(f"# `{symbol_name}`\n\n")
        fd.write(
            f"- **Template notebook:** `{row.get('template_notebook') or '—'}`\n"
            f"- **Template segment:** {row.get('template_segment') or '—'}\n"
            f"- **Role:** `{row.get('role') or 'optional'}`\n"
            f"- **Module:** `{module_name}`\n\n"
        )
        fd.write("## Focused callable dependency view\n\n")
        fd.write(
            f'<iframe src="../../../assets/callable-map.html?focus={symbol_name}&embed=1" '
            'title="Focused callable dependency explorer" '
            'scrolling="no" style="width:100%;height:320px;min-height:220px;border:1px solid #2a2f3a;border-radius:8px;overflow:hidden;display:block;"></iframe>\n\n'
        )
        fd.write(
            f"[Open full dependency explorer](../../../reference/callable-map/?focus={symbol_name})\n\n"
        )
        fd.write(f"::: {PACKAGE}.{module_name}.{symbol_name}\n")
        fd.write("    options:\n")
        fd.write("      show_root_heading: false\n")
        fd.write("      show_source: true\n")
        fd.write("      docstring_style: numpy\n")
        fd.write("      docstring_section_style: table\n")


for module_name, helpers in internal_helpers_by_module.items():
    for helper_name in helpers:
        doc_path = f"api/reference/internal/{module_name}/{helper_name}.md"
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
    if internal_helpers_by_module:
        fd.write("- Internal Helpers\n")
        for module_name, helpers in sorted(internal_helpers_by_module.items()):
            fd.write(f"  - {module_name}\n")
            for helper_name in helpers:
                fd.write(f"    - [{helper_name}](../api/reference/internal/{module_name}/{helper_name}.md)\n")
