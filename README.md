# Intelligent Career Counsellor

The **Intelligent Career Counsellor** is an AI-driven platform designed to provide tailored, personalized career guidance based on your current skills and target role.

The application allows users to upload a resume or input their skills, which is then parsed by the backend to extract relevant information. Based on this information and a target role, the system provides:
- **Skill Overview**: A breakdown of the user's current abilities and missing skills for their desired role.
- **Skill Demand Trends**: Visualizations showing the demand for different skills in the market.
- **AI Career Roadmap**: A personalized step-by-step roadmap to guide the user toward their career goals.
- **Interactive Career Assistant**: A chat interface to answer questions and provide further guidance.
- **Learning Resources**: Suggested courses and materials to help learn missing skills.

The tech stack comprises:
- `frontend`: A responsive dashboard built with Next.js 14 and Tailwind CSS, featuring components for resume upload, stats overview, skill display, demand charts, and AI roadmap.
- `backend`: FastAPI-based APIs handling resume parsing, skill analysis, roadmap generation, dashboard building, and chat services.

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
