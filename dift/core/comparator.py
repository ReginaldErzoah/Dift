from __future__ import annotations

import polars as pl

from dift.core.quality_diff import compare_quality
from dift.core.risk import assign_risk_level
from dift.core.row_diff import compare_rows
from dift.core.schema_diff import compare_schema
from dift.core.stats_diff import compare_stats
from dift.io.readers import read_dataset, read_dataset_chunks
from dift.reports.models import DiffReport, Summary
from dift.thresholds import ThresholdConfig


def _read_dataset_with_optional_chunks(
    dataset: str,
    chunk_size: int | None = None,
) -> pl.DataFrame:
    """
    Read a dataset normally or through the chunked reader path.

    This is the first chunk-aware comparison step. It allows Dift to load
    supported sources incrementally before combining them into the existing
    comparison engine.

    Future versions can push chunk processing deeper into row/stat comparison
    so very large datasets do not need to be materialized before comparison.
    """
    if chunk_size is None:
        return read_dataset(dataset)

    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer.")

    chunks = list(read_dataset_chunks(dataset, chunk_size=chunk_size))

    if not chunks:
        return pl.DataFrame()

    return pl.concat(chunks, how="vertical")


def compare_datasets(
    old_dataset: str,
    new_dataset: str,
    key: str | None = None,
    threshold: float = 0.1,
    threshold_config: ThresholdConfig | None = None,
    chunk_size: int | None = None,
) -> DiffReport:
    """Run the full dataset comparison."""
    old = _read_dataset_with_optional_chunks(old_dataset, chunk_size=chunk_size)
    new = _read_dataset_with_optional_chunks(new_dataset, chunk_size=chunk_size)

    schema_diff = compare_schema(old, new)
    row_diff = compare_rows(old, new, key=key)
    quality_diff = compare_quality(old, new, key=key)
    stats_diff = compare_stats(
        old,
        new,
        threshold=threshold,
        key=key,
        threshold_config=threshold_config,
    )

    report = DiffReport(
        summary=Summary(
            old_rows=old.height,
            new_rows=new.height,
            row_delta=new.height - old.height,
            old_columns=len(old.columns),
            new_columns=len(new.columns),
            column_delta=len(new.columns) - len(old.columns),
            risk_level="unknown",
        ),
        schema_diff=schema_diff,
        row_diff=row_diff,
        quality_diff=quality_diff,
        numeric_diff=stats_diff.numeric_diffs,
        categorical_diff=stats_diff.categorical_diffs,
        outlier_diff=stats_diff.outlier_diffs,
    )

    report.summary.risk_level = assign_risk_level(report)
    return report