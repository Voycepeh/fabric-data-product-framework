from pathlib import Path

import fabricops_kit

CANONICAL_DQ_EXPORTS = {
    "profile_for_dq",
    "suggest_dq_rules",
    "extract_dq_rules",
    "validate_dq_rules",
    "build_dq_rule_history",
    "build_dq_rule_deactivations",
    "load_active_dq_rules",
    "split_dq_rows",
    "run_dq_rules",
    "assert_dq_passed",
}

REMOVED = {
    "AI_SUGGESTABLE_DQ_RULE_TYPES",
    "build_dq_rule_candidate_prompt",
    "generate_dq_rule_candidates_with_fabric_ai",
    "build_manual_dq_rule_prompt_package",
}


def test_canonical_dq_flow_remains_exported_and_legacy_symbols_are_not():
    exports = set(fabricops_kit.__all__)
    assert CANONICAL_DQ_EXPORTS.issubset(exports)
    assert REMOVED.isdisjoint(exports)


def test_generated_reference_excludes_constant_and_legacy_dq_ai_pages():
    text = Path("docs/reference/index.md").read_text(encoding="utf-8")
    for name in REMOVED:
        assert name not in text


def test_ai_module_page_excludes_legacy_dq_ai_helpers():
    text = Path("docs/api/modules/ai.md").read_text(encoding="utf-8")
    for name in [
        "build_dq_rule_candidate_prompt",
        "generate_dq_rule_candidates_with_fabric_ai",
        "build_manual_dq_rule_prompt_package",
    ]:
        assert name not in text
