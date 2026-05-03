# Quick Start (MVP End-to-End Runbook)

Use this as the single runbook to execute the Fabric MVP workflow from local setup to handover artifacts.

## What this starter kit is for

FabricOps Starter Kit gives you a repeatable notebook-driven workflow to:
- profile source and output data,
- apply data quality and drift safety checks,
- run transformations with traceable rationale,
- write governed outputs, and
- export lineage/run/handover context.

It is **AI-in-the-loop**: AI drafts suggestions; humans approve business and release decisions.

## Before you start

Prepare these prerequisites:
- Python 3.11+ and [`uv`](https://docs.astral.sh/uv/) installed locally.
- Access to Microsoft Fabric workspace, Lakehouse/Warehouse, and Environment management.
- Permission to upload wheel files into a Fabric Environment.
- A dataset with clear business purpose and ownership.

Prepare these required human inputs up front:
- dataset purpose and approved usage,
- data steward/owner,
- business rules and acceptance thresholds,
- sensitivity/classification decisions.

## 1) Clone the repository

```bash
git clone https://github.com/Voycepeh/fabric-data-product-framework.git
cd fabric-data-product-framework
```

## 2) Set up with uv

```bash
uv sync --all-extras
```

Run local validation before Fabric execution:

```bash
uv run python -m compileall src tests
uv run python -m pytest -q
```

## 3) Build the wheel file

```bash
uv build
```

The package artifact is created under `dist/`.

## 4) Upload and install wheel in Microsoft Fabric Environment

1. In Fabric, open your target **Environment**.
2. Upload the wheel from `dist/`.
3. Publish/update the Environment.
4. Attach that Environment to your MVP notebook.

For UI-level details, see [UV wheel + Fabric install guide](UV_WHEEL_FABRIC_INSTALL_GUIDE.md).

## 5) Open and run the MVP notebook template

1. Open `templates/notebooks/fabric_data_product_mvp.md` in Fabric.
2. Copy/create your working notebook from the template.
3. Run cells section by section.

## 6) Edit required runtime parameters

At minimum, set parameters for:
- workspace/lakehouse target paths,
- source dataset identifiers,
- output table names/locations,
- run identifiers and environment flags.

Human review required:
- transformation rationale,
- governance labels,
- release gate decisions.

## 7) Declare source data

Define source locations and expected contract context in the notebook configuration cells. Keep assumptions explicit (grain, keys, freshness expectations).

## 8) Run source profiling

Execute profiling steps and capture artifacts for:
- schema,
- distributions/nulls,
- key candidate and uniqueness signals.

These profiling artifacts are inputs for DQ and governance suggestions.

## 9) Generate and review AI-assisted DQ rules

Use AI assistance to draft DQ rules from profiling metadata + business rules. Then perform human review/approval before enforcement.

AI assists with:
- candidate rule drafting,
- plain-language explanation of proposed checks.

Human approval required for:
- thresholds,
- exception policy,
- business criticality.

## 10) Run schema drift, data drift, and incremental safety checks

Execute starter-kit checks to detect:
- schema drift,
- profile/statistical drift,
- unsafe incremental/backfill patterns.

Treat failures as release gates; document overrides explicitly.

## 11) Run transformation section

Implement and run transformation logic in notebook transform cells. Use AI to help explain or summarize logic, but keep human ownership of final logic and rationale.

## 12) Write output tables

Persist transformed outputs to target Lakehouse/Warehouse tables following your naming and partition strategy.

## 13) Profile the output

Run output profiling and compare to source/expected patterns to catch regressions.

## 14) Produce governance labels/metadata

Generate governance metadata suggestions (AI-assisted optional), then perform human validation for:
- sensitivity labels,
- approved usage and caveats,
- ownership/steward fields.

## 15) Generate lineage and transformation summary

Create lineage and transformation summaries for consumers and maintainers.

AI can help draft concise summaries, but humans should validate accuracy.

## 16) Export AI context / handover pack

Export handover artifacts for the next maintainer, including:
- run summary,
- approved DQ/governance decisions,
- lineage context,
- transformation notes and open risks.

## 17) Confirm run succeeded

A successful MVP run includes all of the following:
- source and output profiling artifacts exist,
- DQ and drift checks executed and reviewed,
- outputs written successfully,
- governance metadata captured,
- lineage and handover package exported.

## AI-in-the-loop: what AI does vs what humans must do

AI can help generate or explain:
- DQ rules from profiling metadata and business rules,
- transformation summaries,
- lineage summaries,
- governance metadata suggestions,
- handover context for the next maintainer.

Human input is still required for:
- dataset purpose,
- approved usage,
- steward/owner,
- business rules,
- sensitivity decisions,
- transformation rationale review,
- release decision.

## Troubleshooting

- **Imports fail in Fabric notebook**: verify the Environment was published after wheel upload and attached to the notebook session.
- **Wrong package version loaded**: detach/reattach the Environment and restart notebook session.
- **DQ/drift checks fail unexpectedly**: re-check parameterization, source freshness, and threshold assumptions.
- **Output write failures**: validate destination path/table permissions and naming conventions.
- **Handover artifacts incomplete**: ensure run summary/lineage export cells were executed successfully.
