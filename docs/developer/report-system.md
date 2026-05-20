# Report System

This document explains the internal report architecture of Dift, including report models, rendering workflows, export systems, and future extensibility goals.

The reporting system is one of the core pillars of Dift because it transforms raw comparison results into actionable, human-readable, and automation-friendly outputs.

---

# Reporting Goals

The Dift reporting system is designed to provide:

- consistent report structures
- reusable rendering logic
- multiple export formats
- automation-friendly outputs
- human-readable summaries
- enterprise-ready exports
- extensible rendering pipelines

---

# Supported Report Formats

Dift currently supports:

| Format | Purpose |
|---|---|
| Console | Interactive CLI usage |
| JSON | Machine-readable workflows |
| CSV | Lightweight summaries |
| Excel | Enterprise spreadsheet workflows |
| HTML | Visual dashboard reporting |

---

# Report Architecture Overview

```text
Comparison Engine
        ↓
Report Models
        ↓
Renderer
        ↓
Output File
```

---

# Core Report Directory

```text
dift/reports/
├── console_report.py
├── json_report.py
├── csv_report.py
├── excel_report.py
├── html_report.py
└── models.py
```

---

# Report Pipeline

The reporting workflow follows these stages:

1. comparison execution
2. result aggregation
3. report model creation
4. renderer selection
5. report generation
6. output export

---

# Report Models

File:

```text
dift/reports/models.py
```

This file defines the shared internal report schema used by all report formats.

The report model acts as the:

```text
Single source of truth
```

for report structure.

---

# Why Shared Models Matter

Without shared models:

- report formats drift apart
- inconsistent outputs emerge
- features become duplicated
- testing becomes difficult

Shared models ensure:

- consistency
- predictable serialization
- reusable rendering
- easier maintenance

---

# Current Report Structure

Dift reports currently contain:

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

# Metadata Section

The metadata section includes:

- tool name
- version
- execution timestamps
- report type
- runtime information

Example:

```json
{
  "tool": "dift",
  "version": "0.6.0"
}
```

---

# Summary Section

Contains high-level comparison results.

Examples:

- row counts
- risk levels
- warnings
- drift summaries

---

# Schema Section

Contains schema comparison information.

Examples:

- added columns
- removed columns
- datatype changes

---

# Row Section

Contains row-level comparison results.

Examples:

- added rows
- removed rows
- row deltas

---

# Quality Section

Contains dataset quality analysis.

Examples:

- null spikes
- duplicate spikes
- severity changes

---

# Numeric Drift Section

Contains numeric drift analysis.

Examples:

- mean shifts
- standard deviation drift
- range changes

---

# Categorical Drift Section

Contains categorical drift analysis.

Examples:

- new values
- removed values
- frequency distribution shifts

---

# Console Reports

File:

```text
console_report.py
```

Responsibilities:

- Rich terminal rendering
- risk highlighting
- warning summaries
- progress-safe output

---

# Console Report Goals

Console reports prioritize:

- readability
- fast interpretation
- interactive workflows
- lightweight rendering

---

# JSON Reports

File:

```text
json_report.py
```

Responsibilities:

- structured serialization
- machine-readable output
- API compatibility
- automation support

---

# Why JSON Matters

JSON reports are useful for:

- CI/CD
- APIs
- automation
- downstream systems
- integrations

---

# CSV Reports

File:

```text
csv_report.py
```

Responsibilities:

- lightweight summaries
- spreadsheet compatibility
- quick exports

---

# CSV Philosophy

CSV reports intentionally remain simple.

They prioritize:

- portability
- simplicity
- quick inspection

---

# Excel Reports

File:

```text
excel_report.py
```

Responsibilities:

- workbook generation
- worksheet formatting
- severity styling
- enterprise reporting

---

# Excel Workbook Structure

Typical workbook sheets:

```text
Summary
Schema
Rows
Quality
Numeric Drift
Categorical Drift
```

---

# Excel Formatting Features

Current formatting features include:

- styled headers
- column auto-sizing
- severity highlighting
- worksheet organization

---

# HTML Reports

File:

```text
html_report.py
```

Responsibilities:

- dashboard rendering
- template handling
- responsive layouts
- visual summaries

---

# HTML Templates

Supported templates:

- default
- clean
- compact
- enterprise
- dark

---

# Template Philosophy

Templates allow:

- branding flexibility
- enterprise customization
- lightweight visual variation

---

# Report Rendering Flow

Typical rendering process:

```python
report = compare_datasets(...)
render_html_report(report)
```

---

# Report Renderer Independence

Each renderer is isolated.

This allows:

- easier maintenance
- independent testing
- future plugin renderers

---

# Output Directory Support

Reports support:

```bash
--output-dir reports/
```

Benefits:

- cleaner automation
- batch workflows
- generated filenames

---

# Auto-Generated Filenames

Examples:

```text
dift_report.json
dift_report.csv
dift_report.xlsx
dift_report.html
```

---

# Batch Reporting

Batch workflows generate:

- per-dataset reports
- grouped output directories
- reusable report structures

Example:

```text
reports/
├── customers/
├── orders/
└── products/
```

---

# Report Consistency Guarantees

All report formats should:

- represent the same comparison results
- expose the same risk levels
- preserve validation findings

---

# Report Testing Philosophy

Reports are tested for:

- structure consistency
- serialization validity
- format compatibility
- regression protection

---

# JSON Regression Testing

JSON reports are especially important for:

- schema stability
- automation compatibility
- downstream integrations

---

# Report Metadata Expansion

Recent improvements include:

- execution timestamps
- runtime metrics
- source metadata
- threshold metadata

---

# Automation-Friendly Reporting

Dift reports support:

- CI/CD
- scheduled workflows
- machine-readable outputs
- non-interactive execution

---

# Progress Indicator Compatibility

Report generation is designed to work cleanly with:

- progress indicators
- quiet mode
- automation logs

---

# Future Report Goals

Planned future improvements include:

- PDF reports
- Markdown reports
- interactive dashboards
- streaming reports
- API responses
- cloud report publishing

---

# Potential Future Architecture

Future rendering system may evolve toward:

```text
reports/
├── renderers/
├── templates/
├── exporters/
└── plugins/
```

---

# Report Plugin Preparation

The report system is also being prepared for future extensibility.

Potential future plugin renderers:

- Power BI export
- Tableau export
- Slack summaries
- Teams notifications
- cloud dashboards

---

# Design Philosophy

The report architecture prioritizes:

- consistency
- extensibility
- readability
- automation compatibility
- enterprise usability

---

# Related Developer Docs

See also:

- architecture.md
- codebase-overview.md
- plugin-preparation.md
- reader-registry.md
- testing.md