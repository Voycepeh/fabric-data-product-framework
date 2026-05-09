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
    template_section = text.split("## Lifecycle flow", 1)[0]
    assert "../api/modules/runtime_context/" not in template_section
    assert "../api/modules/data_product_metadata/" not in template_section
    assert "../api/modules/technical_audit_columns/" not in template_section
    assert "../api/modules/handover_documentation/" not in template_section


def test_mkdocs_nav_uses_full_module_names() -> None:
    text = Path("mkdocs.yml").read_text(encoding="utf-8")

    assert "Template Function Map" not in text
    assert "ai: api/modules/ai.md" not in text
    assert "quality: api/modules/quality.md" not in text
    assert "run_summary: api/modules/run_summary.md" not in text
    assert "docs_metadata: api/modules/docs_metadata.md" not in text
    for module_name in [
        "environment_config",
        "fabric_input_output",
        "data_profiling",
        "data_contracts",
        "data_quality",
        "data_governance",
        "data_lineage",
    ]:
        assert f"{module_name}: api/modules/{module_name}.md" in text
    for hidden_module in [
        "runtime_context",
        "data_drift",
        "data_product_metadata",
        "handover_documentation",
        "technical_audit_columns",
    ]:
        assert f"{hidden_module}: api/modules/{hidden_module}.md" not in text


def test_module_pages_split_recommended_and_advanced_sections() -> None:
    contracts_text = Path("docs/api/modules/data_contracts.md").read_text(encoding="utf-8")
    assert "## Recommended notebook entrypoints" in contracts_text
    assert "## Advanced helpers" in contracts_text
    recommended_block = contracts_text.split("## Recommended notebook entrypoints", 1)[1].split("## Advanced helpers", 1)[0]
    assert "`build_contract_header_record`" not in recommended_block
    assert "`build_contract_column_records`" not in recommended_block
    assert "`build_contract_rule_records`" not in recommended_block

    lineage_text = Path("docs/api/modules/data_lineage.md").read_text(encoding="utf-8")
    recommended_lineage = lineage_text.split("## Recommended notebook entrypoints", 1)[1].split("## Advanced helpers", 1)[0]
    assert "[`build_lineage_from_notebook_code`]" in recommended_lineage

    env_text = Path("docs/api/modules/environment_config.md").read_text(encoding="utf-8")
    env_recommended = env_text.split("## Recommended notebook entrypoints", 1)[1].split("## Advanced helpers", 1)[0]
    assert "[`load_fabric_config`]" in env_recommended

    dq_text = Path("docs/api/modules/data_quality.md").read_text(encoding="utf-8")
    dq_recommended = dq_text.split("## Recommended notebook entrypoints", 1)[1].split("## Advanced helpers", 1)[0]
    assert "Run notebook-facing DQ rules and return a Spark DataFrame result." in dq_recommended
    assert "Split a Spark DataFrame into pass/quarantine outputs for row-level DQ rules." in dq_recommended
    assert "Execute the `run_dq_rules` workflow step in FabricOps." not in dq_recommended
    assert "Execute the `split_valid_and_quarantine` workflow step in FabricOps." not in dq_recommended


def test_advanced_modules_hidden_from_primary_docs_but_importable() -> None:
    modules_index = Path("docs/api/modules/index.md").read_text(encoding="utf-8")
    for hidden_module in [
        "data_drift",
        "data_product_metadata",
        "handover_documentation",
        "technical_audit_columns",
    ]:
        assert f"`{hidden_module}`" not in modules_index
