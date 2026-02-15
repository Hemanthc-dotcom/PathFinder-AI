from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status

from app.schemas import (
    AnalyzeSkillsRequest,
    AnalyzeSkillsResponse,
    ChatRequest,
    ChatResponse,
    DashboardResponse,
    LearningResource,
    RefineRoadmapRequest,
    RefineRoadmapResponse,
    ResourcesResponse,
    UploadResumeResponse,
)
from app.services.analysis import analyze_skills
from app.services.chat import generate_chat_reply
from app.services.dashboard import build_dashboard, refine_roadmap, suggest_resources
from app.services.resume_parser import parse_resume

router = APIRouter(tags=["career"])


@router.post("/upload-resume", response_model=UploadResumeResponse)
async def upload_resume(
    file: UploadFile | None = File(default=None),
    resume: UploadFile | None = File(default=None),
) -> UploadResumeResponse:
    selected = file or resume
    if selected is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No file provided. Use 'file' or 'resume' field in multipart form data.",
        )

    file_bytes = await selected.read()
    parsed = parse_resume(
        file_name=selected.filename or "resume.txt",
        mime_type=selected.content_type,
        file_bytes=file_bytes,
    )
    quick_analysis = analyze_skills(AnalyzeSkillsRequest(skills=parsed.skills))
    return UploadResumeResponse(parsed_profile=parsed, quick_analysis=quick_analysis)


@router.get("/analysis", response_model=AnalyzeSkillsResponse)
def get_default_analysis() -> AnalyzeSkillsResponse:
    demo_skills = ["Python", "React", "SQL", "Docker", "Communication"]
    return analyze_skills(AnalyzeSkillsRequest(skills=demo_skills, target_role="AI Engineer"))


@router.post("/analyze-skills", response_model=AnalyzeSkillsResponse)
def analyze(payload: AnalyzeSkillsRequest) -> AnalyzeSkillsResponse:
    return analyze_skills(payload)


@router.get("/roadmap")
def get_roadmap(target_role: str = Query(default="AI Engineer")) -> dict[str, object]:
    analysis = analyze_skills(
        AnalyzeSkillsRequest(skills=["Python", "SQL", "Communication"], target_role=target_role)
    )
    return {"target_role": target_role, "roadmap": analysis.roadmap}


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    return generate_chat_reply(
        message=payload.message,
        profile_skills=payload.profile_skills,
        target_role=payload.target_role,
        history=payload.history,
    )


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(target_role: str | None = Query(default=None), skills: str | None = Query(default=None)) -> DashboardResponse:
    parsed_skills = [item.strip() for item in (skills or "").split(",") if item.strip()]
    return build_dashboard(skills=parsed_skills, target_role=target_role)


@router.post("/roadmap/refine", response_model=RefineRoadmapResponse)
def post_refine_roadmap(payload: RefineRoadmapRequest) -> RefineRoadmapResponse:
    return refine_roadmap(
        current_skills=payload.current_skills,
        target_role=payload.target_role,
        focus_areas=payload.focus_areas,
    )


@router.get("/resources", response_model=ResourcesResponse)
def get_resources(
    target_role: str | None = Query(default=None),
    skills: str | None = Query(default=None),
) -> ResourcesResponse:
    parsed_skills = [item.strip() for item in (skills or "").split(",") if item.strip()]
    selected_target_role = target_role or "General Software Engineer"
    resources: list[LearningResource] = suggest_resources(skills=parsed_skills, target_role=target_role)
    return ResourcesResponse(target_role=selected_target_role, recommended_resources=resources)
