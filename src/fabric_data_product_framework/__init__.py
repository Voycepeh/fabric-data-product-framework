"""Compatibility shim for deprecated package name."""

from __future__ import annotations

import warnings

warnings.warn(
    "fabric_data_product_framework is deprecated. Use fabricops_kit instead.",
    DeprecationWarning,
    stacklevel=2,
)

from fabricops_kit import *  # noqa: F401,F403
