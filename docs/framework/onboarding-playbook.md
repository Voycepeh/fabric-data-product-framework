# Onboarding Playbook for Junior Engineers

Use this playbook to onboard a new data product using the framework in a repeatable and reviewable way.

## Step-by-step workflow

1. **Start with the requirements template.**
   Capture business purpose, key stakeholders, expected outcomes, and known constraints.
2. **Fill the table registry.**
   Define source-to-target mapping, ownership, refresh expectations, and sensitivity.
3. **Fill or generate the column dictionary.**
   Build column-level definitions, datatypes, nullable behavior, and key flags.
4. **Define expected refresh behavior.**
   Confirm batch vs incremental patterns and expected schedule/frequency.
5. **Define data contract.**
   Record agreed schema and quality expectations for the table.
6. **Define pipeline contract.**
   Record orchestration behavior, dependencies, retries, and alerting.
7. **Generate suggested DQ rules.**
   Use AI-assisted drafts for common checks and business-specific validations.
8. **Review rules with business/data owner.**
   Approve or reject each rule with explicit rationale.
9. **Run validation.**
   Execute approved checks during notebook/pipeline runtime.
10. **Check centralized logs.**
    Review validation outcomes, drift findings, and failed-check details.
11. **Generate handover pack.**
    Produce runbook, test plan, support notes, and known limitations from metadata.

## What AI can help with

- summarising requirements
- drafting metadata
- suggesting DQ rules
- explaining validation failures
- generating handover notes
- drafting runbooks

## Guardrails

- Treat AI output as draft content until human-approved.
- Keep approvals and exceptions in metadata for traceability.
- Avoid embedding business-critical assumptions only in notebook code.
