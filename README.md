# Dift

<p align="left">
  <img src="https://raw.githubusercontent.com/ReginaldErzoah/Dift/main/assets/dift-logo.png" width="400" alt="Dift Logo">
</p>

![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-0.5.0-orange)

Dift is an open-source CLI platform for dataset comparison, drift detection, and data trust validation.

It helps data teams instantly understand:

* what changed
* why it matters
* whether the new data is safe to trust

---

# What's New in v0.5.0

Dift v0.5.0 introduces advanced drift analysis, outlier detection, reusable configurations, saved comparison profiles, improved reporting, and stronger dataset risk analysis.

## New Features

* Numeric drift detection
* Advanced categorical drift analysis
* Outlier detection using IQR analysis
* Outlier severity classification
* Outlier risk scoring
* Frequency distribution shift detection
* Numeric drift reporting across all report formats
* Improved Excel reporting
* Improved HTML reporting
* Better CSV drift summaries
* Enhanced weighted risk scoring
* Improved warning system
* Better drift visibility in console reports

---

## Why Dift?

Bad data breaks:

* dashboards
* reports
* ETL pipelines
* analytics workflows
* ML models
* business decisions

Dift helps teams catch risky data changes before they cause damage.

---

# Features (v0.5.0)

## Supported Formats

* CSV
* Parquet
* Excel (`.xlsx`, `.xls`)
* JSON

---

## Drift Detection

### Numeric Drift

* Mean shift detection
* Standard deviation drift
* Range shift detection
* Configurable drift thresholds
* Severity classification

### Categorical Drift

* New categorical value detection
* Removed categorical value detection
* Frequency distribution shifts
* Severity classification

### Outlier Detection

* IQR outlier detection
* Outlier spike detection
* Outlier percentage tracking
* Risk integration

---

# Output Options

* Rich CLI report
* JSON report
* CSV summary report
* Excel workbook report
* HTML dashboard-style report

---

## HTML Templates

Customize your HTML reports:

```bash
dift old.csv new.csv --report html --template clean
```

Available templates:

* `default`
* `clean`
* `compact`
* `enterprise`
* `dark`

---

## Numeric Drift Thresholds

Control drift sensitivity using `--threshold`.

Default threshold:

```bash
0.1
```

Example:

```bash
dift old.csv new.csv --key id --threshold 0.2
```

This helps detect silent numeric drift in:

* ML datasets
* ETL pipelines
* analytics tables
* production data feeds

---

## Output Directory Support

Save reports to a directory without specifying filenames:

```bash
dift old.csv new.csv --report json --output-dir reports/
```

Auto-generated filenames:

* `dift_report.json`
* `dift_report.csv`
* `dift_report.xlsx`
* `dift_report.html`

---

# Configuration System

Dift supports reusable configuration files for cleaner and reproducible workflows.

```bash
dift old.csv new.csv --config examples/config_sample.yaml
```

## Supported Formats

* YAML (`.yaml`, `.yml`)
* TOML (`.toml`)
* JSON (`.json`)

## Example YAML Config

```yaml
old_dataset: "example/old.csv"
new_dataset: "examples/new.csv"
key: "customer_id"
threshold: 0.05
report: "html"
```

## Example TOML Config

```toml
old_dataset = "examples/old.csv"
new_dataset = "examples/new.csv"
key = "customer_id"
threshold = 0.1
report = "json"
```

## Example JSON Config

```json
{
  "old_dataset": "examples/old.csv",
  "new_dataset": "examples/new.csv",
  "key": "customer_id",
  "threshold": 0.2,
  "report": "csv"
}
```
---

## Dataset Paths in Config Files

Dift can also load dataset paths directly from config files.

This means you can run a comparison without typing the old and new dataset paths in the terminal every time.

```bash
dift --config examples/config_with_datasets.yaml
```

### YAML Example

```yaml
old_dataset: examples/old.csv
new_dataset: examples/new.csv
key: customer_id
threshold: 0.2
report: html
output: reports/config_report.html
```

### CLI Override Example

CLI arguments still override config values.

```bash
dift examples/old_drift.csv examples/new_drift.csv \
  --config examples/config_with_datasets.yaml \
  --report json \
  --output override_report.json
```

In this case, Dift uses:

* datasets from the CLI
* report/output from the CLI
* remaining values from the config file


---

# Reusable Threshold Configurations

Dift supports reusable threshold policies for advanced drift detection workflows.

Threshold configurations help teams:

* standardize drift sensitivity
* customize validation rules
* apply column-specific policies
* reuse validation settings across environments

---

## Global Threshold Configuration

```yaml
thresholds:
  numeric: 0.1
  categorical: 0.2
  outlier: 0.15
```

---

## Column-Level Threshold Overrides

```yaml
thresholds:
  numeric: 0.1
  categorical: 0.2
  outlier: 0.15

  columns:
    revenue:
      numeric: 0.05
      outlier: 0.1

    segment:
      categorical: 0.3
```

---

## Full Threshold Config Example

```yaml
old_dataset: examples/old.csv
new_dataset: examples/new.csv

key: customer_id
report: html
output: reports/threshold_report.html

thresholds:
  numeric: 0.1
  categorical: 0.2
  outlier: 0.15

  columns:
    revenue:
      numeric: 0.05
      outlier: 0.1

    status:
      categorical: 0.3
```

---

## Run Using Threshold Configs

```bash
dift --config examples/config_thresholds.yaml
```

---

## CLI Threshold Override

CLI thresholds still override global numeric thresholds for backward compatibility.

```bash
dift --config examples/config_thresholds.yaml --threshold 0.5
```

This overrides:

```yaml
thresholds:
  numeric: 0.1
```

But preserves:

* categorical thresholds
* outlier thresholds
* column-level overrides

---

## Supported Threshold Types

| Threshold Type | Purpose                   |
| -------------- | ------------------------- |
| numeric        | Numeric drift detection   |
| categorical    | Frequency shift detection |
| outlier        | Outlier spike detection   |
| columns        | Column-specific overrides |

---

## Example Use Cases

### Sensitive Revenue Monitoring

```yaml
columns:
  revenue:
    numeric: 0.02
```

Detect even small revenue drift changes.

---

### Relaxed Categorical Drift

```yaml
columns:
  segment:
    categorical: 0.4
```

Reduce noise for highly variable categorical fields.

---

### Strict Outlier Detection

```yaml
columns:
  transactions:
    outlier: 0.05
```

Catch abnormal spikes aggressively.

---

# Environment-Based Configurations

Dift supports reusable environment-specific configurations for development, staging, and production workflows.

This helps teams maintain different comparison settings across environments while keeping configs clean and reusable.

---

## Select an Environment

```bash
dift --config examples/config_env.yaml --env development
```

---

## Example Environment Config

### YAML

```yaml
key: customer_id
report: html
output: reports/env_report.html

environments:
  development:
    old_dataset: examples/old.csv
    new_dataset: examples/new.csv
    threshold: 0.2

  staging:
    old_dataset: staging_old.csv
    new_dataset: staging_new.csv
    threshold: 0.15

  production:
    old_dataset: ${OLD_DATASET}
    new_dataset: ${NEW_DATASET}
    threshold: 0.1
```

---

## Environment Variable Support

Dift supports environment variable interpolation inside config files.

Example:

```yaml
old_dataset: ${OLD_DATASET}
new_dataset: ${NEW_DATASET}
```

Set variables before running Dift.

### Git Bash / Linux / Mac

```bash
export OLD_DATASET=examples/old.csv
export NEW_DATASET=examples/new.csv
```

### PowerShell

```powershell
$env:OLD_DATASET="examples/old.csv"
$env:NEW_DATASET="examples/new.csv"
```

Then run:

```bash
dift --config examples/config_env.yaml --env production
```

---

## Missing Environment Variables

If a required environment variable is missing, Dift shows a helpful error.

Example:

```text
Error: Missing environment variable 'OLD_DATASET'
```

---

## Environment Workflow Benefits

Environment configs help support:

* development workflows
* staging validation
* production deployment checks
* CI/CD pipelines
* secret management preparation
* reusable automation workflows

---

# Saved Comparison Profiles

Dift supports reusable saved comparison profiles.

Profiles help automate recurring dataset checks and validation workflows.

## Create a Profile

```bash
dift profile create nightly-check \
  --old examples/old.csv \
  --new examples/new.csv \
  --key customer_id \
  --report html \
  --threshold 0.1
```

## Run a Profile

```bash
dift profile run nightly-check
```

## List Profiles

```bash
dift profile list
```

## Show Profile Details

```bash
dift profile show nightly-check
```

## Delete a Profile

```bash
dift profile delete nightly-check
```

---

# Configuration Priority

Dift resolves settings using:

```text
CLI arguments > Saved Profiles > Config Files > Defaults
```

This makes Dift flexible for:

* automation
* CI/CD pipelines
* scheduled validations
* reusable workflows

---

# Batch Dataset Comparison

Dift supports batch comparison workflows for validating multiple dataset pairs in one command.

This is useful for:

* ETL validation pipelines
* scheduled dataset monitoring
* multi-table warehouse checks
* automated regression testing

---

## Folder Structure Example

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
````

Dift automatically matches files by filename.

Example:

* `old/customers.csv` <--> `new/customers.csv`
* `old/orders.csv` <--> `new/orders.csv`

---

## Run Batch Comparison

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --key id
```

---

## Generate Batch HTML Reports

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --key id \
  --report html \
  --output-dir reports/batch
```

Example output structure:

```text
reports/
└── batch/
    ├── customers/
    │   └── dift_report.html
    ├── orders/
    │   └── dift_report.html
    └── products/
        └── dift_report.html
```

---

## Batch CSV Reports

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --report csv \
  --output-dir reports/csv
```

---

## Continue On Error

By default, Dift continues running other comparisons even if one fails.

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --continue-on-error
```

Stop immediately on first failure:

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --stop-on-error
old_dataset: "examples/old.csv"
new_dataset: "examples/new.csv"
key: "customer_id"
threshold: 0.05
report: "html"  
```

---

# Comparison History

Dift supports persistent comparison history tracking.

This helps teams monitor:

* dataset drift over time
* recurring quality issues
* historical risk changes
* long-term data trust trends

---

## Save Comparison History

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id \
  --history
````

By default, history is saved to:

```text
.dift/history/history.jsonl
```

---

## Custom History Directory

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id \
  --history \
  --history-dir reports/history
```

---

## View Saved History

```bash
dift history list
```

Example output:

```text
1. 2026-05-15T12:30:00Z | risk=medium | old.csv -> new.csv
2. 2026-05-16T08:10:00Z | risk=high | prod.csv -> staging.csv
```

---

## Show Detailed History Record

```bash
dift history show 1
```

---

## Clear History

```bash
dift history clear
```

---

## Batch Comparison History

Save history during batch workflows:

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --history \
  --history-dir reports/batch-history
```

Example structure:

```text
reports/
└── batch-history/
    ├── customers/
    │   └── history.jsonl
    ├── orders/
    │   └── history.jsonl
    └── products/
        └── history.jsonl
```
### Configuration Priority
Dift follows a strict priority chain to give you maximum flexibility:
1. **CLI Arguments** (Highest priority, overrides everything)
2. **Configuration File** (YAML, TOML, or JSON)
3. **Internal Defaults** (Threshold: 0.1, Report: console)

---

## Scheduled Comparisons

Dift supports reusable scheduled comparison workflows for automation, monitoring, CI/CD pipelines, and recurring data quality checks.

This makes it easy to:

* run nightly drift checks
* automate production dataset validation
* integrate with cron jobs
* schedule profile-based comparisons
* build monitoring workflows

---

# Create a Reusable Profile

First create a comparison profile:

```bash
dift profile create nightly-check \
  --old examples/old.csv \
  --new examples/new.csv \
  --key customer_id \
  --report html \
  --output reports/nightly.html
```

This saves all comparison settings into a reusable profile.

---

# Generate a Cron Schedule

Generate a cron-ready command:

```bash
dift schedule cron nightly-check
```

Example output:

```cron
0 2 * * * dift profile run nightly-check --history --strict-exit-codes
```

This means:

* run every day
* at 2:00 AM
* save comparison history
* use automation-friendly exit codes

---

# Custom Schedule Times

Generate a custom cron schedule:

```bash
dift schedule cron nightly-check \
  --hour 5 \
  --minute 30
```

Output:

```cron
30 5 * * * dift profile run nightly-check --history --strict-exit-codes
```

Runs daily at 5:30 AM.

---

# Save Scheduled Jobs

Create a named schedule:

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

Example:

```text
- daily-check
```

---

# Show Schedule Details

```bash
dift schedule show daily-check
```

Example output:

```json
{
  "profile": "nightly-check",
  "cron": "0 2 * * *"
}
```

---

# Run a Schedule Manually

You can manually trigger a saved schedule:

```bash
dift schedule run daily-check
```

This runs the associated profile immediately.

---

# Delete a Schedule

```bash
dift schedule delete daily-check
```

---

# Example Cron Integration (Linux/macOS)

Open your crontab:

```bash
crontab -e
```

Add:

```cron
0 2 * * * dift profile run nightly-check --history --strict-exit-codes
```

---

# Example Windows Task Scheduler

Use the generated command:

```bash
dift profile run nightly-check --history --strict-exit-codes
```

inside:

* Windows Task Scheduler
* Jenkins
* GitHub Actions
* Airflow
* Prefect
* Dagster
* CI/CD pipelines

---

# Automation-Friendly Exit Codes

Dift supports optional risk-based exit codes for automation workflows.

By default, Dift exits with:

```text
0
```

when comparisons complete successfully.

Enable strict automation behavior with:

```bash
dift prod.csv candidate.csv \
  --key id \
  --strict-exit-codes
```

---

## Exit Code Mapping

| Exit Code | Meaning |
|---|---|
| `0` | Low-risk comparison |
| `1` | Medium-risk drift detected |
| `2` | High-risk drift detected |
| `3` | Runtime error, invalid input, or failed comparison |


This allows Dift to automatically fail pipelines when risky dataset changes are detected.

---

## Example

```bash
dift prod.csv staging.csv \
  --key customer_id \
  --strict-exit-codes

echo $?
```

Example output:

```text
2
```

This means Dift detected a high-risk dataset change.

---

## Backward Compatibility

Strict exit codes are optional.

Without `--strict-exit-codes`, Dift preserves the original behavior and exits successfully when comparisons complete.

---

## Non-Interactive CLI Support

Dift supports automation-friendly execution for CI/CD pipelines, cron jobs, Airflow, Jenkins, GitHub Actions, and scheduled workflows.

### Quiet Mode

Suppress non-error output:

```bash
dift old.csv new.csv \
  --key id \
  --quiet
```

This is useful for:

* cron jobs
* CI/CD pipelines
* scheduled validation workflows
* automated monitoring

Errors will still be displayed.

---

### Disable Colored Output

Disable ANSI terminal colors for cleaner logs:

```bash
dift old.csv new.csv \
  --key id \
  --no-color
```

Useful for:

* log aggregation systems
* CI logs
* plain-text terminals
* automation tools

---

### Fully Automation-Friendly Example

```bash
dift old.csv new.csv \
  --key id \
  --strict-exit-codes \
  --quiet \
  --no-color
```

This combination provides:

* predictable exit codes
* machine-friendly output
* clean CI logs
* non-interactive execution behavior

---

### Scheduled Workflow Example

```bash
dift schedule cron nightly-check
```

Example output:

```cron
0 2 * * * dift profile run nightly-check --history --strict-exit-codes --quiet --no-color
```

---


# DuckDB Support

Dift supports comparing datasets directly from DuckDB databases.

This enables warehouse-style comparisons, SQL-based validation, and Parquet-backed analytical workflows.

## Compare DuckDB Tables

```bash
dift duckdb:///examples/warehouse.duckdb:customers_old \
     duckdb:///examples/warehouse.duckdb:customers_new \
     --key customer_id
```

## URI Format

```text
duckdb:///path/to/database.duckdb:table_name
```

## Example

```text
duckdb:///data/warehouse.duckdb:orders
```

## Works With

* existing risk scoring
* HTML reports
* Excel reports
* JSON reports
* CSV reports
* drift detection
* quality validation

## Common Use Cases

* local analytics warehouses
* Parquet validation workflows
* SQL-based dataset comparison
* batch data quality checks

## Notes

* DuckDB database files must exist locally.
* Remote DuckDB connections are not currently supported.
* Table names may be case-sensitive depending on configuration.
* DuckDB comparisons use the existing Dift comparison engine and reports.

---


# BigQuery Support

Dift supports comparing datasets directly from Google BigQuery.

This enables cloud warehouse validation, analytical comparisons, and SQL-driven data quality workflows.

## Compare BigQuery Tables

```bash
dift bigquery://my-project.analytics.customers_old \
     bigquery://my-project.analytics.customers_new \
     --key customer_id
```

## URI Format

```text
bigquery://project.dataset.table
```

## Example

```text
bigquery://acme-analytics.sales.orders
```

## Authentication

Dift uses standard Google Cloud authentication.

Set your service account credentials:

### Linux / macOS

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
```

### Windows Git Bash

```bash
export GOOGLE_APPLICATION_CREDENTIALS="C:/path/to/service-account.json"
```

## Install Dependencies

```bash
pip install google-cloud-bigquery db-dtypes
```

## Works With

* existing risk scoring
* HTML reports
* Excel reports
* JSON reports
* CSV reports
* drift detection
* quality validation

## Common Use Cases

* cloud warehouse validation
* production dataset monitoring
* analytics QA workflows
* cross-environment data comparison
* SQL-driven data quality checks

## Notes

* BigQuery access requires valid Google Cloud credentials.
* BigQuery billing and permissions are managed through Google Cloud.
* BigQuery comparisons use the existing Dift comparison engine and reports.

---

# SQL Database Support

Dift supports comparing datasets directly from SQL databases using SQLAlchemy-compatible connection strings.

This enables database-native validation workflows without exporting tables to CSV or other intermediate formats.

Supported workflows include:

* table-to-table comparison
* query-to-query comparison
* database-to-database comparison
* database-to-file comparison
* SQL-backed drift detection
* warehouse and ETL validation
* migration verification
* analytics quality assurance
* CI/CD data validation
* production data trust workflows

---

## Compare SQL Tables

### SQLite

SQLite support enables lightweight local database comparison workflows.

Compare SQLite tables directly:

```bash
dift sqlite:///examples/old.db:customers_old \
     sqlite:///examples/new.db:customers_new \
     --key customer_id
```

SQLite is useful for:

* lightweight local testing
* embedded analytics
* file-based database comparison
* CI testing workflows
* portable validation pipelines

---

### PostgreSQL

Install PostgreSQL driver:

```bash
pip install psycopg2-binary
```

Compare PostgreSQL tables:

```bash
dift postgresql://user:password@localhost:5432/sales_db:customers_old \
     postgresql://user:password@localhost:5432/sales_db:customers_new \
     --key customer_id
```

Alternative PostgreSQL driver example:

```bash
dift postgresql+psycopg://user:password@localhost:5432/sales_db:customers_old \
     postgresql+psycopg://user:password@localhost:5432/sales_db:customers_new \
     --key customer_id
```

PostgreSQL support is useful for:

* production ETL validation
* warehouse consistency checks
* analytics engineering workflows
* CI/CD data quality validation
* staging vs production comparison
* migration validation
* operational data verification

---

### MySQL

Install MySQL driver:

```bash
pip install pymysql
```

Compare MySQL tables:

```bash
dift mysql+pymysql://user:password@localhost:3306/sales_db:customers_old \
     mysql+pymysql://user:password@localhost:3306/sales_db:customers_new \
     --key customer_id
```

MySQL support enables direct database-native comparison workflows without intermediate exports.

Useful for:

* operational database validation
* business reporting QA
* ETL verification
* transactional system comparison
* migration checks

---

### Amazon Redshift

Install Redshift dependencies:

```bash
pip install sqlalchemy-redshift redshift-connector
```

Compare Redshift tables:

```bash
dift redshift+redshift_connector://user:password@cluster.region.redshift.amazonaws.com:5439/dev:orders_old \
     redshift+redshift_connector://user:password@cluster.region.redshift.amazonaws.com:5439/dev:orders_new \
     --key order_id
```

Alternative Redshift driver example:

```bash
dift redshift+psycopg2://user:password@cluster.region.redshift.amazonaws.com:5439/dev:orders_old \
     redshift+psycopg2://user:password@cluster.region.redshift.amazonaws.com:5439/dev:orders_new \
     --key order_id
```

Redshift support is useful for:

* warehouse validation
* analytics QA
* production data checks
* ETL reconciliation
* staging vs production comparison
* large-scale analytical workflows
* cloud warehouse quality monitoring

---

## URI Format

```text
connection_string:table_name
```

Examples:

```text
sqlite:///examples/data.db:customers

postgresql://user:password@localhost:5432/mydb:customers
postgresql+psycopg://user:password@localhost:5432/mydb:customers
postgresql+psycopg2://user:password@localhost:5432/mydb:customers

mysql+pymysql://user:password@localhost:3306/mydb:customers

redshift+redshift_connector://user:password@cluster.region.redshift.amazonaws.com:5439/dev:orders
redshift+psycopg2://user:password@cluster.region.redshift.amazonaws.com:5439/dev:orders
```

---

## Install Dependencies

Core SQL support:

```bash
pip install sqlalchemy
```

Database-specific drivers:

```bash
pip install psycopg2-binary   # PostgreSQL
pip install pymysql           # MySQL
```

Redshift dependencies:

```bash
pip install sqlalchemy-redshift redshift-connector
```

Optional PostgreSQL alternative driver:

```bash
pip install psycopg
```

---

## Supported Workflows

SQL database datasets work with the existing Dift comparison engine and reporting system, including:

* schema comparison
* row comparison
* numeric drift detection
* categorical drift detection
* outlier detection
* null spike detection
* duplicate spike detection
* risk scoring
* JSON reports
* CSV reports
* Excel reports
* HTML reports
* history tracking
* automation workflows

---

## Common Use Cases

* ETL validation
* staging vs production comparison
* analytics QA
* warehouse validation
* CI/CD data checks
* migration verification
* database quality monitoring
* drift monitoring
* business reporting validation
* reconciliation workflows

---

## Notes

* SQLite database files must exist locally.
* PostgreSQL, MySQL, and Redshift require valid credentials and reachable database servers.
* PostgreSQL supports standard SQLAlchemy PostgreSQL drivers including `psycopg` and `psycopg2`.
* Redshift support works through SQLAlchemy-compatible Redshift drivers.
* SQL comparisons use the existing Dift comparison engine and reporting system.
* SQL support is powered by SQLAlchemy.
* Database query results are loaded into Polars DataFrames before comparison.

---

## Requirements

* Python 3.10+

---

## Quick Install

```bash
pip install dift-cli
```

Then run:

```bash
dift --help
```

---

## Quick Update (Latest version: 0.5.0)

```bash
pip install --upgrade dift-cli
```

---

## Cross Platform Setup

### Windows (Git Bash)

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install dift-cli
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install dift-cli
```

### Mac / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install dift-cli
```

### pipx (Recommended)

```bash
pipx install dift-cli
```

---

## Verify Install

```bash
dift --help
```

or

```bash
python -m dift.cli --help
```

---

# Quick Start

## Compare CSV Files

```bash
dift examples/old.csv examples/new.csv --key customer_id
```

If your paths are defined in the config, just run:
```bash
dift --config examples/config_sample.yaml
```
---

## Detect Numeric Drift

```bash
dift examples/old_drift.csv examples/new_drift.csv --key id --threshold 0.1
```

---

# Generate Reports

## JSON

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id \
  --report json \
  --output report.json
```

## CSV

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id \
  --report csv \
  --output report.csv
```

## Excel

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id \
  --report excel \
  --output report.xlsx
```

## HTML

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id \
  --report html \
  --output report.html
```

## HTML with Template

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id \
  --report html \
  --template dark \
  --output report.html
```

---

# Run using Config Files

```bash
dift examples/old.csv examples/new.csv \
  --config examples/config_sample.yaml
```

---

# Run using Saved Profiles

```bash
dift profile run nightly-check
```
## Run Batch Dataset Comparison

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --key customer_id
````
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

# Example Files

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
├── config_with_datasets.yaml
├── config_with_datasets.toml
└── config_with_datasets.json
```

---

# Use Cases

## ETL Validation

```bash
dift before.csv after.csv
```

## ML Dataset Drift

```bash
dift train_v1.csv train_v2.csv
```

## Production vs Staging

```bash
dift prod.csv staging.csv --key id
```

## Silent Data Drift Detection

```bash
dift train_v1.csv train_v2.csv --threshold 0.1
```

## Automated Validation Workflow

```bash
dift profile run nightly-check
```


## Multi-Table ETL Validation

```bash
dift batch \
  --old-dir warehouse_snapshot_1 \
  --new-dir warehouse_snapshot_2 \
  --report html \
  --output-dir reports/
```


## Historical Drift Monitoring

```bash
dift prod.csv staging.csv \
  --key customer_id \
  --history
```

Track how risk and drift evolve across repeated comparison runs.


---


# Project Structure

```text
dift/
├── cli.py
├── core/
│   ├── comparator.py
│   ├── schema_diff.py
│   ├── row_diff.py
│   ├── quality_diff.py
│   ├── stats_diff.py
│   └── risk.py
├── io/
│   ├── config_loader.py
|   └── readers.py
├── reports/
│   ├── console_report.py
│   ├── json_report.py
│   ├── csv_report.py
│   ├── excel_report.py
│   ├── html_report.py
│   └── models.py
├── profiles.py
├── batch.py
├── thresholds.py
├── schedules.py
├── history.py
└── utils/

tests/
examples/
```

---

# Run Tests

```bash
pytest
```

Lint:

```bash
ruff check .
```

Type checking:

```bash
mypy dift
```

---

# Roadmap

## v0.6.0

### Database Support

#### SQL Database Integration

* [x] Direct database-to-database comparison
* [x] Table-to-table comparison support
* [x] Query-based dataset comparison
* [x] Connection string support
* [x] CLI database input support

#### PostgreSQL Connector

* [x] PostgreSQL table reader
* [x] Schema inference support
* [x] Query execution support
* [x] Secure connection handling

#### MySQL Connector

* [x] MySQL table reader
* [x] Query-based comparisons
* [x] Type compatibility handling

#### SQLite Connector

* [x] SQLite local database support
* [x] Lightweight comparison workflows
* [x] File-based database comparison

#### DuckDB Support

* [x] Native DuckDB integration
* [x] Analytical dataset support
* [x] Parquet interoperability


### Data Warehouse Support

#### Snowflake Connector

* Snowflake authentication support
* Warehouse query execution
* Large-scale dataset comparison

#### BigQuery Connector

* [x] BigQuery dataset comparison
* [x] Service account authentication
* [x] Query-based workflows

#### Redshift Connector

* Redshift warehouse support
* Efficient table extraction
* Warehouse schema compatibility

### Configuration System

#### Config File Support

* [x] YAML configuration support
* [x] TOML configuration support
* [x] JSON configuration support
* [x] Dataset path support in configuration files  

#### Saved Comparison Profiles

* [x] Reusable comparison profiles
* [x] Saved report configurations
* [x] Named comparison presets

#### Reusable Threshold Configs

* [x] Numeric drift thresholds
* [x] Categorical shift thresholds
* [x] Outlier thresholds
* [x] Column-level threshold overrides

#### Environment-Based Configs

* [x] Development/staging/production configs
* [x] Environment variable support
* [x] Secret management preparation


### Automation Features

#### Scheduled Comparisons

* [x] Scheduled dataset checks
* [x] Cron-friendly execution
* [x] Time-based comparison workflows

#### CLI Automation Workflows

* [x] Non-interactive CLI support
* [x] Automation-friendly exit codes
* Pipeline integration support

#### Batch Dataset Comparison

* [x] Multi-dataset comparison support
* [x] Folder-based comparisons
* [x] Batch report generation

#### Comparison History

* [x] Historical comparison tracking
* [x] Drift trend analysis
* [x] Historical risk tracking

### Reporting Improvements

#### Better Excel Formatting

* [x] Severity color coding
* [x] Conditional formatting
* [x] Improved worksheet layouts
* [x] Better readability styling

#### Better HTML Reports

* [x] Drift highlighting
* [x] Severity badges
* [x] Improved visual summaries
* [x] Responsive layouts

#### Report Metadata Expansion

* [x] Execution timestamps
* [x] Runtime metrics
* [x] Dataset source metadata
* [x] Threshold metadata



### Developer Experience

#### Testing Improvements

* Connector integration tests
* Cross-format consistency tests
* Warehouse mock testing

#### CLI Improvements

* Better help messages
* Clearer validation errors
* Progress indicators

#### Plugin Preparation

* Extensible reader interfaces
* Connector registry architecture
* Internal plugin preparation


---

## Contributing

Contributions are welcome.

See:

```text
CONTRIBUTING.md
```

Ways to help:

* Fix bugs
* Improve docs
* Add tests
* Improve performance
* Add connectors
* Improve CLI UX

---

## License

MIT License

---

## Vision

Dift aims to become the open-source standard for:
* dataset regression testing
* data drift monitoring
* ML data validation
* warehouse trust checks
* automated data quality enforcement