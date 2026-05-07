"""Pipeline contract notebook template (run-all-safe enforcement path)."""

from fabricops_kit import (
    add_audit_columns,
    add_datetime_features,
    add_hash_columns,
    assert_notebook_name_valid,
    bootstrap_fabric_env,
    build_dataset_run_record,
    build_lineage_from_notebook_code,
    build_lineage_handover_markdown,
    build_lineage_records,
    build_quality_result_records,
    build_runtime_context,
    default_technical_columns,
    generate_metadata_profile,
    generate_run_id,
    get_path,
    lakehouse_table_read,
    lakehouse_table_write,
    load_data_contract,
    load_fabric_config,
    profile_dataframe_to_metadata,
    run_quality_rules,
    validate_notebook_name,
    warehouse_read,
    warehouse_write,
    write_metadata_records,
)

# 1) Purpose and approved execution context
NOTEBOOK_NAME = "03_pc_agreement_source_to_target"
print("Pipeline notebook: enforcement only; no AI decisions and no exploration logic.")

# 2) Runtime startup checks
validate_notebook_name(NOTEBOOK_NAME)
assert_notebook_name_valid(NOTEBOOK_NAME)
CONFIG = load_fabric_config(CONFIG)  # Expects `%run 00_env_config` first.
bootstrap_fabric_env(config=CONFIG, environment="dev")

# 3) Load shared config
ENVIRONMENT = "dev"
RUN_ID = generate_run_id(prefix="pc")
runtime_context = build_runtime_context(
    dataset_name="target_dataset",
    environment=ENVIRONMENT,
    source_table="source.table",
    target_table="product.target_table",
    notebook_name=NOTEBOOK_NAME,
    run_id=RUN_ID,
)

# 4) Load approved data contract
CONTRACT_PATH = "contracts/examples/normalized_data_product_contract.yml"  # TODO replace
contract = load_data_contract(CONTRACT_PATH)

# 5) Source and target declaration
SOURCE_LAYER = "source"
TARGET_LAYER = "product"
SOURCE_TABLE = "TODO_source_table"
TARGET_TABLE = "TODO_target_table"

# 6) Load source data
source_house = get_path(ENVIRONMENT, SOURCE_LAYER, config=CONFIG)
target_house = get_path(ENVIRONMENT, TARGET_LAYER, config=CONFIG)
df_source = lakehouse_table_read(source_house, SOURCE_TABLE)

# 7) Pre-flight source validation
required_columns = set(contract.get("source_schema", {}).keys())
actual_columns = set(df_source.columns)
missing_columns = sorted(required_columns - actual_columns)
if missing_columns:
    raise ValueError(f"Fail fast: missing required source columns: {missing_columns}")

# 8) Apply approved transformation logic
# TODO: Replace with approved deterministic business transformation logic.
df_transformed = df_source

# 9) Apply approved DQ rules
approved_rules = contract.get("quality_rules", [])
dq_results = run_quality_rules(df_transformed, approved_rules, dataset_name="target_dataset")
if dq_results.get("failed"):
    raise ValueError("Fail fast: quality rules failed.")

# 10) Apply standard technical columns
df_standard = add_datetime_features(df_transformed)
df_standard = add_audit_columns(df_standard, run_id=RUN_ID)
df_standard = add_hash_columns(df_standard)
tech_cols = default_technical_columns()

# 11) Enforce output contract
expected_output_cols = set(contract.get("target_schema", {}).keys())
actual_output_cols = set(c for c in df_standard.columns if c not in tech_cols)
if expected_output_cols and expected_output_cols != actual_output_cols:
    raise ValueError("Fail fast: output contract mismatch.")

# 12) Write controlled output
WRITE_MODE = "overwrite"
TARGET_KIND = "lakehouse"  # lakehouse or warehouse
if TARGET_KIND == "lakehouse":
    write_result = lakehouse_table_write(df_standard, target_house, TARGET_TABLE, mode=WRITE_MODE)
else:
    write_result = warehouse_write(df_standard, target_house, schema="dbo", table=TARGET_TABLE, mode=WRITE_MODE)

# 13) Validate written output
df_written = lakehouse_table_read(target_house, TARGET_TABLE) if TARGET_KIND == "lakehouse" else warehouse_read(target_house, schema="dbo", table=TARGET_TABLE)
if df_written.count() == 0:
    raise ValueError("Fail fast: target write produced zero rows.")

# 14) Profile output
output_profile = generate_metadata_profile(df_written, dataset_name="target_dataset")
output_profile_rows = profile_dataframe_to_metadata(df_written, dataset_name="target_dataset")

# 15) Write metadata records
quality_records = build_quality_result_records(dq_results, dataset_name="target_dataset", run_id=RUN_ID)
dataset_record = build_dataset_run_record(dataset_name="target_dataset", run_id=RUN_ID, row_count=df_written.count())
write_metadata_records([*quality_records, dataset_record, *output_profile_rows], config=CONFIG)

# 16) Build lineage records
lineage = build_lineage_from_notebook_code(__file__, dataset_name="target_dataset", run_id=RUN_ID)
lineage_records = build_lineage_records(dataset_name="target_dataset", run_id=RUN_ID, lineage_steps=lineage.get("steps", []))

# 17) Build handover markdown
handover_markdown = build_lineage_handover_markdown(dataset_name="target_dataset", run_id=RUN_ID, lineage_result=lineage)
print(handover_markdown)
