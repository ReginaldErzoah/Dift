# Usage Guide

This guide explains how to use Dift across common workflows, connectors, reporting systems, and automation pipelines.

---

# Basic Command Structure

```bash
dift [OLD_DATASET] [NEW_DATASET] [OPTIONS]
```

Example:

```bash
dift old.csv new.csv --key customer_id
```

---

# Required Inputs

Dift compares:

- local files
- SQL tables
- DuckDB tables
- BigQuery tables
- warehouse datasets

Most comparisons require:

- old dataset
- new dataset
- row matching key

---

# Local File Comparisons

---

## CSV

```bash
dift old.csv new.csv --key customer_id
```

---

## Parquet

```bash
dift old.parquet new.parquet --key customer_id
```

---

## Excel

```bash
dift old.xlsx new.xlsx --key customer_id
```

---

## JSON

```bash
dift old.json new.json --key customer_id
```

---

# Drift Detection

Dift automatically detects:

- schema drift
- row-level changes
- numeric drift
- categorical drift
- outlier spikes
- null spikes
- duplicate spikes

---

# Numeric Drift Thresholds

Control sensitivity using `--threshold`.

Default:

```text
0.1
```

Example:

```bash
dift old.csv new.csv \
  --key customer_id \
  --threshold 0.2
```

---

# Reports

---

## Console Report

Default output:

```bash
dift old.csv new.csv --key customer_id
```

---

## JSON Report

```bash
dift old.csv new.csv \
  --report json \
  --output report.json
```

---

## CSV Report

```bash
dift old.csv new.csv \
  --report csv \
  --output report.csv
```

---

## Excel Report

```bash
dift old.csv new.csv \
  --report excel \
  --output report.xlsx
```

---

## HTML Report

```bash
dift old.csv new.csv \
  --report html \
  --output report.html
```

---

# HTML Templates

Customize report styling:

```bash
dift old.csv new.csv \
  --report html \
  --template enterprise \
  --output report.html
```

Available templates:

- default
- clean
- compact
- enterprise
- dark

---

# Output Directory Support

Automatically generate report filenames:

```bash
dift old.csv new.csv \
  --report html \
  --output-dir reports/
```

Generated files:

```text
reports/
└── dift_report.html
```

---

# Configuration Files

Dift supports reusable configuration files.

---

## YAML

```yaml
old_dataset: examples/old.csv
new_dataset: examples/new.csv
key: customer_id
report: html
threshold: 0.1
```

Run:

```bash
dift --config config.yaml
```

---

## TOML

```toml
old_dataset = "examples/old.csv"
new_dataset = "examples/new.csv"
key = "customer_id"
report = "json"
```

---

## JSON

```json
{
  "old_dataset": "examples/old.csv",
  "new_dataset": "examples/new.csv",
  "key": "customer_id",
  "report": "csv"
}
```

---

# Environment Configurations

Select environments dynamically:

```bash
dift --config config_env.yaml --env production
```

Useful for:

- development
- staging
- production
- CI/CD pipelines

---

# Environment Variables

Dift supports environment variable interpolation.

Example:

```yaml
old_dataset: ${OLD_DATASET}
new_dataset: ${NEW_DATASET}
```

Set variables:

```bash
export OLD_DATASET=data/old.csv
export NEW_DATASET=data/new.csv
```

Run:

```bash
dift --config config_env.yaml
```

---

# Saved Profiles

Profiles allow reusable comparison workflows.

---

## Create Profile

```bash
dift profile create nightly-check \
  --old old.csv \
  --new new.csv \
  --key customer_id \
  --report html
```

---

## Run Profile

```bash
dift profile run nightly-check
```

---

## List Profiles

```bash
dift profile list
```

---

## Show Profile

```bash
dift profile show nightly-check
```

---

## Delete Profile

```bash
dift profile delete nightly-check
```

---

# Batch Comparisons

Run multiple dataset comparisons automatically.

---

## Folder Structure

```text
data/
├── old/
└── new/
```

---

## Run Batch Comparison

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --key customer_id
```

---

## Batch Reports

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --report html \
  --output-dir reports/
```

---

# Comparison History

Save comparison history:

```bash
dift old.csv new.csv \
  --key customer_id \
  --history
```

---

## View History

```bash
dift history list
```

---

## Show History Entry

```bash
dift history show 1
```

---

## Clear History

```bash
dift history clear
```

---

# Scheduling

Generate cron workflows:

```bash
dift schedule cron nightly-check
```

Example:

```cron
0 2 * * * dift profile run nightly-check --history
```

---

# Automation-Friendly Features

---

## Strict Exit Codes

```bash
dift old.csv new.csv \
  --strict-exit-codes
```

| Exit Code | Meaning |
|---|---|
| 0 | Low risk |
| 1 | Medium risk |
| 2 | High risk |
| 3 | Runtime error |

---

## Quiet Mode

```bash
dift old.csv new.csv --quiet
```

---

## Disable Colors

```bash
dift old.csv new.csv --no-color
```

---

# Progress Indicators

Dift provides lightweight progress indicators during:

- dataset loading
- SQL extraction
- warehouse queries
- schema comparison
- drift analysis
- report generation

Useful for:

- large datasets
- warehouse comparisons
- CI/CD monitoring
- long-running workflows

---

# DuckDB Usage

Compare DuckDB tables directly:

```bash
dift duckdb:///warehouse.duckdb:customers_old \
     duckdb:///warehouse.duckdb:customers_new \
     --key customer_id
```

---

# BigQuery Usage

```bash
dift bigquery://analytics.sales.orders_old \
     bigquery://analytics.sales.orders_new \
     --key order_id
```

---

# PostgreSQL Usage

```bash
dift postgresql://user:password@localhost:5432/sales:customers_old \
     postgresql://user:password@localhost:5432/sales:customers_new \
     --key customer_id
```

---

# MySQL Usage

```bash
dift mysql+pymysql://user:password@localhost:3306/sales:orders_old \
     mysql+pymysql://user:password@localhost:3306/sales:orders_new \
     --key order_id
```

---

# Redshift Usage

```bash
dift redshift+redshift_connector://user:password@cluster.region.redshift.amazonaws.com:5439/dev:orders_old \
     redshift+redshift_connector://user:password@cluster.region.redshift.amazonaws.com:5439/dev:orders_new \
     --key order_id
```

---

# Snowflake Usage

```bash
dift snowflake://user:password@account/db/schema?warehouse=compute_wh:orders_old \
     snowflake://user:password@account/db/schema?warehouse=compute_wh:orders_new \
     --key order_id
```

---

# Common Workflows

---

## ETL Validation

```bash
dift before.csv after.csv
```

---

## ML Dataset Drift Detection

```bash
dift train_v1.csv train_v2.csv --threshold 0.1
```

---

## Production Validation

```bash
dift prod.csv staging.csv --key id
```

---

## Scheduled Validation

```bash
dift profile run nightly-check
```

---

# Configuration Priority

Dift resolves settings using:

```text
CLI Arguments > Profiles > Config Files > Defaults
```

---

# Error Handling

Dift provides actionable validation errors for:

- invalid URIs
- unsupported formats
- missing dependencies
- connector failures
- missing datasets
- invalid configuration files
- authentication issues

Example:

```text
PostgreSQL support requires psycopg2.
Install it with:
  pip install psycopg2-binary
```

---

# Next Steps

Continue with:

- Reports
- Configuration
- Thresholds
- Profiles
- Batch Comparisons
- Connectors
- Developer Architecture