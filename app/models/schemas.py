from pydantic import BaseModel, Field
from typing import Any, Optional

class DatasetSummary(BaseModel):
    id: str
    filename: str
    rows: int
    columns: int
    created_at: str

class ColumnProfile(BaseModel):
    name: str
    dtype: str
    missing: int
    missing_pct: float
    unique: int
    sample: list[Any] = []

class ProfileResponse(BaseModel):
    dataset_id: str
    rows: int
    columns: int
    duplicate_rows: int
    memory_mb: float
    column_profiles: list[ColumnProfile]

class CorrelationItem(BaseModel):
    column_a: str
    column_b: str
    correlation: float

class ComparisonResponse(BaseModel):
    dataset_a: str
    dataset_b: str
    rows_change: int
    rows_change_pct: float
    columns_added: list[str]
    columns_removed: list[str]
    common_columns: list[str]

class HealthResponse(BaseModel):
    status: str
    version: str
