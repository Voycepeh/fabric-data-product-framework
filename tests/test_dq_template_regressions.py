from pathlib import Path


def _text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_no_mechanical_rename_regressions_in_templates_and_example():
    blobs = [
        _text("templates/notebooks/02_ex_agreement_topic.ipynb"),
        _text("templates/notebooks/03_pc_agreement_source_to_target.ipynb"),
        _text("examples/notebooks/FabricOps_AI_DQ_Source_of_Truth_Widget_Metadata_Flow.ipynb"),
    ]
    combined = "\n".join(blobs)

    forbidden = [
        'profile_rows = draft_dq_rules(',
        'CANDIDATE_DQ_RULES = draft_dq_rules(responses',
        'rules = enforce_dq(metadata_dq_rules',
        'df_valid, df_quarantine, dq_failure_evidence = enforce_dq(',
        'write_dq_rules(\\n    spark=spark',
    ]
    for item in forbidden:
        assert item not in combined

    assert combined.count('draft_dq_rules,') <= 3
    assert combined.count('enforce_dq,') <= 3


def test_expected_canonical_calls_present():
    ex = _text("templates/notebooks/02_ex_agreement_topic.ipynb")
    pc = _text("templates/notebooks/03_pc_agreement_source_to_target.ipynb")
    demo = _text("examples/notebooks/FabricOps_AI_DQ_Source_of_Truth_Widget_Metadata_Flow.ipynb")

    assert 'profile_dataframe_to_metadata' in ex
    assert 'profile_df=profile_rows' in ex
    assert 'write_dq_rules(' in ex

    assert 'metadata_dq_rules = spark.table("METADATA_DQ_RULES")' in pc
    assert 'dq = enforce_dq(' in pc
    assert 'assert_dq_passed(dq.rule_results)' in pc

    assert 'profile_dataframe_to_metadata(df_test, table_name=TABLE_NAME)' in demo
    assert 'dq = enforce_dq(' in demo
    assert 'assert_dq_passed(dq.rule_results)' in demo
