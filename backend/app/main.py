from __future__ import annotations

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.schemas import AnalyzeSkillsRequest
from app.config import settings
from app.services.analysis import analyze_skills
from app.services.resume_parser import parse_resume

app = FastAPI(title=settings.app_name, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Intelligent Career Counsellor API"}


@app.post("/upload")
async def upload_legacy(
    resume: UploadFile | None = File(default=None),
    file: UploadFile | None = File(default=None),
) -> dict[str, object]:
    selected = resume or file
    if selected is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No resume file provided. Use 'resume' or 'file' in multipart form data.",
        )

    file_bytes = await selected.read()
    parsed = parse_resume(
        file_name=selected.filename or "resume.txt",
        mime_type=selected.content_type,
        file_bytes=file_bytes,
    )
    quick_analysis = analyze_skills(AnalyzeSkillsRequest(skills=parsed.skills))

    return {
        "skills": parsed.skills,
        "experience_level": parsed.experience_level,
        "education": parsed.education,
        "interests": parsed.interests,
        "parse_warning": parsed.parse_warning,
        "career_health_score": quick_analysis.career_health_score,
        "recommended_paths": quick_analysis.recommended_paths,
    }
