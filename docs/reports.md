# Reports

Dift provides multiple report formats for dataset comparison, drift analysis, validation workflows, and automation pipelines.

Reports help teams:

- understand dataset changes
- identify drift risks
- validate ETL workflows
- monitor production datasets
- share validation results
- automate quality checks

---

# Supported Report Formats

Dift supports:

- Console
- JSON
- CSV
- Excel
- HTML

---

# Console Reports

Console reports are the default output format.

Example:

```bash
dift old.csv new.csv --key customer_id
```

Console reports display:

- schema changes
- row changes
- drift warnings
- outlier spikes
- quality issues
- overall risk level

---

# Example Console Output

```text
╭─────────────────────────╮
│ Dift Dataset Comparison │
│ Risk Level: MEDIUM      │
╰─────────────────────────╯

Warnings

Numeric drift:
'revenue'
mean shift 900.00%
(high, threshold 0.1)

Outlier spike:
'revenue' increased by 100.00%
(high)

Categorical shift:
'segment' max frequency shift 60.00%
(high)
```

---

# JSON Reports

JSON reports are useful for:

- APIs
- CI/CD pipelines
- machine-readable workflows
- downstream automation
- audit systems

---

## Generate JSON Report

```bash
dift old.csv new.csv \
  --key customer_id \
  --report json \
  --output report.json
```

---

## Example Structure

```json
{
  "metadata": {},
  "summary": {},
  "schema": {},
  "rows": {},
  "quality": {},
  "numeric": {},
  "categorical": {}
}
```

---

# CSV Reports

CSV reports provide lightweight summaries for:

- spreadsheets
- dashboards
- quick audits
- ETL monitoring

---

## Generate CSV Report

```bash
dift old.csv new.csv \
  --report csv \
  --output report.csv
```

---

## Example CSV Output

```csv
metric,value
old_rows,1000
new_rows,1100
row_delta,100
risk_level,medium
```

---

# Excel Reports

Excel reports provide structured workbook-based analysis.

Useful for:

- analysts
- audits
- management reviews
- QA workflows

---

## Generate Excel Report

```bash
dift old.csv new.csv \
  --report excel \
  --output report.xlsx
```

---

# Excel Workbook Structure

Typical sheets include:

- Summary
- Schema
- Rows
- Quality
- Numeric Drift
- Categorical Drift

---

# Excel Features

Excel reports support:

- severity color coding
- formatted headers
- readable layouts
- autosized columns
- worksheet separation

---

# HTML Reports

HTML reports provide dashboard-style visualization.

Useful for:

- stakeholders
- audits
- monitoring workflows
- production validation
- presentation-ready reporting

---

## Generate HTML Report

```bash
dift old.csv new.csv \
  --report html \
  --output report.html
```

---

# HTML Templates

Customize HTML appearance using templates.

---

## Example

```bash
dift old.csv new.csv \
  --report html \
  --template dark \
  --output report.html
```

---

# Available Templates

| Template | Description |
|---|---|
| default | Standard layout |
| clean | Minimal clean layout |
| compact | Dense information layout |
| enterprise | Executive dashboard styling |
| dark | Dark mode report |

---

# HTML Features

HTML reports support:

- responsive layouts
- drift highlighting
- severity badges
- visual summaries
- section grouping
- dashboard-style presentation

---

# Output Directory Support

Automatically generate filenames using `--output-dir`.

---

## Example

```bash
dift old.csv new.csv \
  --report html \
  --output-dir reports/
```

---

# Generated Filenames

| Report Type | Filename |
|---|---|
| JSON | dift_report.json |
| CSV | dift_report.csv |
| Excel | dift_report.xlsx |
| HTML | dift_report.html |

---

# Batch Report Generation

Generate reports for multiple dataset comparisons.

---

## Example

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --report html \
  --output-dir reports/
```

---

# Example Batch Structure

```text
reports/
├── customers/
│   └── dift_report.html
├── orders/
│   └── dift_report.html
└── products/
    └── dift_report.html
```

---

# Progress Indicators

Large report generation workflows display progress indicators.

Examples:

- JSON generation
- Excel export
- HTML rendering
- warehouse extraction
- SQL loading

This improves visibility during long-running workflows.

---

# Report Metadata

Reports include metadata such as:

- execution timestamps
- report format
- Dift version
- dataset source metadata
- thresholds used
- runtime information

---

# Risk Levels

Dift classifies comparisons into:

| Risk Level | Meaning |
|---|---|
| low | Safe dataset changes |
| medium | Moderate drift detected |
| high | Significant risk detected |

---

# Drift Reporting

Reports may include:

- numeric drift
- categorical drift
- outlier spikes
- frequency shifts
- null spikes
- duplicate spikes
- schema changes
- row additions/removals

---

# Numeric Drift Reporting

Examples include:

- mean shift
- standard deviation changes
- range drift
- distribution changes

---

# Categorical Drift Reporting

Examples include:

- new values
- removed values
- frequency shifts
- category instability

---

# Outlier Reporting

Outlier analysis includes:

- IQR-based detection
- outlier spike tracking
- severity classification
- risk integration

---

# Automation Workflows

Reports integrate well with:

- GitHub Actions
- Airflow
- Prefect
- Dagster
- Jenkins
- cron jobs
- CI/CD systems

---

# Example CI Workflow

```bash
dift prod.csv staging.csv \
  --report json \
  --output report.json \
  --strict-exit-codes \
  --quiet
```

---

# Recommended Report Formats

| Workflow | Recommended Format |
|---|---|
| CI/CD | JSON |
| Analysts | Excel |
| Dashboards | HTML |
| Lightweight summaries | CSV |
| Interactive review | Console |

---

# Common Use Cases

---

## ETL Validation

```bash
dift before.csv after.csv \
  --report html
```

---

## ML Drift Monitoring

```bash
dift train_v1.csv train_v2.csv \
  --report json
```

---

## Executive Reporting

```bash
dift prod.csv staging.csv \
  --report enterprise
```

---

## Historical Monitoring

```bash
dift prod.csv staging.csv \
  --history \
  --report html
```

---

# Next Steps

Continue with:

- Configuration
- Thresholds
- Profiles
- Batch Comparisons
- Scheduling
- Automation
- Connectors