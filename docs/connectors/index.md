# Connectors

Dift supports dataset comparison across local files, SQL databases, analytical warehouses, and future extensible connector systems.

This section documents all officially supported connectors and warehouse integrations.

---

# Supported Connector Types

## Local File Connectors

Dift supports:

- CSV
- Parquet
- Excel (`.xlsx`, `.xls`)
- JSON

These are loaded directly into Polars DataFrames before comparison.

---

## SQL Database Connectors

Dift currently supports:

- SQLite
- PostgreSQL
- MySQL

SQL support is powered by:

- SQLAlchemy
- Polars database integration

---

## Analytical Warehouse Connectors

Dift supports:

- DuckDB
- BigQuery
- Redshift
- Snowflake

These connectors enable warehouse validation and analytical comparison workflows.

---

# Connector Architecture

Dift uses a modular connector architecture built around:

- shared reader interfaces
- centralized reader registry
- connector isolation
- plugin preparation systems

This architecture enables future extensibility and third-party connector support.

---

# Connector Routing

Dataset sources are automatically routed using the centralized reader registry.

Example:

```text
postgresql://user:password@localhost:5432/db:customers
```

automatically resolves to:

```text
SQLReader
```

---

# Connector Workflow

Internal loading flow:

```text
CLI
  ↓
Reader Registry
  ↓
Connector Reader
  ↓
Polars DataFrame
  ↓
Comparison Engine
```

---

# Shared Connector Features

All connectors integrate with:

- schema comparison
- row comparison
- drift detection
- risk scoring
- report generation
- automation workflows
- history tracking

---

# Supported Report Formats

Connectors support:

- console reports
- JSON reports
- CSV reports
- Excel reports
- HTML reports

---

# Progress Indicators

Long-running connector workflows provide lightweight progress feedback.

Progress visibility includes:

- dataset loading
- warehouse extraction
- query execution
- comparison execution
- report generation

---

# Authentication & Security

Authentication depends on connector type.

Examples:

| Connector | Authentication |
|---|---|
| SQLite | Local file access |
| PostgreSQL | Username/password |
| MySQL | Username/password |
| BigQuery | Google service account |
| Snowflake | Warehouse credentials |
| Redshift | Warehouse credentials |

---

# Connector Documentation

## SQL Connectors

- [SQL Overview](sql.md)
- [SQLite](sqlite.md)
- [PostgreSQL](postgresql.md)
- [MySQL](mysql.md)

---

## Warehouse Connectors

- [DuckDB](duckdb.md)
- [BigQuery](bigquery.md)
- [Redshift](redshift.md)
- [Snowflake](snowflake.md)

---

# Future Connector Goals

Planned future connectors may include:

- MongoDB
- Databricks
- Spark
- Kafka
- S3
- Delta Lake
- Iceberg

---

# Plugin Architecture Preparation

Dift is being internally prepared for future plugin-based connector ecosystems.

Future goals include:

- third-party connectors
- optional enterprise connectors
- community-maintained integrations
- plugin registries

---

# Related Documentation

See also:

- ../configuration.md
- ../automation.md
- ../examples.md
- ../developer/architecture.md
- ../developer/plugin-preparation.md
- ../developer/reader-registry.md