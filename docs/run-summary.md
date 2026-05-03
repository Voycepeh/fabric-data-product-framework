# Run Summary

Run summaries provide a concise, human-readable handover artifact for each execution.

They combine runtime context plus optional results from profiling, drift, incremental safety, quality, contracts, and lineage.

## Why it helps

- Faster analyst/engineer handover
- Metadata-table-ready flattened record
- Future-ready input for AI context export workflows

## Example

```python
from fabricops_kit.run_summary import build_run_summary, render_run_summary_markdown, build_run_summary_record

summary = build_run_summary(runtime_context=ctx, quality_result=quality_result, contract_validation_result=contract_result)
print(render_run_summary_markdown(summary))
record = build_run_summary_record(summary)
```
