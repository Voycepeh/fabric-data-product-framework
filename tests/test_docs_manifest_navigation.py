from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run_generator() -> None:
    subprocess.run(["python", "scripts/generate_function_reference.py"], cwd=ROOT, check=True)


def test_manifest_drives_public_sidebar_modules() -> None:
    _run_generator()
    manifest = json.loads((ROOT / "docs" / "reference" / "manifest.json").read_text(encoding="utf-8"))
    mkdocs_text = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

    public_sidebar_modules = {
        m["module_name"] for m in manifest["modules"] if m["visibility"] == "public" and m["sidebar_include"]
    }
    internal_modules = {m["module_name"] for m in manifest["modules"] if m["visibility"] == "internal"}

    for module in public_sidebar_modules:
        assert f"- {module}: api/modules/{module}.md" in mkdocs_text
    for module in internal_modules:
        assert f"- {module}: api/modules/{module}.md" not in mkdocs_text


def test_public_callables_align_with_manifest_module_visibility() -> None:
    _run_generator()
    manifest = json.loads((ROOT / "docs" / "reference" / "manifest.json").read_text(encoding="utf-8"))
    callables = manifest["callables"]

    assert all(row["callable_visibility"] == "public" for row in callables)
    assert all(
        row["callable_role"] in {"recommended_entrypoint", "advanced_helper", "internal_helper"}
        for row in callables
    )
    # Keep DQ and review alignment explicit.
    dq = [r for r in callables if r["module_name"] == "data_quality"]
    dq_review = [r for r in callables if r["module_name"] == "dq_review"]
    assert dq
    assert dq_review
    assert all(r["visibility"] == "internal" for r in dq_review)


def test_manifest_callable_modules_exist_in_module_metadata() -> None:
    _run_generator()
    manifest = json.loads((ROOT / "docs" / "reference" / "manifest.json").read_text(encoding="utf-8"))
    module_names = {row["module_name"] for row in manifest["modules"]}
    assert module_names
    for row in manifest["callables"]:
        assert row["module_name"] in module_names
        assert row["module_name"] not in {"config", "runtime", "drift", "metadata", "run_summary", "technical_columns"}


def test_public_sidebar_pages_are_not_internal_and_have_callable_sections() -> None:
    _run_generator()
    manifest = json.loads((ROOT / "docs" / "reference" / "manifest.json").read_text(encoding="utf-8"))
    public_sidebar_modules = [
        row["module_name"] for row in manifest["modules"] if row["visibility"] == "public" and row["sidebar_include"]
    ]
    callable_modules = {row["module_name"] for row in manifest["callables"]}
    for module in public_sidebar_modules:
        page = (ROOT / "docs" / "api" / "modules" / f"{module}.md").read_text(encoding="utf-8")
        first_line = page.splitlines()[0]
        assert "(internal)" not in first_line
        assert "No public exports in this module." not in page
        if module in callable_modules:
            assert "## Recommended notebook entrypoints" in page
            assert "## Advanced helpers" in page
