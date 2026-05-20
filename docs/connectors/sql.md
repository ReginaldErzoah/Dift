# SQL Database Support

Dift supports direct comparison of datasets stored in SQL databases using SQLAlchemy-compatible connection strings.

SQL workflows enable:

- database-to-database comparison
- table-to-table validation
- ETL verification
- warehouse quality checks
- production vs staging validation
- automated data trust workflows

---

# Supported SQL Databases

Current SQL connector support includes:

- SQLite
- PostgreSQL
- MySQL
- Redshift
- Snowflake

---

# SQL Workflow Overview

Dift loads SQL datasets into Polars DataFrames before executing comparisons.

Workflow:

```text
Database
  ↓
SQLAlchemy Connection
  ↓
Polars DataFrame
  ↓
Dift Comparison Engine
```

---

# Connection URI Format

Dift uses the following format:

```text
connection_string:table_name
```

Example:

```text
postgresql://user:password@localhost:5432/sales_db:customers
```

---

# Example SQL Workflows

## SQLite

```bash
dift sqlite:///examples/old.db:customers_old \
     sqlite:///examples/new.db:customers_new \
     --key customer_id
```

---

## PostgreSQL

```bash
dift postgresql://user:password@localhost:5432/sales_db:customers_old \
     postgresql://user:password@localhost:5432/sales_db:customers_new \
     --key customer_id
```

---

## MySQL

```bash
dift mysql+pymysql://user:password@localhost:3306/sales_db:customers_old \
     mysql+pymysql://user:password@localhost:3306/sales_db:customers_new \
     --key customer_id
```

---

## Redshift

```bash
dift redshift+redshift_connector://user:password@cluster.region.redshift.amazonaws.com:5439/dev:orders_old \
     redshift+redshift_connector://user:password@cluster.region.redshift.amazonaws.com:5439/dev:orders_new \
     --key order_id
```

---

## Snowflake

```bash
dift snowflake://user:password@account/db/schema?warehouse=compute_wh:orders_old \
     snowflake://user:password@account/db/schema?warehouse=compute_wh:orders_new \
     --key order_id
```

---

# Supported SQL Features

SQL datasets support:

- schema comparison
- row comparison
- drift detection
- risk scoring
- report generation
- automation workflows
- comparison history

---

# Report Support

SQL workflows integrate with:

- console reports
- JSON reports
- CSV reports
- Excel reports
- HTML reports

---

# Progress Indicators

Long-running SQL workflows show lightweight progress feedback for:

- connection initialization
- table loading
- query execution
- comparison execution
- report generation

---

# SQLAlchemy Integration

Dift uses SQLAlchemy for database connectivity.

Install core SQL support:

```bash
pip install sqlalchemy
```

---

# Driver Installation

Database-specific drivers may also be required.

---

## PostgreSQL

```bash
pip install psycopg2-binary
```

Alternative modern driver:

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

# Connector Routing

SQL dataset sources are routed through:

```text
SQLReader
```

using the centralized reader registry architecture.

---

# Error Handling

Dift provides connector-aware validation errors.

Examples include:

- missing drivers
- invalid connection strings
- authentication failures
- missing tables
- unsupported connector formats

---

# Security Notes

Dift does not store credentials.

Authentication is handled directly by:

- SQLAlchemy
- connector drivers
- database authentication systems

---

# Common Use Cases

## ETL Validation

```bash
dift warehouse_before.db:orders \
     warehouse_after.db:orders
```

---

## Production vs Staging

```bash
dift postgresql://prod-db:sales \
     postgresql://staging-db:sales
```

---

## Warehouse Trust Validation

```bash
dift snowflake://warehouse/prod:customers \
     snowflake://warehouse/candidate:customers
```

---

# Related Connector Docs

- sqlite.md
- postgresql.md
- mysql.md
- redshift.md
- snowflake.md
- duckdb.md
- bigquery.md

---

# Related Developer Docs

See also:

- ../developer/architecture.md
- ../developer/reader-registry.md
- ../developer/plugin-preparation.md