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


def test_gen_ref_pages_generates_legacy_redirect_pages_for_public_callables() -> None:
    outputs = _run_gen_ref_pages()
    assert "reference/build_governance_classification_records.md" in outputs
    assert "api/reference/build_governance_classification_records.md" in outputs


def test_legacy_redirect_points_to_canonical_callable_page() -> None:
    outputs = _run_gen_ref_pages()
    redirect = outputs["api/reference/build_governance_classification_records.md"]
    assert "../../reference/build_governance_classification_records/" in redirect
    assert "http-equiv=\"refresh\"" in redirect
    assert "rel=\"canonical\"" in redirect


def test_generated_primary_reference_links_do_not_use_api_reference_prefix() -> None:
    content = (ROOT / "docs" / "reference" / "index.md").read_text(encoding="utf-8")
    assert "/api/reference/" not in content


def test_generated_module_pages_do_not_use_api_reference_prefix() -> None:
    module_pages = sorted((ROOT / "docs" / "api" / "modules").glob("*.md"))
    for path in module_pages:
        text = path.read_text(encoding="utf-8")
        assert "/api/reference/" not in text
