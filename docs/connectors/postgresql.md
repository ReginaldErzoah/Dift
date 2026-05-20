# PostgreSQL Support

Dift supports direct dataset comparison using PostgreSQL databases.

PostgreSQL workflows enable:

- production vs staging validation
- ETL verification
- warehouse trust checks
- query-based comparison workflows
- analytical regression testing
- automated data validation pipelines

---

# PostgreSQL URI Format

Dift supports PostgreSQL connection strings in the following format:

```text
postgresql://user:password@host:5432/database:table_name
```

Example:

```text
postgresql://admin:secret@localhost:5432/sales_db:customers
```

---

# Basic Comparison Example

```bash
dift postgresql://user:password@localhost:5432/sales_db:customers_old \
     postgresql://user:password@localhost:5432/sales_db:customers_new \
     --key customer_id
```

---

# Alternative Driver Support

Dift also supports modern PostgreSQL SQLAlchemy drivers.

Example:

```text
postgresql+psycopg://user:password@localhost:5432/database:table
```

---

# Install PostgreSQL Driver

## psycopg2

```bash
pip install psycopg2-binary
```

---

## psycopg (modern)

```bash
pip install psycopg
```

---

# Install Core SQL Support

```bash
pip install sqlalchemy
```

---

# Supported Features

PostgreSQL datasets support:

- schema comparison
- row comparison
- drift detection
- risk scoring
- batch workflows
- comparison history
- scheduled workflows
- report generation

---

# Supported Reports

PostgreSQL workflows support:

- console reports
- JSON reports
- CSV reports
- Excel reports
- HTML reports

---

# Example Report Workflow

```bash
dift postgresql://user:password@localhost:5432/sales_db:orders_old \
     postgresql://user:password@localhost:5432/sales_db:orders_new \
     --key order_id \
     --report html \
     --output report.html
```

---

# PostgreSQL Workflow Architecture

Internal workflow:

```text
PostgreSQL
  ↓
SQLAlchemy
  ↓
Polars DataFrame
  ↓
Dift Comparison Engine
```

---

# Progress Indicators

Large PostgreSQL workflows display lightweight progress feedback during:

- connection initialization
- table extraction
- dataset loading
- comparison execution
- report generation

---

# Example Use Cases

## Production Validation

```bash
dift postgresql://prod-db:5432/customers \
     postgresql://staging-db:5432/customers
```

---

## ETL Regression Testing

```bash
dift postgresql://warehouse_before:orders \
     postgresql://warehouse_after:orders
```

---

## Analytics Validation

```bash
dift postgresql://analytics:v1_metrics \
     postgresql://analytics:v2_metrics
```

---

# Authentication

Authentication is handled directly through PostgreSQL credentials provided in the connection string.

Example:

```text
postgresql://username:password@host:5432/database:table
```

---

# Security Notes

Recommendations:

- avoid committing credentials
- prefer environment variables
- use secrets management systems in production
- use least-privilege database accounts

---

# Environment Variable Example

```bash
export DB_URL="postgresql://user:password@localhost:5432/sales_db"
```

Then:

```bash
dift ${DB_URL}:customers_old \
     ${DB_URL}:customers_new
```

---

# Error Handling

Dift provides PostgreSQL-aware validation errors for:

- missing drivers
- invalid connection strings
- authentication failures
- missing tables
- connection timeouts
- unavailable servers

---

# Notes

- PostgreSQL support is powered by SQLAlchemy.
- Datasets are loaded into Polars DataFrames before comparison.
- Comparisons use the standard Dift comparison engine and reporting workflows.

---

# Related Documentation

- sql.md
- mysql.md
- sqlite.md
- redshift.md
- snowflake.md
- ../automation.md
- ../configuration.md