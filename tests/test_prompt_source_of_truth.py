from pathlib import Path
import re
import pytest
from fabricops_kit.config import AIPromptConfig


def test_aipromptconfig_requires_all_canonical_fields():
    with pytest.raises(ValueError, match="business_context_prompt_template"):
        AIPromptConfig()
    with pytest.raises(ValueError, match="dq_rule_suggestion_prompt_template"):
        AIPromptConfig(
            business_context_prompt_template="x",
            dq_rule_suggestion_prompt_template="",
            governance_personal_identifier_prompt_template="x",
            governance_candidate_prompt_template="x",
            governance_review_prompt_template="x",
            handover_summary_prompt_template="x",
        )


def test_00_env_config_exact_prompt_ownership():
    text = Path("templates/notebooks/00_env_config.ipynb").read_text(encoding="utf-8")
    names = [
        "BUSINESS_CONTEXT_PROMPT_TEMPLATE",
        "DQ_RULE_SUGGESTION_PROMPT_TEMPLATE",
        "GOVERNANCE_PERSONAL_IDENTIFIER_PROMPT_TEMPLATE",
        "GOVERNANCE_CANDIDATE_PROMPT_TEMPLATE",
        "GOVERNANCE_REVIEW_PROMPT_TEMPLATE",
        "HANDOVER_SUMMARY_PROMPT_TEMPLATE",
    ]
    for name in names:
        assert len(re.findall(fr'"{name} =', text)) == 1
    forbidden = [
        "DEFAULT_BUSINESS_CONTEXT_PROMPT_TEMPLATE",
        "DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE",
        "DEFAULT_GOVERNANCE_PERSONAL_IDENTIFIER_PROMPT_TEMPLATE",
        "DEFAULT_GOVERNANCE_CANDIDATE_TEMPLATE",
        "DEFAULT_GOVERNANCE_REVIEW_TEMPLATE",
        "DEFAULT_HANDOVER_SUMMARY_TEMPLATE",
        "DEFAULT_HANDOVER_SUMMARY_TEMPLATE$0",
    ]
    for token in forbidden:
        assert token not in text


def test_no_source_module_imports_default_prompt_constants_or_old_aliases():
    src = Path("src").read_text() if False else ""
    files = list(Path("src/fabricops_kit").glob("*.py"))
    bad_import = "DEFAULT_"
    old_aliases = [
        "business_context_template",
        "dq_rule_candidate_template",
        "governance_personal_identifier_template",
        "governance_candidate_template",
        "governance_review_template",
        "handover_summary_template",
    ]
    for f in files:
        text = f.read_text(encoding="utf-8")
        if f.name != "config.py":
            assert "from .config import DEFAULT_" not in text
            assert "from fabricops_kit.config import DEFAULT_" not in text
        for alias in old_aliases:
            assert alias not in text
