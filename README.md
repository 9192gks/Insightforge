# InsightForge FastAPI

A pure FastAPI data-analysis backend. No AI, no LLM, no external AI API.

## Features

- CSV/XLSX upload
- SQLite dataset registry
- Automatic dataset profiling
- Missing-value and duplicate analysis
- Numeric correlation analysis
- Isolation Forest anomaly detection
- Dataset preview
- Dataset-to-dataset structural comparison
- Pydantic response validation
- Swagger/OpenAPI documentation
- Automated health endpoint
- Basic API test

## Install

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc
- http://127.0.0.1:8000/health

## Example workflow

1. `POST /api/v1/datasets/upload`
2. Copy returned dataset ID.
3. Call `/api/v1/datasets/{id}/profile`
4. Call `/api/v1/datasets/{id}/correlations?min_abs=0.7`
5. Call `/api/v1/datasets/{id}/anomalies`
6. Upload another file and use `/api/v1/compare`

No AI service is required.


## Web dashboard

The project now includes a polished browser dashboard at:

```text
http://127.0.0.1:8000/
```

The frontend is plain HTML/CSS/JavaScript served directly by FastAPI. It uses the existing APIs for uploads, profiling, anomaly detection and correlations.
