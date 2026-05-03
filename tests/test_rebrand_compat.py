import warnings


def test_new_package_imports():
    import fabricops_kit

    assert hasattr(fabricops_kit, "load_fabric_config")


def test_legacy_import_works_with_deprecation_warning():
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        import fabric_data_product_framework as legacy  # noqa: F401

    assert any("fabric_data_product_framework is deprecated" in str(w.message) for w in captured)


def test_legacy_profiling_alias_maps_to_new_callable():
    from fabricops_kit import ODI_METADATA_LOGGER, generate_metadata_profile

    assert callable(ODI_METADATA_LOGGER)
    assert callable(generate_metadata_profile)
