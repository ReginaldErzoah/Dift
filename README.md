# Dift

<p align="left">
  <img src="assets/dift-logo.png" width="400" alt="Dift Logo">
</p>

Dift is an open-source CLI tool that helps data professionals compare two datasets and instantly understand:

- what changed  
- why it matters  
- whether the new data is safe to trust  

---

## What's New in v0.2.1

Dift v0.2.1 introduces a more polished CLI experience and broader file support.

### New Improvements

- Better console formatting
- Rich terminal colors
- Cleaner summary tables
- Risk level highlighting
- Percentage row change display
- Better missing file error messages
- JSON dataset support
- JSON example datasets
- Excel example datasets
- Parquet example datasets
- Improved installation instructions

---

## Why Dift?

Bad data breaks:

- dashboards  
- reports  
- ETL pipelines  
- analytics workflows  
- ML models  
- business decisions  

Dift helps teams catch risky data changes **before they cause damage**.

---

## Features (v0.2.1)

Compare two datasets in seconds.

### Supported Formats

- CSV
- Parquet
- Excel (`.xlsx`, `.xls`)
- JSON

### Detect Changes

- Schema diff
- Row count diff
- Added rows
- Removed rows
- Changed rows (with key column)
- Column type changes
- Null spikes
- Duplicate increases
- Numeric stats diff
- Categorical value changes
- Risk scoring (`low`, `medium`, `high`)

### Output

- Rich CLI report
- JSON report export

---

## Requirements

- Python 3.10+

---

## Quick Install

```bash
pip install dift-cli
````

Then run:

```bash
dift --help
```

## Quick Update (Latest version: 0.2.1)
```
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

### pipx (Recommended for CLI Tools)

```bash
pipx install dift-cli
```

If `pipx` is not installed:

```bash
python -m pip install pipx
python -m pipx ensurepath
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

## If Command Not Found

Use:

```bash
python -m dift.cli --help
```

Or restart your terminal.

---

## Quick Start

### Compare CSV Files

```bash
dift examples/old.csv examples/new.csv --key customer_id
```
```bash
dift examples/old3.csv examples/new3.csv --key emp_id
```

### Compare Parquet Files

```bash
dift examples/old.parquet examples/new.parquet --key customer_id
```

### Compare Excel Files

```bash
dift examples/old.xlsx examples/new.xlsx --key customer_id
```

### Compare JSON Files

```bash
dift examples/old.json examples/new.json --key customer_id
```

### Generate JSON Report

```bash
dift examples/old.csv examples/new.csv --key customer_id --report json --output report.json
```
### Generate CSV Report

```bash
dift examples/old.csv examples/new.csv --key customer_id --report csv --output csv.json
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

## Example Files Included

```text
examples/
├── old.csv
├── new.csv
├── old.parquet
├── new.parquet
├── old.xlsx
├── new.xlsx
├── old.json
|── new.json
├── old.csv
├── new.csv
├── old.parquet
├── new.parquet
├── old.xlsx
├── new.xlsx
├── old.json
└── new.json
```
More examples also available.
Check examples folder and use them to test instantly.

But familiar with the examples columns and remember to use it's primary key column for the --key input.

---

## Example Use Cases

### ETL Validation

```bash
dift before.csv after.csv
```

### Daily Snapshot Checks

```bash
dift yesterday.parquet today.parquet
```

### Excel File Audits

```bash
dift old.xlsx new.xlsx --key id
```

### JSON API Export Checks

```bash
dift old.json new.json --key id
```

### Production vs Staging

```bash
dift prod.csv staging.csv --key id
```

### ML Dataset Drift Checks

```bash
dift train_v1.csv train_v2.csv
```

---

## Project Structure

```text
dift/
├── cli.py
├── core/
│   ├── comparator.py
│   ├── schema_diff.py
│   ├── row_diff.py
│   ├── quality_diff.py
│   ├── risk.py
│   └── stats_diff.py
├── io/
│   └── readers.py
├── reports/
│   ├── console_report.py
│   ├── json_report.py
|   ├── csv_report.py
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

Lint code:

```bash
ruff check .
```

---

## Roadmap

## v0.3.0

* HTML report export
* CSV summary export
* Excel report export
* Better JSON report structure
* Report templates
* `--output-dir`

## v0.4.0

* Improve null spike detection
* Improve duplicate detection

## v0.5.0

* Outlier detection
* Numeric drift thresholds
* Categorical shift warnings
* Better risk scoring

## v0.6.0

* SQL database support
* Postgres connector

## v0.7.0

* Snowflake connector
* BigQuery connector

## v0.8.0

* CI/CD fail checks
* dbt integration

## v0.9.0

* Drift alerts
* Python API
* Plugin system

## v1.0.0

* Stable CLI
* Stable Python API
* Full test coverage
* Full docs site
* Benchmarks
* Security review
* Production-ready install

---

## Contributing

Contributions are welcome.

Please read:

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
