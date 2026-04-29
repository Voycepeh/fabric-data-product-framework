# Lineage recorder and transformation summaries

## Why lineage matters

Execution logs show **what ran**, but they rarely explain **why changes were made**. A lightweight lineage record helps teams track source-to-target flow, business intent, and transformation impact in a handover-friendly way.

## Code execution vs explanation

- Execution gives technical outcomes (row counts, schemas, checks).
- Explanation gives context (reasoning, business impact, decision notes).
- This module captures both in JSON-safe records that are metadata-table friendly.

## Manual recorder pattern

Use `LineageRecorder` during transformation steps. Record only notable changes (filtering, joins, derived fields, deduplication), not every cell.

```python
from fabric_data_product_framework.lineage import (
    LineageRecorder,
    generate_mermaid_lineage,
    build_transformation_summary_markdown,
)

lineage = LineageRecorder(
    dataset_name=ctx["dataset_name"],
    run_id=ctx["run_id"],
    source_tables=[ctx["source_table"]],
    target_table=ctx["target_table"],
)

lineage.add_step(
    step_id="T001",
    step_name="Filter active records",
    input_name="df_source",
    output_name="df_active",
    description="Keep only active records.",
    reason="Downstream reporting should exclude inactive records.",
    transformation_type="filter",
    columns_used=["status"],
)

lineage.add_step(
    step_id="T002",
    step_name="Derive reporting date",
    input_name="df_active",
    output_name="df_output",
    description="Create reporting_date from updated_at.",
    reason="Reports need a stable date field for filtering.",
    transformation_type="derive_column",
    columns_used=["updated_at"],
    columns_created=["reporting_date"],
)

summary = lineage.build_summary()
print(build_transformation_summary_markdown(summary))
```

## Handover support

The summary markdown and mermaid output give junior engineers or analysts a fast way to understand the transformation path and rationale without reverse engineering notebook cells.

## AI-assisted lineage review (without AI API calls)

`build_lineage_prompt_context` generates prompt-ready markdown for Copilot/AI-assisted review. It includes strict guidance not to invent transformations and keeps all facts sourced from recorded steps.

## Future evolution

This design intentionally stays manual-first. It can later connect to automated notebook/code analysis while preserving today’s notebook-friendly workflow.

## Metadata integration

Use `build_lineage_records` to convert steps into one-record-per-step rows that can be written to lineage metadata tables alongside run summaries and quality outputs.
