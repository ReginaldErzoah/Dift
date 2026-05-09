from __future__ import annotations
import polars as pl

from dift.reports.models import CategoricalDiff, NumericDiff, StatsDiff

NUMERIC_DTYPES = {
    pl.Int8,
    pl.Int16,
    pl.Int32,
    pl.Int64,
    pl.UInt8,
    pl.UInt16,
    pl.UInt32,
    pl.UInt64,
    pl.Float32,
    pl.Float64,
}

CATEGORICAL_DTYPES = {pl.String, pl.Categorical, pl.Enum, pl.Boolean}


def compare_stats(old: pl.DataFrame, new: pl.DataFrame, top_n: int = 10) -> StatsDiff:
    """Compare numeric summary stats and categorical top values."""
    shared_cols = sorted(set(old.columns) & set(new.columns))
    numeric_diffs: list[NumericDiff] = []
    categorical_diffs: list[CategoricalDiff] = []

    for column in shared_cols:
        old_dtype = old.schema[column]
        new_dtype = new.schema[column]

        if old_dtype in NUMERIC_DTYPES and new_dtype in NUMERIC_DTYPES:
            old_series = old[column]
            new_series = new[column]
            old_mean = _safe_float(old_series.mean())
            new_mean = _safe_float(new_series.mean())
            old_outliers = _list_outliers_iqr(old_series)
            new_outliers = _list_outliers_iqr(new_series)

            numeric_diffs.append(
                NumericDiff(
                    column=column,
                    old_min=_safe_float(old_series.min()),
                    new_min=_safe_float(new_series.min()),
                    old_max=_safe_float(old_series.max()),
                    new_max=_safe_float(new_series.max()),
                    old_mean=old_mean,
                    new_mean=new_mean,
                    delta_mean=_safe_delta(new_mean, old_mean),
                    old_std=_safe_float(old_series.std()),
                    new_std=_safe_float(new_series.std()),
                    old_outliers=old_outliers,
                    new_outliers=new_outliers,
                )
            )

        elif old_dtype in CATEGORICAL_DTYPES and new_dtype in CATEGORICAL_DTYPES:
            old_counts = _top_counts(old, column, top_n)
            new_counts = _top_counts(new, column, top_n)
            old_values = set(old_counts)
            new_values = set(new_counts)
            categorical_diffs.append(
                CategoricalDiff(
                    column=column,
                    values_added=sorted(map(str, new_values - old_values)),
                    values_removed=sorted(map(str, old_values - new_values)),
                    old_top_values={str(k): v for k, v in old_counts.items()},
                    new_top_values={str(k): v for k, v in new_counts.items()},
                )
            )

    return StatsDiff(numeric_diffs=numeric_diffs, categorical_diffs=categorical_diffs)


def _top_counts(df: pl.DataFrame, column: str, top_n: int) -> dict[object, int]:
    result = (
        df.group_by(column)
        .len()
        .sort("len", descending=True)
        .head(top_n)
        .to_dicts()
    )
    return {row[column]: row["len"] for row in result}


def _safe_float(value: object) -> float | None:
    if value is None:
        return None
    return float(value)


def _safe_delta(new_value: float | None, old_value: float | None) -> float | None:
    if new_value is None or old_value is None:
        return None
    return new_value - old_value


def _list_outliers_iqr(col: pl.Series) -> list[float] | None:
    q1, q3 = col.quantile(0.25), col.quantile(0.75)
    if (q1 is None) or (q3 is None):
        return None

    iqr = q3 - q1
    threshold = 1.5
    lower_limit = q1 - iqr * threshold
    upper_limit = q3 + iqr * threshold
    return [val for val
            in col.drop_nans().drop_nulls().sort(descending=True)
            if (val < lower_limit) | (val > upper_limit)]
