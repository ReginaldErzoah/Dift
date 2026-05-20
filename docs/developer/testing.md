# Testing

This document explains the testing philosophy, testing architecture, and recommended testing workflows used in Dift.

Testing is a critical part of Dift because the project focuses on:

- data trust validation
- regression detection
- automation workflows
- connector reliability
- report consistency

Dift aims to maintain predictable and stable behavior across all supported workflows.

---

# Testing Goals

The Dift testing strategy focuses on:

- preventing regressions
- validating comparison correctness
- ensuring connector reliability
- maintaining report consistency
- validating CLI workflows
- protecting automation behavior
- enabling safe refactoring

---

# Testing Philosophy

Dift emphasizes:

- readable tests
- isolated failures
- realistic workflows
- automation-safe validation
- actionable failure output

Tests should behave like real user workflows whenever possible.

---

# Test Directory Structure

```text
tests/
├── test_cli.py
├── test_cli_errors.py
├── test_sql_reader.py
├── test_connector_integration.py
├── test_warehouse_mocking.py
├── test_json_report.py
├── test_excel_report.py
├── test_html_report.py
├── test_batch.py
├── test_history.py
└── ...
```

---

# Core Testing Areas

Dift tests focus on:

| Area | Purpose |
|---|---|
| CLI Tests | User workflow validation |
| Reader Tests | Connector reliability |
| Report Tests | Output consistency |
| Integration Tests | End-to-end workflows |
| Validation Tests | Error clarity |
| Automation Tests | CI/CD compatibility |

---

# Primary Testing Framework

Dift uses:

```text
pytest
```

---

# Running Tests

Run all tests:

```bash
pytest
```

Run a specific file:

```bash
pytest tests/test_cli.py
```

Run a specific test:

```bash
pytest tests/test_cli.py::test_cli_help_runs
```

---

# Test Environment

Typical environment:

```text
Python 3.10+
pytest
```

Dift is tested across multiple workflows including:

- local datasets
- warehouse connectors
- batch comparisons
- report generation
- automation execution

---

# CLI Testing

CLI tests validate:

- argument parsing
- help output
- validation behavior
- automation flags
- report generation
- progress indicators

Example:

```python
result = runner.invoke(compare_app, ["--help"])

assert result.exit_code == 0
```

---

# Subprocess CLI Testing

Some tests use:

```python
subprocess.run(...)
```

This validates:

- real shell behavior
- terminal compatibility
- actual CLI execution

---

# Why Subprocess Testing Matters

Typer runner tests are useful, but subprocess tests validate:

- true command execution
- real environment behavior
- packaging compatibility

---

# Reader Testing

Reader tests validate:

- URI parsing
- routing behavior
- connector validation
- dependency guidance
- error handling

---

# SQL Reader Tests

Examples:

- valid SQL URI parsing
- invalid URI rejection
- missing table handling
- dependency guidance
- query execution

---

# Warehouse Mock Testing

Warehouse tests use mocking to avoid:

- real cloud credentials
- billing costs
- external dependencies

Examples:

- BigQuery
- Snowflake
- Redshift

---

# Why Warehouse Mocking Matters

Warehouse mocking enables:

- deterministic tests
- fast execution
- offline development
- reproducible behavior

---

# Validation Testing

Validation tests ensure errors remain:

- actionable
- readable
- consistent

Examples:

- missing dataset guidance
- invalid URI guidance
- unsupported format guidance
- dependency installation hints

---

# Example Validation Test

```python
assert "Supported local file types" in combined_output
```

---

# Report Testing

Report tests validate:

- serialization consistency
- output generation
- schema stability
- file creation

---

# JSON Report Testing

JSON report tests are especially important because JSON outputs are often consumed by:

- CI/CD systems
- APIs
- automation workflows
- downstream tooling

---

# JSON Regression Protection

Tests verify:

- required fields exist
- deprecated fields remain absent
- schema stability is preserved

Example:

```python
assert "metadata" in report
assert "summary" in report
```

---

# Excel Report Testing

Excel tests validate:

- workbook generation
- worksheet structure
- formatting consistency

---

# HTML Report Testing

HTML tests validate:

- template rendering
- report creation
- dashboard structure

---

# Batch Workflow Testing

Batch tests validate:

- directory traversal
- dataset matching
- partial failure handling
- report generation

---

# History System Testing

History tests validate:

- history persistence
- JSONL writing
- listing behavior
- cleanup workflows

---

# Automation Workflow Testing

Automation-focused tests validate:

- strict exit codes
- quiet mode
- no-color mode
- cron generation
- scheduled execution

---

# Progress Indicator Testing

Progress testing ensures:

- output remains readable
- automation workflows stay stable
- progress output does not corrupt reports

---

# Connector Integration Testing

Integration tests validate:

- reader routing
- registry behavior
- connector compatibility
- shared loading contracts

---

# Registry Testing

Registry tests validate:

- dynamic registration
- reader prioritization
- source routing
- extensibility behavior

---

# Plugin Preparation Testing

Plugin preparation tests validate:

- reader isolation
- shared interfaces
- modular loading behavior

---

# Cross-Format Consistency Testing

Dift aims to ensure all report formats represent the same comparison result.

Tests help validate:

- consistent risk levels
- matching warning counts
- stable summary metrics

---

# Common Test Patterns

---

# Temporary File Testing

Dift frequently uses:

```python
tmp_path
```

Example:

```python
def test_report_generation(tmp_path):
```

Benefits:

- isolated execution
- safe filesystem usage
- reproducible tests

---

# Fixture Usage

Fixtures are used for:

- sample datasets
- temporary databases
- reusable workflows

---

# Example Fixture Workflow

```python
def test_cli(sample_csv_files):
```

---

# Mocking Philosophy

Mocking is primarily used for:

- warehouses
- cloud connectors
- expensive external systems

Dift prefers real execution whenever practical.

---

# Error Message Stability

Dift intentionally tests exact error wording in some cases.

Why?

Because actionable validation UX is considered a core feature.

---

# Performance Philosophy

Tests should remain:

- deterministic
- lightweight
- reproducible

Large-scale benchmarking is intentionally separated from standard CI workflows.

---

# Linting

Run linting:

```bash
ruff check .
```

---

# Type Checking

Run type checks:

```bash
mypy dift
```

---

# Recommended Development Workflow

Before opening a PR:

```bash
pytest
ruff check .
mypy dift
```

---

# Contributor Expectations

Contributors should:

- add tests for new features
- preserve backward compatibility
- avoid breaking automation workflows
- maintain report consistency

---

# Good Test Characteristics

Good tests should be:

- readable
- focused
- deterministic
- isolated
- descriptive

---

# Bad Test Characteristics

Avoid tests that are:

- overly coupled
- flaky
- network-dependent
- environment-specific
- difficult to debug

---

# Regression Prevention Philosophy

Dift heavily values regression prevention because:

- data trust tooling must remain stable
- automation workflows depend on predictable behavior
- connector UX must remain consistent

---

# CI/CD Readiness

The test architecture is designed for:

- GitHub Actions
- Jenkins
- GitLab CI
- Airflow workflows
- scheduled validation pipelines

---

# Future Testing Areas

Planned future testing improvements:

- plugin compatibility testing
- distributed execution testing
- performance benchmarking
- snapshot testing
- visual HTML regression testing

---

# Design Philosophy

The Dift testing architecture prioritizes:

- reliability
- stability
- reproducibility
- maintainability
- automation compatibility

---

# Related Developer Docs

See also:

- architecture.md
- codebase-overview.md
- plugin-preparation.md
- reader-registry.md
- report-system.md