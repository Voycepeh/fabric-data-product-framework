# Source package guide (`src/fabric_data_product_framework`)

This package keeps runtime logic in `src/fabric_data_product_framework/` and publishes user-facing callables through `fabric_data_product_framework.__all__` in `src/fabric_data_product_framework/__init__.py`.

## Public callable catalogue sources

- **Public callable source of truth:** `__all__` in `src/fabric_data_product_framework/__init__.py`.
- **Workflow registry source:** `get_mvp_step_registry` in `src/fabric_data_product_framework/handover.py` (canonical 13-step mapping and module ownership).
- **Generated docs outputs:**
  - Step-first reference: `docs/reference/index.md`
  - Module catalogues: `docs/api/modules/*.md`

## Regenerate the function reference

```bash
PYTHONPATH=src python scripts/generate_function_reference.py
```

Run the generator whenever public exports change (add/remove/rename) so GitHub Pages stays aligned with the package surface.
