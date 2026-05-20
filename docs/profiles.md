# Profiles

Dift supports reusable comparison profiles for automating recurring dataset validation workflows.

Profiles help teams:

- avoid repetitive CLI commands
- standardize comparisons
- automate recurring checks
- simplify scheduled workflows
- reuse report configurations
- build production validation pipelines

---

# What Are Profiles?

A profile stores comparison settings such as:

- datasets
- keys
- thresholds
- report formats
- output locations
- automation options

Instead of repeatedly typing long CLI commands, you can reuse a saved profile.

---

# Create a Profile

Use `profile create` to save a reusable workflow.

---

## Example

```bash
dift profile create nightly-check \
  --old examples/old.csv \
  --new examples/new.csv \
  --key customer_id \
  --report html \
  --threshold 0.1
```

This creates a reusable profile named:

```text
nightly-check
```

---

# Run a Profile

Execute a saved profile:

```bash
dift profile run nightly-check
```

Dift automatically loads all saved settings.

---

# List Profiles

View all saved profiles:

```bash
dift profile list
```

Example output:

```text
- nightly-check
- production-validation
- warehouse-monitor
```

---

# Show Profile Details

Inspect a saved profile:

```bash
dift profile show nightly-check
```

Example output:

```json
{
  "old_dataset": "examples/old.csv",
  "new_dataset": "examples/new.csv",
  "key": "customer_id",
  "threshold": 0.1,
  "report": "html"
}
```

---

# Delete a Profile

Remove a saved profile:

```bash
dift profile delete nightly-check
```

---

# Common Profile Fields

Profiles can store:

| Field | Description |
|---|---|
| old_dataset | Original dataset |
| new_dataset | New dataset |
| key | Row matching key |
| threshold | Numeric drift threshold |
| report | Report format |
| output | Report output path |
| output_dir | Output directory |
| template | HTML template |
| history | Enable history tracking |
| history_dir | History directory |
| strict_exit_codes | Automation-friendly exit codes |
| quiet | Suppress non-error output |
| no_color | Disable terminal colors |

---

# Example HTML Reporting Profile

```bash
dift profile create executive-report \
  --old prod.csv \
  --new staging.csv \
  --key customer_id \
  --report html \
  --template enterprise \
  --output reports/executive.html
```

Run:

```bash
dift profile run executive-report
```

---

# Example CI/CD Profile

```bash
dift profile create ci-validation \
  --old prod.csv \
  --new candidate.csv \
  --key id \
  --report json \
  --strict-exit-codes \
  --quiet
```

Useful for:

- GitHub Actions
- Jenkins
- Airflow
- Prefect
- Dagster
- cron workflows

---

# Example Warehouse Profile

```bash
dift profile create warehouse-check \
  --old postgresql://user:password@localhost:5432/sales:orders_old \
  --new postgresql://user:password@localhost:5432/sales:orders_new \
  --key order_id \
  --report html
```

Run:

```bash
dift profile run warehouse-check
```

---

# DuckDB Profile Example

```bash
dift profile create duckdb-monitor \
  --old duckdb:///warehouse.duckdb:customers_old \
  --new duckdb:///warehouse.duckdb:customers_new \
  --key customer_id
```

---

# BigQuery Profile Example

```bash
dift profile create bigquery-monitor \
  --old bigquery://analytics.sales.orders_old \
  --new bigquery://analytics.sales.orders_new \
  --key order_id
```

---

# Profiles and History

Profiles work seamlessly with comparison history.

---

## Example

```bash
dift profile create monitored-check \
  --old old.csv \
  --new new.csv \
  --key customer_id \
  --history
```

Run:

```bash
dift profile run monitored-check
```

---

# Profiles and Scheduling

Profiles integrate directly with scheduled workflows.

---

## Generate Cron Schedule

```bash
dift schedule cron nightly-check
```

Example output:

```cron
0 2 * * * dift profile run nightly-check --history --strict-exit-codes
```

---

# Profiles and Batch Workflows

Profiles can standardize recurring batch validation workflows.

Useful for:

- ETL pipelines
- warehouse monitoring
- multi-table comparisons
- scheduled audits

---

# Configuration Priority

Profiles participate in Dift’s configuration hierarchy.

Priority order:

```text
CLI Arguments > Profiles > Config Files > Defaults
```

This means:

- CLI options override profiles
- profiles override config files
- configs override defaults

---

# CLI Override Example

```bash
dift profile run nightly-check --report json
```

This temporarily overrides the saved report format.

---

# Profiles and Thresholds

Profiles can store:

- global thresholds
- categorical thresholds
- outlier thresholds
- reusable validation policies

---

# Example Threshold Workflow

```bash
dift profile create strict-monitor \
  --old prod.csv \
  --new candidate.csv \
  --threshold 0.03
```

Useful for:

- financial data
- ML feature monitoring
- regulated environments

---

# Profiles and Reports

Profiles simplify report generation.

---

## Example

```bash
dift profile create reporting-workflow \
  --report html \
  --template dark \
  --output reports/nightly.html
```

---

# Profiles and Automation

Profiles are ideal for:

- CI/CD pipelines
- scheduled validation
- cron jobs
- recurring ETL checks
- warehouse monitoring
- historical drift tracking

---

# Example GitHub Actions Workflow

```bash
dift profile run ci-validation
```

---

# Example Cron Workflow

```cron
0 2 * * * dift profile run nightly-check
```

---

# Profile Storage

Profiles are stored locally by Dift.

This enables:

- reusable workflows
- lightweight automation
- local development workflows
- environment-specific validation

---

# Progress Indicators

Profile execution supports progress indicators for:

- dataset loading
- warehouse extraction
- comparison execution
- report generation

Useful for large datasets and scheduled workflows.

---

# Validation Errors

Dift provides helpful profile validation messages.

Examples:

```text
Error: Profile 'nightly-check' does not exist
```

```text
Error: Invalid report template 'modern'
```

---

# Best Practices

Recommended practices:

- use descriptive profile names
- separate production/staging workflows
- combine profiles with schedules
- enable strict exit codes in CI/CD
- version-control config-based workflows
- standardize thresholds across teams

---

# Example Workflow Patterns

---

## Nightly Production Validation

```bash
dift profile create nightly-prod \
  --old prod.csv \
  --new candidate.csv \
  --report html \
  --history
```

---

## ML Drift Monitoring

```bash
dift profile create ml-monitor \
  --threshold 0.03
```

---

## Warehouse Governance

```bash
dift profile create warehouse-audit \
  --report json \
  --strict-exit-codes
```

---

# Next Steps

Continue with:

- Batch Comparisons
- History
- Scheduling
- Automation
- Reports
- Connectors
- Developer Documentation