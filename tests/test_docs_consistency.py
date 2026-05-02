from __future__ import annotations

from pathlib import Path
import inspect

from fabric_data_product_framework import drift, incremental, metadata, profiling, technical_columns


IMPORTANT_PUBLIC_FUNCTIONS = [
    profiling.profile_dataframe,
    profiling.flatten_profile_for_metadata,
    technical_columns.add_audit_columns,
    technical_columns.add_hash_columns,
    technical_columns.add_datetime_features,
    drift.build_schema_snapshot,
    drift.compare_schema_snapshots,
    incremental.build_partition_snapshot,
    incremental.compare_partition_snapshots,
    metadata.build_dataset_run_record,
    metadata.write_multiple_metadata_outputs,
]


def test_important_public_functions_have_docstrings():
    missing = [func.__name__ for func in IMPORTANT_PUBLIC_FUNCTIONS if not inspect.getdoc(func)]
    assert missing == []


def test_readme_contains_callable_function_reference_section():
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "Callable Function Reference" in readme


def test_fabric_manual_validation_doc_exists():
    assert Path("docs/fabric-manual-validation.md").exists()


def test_docs_do_not_use_outdated_technical_columns_argument_names():
    banned = ["pipeline_run_id=", "business_key_columns=", "row_hash_columns="]
    files_to_check = [Path("README.md"), *Path("docs").rglob("*.md")]
    offending: list[tuple[str, str]] = []
    for file_path in files_to_check:
        text = file_path.read_text(encoding="utf-8")
        for token in banned:
            if token in text:
                offending.append((str(file_path), token))
    assert offending == []
