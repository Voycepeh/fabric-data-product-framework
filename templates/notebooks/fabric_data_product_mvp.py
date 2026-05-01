"""
Fabric Data Product MVP notebook starter.

This starter helps you move through a Fabric-first MVP workflow with a safe
DRY_RUN default and explicit handover artifacts.
"""

from __future__ import annotations

import pandas as pd

from fabric_data_product_framework.governance_classifier import classify_columns
from fabric_data_product_framework.lineage import (
    build_lineage_records,
    build_transformation_summary_markdown,
    generate_mermaid_lineage,
)
from fabric_data_product_framework.profiling import profile_dataframe
from fabric_data_product_framework.quality import run_quality_rules

# ==========================================================
# PARAMETER BLOCK
# ==========================================================
DRY_RUN = True
ENVIRONMENT = "Sandbox"
SOURCE_TARGET = "Source"
OUTPUT_TARGET = "Unified"

DATASET_NAME = "replace_me"
SOURCE_TABLE = "replace_me"
TARGET_TABLE = "replace_me"
RUN_ID = "replace_me_run_id"
APPROVED_USAGE = "analytics"


def fabric_reader() -> pd.DataFrame:
    """Read source data; return synthetic data in DRY_RUN mode."""
    if DRY_RUN:
        return pd.DataFrame(
            {
                "order_id": [1, 2, 3],
                "customer_id": ["C1", "C2", "C3"],
                "amount": [10.0, 25.5, 30.0],
            }
        )
    raise NotImplementedError(
        "Replace fabric_reader() with project-specific read logic."
    )


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Replace this stub with your business transformation logic."""
    return df


def fabric_writer(df: pd.DataFrame) -> None:
    """Replace this stub with your Fabric write logic."""
    if DRY_RUN:
        print("DRY_RUN enabled: skipping write.")
        return
    raise NotImplementedError(
        "Replace fabric_writer() with project-specific write logic."
    )


def main() -> None:
    """Run the MVP workflow: profile -> DQ -> governance -> lineage -> handover."""
    print("Starting Fabric data product MVP notebook")
    print(f"DRY_RUN={DRY_RUN}")
    print(f"ENVIRONMENT={ENVIRONMENT}")

    # 1) Read source and profile.
    source_df = fabric_reader()
    source_profile = profile_dataframe(
        source_df,
        dataset_name=DATASET_NAME,
        engine="auto",
    )

    # 2) Apply transformation.
    transformed_df = transform(source_df)

    # 3) Generate or review DQ rules.
    # Copilot prompt example:
    # "Given columns and business grain, generate deterministic data
    # quality rules with severity and rationale."
    quality_rules = [
        {
            "rule_id": "id_not_null",
            "rule_type": "not_null",
            "column": "order_id",
            "severity": "critical",
        }
    ]

    dq_result = run_quality_rules(
        transformed_df,
        quality_rules,
        dataset_name=DATASET_NAME,
        table_name=TARGET_TABLE,
        engine="auto",
    )

    # 4) Governance suggestions (AI-in-the-loop; human review required).
    columns_profile = [
        {
            "column_name": col,
            "data_type": str(transformed_df[col].dtype),
        }
        for col in transformed_df.columns
    ]
    governance_suggestions = classify_columns(
        profile={"columns": columns_profile},
        business_context={"approved_usage": APPROVED_USAGE},
    )

    # 5) Build lineage artifacts.
    steps = [
        {
            "step_id": "1",
            "step_name": "read_source",
            "input_name": SOURCE_TABLE,
            "output_name": "source_df",
            "transformation_type": "ingest",
        },
        {
            "step_id": "2",
            "step_name": "apply_business_transformation",
            "input_name": "source_df",
            "output_name": "transformed_df",
            "transformation_type": "transform",
        },
    ]

    lineage_records = build_lineage_records(
        dataset_name=DATASET_NAME,
        run_id=RUN_ID,
        source_tables=[SOURCE_TABLE],
        target_table=TARGET_TABLE,
        transformation_steps=steps,
    )

    lineage_mermaid = generate_mermaid_lineage(
        source_tables=[SOURCE_TABLE],
        target_table=TARGET_TABLE,
        transformation_steps=steps,
    )

    summary = {
        "dataset_name": DATASET_NAME,
        "run_id": RUN_ID,
        "source_tables": [SOURCE_TABLE],
        "target_table": TARGET_TABLE,
        "step_count": len(steps),
        "steps": steps,
        "columns_used": [],
        "columns_created": [],
    }
    summary_md = build_transformation_summary_markdown(summary)

    # 6) Handover pack.
    handover_pack = {
        "profile": source_profile,
        "dq": dq_result,
        "governance": governance_suggestions,
        "lineage_records": lineage_records,
        "lineage_mermaid": lineage_mermaid,
        "transformation_summary_markdown": summary_md,
        "status": "dry_run" if DRY_RUN else "completed",
    }

    print(handover_pack)
    print("Validation:", "passed")
    fabric_writer(transformed_df)

    # Human fills this in:
    # - Source/target names and environment values
    # - Fabric reader/writer implementations
    # - Business transformation logic
    # - Final governance approvals
    #
    # Framework generates this:
    # - Profile artifacts
    # - DQ execution result
    # - Governance suggestions
    # - Lineage and transformation summaries


if __name__ == "__main__":
    main()
