# Intelligent Career Counsellor

The **Intelligent Career Counsellor** is an AI-driven platform designed to provide tailored, personalized career guidance.

By analyzing user inputs, the system identifies current abilities, pinpoints missing skills, and constructs personalized roadmaps to help users reach their career goals. It also includes an interactive career assistant chatbot.

Features include:
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
