# Public Repository Safety

This repository is intended for public use. Keep all examples and artifacts synthetic.

## Safe to include

- Generic framework code
- Synthetic examples
- Templates
- Fake metadata
- Fake contracts
- Generic documentation
- Tests using synthetic data

## Unsafe to include

- Real data
- Production metadata exports
- Internal table names
- Tenant IDs
- Workspace names
- Service principal details
- Secrets
- Internal URLs
- Screenshots with sensitive details
- Real staff/student/customer examples

## Recommended practices

- Use clearly fake project, workspace, and table names (for example, `demo_sales_orders`).
- Redact any accidental identifiers before commit.
- Validate sample configs contain placeholder emails and non-production domains.
- Prefer generated synthetic records for tests and examples.
