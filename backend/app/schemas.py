from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ParsedResumeProfile(BaseModel):
    skills: list[str] = Field(default_factory=list)
    experience_level: str = "Unknown"
    education: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)
    raw_text_preview: str = ""
    parse_warning: str | None = None


class TrendPoint(BaseModel):
    label: str
    demand_score: int = Field(ge=0, le=100)


class SkillTrend(BaseModel):
    skill_name: str
    points: list[TrendPoint]


class SkillScore(BaseModel):
    skill_name: str
    status: Literal["obsolete", "stable", "high_growth"]
    trend_score: int = Field(ge=0, le=100)
    insight: str


class RoadmapItem(BaseModel):
    week: int = Field(ge=1)
    title: str
    outcome: str


class AnalyzeSkillsRequest(BaseModel):
    skills: list[str] = Field(default_factory=list)
    target_role: str | None = None


class AnalyzeSkillsResponse(BaseModel):
    career_health_score: int = Field(ge=0, le=100)
    skill_scores: list[SkillScore]
    recommended_paths: list[str]
    roadmap: list[RoadmapItem]
    trends: list[SkillTrend]


class UploadResumeResponse(BaseModel):
    parsed_profile: ParsedResumeProfile
    quick_analysis: AnalyzeSkillsResponse


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=2000)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    profile_skills: list[str] = Field(default_factory=list)
    history: list[ChatMessage] = Field(default_factory=list)
    target_role: str | None = None


class ChatResponse(BaseModel):
    reply: str
    suggested_next_questions: list[str]


class LearningResource(BaseModel):
    title: str
    url: str
    resource_type: Literal["course", "documentation", "project", "article"]
    difficulty: Literal["beginner", "intermediate", "advanced"]
    reason: str


class DashboardStat(BaseModel):
    label: str
    value: str
    change: str
    icon: Literal["target", "zap", "trending_up", "book_open"]


class DashboardSkill(BaseModel):
    name: str
    level: int = Field(ge=0, le=100)
    category: str
    trending: bool
    status: Literal["obsolete", "stable", "high_growth"]


class RoleDemandItem(BaseModel):
    role: str
    demand: int = Field(ge=0, le=100)


class RoadmapStep(BaseModel):
    id: int = Field(ge=1)
    title: str
    description: str
    timeline: str
    status: Literal["complete", "current", "upcoming"]
    tasks: list[str] = Field(default_factory=list)


class DashboardResponse(BaseModel):
    user_name: str
    headline: str
    subtitle: str
    stats: list[DashboardStat]
    skills: list[DashboardSkill]
    trend_data: list[dict[str, str | int]]
    role_demand: list[RoleDemandItem]
    roadmap_steps: list[RoadmapStep]
    recommended_resources: list[LearningResource] = Field(default_factory=list)
    ai_insight: str


class RefineRoadmapRequest(BaseModel):
    current_skills: list[str] = Field(default_factory=list)
    target_role: str | None = None
    focus_areas: list[str] = Field(default_factory=list)


class RefineRoadmapResponse(BaseModel):
    message: str
    roadmap_steps: list[RoadmapStep]


class ResourcesResponse(BaseModel):
    target_role: str
    recommended_resources: list[LearningResource]
