from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ReportMetadata(BaseModel):
    tool: str = "dift"
    version: str = "0.5.0"
    report_type: str = "dataset_diff"


class Summary(BaseModel):
    old_rows: int
    new_rows: int
    row_delta: int
    old_columns: int
    new_columns: int
    column_delta: int
    risk_level: str


class TypeChange(BaseModel):
    column: str
    old_type: str
    new_type: str
    change_type: str = "type_changed"


class SchemaDiff(BaseModel):
    columns_added: list[str] = Field(default_factory=list)
    columns_removed: list[str] = Field(default_factory=list)
    shared_columns: list[str] = Field(default_factory=list)
    type_changes: list[TypeChange] = Field(default_factory=list)


class RowDiff(BaseModel):
    key: str | None = None
    added_rows: int | None = None
    removed_rows: int | None = None
    changed_rows: int | None = None
    unchanged_rows: int | None = None
    compared_columns: list[str] = Field(default_factory=list)
    note: str | None = None


class NullDiff(BaseModel):
    column: str
    old_nulls: int
    new_nulls: int
    old_null_pct: float
    new_null_pct: float
    delta_null_pct: float
    is_spike: bool = False
    severity: str = "low"


class DuplicateDiff(BaseModel):
    old_duplicates: int
    new_duplicates: int
    delta_duplicates: int
    old_duplicate_pct: float = 0.0
    new_duplicate_pct: float = 0.0
    delta_duplicate_pct: float = 0.0
    duplicate_basis: str
    is_spike: bool = False
    severity: str = "low"


class QualityDiff(BaseModel):
    null_diffs: list[NullDiff] = Field(default_factory=list)
    duplicate_diff: DuplicateDiff


class NumericDiff(BaseModel):
    column: str
    old_min: float | None = None
    new_min: float | None = None
    old_max: float | None = None
    new_max: float | None = None
    old_mean: float | None = None
    new_mean: float | None = None
    delta_mean: float | None = None
    old_std: float | None = None
    new_std: float | None = None
    delta_std: float | None = None
    delta_range: float | None = None
    mean_shift_pct: float | None = None
    std_shift_pct: float | None = None
    range_shift_pct: float | None = None
    drift_threshold: float | None = None
    is_drifted: bool = False
    severity: str = "low"


class OutlierDiff(BaseModel):
    column: str
    method: str = "iqr"
    old_outliers: int = 0
    new_outliers: int = 0
    delta_outliers: int = 0
    old_outlier_pct: float = 0.0
    new_outlier_pct: float = 0.0
    delta_outlier_pct: float = 0.0
    lower_bound: float | None = None
    upper_bound: float | None = None
    is_spike: bool = False
    severity: str = "low"


class CategoricalDiff(BaseModel):
    column: str
    values_added: list[str] = Field(default_factory=list)
    values_removed: list[str] = Field(default_factory=list)
    old_top_values: dict[str, int] = Field(default_factory=dict)
    new_top_values: dict[str, int] = Field(default_factory=dict)
    frequency_shifts: dict[str, float] = Field(default_factory=dict)
    max_frequency_shift: float = 0.0
    is_shifted: bool = False
    severity: str = "low"


class StatsDiff(BaseModel):
    numeric_diffs: list[NumericDiff] = Field(default_factory=list)
    categorical_diffs: list[CategoricalDiff] = Field(default_factory=list)
    outlier_diffs: list[OutlierDiff] = Field(default_factory=list)


class DiffReport(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    metadata: ReportMetadata = Field(default_factory=ReportMetadata)
    summary: Summary

    schema_diff: SchemaDiff = Field(alias="schema")
    row_diff: RowDiff = Field(alias="rows")
    quality_diff: QualityDiff = Field(alias="quality")

    numeric_diff: list[NumericDiff] = Field(default_factory=list, alias="numeric")
    categorical_diff: list[CategoricalDiff] = Field(
        default_factory=list,
        alias="categorical",
    )
    outlier_diff: list[OutlierDiff] = Field(default_factory=list, alias="outliers")
