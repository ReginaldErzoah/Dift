# Dift

<p align="left">
  <img src="https://raw.githubusercontent.com/ReginaldErzoah/Dift/main/assets/dift-logo.png" width="400" alt="Dift Logo">
</p>

![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-0.6.0-orange)

Dift is an open-source platform for dataset comparison, drift detection, and automated data trust validation.

It helps data teams instantly understand:

- what changed
- why it matters
- whether new data is safe to trust

Dift supports:

- local datasets
- SQL databases
- analytical warehouses
- drift analysis
- automation workflows
- historical validation
- reusable comparison systems

---

# Why Dift?

Bad data silently breaks:

- dashboards
- ETL pipelines
- analytics workflows
- ML models
- warehouse transformations
- business decisions

Dift helps teams detect risky dataset changes before they propagate into production systems.

---

# Key Features

## Dataset Comparison

- Schema comparison
- Row-level comparison
- Null analysis
- Duplicate analysis
- Risk scoring
- Drift analysis

---

## Drift Detection

### Numeric Drift

- Mean shift detection
- Standard deviation drift
- Range shift analysis
- Severity classification

### Categorical Drift

- New value detection
- Removed value detection
- Frequency shift analysis
- Severity scoring

### Outlier Detection

- IQR outlier analysis
- Outlier spike detection
- Risk integration

---

# Supported Dataset Sources

## Local Files

- CSV
- Parquet
- Excel (`.xlsx`, `.xls`)
- JSON

## Databases & Warehouses

- SQLite
- PostgreSQL
- MySQL
- DuckDB
- BigQuery
- Redshift
- Snowflake

---

# Reporting

Dift supports:

- Rich CLI reports
- JSON reports
- CSV reports
- Excel reports
- HTML reports

---

# HTML Templates

Available templates:

- default
- clean
- compact
- enterprise
- dark

Example:

```bash
dift old.csv new.csv \
  --report html \
  --template dark
```

---

# Automation Features

- Scheduled comparisons
- Batch dataset comparison
- Comparison history
- Reusable profiles
- Environment-based configs
- Automation-friendly exit codes
- Non-interactive execution

---

# Installation

## Install

```bash
pip install dift-cli
```

---

## Upgrade

```bash
pip install --upgrade dift-cli
```

---

# Optional Connector Dependencies

## SQL Support

```bash
pip install sqlalchemy
```

## PostgreSQL

```bash
pip install psycopg2-binary
```

## MySQL

```bash
pip install pymysql
```

## Redshift

```bash
pip install sqlalchemy-redshift redshift-connector
```

## Snowflake

```bash
pip install snowflake-sqlalchemy
```

## BigQuery

```bash
pip install google-cloud-bigquery db-dtypes
```

## DuckDB

```bash
pip install duckdb
```

---

# Quick Start

## Compare CSV Files

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id
```

---

## Generate JSON Report

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id \
  --report json \
  --output report.json
```

---

## Generate HTML Report

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id \
  --report html \
  --template enterprise \
  --output report.html
```

---

## Detect Numeric Drift

```bash
dift examples/old_drift.csv examples/new_drift.csv \
  --key id \
  --threshold 0.1
```

---

# Database & Warehouse Examples

## PostgreSQL

```bash
dift postgresql://user:password@localhost:5432/sales_db:customers_old \
     postgresql://user:password@localhost:5432/sales_db:customers_new \
     --key customer_id
```

---

## DuckDB

```bash
dift duckdb:///warehouse.duckdb:orders_old \
     duckdb:///warehouse.duckdb:orders_new \
     --key order_id
```

---

## BigQuery

```bash
dift bigquery://analytics.sales.orders_old \
     bigquery://analytics.sales.orders_new \
     --key order_id
```

---

# Batch Comparison

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --key id
```

---

# Scheduled Workflows

## Create Profile

```bash
dift profile create nightly-check \
  --old examples/old.csv \
  --new examples/new.csv \
  --key customer_id
```

## Run Profile

```bash
dift profile run nightly-check
```

## Generate Cron Schedule

```bash
dift schedule cron nightly-check
```

---

# Comparison History

Enable persistent history tracking:

```bash
dift examples/old.csv examples/new.csv \
  --history
```

---

# Automation-Friendly Execution

```bash
dift prod.csv staging.csv \
  --strict-exit-codes \
  --quiet \
  --no-color
```

---

# Configuration Support

Supported config formats:

- YAML
- TOML
- JSON

Run using config:

```bash
dift --config examples/config_sample.yaml
```

---

# Environment-Based Configs

```bash
dift --config examples/config_env.yaml \
  --env production
```

---

# Example Files

Most examples use files located in the project's `examples/` directory.

Example structure:

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
├── config_thresholds.yaml
├── config_env.yaml
└── warehouse.duckdb
```

---

# Documentation

Full documentation now lives in the `docs/` directory.

## Getting Started

- `docs/getting-started/installation.md`
- `docs/getting-started/quickstart.md`

## Core Guides

- `docs/configuration.md`
- `docs/reports.md`
- `docs/automation.md`
- `docs/examples.md`

## Connectors

- `docs/connectors/sql.md`
- `docs/connectors/duckdb.md`
- `docs/connectors/bigquery.md`

## Developer Documentation

- `docs/developer/architecture.md`
- `docs/developer/plugin-preparation.md`
- `docs/developer/reader-registry.md`
- `docs/developer/testing.md`

## Release Notes

- `docs/releases/index.md`

---

# Project Structure

```text
dift/
├── cli.py
├── core/
├── io/
│   ├── readers.py
│   ├── registry.py
│   ├── sql_reader.py
│   ├── duckdb_reader.py
│   ├── bigquery_reader.py
│   └── base_reader.py
├── reports/
├── profiles.py
├── schedules.py
├── history.py
└── utils/

docs/
tests/
examples/
```

---

# Developer Features

- Connector registry architecture
- Shared reader interfaces
- Plugin preparation architecture
- Modular connector system
- Extensible reporting system
- Warehouse-ready workflows

---

# Run Tests

```bash
pytest
```

---

# Linting

```bash
ruff check .
```

---

# Type Checking

```bash
mypy dift
```

---

# Roadmap

Upcoming areas of focus include:

- streaming comparisons
- distributed execution
- MongoDB support
- ML feature drift analysis
- observability dashboards
- alerting workflows
- native Airflow integration
- plugin ecosystem
- Python SDK
- Web UI dashboard

See:

```text
docs/roadmap.md
```

---

# Contributing

Contributions are welcome.

See:

```text
CONTRIBUTING.md
```

Ways to contribute:

- fix bugs
- improve docs
- improve testing
- improve performance
- add connectors
- improve reporting
- improve automation workflows

---

# License

MIT License

---

# Vision

Dift aims to become the open-source standard for:

- dataset regression testing
- data drift monitoring
- ML dataset validation
- warehouse trust validation
- automated data quality enforcement
- data deployment validation
- dataset observability