# Build and install the starter kit wheel in Microsoft Fabric

This **Fabric-first, notebook-friendly, AI-in-the-loop starter kit** is designed to ship as a reusable package, not copy-paste helper cells in every notebook.

## Why use a wheel
A wheel-based install lets you:
- version starter kit behavior explicitly
- upload once to a Fabric Environment and reuse across notebooks
- test locally in VS Code and deploy consistently into Fabric
- keep notebook code focused on business context and transformation intent

This is the preferred path for MVP testing. `%run 00_config` can still be used as a temporary development fallback while iterating directly on helper functions.

## Prerequisites
- VS Code
- Python installed locally
- uv installed
- Access to the Fabric workspace
- Permission to create or edit a Fabric Environment
- Repo cloned locally

## 1. Clone the repo
```bash
git clone https://github.com/Voycepeh/fabric-data-product-framework.git
cd fabric-data-product-framework
```

## 2. Install uv
Windows (PowerShell):
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

macOS/Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 3. Create local environment
```bash
uv venv
uv sync
```

If `uv sync` cannot run yet (for example, no lockfile or you only need a fast local package install), use:
```bash
uv pip install -e .
```

## 4. Build the wheel
```bash
uv build --wheel
```

Expected output artifact:

`dist/fabric_data_product_framework-0.1.0-py3-none-any.whl`

## 5. Upload wheel to Microsoft Fabric Environment
1. Go to Microsoft Fabric.
2. Open the target workspace.
3. Open or create an Environment.
4. Go to **Libraries**.
5. Upload the `.whl` file from the local `dist/` folder.
6. Save and publish the Environment.
7. Wait for the Environment to finish publishing.

## 6. Attach Environment to notebook
1. Open the Fabric notebook.
2. Select the Environment from notebook settings.
3. Restart the session.
4. Run an import test.

```python
import fabric_data_product_framework as fdpf
print("FabricOps Starter Kit loaded")
```

You can also import helpers directly:

```python
from fabric_data_product_framework import get_path, lakehouse_table_read, lakehouse_table_write

lh_in = get_path("Sandbox", "Source")
lh_out = get_path("Sandbox", "Unified")
```

## 7. Use the template notebook
The template notebook is the runbook for onboarding and handover. The expected sequence is:
1. Introduction and data agreement
2. Parameters and environment setup
3. Source declaration
4. Source profiling
5. Schema drift, data drift, and incremental guards
6. EDA notes and business nuance
7. Transformation logic
8. Standard cleaning and technical columns
9. Output write
10. Output profiling
11. DQ rules
12. Governance labeling
13. Data contract summary
14. Lineage and AI handoff
15. Run summary and AI context export

What you edit:
- Dataset purpose
- Source and target environment
- Source table or file path
- Business metadata
- Transformation logic
- Data quality expectations
- Governance/sensitivity requirements

What the starter kit handles:
- Path resolution
- Lakehouse/warehouse IO helpers
- Profiling metadata capture
- Naming convention checks
- Standard datetime cleaning
- Technical audit columns
- Transformation summary helpers
- Metadata logging
- Future DQ/gov/lineage exports

Where AI is used:
- Generate draft DQ rules from profiling metadata and business context
- Translate layperson business rules into executable checks
- Summarise transformation logic from notebook code
- Generate lineage/handoff documentation
- Suggest governance labels from metadata and business context

In this model, humans provide business context and transformation intent, the framework handles repeatable engineering scaffolding, and AI supports DQ, lineage, governance suggestions, and handover documentation.

## 8. Update the wheel after code changes
```bash
uv build --wheel
```

Then:
- Upload the new wheel to the Fabric Environment
- Save and publish Environment
- Restart notebook session
- Re-run import test

When sharing with other users or teams, bump the package version first so they can confirm which wheel is installed.

## 9. Troubleshooting
- **ImportError after uploading wheel:** Environment may not be published yet, or notebook session was not restarted.
- **Old code still running:** Notebook session is using cached runtime state; restart the session.
- **Fabric-specific imports fail locally:** Expected outside Fabric for some adapters; keep Fabric-specific imports lazy inside functions where possible.
- **Wheel file not found:** Run `uv build --wheel` and confirm the `dist/` folder was created.
- **Package imports but functions missing:** Check `src/fabric_data_product_framework/__init__.py` exports.
- **Dependency unavailable in Fabric:** Add dependency to `pyproject.toml` only if needed, then rebuild/re-upload/publish.

## MVP validation checklist
- Wheel builds successfully with uv.
- Wheel appears in `dist/`.
- Wheel uploads to Fabric Environment.
- Fabric Environment publishes successfully.
- Notebook imports the framework without `%run 00_config`.
- `get_path("Sandbox", "Source")` returns a configured path object.
- `lakehouse_table_read` can read a known test/source table.
- `ODI_METADATA_LOGGER` can profile a test DataFrame.
- `lakehouse_table_write` can write to a test output table.
- Template notebook can run end to end on real data.
