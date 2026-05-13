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

Dift v0.5.0 introduces advanced drift analysis, outlier detection, improved reporting, and stronger dataset risk analysis.

## New Features

* Outlier detection using IQR analysis
* Outlier severity classification
* Outlier risk scoring
* Advanced categorical drift detection
* Frequency distribution shift detection
* Categorical severity classification
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

### HTML Templates

Customize your HTML reports:

```bash
dift old.csv new.csv --report html --template cleans
```

Available templates:

* `default`
* `clean`
* `compact`
* `enterprise`
* `dark`

---

### Numeric Drift Thresholds

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

### Output Directory Support

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

### Configuration System

Dift supports persistent configuration files to make your workflows reproducible and cleaner.

```bash
dift old.csv new.csv --config dift.yaml
```

### Supported Formats
* **YAML** (`.yaml`, `.yml`)
* **TOML** (`.toml`)
* **JSON** (`.json`)

### Example Configuration (`dift.yaml`)
```yaml
key: "customer_id"
threshold: 0.05
report: "html"  
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

## Quick Start

### Compare CSV Files

```bash
dift examples/old.csv examples/new.csv --key customer_id
```

---

### Detect Numeric Drift

```bash
dift examples/old_drift.csv examples/new_drift.csv --key id --threshold 0.1
```

---

### Generate Reports

#### JSON

```bash
dift examples/old.csv examples/new.csv --key customer_id --report json --output report.json
```

#### CSV

```bash
dift examples/old.csv examples/new.csv --key customer_id --report csv --output report.csv
```

#### Excel

```bash
dift examples/old.csv examples/new.csv --key customer_id --report excel --output report.xlsx
```

#### HTML

```bash
dift examples/old.csv examples/new.csv --key customer_id --report html --output report.html
```

#### HTML with Template

```bash
dift examples/old.csv examples/new.csv --key customer_id --report html --template dark --output report.html
```

### Compare using a Config File

```bash
dift examples/old.csv examples/new.csv --config examples/config_sample.yaml
```

---

# Example Output

```text
╭─────────────────────────╮
│ Dift Dataset Comparison │
│ Risk Level: MEDIUM      │
╰─────────────────────────╯

Warnings

Numeric drift: 'revenue'
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

## Example Files

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
└── new_drift.csv
├── ...
├── config_sample.yaml
├── config_sample.toml
└── config_sample.json
```

---

## Use Cases

### ETL Validation

```bash
dift before.csv after.csv
```

### ML Dataset Drift

```bash
dift train_v1.csv train_v2.csv
```

### Production vs Staging

```bash
dift prod.csv staging.csv --key id
```

### Silent Data Drift Detection

```bash
dift train_v1.csv train_v2.csv --threshold 0.1
```

---

## Project Structure

```text
dift/
├── cli.py
├── core/
│   ├── schema_diff.py
│   ├── row_diff.py
│   ├── quality_diff.py
│   ├── stats_diff.py
│   └── risk.py
├── io/
├── reports/
│   ├── console_report.py
│   ├── json_report.py
│   ├── csv_report.py
│   ├── excel_report.py
│   ├── html_report.py
│   └── models.py
└── utils/

tests/
examples/
```

---

## Run Tests

```bash
pytest
```

Lint:

```bash
ruff check .
```

---

## Roadmap

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

* Reusable comparison profiles
* Saved report configurations
* Named comparison presets

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

* Multi-dataset comparison support
* Folder-based comparisons
* Batch report generation

#### Comparison History

* Historical comparison tracking
* Drift trend analysis
* Historical risk tracking

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