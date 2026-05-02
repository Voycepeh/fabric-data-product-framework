# Source package guide (`src/fabric_data_product_framework`)

Open `mvp_steps.py` first when manually testing in Fabric notebooks. It gives the end-to-end notebook run order and references the canonical module for each step.

## Module ownership

- **Environment and Fabric IO**: `fabric.py`, `runtime.py`
- **Profiling and metadata**: `profiling.py`, `metadata.py`
- **Data quality and rule compilation**: `quality.py`, `rule_compiler.py`, `ai_quality_rules.py`
- **Drift and incremental safety**: `drift.py`, `incremental.py`
- **Governance and sensitivity classification**: `governance.py`
- **Lineage and AI handover**: `lineage.py`, `ai_lineage_summary.py`
- **Runtime summary and orchestration**: `run_summary.py`, `contracts.py`
- **Templates and notebook helpers**: `template_generator.py`, `mvp_steps.py`

## Recommended manual Fabric test order

1. Configure runtime and identifiers (`runtime.py`, `fabric.py`).
2. Read source table/file (`fabric.py`).
3. Profile source (`profiling.py`).
4. Generate or compile quality rules (`ai_quality_rules.py`, `rule_compiler.py`).
5. Run quality checks (`quality.py`).
6. Check schema/profile/partition drift (`drift.py`, `incremental.py`).
7. Apply governance classification (`governance.py`).
8. Transform and write output (`fabric.py`, project notebook cell).
9. Profile output (`profiling.py`).
10. Build lineage and handover summary (`lineage.py`, `ai_lineage_summary.py`).
11. Write run summary (`run_summary.py`, `metadata.py`).

## MVP run order helper

Use `mvp_steps.py` for a notebook-friendly list:

```python
from fabric_data_product_framework.mvp_steps import get_mvp_step_registry

for step in get_mvp_step_registry():
    print(
        step["step_number"],
        step["step_name"],
        step["owner_type"],
        step["canonical_modules"],
    )
```


## Canonical 13 step MVP flow

Use the canonical flow artifacts below when onboarding or running end-to-end smoke tests in Fabric:

- Template notebook: `templates/notebooks/fabric_data_product_mvp.py`
- Roadmap: `docs/mvp-13-step-roadmap.md`
- Registry + artifact validation helpers: `src/fabric_data_product_framework/mvp_steps.py`
