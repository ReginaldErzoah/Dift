from __future__ import annotations

import polars as pl

from dift.reports.models import RowDiff
from dift.utils.hashing import row_hash_expr


class RowDiffError(ValueError):
    """Raised when row-level comparison cannot be performed."""


def validate_row_comparison_inputs(
    old: pl.DataFrame,
    new: pl.DataFrame,
    key: str,
) -> None:
    """
    Validate datasets before row-level comparison.

    This helper prepares the row comparison system for future chunk-aware
    and distributed comparison workflows by centralizing validation logic.
    """
    if key not in old.columns:
        raise RowDiffError(f"Key column '{key}' is missing from old dataset")

    if key not in new.columns:
        raise RowDiffError(f"Key column '{key}' is missing from new dataset")


def compare_rows(
    old: pl.DataFrame,
    new: pl.DataFrame,
    key: str | None = None,
) -> RowDiff:
    """Compare rows, optionally by a primary key column."""
    if key is None:
        return RowDiff(
            key=None,
            added_rows=None,
            removed_rows=None,
            changed_rows=None,
            unchanged_rows=None,
            note="Pass --key to enable added/removed/changed row comparison.",
        )

    validate_row_comparison_inputs(old, new, key)

    shared_columns = sorted((set(old.columns) & set(new.columns)) - {key})

    old_hashed = old.select(
        [pl.col(key), row_hash_expr(shared_columns).alias("_dift_hash")]
    )

    new_hashed = new.select(
        [pl.col(key), row_hash_expr(shared_columns).alias("_dift_hash")]
    )

    old_keys = old_hashed.select(key).unique()
    new_keys = new_hashed.select(key).unique()

    removed_rows = old_keys.join(new_keys, on=key, how="anti").height

    added_rows = new_keys.join(old_keys, on=key, how="anti").height

    joined = old_hashed.join(
        new_hashed,
        on=key,
        how="inner",
        suffix="_new",
    )

    changed_rows = joined.filter(
        pl.col("_dift_hash") != pl.col("_dift_hash_new")
    ).height

    unchanged_rows = joined.filter(
        pl.col("_dift_hash") == pl.col("_dift_hash_new")
    ).height

    return RowDiff(
        key=key,
        added_rows=added_rows,
        removed_rows=removed_rows,
        changed_rows=changed_rows,
        unchanged_rows=unchanged_rows,
        compared_columns=shared_columns,
    )