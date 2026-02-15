# Backend Implementation Plan

## Intelligent Career Counsellor system

### Technology Stack

- **Language:** Python 3.10+
- **Framework:** FastAPI
- **Database:** PostgreSQL (or MongoDB)
- **AI Integration:** Google Gemini API

### Phase 1: Setup & Environment

1.  **Initialize Project**
    - Create `backend` directory.
    - Set up virtual environment (`venv`).
    - Create `requirements.txt`.

2.  **Install Dependencies**

    ```bash
    pip install fastapi uvicorn pydantic python-multipart google-generativeai python-dotenv SQLAlchemy psycopg2-binary
    ```

3.  **Basic Application Structure**
    - `main.py`: Entry point, app initialization.
    - `config.py`: Environment variable management.
    - `database.py`: DB connection handling.

### Phase 2: Core API Development

1.  **Resume Operations**
    - **Endpoint:** `POST /api/upload-resume`
    - **Logic:** Accept PDF/DOCX, extract text (using `pypdf` or similar), send to LLM for parsing.
    - **Output:** structured JSON (Skills, Experience, Education).

2.  **Analysis Engine**
    - **Endpoint:** `POST /api/analyze-skills`
    - **Logic:** Take parsed skills, query LLM for "Obsolescence Score" and "Future Demand".
    - **Output:** JSON with scores and trend data.

3.  **Chatbot**
    - **Endpoint:** `POST /api/chat`
    - **Logic:** Streaming response from LLM, maintaining conversation history (context window).

### Phase 3: Database Integration

- Design Schema (Users, Resumes, ChatHistory).
- Implement CRUD operations.

### Verification

- **Unit Tests:** `pytest` for all endpoints.
- **Manual Test:** Use Swagger UI (`/docs`) to upload a dummy resume and check JSON output.
