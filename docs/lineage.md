# AI-assisted notebook lineage

Lineage in this framework is **not hard coded** and **not manually authored from scratch**.

Workflow:
1. User runs their Fabric notebook.
2. User calls `get_fabric_copilot_lineage_prompt()` and pastes the prompt into Fabric Copilot.
3. Copilot scans the entire notebook and returns Python code with `lineage_steps = [...]`.
4. User runs that generated cell.
5. Framework validates with `validate_lineage_steps(...)`.
6. Framework builds a structured record with `build_lineage_record_from_steps(...)`.
7. Framework renders notebook lineage with `plot_lineage_networkx(...)` (matplotlib + networkx).
8. Human reviews low-confidence/unknown/ambiguous items.
9. Approved lineage is stored as metadata or exported as JSON.

## Actor split

- **AI / Fabric Copilot**: scans notebook and drafts `lineage_steps`, including transformation summary and reason from code, markdown, and comments.
- **Framework**: provides schema + prompt, validates generated lineage, renders the diagram, and prepares metadata-ready records.
- **Human**: reviews low-confidence/"Needs human review" entries, corrects issues, and approves final lineage.

## Important scope clarification

- Microsoft Fabric native lineage view is useful for **workspace item-level dependencies**.
- This framework lineage is **notebook-level transformation lineage** (DataFrame/table/file flow inside notebook logic).
- Mermaid can be used in GitHub documentation when useful, but Fabric notebook lineage rendering should use matplotlib + networkx.

## Minimal runnable pattern

```python
import fabricops_kit as fw

prompt = fw.get_fabric_copilot_lineage_prompt()
print(prompt)

# Paste Copilot output here
lineage_steps = []

validation = fw.validate_lineage_steps(lineage_steps)
display(validation)

lineage_record = fw.build_lineage_record_from_steps(
    dataset_name=DATASET_NAME,
    lineage_steps=lineage_steps,
    run_id=RUN_ID,
)
display(lineage_record)

fw.plot_lineage_networkx(lineage_record, title=f"{DATASET_NAME} Notebook Lineage")
```

## Plotting dependencies

`plot_lineage_networkx(...)` requires `matplotlib` and `networkx`.

- In many Fabric notebook runtimes these may already exist.
- For local usage, install optional lineage extras:

```bash
pip install "fabricops-kit[lineage]"
```
