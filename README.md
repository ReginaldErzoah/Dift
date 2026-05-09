# Dift

<p align="left">
  <img src="assets/dift-logo.png" width="400" alt="Dift Logo">
</p>

Dift is an open-source CLI tool that helps data professionals compare two datasets and instantly understand:

* what changed
* why it matters
* whether the new data is safe to trust

---

## What's New in v0.3.0

Dift v0.3.0 introduces powerful reporting and export capabilities, making it easier to analyze and share dataset changes.

### New Features

* HTML report export
* CSV summary export
* Excel report export
* Improved JSON report structure
* Report templates (HTML)
* `--output-dir` support for directory-based exports

---

## Why Dift?

Bad data breaks:

* dashboards
* reports
* ETL pipelines
* analytics workflows
* ML models
* business decisions

Dift helps teams catch risky data changes **before they cause damage**.

---

## Features (v0.3.0)

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
* Null spikes
* Duplicate increases
* Numeric stats diff (with configurable threshold)
* Categorical value changes
* Risk scoring (`low`, `medium`, `high`)

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
```

Available templates:

* `default`
* `clean`
* `compact`
* `enterprise`
* `dark`

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

## Quick Update (Latest version: 0.3.0)

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
│ Risk Level: HIGH        │
╰─────────────────────────╯

Summary
Rows old: 10
Rows new: 11
Row delta: +1
Row change %: +10.00%

Warnings:
Nulls increased in revenue by 9.09%
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
└── new.json
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

---

## Project Structure

```text
dift/
├── cli.py
├── core/
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

* Improve null detection
* Improve duplicate detection

### v0.5.0

* Outlier detection
* Categorical shift warnings
* Better risk scoring

## v0.6.0

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

**If Git has `git diff`, data teams should have `dift`.**


