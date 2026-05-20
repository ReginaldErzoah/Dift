# BigQuery Support

Dift supports direct dataset comparison using Google BigQuery.

BigQuery workflows enable:

- cloud warehouse validation
- analytical regression testing
- production data quality checks
- large-scale comparison workflows
- scheduled warehouse monitoring
- enterprise trust validation

---

# BigQuery URI Format

Dift uses the following BigQuery URI format:

```text
bigquery://project.dataset.table
```

Example:

```text
bigquery://acme-analytics.sales.orders
```

---

# Basic Comparison Example

```bash
dift bigquery://analytics.sales.customers_old \
     bigquery://analytics.sales.customers_new \
     --key customer_id
```

---

# Generate HTML Report

```bash
dift bigquery://analytics.sales.orders_old \
     bigquery://analytics.sales.orders_new \
     --key order_id \
     --report html \
     --output report.html
```

---

# Generate JSON Report

```bash
dift bigquery://analytics.sales.customers_old \
     bigquery://analytics.sales.customers_new \
     --key customer_id \
     --report json \
     --output report.json
```

---

# Install Dependencies

Install BigQuery support:

```bash
pip install google-cloud-bigquery db-dtypes
```

---

# Authentication

Dift uses standard Google Cloud authentication.

Set your Google service account credentials:

---

## Linux / macOS

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
```

---

## Windows Git Bash

```bash
export GOOGLE_APPLICATION_CREDENTIALS="C:/path/to/service-account.json"
```

---

## PowerShell

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\service-account.json"
```

---

# Supported Features

BigQuery datasets support:

- schema comparison
- row comparison
- drift detection
- null analysis
- duplicate analysis
- risk scoring
- batch workflows
- comparison history
- scheduled workflows

---

# Report Support

BigQuery workflows support:

- console reports
- JSON reports
- CSV reports
- Excel reports
- HTML reports

---

# Internal Workflow

BigQuery datasets follow this workflow:

```text
BigQuery
  ↓
Google BigQuery Client
  ↓
Polars DataFrame
  ↓
Dift Comparison Engine
```

---

# Progress Indicators

Large BigQuery workflows provide lightweight progress feedback during:

- authentication
- query execution
- dataset extraction
- comparison execution
- report generation

---

# Example Use Cases

## Production Warehouse Validation

```bash
dift bigquery://prod.sales.orders \
     bigquery://candidate.sales.orders
```

---

## ETL Regression Testing

```bash
dift bigquery://warehouse.v1.metrics \
     bigquery://warehouse.v2.metrics
```

---

## Analytics Quality Checks

```bash
dift bigquery://analytics.daily.customers_old \
     bigquery://analytics.daily.customers_new
```

---

# Security Recommendations

Recommended production practices:

- use dedicated service accounts
- avoid committing credentials
- use environment variables
- use least-privilege permissions
- restrict dataset access

---

# Environment Variable Example

```bash
export BQ_OLD="bigquery://analytics.sales.orders_old"
export BQ_NEW="bigquery://analytics.sales.orders_new"
```

Then:

```bash
dift $BQ_OLD $BQ_NEW --key order_id
```

---

# Error Handling

Dift provides BigQuery-aware validation errors for:

- missing BigQuery dependencies
- invalid BigQuery URIs
- authentication failures
- missing datasets
- missing tables
- query execution failures

---

# Notes

- BigQuery access requires valid Google Cloud credentials.
- BigQuery billing and permissions are managed through Google Cloud.
- Datasets are loaded into Polars DataFrames before comparison.
- Comparisons use the standard Dift comparison engine and reporting workflows.
- Performance depends on dataset size and warehouse query execution time.

---

# Related Documentation

- sql.md
- duckdb.md
- redshift.md
- snowflake.md
- ../automation.md
- ../configuration.md