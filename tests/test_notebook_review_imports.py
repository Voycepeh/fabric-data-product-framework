from fabricops_kit import __all__


def test_review_callables_exported():
    assert "review_dq_rules" in __all__
    assert "review_dq_rule_deactivations" in __all__


def test_legacy_dq_review_import_path_works():
    from fabricops_kit import dq_review

    assert callable(dq_review.review_dq_rules)
    assert callable(dq_review.review_dq_rule_deactivations)


def test_new_notebook_review_import_path_works():
    from fabricops_kit import notebook_review

    assert callable(notebook_review.review_dq_rules)
    assert callable(notebook_review.review_dq_rule_deactivations)
