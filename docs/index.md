# Dift Documentation

<p align="left">
  <img src="https://raw.githubusercontent.com/ReginaldErzoah/Dift/main/assets/dift-logo.png" width="400" alt="Dift Logo">
</p>

Dift is an open-source CLI platform for dataset comparison, drift detection, and data trust validation.

It helps data teams quickly understand:

- what changed
- why it matters
- whether new data is safe to trust

Dift supports:

- local files
- SQL databases
- DuckDB
- BigQuery
- warehouse workflows
- automation pipelines
- batch dataset validation
- reusable comparison profiles
- scheduled comparisons
- drift monitoring workflows

---

# Core Features

## Dataset Comparison

Compare datasets across:

- CSV
- Parquet
- Excel
- JSON
- SQL databases
- DuckDB
- BigQuery
- cloud warehouse workflows

---

## Drift Detection

Dift detects:

- numeric drift
- categorical drift
- frequency shifts
- outlier spikes
- schema changes
- row-level changes
- null spikes
- duplicate spikes

---

## Risk Analysis

Dift converts dataset changes into understandable risk levels:

- low
- medium
- high

This helps teams prioritize risky dataset changes before they impact production systems.

---

# Reporting

Generate reports in multiple formats:

- Console
- JSON
- CSV
- Excel
- HTML

HTML reports support multiple templates:

- default
- clean
- compact
- enterprise
- dark

---

# Automation Workflows

Dift supports:

- CI/CD integration
- scheduled comparisons
- batch comparisons
- reusable profiles
- reusable configs
- comparison history tracking
- strict exit codes
- non-interactive execution

---

# Quick Example

```bash
dift examples/old.csv examples/new.csv --key customer_id
```

Generate an HTML report:

```bash
dift examples/old.csv examples/new.csv \
  --key customer_id \
  --report html \
  --output report.html
```

---

# Documentation Sections

## Getting Started

- Installation
- Quick Start
- Usage Guide

## Core Workflows

- Reports
- Configuration
- Thresholds
- Profiles
- Batch Comparisons
- Scheduling
- Automation

## Connectors

- DuckDB
- SQLite
- PostgreSQL
- MySQL
- Redshift
- Snowflake
- BigQuery

## Developer Documentation

- Architecture
- Reader Registry
- Plugin Preparation
- Testing

## Release Notes

Track feature evolution across Dift versions.

---

# Philosophy

Dift is designed to help teams build trust in data.

The goal is not only to detect changes - but to explain their operational risk clearly and consistently.

---

# Open Source

Dift is fully open source and community-driven.

Contributions are welcome.

GitHub:

```text
https://github.com/ReginaldErzoah/Dift
```