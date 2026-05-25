# Performance

Dift is being designed to scale from small local dataset comparisons to larger analytical and warehouse-style workflows.

This document explains performance-related features, current scalability behavior, chunked dataset processing, memory considerations, and future optimization direction.

---

# Performance Philosophy

Dift performance work focuses on:

- reducing memory usage
- supporting larger datasets
- keeping existing workflows stable
- improving CLI responsiveness
- preparing for future distributed comparison
- maintaining report consistency

The goal is to make Dift useful across:

- local development workflows
- ETL validation
- warehouse exports
- large analytical datasets
- automation pipelines

---

# Current Performance Model

Dift currently performs comparisons by loading datasets into Polars DataFrames and then running comparison stages.

Current workflow:

```text
Dataset Source
  ↓
Reader
  ↓
Polars DataFrame
  ↓
Comparison Engine
  ↓
Reports
```

This works well for small and medium datasets.

For very large datasets, memory usage can increase because the full dataset may need to be available during comparison.

---

# Chunked Dataset Processing

Chunked dataset processing allows Dift to read supported datasets incrementally instead of loading the file in one operation.

This is useful for large CSV files where reading the entire file at once may consume too much memory.

---

# Why Chunking Matters

Chunked reading helps with:

- lower peak memory usage during loading
- large CSV workflows
- memory-constrained environments
- future streaming and distributed comparison work

---

# Supported Chunked Sources

Current chunked reading support:

| Source Type | Chunked Support |
|---|---|
| CSV | Supported |
| Parquet | Not yet supported |
| Excel | Not yet supported |
| JSON | Not yet supported |
| SQL databases | Not yet supported |
| DuckDB | Not yet supported |
| BigQuery | Not yet supported |

---

# Basic Usage

Use the `--chunk-size` option:

```bash
dift large_old.csv large_new.csv \
  --key id \
  --chunk-size 50000
```

This reads supported datasets in chunks of 50,000 rows.

---

# Example With Report Output

```bash
dift large_old.csv large_new.csv \
  --key id \
  --chunk-size 50000 \
  --report html \
  --output reports/large-comparison.html
```

---

# Example With JSON Report

```bash
dift large_old.csv large_new.csv \
  --key id \
  --chunk-size 25000 \
  --report json \
  --output reports/large-comparison.json
```

---

# Config File Example

Chunk size can also be defined in a config file.

```yaml
old_dataset: large_old.csv
new_dataset: large_new.csv
key: id
report: html
output: reports/large-comparison.html
chunk_size: 50000
```

Run:

```bash
dift --config config_large.yaml
```

---

# Profile Example

Chunk size can be saved in reusable profiles.

```bash
dift profile create large-check \
  --old large_old.csv \
  --new large_new.csv \
  --key id \
  --chunk-size 50000 \
  --report html
```

Run the profile:

```bash
dift profile run large-check
```

Override chunk size during profile execution:

```bash
dift profile run large-check --chunk-size 25000
```

---

# Batch Workflow Example

Chunked loading can also be used with batch comparisons.

```bash
dift batch \
  --old-dir data/old \
  --new-dir data/new \
  --key id \
  --chunk-size 50000
```

---

# Choosing a Chunk Size

There is no universal best chunk size.

Recommended starting points:

| Dataset Size | Suggested Chunk Size |
|---|---|
| Small datasets | No chunking needed |
| 100k–1M rows | 25,000–50,000 |
| 1M–10M rows | 50,000–100,000 |
| Very large CSVs | Start with 50,000 and benchmark |

Smaller chunks may reduce memory usage but increase overhead.

Larger chunks may improve speed but use more memory.

---

# Current Limitation

In the current implementation, Dift supports chunk-aware dataset loading, but the existing comparison engine still materializes the loaded chunks into a full Polars DataFrame before comparison.

This means chunking helps improve the loading path and prepares the architecture for future streaming comparison, but it is not yet a full streaming comparison engine.

Future work will push chunk processing deeper into:

- row comparison
- statistical drift detection
- quality analysis
- report generation

---

# What Chunking Improves Today

Current chunking improves:

- reader architecture
- large CSV loading workflow
- memory behavior during initial file reading
- preparation for future incremental comparison

---

# What Chunking Does Not Fully Solve Yet

Current chunking does not fully eliminate memory usage during:

- row-level comparison
- full DataFrame hashing
- statistical drift computation
- report model construction

These areas are planned for future optimization.

---

# Error Handling

If chunked reading is used with an unsupported source, Dift shows a clear error.

Example:

```bash
dift old.json new.json --chunk-size 50000
```

Current behavior:

```text
Chunked reading is not supported for source: old.json
Currently supported chunked sources: local CSV files.
```

---

# Invalid Chunk Sizes

Chunk size must be a positive integer.

Invalid:

```bash
dift old.csv new.csv --chunk-size 0
```

Valid:

```bash
dift old.csv new.csv --chunk-size 50000
```

---

# Performance Testing

Run tests:

```bash
pytest
ruff check .
```

Run chunk-specific tests:

```bash
pytest tests/test_chunk_processing.py
```

---

# Manual Validation

Create or use large CSV files and run:

```bash
dift large_old.csv large_new.csv \
  --key id \
  --chunk-size 50000 \
  --verbose
```

Verify:

- comparison completes successfully
- reports remain correct
- no existing workflow breaks
- memory behavior is improved during loading

---

# Recommended Benchmark Workflow

For local benchmarking, compare runtime and memory behavior between:

```bash
dift large_old.csv large_new.csv --key id
```

and:

```bash
dift large_old.csv large_new.csv --key id --chunk-size 50000
```

Track:

- runtime
- peak memory usage
- report consistency
- output correctness

---

# Performance Best Practices

Recommended practices:

- use CSV chunking for large local CSV workflows
- start with `--chunk-size 50000`
- use `--verbose` for visibility
- use JSON reports for automation workflows
- use HTML reports for human review
- benchmark before choosing very small chunk sizes

---

# Large Dataset Considerations

For very large datasets, consider:

- using warehouse-native filtering before comparison
- comparing sampled outputs first
- exporting only relevant columns
- using a key column for row comparison
- generating JSON reports for automation
- avoiding unnecessary wide-column comparisons

---

# Connector Performance

Performance depends on the source type.

| Source | Performance Notes |
|---|---|
| CSV | Chunking available |
| Parquet | Usually efficient through Polars |
| Excel | Best for smaller datasets |
| JSON | Useful for structured records, not ideal for very large files |
| SQL | Depends on query size and database performance |
| DuckDB | Strong for analytical local workflows |
| BigQuery | Depends on warehouse query execution and network transfer |

---

# Future Performance Roadmap

Planned future improvements include:

- streaming comparisons
- true chunk-aware row comparison
- chunk-aware drift detection
- parallel processing
- lazy loading workflows
- sampling-based comparison
- approximate diff algorithms
- distributed comparison preparation
- billion-row workflow preparation

---

# Developer Notes

Chunked reading currently lives in the dataset reader layer.

Relevant files:

```text
dift/io/base_reader.py
dift/io/readers.py
dift/core/comparator.py
tests/test_chunk_processing.py
```

Future contributors should avoid coupling chunked processing too tightly to CSV-only logic.

The long-term goal is to make chunk-aware behavior part of Dift’s broader reader and comparison architecture.

---

# Related Documentation

See also:

- examples.md
- automation.md
- configuration.md
- reports.md
- developer/architecture.md
- developer/testing.md
- developer/reader-registry.md