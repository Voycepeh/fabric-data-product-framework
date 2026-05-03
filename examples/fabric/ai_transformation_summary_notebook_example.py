"""Notebook-style example for AI-assisted transformation summary workflow."""

from fabricops_kit.ai_lineage_summary import (
    build_transformation_summary_generation_prompt,
    build_transformation_summary_records,
    parse_ai_transformation_summaries,
)
from fabricops_kit.lineage import (
    build_lineage_from_notebook_code,
    build_lineage_handover_markdown,
    plot_lineage_steps,
)


def notebook_ai_transformation_summary_example(run_id: str, dataset_name: str):
    notebook_code = """
orders = lakehouse_table_read(spark, env, cfg, "bronze", "orders")
filtered = orders.filter(col("is_active") == 1)
lakehouse_table_write(filtered, spark, env, cfg, "silver", "orders")
"""
    summary = build_lineage_from_notebook_code(notebook_code, use_ai=False)
    prompt = build_transformation_summary_generation_prompt(summary, runtime_metrics={"row_count_before": 1000, "row_count_after": 800})

    # notebook-layer pseudocode only:
    # raw_response = ai.generate_response(prompt)
    raw_response = "[]"

    parsed = parse_ai_transformation_summaries(raw_response)
    records = build_transformation_summary_records(parsed["candidates"], run_id, dataset_name, "silver.orders")

    mermaid = plot_lineage_steps(summary["steps"])
    handover_markdown = build_lineage_handover_markdown(summary)
    return {"prompt": prompt, "records": records, "mermaid": mermaid, "handover_markdown": handover_markdown}
