# Product Requirements Document (PRD)

## Intelligent Career Counsellor & Skill Obsolescence Forecasting System

### 1. Introduction

**Problem Statement:**
In a rapidly changing job market, professionals struggle to keep their skills relevant. Traditional career advice is static and generic. We aim to build an intelligent system that analyzes a user’s current profile (skills, resume), cross-references it with live industry trends, and forecasts skill obsolescence while recommending personalized learning paths.

**Goals:**

- Identify outdated or declining skills.
- Predict future skill demand using AI.
- recommend personalized learning paths and career transition strategies.
- Provide a career mentorship chatbot.

### 2. Technology Stack

#### Frontend

- **Framework:** Next.js (React) - for server-side rendering and scalable application structure.
- **Styling:** Tailwind CSS - for rapid, responsive, and modern UI development.
- **State Management:** React Context API or Zustand.
- **Charts/Visuals:** Recharts or Chart.js for skill demand graphs.
- **Icons:** Lucide-React or Heroicons.

#### Backend

- **Framework:** Python FastAPI - Chosen for its speed and seamless integration with AI/ML libraries.
- **Database:** PostgreSQL (with pgvector for semantic search if needed) or MongoDB (for flexible document storage of resumes/profiles).
- **Authentication:** OAuth2 (Google/GitHub login) or JWT-based auth.

#### AI / ML Integration

- **LLM Provider:** Gemini API (Google) - for analyzing text, generating advice, and powering the chatbot.
- **NLP:** Spacy or NLTK (optional, if local parsing is needed), or rely on LLM for resume parsing.
- **Data Source:** Aggregated job descriptions (mocked or scraped from public sources) to detect trends.

### 3. Core Features & Functional Requirements

#### 3.1 User Profiling & Resume Parsing

- **User Upload:** Users can upload a resume (PDF/DOCX) or manually input skills.
- **Parsing:** System extracts:
  - Current Skills (Hard & Soft)
  - Experience Level
  - Education
  - Interests

#### 3.2 Skill Gap Analysis & Obsolescence Forecasting

- **Market Comparison:** Compare user skills against high-demand skills in target roles (e.g., "Frontend Dev" -> "Fullstack AI Engineer").
- **Obsolescence Score:** AI rates skills on a scale of "Obsolete" to "High Growth".
- **Visuals:** Display a graph showing the trend of specific skills over time (e.g., jQuery vs. React).

#### 3.3 AI Career Recommendations & Roadmap

- **Path Generation:** Suggest 2-3 viable career paths (e.g., "Stay in Web Dev", "Pivot to AI Engineering").
- **Learning Roadmap:** Generate a step-by-step learning plan (Week 1: Learn Python, Week 5: Build RAG app).
- **Resource Linking:** Suggest courses or documentation (e.g., "Learn React Docs").

#### 3.4 AI Career Chatbot

- **Interactive Mentor:** A chat interface where users can ask specific questions:
  - "Is it worth learning COBOL in 2024?"
  - "How do I transition from QA to DevOps?"
- **Context Aware:** The chatbot is aware of the user's uploaded profile.

### 4. Database Schema (Conceptual)

**Users Table**

- `id`: UUID
- `email`: String
- `name`: String
- `current_role`: String

**Skills Matrix**

- `skill_name`: String (e.g., "Python")
- `category`: Enum (Language, Framework, Soft Skill)
- `trend_score`: Integer (1-100, updated periodically)

**UserProfiles**

- `user_id`: FK
- `skills`: JSON List
- `parsed_resume`: Text

### 5. API Endpoints (Draft)

- `POST /api/upload-resume`: Upload and parse resume file.
- `GET /api/analysis`: Get skill gap analysis for the current user.
- `POST /api/chat`: Send message to AI mentor.
- `GET /api/roadmap`: Generate learning path based on target role.

### 6. User Interface Design (Lo-Fi)

- **Dashboard:** Overview card with "Career Health Score", "Top Skills", "Recommended Actions".
- **Skill Graph:** Line chart showing demand trends.
- **Upload Modal:** Drag & drop interface for resumes.
- **Chat Widget:** Floating or dedicated page for AI mentorship.
