# Thresholds

Dift supports configurable drift thresholds for controlling comparison sensitivity.

Thresholds help teams:

- detect subtle drift
- reduce noisy alerts
- standardize validation rules
- customize risk policies
- enforce production quality standards

---

# Why Thresholds Matter

Not every dataset change is equally important.

For example:

- a 1% revenue shift may be critical
- a 10% marketing category shift may be acceptable
- outlier spikes may require aggressive detection

Thresholds help Dift determine:

- when drift becomes risky
- how severe changes are
- whether alerts should be raised

---

# Default Threshold

Dift uses a default numeric drift threshold of:

```text
0.1
```

This means:

- drift above 10% is considered significant
- lower values increase sensitivity
- higher values reduce sensitivity

---

# CLI Threshold Usage

Override the threshold directly from the CLI.

---

## Example

```bash
dift old.csv new.csv \
  --key customer_id \
  --threshold 0.2
```

This increases the drift threshold to 20%.

---

# Lower Threshold Example

```bash
dift old.csv new.csv \
  --threshold 0.03
```

Useful for:

- ML features
- financial metrics
- sensitive production datasets

---

# Threshold Types

Dift supports multiple threshold categories.

| Threshold Type | Purpose |
|---|---|
| numeric | Numeric drift detection |
| categorical | Frequency distribution shifts |
| outlier | Outlier spike detection |
| columns | Column-specific overrides |

---

# Threshold Configuration Files

Thresholds can be stored in reusable configuration files.

---

# Global Threshold Example

```yaml
thresholds:
  numeric: 0.1
  categorical: 0.2
  outlier: 0.15
```

---

# Column-Level Threshold Overrides

Customize thresholds for specific columns.

---

## Example

```yaml
thresholds:
  numeric: 0.1
  categorical: 0.2
  outlier: 0.15

  columns:
    revenue:
      numeric: 0.03

    transactions:
      outlier: 0.05

    segment:
      categorical: 0.4
```

---

# Example Use Cases

---

## Sensitive Revenue Monitoring

```yaml
columns:
  revenue:
    numeric: 0.02
```

Detect even small revenue shifts.

---

## Strict Outlier Detection

```yaml
columns:
  transactions:
    outlier: 0.03
```

Aggressively detect abnormal spikes.

---

## Relaxed Categorical Drift

```yaml
columns:
  segment:
    categorical: 0.4
```

Reduce alerts for naturally variable categories.

---

# Full Threshold Configuration Example

```yaml
old_dataset: examples/old.csv
new_dataset: examples/new.csv

key: customer_id

report: html
output: reports/report.html

thresholds:
  numeric: 0.1
  categorical: 0.2
  outlier: 0.15

  columns:
    revenue:
      numeric: 0.05
      outlier: 0.1

    segment:
      categorical: 0.3
```

Run:

```bash
dift --config config_thresholds.yaml
```

---

# CLI Override Behavior

CLI thresholds override global numeric thresholds.

---

## Example

```bash
dift --config config_thresholds.yaml --threshold 0.5
```

This overrides:

```yaml
thresholds:
  numeric: 0.1
```

But preserves:

- categorical thresholds
- outlier thresholds
- column-level overrides

---

# Numeric Drift Thresholds

Numeric thresholds affect:

- mean shift detection
- standard deviation drift
- range shifts
- statistical variation

---

# Categorical Thresholds

Categorical thresholds affect:

- frequency shifts
- category instability
- new value detection
- removed value detection

---

# Outlier Thresholds

Outlier thresholds affect:

- IQR outlier spikes
- anomaly growth
- abnormal distributions
- extreme value monitoring

---

# Threshold Severity

Dift uses thresholds to classify severity levels.

| Severity | Description |
|---|---|
| low | Minor drift |
| medium | Moderate drift |
| high | Significant drift |

---

# Thresholds and Risk Scoring

Thresholds directly influence:

- overall risk classification
- warning generation
- strict exit codes
- automation workflows

---

# Example Drift Sensitivity

---

## Conservative Detection

```yaml
thresholds:
  numeric: 0.02
```

Detects small changes aggressively.

Useful for:

- finance
- ML features
- regulated datasets

---

## Relaxed Detection

```yaml
thresholds:
  numeric: 0.3
```

Reduces alert noise.

Useful for:

- exploratory analytics
- unstable datasets
- low-risk environments

---

# Production Recommendations

Recommended production thresholds:

| Workflow | Suggested Threshold |
|---|---|
| Financial data | 0.01 - 0.05 |
| ML features | 0.03 - 0.1 |
| ETL pipelines | 0.05 - 0.15 |
| Marketing analytics | 0.15 - 0.3 |

---

# Team Standardization

Threshold configs help teams:

- standardize policies
- reuse validation rules
- reduce alert inconsistency
- simplify CI/CD validation
- enforce governance

---

# Automation Workflows

Thresholds integrate with:

- profiles
- batch comparisons
- scheduled comparisons
- history tracking
- strict exit codes

---

# Example CI/CD Workflow

```bash
dift prod.csv staging.csv \
  --config production_thresholds.yaml \
  --strict-exit-codes
```

---

# Common Validation Patterns

---

## ML Dataset Monitoring

```yaml
thresholds:
  numeric: 0.03
```

---

## ETL Drift Monitoring

```yaml
thresholds:
  numeric: 0.1
  outlier: 0.1
```

---

## Production Governance

```yaml
thresholds:
  numeric: 0.02
  categorical: 0.05
```

---

# Validation Errors

Dift provides clear threshold validation errors.

Example:

```text
Error: Invalid numeric threshold value.
Thresholds must be between 0 and 1.
```

---

# Best Practices

Recommended practices:

- version-control threshold configs
- separate thresholds by environment
- use stricter thresholds in production
- apply column overrides carefully
- tune thresholds gradually
- monitor alert frequency

---

# Next Steps

Continue with:

- Profiles
- Batch Comparisons
- History
- Scheduling
- Automation
- Reports
- Connectors