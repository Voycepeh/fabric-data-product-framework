import importlib

FULL_MODULES = [
    'fabricops_kit.environment_config',
    'fabricops_kit.runtime_context',
    'fabricops_kit.fabric_input_output',
    'fabricops_kit.data_profiling',
    'fabricops_kit.data_contracts',
    'fabricops_kit.data_quality',
    'fabricops_kit.data_drift',
    'fabricops_kit.data_governance',
    'fabricops_kit.data_product_metadata',
    'fabricops_kit.data_lineage',
    'fabricops_kit.handover_documentation',
    'fabricops_kit.technical_audit_columns',
]


def test_full_module_imports():
    for name in FULL_MODULES:
        assert importlib.import_module(name)


def test_data_quality_alias_functions():
    mod = importlib.import_module('fabricops_kit.data_quality')
    assert mod.run_data_quality_rules is not None
    assert mod.validate_data_quality_rules is not None
