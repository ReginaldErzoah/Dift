# Comparison History

Dift supports persistent comparison history tracking for monitoring dataset drift and risk over time.

History tracking helps teams:

- monitor recurring drift
- analyze long-term risk trends
- audit validation workflows
- investigate incidents
- track dataset trust evolution
- build governance workflows

---

# Why History Tracking Matters

Modern datasets change constantly.

Without historical tracking, teams often cannot answer:

- When did drift begin?
- Has this issue happened before?
- Is risk increasing over time?
- Which datasets are unstable?
- Which pipelines regress frequently?

Dift history tracking helps answer these questions.

---

# Enable History Tracking

Save comparison history automatically:

```bash
dift old.csv new.csv \
  --key customer_id \
  --history
```

---

# Default History Location

By default, Dift stores history in:

```text
.dift/history/history.jsonl
```

---

# Custom History Directory

Specify a custom history location:

```bash
dift old.csv new.csv \
  --key customer_id \
  --history \
  --history-dir reports/history
```

Useful for:

- CI/CD systems
- centralized storage
- audit workflows
- scheduled monitoring

---

# View History Records

List saved comparison runs:

```bash
dift history list
```

---

# Example Output

```text
1. 2026-05-15T12:30:00Z | risk=medium | old.csv -> new.csv
2. 2026-05-16T08:10:00Z | risk=high | prod.csv -> staging.csv
3. 2026-05-17T03:45:00Z | risk=low | train_v1.csv -> train_v2.csv
```

---

# Show Detailed History Entry

Inspect a specific comparison record:

```bash
dift history show 1
```

---

# Example Output

```json
{
  "timestamp": "2026-05-15T12:30:00Z",
  "risk_level": "medium",
  "old_dataset": "old.csv",
  "new_dataset": "new.csv",
  "row_delta": 150,
  "schema_changes": 2,
  "warnings": [
    "Numeric drift detected in revenue"
  ]
}
```

---

# Clear History

Delete all saved history:

```bash
dift history clear
```

Useful for:

- resetting environments
- test workflows
- temporary monitoring setups

---

# Batch Comparison History

History tracking also works with batch comparisons.

---

## Example

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --history
```

---

# Batch History Structure

```text
reports/
└── history/
    ├── customers/
    │   └── history.jsonl
    ├── orders/
    │   └── history.jsonl
    └── products/
        └── history.jsonl
```

---

# What Gets Stored

History records may include:

- timestamp
- dataset paths
- comparison runtime
- risk level
- row statistics
- schema changes
- drift warnings
- threshold metadata
- report configuration

---

# Historical Risk Monitoring

Track risk changes over time.

Example:

```text
Day 1 → LOW
Day 2 → MEDIUM
Day 3 → HIGH
```

Useful for:

- anomaly detection
- pipeline instability monitoring
- warehouse validation
- ML data governance

---

# Historical Drift Monitoring

Monitor recurring numeric and categorical drift.

Examples:

- revenue drift
- customer segmentation changes
- feature distribution shifts
- outlier spikes

---

# Historical Quality Monitoring

Track:

- null spikes
- duplicate spikes
- schema instability
- dataset volatility

Useful for:

- data governance
- SLA monitoring
- reliability analysis

---

# Example Automation Workflow

```bash
dift prod.csv staging.csv \
  --key customer_id \
  --history \
  --strict-exit-codes
```

Useful for:

- CI/CD pipelines
- scheduled monitoring
- nightly validations

---

# Scheduled History Workflows

Combine history tracking with schedules.

---

## Example

```bash
dift schedule create nightly-check \
  --profile production-validation \
  --cron "0 2 * * *"
```

Generated workflow:

```bash
dift profile run production-validation \
  --history \
  --strict-exit-codes
```

---

# History + HTML Reports

Generate reports while tracking history.

---

## Example

```bash
dift old.csv new.csv \
  --report html \
  --output report.html \
  --history
```

Useful for:

- audits
- stakeholder reviews
- historical reporting

---

# History + JSON Reports

Useful for machine-readable audit systems.

---

## Example

```bash
dift old.csv new.csv \
  --report json \
  --history
```

---

# Example CI/CD Integration

```bash
dift prod.csv candidate.csv \
  --history \
  --strict-exit-codes \
  --quiet
```

Useful for:

- GitHub Actions
- Jenkins
- Airflow
- Dagster
- Prefect

---

# Example ML Monitoring Workflow

```bash
dift train_v1.csv train_v2.csv \
  --threshold 0.03 \
  --history
```

Useful for:

- feature drift tracking
- model retraining validation
- training stability analysis

---

# Example Warehouse Monitoring Workflow

```bash
dift snowflake://... \
     snowflake://... \
     --history
```

Useful for:

- production warehouse monitoring
- nightly validation
- trust enforcement

---

# History File Format

Dift uses JSON Lines format:

```text
history.jsonl
```

Benefits:

- append-only
- machine-readable
- scalable
- streaming-friendly
- audit-friendly

---

# Example History Record

```json
{
  "timestamp": "2026-05-15T12:30:00Z",
  "risk_level": "high",
  "old_dataset": "prod.csv",
  "new_dataset": "candidate.csv"
}
```

---

# Validation Errors

Dift provides actionable history validation messages.

Examples:

```text
Error: History directory not found
```

```text
Error: Invalid history record
```

```text
Error: Failed to load history file
```

---

# Best Practices

Recommended practices:

- enable history in production workflows
- separate history directories by environment
- combine history with strict exit codes
- archive long-term records
- use reports for investigations
- integrate with automation systems

---

# Common Use Cases

---

## ETL Monitoring

```bash
dift before.csv after.csv --history
```

---

## Production Monitoring

```bash
dift prod.csv staging.csv --history
```

---

## ML Drift Tracking

```bash
dift train_v1.csv train_v2.csv --history
```

---

## Governance Auditing

```bash
dift history list
```

---

## Historical Risk Analysis

```bash
dift history show 1
```

---

# Example Enterprise Workflow

```bash
dift batch \
  --old-dir warehouse/prod \
  --new-dir warehouse/staging \
  --history \
  --strict-exit-codes \
  --report html \
  --template enterprise
```

---

# Next Steps

Continue with:

- Scheduling
- Automation
- Reports
- Connectors
- Plugin Architecture
- Developer Documentation