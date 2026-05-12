from __future__ import annotations

import polars as pl

from dift.reports.models import (
    CategoricalDiff,
    NumericDiff,
    OutlierDiff,
    StatsDiff,
)

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


def compare_stats(
    old: pl.DataFrame,
    new: pl.DataFrame,
    top_n: int = 10,
    threshold: float = 0.1,
    key: str | None = None,
) -> StatsDiff:
    """Compare numeric summary stats, categorical top values, and outliers."""
    shared_cols = sorted(set(old.columns) & set(new.columns))
    numeric_diffs: list[NumericDiff] = []
    categorical_diffs: list[CategoricalDiff] = []
    outlier_diffs: list[OutlierDiff] = []

    for column in shared_cols:
        if key and column == key:
            continue

        old_dtype = old.schema[column]
        new_dtype = new.schema[column]

        if old_dtype in NUMERIC_DTYPES and new_dtype in NUMERIC_DTYPES:
            old_series = old[column]
            new_series = new[column]

            o_min = _safe_float(old_series.min())
            n_min = _safe_float(new_series.min())
            o_max = _safe_float(old_series.max())
            n_max = _safe_float(new_series.max())
            o_mean = _safe_float(old_series.mean())
            n_mean = _safe_float(new_series.mean())
            o_std = _safe_float(old_series.std())
            n_std = _safe_float(new_series.std())

            o_range = (
                o_max - o_min
                if o_max is not None and o_min is not None
                else None
            )
            n_range = (
                n_max - n_min
                if n_max is not None and n_min is not None
                else None
            )

            mean_shift_pct = _relative_change(n_mean, o_mean)
            std_shift_pct = _relative_change(n_std, o_std)
            range_shift_pct = _relative_change(n_range, o_range)

            is_drifted = any(
                shift is not None and shift >= threshold
                for shift in [mean_shift_pct, std_shift_pct, range_shift_pct]
            )

            severity = _classify_numeric_drift(
                mean_shift_pct=mean_shift_pct,
                std_shift_pct=std_shift_pct,
                range_shift_pct=range_shift_pct,
                threshold=threshold,
            )

            numeric_diffs.append(
                NumericDiff(
                    column=column,
                    old_min=o_min,
                    new_min=n_min,
                    old_max=o_max,
                    new_max=n_max,
                    old_mean=o_mean,
                    new_mean=n_mean,
                    delta_mean=_safe_delta(n_mean, o_mean),
                    old_std=o_std,
                    new_std=n_std,
                    delta_std=_safe_delta(n_std, o_std),
                    delta_range=_safe_delta(n_range, o_range),
                    mean_shift_pct=mean_shift_pct,
                    std_shift_pct=std_shift_pct,
                    range_shift_pct=range_shift_pct,
                    is_drifted=is_drifted,
                    drift_threshold=threshold,
                    severity=severity,
                )
            )

            outlier_diffs.append(
                _compare_outliers(
                    column=column,
                    old_series=old_series,
                    new_series=new_series,
                )
            )

        elif old_dtype in CATEGORICAL_DTYPES and new_dtype in CATEGORICAL_DTYPES:
            old_counts = _top_counts(old, column, top_n)
            new_counts = _top_counts(new, column, top_n)
            old_values = set(old_counts)
            new_values = set(new_counts)

            old_freq = _value_frequencies(old, column)
            new_freq = _value_frequencies(new, column)

            frequency_shifts: dict[str, float] = {}
            for value in sorted(set(old_freq) | set(new_freq), key=str):
                shift = round(
                    new_freq.get(value, 0.0) - old_freq.get(value, 0.0),
                    4,
                )

                if abs(shift) >= threshold:
                    frequency_shifts[str(value)] = shift

            max_frequency_shift = (
                max(abs(shift) for shift in frequency_shifts.values())
                if frequency_shifts
                else 0.0
            )

            values_added = sorted(map(str, new_values - old_values))
            values_removed = sorted(map(str, old_values - new_values))
            is_shifted = bool(values_added or values_removed or frequency_shifts)
            severity = _classify_categorical_shift(max_frequency_shift, threshold)

            categorical_diffs.append(
                CategoricalDiff(
                    column=column,
                    values_added=values_added,
                    values_removed=values_removed,
                    old_top_values={str(k): v for k, v in old_counts.items()},
                    new_top_values={str(k): v for k, v in new_counts.items()},
                    frequency_shifts=frequency_shifts,
                    max_frequency_shift=max_frequency_shift,
                    is_shifted=is_shifted,
                    severity=severity,
                )
            )

    return StatsDiff(
        numeric_diffs=numeric_diffs,
        categorical_diffs=categorical_diffs,
        outlier_diffs=outlier_diffs,
    )


def _compare_outliers(
    column: str,
    old_series: pl.Series,
    new_series: pl.Series,
) -> OutlierDiff:
    method = "iqr"

    old_values = old_series.drop_nulls()
    new_values = new_series.drop_nulls()

    if old_values.len() == 0 or new_values.len() == 0:
        return OutlierDiff(column=column, method=method)

    q1 = _safe_float(old_values.quantile(0.25))
    q3 = _safe_float(old_values.quantile(0.75))

    if q1 is None or q3 is None:
        return OutlierDiff(column=column, method=method)

    iqr = q3 - q1

    if iqr == 0:
        lower_bound = q1
        upper_bound = q3
    else:
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

    old_outliers = _count_outliers(old_values, lower_bound, upper_bound)
    new_outliers = _count_outliers(new_values, lower_bound, upper_bound)

    old_rows = old_values.len() or 1
    new_rows = new_values.len() or 1

    old_outlier_pct = round(old_outliers / old_rows * 100, 4)
    new_outlier_pct = round(new_outliers / new_rows * 100, 4)
    delta_outlier_pct = round(new_outlier_pct - old_outlier_pct, 4)

    delta_outliers = new_outliers - old_outliers
    is_spike, severity = _classify_outlier_spike(delta_outlier_pct)

    return OutlierDiff(
        column=column,
        method=method,
        old_outliers=old_outliers,
        new_outliers=new_outliers,
        delta_outliers=delta_outliers,
        old_outlier_pct=old_outlier_pct,
        new_outlier_pct=new_outlier_pct,
        delta_outlier_pct=delta_outlier_pct,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        is_spike=is_spike,
        severity=severity,
    )


def _count_outliers(
    values: pl.Series,
    lower_bound: float,
    upper_bound: float,
) -> int:
    return values.filter((values < lower_bound) | (values > upper_bound)).len()


def _classify_outlier_spike(delta_outlier_pct: float) -> tuple[bool, str]:
    if delta_outlier_pct >= 15:
        return True, "high"

    if delta_outlier_pct >= 5:
        return True, "medium"

    return False, "low"


def _top_counts(df: pl.DataFrame, column: str, top_n: int) -> dict[object, int]:
    result = (
        df.group_by(column)
        .len()
        .sort("len", descending=True)
        .head(top_n)
        .to_dicts()
    )
    return {row[column]: row["len"] for row in result}


def _value_frequencies(df: pl.DataFrame, column: str) -> dict[object, float]:
    total = df.height or 1
    counts = df.group_by(column).len().to_dicts()

    return {row[column]: row["len"] / total for row in counts}


def _safe_float(value: object) -> float | None:
    if value is None:
        return None
    return float(value)


def _relative_change(
    new_value: float | None,
    old_value: float | None,
) -> float | None:
    if new_value is None or old_value is None:
        return None

    baseline = abs(old_value)

    if baseline == 0:
        return abs(new_value) if new_value != 0 else 0.0

    return abs(new_value - old_value) / baseline


def _classify_numeric_drift(
    mean_shift_pct: float | None,
    std_shift_pct: float | None,
    range_shift_pct: float | None,
    threshold: float,
) -> str:
    shifts = [
        shift
        for shift in [mean_shift_pct, std_shift_pct, range_shift_pct]
        if shift is not None
    ]

    if not shifts:
        return "low"

    max_shift = max(shifts)

    if max_shift >= threshold * 5:
        return "high"

    if max_shift >= threshold * 2:
        return "medium"

    if max_shift >= threshold:
        return "low"

    return "low"


def _classify_categorical_shift(
    max_frequency_shift: float,
    threshold: float,
) -> str:
    if max_frequency_shift >= threshold * 5:
        return "high"

    if max_frequency_shift >= threshold * 2:
        return "medium"

    if max_frequency_shift >= threshold:
        return "low"

    return "low"


def _safe_delta(
    new_value: float | None,
    old_value: float | None,
) -> float | None:
    if new_value is None or old_value is None:
        return None
    return new_value - old_value