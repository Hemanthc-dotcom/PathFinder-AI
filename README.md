# Intelligent Career Counsellor

The **Intelligent Career Counsellor** is an AI-driven platform designed to provide tailored, personalized career guidance based on your current skills and target role.

The application allows users to upload a resume or input their skills, which is then parsed by the backend using intelligent text extraction. Based on your profile and target role, the AI analyzes your current stack against market trends to generate actionable insights:

### 🌟 Core AI & Analytics Features
- **AI Career Health Score & Skill Overview**: Instantly evaluates your profile, identifying core strengths, missing gaps for your target role, and highlighting "high growth" versus "obsolete" skills.
- **Predictive Skill Demand Trends**: Visualizes market demand over time, helping you focus on the capabilities that matter most for future roles.
- **Generative Career Roadmap**: Synthesizes your skill gaps into a structured, step-by-step learning path mapped to actionable monthly timelines and measurable outcomes.
- **Contextual Career Assistant Chatbot**: An interactive AI chat that remembers your history and provides personalized advice on transitioning roles, prioritizing skills, or handling obsolete tech.
- **Smart Resource Recommendations**: Context-aware suggestions for courses, documentation, and portfolio projects tailored specifically to your roadmap and missing skills (e.g. AI Engineer, DevOps, Fullstack paths).

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
