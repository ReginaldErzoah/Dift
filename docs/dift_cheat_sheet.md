# Dift Cheat Sheet

# Overview

Dift is an open-source CLI tool for comparing datasets and detecting:

* schema changes
* row-level changes
* data quality issues
* numeric drift
* categorical drift
* outlier spikes
* dataset risk levels

Dift helps data professionals understand:

* what changed
* why it matters
* whether the new dataset is safe to trust

> Latest version is v.0.5.0
---

# Evolution of Dift

## MVP (Initial Version)

The original version focused on:

* schema comparison
* row comparison
* JSON reporting
* CSV reporting
* console summaries

Example:

```bash id="g92d1f"
dift old.csv new.csv
```

---

## v0.3.0

Added:

* HTML reports
* Excel reports
* `--output-dir`
* improved JSON structure
* better CLI UX

---

## v0.4.0

Added:

* weighted risk scoring
* numeric drift detection
* configurable thresholds
* severity classification
* better quality validation

---

## v0.5.0

Added:

* advanced categorical drift detection
* outlier detection (IQR)
* outlier severity scoring
* categorical frequency shift detection
* improved HTML reports
* improved Excel reports
* expanded CSV metrics
* richer console warnings

---

# Core Command Structure

```bash id="t3k5m2"
dift <old_dataset> <new_dataset> [OPTIONS]
```

## Explanation

* `<old_dataset>` --> original dataset
* `<new_dataset>` --> updated dataset
* `[OPTIONS]` --> optional flags

---

# Basic Usage

```bash id="s8r7qy"
dift old.csv new.csv
```

## What Happens

Dift:

* loads both datasets
* compares schema
* compares rows
* analyzes data quality
* calculates risk level
* outputs results to terminal

---

# Using a Key for Row Comparison

```bash id="z9m4ba"
dift old.csv new.csv --key id
```

## Why This Matters

Without `--key`:

* dataset-level comparison only

With `--key`:

* detects added rows
* detects removed rows
* detects changed rows
* detects unchanged rows

---

# Supported Formats

## Input Formats

* CSV
* Parquet
* Excel (`.xlsx`, `.xls`)
* JSON

## Output Formats

* console
* JSON
* CSV
* Excel
* HTML

---

# Output Reports

## JSON Report

```bash id="m5x8pw"
dift old.csv new.csv --report json --output report.json
```

### Best For

* APIs
* integrations
* automation
* pipelines

### JSON Structure

* metadata
* summary
* schema
* rows
* quality
* numeric
* categorical
* outliers

---

## CSV Report

```bash id="n7v2ke"
dift old.csv new.csv --report csv --output report.csv
```

### Best For

* CI/CD
* pipelines
* lightweight summaries

### Example

```text id="5w1u3n"
metric,value
old_rows,10
new_rows,11
risk_level,medium
```

---

## Excel Report

```bash id="d0q4ta"
dift old.csv new.csv --report excel --output report.xlsx
```

### Best For

* analysts
* business users
* audit workflows

### Worksheets

* Summary
* Quality Diff
* Outlier Diff
* Categorical Diff
* Numeric Diff

---

## HTML Report

```bash id="j8r2lv"
dift old.csv new.csv --report html --output report.html
```

### Best For

* visual analysis
* sharing reports
* dashboards
* presentations

---

# HTML Templates

```bash id="x1n6pe"
dift old.csv new.csv --report html --template clean
```

## Available Templates

* default
* clean
* compact
* enterprise
* dark

---

# Output Directory Support

```bash id="a4p9wm"
dift old.csv new.csv --report json --output-dir reports/
```

## Behavior

* creates directory automatically
* auto-generates filenames

## Example Output

```text id="v7c2ds"
reports/
└── dift_report.json
```

## Important

Do NOT use:

* `--output`
  and
* `--output-dir`

together.

Dift will reject the command.

---

# Numeric Drift Detection

## Example

```bash id="y2q7rt"
dift old.csv new.csv --key id --threshold 0.1
```

## Detects

* mean shifts
* standard deviation drift
* range shifts

---

## Example Warning

```text id="f4w9zu"
Numeric drift:
'revenue'
mean shift 900.00%
(high, threshold 0.1)
```

---

# Configurable Thresholds

```bash id="k6m1hy"
dift old.csv new.csv --threshold 0.2
```

## Default Threshold

```text id="e3u8vk"
0.1
```

Higher threshold:

* less sensitive

Lower threshold:

* more sensitive

---

# Categorical Drift Detection

Dift detects:

* new categories
* removed categories
* frequency distribution shifts

---

## Example Warning

```text id="q9t2cp"
Categorical shift:
'segment'
max frequency shift 60.00%
(high)
```

---

# Outlier Detection

Dift uses:

* IQR outlier detection

to identify sudden spikes in abnormal values.

---

## Example Warning

```text id="h8s5ab"
Outlier spike:
'revenue' increased by 100.00%
(high)
```

---

# Severity Levels

Dift uses:

* low
* medium
* high

severity classifications across:

* numeric drift
* categorical drift
* null spikes
* duplicate spikes
* outlier spikes

---

# Weighted Risk Scoring

Dift calculates overall dataset risk using:

* schema changes
* row changes
* quality issues
* drift analysis
* outlier analysis

---

## Risk Levels

* low
* medium
* high

---

# What Dift Detects

## Schema Changes

* columns added
* columns removed
* type changes

## Row Changes

* added rows
* removed rows
* changed rows
* unchanged rows

## Data Quality Issues

* null spikes
* duplicate spikes

## Drift Detection

* numeric drift
* categorical drift
* frequency shifts

## Statistical Analysis

* outlier spikes
* distribution shifts

---

# Common Errors

## Missing File

```text id="p3z7kr"
Error: File not found
```

---

## Invalid Option Combination

```text id="o5r2xu"
--output and --output-dir cannot be used together
```

---

## Unsupported Format

```text id="i1w9sb"
Unsupported dataset type
```

---

# Best Practices

## Recommended Workflow

* always use a key when possible
* use JSON for integrations
* use CSV for automation
* use Excel for analysis
* use HTML for presentations
* use thresholds for drift monitoring

---

# Good Use Cases

## ETL Validation

```bash id="r6u2ta"
dift before.csv after.csv
```

## ML Dataset Drift

```bash id="w4p8nm"
dift train_v1.csv train_v2.csv --threshold 0.1
```

## Production Validation

```bash id="c7s5yx"
dift prod.csv staging.csv --key id
```

## Silent Drift Detection

```bash id="u2q9kl"
dift yesterday.csv today.csv --threshold 0.05
```

---

# Quick Commands

```bash id="b8n1vd"
dift old.csv new.csv

dift old.csv new.csv --key id

dift old.csv new.csv --report json --output report.json

dift old.csv new.csv --report excel --output report.xlsx

dift old.csv new.csv --report html --template dark

dift old.csv new.csv --report csv --output-dir reports/

dift old_drift.csv new_drift.csv --key id --threshold 0.1
```


# Vision

Dift aims to become the open-source standard for dataset comparison, drift detection, and data trust validation.
