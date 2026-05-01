# AI-generated DQ rules (MVP steps 8 and 9)

## Scope
- **Step 8:** AI generate DQ rules from metadata, profile, and context.
- **Step 9:** Human review DQ rules.

## Inputs
- Source profile
- Business context
- Column metadata
- Data product purpose
- Expected grain
- Refresh pattern
- Approved usage

## Outputs
- Candidate DQ rules
- Reason
- Severity
- Suggested action
- Review status
- Approved rule record

## Flow
1. Build prompt context from profile + metadata + business context.
2. Generate candidate rules (AI or deterministic fallback).
3. Normalize and validate rule shape.
4. Present candidates for human review.
5. Approve/edit/reject and freeze approved rules.
6. Run DQ gate with approved rules and log artifacts.

Decision boundary: **AI proposes. Humans approve.**
