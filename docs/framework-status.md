# Framework Status

## Implemented in this repo

1. Dataset contract schema validation
2. DataFrame profiling utility
3. Schema snapshot and schema drift comparison
4. Engine-aware dataframe API pattern for pandas, Spark, and auto mode
5. Safe public examples and documentation structure
6. Data quality rule execution
7. AI-assisted DQ prompt, parse, validation, and compilation helpers
8. AI-assisted transformation summary prompt, parse, and record helpers
9. Row-level quarantine helper with partial rule coverage

## Partially implemented

1. Human approval pattern is documented, not a full approval workflow app/table yet
2. Fabric AI provider call remains notebook-layer
3. Quarantine is row-level for selected rules only

## Planned

1. Governance labeling checks
2. AI context export
3. Production dashboard schema
4. Full row-level coverage or explicit aggregate-only handling for all rule types

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
