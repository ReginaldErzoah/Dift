# Dift Architecture

This document explains the internal architecture of Dift, including the comparison engine, reader system, reporting pipeline, configuration system, and future plugin preparation.

The goal of this document is to help contributors and maintainers understand how Dift is structured internally and how new capabilities can be added safely and consistently.

---

# Architecture Goals

Dift is designed around the following principles:

- modularity
- extensibility
- predictable validation behavior
- reusable comparison workflows
- connector scalability
- automation friendliness
- plugin readiness
- minimal core coupling

---

# High-Level Architecture

```text
                    ┌────────────────────┐
                    │       CLI          │
                    │      cli.py        │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Configuration      │
                    │ Loader & Profiles  │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Dataset Readers    │
                    │ Reader Registry    │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Comparison Engine  │
                    │ core/comparator.py │
                    └─────────┬──────────┘
                              │
             ┌────────────────┼────────────────┐
             ▼                ▼                ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ Schema Diff  │ │ Row Diff     │ │ Quality Diff │
    └──────────────┘ └──────────────┘ └──────────────┘
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                    ┌────────────────────┐
                    │ Drift Analysis     │
                    │ Risk Scoring       │
                    └─────────┬──────────┘
                              ▼
                    ┌────────────────────┐
                    │ Report Generation  │
                    └────────────────────┘
```

---

# Core Components

---

# CLI Layer

File:

```text
dift/cli.py
```

Responsibilities:

- parse CLI arguments
- validate options
- load configuration files
- initialize comparisons
- manage automation flags
- trigger report generation
- handle progress output
- manage exit codes

The CLI layer acts as the orchestration layer for the entire platform.

---

# Configuration System

Key files:

```text
dift/io/config_loader.py
dift/profiles.py
dift/thresholds.py
dift/schedules.py
```

Responsibilities:

- YAML/TOML/JSON parsing
- environment interpolation
- reusable threshold policies
- saved comparison profiles
- scheduling configuration
- configuration precedence resolution

Priority order:

```text
CLI Arguments
→ Profiles
→ Config Files
→ Defaults
```

---

# Dataset Reader System

Key files:

```text
dift/io/readers.py
dift/io/base_reader.py
dift/io/registry.py
```

Responsibilities:

- dataset loading
- connector routing
- URI validation
- connector abstraction
- future plugin preparation

Supported sources:

- CSV
- Parquet
- Excel
- JSON
- DuckDB
- SQL databases
- BigQuery
- warehouses

---

# Reader Registry Architecture

Dift uses a centralized registry architecture.

Example flow:

```python
reader = registry.get_reader(source)
df = reader.read(source)
```

Benefits:

- centralized routing
- modular connectors
- future plugin support
- reduced coupling
- cleaner connector isolation

---

# Base Reader Interface

All readers implement a shared interface:

```python
class BaseReader:
    def can_handle(self, source: str) -> bool:
        ...

    def read(self, source: str):
        ...
```

This standardizes connector behavior across the platform.

---

# Connector Design Philosophy

Connectors are designed to be:

- isolated
- reusable
- independently testable
- plugin-safe
- optionally loadable

This prepares Dift for future ecosystem expansion.

---

# Comparison Engine

Key file:

```text
dift/core/comparator.py
```

Responsibilities:

- coordinate dataset comparison
- aggregate comparison results
- execute diff modules
- calculate risk
- generate unified report models

The comparator acts as the central execution engine.

---

# Schema Comparison

Key file:

```text
dift/core/schema_diff.py
```

Responsibilities:

- added column detection
- removed column detection
- datatype changes
- schema compatibility analysis

---

# Row Comparison

Key file:

```text
dift/core/row_diff.py
```

Responsibilities:

- row additions
- row removals
- key-based matching
- row count deltas

---

# Quality Analysis

Key file:

```text
dift/core/quality_diff.py
```

Responsibilities:

- null spike detection
- duplicate spike detection
- quality degradation analysis

---

# Drift Analysis

Key file:

```text
dift/core/stats_diff.py
```

Responsibilities:

- numeric drift detection
- categorical drift detection
- outlier analysis
- threshold evaluation
- severity classification

---

# Numeric Drift

Numeric analysis includes:

- mean shifts
- standard deviation shifts
- range changes
- configurable thresholds

---

# Categorical Drift

Categorical analysis includes:

- new values
- removed values
- frequency distribution shifts

---

# Outlier Analysis

Outlier analysis uses:

- IQR detection
- outlier percentage tracking
- severity classification

---

# Risk Scoring Engine

Key file:

```text
dift/core/risk.py
```

Responsibilities:

- weighted risk calculation
- severity aggregation
- risk normalization
- final risk classification

Risk levels:

- low
- medium
- high

---

# Reporting System

Key files:

```text
dift/reports/
```

Supported reports:

- console
- json
- csv
- excel
- html

Responsibilities:

- report rendering
- metadata generation
- formatting
- template handling
- export workflows

---

# Report Model Architecture

Key file:

```text
dift/reports/models.py
```

Responsibilities:

- shared report schema
- structured report serialization
- metadata standardization

This ensures consistency across all report formats.

---

# Batch Comparison Engine

Key file:

```text
dift/batch.py
```

Responsibilities:

- multi-dataset execution
- filename matching
- directory traversal
- batch reporting
- partial failure handling

---

# History Tracking

Key file:

```text
dift/history.py
```

Responsibilities:

- historical comparison storage
- trend monitoring
- persistent audit records

Storage format:

```text
JSON Lines (.jsonl)
```

---

# Scheduling System

Key file:

```text
dift/schedules.py
```

Responsibilities:

- reusable schedule definitions
- cron generation
- automation workflows

---

# Automation Features

Dift supports:

- strict exit codes
- quiet mode
- non-interactive execution
- progress indicators
- machine-readable reports

This makes Dift CI/CD friendly.

---

# Progress Indicator System

Progress feedback supports:

- dataset loading
- connector extraction
- comparison execution
- report generation

Design goals:

- lightweight
- non-blocking
- automation-safe

---

# Validation Architecture

Dift emphasizes actionable validation behavior.

Examples:

- unsupported format guidance
- missing dependency hints
- connector troubleshooting
- configuration validation
- invalid URI guidance

---

# Error Handling Philosophy

Errors should be:

- actionable
- consistent
- connector-aware
- beginner-friendly
- automation-friendly

---

# Testing Architecture

Testing areas include:

- CLI behavior
- reader routing
- connector validation
- report generation
- warehouse mocking
- automation workflows
- regression coverage

---

# Plugin Preparation

Dift is being internally prepared for future plugin support.

Future goals:

```text
dift/plugins/
├── snowflake/
├── databricks/
├── s3/
├── kafka/
```

Current preparation includes:

- registry abstraction
- connector isolation
- base interfaces
- modular loading behavior

---

# Current Project Structure

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

# Design Philosophy

Dift prioritizes:

- simplicity
- extensibility
- trust validation
- reproducibility
- automation
- scalability

The architecture is intentionally modular to support future enterprise and community ecosystem growth.

---

# Future Architecture Goals

Planned future areas include:

- external plugin system
- connector marketplace
- streaming validation
- cloud-native execution
- distributed comparison
- interactive dashboards
- API services
- enterprise governance integrations

---

# Related Developer Docs

See also:

- reader-registry.md
- plugin-preparation.md
- testing.md
- report-system.md
- codebase-overview.md