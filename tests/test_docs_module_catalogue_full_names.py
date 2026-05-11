from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VISIBLE_MODULES = [
    "config",
    "fabric_io",
    "profiling",
    "contracts",
    "dq",
    "governance",
    "lineage",
]


def test_generated_docs_use_canonical_module_names() -> None:
    subprocess.run(["python", "scripts/generate_function_reference.py"], cwd=ROOT, check=True)

    modules_index = (ROOT / "docs" / "api" / "modules" / "index.md").read_text(encoding="utf-8")
    reference_index = (ROOT / "docs" / "reference" / "index.md").read_text(encoding="utf-8")

    for module in VISIBLE_MODULES:
        assert f"[`{module}`]({module}.md)" in modules_index
        assert f"../api/modules/{module}/" in reference_index

    assert "import-compatible aliases" not in modules_index
    assert "../api/modules/quality/" not in reference_index
