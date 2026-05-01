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
}

SYMBOL_SECTION_OVERRIDES = {
    "MVP_STEPS": "mvp_steps",
}

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

with mkdocs_gen_files.open("reference/index.md", "w") as fd:
    fd.write("# Callable Reference\n\n")
    fd.write(
        "Generated API pages for each public callable in "
        "`fabric_data_product_framework.__all__`.\n"
    )

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as fd:
    fd.write("- [Reference Home](index.md)\n")
    for section in sorted(symbols_by_section):
        pretty = section.replace("_", " ").title()
        fd.write(f"- {pretty}\n")
        for symbol, _ in sorted(symbols_by_section[section], key=lambda item: item[0].lower()):
            fd.write(f"  - [{symbol}]({section}/{symbol}.md)\n")
