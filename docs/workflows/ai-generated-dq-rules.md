# AI-generated DQ rules workflow (Fabric notebook + framework)

This is the canonical AI workflow doc for data quality rule generation.

## Decision boundary

**AI proposes. Humans approve. The framework validates and records.**

## Responsibility split

| Layer | Responsibility |
|---|---|
| Fabric Copilot | Notebook/code/prompt authoring assistance for practitioners. |
| Fabric AI functions (execution-time, where available) | Generate candidate DQ rules from explicit prompt context using `ai.generate_response` and summarize artifacts using `ai.summarize`. |
| Framework code | Build evidence context, parse outputs, validate shape, compile approved rules, execute checks, persist artifacts. |
| Human reviewer | Approve/reject AI candidates and decide whether a rule should be enforced. |

## Required evidence for AI suggestions

AI prompts should be grounded in explicit artifacts, not memory:
- Profile evidence (column stats, null behavior, value patterns).
- Metadata and contract context (critical fields, expectations, constraints).
- Business context (approved usage, caveats, known exclusions).

Do not depend on invisible chat history to define rules; all accepted rules must be reproducible from saved artifacts.

## End-to-end flow

```mermaid
flowchart TD
    A[Profile table] --> B[Build evidence-rich prompt context]
    B --> C[Call Fabric AI function in notebook]
    C --> D[Parse and validate candidate rules]
    D --> E[Store reviewable candidate artifacts]
    E --> F[Compile approved candidates to executable rules]
    F --> G[Run framework DQ checks]
    G --> H[Record quality + quarantine outputs]
```

## Steps

1. Profile source/output data with `profile_dataframe`.
2. Build prompt context with `build_quality_rule_prompt_context` and `build_quality_rule_generation_prompt`.
3. Call Fabric AI from notebook code (provider call stays outside the framework package).
4. Parse and validate candidates with `parse_ai_quality_rule_candidates`, `normalize_quality_rule_candidate`, and `validate_ai_quality_rule_candidate`.
5. Persist human-review artifacts with `build_layman_rule_records`.
6. Compile approved rules via `compile_layman_rules_to_quality_rules`.
7. Execute rules using `run_quality_rules` and gate with `assert_quality_gate` where required.
8. Produce row-level quarantine artifacts with `add_dq_failure_columns`, `split_valid_and_quarantine`, and `build_quarantine_summary_records`.

## Related docs
- Lifecycle placement: [../lifecycle-operating-model.md](../lifecycle-operating-model.md)
- API reference: [../../src/README.md](../../src/README.md)

## Fabric-native AI execution guidance

1. Preferred AI execution path is Fabric AI functions.
2. Use `ai.generate_response` for candidate DQ rules built from profile evidence, metadata context, and business context.
3. Use `ai.summarize` for transformation summaries, run summaries, and handover-friendly descriptions.
4. Use Microsoft Copilot for notebook authoring assistance and human-in-the-loop drafting.
5. The framework should build prompt context, parse AI responses, validate candidate shape, and store candidates for review.
6. Humans must approve candidates before enforcement.
7. Core enterprise flow should not require external internet access or external OpenAI endpoints.

`generate_dq_rule_candidates_with_fabric_ai` is the framework wrapper that orchestrates prompt construction and candidate parsing around Fabric-native AI functions.
