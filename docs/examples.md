# Examples

This document contains practical examples for using Dift across local datasets, databases, warehouses, automation workflows, reporting, scheduling, and validation pipelines.

Examples are organized by workflow category.

---

# Basic Dataset Comparison

Compare two CSV datasets:

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id
```

---

# Compare Parquet Files

```bash
dift examples/old.parquet examples/new.parquet \
  --key customer_id
```

---

# Compare Excel Files

```bash
dift examples/old.xlsx examples/new.xlsx \
  --key customer_id
```

---

# Compare JSON Files

```bash
dift examples/old.json examples/new.json \
  --key customer_id
```

---

# Numeric Drift Detection

Detect numeric drift using thresholds:

```bash
dift examples/old_drift.csv examples/new_drift.csv \
  --key id \
  --threshold 0.1
```

---

# Generate JSON Report

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id \
  --report json \
  --output report.json
```

---

# Generate CSV Report

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id \
  --report csv \
  --output report.csv
```

---

# Generate Excel Report

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id \
  --report excel \
  --output report.xlsx
```

---

# Generate HTML Report

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id \
  --report html \
  --output report.html
```

---

# Use HTML Templates

Generate report using a template:

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id \
  --report html \
  --template dark \
  --output report.html
```

---

# Available HTML Templates

Supported templates:

- default
- clean
- compact
- enterprise
- dark

---

# Save Reports to Output Directory

```bash
dift examples/old.csv examples/new.csv \
  --report json \
  --output-dir reports/
```

Generated filenames:

```text
dift_report.json
dift_report.csv
dift_report.xlsx
dift_report.html
```

---

# Use YAML Config File

```bash
dift --config examples/config_sample.yaml
```

---

# Example YAML Config

```yaml
old_dataset: examples/old.csv
new_dataset: examples/new.csv
key: customer_id
threshold: 0.1
report: html
```

---

# Use TOML Config

```bash
dift --config examples/config_sample.toml
```

---

# Example TOML Config

```toml
old_dataset = "examples/old.csv"
new_dataset = "examples/new.csv"
key = "customer_id"
report = "json"
```

---

# Use JSON Config

```bash
dift --config examples/config_sample.json
```

---

# Example JSON Config

```json
{
  "old_dataset": "examples/old.csv",
  "new_dataset": "examples/new.csv",
  "key": "customer_id",
  "report": "csv"
}
```

---

# Dataset Paths Inside Configs

```bash
dift --config examples/config_with_datasets.yaml
```

---

# CLI Override Example

```bash
dift examples/override_old.csv examples/override_new.csv \
  --config examples/config_sample.yaml \
  --report json
```

CLI arguments override config values.

---

# Threshold Config Example

```yaml
thresholds:
  numeric: 0.1
  categorical: 0.2
  outlier: 0.15
```

---

# Column-Level Threshold Override

```yaml
thresholds:
  columns:
    revenue:
      numeric: 0.05
      outlier: 0.1
```

---

# Use Threshold Config

```bash
dift --config examples/config_thresholds.yaml
```

---

# Environment-Based Configs

Run environment-specific workflow:

```bash
dift --config examples/config_env.yaml \
  --env production
```

---

# Example Environment Config

```yaml
environments:
  development:
    threshold: 0.2

  production:
    threshold: 0.05
```

---

# Environment Variable Interpolation

Example config:

```yaml
old_dataset: ${OLD_DATASET}
new_dataset: ${NEW_DATASET}
```

Set variables:

```bash
export OLD_DATASET=examples/old.csv
export NEW_DATASET=examples/new.csv
```

---

# Create Saved Profile

```bash
dift profile create nightly-check \
  --old examples/old.csv \
  --new examples/new.csv \
  --key customer_id \
  --report html
```

---

# Run Saved Profile

```bash
dift profile run nightly-check
```

---

# List Profiles

```bash
dift profile list
```

---

# Show Profile Details

```bash
dift profile show nightly-check
```

---

# Delete Profile

```bash
dift profile delete nightly-check
```

---

# Generate Cron Schedule

```bash
dift schedule cron nightly-check
```

Example output:

```cron
0 2 * * * dift profile run nightly-check --history --strict-exit-codes
```

---

# Create Saved Schedule

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

# Run Schedule

```bash
dift schedule run daily-check
```

---

# Delete Schedule

```bash
dift schedule delete daily-check
```

---

# Batch Dataset Comparison

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --key id
```

---

# Batch HTML Reports

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --report html \
  --output-dir reports/batch
```

---

# Continue On Error

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --continue-on-error
```

---

# Stop On Error

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --stop-on-error
```

---

# Save Comparison History

```bash
dift examples/old.csv examples/new.csv \
  --history
```

---

# Custom History Directory

```bash
dift examples/old.csv examples/new.csv \
  --history \
  --history-dir reports/history
```

---

# List Comparison History

```bash
dift history list
```

---

# Show History Record

```bash
dift history show 1
```

---

# Clear History

```bash
dift history clear
```

---

# Strict Exit Codes

```bash
dift prod.csv staging.csv \
  --strict-exit-codes
```

---

# Quiet Mode

```bash
dift old.csv new.csv \
  --quiet
```

---

# Disable Colored Output

```bash
dift old.csv new.csv \
  --no-color
```

---

# Full Automation Workflow

```bash
dift prod.csv staging.csv \
  --key customer_id \
  --strict-exit-codes \
  --quiet \
  --no-color
```

---

# DuckDB Comparison

```bash
dift duckdb:///examples/warehouse.duckdb:customers_old \
     duckdb:///examples/warehouse.duckdb:customers_new \
     --key customer_id
```

---

# DuckDB URI Format

```text
duckdb:///path/to/database.duckdb:table_name
```

---

# SQLite Comparison

```bash
dift sqlite:///examples/data.db:customers_old \
     sqlite:///examples/data.db:customers_new \
     --key customer_id
```

---

# PostgreSQL Comparison

```bash
dift postgresql://user:password@localhost:5432/sales_db:customers_old \
     postgresql://user:password@localhost:5432/sales_db:customers_new \
     --key customer_id
```

---

# PostgreSQL Psycopg Example

```bash
dift postgresql+psycopg://user:password@localhost:5432/sales_db:customers_old \
     postgresql+psycopg://user:password@localhost:5432/sales_db:customers_new \
     --key customer_id
```

---

# MySQL Comparison

```bash
dift mysql+pymysql://user:password@localhost:3306/sales_db:customers_old \
     dift mysql+pymysql://user:password@localhost:3306/sales_db:customers_new \
     --key customer_id
```

---

# Redshift Comparison

```bash
dift redshift+redshift_connector://user:password@cluster.region.redshift.amazonaws.com:5439/dev:orders_old \
     redshift+redshift_connector://user:password@cluster.region.redshift.amazonaws.com:5439/dev:orders_new \
     --key order_id
```

---

# Snowflake Comparison

```bash
dift snowflake://user:password@account/db/schema?warehouse=compute_wh:orders_old \
     snowflake://user:password@account/db/schema?warehouse=compute_wh:orders_new \
     --key order_id
```

---

# BigQuery Comparison

```bash
dift bigquery://analytics.sales.orders_old \
     bigquery://analytics.sales.orders_new \
     --key order_id
```

---

# Install SQL Support

```bash
pip install sqlalchemy
```

---

# Install PostgreSQL Driver

```bash
pip install psycopg2-binary
```

---

# Install MySQL Driver

```bash
pip install pymysql
```

---

# Install Redshift Dependencies

```bash
pip install sqlalchemy-redshift redshift-connector
```

---

# Install Snowflake Support

```bash
pip install snowflake-sqlalchemy
```

---

# Install BigQuery Support

```bash
pip install google-cloud-bigquery db-dtypes
```

---

# Install DuckDB Support

```bash
pip install duckdb
```

---

# GitHub Actions Example

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
            --strict-exit-codes \
            --quiet \
            --no-color
```

---

# Airflow Example

```python
from airflow.operators.bash import BashOperator

validate = BashOperator(
    task_id="validate_data",
    bash_command="""
    dift old.csv new.csv \
      --strict-exit-codes
    """
)
```

---

# ETL Validation Example

```bash
dift before.csv after.csv
```

---

# ML Drift Monitoring Example

```bash
dift train_v1.csv train_v2.csv \
  --threshold 0.1
```

---

# Production vs Staging Example

```bash
dift prod.csv staging.csv \
  --key id
```

---

# Multi-Table Validation Example

```bash
dift batch \
  --old-dir warehouse_snapshot_1 \
  --new-dir warehouse_snapshot_2 \
  --report html
```

---

# Historical Drift Monitoring Example

```bash
dift prod.csv staging.csv \
  --history
```

---

# Example Console Output

```text
╭─────────────────────────╮
│ Dift Dataset Comparison │
│ Risk Level: MEDIUM      │
╰─────────────────────────╯

Warnings

Numeric drift:
'revenue'
mean shift 900.00%
(high, threshold 0.1)

Outlier spike:
'revenue' increased by 100.00%
(high)

Categorical shift:
'segment' max frequency shift 60.00%
(high)
```

---

# Example Directory Structure

Most examples in this documentation use datasets and configuration files located in the project's `examples/` directory.

```text
examples/
├── old.csv
├── new.csv
├── old.parquet
├── new.parquet
├── old.xlsx
├── new.xlsx
├── old.json
├── new.json
├── old_drift.csv
├── new_drift.csv
├── config_sample.yaml
├── config_sample.toml
├── config_sample.json
├── config_thresholds.yaml
├── config_env.yaml
└── warehouse.duckdb
```

---

# Related Documentation

See also:

- configuration.md
- automation.md
- profiles.md
- history.md
- connectors/sql.md
- reports.md