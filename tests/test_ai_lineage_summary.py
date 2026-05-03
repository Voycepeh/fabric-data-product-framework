from fabric_data_product_framework.lineage import (
    build_transformation_summary_generation_prompt,
    build_transformation_summary_prompt_context,
    build_transformation_summary_records,
    normalize_transformation_summary_candidate,
    parse_ai_transformation_summaries,
)


def _lineage_summary():
    return {
        "dataset_name": "orders",
        "transformation_steps": [
            {
                "step_id": "T001",
                "step_name": "Filter active",
                "input_name": "df_source",
                "output_name": "df_filtered",
                "transformation_type": "filter",
                "description": "Keep active rows",
            }
        ],
    }


def test_prompt_context_includes_lineage_steps_and_prompt_requirements():
    context = build_transformation_summary_prompt_context(_lineage_summary())
    prompt = build_transformation_summary_generation_prompt(_lineage_summary())
    assert "transformation_steps" in str(context["lineage_summary"])
    assert "technical_summary" in prompt
    assert "business_summary" in prompt


def test_parse_valid_json_and_fenced_json_and_malformed():
    raw = '[{"step_id":"T001","step_name":"Filter active","input_name":"df_source","output_name":"df_filtered","transformation_type":"filter","technical_summary":"x","business_summary":"y","business_impact":"z","risk_or_caveat":"low","confidence":"high","evidence":["where status=active"],"approval_status":"candidate"}]'
    ok = parse_ai_transformation_summaries(raw)
    assert ok["ok"] is True

    fenced = f"```json\n{raw}\n```"
    ok2 = parse_ai_transformation_summaries(fenced)
    assert ok2["ok"] is True

    bad = parse_ai_transformation_summaries("not-json")
    assert bad["ok"] is False


def test_normalize_defaults_and_records():
    c = normalize_transformation_summary_candidate(
        {
            "step_id": "T001",
            "step_name": "Filter active",
            "input_name": "df_source",
            "output_name": "df_filtered",
            "transformation_type": "filter",
            "technical_summary": "tech",
            "business_summary": "biz",
            "business_impact": "impact",
            "risk_or_caveat": "risk",
            "evidence": ["predicate"],
        }
    )
    assert c["approval_status"] == "candidate"
    assert c["confidence"] == "medium"

    rows = build_transformation_summary_records([c], "run1", "orders", "silver.orders")
    assert rows[0]["run_id"] == "run1"
