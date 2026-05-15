# Dift

<p align="left">
  <img src="assets/dift-logo.png" width="400" alt="Dift Logo">
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
key: customer_id
threshold: 0.1
report: html
template: dark
output_dir: reports/
```

## Example TOML Config

```toml
key = "customer_id"
threshold = 0.1
report = "html"
template = "dark"
output_dir = "reports/"
```

## Example JSON Config

```json
{
  "key": "customer_id",
  "threshold": 0.1,
  "report": "html",
  "template": "dark",
  "output_dir": "reports/"
}
```

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

* `old/customers.csv` ↔ `new/customers.csv`
* `old/orders.csv` ↔ `new/orders.csv`

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
└── config_sample.json
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

* Direct database-to-database comparison
* Table-to-table comparison support
* Query-based dataset comparison
* Connection string support
* CLI database input support

#### PostgreSQL Connector

* PostgreSQL table reader
* Schema inference support
* Query execution support
* Secure connection handling

#### MySQL Connector

* MySQL table reader
* Query-based comparisons
* Type compatibility handling

#### SQLite Connector

* SQLite local database support
* Lightweight comparison workflows
* File-based database comparison

#### DuckDB Support

* Native DuckDB integration
* Analytical dataset support
* Parquet interoperability


### Data Warehouse Support

#### Snowflake Connector

* Snowflake authentication support
* Warehouse query execution
* Large-scale dataset comparison

#### BigQuery Connector

* BigQuery dataset comparison
* Service account authentication
* Query-based workflows

#### Redshift Connector

* Redshift warehouse support
* Efficient table extraction
* Warehouse schema compatibility

### Configuration System

#### Config File Support

* [x] YAML configuration support
* [x] TOML configuration support
* [x] JSON configuration support

#### Saved Comparison Profiles

* [x] Reusable comparison profiles
* [x] Saved report configurations
* [x] Named comparison presets

#### Reusable Threshold Configs

* Numeric drift thresholds
* Categorical shift thresholds
* Outlier thresholds
* Column-level threshold overrides

#### Environment-Based Configs

* Development/staging/production configs
* Environment variable support
* Secret management support


### Automation Features

#### Scheduled Comparisons

* Scheduled dataset checks
* Cron-friendly execution
* Time-based comparison workflows

#### CLI Automation Workflows

* Non-interactive CLI support
* Automation-friendly exit codes
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

* Severity color coding
* Conditional formatting
* Improved worksheet layouts
* Better readability styling

#### Better HTML Reports

* Drift highlighting
* Severity badges
* Improved visual summaries
* Responsive layouts

#### Report Metadata Expansion

* Execution timestamps
* Runtime metrics
* Dataset source metadata
* Threshold metadata



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