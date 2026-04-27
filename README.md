# Dift

> **Git diff for datasets.**

Dift is an open-source CLI tool that helps data professionals compare two datasets and instantly understand:

- what changed  
- why it matters  
- whether the new data is safe to trust  

## Install Anywhere (Windows / Mac / Linux)

```bash
pip install dift-cli
```

Then run:

```bash
dift --help
```

Install package name: dift-cli  
Command name: dift

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

## Features (v0.1 MVP)

Compare two datasets in seconds

### Supported Formats

- CSV
- Parquet

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

---

## Installation

### Clone Repository

```bash
git clone https://github.com/ReginaldErzoah/Dift.git
cd Dift
```

### Create Virtual Environment

```bash
python -m venv .venv
source .venv/Scripts/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install CLI Locally

```bash
pip install -e .
```

---

## Quick Start

Run a comparison:

```bash
dift examples/old.csv examples/new.csv --key customer_id
```

Or:

```bash
python -m dift.cli examples/old.csv examples/new.csv --key customer_id
```

Generate JSON report:

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

## Example Use Cases

### ETL Validation

```bash
dift before.csv after.csv
```

### Daily Snapshot Checks

```bash
dift yesterday.parquet today.parquet
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
│   └── stats_diff.py
├── io/
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

---

## Roadmap

### v0.2

- HTML reports
- Better console formatting
- Performance improvements

### v0.5

- SQL database support
- Postgres connector
- Snowflake connector
- BigQuery connector

### v1.0

- CI/CD fail checks
- dbt integration
- Drift alerts
- Python API
- Plugin system

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
