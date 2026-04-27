from __future__ import annotations

from pydantic import BaseModel, Field


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


class DuplicateDiff(BaseModel):
    old_duplicates: int
    new_duplicates: int
    delta_duplicates: int
    duplicate_basis: str


class QualityDiff(BaseModel):
    null_diffs: list[NullDiff] = Field(default_factory=list)
    duplicate_diff: DuplicateDiff


class NumericDiff(BaseModel):
    column: str
    old_min: float | None
    new_min: float | None
    old_max: float | None
    new_max: float | None
    old_mean: float | None
    new_mean: float | None
    delta_mean: float | None
    old_std: float | None
    new_std: float | None


class CategoricalDiff(BaseModel):
    column: str
    values_added: list[str] = Field(default_factory=list)
    values_removed: list[str] = Field(default_factory=list)
    old_top_values: dict[str, int] = Field(default_factory=dict)
    new_top_values: dict[str, int] = Field(default_factory=dict)


class StatsDiff(BaseModel):
    numeric_diffs: list[NumericDiff] = Field(default_factory=list)
    categorical_diffs: list[CategoricalDiff] = Field(default_factory=list)


class DiffReport(BaseModel):
    summary: Summary
    schema_diff: SchemaDiff
    row_diff: RowDiff
    quality_diff: QualityDiff
    numeric_diff: list[NumericDiff] = Field(default_factory=list)
    categorical_diff: list[CategoricalDiff] = Field(default_factory=list)
