# Framework Status

## Implemented in this repo

1. Dataset contract schema validation
2. DataFrame profiling utility
3. Schema snapshot and schema drift comparison
4. Engine-aware dataframe API pattern for pandas, Spark, and auto mode
5. Safe public examples and documentation structure

## Proven in the Fabric notebook pattern

1. Dataset purpose and approved usage section
2. Notebook parameters and environment setup
3. Naming convention check
4. Source table declaration
5. Source profiling written to metadata table
6. EDA notes and frozen data nuance explanation
7. Core transformation section designed for run-all execution
8. Technical audit columns
9. Datetime standardization such as timezone conversion, date, time, and time block columns
10. Lakehouse write pattern
11. Output profiling written to metadata table
12. AI-assisted lineage prompt/template

## Planned next

1. Governance labeling checks
2. AI context export

## Implemented or partially implemented

1. Data quality rule execution (`run_quality_rules`, quality result records, and quality gate)
2. AI-assisted DQ rule generation workflow (provider-neutral prompt building/parsing/validation)
3. DQ rule compilation from layman candidates to executable quality rules
4. Row-level quarantine helper for pandas/Spark (`add_dq_failure_columns`, `split_valid_and_quarantine`)
5. Human approval pattern documented in workflow docs (implementation pattern, not full governance app)
6. AI-assisted transformation summary workflow (partially implemented: framework prompt/parse/record helpers; provider call remains notebook-layer)
7. Data drift checks, incremental partition safety checks, runtime data contract enforcement, automated lineage summary, and run summary are implemented in this repository

Note: AI provider integration remains notebook-layer (for example Fabric AI response APIs).

## GitHub vs Fabric

### GitHub (source of truth)

- Templates and reusable framework code
- Contracts, examples, tests, and documentation
- Review history and change control

### Fabric (execution environment)

- Notebook and pipeline execution
- Lakehouse reads/writes and operational runs
- Metadata tables, monitoring, and runtime outputs

## Repository status

This repository is in an **early scaffold** stage. The current focus is standards, lifecycle consistency, and safe public templates.
