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
    alias = {}
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


def test_workflow_modules_are_present_and_internal_modules_hidden_from_sidebar() -> None:
    _run_generator()
    mkdocs_text = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    assert "- business_context: api/modules/business_context.md" in mkdocs_text
    assert "- data_agreement: api/modules/data_agreement.md" in mkdocs_text
    assert "- metadata: api/modules/metadata.md" in mkdocs_text
    assert "- ai: api/modules/ai.md" not in mkdocs_text
    assert "- docs_metadata: api/modules/docs_metadata.md" not in mkdocs_text
    assert "- schemas: api/modules/schemas.md" not in mkdocs_text
    assert "- 3. Data engineer:" in mkdocs_text
    assert "- drift: api/modules/drift.md" in mkdocs_text


def test_data_agreement_module_page_is_generated_normally() -> None:
    _run_generator()
    text = (ROOT / "docs" / "api" / "modules" / "data_agreement.md").read_text(encoding="utf-8")
    assert "## Essential callables" in text
    assert "placeholder" not in text.lower()


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
    sidebar_modules = [m["module_name"] for m in manifest["modules"]]
    for module in sidebar_modules:
        assert f"- {module}: api/modules/{module}.md" in block


def test_sidebar_include_flag_controls_visibility() -> None:
    _run_generator()
    manifest = json.loads((ROOT / "docs" / "reference" / "manifest.json").read_text(encoding="utf-8"))
    mkdocs_text = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    for row in manifest["modules"]:
        nav_line = f"- {row['module_name']}: api/modules/{row['module_name']}.md"
        if row["sidebar_include"]:
            assert nav_line in mkdocs_text
        else:
            assert nav_line not in mkdocs_text


def test_only_explicit_blacklist_hides_modules() -> None:
    _run_generator()
    mkdocs_text = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    assert "- _utils: api/modules/_utils.md" not in mkdocs_text


def test_manifest_module_and_callable_visibility_are_consistent() -> None:
    _run_generator()
    manifest = json.loads((ROOT / "docs" / "reference" / "manifest.json").read_text(encoding="utf-8"))
    module_rows = {row["module_name"]: row for row in manifest["modules"]}
    for callable_row in manifest["callables"]:
        module_row = module_rows[callable_row["module_name"]]
        assert callable_row["visibility"] == module_row["visibility"]
        assert callable_row["sidebar_include"] == module_row["sidebar_include"]


def test_manifest_module_rows_match_all_callable_visibility_flags_by_module() -> None:
    _run_generator()
    manifest = json.loads((ROOT / "docs" / "reference" / "manifest.json").read_text(encoding="utf-8"))
    module_rows = {row["module_name"]: row for row in manifest["modules"]}
    for module_name, module_row in module_rows.items():
        module_callables = [row for row in manifest["callables"] if row["module_name"] == module_name]
        for callable_row in module_callables:
            assert callable_row["visibility"] == module_row["visibility"]
            assert callable_row["sidebar_include"] == module_row["sidebar_include"]
