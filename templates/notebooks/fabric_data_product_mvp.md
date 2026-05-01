# Fabric data product MVP notebook template

This page explains how to use `templates/notebooks/fabric_data_product_mvp.py` as the starter for testing the framework in Microsoft Fabric. Recommended first run is DRY_RUN with synthetic data.

## Recommended first-run path
1. Open `templates/notebooks/fabric_data_product_mvp.py`
2. Create a new Fabric notebook
3. Copy/paste the template into Fabric
4. Run it in DRY_RUN mode first
5. Validate outputs using `docs/fabric-smoke-test.md`
6. Replace placeholder reader/writer adapters only after the dry run works

## What the template covers
The template aligns to the current 13-step MVP workflow:
1. Define data product
2. Setup config and environment
3. Declare source and ingest data
4. Profile source and capture metadata
5. Explore data
6. Explain transformation logic
7. Build transformation pipeline
8. AI generate DQ rules
9. Human review DQ rules
10. AI suggest sensitivity labels
11. Human review and governance gate
12. AI generated lineage and transformation summary
13. Handover framework pack


## Preferred packaged setup (Fabric Environment)
Use package imports as the default path when running notebooks attached to a Fabric Environment:

```python
from fabric_data_product_framework import (
    get_path,
    lakehouse_table_read,
    lakehouse_table_write,
    ODI_METADATA_LOGGER,
    clean_datetime_columns,
    add_system_technical_columns,
    check_naming_convention,
)
```

Development fallback while editing helpers directly in Fabric:

```python
# %run 00_config
```

Use the packaged import for repeatable onboarding, validation, and handover. Use `%run 00_config` only as a temporary early-development fallback when changing helper function internals in-notebook.

## Adapter replacement points
The current template includes one placeholder adapter that you replace when moving from synthetic dry-run to real Fabric reads:
- `fabric_reader(table_name: str)`

The template currently keeps writes in-memory via `output_table` (`written_in_fabric` marker when not in dry run), so add your own Fabric write path in the transformation/output section after dry-run validation.

## How to customize safely
- Keep the synthetic/default dry-run path first.
- Then swap source read for real Fabric source.
- Then add real target write.
- Then connect metadata outputs if needed.
- Keep AI outputs human-reviewed before production use.

## Expected outputs
The template assembles these main artifacts:
- `data_product_context`
- `runtime_config`
- `source_declaration`
- `source_profile`
- `exploration_notes`
- `transformation_rationale`
- `output_table`
- `dq_candidate_rules`
- `approved_dq_rules`
- `sensitivity_suggestions`
- `approved_governance_labels`
- `lineage_record`
- `handover_pack`

## Related pages
- `docs/fabric-smoke-test.md`
- `docs/mvp-workflow.md`
- `src/README.md`
