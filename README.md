# Intelligent Career Counsellor

Local full-stack scaffold for a career guidance platform with:

- `frontend`: Next.js 14 + Tailwind dashboard, analysis, upload, and chat UI
- `backend`: FastAPI APIs for resume parsing, skill analysis, roadmap generation, and chat

## Structure

```text
.
├─ docs/
├─ frontend/
└─ backend/
```

## Run Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend expects backend at `http://localhost:8000` by default.
