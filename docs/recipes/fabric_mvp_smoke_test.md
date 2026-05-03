# Fabric MVP Smoke Test Recipe

## Purpose

Use this smoke test to validate the end-to-end Microsoft Fabric lifecycle workflow after packaging and environment setup. It confirms that the framework can:

- build as a wheel
- install into a Fabric Environment
- import correctly inside a Fabric notebook
- run the lifecycle workflow in safe sample mode
- generate profiling output
- generate or load DQ rules
- run DQ validation
- review drift/incremental guard status
- generate governance suggestions
- generate lineage and AI handoff context
- produce a final release gate
- keep Fabric writes disabled until explicitly approved

## When to run

Run this recipe:

- after packaging changes
- after MVP notebook template changes
- after DQ/profiling/drift/governance/lineage/metadata/run summary changes
- before full actual-data MVP testing
- before publishing a new wheel for team use

## Prerequisites

Before running this smoke test, confirm:

- latest `main` pulled locally
- wheel built using `docs/setup/fabric-wheel-install.md`
- wheel uploaded to Fabric Environment custom libraries
- Environment published
- Environment attached to notebook
- notebook session restarted
- MVP notebook template available
- optional Fabric workspace access for write-enabled test

References:

- [UV wheel build + Fabric install guide](../setup/fabric-wheel-install.md)
- [MVP notebook template](../../templates/notebooks/fabric_data_product_mvp.py)

## Test mode matrix

| Mode | Purpose | Key settings | Writes enabled | Expected outcome |
|---|---|---|---|---|
| Local/package sanity | Verify package builds and tests locally | N/A | No | Compile/tests pass |
| Fabric sample safe mode | Validate full workflow with deterministic safe inputs | `USE_SAMPLE_DATA=True`, `ENABLE_FABRIC_WRITES=False` | No | Full workflow runs without writing tables |
| Fabric actual data dry run | Validate real-source behavior without writes | `USE_SAMPLE_DATA=False`, `ENABLE_FABRIC_WRITES=False` | No | Real source profile/DQ/governance/lineage summary generated without target writes |
| Fabric approved write run | Validate controlled write path after review | `USE_SAMPLE_DATA=False`, `ENABLE_FABRIC_WRITES=True` | Yes (approved only) | Target and metadata tables written only after review |

## Step-by-step smoke test

### 1) Local validation

Run:

```bash
git checkout main
git pull
uv sync
uv run python -m compileall src tests
uv run python -m pytest -q
uv build
```

If `uv` cannot access PyPI in your environment, record that limitation and run equivalent `python` commands where possible.

### 2) Fabric Environment validation

1. Upload `dist/*.whl` as a custom library in your Fabric Environment.
2. Publish/save the Environment.
3. Attach the Environment to the notebook.
4. Restart the notebook session.
5. Run import/version validation:

```python
import fabricops_kit as fdpf

print("Package path:", fdpf.__file__)
print("Package version:", getattr(fdpf, "__version__", "unknown"))
```

### 3) MVP notebook safe sample run

Expected settings:

```python
USE_SAMPLE_DATA = True
ENABLE_FABRIC_WRITES = False
ENABLE_AI_ASSISTED_DQ = False
ENABLE_AI_ASSISTED_GOVERNANCE = False
ENABLE_AI_ASSISTED_LINEAGE = False
```

Expected outcome:

- notebook runs all cells
- no Fabric tables are written
- intentional sample DQ issues appear
- final gate may be `NOT_READY` if governance approval is false, and that is acceptable

### 4) Review generated artifacts

Checklist:

- source profile has row count, column count, null stats, distinct stats
- DQ rules are visible and understandable
- DQ summary includes passed/failed/warning counts
- row-level issues are visible if supported
- drift section explains baseline vs compare behavior
- governance classification suggests identifiers/sensitive fields
- lineage steps are machine-readable
- AI handoff context includes business context, profile, DQ, drift, governance, lineage, limitations
- final gate gives reasons, not just pass/fail

### 5) Actual data dry run

1. Switch `USE_SAMPLE_DATA=False`.
2. Set generic source/target placeholders (for example, `SOURCE_TABLE = "<SOURCE_TABLE>"` and `TARGET_TABLE = "<TARGET_TABLE>"`).
3. Keep `ENABLE_FABRIC_WRITES=False`.
4. Run against the actual source.
5. Review row counts and performance.
6. Confirm no target table is written.

### 6) Approved write run

1. Confirm target table names.
2. Confirm metadata table names.
3. Confirm DQ rules approved.
4. Confirm governance classification reviewed.
5. Confirm lineage reviewed.
6. Set `ENABLE_FABRIC_WRITES=True`.
7. Run again.
8. Verify output/metadata/result tables exist.

## Pass/fail criteria

PASS if:

- package imports in Fabric
- version matches expected wheel
- sample mode runs end to end
- deterministic DQ rules run
- sample DQ issues are surfaced
- no writes happen in safe mode
- run summary and AI handoff context are generated
- final gate gives clear readiness status

FAIL if:

- import fails
- wrong package version loads
- notebook writes when `ENABLE_FABRIC_WRITES=False`
- deterministic DQ rules cannot run
- final gate is missing or ambiguous
- actual data dry run cannot profile source
- approved write mode writes to unexpected tables

## Evidence to record

Use this table template for each smoke-test execution:

| Date | Tester | Git commit SHA | Package version | Wheel filename | Fabric workspace/environment name | Notebook name | Mode tested | Result | Notes/failure reason |
|---|---|---|---|---|---|---|---|---|---|
| YYYY-MM-DD | `<name>` | `<sha>` | `<version>` | `<wheel.whl>` | `<workspace / environment>` | `<notebook>` | `<mode>` | PASS/FAIL | `<notes>` |

## Troubleshooting

- old wheel still loaded
- Environment not published
- notebook session not restarted
- wrong Environment attached
- package version mismatch between `pyproject.toml` and `__init__.__version__`
- missing Fabric runtime dependency
- sample mode passes but actual data fails due to schema/content assumptions
- writes disabled by default
- AI-assisted sections disabled by default

## Relationship to PR 69

This recipe assumes the MVP notebook template exposes safe runtime flags such as `USE_SAMPLE_DATA` and `ENABLE_FABRIC_WRITES`. If PR 69 changes those names, rebase PR 70 and update this recipe before merge.
