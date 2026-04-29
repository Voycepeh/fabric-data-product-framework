"""Notebook-style example for AI-assisted transformation summary workflow."""

from fabric_data_product_framework.ai_lineage_summary import (
    build_transformation_summary_generation_prompt,
    build_transformation_summary_records,
    parse_ai_transformation_summaries,
)
from fabric_data_product_framework.lineage import (
    LineageRecorder,
    build_transformation_summary_markdown,
    generate_mermaid_lineage,
)


def notebook_ai_transformation_summary_example(run_id: str, dataset_name: str):
    lineage = LineageRecorder(dataset_name=dataset_name, run_id=run_id, source_tables=["bronze.orders"], target_table="silver.orders")
    lineage.add_step(
        step_id="T001",
        step_name="Filter active",
        input_name="df_source",
        output_name="df_filtered",
        description="Keep active rows only",
        reason="Inactive rows should not flow downstream",
        transformation_type="filter",
    )

    summary = lineage.build_summary()
    prompt = build_transformation_summary_generation_prompt(summary, runtime_metrics={"row_count_before": 1000, "row_count_after": 800})

    # notebook-layer pseudocode only:
    # raw_response = ai.generate_response(prompt)
    raw_response = "[]"

    parsed = parse_ai_transformation_summaries(raw_response)
    records = build_transformation_summary_records(parsed["candidates"], run_id, dataset_name, "silver.orders")

    mermaid = generate_mermaid_lineage(summary)
    handover_markdown = build_transformation_summary_markdown(summary)
    return {"prompt": prompt, "records": records, "mermaid": mermaid, "handover_markdown": handover_markdown}
