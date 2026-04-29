# Fabric smoke test example

This example shows a minimal Fabric notebook path to verify framework wiring with synthetic data.

## Files
- `synthetic_orders_contract.yaml`: sample dataset contract.
- `synthetic_orders_source.py`: notebook cell to create source table.
- `smoke_test_notebook.py`: simplified run flow using adapters.

## Suggested run order
1. Bootstrap metadata tables using `docs/metadata-table-bootstrap.md`.
2. Run `synthetic_orders_source.py` in a Fabric notebook.
3. Configure paths and table identifiers in `smoke_test_notebook.py`.
4. Execute with `DRY_RUN=True` first.
5. Validate metadata rows, then run with writes enabled.
