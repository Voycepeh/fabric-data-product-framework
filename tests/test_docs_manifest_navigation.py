from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG_DIR = ROOT / "src" / "fabricops_kit"


def _run_generator() -> None:
    subprocess.run(["python", "scripts/generate_function_reference.py"], cwd=ROOT, check=True)


def _discover_expected_modules() -> set[str]:
    blacklist = {"__init__", "docs_metadata", "_utils"}
    alias = {"config": "environment_config", "drift": "data_drift", "metadata": "data_product_metadata"}
    modules = {p.stem for p in PKG_DIR.glob("*.py") if p.stem not in blacklist}
    return {alias.get(m, m) for m in modules}


def test_discovered_modules_generate_docs_pages_and_nav() -> None:
    _run_generator()
    manifest = json.loads((ROOT / "docs" / "reference" / "manifest.json").read_text(encoding="utf-8"))
    mkdocs_text = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

    expected_modules = _discover_expected_modules()
    manifest_modules = {m["module_name"] for m in manifest["modules"]}
    assert expected_modules <= manifest_modules

    for module in expected_modules:
        assert (ROOT / "docs" / "api" / "modules" / f"{module}.md").exists()
        assert f"- {module}: api/modules/{module}.md" in mkdocs_text


def test_business_context_and_metadata_appear_automatically() -> None:
    _run_generator()
    manifest = json.loads((ROOT / "docs" / "reference" / "manifest.json").read_text(encoding="utf-8"))
    modules = {m["module_name"] for m in manifest["modules"]}
    assert "business_context" in modules
    assert "data_product_metadata" in modules


def test_public_callables_point_to_generated_module_pages() -> None:
    _run_generator()
    manifest = json.loads((ROOT / "docs" / "reference" / "manifest.json").read_text(encoding="utf-8"))
    modules = {m["module_name"] for m in manifest["modules"]}
    for row in manifest["callables"]:
        assert row["module_name"] in modules


def test_mkdocs_sync_markers_render_current_manifest_modules() -> None:
    _run_generator()
    mkdocs_text = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    start = "      # AUTO-GENERATED-MODULES-START"
    end = "      # AUTO-GENERATED-MODULES-END"
    assert start in mkdocs_text and end in mkdocs_text
    block = mkdocs_text.split(start, 1)[1].split(end, 1)[0]

    manifest = json.loads((ROOT / "docs" / "reference" / "manifest.json").read_text(encoding="utf-8"))
    sidebar_modules = [m["module_name"] for m in manifest["modules"] if m["visibility"] == "public" and m["sidebar_include"]]
    for module in sidebar_modules:
        assert f"- {module}: api/modules/{module}.md" in block
