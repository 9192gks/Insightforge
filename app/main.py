from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.config import settings
from app.db.database import init_db
from app.routers import datasets, analysis, compare, system

@asynccontextmanager
async def lifespan(app):
    init_db()
    yield

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=(
        "A production-style dataset analysis API without AI. "
        "Upload CSV/Excel files, profile them, find correlations, "
        "detect anomalies and compare datasets."
    ),
    lifespan=lifespan
)

app.include_router(system.router)
app.include_router(datasets.router)
app.include_router(analysis.router)
app.include_router(compare.router)

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", include_in_schema=False)
def frontend():
    return FileResponse(STATIC_DIR / "index.html")
