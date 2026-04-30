# Fabric notebook template workflow

The framework preserves existing deployed Fabric notebook helper names so older notebooks can continue running with minimal changes.

Preserved helper names include:
- `get_path`
- `lakehouse_table_read`
- `lakehouse_table_write`
- `clean_datetime_columns`
- `add_system_technical_columns`
- `ODI_METADATA_LOGGER`

Use `create_pipeline_notebook_template(...)` to generate a cell-separated `.py` notebook source with `# %%` / `# %% [markdown]` sections.

Copilot guidance:
- Use Fabric Copilot section by section.
- Do **not** ask Copilot to generate the whole notebook as one giant code block.

Public safety:
- Do not commit real workspace IDs.
- Do not commit real house/lakehouse IDs.
- Do not commit internal lakehouse names.
- Do not commit internal table names.
