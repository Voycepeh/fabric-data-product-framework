from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VISIBLE_MODULES = [
    "environment_config",
    "runtime_context",
    "fabric_input_output",
    "data_profiling",
    "data_contracts",
    "data_quality",
    "data_drift",
    "data_governance",
    "data_product_metadata",
    "data_lineage",
    "handover_documentation",
    "technical_audit_columns",
]
HIDDEN_MODULES = [
    "dq",
    "quality",
    "ai",
    "config",
    "runtime",
    "run_summary",
    "contracts",
    "lineage",
]


def test_generated_docs_use_full_module_names() -> None:
    subprocess.run(["python", "scripts/generate_function_reference.py"], cwd=ROOT, check=True)

    modules_index = (ROOT / "docs" / "api" / "modules" / "index.md").read_text(encoding="utf-8")
    reference_index = (ROOT / "docs" / "reference" / "index.md").read_text(encoding="utf-8")

    for module in VISIBLE_MODULES:
        assert f"[`{module}`]({module}.md)" in modules_index
        assert f"../api/modules/{module}/" in reference_index

    for module in HIDDEN_MODULES:
        assert f"[`{module}`]({module}.md)" not in modules_index
        assert f"../api/modules/{module}/" not in reference_index

    data_quality_page = (ROOT / "docs" / "api" / "modules" / "data_quality.md").read_text(encoding="utf-8")
    assert "../../reference/internal/data_quality/" not in data_quality_page
    assert "../../reference/internal/dq/" in data_quality_page

    data_contracts_page = (ROOT / "docs" / "api" / "modules" / "data_contracts.md").read_text(encoding="utf-8")
    assert "../../reference/internal/contracts/" in data_contracts_page

    runtime_context_page = (ROOT / "docs" / "api" / "modules" / "runtime_context.md").read_text(encoding="utf-8")
    assert "../../reference/internal/runtime/" in runtime_context_page
