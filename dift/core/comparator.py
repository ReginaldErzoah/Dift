from __future__ import annotations

from dift.core.quality_diff import compare_quality
from dift.core.risk import assign_risk_level
from dift.core.row_diff import compare_rows
from dift.core.schema_diff import compare_schema
from dift.core.stats_diff import compare_stats
from dift.io.readers import read_dataset
from dift.reports.models import DiffReport, Summary


def compare_datasets(
    old_path: str,
    new_path: str,
    key: str | None = None,
    threshold: float = 0.1,
) -> DiffReport:
    """Run the full MVP dataset comparison."""
    old = read_dataset(old_path)
    new = read_dataset(new_path)

    schema_diff = compare_schema(old, new)
    row_diff = compare_rows(old, new, key=key)
    quality_diff = compare_quality(old, new, key=key)
    stats_diff = compare_stats(
        old,
        new,
        threshold=threshold,
        key=key,
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
