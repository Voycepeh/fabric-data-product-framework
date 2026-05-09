from __future__ import annotations

import re
from pathlib import Path

OLD_MODULES = [
    "dq",
    "quality",
    "ai",
    "contracts",
    "lineage",
    "runtime",
    "run_summary",
    "config",
    "fabric_io",
    "technical_columns",
    "metadata",
    "governance",
    "profiling",
    "drift",
]

SCAN_PATHS = [
    Path("templates"),
    Path("docs/notebook-structure.md"),
    Path("templates/notebooks/README.md"),
    Path("templates/pipelines/README.md"),
]


def _iter_target_files():
    for entry in SCAN_PATHS:
        if entry.is_dir():
            yield from entry.rglob("*.md")
            yield from entry.rglob("*.py")
            yield from entry.rglob("*.ipynb")
        elif entry.exists():
            yield entry


def test_template_facing_content_does_not_use_short_form_modules() -> None:
    offending: list[tuple[str, str]] = []
    patterns = [rf"from\s+fabricops_kit\.{name}\s+import" for name in OLD_MODULES]

    for file_path in _iter_target_files():
        text = file_path.read_text(encoding="utf-8")
        for pattern in patterns:
            if re.search(pattern, text):
                offending.append((str(file_path), pattern))

    assert offending == []


def test_templates_include_full_name_module_imports() -> None:
    template_notebooks = list(Path("templates/notebooks").glob("*.ipynb"))
    combined = "\n".join(p.read_text(encoding="utf-8") for p in template_notebooks)
    assert "from fabricops_kit.data_quality import" in combined
    assert "from fabricops_kit.environment_config import" in combined
    assert "from fabricops_kit.runtime_context import" in combined
    assert "from fabricops_kit.fabric_input_output import" in combined
