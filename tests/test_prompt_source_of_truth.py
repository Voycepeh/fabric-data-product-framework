from pathlib import Path


def test_config_exposes_prompt_constants_and_ai_prompt_defaults():
    import fabricops_kit.config as c

    assert c.DEFAULT_BUSINESS_CONTEXT_PROMPT_TEMPLATE
    assert c.DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE
    assert c.DEFAULT_GOVERNANCE_PERSONAL_IDENTIFIER_PROMPT_TEMPLATE
    cfg = c.AIPromptConfig()
    assert cfg.business_context_template == c.DEFAULT_BUSINESS_CONTEXT_PROMPT_TEMPLATE
    assert cfg.dq_rule_candidate_template == c.DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE
    assert cfg.governance_personal_identifier_template == c.DEFAULT_GOVERNANCE_PERSONAL_IDENTIFIER_PROMPT_TEMPLATE


def test_modules_reference_config_prompt_defaults():
    import fabricops_kit.business_context as bc
    import fabricops_kit.data_quality as dq
    import fabricops_kit.data_governance as gov
    import fabricops_kit.config as c

    assert bc.BUSINESS_CONTEXT_PROMPT == c.DEFAULT_BUSINESS_CONTEXT_PROMPT_TEMPLATE
    assert dq.DQ_RULE_SUGGESTION_PROMPT_TEMPLATE == c.DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE
    assert gov.PDPA_PERSONAL_IDENTIFIER_PROMPT == c.DEFAULT_GOVERNANCE_PERSONAL_IDENTIFIER_PROMPT_TEMPLATE


def test_02_ex_uses_config_ai_prompt_config_and_03_pc_has_no_prompt_helpers():
    ex = Path('templates/notebooks/02_ex_agreement_topic.ipynb').read_text(encoding='utf-8')
    pc = Path('templates/notebooks/03_pc_agreement_source_to_target.ipynb').read_text(encoding='utf-8')
    assert 'CONFIG.ai_prompt_config.business_context_template' in ex
    assert 'CONFIG.ai_prompt_config.dq_rule_candidate_template' in ex
    assert 'CONFIG.ai_prompt_config.governance_personal_identifier_template' in ex
    assert 'suggest_column_business_contexts' not in pc
    assert 'suggest_personal_identifier_classifications' not in pc


def test_config_dq_prompt_uses_lower_upper_bounds_not_min_max_output():
    import fabricops_kit.config as c
    prompt = c.DEFAULT_DQ_RULE_SUGGESTION_PROMPT_TEMPLATE
    assert "lower_bound" in prompt and "upper_bound" in prompt
    assert "min_value or max_value" not in prompt


def test_all_does_not_expose_module_prompt_aliases():
    import fabricops_kit as f
    assert "DQ_RULE_SUGGESTION_PROMPT_TEMPLATE" not in f.__all__
    assert "BUSINESS_CONTEXT_PROMPT" not in f.__all__
    assert "PDPA_PERSONAL_IDENTIFIER_PROMPT" not in f.__all__


def test_02_ex_has_no_old_todo_draft_flow():
    ex = Path('templates/notebooks/02_ex_agreement_topic.ipynb').read_text(encoding='utf-8')
    assert 'TODO_replace_business_context' not in ex
    assert 'draft_dq_rules(' not in ex
