"""Generate workflow-aligned API reference pages from public surface (__all__)."""
from __future__ import annotations

from collections import defaultdict
import importlib

import mkdocs_gen_files

PACKAGE = "fabric_data_product_framework"
pkg = importlib.import_module(PACKAGE)

PUBLIC_SYMBOLS = list(getattr(pkg, "__all__", []))

WORKFLOW_STEPS = [
    {
        "number": 1,
        "slug": "step-01-purpose-setup",
        "title": "Purpose, steward, and notebook setup",
    },
    {
        "number": 2,
        "slug": "step-02-runtime-configuration",
        "title": "Environment and runtime configuration",
    },
    {
        "number": 3,
        "slug": "step-03-source-declaration-paths",
        "title": "Source declaration and Fabric path resolution",
    },
    {
        "number": 4,
        "slug": "step-04-source-ingestion-read-helpers",
        "title": "Source ingestion and read helpers",
    },
    {
        "number": 5,
        "slug": "step-05-source-profiling-metadata",
        "title": "Source profiling and metadata capture",
    },
    {
        "number": 6,
        "slug": "step-06-drift-checks",
        "title": "Schema drift and data drift checks",
    },
    {
        "number": 7,
        "slug": "step-07-ai-rule-generation-review",
        "title": "AI-assisted rule generation and human review",
        "note": "No public callable is currently exposed for this step. In the MVP workflow, this step is currently handled through notebook prompts and human review.",
    },
    {
        "number": 8,
        "slug": "step-08-quality-rule-execution",
        "title": "Data quality rule execution",
    },
    {
        "number": 9,
        "slug": "step-09-core-transformation-business-logic",
        "title": "Core transformation and business logic support",
    },
    {
        "number": 10,
        "slug": "step-10-technical-columns-write-prep",
        "title": "Standard technical columns and write preparation",
        "note": "No public callable is currently exposed for this step yet. Technical write preparation is currently handled inside the notebook pattern and output helpers.",
    },
    {
        "number": 11,
        "slug": "step-11-output-write-metadata-logging",
        "title": "Output write, output profiling, and metadata logging",
    },
    {
        "number": 12,
        "slug": "step-12-governance-classification",
        "title": "Governance classification and sensitivity handling",
    },
    {
        "number": 13,
        "slug": "step-13-lineage-summary-handover",
        "title": "Lineage, run summary, and handover documentation",
    },
]

SYMBOL_WORKFLOW_STEP = {
    "validate_notebook_name": 1,
    "assert_notebook_name_valid": 1,
    "generate_run_id": 2,
    "build_runtime_context": 2,
    "load_fabric_config": 2,
    "Housepath": 3,
    "get_path": 3,
    "lakehouse_table_read": 4,
    "lakehouse_csv_read": 4,
    "lakehouse_parquet_read_as_spark": 4,
    "lakehouse_excel_read_as_spark": 4,
    "warehouse_read": 4,
    "profile_dataframe": 5,
    "summarize_profile": 5,
    "check_schema_drift": 6,
    "check_partition_drift": 6,
    "check_profile_drift": 6,
    "summarize_drift_results": 6,
    "run_quality_rules": 8,
    "load_data_contract": 9,
    "run_data_product": 9,
    "warehouse_write": 11,
    "write_multiple_metadata_outputs": 11,
    "classify_columns": 12,
    "summarize_governance_classifications": 12,
    "LineageRecorder": 13,
    "build_lineage_records": 13,
    "generate_mermaid_lineage": 13,
    "build_transformation_summary_markdown": 13,
    "build_run_summary": 13,
    "render_run_summary_markdown": 13,
}

symbols_by_step: dict[int, list[tuple[str, str]]] = defaultdict(list)
other_utilities: list[tuple[str, str]] = []

for symbol in PUBLIC_SYMBOLS:
    obj = getattr(pkg, symbol)
    module_name = getattr(obj, "__module__", PACKAGE)
    dotted_path = f"{module_name}.{symbol}"
    step_number = SYMBOL_WORKFLOW_STEP.get(symbol)
    if step_number is None:
        other_utilities.append((symbol, dotted_path))
    else:
        symbols_by_step[step_number].append((symbol, dotted_path))

for items in symbols_by_step.values():
    items.sort(key=lambda item: item[0].lower())
other_utilities.sort(key=lambda item: item[0].lower())

for step in WORKFLOW_STEPS:
    step_number = step["number"]
    step_slug = step["slug"]
    for symbol, dotted_path in symbols_by_step.get(step_number, []):
        doc_path = f"reference/{step_slug}/{symbol}.md"
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            fd.write(f"# `{symbol}`\n\n")
            fd.write(f"::: {dotted_path}\n")
            fd.write("    options:\n")
            fd.write("      show_root_heading: false\n")
            fd.write("      show_source: true\n")
            fd.write("      docstring_style: numpy\n")
            fd.write("      docstring_section_style: table\n")

for symbol, dotted_path in other_utilities:
    doc_path = f"reference/other-utilities/{symbol}.md"
    with mkdocs_gen_files.open(doc_path, "w") as fd:
        fd.write(f"# `{symbol}`\n\n")
        fd.write(f"::: {dotted_path}\n")
        fd.write("    options:\n")
        fd.write("      show_root_heading: false\n")
        fd.write("      show_source: true\n")
        fd.write("      docstring_style: numpy\n")
        fd.write("      docstring_section_style: table\n")

with mkdocs_gen_files.open("reference/index.md", "w") as fd:
    fd.write("# Callable Reference\n\n")
    fd.write(
        "The callable reference is arranged by the 13-step Fabric data product workflow, "
        "not by Python module name.\n\n"
    )

    for step in WORKFLOW_STEPS:
        step_number = step["number"]
        step_slug = step["slug"]
        step_title = step["title"]
        fd.write(f"## Step {step_number}: {step_title}\n\n")

        for symbol, _ in symbols_by_step.get(step_number, []):
            fd.write(f"- [`{symbol}`]({step_slug}/{symbol}.md)\n")

        note = step.get("note")
        if note:
            fd.write(f"\n{note}\n")

        fd.write("\n")

    if other_utilities:
        fd.write("## Other Utilities\n\n")
        for symbol, _ in other_utilities:
            fd.write(f"- [`{symbol}`](other-utilities/{symbol}.md)\n")
        fd.write("\n")

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as fd:
    fd.write("- [Reference Home](index.md)\n")

    for step in WORKFLOW_STEPS:
        step_number = step["number"]
        step_slug = step["slug"]
        step_title = step["title"]
        fd.write(f"- Step {step_number}: {step_title}\n")
        for symbol, _ in symbols_by_step.get(step_number, []):
            fd.write(f"  - [{symbol}]({step_slug}/{symbol}.md)\n")

    if other_utilities:
        fd.write("- Other Utilities\n")
        for symbol, _ in other_utilities:
            fd.write(f"  - [{symbol}](other-utilities/{symbol}.md)\n")
