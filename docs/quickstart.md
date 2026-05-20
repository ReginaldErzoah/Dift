# Quick Start

This guide helps you get started with Dift quickly.

You will learn how to:

- compare datasets
- detect drift
- generate reports
- use configuration files
- run batch comparisons
- automate workflows

---

# Your First Comparison

Compare two CSV files:

```bash
dift examples/old.csv examples/new.csv --key customer_id
```

This command compares:

- schema changes
- row changes
- null spikes
- duplicate spikes
- drift patterns
- outlier changes

---

# Understanding the `--key`

The `--key` option defines the column used to match rows across datasets.

Example:

```bash
--key customer_id
```

Typical keys:

- customer_id
- order_id
- transaction_id
- product_id

---

# Example Output

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

# Generate Reports

---

## JSON Report

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id \
  --report json \
  --output report.json
```

---

## CSV Report

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id \
  --report csv \
  --output report.csv
```

---

## Excel Report

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id \
  --report excel \
  --output report.xlsx
```

---

## HTML Report

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id \
  --report html \
  --output report.html
```

---

# HTML Templates

Customize HTML report appearance:

```bash
dift examples/old.csv examples/new.csv \
  --report html \
  --template dark \
  --output report.html
```

Available templates:

- default
- clean
- compact
- enterprise
- dark

---

# Drift Thresholds

Control drift sensitivity using `--threshold`.

Default threshold:

```text
0.1
```

Example:

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id \
  --threshold 0.2
```

Lower values detect smaller changes.

Higher values reduce sensitivity.

---

# Output Directory Support

Save reports into a directory with auto-generated filenames:

```bash
dift examples/old.csv examples/new.csv \
  --report html \
  --output-dir reports/
```

Generated filenames include:

- dift_report.json
- dift_report.csv
- dift_report.xlsx
- dift_report.html

---

# Using Configuration Files

Run comparisons using reusable configuration files.

---

## YAML Example

```yaml
old_dataset: examples/old.csv
new_dataset: examples/new.csv
key: customer_id
threshold: 0.1
report: html
```

Run:

```bash
dift --config examples/config_sample.yaml
```

---

# Environment-Based Configs

Select reusable environments:

```bash
dift --config examples/config_env.yaml --env production
```

Useful for:

- development
- staging
- production
- CI/CD workflows

---

# Saved Profiles

Create reusable comparison workflows.

---

## Create Profile

```bash
dift profile create nightly-check \
  --old examples/old.csv \
  --new examples/new.csv \
  --key customer_id \
  --report html
```

---

## Run Profile

```bash
dift profile run nightly-check
```

---

# Batch Comparisons

Compare multiple dataset pairs automatically.

---

## Example

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --key customer_id
```

Useful for:

- ETL validation
- warehouse monitoring
- scheduled quality checks
- multi-table validation

---

# Comparison History

Save historical comparison results:

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id \
  --history
```

View history:

```bash
dift history list
```

---

# Automation-Friendly Mode

Use Dift inside:

- CI/CD pipelines
- Airflow
- Jenkins
- Prefect
- Dagster
- cron jobs

---

## Strict Exit Codes

```bash
dift prod.csv staging.csv \
  --key customer_id \
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

# DuckDB Example

```bash
dift duckdb:///warehouse.duckdb:customers_old \
     duckdb:///warehouse.duckdb:customers_new \
     --key customer_id
```

---

# BigQuery Example

```bash
dift bigquery://analytics.sales.orders_old \
     bigquery://analytics.sales.orders_new \
     --key order_id
```

---

# PostgreSQL Example

```bash
dift postgresql://user:password@localhost:5432/sales:customers_old \
     postgresql://user:password@localhost:5432/sales:customers_new \
     --key customer_id
```

---

# MySQL Example

```bash
dift mysql+pymysql://user:password@localhost:3306/sales:orders_old \
     mysql+pymysql://user:password@localhost:3306/sales:orders_new \
     --key order_id
```

---

# Snowflake Example

```bash
dift snowflake://user:password@account/db/schema?warehouse=compute_wh:orders_old \
     snowflake://user:password@account/db/schema?warehouse=compute_wh:orders_new \
     --key order_id
```

---

# Redshift Example

```bash
dift redshift+redshift_connector://user:password@cluster.region.redshift.amazonaws.com:5439/dev:orders_old \
     redshift+redshift_connector://user:password@cluster.region.redshift.amazonaws.com:5439/dev:orders_new \
     --key order_id
```

---

# Common Use Cases

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

## Production vs Staging Validation

```bash
dift prod.csv staging.csv --key id
```

---

## Historical Monitoring

```bash
dift prod.csv staging.csv \
  --key customer_id \
  --history
```

---

# Next Steps

Continue with:

- Usage Guide
- Reports
- Configuration
- Thresholds
- Automation
- Connectors
- Developer Architecture