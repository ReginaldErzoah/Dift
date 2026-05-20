# SQLite Support

Dift supports dataset comparison directly from SQLite databases.

SQLite workflows are ideal for:

- local ETL validation
- lightweight analytics workflows
- embedded database testing
- reproducible validation environments
- local development comparisons

---

# SQLite URI Format

Dift uses the following SQLite URI format:

```text
sqlite:///path/to/database.db:table_name
```

Example:

```text
sqlite:///examples/customers.db:orders
```

---

# Basic Comparison Example

```bash
dift sqlite:///examples/old.db:customers_old \
     sqlite:///examples/new.db:customers_new \
     --key customer_id
```

---

# Generate HTML Report

```bash
dift sqlite:///examples/old.db:customers_old \
     sqlite:///examples/new.db:customers_new \
     --key customer_id \
     --report html \
     --output report.html
```

---

# Generate JSON Report

```bash
dift sqlite:///examples/old.db:customers_old \
     sqlite:///examples/new.db:customers_new \
     --key customer_id \
     --report json \
     --output report.json
```

---

# Supported Features

SQLite datasets support:

- schema comparison
- row comparison
- drift detection
- null analysis
- duplicate analysis
- risk scoring
- comparison history
- batch workflows
- scheduled workflows

---

# SQLite Workflow

Internal loading flow:

```text
SQLite Database
  ↓
SQLAlchemy
  ↓
Polars DataFrame
  ↓
Dift Comparison Engine
```

---

# Installation

Install SQL support:

```bash
pip install sqlalchemy
```

SQLite itself requires no additional external database server.

---

# Local Database Workflows

SQLite is useful for:

- local testing
- CI workflows
- reproducible examples
- lightweight validation
- temporary comparison databases

---

# Example Use Cases

## ETL Validation

```bash
dift sqlite:///warehouse_before.db:orders \
     sqlite:///warehouse_after.db:orders
```

---

## Development vs Production Snapshot

```bash
dift sqlite:///dev.db:customers \
     sqlite:///prod_snapshot.db:customers
```

---

## Batch Validation Workflow

```bash
dift batch \
  --old-dir snapshots/old \
  --new-dir snapshots/new \
  --report html
```

---

# Progress Indicators

SQLite workflows display lightweight progress feedback during:

- dataset loading
- query execution
- comparison execution
- report generation

---

# Error Handling

Dift provides validation errors for:

- missing SQLite database files
- invalid table names
- invalid connection URIs
- unsupported workflows

---

# Notes

- SQLite database files must exist locally.
- SQLite workflows use SQLAlchemy internally.
- Dift loads SQLite datasets into Polars DataFrames before comparison.
- SQLite comparisons use the same core comparison engine as file-based workflows.

---

# Related Documentation

- sql.md
- postgresql.md
- mysql.md
- ../automation.md
- ../examples.md