from pathlib import Path


def test_reference_index_templates_first_sections_present() -> None:
    text = Path("docs/reference/index.md").read_text(encoding="utf-8")

    assert "## Start from the templates" in text
    assert "## Callable map by workflow step" in text
    assert "https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/00_env_config.ipynb" in text
    assert "https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/02_ex_agreement_topic.ipynb" in text
    assert "https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/03_pc_agreement_source_to_target.ipynb" in text
    assert "../api/modules/dq/" not in text
    assert "../api/modules/quality/" not in text


def test_mkdocs_nav_uses_full_module_names() -> None:
    text = Path("mkdocs.yml").read_text(encoding="utf-8")

    assert "Template Function Map" not in text
    assert "ai: api/modules/ai.md" not in text
    assert "quality: api/modules/quality.md" not in text
    assert "run_summary: api/modules/run_summary.md" not in text
    assert "docs_metadata: api/modules/docs_metadata.md" not in text
    assert "data_quality: api/modules/data_quality.md" in text
    assert "environment_config: api/modules/environment_config.md" in text
    assert "handover_documentation: api/modules/handover_documentation.md" in text
