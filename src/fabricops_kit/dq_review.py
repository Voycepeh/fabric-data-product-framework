"""Deprecated compatibility shim for notebook review widgets.

This module remains import-compatible for existing notebooks that use
``fabricops_kit.dq_review``. Import from ``fabricops_kit.notebook_review`` for
new development.
"""

from .notebook_review import (
    APPROVED_RULES_FROM_WIDGET,
    DEACTIVATED_RULES_FROM_WIDGET,
    KEPT_ACTIVE_RULES_FROM_WIDGET,
    REJECTED_RULES_FROM_WIDGET,
    review_dq_rule_deactivations,
    review_dq_rules,
)

__all__ = [
    "review_dq_rules",
    "review_dq_rule_deactivations",
    "APPROVED_RULES_FROM_WIDGET",
    "REJECTED_RULES_FROM_WIDGET",
    "DEACTIVATED_RULES_FROM_WIDGET",
    "KEPT_ACTIVE_RULES_FROM_WIDGET",
]
