from pathlib import Path


def test_config_requires_explicit_ai_prompt_values():
    import pytest
    from fabricops_kit.config import AIPromptConfig

    with pytest.raises(ValueError, match="business_context_template must be a non-empty string"):
        AIPromptConfig()


def test_00_env_config_uses_visible_prompt_strings_not_default_imports():
    text = Path("templates/notebooks/00_env_config.ipynb").read_text(encoding="utf-8")
    required = [
        "BUSINESS_CONTEXT_PROMPT_TEMPLATE =",
        "DQ_RULE_SUGGESTION_PROMPT_TEMPLATE =",
        "GOVERNANCE_PERSONAL_IDENTIFIER_PROMPT_TEMPLATE =",
        "GOVERNANCE_CANDIDATE_PROMPT_TEMPLATE =",
        "GOVERNANCE_REVIEW_PROMPT_TEMPLATE =",
        "HANDOVER_SUMMARY_PROMPT_TEMPLATE =",
    ]
    for token in required:
        assert token in text
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


def test_missing_prompt_templates_raise_clear_value_errors():
    import pytest
    from fabricops_kit.business_context import draft_business_context
    from fabricops_kit.data_governance import draft_governance
    from fabricops_kit.data_quality import _suggest_dq_rules

    with pytest.raises(ValueError, match="Missing business_context_prompt_template"):
        draft_business_context(object(), prompt_template=None)
    with pytest.raises(ValueError, match="Missing governance_personal_identifier_prompt_template"):
        draft_governance(object(), prompt=None)
    with pytest.raises(ValueError, match="Missing dq_rule_suggestion_prompt_template"):
        _suggest_dq_rules(object(), prompt_template=None)
