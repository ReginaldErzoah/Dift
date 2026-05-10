from __future__ import annotations

from dift.reports.models import DiffReport

LOW_RISK_THRESHOLD = 30
HIGH_RISK_THRESHOLD = 70


def assign_risk_level(report: DiffReport) -> str:
    """Assign risk level using weighted dataset change signals."""
    score = calculate_risk_score(report)

    if score >= HIGH_RISK_THRESHOLD:
        return "high"

    if score >= LOW_RISK_THRESHOLD:
        return "medium"

    return "low"


def calculate_risk_score(report: DiffReport) -> int:
    """Calculate weighted dataset risk score from 0 to 100."""
    score = 0

    score += _schema_risk_score(report)
    score += _row_risk_score(report)
    score += _quality_risk_score(report)
    score += _stats_risk_score(report)

    return min(score, 100)


def _schema_risk_score(report: DiffReport) -> int:
    score = 0

    score += len(report.schema_diff.columns_added) * 5
    score += len(report.schema_diff.columns_removed) * 10
    score += len(report.schema_diff.type_changes) * 15

    return score


def _row_risk_score(report: DiffReport) -> int:
    score = 0

    changed_rows = report.row_diff.changed_rows or 0
    removed_rows = report.row_diff.removed_rows or 0
    added_rows = report.row_diff.added_rows or 0

    score += min(changed_rows * 2, 20)
    score += min(removed_rows * 3, 25)
    score += min(added_rows * 1, 10)

    return score


def _quality_risk_score(report: DiffReport) -> int:
    score = 0

    duplicate = report.quality_diff.duplicate_diff

    if duplicate.is_spike:
        if duplicate.severity == "high":
            score += 25
        elif duplicate.severity == "medium":
            score += 15
        else:
            score += 5
    elif duplicate.delta_duplicates > 0:
        score += min(duplicate.delta_duplicates * 5, 20)

    for null_diff in report.quality_diff.null_diffs:
        if not null_diff.is_spike:
            continue

        if null_diff.severity == "high":
            score += 25
        elif null_diff.severity == "medium":
            score += 15
        else:
            score += 5

    return min(score, 50)


def _stats_risk_score(report: DiffReport) -> int:
    score = 0

    for numeric_diff in report.numeric_diff:

        if not numeric_diff.is_drifted:
            continue

        if numeric_diff.old_mean is not None and numeric_diff.delta_mean is not None:
            baseline = abs(numeric_diff.old_mean) or 1
            shift_pct = abs(numeric_diff.delta_mean) / baseline * 100
            if shift_pct >= 50: 
                score += 15
            elif shift_pct >= 20: 
                score += 10
            elif shift_pct >= 10: 
                score += 5
        
        if numeric_diff.old_std is not None and numeric_diff.delta_std is not None:
            baseline = abs(numeric_diff.old_std) or 1
            shift_pct = abs(numeric_diff.delta_std) / baseline * 100
            if shift_pct >= 50: 
                score += 10  
            elif shift_pct >= 20: 
                score += 5

        old_range = (numeric_diff.old_max or 0) - (numeric_diff.old_min or 0)
        if old_range > 0 and numeric_diff.delta_range is not None:
            shift_pct = abs(numeric_diff.delta_range) / old_range * 100
            if shift_pct >= 50: 
                score += 5

    for categorical_diff in report.categorical_diff:
        added_count = len(categorical_diff.values_added)
        removed_count = len(categorical_diff.values_removed)

        score += min(added_count * 3, 15)
        score += min(removed_count * 4, 20)

    return min(score, 30)