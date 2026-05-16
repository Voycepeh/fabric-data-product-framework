"""Regression tests for package-level imports used by starter templates."""


def test_template_bootstrap_imports_smoke():
    """Ensure first-cell notebook imports work from installed package surfaces."""
    import fabricops_kit
    import fabricops_kit.config
    from fabricops_kit.config import load_config, setup_notebook
    from fabricops_kit.data_profiling import profile_dataframe
    from fabricops_kit.technical_columns import standardize_columns

    assert fabricops_kit is not None
    assert fabricops_kit.config is not None
    assert callable(setup_notebook)
    assert callable(load_config)
    assert callable(profile_dataframe)
    assert callable(standardize_columns)
