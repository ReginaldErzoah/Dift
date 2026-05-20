# DuckDB Support

Dift supports direct dataset comparison using DuckDB databases.

DuckDB workflows are ideal for:

- analytical data validation
- local warehouse workflows
- Parquet-based analytics
- embedded analytics systems
- fast local comparison pipelines
- reproducible warehouse testing

---

# DuckDB URI Format

Dift uses the following DuckDB URI format:

```text
duckdb:///path/to/database.duckdb:table_name
```

Example:

```text
duckdb:///examples/warehouse.duckdb:orders
```

---

# Basic Comparison Example

```bash
dift duckdb:///examples/warehouse.duckdb:customers_old \
     duckdb:///examples/warehouse.duckdb:customers_new \
     --key customer_id
```

---

# Generate HTML Report

```bash
dift duckdb:///examples/warehouse.duckdb:orders_old \
     duckdb:///examples/warehouse.duckdb:orders_new \
     --key order_id \
     --report html \
     --output report.html
```

---

# Generate JSON Report

```bash
dift duckdb:///examples/warehouse.duckdb:customers_old \
     duckdb:///examples/warehouse.duckdb:customers_new \
     --key customer_id \
     --report json \
     --output report.json
```

---

# Install DuckDB Support

Install DuckDB integration:

```bash
pip install duckdb
```

---

# Supported Features

DuckDB datasets support:

- schema comparison
- row comparison
- drift detection
- null analysis
- duplicate analysis
- risk scoring
- batch workflows
- scheduled workflows
- comparison history

---

# Report Support

DuckDB workflows support:

- console reports
- JSON reports
- CSV reports
- Excel reports
- HTML reports

---

# Internal Workflow

DuckDB datasets follow this workflow:

```text
DuckDB Database
  ↓
DuckDB Reader
  ↓
Polars DataFrame
  ↓
Dift Comparison Engine
```

---

# Analytical Workflow Support

DuckDB is especially useful for:

- Parquet validation
- local warehouse analytics
- ETL testing
- analytics regression testing
- embedded analytical systems
- lightweight warehouse workflows

---

# Example Use Cases

## Parquet Validation

```bash
dift duckdb:///warehouse.duckdb:daily_orders_v1 \
     duckdb:///warehouse.duckdb:daily_orders_v2
```

---

## Analytics Regression Testing

```bash
dift duckdb:///analytics.duckdb:metrics_old \
     duckdb:///analytics.duckdb:metrics_new
```

---

## Warehouse Snapshot Validation

```bash
dift duckdb:///snapshots.duckdb:customers_before \
     duckdb:///snapshots.duckdb:customers_after
```

---

# Progress Indicators

Large DuckDB workflows display lightweight progress feedback during:

- dataset loading
- query execution
- comparison execution
- drift analysis
- report generation

---

# Error Handling

Dift provides DuckDB-aware validation errors for:

- missing DuckDB package
- missing database files
- invalid table names
- invalid DuckDB URIs
- query execution failures

---

# Notes

- DuckDB database files must exist locally.
- Remote DuckDB connections are not currently supported.
- Datasets are loaded into Polars DataFrames before comparison.
- Comparisons use the standard Dift comparison engine and reporting workflows.
- DuckDB workflows are optimized for analytical and local warehouse use cases.

---

# Related Documentation

- sql.md
- bigquery.md
- redshift.md
- snowflake.md
- ../automation.md
- ../examples.md