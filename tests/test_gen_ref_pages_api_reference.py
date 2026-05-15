from __future__ import annotations

import io
import runpy
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "docs" / "gen_ref_pages.py"


class _Recorder:
    def __init__(self) -> None:
        self.files: dict[str, io.StringIO] = {}

    def open(self, path: str, mode: str = "w"):
        buf = io.StringIO()
        self.files[path] = buf

        class _Ctx:
            def __enter__(self_nonlocal):
                return buf

            def __exit__(self_nonlocal, exc_type, exc, tb):
                return False

        return _Ctx()


def _run_gen_ref_pages() -> dict[str, str]:
    recorder = _Recorder()
    fake_module = types.SimpleNamespace(open=recorder.open)
    original = sys.modules.get("mkdocs_gen_files")
    sys.modules["mkdocs_gen_files"] = fake_module
    try:
        runpy.run_path(str(SCRIPT), run_name="__main__")
    finally:
        if original is not None:
            sys.modules["mkdocs_gen_files"] = original
        else:
            del sys.modules["mkdocs_gen_files"]
    return {path: buf.getvalue() for path, buf in recorder.files.items()}


def test_gen_ref_pages_generates_public_callable_pages_under_api_reference() -> None:
    outputs = _run_gen_ref_pages()
    assert "api/reference/build_governance_classification_records.md" in outputs
    assert "reference/build_governance_classification_records.md" not in outputs


def test_generated_primary_reference_links_use_api_reference_prefix() -> None:
    content = (ROOT / "docs" / "reference" / "index.md").read_text(encoding="utf-8")
    assert "../api/reference/" in content
    assert "./build_governance_classification_records/" not in content


def test_generated_module_pages_use_api_reference_prefix() -> None:
    import json
    manifest = json.loads((ROOT / "docs" / "reference" / "manifest.json").read_text(encoding="utf-8"))
    module_pages = [ROOT / "docs" / "api" / "modules" / f"{row['module_name']}.md" for row in manifest["modules"]]
    for path in module_pages:
        text = path.read_text(encoding="utf-8")
        assert "../../api/reference/" not in text


def test_generated_notebook_structure_pages_use_api_reference_prefix() -> None:
    notebook_pages = sorted((ROOT / "docs" / "notebook-structure").glob("*.md"))
    assert notebook_pages
    for path in notebook_pages:
        text = path.read_text(encoding="utf-8")
        assert "../../api/reference/" in text
        assert "../../reference/internal/" in text or "../../reference/" not in text


def test_no_legacy_top_level_reference_callable_page_exists() -> None:
    outputs = _run_gen_ref_pages()
    assert "api/reference/build_governance_classification_records.md" in outputs
    assert "reference/build_governance_classification_records.md" not in outputs
