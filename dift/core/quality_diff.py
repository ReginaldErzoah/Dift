from __future__ import annotations

import polars as pl

from dift.reports.models import DuplicateDiff, NullDiff, QualityDiff


def classify_null_spike(delta_null_pct: float) -> tuple[bool, str]:
    """
    Classify null percentage increases.

    Thresholds:
    - < 5% increase: low
    - 5% to < 15% increase: medium
    - >= 15% increase: high
    """

    if delta_null_pct >= 15:
        return True, "high"

    if delta_null_pct >= 5:
        return True, "medium"

    return False, "low"


def compare_quality(
    old: pl.DataFrame,
    new: pl.DataFrame,
    key: str | None = None,
) -> QualityDiff:
    """Compare null and duplicate behavior across shared columns."""
    shared_cols = sorted(set(old.columns) & set(new.columns))
    old_rows = old.height or 1
    new_rows = new.height or 1

    null_diffs: list[NullDiff] = []
    for column in shared_cols:
        old_nulls = old[column].null_count()
        new_nulls = new[column].null_count()
        old_pct = old_nulls / old_rows * 100
        new_pct = new_nulls / new_rows * 100
        delta_null_pct = round(new_pct - old_pct, 4)
        is_spike, severity = classify_null_spike(delta_null_pct)

        null_diffs.append(
            NullDiff(
                column=column,
                old_nulls=old_nulls,
                new_nulls=new_nulls,
                old_null_pct=round(old_pct, 4),
                new_null_pct=round(new_pct, 4),
                delta_null_pct=delta_null_pct,
                is_spike=is_spike,
                severity=severity,
            )
        )

    duplicate_subset = [key] if key else None
    old_duplicates = old.height - old.unique(subset=duplicate_subset).height
    new_duplicates = new.height - new.unique(subset=duplicate_subset).height

    return QualityDiff(
        null_diffs=null_diffs,
        duplicate_diff=DuplicateDiff(
            old_duplicates=old_duplicates,
            new_duplicates=new_duplicates,
            delta_duplicates=new_duplicates - old_duplicates,
            duplicate_basis=key or "entire_row",
        ),
    )