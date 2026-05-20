# Reader Registry System

This document explains Dift’s centralized dataset reader registry architecture, connector routing system, and extensibility model.

The reader registry is a foundational part of Dift’s internal architecture because it enables scalable connector growth while keeping the comparison engine connector-agnostic.

---

# Why the Reader Registry Exists

Earlier versions of Dift handled dataset routing directly inside a single loading workflow.

As connector support expanded, this created several architectural problems:

- connector logic became tightly coupled
- routing logic became difficult to maintain
- validation behavior became duplicated
- adding connectors required core modifications
- plugin preparation became difficult

The reader registry architecture solves these issues by introducing a centralized routing and registration system.

---

# Design Goals

The reader registry system was designed to provide:

- centralized connector routing
- modular dataset readers
- reusable validation workflows
- dynamic reader registration
- future plugin preparation
- connector isolation
- scalable connector architecture

---

# High-Level Architecture

```text
                 ┌────────────────────┐
                 │   CLI / Config     │
                 └─────────┬──────────┘
                           ▼
                 ┌────────────────────┐
                 │  Reader Registry   │
                 └─────────┬──────────┘
                           ▼
        ┌────────────────────────────────────┐
        │              Readers              │
        ├────────────────────────────────────┤
        │ LocalFileReader                   │
        │ DuckDBReader                      │
        │ SQLReader                         │
        │ BigQueryReader                    │
        └────────────────────────────────────┘
                           ▼
                 ┌────────────────────┐
                 │ Polars DataFrame   │
                 └────────────────────┘
```

---

# Core Files

The registry architecture is implemented primarily in:

```text
dift/io/
├── base_reader.py
├── registry.py
├── readers.py
├── sql_reader.py
├── duckdb_reader.py
└── bigquery_reader.py
```

---

# Base Reader Interface

File:

```text
dift/io/base_reader.py
```

All dataset readers implement a shared interface.

Example:

```python
class BaseReader:
    def can_handle(self, source: str) -> bool:
        ...

    def read(self, source: str):
        ...
```

---

# Why a Shared Interface Matters

The shared interface standardizes:

- connector behavior
- routing logic
- dataset loading contracts
- validation expectations

This allows the registry to treat all readers consistently.

---

# Reader Responsibilities

Each reader is responsible for:

- determining whether it supports a source
- validating connector input
- loading datasets
- raising actionable errors

Readers should NOT:

- perform comparisons
- generate reports
- calculate risk
- handle CLI orchestration

---

# Reader Registry

File:

```text
dift/io/registry.py
```

The registry acts as the central connector routing system.

Responsibilities include:

- registering readers
- discovering compatible readers
- prioritizing readers
- centralizing routing logic

---

# Registry Example

Example registration:

```python
registry = ReaderRegistry()

registry.register(LocalFileReader())
registry.register(SQLReader())
registry.register(DuckDBReader())
```

---

# Reader Resolution Example

Example routing workflow:

```python
reader = registry.get_reader(source)
df = reader.read(source)
```

---

# Reader Discovery Flow

Current routing flow:

```text
Source Input
      ↓
Registry Iteration
      ↓
Reader.can_handle()
      ↓
Compatible Reader
      ↓
Reader.read()
```

---

# Current Built-In Readers

Dift currently includes:

| Reader | Purpose |
|---|---|
| LocalFileReader | Local files |
| DuckDBReader | DuckDB databases |
| SQLReader | SQL databases |
| BigQueryReader | BigQuery warehouses |

---

# LocalFileReader

Responsibilities:

- local path validation
- file extension handling
- filesystem checks
- local dataset loading

Supported formats:

- CSV
- Parquet
- Excel
- JSON

---

# DuckDBReader

Responsibilities:

- DuckDB URI parsing
- local database access
- analytical table loading

Example URI:

```text
duckdb:///warehouse.duckdb:customers
```

---

# SQLReader

Responsibilities:

- SQLAlchemy connector integration
- SQL URI parsing
- dependency guidance
- database loading

Supported systems include:

- SQLite
- PostgreSQL
- MySQL
- Redshift
- Snowflake

---

# BigQueryReader

Responsibilities:

- BigQuery URI parsing
- warehouse extraction
- Google Cloud authentication workflows

Example URI:

```text
bigquery://project.dataset.table
```

---

# Unified Dataset Contract

All readers return:

```python
polars.DataFrame
```

This is extremely important because the comparison engine remains completely connector-agnostic.

The comparison engine never needs to understand:

- SQLAlchemy
- DuckDB
- warehouse APIs
- cloud authentication
- connector-specific behavior

---

# Why Connector Isolation Matters

Connector isolation improves:

- maintainability
- testability
- scalability
- plugin preparation
- dependency management

---

# Validation Philosophy

Readers are responsible for actionable validation behavior.

Examples include:

- unsupported format guidance
- invalid URI guidance
- missing dependency guidance
- connector troubleshooting hints

---

# Good Validation Example

```text
PostgreSQL support requires psycopg2.

Install it with:
  pip install psycopg2-binary
```

---

# Poor Validation Example

```text
ValueError: failed
```

---

# Reader Prioritization

Reader registration order matters.

Example:

```python
registry.register(SQLReader())
registry.register(LocalFileReader())
```

Specialized readers should generally be registered before generic readers.

---

# Why Prioritization Exists

Some source patterns may overlap.

Prioritization ensures:

- deterministic routing
- predictable behavior
- extensibility safety

---

# Centralized Routing Benefits

Without a registry:

```text
CLI
 └── Large conditional routing logic
```

With a registry:

```text
CLI
 └── Registry
      └── Readers
```

Benefits include:

- cleaner architecture
- modular connectors
- future scalability

---

# Dynamic Registration

Readers can be registered dynamically.

Example:

```python
registry.register(MyCustomReader())
```

This is foundational for future plugin support.

---

# Current Routing Workflow

Current workflow:

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
```

---

# Future Plugin Preparation

The registry architecture is intentionally designed to support future plugin ecosystems.

Potential future structure:

```text
dift/plugins/
├── databricks/
├── kafka/
├── s3/
├── spark/
└── custom/
```

---

# Future Plugin Workflow

Potential future behavior:

```python
registry.load_plugins()
```

Potential capabilities:

- dynamic plugin discovery
- optional connectors
- third-party integrations
- enterprise extensions

---

# Optional Connector Loading

Future connectors may become separately installable.

Examples:

```bash
pip install dift-snowflake
pip install dift-kafka
```

Benefits:

- reduced dependency bloat
- modular ecosystems
- isolated integrations

---

# Connector Metadata (Future)

Future reader metadata may include:

```python
class ReaderMetadata:
    name: str
    version: str
    supported_sources: list[str]
```

Potential uses:

- capability discovery
- debugging
- plugin inspection
- enterprise tooling

---

# Registry Testing

Registry testing validates:

- reader routing
- prioritization
- extensibility behavior
- connector isolation
- dynamic registration

---

# Error Handling Philosophy

Readers should raise errors that are:

- actionable
- readable
- connector-aware
- beginner-friendly

---

# Design Philosophy

The reader registry architecture prioritizes:

- modularity
- extensibility
- maintainability
- connector scalability
- plugin readiness

---

# Future Goals

Planned future improvements include:

- plugin auto-discovery
- capability inspection
- async loading
- streaming connectors
- remote connector support
- distributed loading

---

# Architectural Benefits

The registry architecture enables:

- scalable connector growth
- cleaner maintenance
- future ecosystem expansion
- enterprise extensibility
- community integrations

---

# Related Developer Docs

See also:

- architecture.md
- plugin-preparation.md
- report-system.md
- testing.md
- codebase-overview.md