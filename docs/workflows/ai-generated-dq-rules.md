# AI-generated DQ rules (MVP steps 8 and 9)

This workflow maps directly to:
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
1. Build prompt context from profile + metadata + business inputs.
2. Generate candidate DQ rules with AI (or dry-run stub).
3. Parse and normalize candidate rules.
4. Human reviewer approves/edits/rejects.
5. Freeze approved rule records for enforcement.

Rule enforcement remains human-approved only.
