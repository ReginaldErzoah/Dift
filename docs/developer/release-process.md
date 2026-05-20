# Release Process

This document explains the release workflow, versioning philosophy, packaging process, and maintenance workflow used in Dift.

The goal of the release process is to ensure that Dift releases remain:

- stable
- reproducible
- well-tested
- backward compatible
- automation friendly
- professionally documented

---

# Release Philosophy

Dift follows a release philosophy centered around:

- incremental improvements
- stability-first development
- developer experience
- automation compatibility
- extensibility preparation

Releases should improve the platform without introducing unnecessary breaking changes.

---

# Current Versioning Strategy

Dift currently uses semantic-style versioning:

```text
MAJOR.MINOR.PATCH
```

Example:

```text
0.6.0
```

---

# Version Meaning

| Part | Meaning |
|---|---|
| MAJOR | Significant architectural changes |
| MINOR | New features and improvements |
| PATCH | Bug fixes and small corrections |

---

# Current Development Phase

Dift is currently in the:

```text
0.x.x
```

phase.

This means:

- architecture is still evolving
- features are expanding rapidly
- internal APIs may still evolve

However, stability and backward compatibility are still strongly prioritized.

---

# Typical Release Workflow

The standard release process is:

```text
Feature Development
        ↓
Testing
        ↓
Documentation Updates
        ↓
Version Bump
        ↓
Release Notes
        ↓
Git Tag
        ↓
PyPI Release
        ↓
GitHub Release
```

---

# Step 1 — Feature Development

Features are typically developed through:

- isolated branches
- pull requests
- incremental commits

Recommended branch naming:

```text
feature/add-html-template-system
fix/sql-validation-errors
refactor/reader-registry
```

---

# Step 2 — Run Tests

Before releasing:

```bash
pytest
```

All tests should pass successfully.

---

# Step 3 — Run Linting

Run lint checks:

```bash
ruff check .
```

---

# Step 4 — Run Type Checking

Run static typing checks:

```bash
mypy dift
```

---

# Step 5 — Manual Validation

Manual workflows should also be tested.

Examples:

```bash
dift examples/old.csv examples/new.csv --key customer_id
```

---

# Important Manual Validation Areas

Before release, verify:

- CLI help output
- report generation
- output directory support
- connector workflows
- config loading
- scheduling workflows
- progress indicators

---

# Step 6 — Update Version Numbers

Update version references in:

```text
pyproject.toml
README.md
dift/__init__.py   (if applicable)
```

Example:

```text
0.5.0 → 0.6.0
```

---

# Step 7 — Update Documentation

Update:

- README
- release notes
- roadmap
- developer docs
- examples

Documentation updates are considered part of the release itself.

---

# Step 8 — Create Release Notes

Release notes should summarize:

- new features
- fixes
- architectural improvements
- contributor credits
- migration notes

---

# Example Release Structure

```text
# What's New in v0.6.0

## New Features
- SQL connectors
- BigQuery support
- Reader registry system

## Improvements
- Better validation errors
- Progress indicators
- Improved HTML reports
```

---

# Step 9 — Build Distribution Packages

Build packages:

```bash
python -m build
```

This generates:

```text
dist/
├── *.whl
└── *.tar.gz
```

---

# Step 10 — Verify Package

Verify generated packages:

```bash
twine check dist/*
```

---

# Step 11 — Publish to PyPI

Upload to PyPI:

```bash
twine upload dist/*
```

---

# Step 12 — Create Git Tag

Create version tag:

```bash
git tag v0.6.0
git push origin v0.6.0
```

---

# Step 13 — GitHub Release

Create a GitHub release using:

- version tag
- release notes
- changelog summary

---

# Recommended Release Checklist

Before releasing:

```text
[ ] All tests pass
[ ] Lint checks pass
[ ] Type checks pass
[ ] Documentation updated
[ ] README updated
[ ] Version bumped
[ ] Release notes written
[ ] Manual workflows validated
[ ] Package builds successfully
```

---

# Backward Compatibility Philosophy

Dift strongly prioritizes:

- stable CLI behavior
- stable report schemas
- stable automation workflows

Breaking changes should be minimized.

---

# JSON Schema Stability

JSON reports are especially important because they may be consumed by:

- CI/CD systems
- APIs
- automation pipelines
- integrations

Schema-breaking changes should be handled carefully.

---

# Automation Stability

Release validation should ensure:

- strict exit codes still behave correctly
- quiet mode remains stable
- scheduled workflows still work
- progress indicators remain automation-safe

---

# Dependency Philosophy

Dift aims to keep core dependencies:

- lightweight
- stable
- optional when possible

Connector-specific dependencies should remain isolated.

---

# Optional Dependency Strategy

Examples:

```bash
pip install sqlalchemy
pip install duckdb
pip install google-cloud-bigquery
```

This helps reduce unnecessary install bloat.

---

# Connector Stability

Connector releases should preserve:

- URI formats
- routing behavior
- validation clarity
- dependency guidance

---

# Release Documentation Philosophy

Documentation should evolve alongside architecture.

Major features should never ship undocumented.

---

# Contributor Release Expectations

Before merging major features:

- tests should exist
- documentation should exist
- CLI UX should be validated
- error messaging should be reviewed

---

# Recommended Release Frequency

Dift currently favors:

```text
Feature-focused minor releases
```

instead of overly frequent micro releases.

This helps maintain:

- release quality
- architectural consistency
- manageable documentation

---

# Internal Refactor Policy

Internal architecture improvements are encouraged when they:

- reduce coupling
- improve extensibility
- simplify maintenance
- prepare future scaling

But they should avoid unnecessary user-facing disruption.

---

# Roadmap Alignment

Releases should align with the public roadmap.

Example areas:

- connectors
- plugin preparation
- automation workflows
- enterprise reporting
- warehouse integrations

---

# Future Release Goals

Future release infrastructure may include:

- automated GitHub Actions publishing
- automated changelog generation
- release validation pipelines
- plugin compatibility checks
- integration test matrices

---

# Potential Future CI Pipeline

Example future release flow:

```text
GitHub Actions
    ↓
Run Tests
    ↓
Run Linting
    ↓
Build Package
    ↓
Publish to PyPI
    ↓
Create GitHub Release
```

---

# Release Quality Principles

Every Dift release should aim to improve:

- reliability
- usability
- extensibility
- trust validation workflows
- developer experience

---

# Design Philosophy

The Dift release process prioritizes:

- stability
- reproducibility
- maintainability
- documentation quality
- ecosystem scalability

---

# Related Developer Docs

See also:

- architecture.md
- testing.md
- plugin-preparation.md
- report-system.md
- codebase-overview.md