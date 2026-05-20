# MySQL Support

Dift supports direct dataset comparison using MySQL databases.

MySQL workflows are useful for:

- ETL validation
- transactional data verification
- production vs staging comparisons
- analytics QA workflows
- automated data trust checks
- scheduled validation pipelines

---

# MySQL URI Format

Dift supports MySQL connection strings in the following format:

```text
mysql+pymysql://user:password@host:3306/database:table_name
```

Example:

```text
mysql+pymysql://admin:secret@localhost:3306/sales_db:customers
```

---

# Install MySQL Driver

Install MySQL support:

```bash
pip install pymysql
```

---

# Install Core SQL Support

```bash
pip install sqlalchemy
```

---

# Basic Comparison Example

```bash
dift mysql+pymysql://user:password@localhost:3306/sales_db:customers_old \
     mysql+pymysql://user:password@localhost:3306/sales_db:customers_new \
     --key customer_id
```

---

# Generate HTML Report

```bash
dift mysql+pymysql://user:password@localhost:3306/sales_db:orders_old \
     mysql+pymysql://user:password@localhost:3306/sales_db:orders_new \
     --key order_id \
     --report html \
     --output report.html
```

---

# Generate JSON Report

```bash
dift mysql+pymysql://user:password@localhost:3306/sales_db:orders_old \
     mysql+pymysql://user:password@localhost:3306/sales_db:orders_new \
     --key order_id \
     --report json \
     --output report.json
```

---

# Supported Features

MySQL datasets support:

- schema comparison
- row comparison
- drift detection
- duplicate analysis
- null analysis
- risk scoring
- comparison history
- batch workflows
- scheduled workflows

---

# Report Support

MySQL workflows support:

- console reports
- JSON reports
- CSV reports
- Excel reports
- HTML reports

---

# Internal Workflow

MySQL datasets follow this loading workflow:

```text
MySQL
  ↓
SQLAlchemy
  ↓
Polars DataFrame
  ↓
Dift Comparison Engine
```

---

# Progress Indicators

Large MySQL workflows provide lightweight progress feedback during:

- connection setup
- table loading
- comparison execution
- drift analysis
- report generation

---

# Example Use Cases

## ETL Validation

```bash
dift mysql+pymysql://warehouse_before:orders \
     mysql+pymysql://warehouse_after:orders
```

---

## Production vs Staging Validation

```bash
dift mysql+pymysql://prod-db:customers \
     mysql+pymysql://staging-db:customers
```

---

## Regression Testing

```bash
dift mysql+pymysql://analytics:v1_metrics \
     mysql+pymysql://analytics:v2_metrics
```

---

# Authentication

Authentication is handled through the MySQL connection string.

Example:

```text
mysql+pymysql://username:password@host:3306/database:table
```

---

# Security Recommendations

Recommended production practices:

- avoid hardcoded credentials
- use environment variables
- use secret management systems
- use restricted database accounts
- prefer TLS-enabled database connections

---

# Environment Variable Example

```bash
export MYSQL_DB="mysql+pymysql://user:password@localhost:3306/sales_db"
```

Then:

```bash
dift ${MYSQL_DB}:customers_old \
     ${MYSQL_DB}:customers_new
```

---

# Error Handling

Dift provides MySQL-aware validation errors for:

- missing drivers
- invalid connection strings
- authentication failures
- unavailable databases
- missing tables
- network connection failures

---

# Notes

- MySQL support is powered by SQLAlchemy.
- Datasets are loaded into Polars DataFrames before comparison.
- Comparisons use the standard Dift comparison engine and reporting system.

---

# Related Documentation

- sql.md
- sqlite.md
- postgresql.md
- redshift.md
- snowflake.md
- ../automation.md
- ../configuration.md