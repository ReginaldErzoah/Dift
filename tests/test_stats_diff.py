import polars as pl

from dift.core.stats_diff import compare_stats


def test_outlier_detection_finds_new_outliers():
    old = pl.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "revenue": [100, 102, 98, 101, 99],
        }
    )

    new = pl.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "revenue": [100, 102, 98, 101, 1000],
        }
    )

    result = compare_stats(old, new)

    revenue_outlier = next(
        item for item in result.outlier_diffs if item.column == "revenue"
    )

    assert revenue_outlier.new_outliers > revenue_outlier.old_outliers
    assert revenue_outlier.delta_outliers > 0
    assert revenue_outlier.is_spike is True
    assert revenue_outlier.severity in {"medium", "high"}


def test_outlier_detection_ignores_non_numeric_columns():
    old = pl.DataFrame(
        {
            "id": [1, 2, 3],
            "segment": ["basic", "basic", "pro"],
        }
    )

    new = pl.DataFrame(
        {
            "id": [1, 2, 3],
            "segment": ["basic", "enterprise", "pro"],
        }
    )

    result = compare_stats(old, new)

    assert all(item.column != "segment" for item in result.outlier_diffs)

def test_categorical_frequency_shift_is_detected():
    old = pl.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "segment": ["basic", "basic", "basic", "basic", "enterprise"],
        }
    )

    new = pl.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "segment": ["basic", "enterprise", "enterprise", "startup", "startup"],
        }
    )

    result = compare_stats(old, new, threshold=0.1, key="id")

    segment_diff = next(
        item for item in result.categorical_diffs if item.column == "segment"
    )

    assert segment_diff.is_shifted is True
    assert segment_diff.severity == "high"
    assert segment_diff.max_frequency_shift == 0.6
    assert segment_diff.frequency_shifts["basic"] == -0.6
    assert segment_diff.frequency_shifts["startup"] == 0.4
    assert segment_diff.values_added == ["startup"]


def test_categorical_frequency_shift_respects_threshold():
    old = pl.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "segment": ["basic", "basic", "basic", "basic", "enterprise"],
        }
    )

    new = pl.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "segment": ["basic", "enterprise", "enterprise", "startup", "startup"],
        }
    )

    result = compare_stats(old, new, threshold=0.9, key="id")

    segment_diff = next(
        item for item in result.categorical_diffs if item.column == "segment"
    )

    assert segment_diff.frequency_shifts == {}
    assert segment_diff.max_frequency_shift == 0.0