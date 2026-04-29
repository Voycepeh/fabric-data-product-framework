"""End-to-end notebook-style example for AI-assisted DQ rule workflow.

This file is provider-neutral; Fabric AI calls are shown as pseudocode placeholders.
"""

from fabric_data_product_framework.ai_quality_rules import (
    build_layman_rule_records,
    build_quality_rule_generation_prompt,
    parse_ai_quality_rule_candidates,
)
from fabric_data_product_framework.profiling import profile_dataframe
from fabric_data_product_framework.quality import build_quality_result_records, run_quality_rules
from fabric_data_product_framework.quarantine import split_valid_and_quarantine
from fabric_data_product_framework.rule_compiler import (
    build_rule_registry_records,
    compile_layman_rules_to_quality_rules,
)


def notebook_flow_example(spark_df, run_id: str, dataset_name: str, table_name: str):
    profile = profile_dataframe(spark_df, dataset_name=dataset_name, engine="spark")
    prompt = build_quality_rule_generation_prompt(profile, dataset_name=dataset_name, table_name=table_name)

    # NOTE: notebook-layer pseudocode only (do not import Fabric AI packages in core framework modules)
    # raw_ai_response = ai.generate_response(prompt)
    raw_ai_response = "[]"

    parsed = parse_ai_quality_rule_candidates(raw_ai_response)
    candidate_records = build_layman_rule_records(parsed["candidates"], run_id, dataset_name, table_name)

    compile_result = compile_layman_rules_to_quality_rules(parsed["candidates"])
    executable_rules = compile_result["compiled_rules"]
    rule_registry_records = build_rule_registry_records(executable_rules, run_id, dataset_name, table_name)

    quality_result = run_quality_rules(spark_df, executable_rules, dataset_name=dataset_name, table_name=table_name, engine="spark")
    quality_records = build_quality_result_records(quality_result, run_id=run_id)

    valid_df, quarantine_df = split_valid_and_quarantine(spark_df, executable_rules, engine="spark")

    return {
        "candidate_records": candidate_records,
        "rule_registry_records": rule_registry_records,
        "quality_records": quality_records,
        "valid_df": valid_df,
        "quarantine_df": quarantine_df,
    }
