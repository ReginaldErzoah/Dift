# Dift

<p align="left">
  <img src="assets/dift-logo.png" width="400" alt="Dift Logo">
</p>

Dift is an open-source CLI tool that helps data professionals compare two datasets and instantly understand:

* what changed
* why it matters
* whether the new data is safe to trust

---

## What's New in v0.4.0

Dift v0.4.0 introduces major improvements to data quality validation, numeric drift detection, and weighted risk scoring.

### New Features

* Improved null spike detection
* Improved duplicate spike detection
* Weighted risk scoring system
* Numeric drift detection
* Configurable drift thresholds
* Severity-based warnings
* Better quality validation
* Improved JSON report structure
* HTML report templates
* Excel report export
* CSV summary export
* `--output-dir` support

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

## Features (v0.4.0)

Compare two datasets in seconds.

### Supported Formats

* CSV
* Parquet
* Excel (`.xlsx`, `.xls`)
* JSON

---

### Detect Changes

* Schema diff
* Row count diff
* Added rows
* Removed rows
* Changed rows (with key column)
* Column type changes

### Data Quality Checks

* Null spikes
* Duplicate spikes
* Duplicate percentage changes
* Severity classification (`low`, `medium`, `high`)

### Drift Detection

* Numeric drift detection
* Mean shift detection
* Standard deviation drift
* Range shift detection
* Configurable drift threshold
* Categorical value changes
* Frequency distribution changes

### Risk Analysis

* Weighted risk scoring
* Risk classification (`low`, `medium`, `high`)
* Multi-signal risk evaluation

---

### Output Options

* Rich CLI report
* JSON report
* CSV summary
* Excel report
* HTML report

---

### HTML Templates

Customize your HTML reports:

```bash
dift old.csv new.csv --report html --template clean
````

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

## Quick Update (Latest version: 0.4.0)

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

---

## Example Output

```text
╭─────────────────────────╮
│ Dift Dataset Comparison │
│ Risk Level: MEDIUM      │
╰─────────────────────────╯

Summary
Rows old: 5
Rows new: 5
Row delta: 0

Warnings
Null spike: 'revenue' increased by 80.00% (high)
Duplicate spike: increased by 40.00% (high) using id
Numeric drift detected in 'revenue'
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

### v0.4.0

* Improved null spike detection
* Improved duplicate spike detection
* Weighted risk scoring
* Numeric drift detection
* Threshold-based drift alerts
* Better reporting

### v0.5.0

* Outlier detection
* Advanced categorical drift analysis
* Frequency shift alerts
* Trend analysis
* Time-series comparison
* Better visualization support

### v0.6.0

* SQL database support
* Postgres connector

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

Dift aims to become the standard open-source tool for dataset comparison and trust checks.