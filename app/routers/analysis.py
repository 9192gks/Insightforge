from fastapi import APIRouter, HTTPException, Query
from app.db.database import get_dataset
from app.services.datasets import load_dataframe, profile, numeric_correlations
from app.services.anomaly import detect
from app.models.schemas import ProfileResponse, CorrelationItem

router = APIRouter(prefix="/api/v1/datasets", tags=["Analysis"])

def get_df(dataset_id):
    item = get_dataset(dataset_id)
    if not item:
        raise HTTPException(404, "Dataset not found.")
    try:
        return load_dataframe(item["path"])
    except Exception as exc:
        raise HTTPException(500, f"Could not read dataset: {exc}")

@router.get("/{dataset_id}/profile", response_model=ProfileResponse)
def dataset_profile(dataset_id: str):
    return {"dataset_id": dataset_id, **profile(get_df(dataset_id))}

@router.get("/{dataset_id}/correlations", response_model=list[CorrelationItem])
def correlations(dataset_id: str, min_abs: float = Query(0.0, ge=0, le=1)):
    return numeric_correlations(get_df(dataset_id), min_abs)

@router.get("/{dataset_id}/anomalies")
def anomalies(dataset_id: str, limit: int = Query(100, ge=1, le=1000)):
    return {
        "dataset_id": dataset_id,
        "count": len(detect(get_df(dataset_id), limit)),
        "items": detect(get_df(dataset_id), limit)
    }

@router.get("/{dataset_id}/preview")
def preview(dataset_id: str, limit: int = Query(50, ge=1, le=500)):
    df = get_df(dataset_id).head(limit)
    return {
        "columns": [str(c) for c in df.columns],
        "rows": df.where(df.notna(), None).to_dict(orient="records")
    }
