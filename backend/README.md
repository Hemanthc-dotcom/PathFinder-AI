# Backend

FastAPI service for resume parsing, skill analysis, roadmap generation, and chat endpoints.

## Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## API

- `GET /health`
- `POST /api/upload-resume`
- `GET /api/analysis`
- `POST /api/analyze-skills`
- `GET /api/roadmap?target_role=AI Engineer`
- `GET /api/dashboard?target_role=AI Engineer&skills=Python,React,SQL`
- `POST /api/roadmap/refine`
- `POST /api/chat`
