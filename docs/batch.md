# Batch Comparisons

Dift supports batch dataset comparison workflows for validating multiple dataset pairs in a single command.

Batch workflows help teams:

- validate ETL pipelines
- monitor warehouse snapshots
- compare multiple tables automatically
- run scheduled quality checks
- generate large-scale reports
- automate regression testing

---

# What Is Batch Comparison?

Batch comparison allows Dift to:

- scan two directories
- match datasets automatically
- run comparisons in sequence
- generate reports for each dataset pair

Dift matches files by filename.

Example:

```text
old/customers.csv  <-->  new/customers.csv
```

---

# Example Folder Structure

```text
data/
├── old/
│   ├── customers.csv
│   ├── orders.csv
│   └── products.csv
│
└── new/
    ├── customers.csv
    ├── orders.csv
    └── products.csv
```

---

# Run Batch Comparison

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --key customer_id
```

Dift automatically:

- matches files
- compares datasets
- calculates risk
- detects drift
- generates output

---

# Generate HTML Reports

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --key customer_id \
  --report html \
  --output-dir reports/
```

---

# Example Output Structure

```text
reports/
├── customers/
│   └── dift_report.html
├── orders/
│   └── dift_report.html
└── products/
    └── dift_report.html
```

---

# Generate JSON Reports

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --report json \
  --output-dir reports/json
```

---

# Generate CSV Reports

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --report csv \
  --output-dir reports/csv
```

---

# Generate Excel Reports

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --report excel \
  --output-dir reports/excel
```

---

# HTML Templates

Customize batch HTML reports:

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --report html \
  --template enterprise \
  --output-dir reports/
```

Available templates:

- default
- clean
- compact
- enterprise
- dark

---

# Continue On Error

By default, Dift continues running comparisons even if one dataset fails.

---

## Example

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --continue-on-error
```

Useful for:

- large pipelines
- scheduled monitoring
- partial dataset failures

---

# Stop On Error

Stop immediately after the first failure:

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --stop-on-error
```

Useful for:

- strict validation workflows
- CI/CD pipelines
- production gates

---

# Batch Comparison History

Save historical comparison records during batch execution.

---

## Example

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --history \
  --history-dir reports/history
```

---

# Example History Structure

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

# Batch + Strict Exit Codes

Enable automation-friendly exit codes.

---

## Example

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --strict-exit-codes
```

Exit codes:

| Code | Meaning |
|---|---|
| 0 | Low risk |
| 1 | Medium risk |
| 2 | High risk |
| 3 | Runtime error |

---

# Quiet Mode

Suppress non-error output:

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --quiet
```

Useful for:

- CI/CD systems
- cron jobs
- automated monitoring

---

# Disable Colored Output

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --no-color
```

Useful for:

- plain-text logs
- CI systems
- terminal compatibility

---

# Progress Indicators

Dift provides lightweight progress indicators during batch workflows.

Examples:

- dataset loading
- warehouse extraction
- schema comparison
- drift analysis
- report generation

Useful for:

- large datasets
- warehouse monitoring
- long-running workflows

---

# Supported Formats

Batch workflows support:

- CSV
- Parquet
- Excel
- JSON

---

# Supported Connectors

Batch workflows can integrate with:

- DuckDB
- SQL databases
- BigQuery
- warehouse workflows

depending on your dataset structure.

---

# Example ETL Validation Workflow

```bash
dift batch \
  --old-dir warehouse_snapshot_1 \
  --new-dir warehouse_snapshot_2 \
  --report html \
  --output-dir reports/
```

Useful for:

- ETL regression testing
- warehouse validation
- production monitoring

---

# Example ML Validation Workflow

```bash
dift batch \
  --old-dir train_v1 \
  --new-dir train_v2 \
  --threshold 0.03
```

Useful for:

- feature drift detection
- training validation
- ML dataset governance

---

# Example CI/CD Workflow

```bash
dift batch \
  --old-dir prod \
  --new-dir candidate \
  --report json \
  --strict-exit-codes \
  --quiet
```

---

# File Matching Rules

Dift matches datasets using filenames.

Example:

```text
old/customers.csv
new/customers.csv
```

Files without matches may generate warnings.

---

# Validation Errors

Dift provides actionable validation messages.

Examples:

```text
Error: Batch directory not found
```

```text
Error: No matching datasets found
```

```text
Error: Unsupported dataset type '.txt'
```

---

# Best Practices

Recommended practices:

- standardize filenames
- separate environments clearly
- enable history tracking
- use strict exit codes in CI/CD
- generate reports into isolated directories
- use templates for stakeholder reporting

---

# Common Use Cases

---

## ETL Validation

```bash
dift batch \
  --old-dir before \
  --new-dir after
```

---

## Warehouse Monitoring

```bash
dift batch \
  --old-dir snapshots/day1 \
  --new-dir snapshots/day2
```

---

## Scheduled Quality Checks

```bash
dift batch \
  --old-dir prod \
  --new-dir nightly
```

---

## Historical Drift Monitoring

```bash
dift batch \
  --history
```

---

# Example Enterprise Workflow

```bash
dift batch \
  --old-dir warehouse/prod \
  --new-dir warehouse/staging \
  --report html \
  --template enterprise \
  --history \
  --strict-exit-codes \
  --output-dir reports/
```

---

# Next Steps

Continue with:

- History
- Scheduling
- Automation
- Reports
- Connectors
- Developer Documentation