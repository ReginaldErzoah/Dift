# Scheduled Comparisons

Dift supports reusable scheduled comparison workflows for automation, monitoring, CI/CD pipelines, and recurring data validation.

Scheduling helps teams:

- run nightly drift checks
- automate production validations
- monitor warehouse stability
- build recurring governance workflows
- integrate with cron jobs
- create CI/CD monitoring pipelines

---

# Why Scheduling Matters

Modern data systems change continuously.

Without scheduling, teams often:

- detect drift too late
- miss silent regressions
- discover broken pipelines manually
- lose visibility into data quality trends

Dift scheduling enables proactive monitoring.

---

# Scheduling Workflow Overview

Dift scheduling is built around reusable profiles.

Typical workflow:

1. Create a profile
2. Create a schedule
3. Run automatically
4. Track history
5. Trigger alerts or pipeline failures

---

# Create a Comparison Profile

First create a reusable comparison profile.

---

## Example

```bash
dift profile create nightly-check \
  --old examples/old.csv \
  --new examples/new.csv \
  --key customer_id \
  --report html \
  --output reports/nightly.html
```

This saves comparison settings for reuse.

---

# Generate a Cron Schedule

Generate a cron-ready automation command.

---

## Example

```bash
dift schedule cron nightly-check
```

---

# Example Output

```cron
0 2 * * * dift profile run nightly-check --history --strict-exit-codes
```

Meaning:

- run daily
- at 2:00 AM
- save comparison history
- fail pipelines on risky drift

---

# Custom Schedule Times

Customize cron generation.

---

## Example

```bash
dift schedule cron nightly-check \
  --hour 5 \
  --minute 30
```

---

# Example Output

```cron
30 5 * * * dift profile run nightly-check --history --strict-exit-codes
```

Runs daily at 5:30 AM.

---

# Create a Saved Schedule

Store reusable schedules.

---

## Example

```bash
dift schedule create daily-check \
  --profile nightly-check \
  --cron "0 2 * * *"
```

---

# List Saved Schedules

```bash
dift schedule list
```

---

# Example Output

```text
- daily-check
- warehouse-monitor
- ml-validation
```

---

# Show Schedule Details

Inspect a saved schedule.

---

## Example

```bash
dift schedule show daily-check
```

---

# Example Output

```json
{
  "profile": "nightly-check",
  "cron": "0 2 * * *"
}
```

---

# Run a Schedule Manually

Trigger a saved schedule immediately.

---

## Example

```bash
dift schedule run daily-check
```

Useful for:

- testing workflows
- manual validation
- debugging automation

---

# Delete a Schedule

```bash
dift schedule delete daily-check
```

---

# Linux/macOS Cron Integration

Open your crontab:

```bash
crontab -e
```

Add:

```cron
0 2 * * * dift profile run nightly-check --history --strict-exit-codes
```

---

# Windows Task Scheduler

Use the generated command:

```bash
dift profile run nightly-check --history --strict-exit-codes
```

inside:

- Windows Task Scheduler
- PowerShell automation
- enterprise schedulers

---

# GitHub Actions Integration

Example workflow step:

```yaml
- name: Run Dift validation
  run: |
    dift profile run nightly-check \
      --history \
      --strict-exit-codes
```

Useful for:

- pull request validation
- production monitoring
- deployment gates

---

# Jenkins Integration

```bash
dift profile run nightly-check \
  --history \
  --strict-exit-codes
```

Useful for:

- nightly jobs
- ETL validation
- warehouse monitoring

---

# Airflow Integration

Example Airflow task:

```python
BashOperator(
    task_id="dift_validation",
    bash_command="dift profile run nightly-check --history"
)
```

Useful for:

- data pipelines
- orchestration workflows
- scheduled monitoring

---

# Prefect Integration

```python
subprocess.run(
    ["dift", "profile", "run", "nightly-check"]
)
```

---

# Dagster Integration

```python
os.system(
    "dift profile run nightly-check"
)
```

---

# Scheduled Batch Workflows

Scheduling works with batch comparisons.

---

## Example

```bash
dift batch \
  --old-dir warehouse/day1 \
  --new-dir warehouse/day2 \
  --history
```

Useful for:

- warehouse snapshots
- multi-table monitoring
- regression testing

---

# Scheduled Warehouse Validation

Example Snowflake monitoring:

```bash
dift snowflake://... \
     snowflake://... \
     --history
```

Useful for:

- enterprise monitoring
- warehouse governance
- production validation

---

# Scheduled BigQuery Validation

```bash
dift bigquery://project.dataset.table_old \
     bigquery://project.dataset.table_new \
     --history
```

---

# Scheduled ML Monitoring

```bash
dift train_v1.csv train_v2.csv \
  --threshold 0.03 \
  --history
```

Useful for:

- feature drift monitoring
- retraining validation
- data governance

---

# Strict Exit Codes

Use risk-based automation behavior.

---

## Example

```bash
dift profile run nightly-check \
  --strict-exit-codes
```

---

# Exit Code Mapping

| Exit Code | Meaning |
|---|---|
| 0 | Low risk |
| 1 | Medium risk |
| 2 | High risk |
| 3 | Runtime error |

Useful for:

- CI/CD enforcement
- pipeline protection
- deployment validation

---

# Quiet Mode

Suppress non-error output.

---

## Example

```bash
dift profile run nightly-check \
  --quiet
```

Useful for:

- cron jobs
- CI systems
- automated monitoring

---

# Disable Colored Output

```bash
dift profile run nightly-check \
  --no-color
```

Useful for:

- plain-text logs
- CI/CD systems
- monitoring tools

---

# Progress Indicators

Dift provides lightweight progress feedback during scheduled workflows.

Examples:

- dataset loading
- warehouse extraction
- comparison execution
- report generation

Useful for:

- long-running jobs
- enterprise workflows
- warehouse comparisons

---

# Example Production Workflow

```bash
dift profile run production-validation \
  --history \
  --strict-exit-codes \
  --quiet
```

Useful for:

- nightly monitoring
- governance enforcement
- automated validation

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

# Validation Errors

Dift provides actionable scheduling errors.

Examples:

```text
Error: Schedule not found
```

```text
Error: Invalid cron expression
```

```text
Error: Profile does not exist
```

---

# Best Practices

Recommended practices:

- use reusable profiles
- enable history tracking
- combine schedules with strict exit codes
- use quiet mode in CI/CD
- separate schedules by environment
- archive reports for audits
- automate nightly validation

---

# Common Use Cases

---

## Nightly Drift Monitoring

```bash
dift schedule create nightly-check
```

---

## Production Warehouse Validation

```bash
dift schedule create warehouse-monitor
```

---

## ML Feature Drift Monitoring

```bash
dift schedule create ml-validation
```

---

## ETL Regression Testing

```bash
dift schedule create etl-check
```

---

# Future Roadmap

Planned future scheduling capabilities:

- native scheduler daemon
- alerting integrations
- Slack notifications
- email alerts
- webhook support
- enterprise orchestration plugins

---

# Next Steps

Continue with:

- Reports
- Connectors
- Plugin Architecture
- Developer Documentation
- Contributing