# Lifecycle Operating Model

![FabricOps Starter Kit end-to-end workflow](assets/mvp-flow.png)

*Figure: The practical end-to-end workflow used to move from approved purpose to publishable, governed outputs and handover artifacts.*

# Lifecycle Operating Model

FabricOps Starter Kit follows an end-to-end lifecycle for building Fabric data products that are governed, repeatable, explainable, and ready for handover.

The goal is not just to move data from source to target. The goal is to make the purpose, source assumptions, transformation rationale, data quality rules, governance checks, lineage, and handover notes explicit enough that another engineer, analyst, or data steward can understand and operate the pipeline later.

## Canonical Lifecycle

### 1. Define purpose, approved usage, and governance ownership

Start with why the data product exists and whether the data is approved for the intended use.

At minimum, capture:

* Data product purpose
* Approved usage
* Data agreement or approval reference
* Data steward
* Data product manager
* Release approver
* Known restrictions
* Initial sensitivity or confidentiality assumptions

This section can be backfilled as the project matures, but the data steward and data product manager should be known early.

### 2. Configure runtime, environment, dependencies, and path rules

Set up the operating context required for the notebook or pipeline to run safely.

This includes:

* Development and production environment selection
* Lakehouse and Warehouse path configuration
* Source, unified, and product store routing
* Runtime dependency checks
* Notebook naming rules
* Prompt templates used by AI-assisted functions
* Shared configuration used by framework functions

This step exists because Fabric notebooks usually operate with one default attached data store. When a workflow needs to move data across multiple Lakehouses or Warehouses, the paths and routing rules need to be explicit in code.

### 3. Declare source contract and ingest source data

Before treating the source as reliable, declare what the source is expected to provide.

The source contract should describe:

* Source owner
* Source system
* Source table, file, or path
* Load type, such as one-time load, full refresh, or incremental load
* Refresh frequency
* Expected schema
* Expected data types
* Required columns
* Allowed extra columns, if any
* Primary key or business key
* Incremental column or partition column
* Expected freshness
* Expected row volume range
* Known source limitations

Then ingest the source based on that contract.

The source contract is the pipeline agreement with the upstream source. It defines what the source should look like, how often it should arrive, and how the pipeline should detect when the source has changed unexpectedly.

### 4. Validate source against contract and profile reusable metadata

After ingestion, validate the actual source against the declared source contract.

This can include:

* Schema drift checks
* Data type drift checks
* Missing column checks
* Unexpected column checks
* Freshness checks
* Incremental window checks
* Duplicate key checks
* Volume drift checks
* Null threshold checks
* Value range or category drift checks

Drift should be powered by the source contract. The contract defines expectation, the profile captures reality, and the drift check compares the two.

The source profile should also be saved as reusable metadata. This metadata becomes the factual base for:

* Data quality rule generation
* Schema and data drift monitoring
* Sensitivity and classification suggestions
* Lineage and transformation summaries
* Handover documentation

### 5. Explore data and capture transformation / data quality rationale

Use exploration notebooks to investigate the data and document why transformations or quality rules are needed.

Exploration should capture:

* Exploratory findings
* Data issues discovered
* Business logic assumptions
* Transformation rationale
* Data quality rationale
* Manual decisions made during analysis

Exploration logic should not automatically become part of the scheduled production pipeline. Once a finding matters operationally, convert it into a reusable transformation, validation, source contract expectation, or data quality rule.

### 6. Build production transformation and write target output

Use pipeline notebooks to implement repeatable transformation logic and write target data.

This step should include:

* Business transformations
* Standard cleaning patterns
* Common date and time standardization
* Audit columns
* Technical lineage columns
* Contract-driven drift checks where appropriate
* Output write logic
* Read-back checks after writing

The production pipeline notebook should be safe to run end to end. Diagnostic or exploratory cells should be removed, frozen, or clearly separated from scheduled execution.

### 7. Validate output and persist target metadata

After writing the target table, validate that the output was written correctly.

This should include:

* Row count checks
* Target read-back checks
* Output schema checks
* Output completeness checks
* Target metadata profiling
* Run-level logging where applicable

Target metadata should be saved so future users can understand what was produced, when it was produced, and how the output changed over time.

### 8. Generate, review, and configure data quality rules

Use profile metadata and exploration rationale to generate draft data quality rules.

This can be done through:

* Fabric native AI functions where available
* A generated prompt manually copied into ChatGPT, Claude, or another LLM
* Manual rule drafting where AI is not appropriate

AI can help draft rules from metadata, but the rules should not be accepted blindly.

A human reviewer should validate and configure the executable checks, such as:

* Not-null checks
* Uniqueness checks
* Accepted value checks
* Range checks
* Referential checks
* Freshness checks
* Business logic checks

Only reviewed and accepted rules should be added to the pipeline.

### 9. Generate and review classification / sensitivity suggestions

Use AI to suggest classification and sensitivity labels where a mature human-labelled governance setup is not yet available.

This may include suggestions for:

* Confidential columns
* Personal data
* Restricted fields
* Business-sensitive attributes
* Recommended handling notes
* Fields that require masking, restricted access, or steward review

These suggestions support governance, but final classification still requires human review.

### 10. Approve release and produce lineage + handover documentation

Before release, the data product must be reviewed and approved by the responsible data steward or assigned approver.

Approval should confirm:

* Purpose is valid
* Usage is approved
* Source contract is documented
* Drift expectations are configured
* Data quality rules are reviewed
* Sensitivity classification is reviewed
* Output is suitable for release
* Known limitations are documented

The final handover package should include:

* Purpose and approved usage
* Ownership and governance context
* Source contract
* Runtime and environment setup
* Transformation summary
* Data quality rules
* Classification notes
* Lineage summary
* Refresh logic
* Known limitations
* Operational notes

AI should assist with generating lineage, transformation summaries, and handover documentation by scanning the notebook, source contract, profiling metadata, and accepted rules.

The final outcome should be a Fabric data product that another engineer, analyst, or steward can understand, operate, review, and improve with minimal handholding.
