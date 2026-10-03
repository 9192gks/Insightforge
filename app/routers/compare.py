from fastapi import APIRouter, HTTPException
from app.db.database import get_dataset
from app.services.datasets import load_dataframe
from app.models.schemas import ComparisonResponse

router = APIRouter(prefix="/api/v1/compare", tags=["Comparison"])

@router.get("", response_model=ComparisonResponse)
def compare(dataset_a: str, dataset_b: str):
    a = get_dataset(dataset_a)
    b = get_dataset(dataset_b)
    if not a or not b:
        raise HTTPException(404, "One or both datasets were not found.")

    df_a = load_dataframe(a["path"])
    df_b = load_dataframe(b["path"])

    cols_a = {str(c) for c in df_a.columns}
    cols_b = {str(c) for c in df_b.columns}
    common = sorted(cols_a & cols_b)
    added = sorted(cols_b - cols_a)
    removed = sorted(cols_a - cols_b)

    change = len(df_b) - len(df_a)
    pct = (change / len(df_a) * 100) if len(df_a) else 0

    return {
        "dataset_a": dataset_a,
        "dataset_b": dataset_b,
        "rows_change": change,
        "rows_change_pct": round(pct, 2),
        "columns_added": added,
        "columns_removed": removed,
        "common_columns": common
    }
