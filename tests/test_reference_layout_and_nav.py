from pathlib import Path

def test_nav_excludes_runtime_context_module() -> None:
    text = Path("mkdocs.yml").read_text(encoding="utf-8")
    assert "runtime_context: api/modules/runtime_context.md" not in text

def test_module_pages_use_role_headings() -> None:
    text = Path("docs/api/modules/config.md").read_text(encoding="utf-8")
    assert "## Essential callables" in text
    assert "## Optional callables" in text
    assert "## Related internal helpers" in text


def test_nav_excludes_stale_public_aliases() -> None:
    text = Path("mkdocs.yml").read_text(encoding="utf-8")
    assert "environment_config: api/modules/environment_config.md" not in text
    assert "data_drift: api/modules/data_drift.md" not in text
    assert "data_product_metadata: api/modules/data_product_metadata.md" not in text
    assert "notebook_registry: api/modules/notebook_registry.md" not in text
