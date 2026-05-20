# Automation

Dift is designed to support automation-first data validation workflows.

This document explains how to integrate Dift into:

- CI/CD pipelines
- cron jobs
- scheduled workflows
- Airflow
- Jenkins
- GitHub Actions
- Prefect
- Dagster
- enterprise monitoring systems

---

# Why Automation Matters

Modern data systems continuously evolve.

Bad data can silently break:

- dashboards
- ML models
- ETL pipelines
- reports
- warehouse transformations
- production analytics

Dift helps automate trust validation before bad data propagates downstream.

---

# Core Automation Features

Dift automation features include:

- reusable profiles
- scheduled comparisons
- strict exit codes
- quiet mode
- no-color mode
- comparison history
- batch workflows
- reusable configs
- environment-aware execution

---

# Automation Philosophy

Dift automation workflows prioritize:

- reproducibility
- machine-readable outputs
- predictable execution
- CI/CD compatibility
- non-interactive workflows

---

# Non-Interactive CLI Execution

Dift fully supports non-interactive execution.

Example:

```bash
dift old.csv new.csv \
  --key customer_id \
  --strict-exit-codes \
  --quiet \
  --no-color
```

This is ideal for:

- cron jobs
- CI/CD systems
- scheduled monitoring
- automated warehouse checks

---

# Strict Exit Codes

Strict exit codes allow Dift to fail workflows automatically when risky drift is detected.

Enable strict mode:

```bash
dift old.csv new.csv \
  --strict-exit-codes
```

---

# Exit Code Mapping

| Exit Code | Meaning |
|---|---|
| `0` | Low-risk comparison |
| `1` | Medium-risk drift detected |
| `2` | High-risk drift detected |
| `3` | Runtime error or failed comparison |

---

# Why Strict Exit Codes Matter

Strict exit codes allow systems to automatically:

- fail CI jobs
- stop deployments
- block ETL workflows
- trigger alerts
- enforce validation gates

---

# Quiet Mode

Suppress non-error output:

```bash
dift old.csv new.csv --quiet
```

Useful for:

- automation logs
- scheduled workflows
- CI environments

---

# No-Color Mode

Disable ANSI terminal colors:

```bash
dift old.csv new.csv --no-color
```

Useful for:

- plain-text logging systems
- CI logs
- centralized observability platforms

---

# Recommended Automation Command

Recommended production automation workflow:

```bash
dift prod.csv staging.csv \
  --key customer_id \
  --strict-exit-codes \
  --quiet \
  --no-color
```

---

# Reusable Profiles

Profiles simplify recurring workflows.

Create profile:

```bash
dift profile create nightly-check \
  --old prod.csv \
  --new candidate.csv \
  --key customer_id \
  --report html
```

Run profile:

```bash
dift profile run nightly-check
```

---

# Why Profiles Matter

Profiles help standardize:

- nightly validations
- production checks
- warehouse monitoring
- recurring comparisons

---

# Scheduled Comparisons

Dift supports reusable schedule generation workflows.

Generate cron command:

```bash
dift schedule cron nightly-check
```

Example output:

```cron
0 2 * * * dift profile run nightly-check --history --strict-exit-codes
```

---

# Custom Schedule Times

Generate custom schedules:

```bash
dift schedule cron nightly-check \
  --hour 5 \
  --minute 30
```

---

# Saved Schedules

Create reusable schedules:

```bash
dift schedule create daily-check \
  --profile nightly-check \
  --cron "0 2 * * *"
```

---

# List Schedules

```bash
dift schedule list
```

---

# Run Saved Schedule

```bash
dift schedule run daily-check
```

---

# Delete Schedule

```bash
dift schedule delete daily-check
```

---

# Cron Integration

Open cron editor:

```bash
crontab -e
```

Add generated schedule:

```cron
0 2 * * * dift profile run nightly-check --history --strict-exit-codes
```

---

# Linux/macOS Workflow Example

Example nightly validation:

```cron
0 2 * * * dift profile run production-check \
  --history \
  --strict-exit-codes \
  --quiet \
  --no-color
```

---

# Windows Task Scheduler

Use generated Dift commands directly inside:

- Windows Task Scheduler
- PowerShell automation
- scheduled batch workflows

Example:

```bash
dift profile run nightly-check --history --strict-exit-codes
```

---

# GitHub Actions Integration

Example workflow:

```yaml
name: Dift Validation

on:
  push:

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install Dift
        run: pip install dift-cli

      - name: Run Validation
        run: |
          dift old.csv new.csv \
            --key customer_id \
            --strict-exit-codes \
            --quiet \
            --no-color
```

---

# Jenkins Integration

Example Jenkins pipeline step:

```groovy
stage('Validate Data') {
    steps {
        sh '''
        dift prod.csv staging.csv \
          --key customer_id \
          --strict-exit-codes
        '''
    }
}
```

---

# Airflow Integration

Dift integrates naturally into Airflow workflows.

Example:

```python
from airflow.operators.bash import BashOperator

validate_data = BashOperator(
    task_id="validate_data",
    bash_command="""
    dift old.csv new.csv \
      --key customer_id \
      --strict-exit-codes
    """
)
```

---

# Airflow Use Cases

Common Airflow workflows:

- ETL validation
- warehouse regression testing
- production dataset checks
- scheduled monitoring

---

# Prefect Integration

Example:

```python
from prefect import flow
import subprocess

@flow
def validate():
    subprocess.run(
        [
            "dift",
            "old.csv",
            "new.csv",
            "--strict-exit-codes"
        ],
        check=True,
    )
```

---

# Dagster Integration

Example:

```python
import subprocess

subprocess.run(
    [
        "dift",
        "old.csv",
        "new.csv",
        "--strict-exit-codes",
    ],
    check=True,
)
```

---

# Batch Comparison Automation

Batch workflows are ideal for:

- warehouse snapshots
- multi-table ETL validation
- large monitoring workflows

Example:

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --strict-exit-codes
```

---

# Batch HTML Reports

Example:

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --report html \
  --output-dir reports/batch
```

---

# Comparison History

Persist historical validation runs:

```bash
dift old.csv new.csv \
  --history
```

---

# Why History Tracking Matters

History tracking supports:

- trend analysis
- recurring risk visibility
- long-term monitoring
- compliance workflows

---

# History Directory

Default location:

```text
.dift/history/history.jsonl
```

---

# Custom History Location

Example:

```bash
dift old.csv new.csv \
  --history \
  --history-dir reports/history
```

---

# Environment-Aware Automation

Dift supports environment-specific configs.

Example:

```yaml
environments:
  development:
    threshold: 0.2

  production:
    threshold: 0.05
```

Run:

```bash
dift --config config.yaml --env production
```

---

# Environment Variables

Dift supports environment variable interpolation.

Example:

```yaml
old_dataset: ${OLD_DATASET}
new_dataset: ${NEW_DATASET}
```

---

# CI/CD-Friendly Configs

Configs help centralize automation behavior.

Example:

```yaml
report: json
threshold: 0.1
```

Run:

```bash
dift --config ci_config.yaml
```

---

# Machine-Readable Reporting

Recommended formats for automation:

- JSON
- CSV

Example:

```bash
dift old.csv new.csv \
  --report json \
  --output report.json
```

---

# JSON Reporting Benefits

JSON reports support:

- APIs
- observability systems
- custom dashboards
- downstream automation

---

# Progress Indicators

Dift includes lightweight progress indicators for long-running workflows.

Progress visibility includes:

- dataset loading
- warehouse queries
- report generation
- comparison execution

---

# Progress Design Goals

Progress indicators are intentionally:

- lightweight
- automation-safe
- non-intrusive
- readable

---

# Connector Automation Workflows

Automation works across:

- local datasets
- DuckDB
- PostgreSQL
- MySQL
- BigQuery
- Snowflake
- Redshift

---

# Example SQL Workflow

```bash
dift postgresql://user:password@localhost:5432/db:old \
     postgresql://user:password@localhost:5432/db:new \
     --strict-exit-codes
```

---

# Example BigQuery Workflow

```bash
dift bigquery://analytics.sales.old \
     bigquery://analytics.sales.new \
     --strict-exit-codes
```

---

# Example DuckDB Workflow

```bash
dift duckdb:///warehouse.duckdb:old \
     duckdb:///warehouse.duckdb:new \
     --strict-exit-codes
```

---

# Automation Best Practices

Recommended best practices:

- use strict exit codes
- use reusable profiles
- use quiet mode in CI
- persist history
- use JSON reporting
- standardize configs

---

# Enterprise Workflow Goals

Dift automation workflows are designed to support:

- deployment gating
- warehouse trust validation
- ML dataset regression testing
- production monitoring
- scheduled data quality enforcement

---

# Design Philosophy

The Dift automation architecture prioritizes:

- reproducibility
- CI/CD compatibility
- predictable execution
- enterprise readiness
- automation scalability

---

# Related Documentation

See also:

- configuration.md
- profiles.md
- history.md
- connectors/sql.md
- developer/architecture.md
- developer/plugin-preparation.md