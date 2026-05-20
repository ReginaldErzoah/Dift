# Amazon Redshift Support

Dift supports dataset comparison directly from Amazon Redshift warehouses.

Redshift workflows enable:

- warehouse validation
- analytical regression testing
- ETL verification
- production quality checks
- large-scale dataset comparison
- scheduled warehouse trust workflows

---

# Redshift URI Format

Dift supports Redshift connection strings in the following format:

```text
redshift+redshift_connector://user:password@host:5439/database:table_name
```

Example:

```text
redshift+redshift_connector://admin:secret@cluster.region.redshift.amazonaws.com:5439/dev:orders
```

---

# Install Dependencies

Install Redshift support:

```bash
pip install sqlalchemy-redshift redshift-connector
```

---

# Install Core SQL Support

```bash
pip install sqlalchemy
```

---

# Basic Comparison Example

```bash
dift redshift+redshift_connector://user:password@cluster.region.redshift.amazonaws.com:5439/dev:orders_old \
     redshift+redshift_connector://user:password@cluster.region.redshift.amazonaws.com:5439/dev:orders_new \
     --key order_id
```

---

# Generate HTML Report

```bash
dift redshift+redshift_connector://user:password@cluster.region.redshift.amazonaws.com:5439/dev:customers_old \
     redshift+redshift_connector://user:password@cluster.region.redshift.amazonaws.com:5439/dev:customers_new \
     --key customer_id \
     --report html \
     --output report.html
```

---

# Generate JSON Report

```bash
dift redshift+redshift_connector://user:password@cluster.region.redshift.amazonaws.com:5439/dev:orders_old \
     redshift+redshift_connector://user:password@cluster.region.redshift.amazonaws.com:5439/dev:orders_new \
     --key order_id \
     --report json \
     --output report.json
```

---

# Supported Features

Redshift datasets support:

- schema comparison
- row comparison
- drift detection
- null analysis
- duplicate analysis
- risk scoring
- batch workflows
- comparison history
- scheduled validation

---

# Report Support

Redshift workflows support:

- console reports
- JSON reports
- CSV reports
- Excel reports
- HTML reports

---

# Internal Workflow

Redshift datasets follow this workflow:

```text
Amazon Redshift
  ↓
SQLAlchemy
  ↓
Polars DataFrame
  ↓
Dift Comparison Engine
```

---

# Progress Indicators

Large Redshift workflows provide lightweight progress feedback during:

- warehouse connection
- query execution
- dataset extraction
- comparison execution
- report generation

---

# Example Use Cases

## Warehouse Validation

```bash
dift redshift+redshift_connector://warehouse_before:orders \
     redshift+redshift_connector://warehouse_after:orders
```

---

## Production vs Candidate Comparison

```bash
dift redshift+redshift_connector://prod-cluster:customers \
     redshift+redshift_connector://candidate-cluster:customers
```

---

## ETL Regression Testing

```bash
dift redshift+redshift_connector://analytics:v1_metrics \
     redshift+redshift_connector://analytics:v2_metrics
```

---

# Authentication

Authentication is handled through Redshift credentials in the connection string.

Example:

```text
redshift+redshift_connector://username:password@host:5439/database:table
```

---

# Security Recommendations

Production recommendations:

- avoid committing credentials
- use IAM-based workflows where possible
- use environment variables
- use least-privilege warehouse accounts
- restrict warehouse access

---

# Environment Variable Example

```bash
export REDSHIFT_DB="redshift+redshift_connector://user:password@cluster.region.redshift.amazonaws.com:5439/dev"
```

Then:

```bash
dift ${REDSHIFT_DB}:orders_old \
     ${REDSHIFT_DB}:orders_new
```

---

# Error Handling

Dift provides Redshift-aware validation errors for:

- missing drivers
- invalid connection strings
- authentication failures
- unreachable clusters
- missing tables
- warehouse query failures

---

# Notes

- Redshift support is powered by SQLAlchemy.
- Datasets are loaded into Polars DataFrames before comparison.
- Comparisons use the standard Dift comparison engine and reporting workflows.
- Warehouse extraction performance depends on network and query size.

---

# Related Documentation

- sql.md
- snowflake.md
- bigquery.md
- duckdb.md
- ../automation.md
- ../configuration.md