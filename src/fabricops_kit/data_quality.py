"""Public module alias for notebook-facing data quality helpers."""
from .dq import *

def get_default_data_quality_rule_templates():
    """Return editable example data quality rules."""
    return get_default_dq_rule_templates()

def suggest_data_quality_rules_prompt(*args, **kwargs):
    """Build a prompt for candidate data quality rule suggestions."""
    return suggest_dq_rules_prompt(*args, **kwargs)

def validate_data_quality_rules(*args, **kwargs):
    """Validate notebook-facing data quality rules."""
    return validate_dq_rules(*args, **kwargs)

def run_data_quality_rules(*args, **kwargs):
    """Run notebook-facing data quality rules and return a Spark DataFrame result."""
    return run_dq_rules(*args, **kwargs)

def assert_data_quality_passed(*args, **kwargs):
    """Raise when any error-severity data quality rule failed after results are logged."""
    return assert_dq_passed(*args, **kwargs)
