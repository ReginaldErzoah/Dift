# Snowflake Support

Dift supports direct dataset comparison from Snowflake warehouses.

Snowflake workflows enable:

- warehouse trust validation
- production analytics QA
- ETL verification
- large-scale dataset comparison
- scheduled warehouse monitoring
- enterprise validation workflows

---

# Snowflake URI Format

Dift supports Snowflake connection strings in the following format:

```text
snowflake://user:password@account/database/schema?warehouse=name:table_name
```

Example:

```text
snowflake://admin:secret@acme-prod/sales/public?warehouse=compute_wh:orders
```

---

# Install Dependencies

Install Snowflake support:

```bash
pip install snowflake-sqlalchemy
```

---

# Install Core SQL Support

```bash
pip install sqlalchemy
```

---

# Basic Comparison Example

```bash
dift snowflake://user:password@account/db/schema?warehouse=compute_wh:orders_old \
     snowflake://user:password@account/db/schema?warehouse=compute_wh:orders_new \
     --key order_id
```

---

# Generate HTML Report

```bash
dift snowflake://user:password@account/db/schema?warehouse=compute_wh:customers_old \
     snowflake://user:password@account/db/schema?warehouse=compute_wh:customers_new \
     --key customer_id \
     --report html \
     --output report.html
```

---

# Generate JSON Report

```bash
dift snowflake://user:password@account/db/schema?warehouse=compute_wh:orders_old \
     snowflake://user:password@account/db/schema?warehouse=compute_wh:orders_new \
     --key order_id \
     --report json \
     --output report.json
```

---

# Supported Features

Snowflake datasets support:

- schema comparison
- row comparison
- drift detection
- null analysis
- duplicate analysis
- risk scoring
- comparison history
- scheduled workflows
- automation workflows

---

# Report Support

Snowflake workflows support:

- console reports
- JSON reports
- CSV reports
- Excel reports
- HTML reports

---

# Internal Workflow

Snowflake datasets follow this workflow:

```text
Snowflake Warehouse
  ↓
SQLAlchemy
  ↓
Polars DataFrame
  ↓
Dift Comparison Engine
```

---

# Progress Indicators

Large Snowflake workflows provide lightweight progress feedback during:

- warehouse authentication
- query execution
- dataset extraction
- comparison execution
- report generation

---

# Example Use Cases

## Warehouse Validation

```bash
dift snowflake://warehouse_before:orders \
     snowflake://warehouse_after:orders
```

---

## Production vs Candidate Comparison

```bash
dift snowflake://prod/customers \
     snowflake://candidate/customers
```

---

## ETL Verification

```bash
dift snowflake://analytics:v1_metrics \
     snowflake://analytics:v2_metrics
```

---

# Authentication

Authentication is handled through Snowflake credentials in the connection string.

Example:

```text
snowflake://username:password@account/database/schema?warehouse=name:table
```

---

# Security Recommendations

Recommended production practices:

- avoid hardcoded credentials
- use environment variables
- use Snowflake role-based access control
- use least-privilege warehouse accounts
- rotate credentials regularly

---

# Environment Variable Example

```bash
export SNOWFLAKE_DB="snowflake://user:password@account/db/schema?warehouse=compute_wh"
```

Then:

```bash
dift ${SNOWFLAKE_DB}:orders_old \
     ${SNOWFLAKE_DB}:orders_new
```

---

# Error Handling

Dift provides Snowflake-aware validation errors for:

- missing drivers
- invalid connection strings
- authentication failures
- warehouse connectivity issues
- missing tables
- query execution failures

---

# Notes

- Snowflake support is powered by SQLAlchemy.
- Datasets are loaded into Polars DataFrames before comparison.
- Comparisons use the standard Dift comparison engine and reporting workflows.
- Performance depends on warehouse size and query complexity.

---

# Related Documentation

- sql.md
- redshift.md
- bigquery.md
- duckdb.md
- ../automation.md
- ../configuration.md