from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from uuid import uuid4
from datetime import datetime, timezone
import shutil

from app.config import settings
from app.db.database import add_dataset, get_dataset, list_datasets
from app.services.datasets import load_dataframe, SUPPORTED
from app.models.schemas import DatasetSummary

router = APIRouter(prefix="/api/v1/datasets", tags=["Datasets"])
DATA_DIR = Path(settings.data_dir)
DATA_DIR.mkdir(exist_ok=True)

@router.post("/upload", response_model=DatasetSummary)
async def upload_dataset(file: UploadFile = File(...)):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in SUPPORTED:
        raise HTTPException(400, "Only CSV and Excel files are supported.")

    dataset_id = uuid4().hex[:12]
    target = DATA_DIR / f"{dataset_id}{suffix}"

    with target.open("wb") as out:
        shutil.copyfileobj(file.file, out)

    try:
        df = load_dataframe(str(target))
    except Exception as exc:
        target.unlink(missing_ok=True)
        raise HTTPException(400, f"Could not read dataset: {exc}")

    if len(df) == 0:
        target.unlink(missing_ok=True)
        raise HTTPException(400, "The uploaded dataset is empty.")

    created = datetime.now(timezone.utc).isoformat()
    add_dataset(dataset_id, file.filename, len(df), len(df.columns), created, str(target))

    return {
        "id": dataset_id,
        "filename": file.filename,
        "rows": len(df),
        "columns": len(df.columns),
        "created_at": created
    }

@router.get("", response_model=list[DatasetSummary])
def datasets():
    return list_datasets()

@router.get("/{dataset_id}", response_model=DatasetSummary)
def dataset(dataset_id: str):
    item = get_dataset(dataset_id)
    if not item:
        raise HTTPException(404, "Dataset not found.")
    return {k: item[k] for k in ["id", "filename", "rows", "columns", "created_at"]}
