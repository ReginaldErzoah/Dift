# Codebase Overview

This document provides a high-level overview of the Dift codebase structure, responsibilities of major modules, and development organization.

It is intended for:

- contributors
- maintainers
- plugin developers
- connector developers
- report system contributors

---

# Project Structure

```text
dift/
├── cli.py
├── batch.py
├── history.py
├── profiles.py
├── schedules.py
├── thresholds.py
│
├── core/
├── io/
├── reports/
├── utils/
│
└── plugins/   (future)
```

---

# Top-Level Modules

---

# `cli.py`

Primary command-line entrypoint.

Responsibilities:

- CLI argument parsing
- workflow orchestration
- progress handling
- configuration loading
- report execution
- automation behavior
- validation handling

Main technologies:

- Typer
- Rich

---

# `batch.py`

Handles multi-dataset comparison workflows.

Responsibilities:

- directory scanning
- dataset matching
- batch execution
- batch report handling
- partial failure management

Used for:

- ETL validation
- warehouse snapshots
- scheduled monitoring

---

# `history.py`

Manages persistent comparison history.

Responsibilities:

- saving history records
- reading historical runs
- history listing
- historical inspection
- history cleanup

Storage format:

```text
JSON Lines (.jsonl)
```

---

# `profiles.py`

Manages reusable comparison profiles.

Responsibilities:

- create profiles
- load profiles
- list profiles
- delete profiles
- reusable workflow configuration

Used for:

- scheduled jobs
- automation workflows
- recurring validations

---

# `schedules.py`

Handles scheduling workflows.

Responsibilities:

- cron generation
- schedule storage
- schedule execution
- reusable automation workflows

Designed for:

- cron jobs
- CI/CD
- Airflow
- Prefect
- Dagster

---

# `thresholds.py`

Handles reusable drift threshold configuration.

Responsibilities:

- global thresholds
- column-level overrides
- threshold validation
- threshold resolution

Supports:

- numeric drift
- categorical drift
- outlier thresholds

---

# Core Comparison Engine

Directory:

```text
dift/core/
```

This contains the main comparison logic.

---

# `core/comparator.py`

Central comparison orchestration engine.

Responsibilities:

- coordinate comparison execution
- aggregate diff modules
- calculate risk
- generate report models

Acts as:

```text
Central execution coordinator
```

---

# `core/schema_diff.py`

Schema comparison logic.

Responsibilities:

- added columns
- removed columns
- datatype changes
- schema compatibility analysis

---

# `core/row_diff.py`

Row comparison engine.

Responsibilities:

- row additions
- row removals
- row matching
- key-based comparison

---

# `core/quality_diff.py`

Quality validation engine.

Responsibilities:

- null analysis
- duplicate analysis
- quality degradation detection

---

# `core/stats_diff.py`

Drift analysis engine.

Responsibilities:

- numeric drift
- categorical drift
- outlier detection
- severity classification

---

# `core/risk.py`

Risk scoring engine.

Responsibilities:

- weighted scoring
- severity aggregation
- final risk classification

Risk levels:

- low
- medium
- high

---

# Dataset Reader System

Directory:

```text
dift/io/
```

Handles all dataset loading and connector workflows.

---

# `io/readers.py`

Main dataset loading entrypoint.

Responsibilities:

- dataset loading
- registry integration
- connector routing
- unified loading contract

---

# `io/base_reader.py`

Defines the shared reader interface.

Example:

```python
class BaseReader:
    def can_handle(self, source: str) -> bool:
        ...

    def read(self, source: str):
        ...
```

Purpose:

- standardize connectors
- reduce coupling
- prepare plugin support

---

# `io/registry.py`

Centralized reader registry.

Responsibilities:

- connector registration
- connector discovery
- routing logic
- reader prioritization

Example:

```python
registry.register(MyReader())
reader = registry.get_reader(source)
```

---

# `io/sql_reader.py`

SQLAlchemy-based SQL connector support.

Supports:

- SQLite
- PostgreSQL
- MySQL
- Redshift
- Snowflake
- SQLAlchemy-compatible systems

Responsibilities:

- URI parsing
- SQL loading
- driver guidance
- connector validation

---

# `io/duckdb_reader.py`

DuckDB connector implementation.

Responsibilities:

- DuckDB URI parsing
- local database access
- query execution

---

# `io/bigquery_reader.py`

BigQuery connector implementation.

Responsibilities:

- BigQuery URI parsing
- warehouse extraction
- Google authentication support

---

# `io/config_loader.py`

Configuration loading system.

Supports:

- YAML
- TOML
- JSON

Responsibilities:

- config parsing
- validation
- environment interpolation

---

# Reporting System

Directory:

```text
dift/reports/
```

Responsible for all report generation workflows.

---

# `reports/models.py`

Shared report schema models.

Responsibilities:

- structured report representation
- serialization
- report consistency

Acts as:

```text
Central report contract
```

---

# `reports/console_report.py`

Rich CLI rendering.

Responsibilities:

- terminal output
- warning formatting
- risk display
- progress-friendly UX

---

# `reports/json_report.py`

JSON export renderer.

Responsibilities:

- structured serialization
- machine-readable output
- API-friendly workflows

---

# `reports/csv_report.py`

CSV summary report generation.

Responsibilities:

- lightweight export
- summary metrics
- spreadsheet compatibility

---

# `reports/excel_report.py`

Excel workbook generation.

Responsibilities:

- worksheet creation
- formatting
- severity styling
- enterprise reporting

---

# `reports/html_report.py`

HTML dashboard report generation.

Responsibilities:

- HTML rendering
- template handling
- responsive layouts
- visual summaries

Supported templates:

- default
- clean
- compact
- enterprise
- dark

---

# Utilities

Directory:

```text
dift/utils/
```

Contains shared utility helpers.

Examples:

- formatting
- validation helpers
- filesystem helpers
- reusable logic

---

# Tests

Directory:

```text
tests/
```

Testing areas include:

- CLI behavior
- report generation
- connector routing
- warehouse mocking
- validation workflows
- regression coverage

---

# Examples

Directory:

```text
examples/
```

Contains:

- sample datasets
- example configs
- drift examples
- automation examples

Useful for:

- documentation
- onboarding
- regression testing

---

# Current Reader Architecture

Current architecture:

```text
CLI
  ↓
Registry
  ↓
Reader
  ↓
Polars DataFrame
  ↓
Comparison Engine
  ↓
Report System
```

---

# Current Report Pipeline

Current reporting flow:

```text
Comparison Engine
  ↓
Report Models
  ↓
Renderer
  ↓
Output File
```

---

# Technology Stack

Core technologies:

| Technology | Purpose |
|---|---|
| Python | Core language |
| Polars | DataFrame engine |
| Typer | CLI framework |
| Rich | Terminal rendering |
| SQLAlchemy | SQL connectors |
| DuckDB | Local analytics engine |
| pytest | Testing |
| openpyxl | Excel export |

---

# Design Principles

The Dift codebase prioritizes:

- modularity
- readability
- extensibility
- low coupling
- reusable abstractions
- automation readiness
- plugin preparation

---

# Plugin Preparation

Future plugin goals include:

```text
dift/plugins/
├── snowflake/
├── databricks/
├── kafka/
├── s3/
└── spark/
```

Current preparation includes:

- registry abstraction
- reader isolation
- shared interfaces
- optional connector loading

---

# Architectural Strengths

Current architecture enables:

- connector scalability
- report extensibility
- reusable validation
- future plugin support
- warehouse expansion
- enterprise workflows

---

# Contributor Recommendations

New contributors should begin by exploring:

1. `cli.py`
2. `core/comparator.py`
3. `io/readers.py`
4. `reports/models.py`

These files provide the best understanding of Dift’s internal flow.

---

# Recommended Development Workflow

```bash
pytest
ruff check .
mypy dift
```

---

# Future Areas of Expansion

Planned future architecture areas:

- external plugins
- streaming validation
- distributed execution
- cloud-native workflows
- API services
- orchestration integrations

---

# Related Developer Docs

See also:

- architecture.md
- reader-registry.md
- plugin-preparation.md
- report-system.md
- testing.md