# Configuration

Dift supports reusable configuration files for cleaner, reproducible, and automation-friendly workflows.

Configuration files help teams:

- reduce repetitive CLI commands
- standardize validation rules
- simplify CI/CD workflows
- manage environments
- reuse comparison settings
- centralize drift policies

---

# Supported Configuration Formats

Dift supports:

- YAML (`.yaml`, `.yml`)
- TOML (`.toml`)
- JSON (`.json`)

---

# Basic Configuration Example

## YAML

```yaml
old_dataset: examples/old.csv
new_dataset: examples/new.csv

key: customer_id

threshold: 0.1

report: html
output: reports/report.html
```

Run:

```bash
dift --config config.yaml
```

---

# TOML Example

```toml
old_dataset = "examples/old.csv"
new_dataset = "examples/new.csv"

key = "customer_id"

threshold = 0.1

report = "json"
output = "reports/report.json"
```

---

# JSON Example

```json
{
  "old_dataset": "examples/old.csv",
  "new_dataset": "examples/new.csv",
  "key": "customer_id",
  "threshold": 0.1,
  "report": "csv",
  "output": "reports/report.csv"
}
```

---

# Dataset Paths in Config Files

Dift can load dataset paths directly from configuration files.

This allows reusable workflows without typing datasets repeatedly.

---

## Example

```yaml
old_dataset: examples/old.csv
new_dataset: examples/new.csv

key: customer_id
report: html
```

Run:

```bash
dift --config config.yaml
```

---

# CLI Override Behavior

CLI arguments override configuration values.

---

## Example

```bash
dift prod.csv staging.csv \
  --config config.yaml \
  --report json \
  --output override.json
```

Dift will use:

- datasets from CLI
- report/output from CLI
- remaining values from config

---

# Configuration Priority

Dift resolves settings using:

```text
CLI Arguments > Profiles > Config Files > Defaults
```

This provides flexibility while keeping workflows reproducible.

---

# Supported Configuration Fields

| Field | Description |
|---|---|
| old_dataset | Original dataset |
| new_dataset | New dataset |
| key | Row matching key |
| threshold | Numeric drift threshold |
| report | Report format |
| output | Report output path |
| output_dir | Output directory |
| template | HTML template |
| history | Enable history tracking |
| history_dir | History directory |
| strict_exit_codes | Risk-based exit codes |
| quiet | Suppress non-error output |
| no_color | Disable terminal colors |

---

# Threshold Configurations

Dift supports reusable threshold policies.

---

## Example

```yaml
thresholds:
  numeric: 0.1
  categorical: 0.2
  outlier: 0.15
```

---

# Column-Level Threshold Overrides

```yaml
thresholds:
  numeric: 0.1

  columns:
    revenue:
      numeric: 0.05

    transactions:
      outlier: 0.03
```

Useful for:

- sensitive metrics
- production monitoring
- anomaly-heavy datasets

---

# Environment-Based Configurations

Dift supports environment-specific workflows.

Useful for:

- development
- staging
- production
- CI/CD pipelines

---

# Example Environment Config

```yaml
key: customer_id
report: html

environments:
  development:
    old_dataset: examples/dev_old.csv
    new_dataset: examples/dev_new.csv
    threshold: 0.2

  staging:
    old_dataset: staging_old.csv
    new_dataset: staging_new.csv
    threshold: 0.15

  production:
    old_dataset: prod_old.csv
    new_dataset: prod_new.csv
    threshold: 0.1
```

---

# Select Environment

```bash
dift --config config_env.yaml --env production
```

---

# Environment Variable Support

Dift supports environment variable interpolation.

---

## Example

```yaml
old_dataset: ${OLD_DATASET}
new_dataset: ${NEW_DATASET}
```

---

# Set Variables

## Linux / macOS

```bash
export OLD_DATASET=data/old.csv
export NEW_DATASET=data/new.csv
```

---

## Windows PowerShell

```powershell
$env:OLD_DATASET="data/old.csv"
$env:NEW_DATASET="data/new.csv"
```

---

# Run

```bash
dift --config config_env.yaml
```

---

# Missing Environment Variables

If a required variable is missing, Dift shows a helpful validation error.

Example:

```text
Error: Missing environment variable 'OLD_DATASET'
```

---

# Output Directory Support

Save reports into directories:

```yaml
report: html
output_dir: reports/
```

Generated filename:

```text
reports/dift_report.html
```

---

# HTML Templates

Specify HTML templates directly inside configs.

---

## Example

```yaml
report: html
template: enterprise
```

Available templates:

- default
- clean
- compact
- enterprise
- dark

---

# History Tracking

Enable persistent comparison history.

---

## Example

```yaml
history: true
history_dir: reports/history
```

---

# Strict Exit Codes

Automation-friendly validation:

```yaml
strict_exit_codes: true
```

Exit codes:

| Code | Meaning |
|---|---|
| 0 | Low risk |
| 1 | Medium risk |
| 2 | High risk |
| 3 | Runtime error |

---

# Quiet Mode

Useful for automation workflows.

```yaml
quiet: true
```

---

# Disable Colors

```yaml
no_color: true
```

Useful for:

- CI logs
- plain-text terminals
- log aggregation systems

---

# Example Full Configuration

```yaml
old_dataset: examples/old.csv
new_dataset: examples/new.csv

key: customer_id

report: html
template: enterprise
output: reports/report.html

thresholds:
  numeric: 0.1
  categorical: 0.2
  outlier: 0.15

history: true
history_dir: reports/history

strict_exit_codes: true
quiet: false
no_color: false
```

---

# Example Production Workflow

```yaml
environments:
  production:
    old_dataset: ${PROD_OLD}
    new_dataset: ${PROD_NEW}

    report: json
    output: reports/prod_report.json

    threshold: 0.05

    strict_exit_codes: true
    quiet: true
```

Run:

```bash
dift --config production.yaml --env production
```

---

# Validation Errors

Dift provides actionable validation messages for:

- invalid configs
- missing fields
- unsupported formats
- invalid templates
- missing environment variables
- conflicting options

Example:

```text
Error: Unsupported report format 'xml'
```

---

# Best Practices

Recommended practices:

- store reusable configs in version control
- separate environments clearly
- use profiles for recurring workflows
- use environment variables for secrets
- standardize thresholds across teams
- enable strict exit codes in CI/CD

---

# Common Use Cases

---

## CI/CD Validation

```yaml
report: json
strict_exit_codes: true
quiet: true
```

---

## Executive Reporting

```yaml
report: html
template: enterprise
```

---

## ML Drift Monitoring

```yaml
thresholds:
  numeric: 0.03
```

---

## Historical Monitoring

```yaml
history: true
```

---

# Next Steps

Continue with:

- Thresholds
- Profiles
- Batch Comparisons
- Scheduling
- Automation
- Connectors
- Reports