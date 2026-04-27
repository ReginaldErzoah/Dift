# Dift
<p align="left">
  <img src="assets/dift-logo.png" width="400" alt="Dift Logo">
</p>

Dift is an open-source CLI tool that helps data professionals compare two datasets and instantly understand:

- what changed  
- why it matters  
- whether the new data is safe to trust  


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

## Features (v0.1.1)

Compare two datasets in seconds.

### Supported Formats

- CSV
- Parquet
- Excel (`.xlsx`, `.xls`)

### Detect Changes

- Schema diff
- Row count diff
- Added / removed rows
- Changed rows (with key column)
- Column type changes
- Null spikes
- Duplicate increases
- Numeric stats diff
- Categorical value changes

### Output

- Rich CLI report
- JSON report export

## Required version

Requires Python 3.10+

---
## Quick Install

```bash
pip install dift-cli
```

Then run:

```bash
dift --help
```

## Cross-Platform Setup

### Windows Git Bash
```bash
python -m venv .venv
source .venv/Scripts/activate
pip install dift-cli
```

### Windows PowerShell
```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install dift-cli
```

If `dift` is not recognized, restart terminal or reinstall Python with "Add Python to PATH".

### Mac / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install dift-cli
```

### pipx (Recommended for CLI tools)
```bash
pipx install dift-cli
```

If user does not have pipx,
```bash
python -m pip install pipx
python -m pipx ensurepath
```


## Verify Install

```bash
dift --help
```

or

```bash
python -m dift.cli --help
```

## Upgrade Later

```bash
pip install --upgrade dift-cli
```

## If Command Not Found

Use:

```bash
python -m dift.cli --help
```


---

## Quick Start

### Compare CSV Files

```bash
dift examples/old.csv examples/new.csv --key customer_id
```

### Compare Parquet Files

```bash
dift examples/old.parquet examples/new.parquet --key customer_id
```

### Compare Excel Files

```bash
dift examples/old.xlsx examples/new.xlsx --key customer_id
```

### Run via Python Module

```bash
python -m dift.cli examples/old.csv examples/new.csv --key customer_id
```

### Generate JSON Report

```bash
dift examples/old.csv examples/new.csv --key customer_id --report json --output report.json
```

---

## Example Output

```text
Dift Comparison Report

Rows old: 10
Rows new: 11

Added rows: 2
Removed rows: 1
Changed rows: 6

Schema changes: 1
Null spikes: 1

Risk Level: MEDIUM
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
└── new.xlsx
```

Use them to test instantly.

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

### v0.2.0

- Better console formatting
- Rich colors
- Cleaner summary tables
- JSON support & examples datasets
- More supports & example datasets

## v0.3.0 — Report exports

- Add HTML report export
- Add CSV summary export
- Add Excel report export
- Improve JSON report structure
- Add report templates
- Add --output-dir

## v0.4.0

- Improve null spike detection
- Improve duplicate detection

## v0.5.0

- Add outlier detection
- Add numeric drift thresholds
- Add categorical shift warnings
- Improve risk scoring

### v0.6.0

- SQL database support
- Postgres connector

### v0.7.0

- Snowflake connector
- BigQuery connector

### v0.8.0

- CI/CD fail checks
- dbt integration

### v0.9.0
- Drift alerts
- Python API
- Plugin system


## v1.0.0 - Stable release

- Stable CLI
- Stable Python API
- Full test coverage
- Full docs site
- Benchmarks
- Security review
- Production ready install

---

## Contributing

Contributions are welcome.

Please read:

```text
CONTRIBUTING.md
```

Ways to help:

- Fix bugs
- Improve docs
- Add tests
- Improve performance
- Add connectors
- Improve CLI UX

---

## License

MIT License

---

## Vision

Dift aims to become the standard open-source tool for dataset comparison and trust checks.

**If Git has `git diff`, data teams should have `dift`.**