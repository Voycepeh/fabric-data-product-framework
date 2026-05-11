from pathlib import Path

import fabricops_kit

CANONICAL_DQ_EXPORTS = {
    "draft_dq_rules",
    "write_dq_rules",
    "enforce_dq_rules",
    "validate_dq_rules",
    "assert_dq_passed",
    "review_dq_rules",
}

REMOVED = {
    "profile_for_dq",
    "suggest_dq_rules",
    "extract_dq_rules",
    "build_dq_rule_history",
    "load_active_dq_rules",
    "split_dq_rows",
    "run_dq_rules",
}


def test_canonical_dq_flow_exports_updated():
    exports = set(fabricops_kit.__all__)
    assert CANONICAL_DQ_EXPORTS.issubset(exports)
    assert REMOVED.isdisjoint(exports)


def test_reference_excludes_removed_fragments():
    text = Path("docs/reference/index.md").read_text(encoding="utf-8")
    for name in REMOVED:
        assert name not in text
