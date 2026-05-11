from pathlib import Path

def test_nav_excludes_runtime_context_module() -> None:
    text = Path("mkdocs.yml").read_text(encoding="utf-8")
    assert "runtime_context: api/modules/runtime_context.md" not in text

def test_module_pages_use_role_headings() -> None:
    text = Path("docs/api/modules/environment_config.md").read_text(encoding="utf-8")
    assert "## Essential callables" in text
    assert "## Optional callables" in text
    assert "## Related internal helpers" in text
