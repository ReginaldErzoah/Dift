# Release Notes

This section contains official release notes for Dift.

Release notes document:

- new features
- architectural improvements
- connector support
- reporting improvements
- automation workflows
- breaking changes
- migration guidance
- developer experience improvements

---

# Release Philosophy

Dift follows an incremental release strategy focused on:

- stability
- extensibility
- automation compatibility
- connector scalability
- data trust workflows

Each release aims to improve:

- usability
- reporting quality
- validation reliability
- extensibility
- enterprise readiness

---

# Available Releases

| Version | Highlights |
|---|---|
| [v0.1.0](v0.1.0.md) | Initial public release |
| [v0.2.1](v0.2.1.md) | Reporting improvements and validation enhancements |
| [v0.3.0](v0.3.0.md) | Config system, threshold policies, output directories |
| [v0.5.0](v0.5.0.md) | Advanced drift detection, automation workflows, history tracking |
| [v0.6.0](v0.6.0.md) | SQL support, warehouse connectors, reader registry, plugin preparation |

---

# Major Evolution Timeline

---

# v0.1.0 — Foundation

Core comparison engine introduced:

- schema comparison
- row comparison
- quality analysis
- risk scoring
- report generation

---

# v0.2.1 - Stability & Reporting

Focused on:

- report improvements
- CLI usability
- validation clarity
- output consistency

---

# v0.3.0 - Reusable Workflows

Introduced:

- config files
- threshold policies
- environment configs
- output directory workflows
- reusable validation setups

---

# v0.5.0 - Automation & Drift Intelligence

Major additions:

- numeric drift detection
- categorical drift analysis
- outlier detection
- scheduling workflows
- batch comparisons
- comparison history
- automation-friendly execution

---

# v0.6.0 - Connectors & Architecture

Major architectural release introducing:

- SQL database support
- BigQuery support
- DuckDB support
- connector registry architecture
- modular reader interfaces
- plugin preparation systems
- progress indicators

---

# Reading Release Notes

Each release document may include:

- feature summaries
- CLI examples
- architectural changes
- migration notes
- workflow improvements
- future roadmap direction

---

# Versioning Strategy

Dift currently follows a semantic-style versioning strategy:

```text
MAJOR.MINOR.PATCH
```

Example:

```text
0.6.0
```

---

# Current Development Phase

Dift is currently in the:

```text
0.x.x
```

development phase.

This means:

- architecture continues evolving
- features expand rapidly
- extensibility work is ongoing

However, backward compatibility and stability remain important priorities.

---

# Upgrade Recommendation

Upgrade to the latest version:

```bash
pip install --upgrade dift-cli
```

---

# Verify Installed Version

```bash
dift --help
```

or:

```bash
python -m dift.cli --help
```

---

# Release Goals

Dift releases aim to improve:

- data trust validation
- drift detection workflows
- warehouse compatibility
- automation support
- enterprise readiness
- extensibility

---

# Long-Term Vision

Dift aims to become the open-source standard for:

- dataset regression testing
- data drift monitoring
- warehouse trust validation
- ML dataset validation
- automated data quality enforcement

---

# Related Documentation

See also:

- ../getting-started/installation.md
- ../configuration.md
- ../connectors/sql.md
- ../automation.md
- ../developer/architecture.md
- ../developer/release-process.md