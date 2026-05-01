# Lineage API Reference

## Module purpose
`fabric_data_product_framework.lineage` records transformation steps and renders lineage artifacts for handover.

## Core public callables
- `LineageRecorder.add_step(...)`
- `generate_mermaid_lineage(source_tables, target_table, transformation_steps, graph_direction="LR")`
- `build_transformation_summary_markdown(summary, include_mermaid=True)`
- `build_lineage_records(...)` / `build_lineage_record(...)`

## Typical chaining
1. capture transformation steps during notebook processing.
2. build summary/mermaid markdown.
3. store lineage records and link them in run summary.
