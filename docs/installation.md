# Installation

This guide explains how to install Dift across different operating systems and environments.

---

# Requirements

Dift requires:

- Python 3.10+
- pip
- terminal or shell access

Verify your Python version:

```bash
python --version
```

or

```bash
python3 --version
```

---

# Install Dift

## Standard Installation

```bash
pip install dift-cli
```

---

# Upgrade Dift

Upgrade to the latest version:

```bash
pip install --upgrade dift-cli
```

---

# Verify Installation

Run:

```bash
dift --help
```

or:

```bash
python -m dift.cli --help
```

You should see the Dift CLI help output.

---

# Virtual Environment Setup

Using a virtual environment is strongly recommended.

---

## Windows (Git Bash)

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install dift-cli
```

---

## Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install dift-cli
```

---

## Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install dift-cli
```

---

# pipx Installation (Recommended)

For isolated CLI environments:

```bash
pipx install dift-cli
```

Upgrade later:

```bash
pipx upgrade dift-cli
```

---

# Install From Source

Clone the repository:

```bash
git clone https://github.com/ReginaldErzoah/Dift.git
```

Enter the project directory:

```bash
cd Dift
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

### Windows (Git Bash)

```bash
source .venv/Scripts/activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Dift in editable mode:

```bash
pip install -e .
```

---

# Optional Connector Dependencies

Some connectors require additional packages.

---

## PostgreSQL

```bash
pip install psycopg2-binary
```

or:

```bash
pip install psycopg
```

---

## MySQL

```bash
pip install pymysql
```

---

## Redshift

```bash
pip install sqlalchemy-redshift redshift-connector
```

---

## Snowflake

```bash
pip install snowflake-sqlalchemy
```

---

## BigQuery

```bash
pip install google-cloud-bigquery db-dtypes
```

---

## DuckDB

```bash
pip install duckdb
```

---

# Install SQL Support

Core SQL support requires SQLAlchemy:

```bash
pip install sqlalchemy
```

---

# Development Installation

Install development tools:

```bash
pip install -r requirements-dev.txt
```

Typical development tooling includes:

- pytest
- ruff
- mypy

---

# Verify Development Environment

Run tests:

```bash
pytest
```

Run linting:

```bash
ruff check .
```

Run type checking:

```bash
mypy dift
```

---

# Common Installation Issues

## Python Version Too Old

Error example:

```text
Python 3.9 is not supported
```

Solution:

Install Python 3.10 or newer.

---

## Command Not Found

Error example:

```text
dift: command not found
```

Possible fixes:

### Reinstall

```bash
pip install dift-cli
```

### Use Python Module Execution

```bash
python -m dift.cli --help
```

### Verify PATH

Ensure your Python scripts directory is available in your system PATH.

---

## Missing Connector Drivers

Error example:

```text
PostgreSQL support requires psycopg2
```

Install the required driver:

```bash
pip install psycopg2-binary
```

---

# Next Steps

After installation:

- Continue to the Quick Start guide
- Learn dataset comparison workflows
- Explore reports and automation features
- Configure connectors and warehouses

---

# Quick Start

Basic comparison:

```bash
dift examples/old.csv examples/new.csv --key customer_id
```

Generate an HTML report:

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id \
  --report html \
  --output report.html
```