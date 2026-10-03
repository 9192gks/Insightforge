from fastapi import APIRouter
from app.config import settings
from app.models.schemas import HealthResponse

router = APIRouter(tags=["System"])

@router.get("/health", response_model=HealthResponse)
def health():
    return {"status": "healthy", "version": settings.version}
