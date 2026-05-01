"""Generate per-symbol API reference pages from public surface (__all__)."""
from __future__ import annotations

from collections import defaultdict
import importlib

import mkdocs_gen_files

PACKAGE = "fabric_data_product_framework"
pkg = importlib.import_module(PACKAGE)

PUBLIC_SYMBOLS = list(getattr(pkg, "__all__", []))

MODULE_LABEL_OVERRIDES = {
    "governance_classifier": "governance",
    "data_contract": "contracts",
    "dq": "dq_workflow",
}

SYMBOL_SECTION_OVERRIDES = {
    "MVP_STEPS": "mvp_steps",
}

SECTION_DISPLAY_NAMES = {
    "fabric_notebook": "Fabric Notebook",
    "template_generator": "Template Generator",
    "lineage": "Lineage",
    "dq_workflow": "DQ Workflow",
    "governance": "Governance",
    "contracts": "Contracts",
    "drift_checkers": "Drift Checkers",
    "mvp_steps": "MVP Steps",
}

SECTION_ORDER = [
    "fabric_notebook",
    "template_generator",
    "lineage",
    "dq_workflow",
    "governance",
    "contracts",
    "drift_checkers",
    "mvp_steps",
]

symbols_by_section: dict[str, list[tuple[str, str]]] = defaultdict(list)

for symbol in PUBLIC_SYMBOLS:
    obj = getattr(pkg, symbol)
    module_name = getattr(obj, "__module__", PACKAGE)
    section = module_name.split(".")[-1]
    section = MODULE_LABEL_OVERRIDES.get(section, section)
    section = SYMBOL_SECTION_OVERRIDES.get(symbol, section)
    dotted_path = f"{module_name}.{symbol}"
    symbols_by_section[section].append((symbol, dotted_path))

for section, items in symbols_by_section.items():
    items.sort(key=lambda item: item[0].lower())
    for symbol, dotted_path in items:
        doc_path = f"reference/{section}/{symbol}.md"
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            fd.write(f"# `{symbol}`\n\n")
            fd.write(f"::: {dotted_path}\n")
            fd.write("    options:\n")
            fd.write("      show_root_heading: false\n")
            fd.write("      show_source: true\n")

ordered_sections = [section for section in SECTION_ORDER if section in symbols_by_section]
remaining_sections = sorted(set(symbols_by_section) - set(ordered_sections))
all_sections = ordered_sections + remaining_sections

with mkdocs_gen_files.open("reference/index.md", "w") as fd:
    fd.write("# Callable Reference\n\n")
    fd.write(
        "These callable reference pages are generated from "
        "`fabric_data_product_framework.__all__`.\n\n"
    )
    fd.write("Browse callables by section:\n\n")

    for section in all_sections:
        pretty = SECTION_DISPLAY_NAMES.get(section, section.replace("_", " ").title())
        fd.write(f"## {pretty}\n\n")
        for symbol, _ in symbols_by_section[section]:
            fd.write(f"- [`{symbol}`]({section}/{symbol}.md)\n")
        fd.write("\n")

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as fd:
    fd.write("- [Reference Home](index.md)\n")
    for section in all_sections:
        pretty = SECTION_DISPLAY_NAMES.get(section, section.replace("_", " ").title())
        fd.write(f"- {pretty}\n")
        for symbol, _ in symbols_by_section[section]:
            fd.write(f"  - [{symbol}]({section}/{symbol}.md)\n")
