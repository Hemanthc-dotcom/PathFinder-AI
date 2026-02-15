from __future__ import annotations

import calendar
import hashlib
from datetime import datetime, timezone
from statistics import mean

from app.schemas import (
    AnalyzeSkillsRequest,
    AnalyzeSkillsResponse,
    RoadmapItem,
    SkillScore,
    SkillTrend,
    TrendPoint,
)

TREND_SCORES: dict[str, int] = {
    "python": 90,
    "javascript": 82,
    "typescript": 88,
    "react": 84,
    "next.js": 86,
    "node.js": 80,
    "fastapi": 78,
    "django": 62,
    "sql": 85,
    "postgresql": 76,
    "mongodb": 70,
    "docker": 83,
    "kubernetes": 81,
    "aws": 87,
    "azure": 79,
    "machine learning": 92,
    "generative ai": 95,
    "data analysis": 75,
    "git": 72,
    "ci/cd": 77,
    "testing": 73,
    "jquery": 28,
    "php": 45,
    "cobol": 30,
}

ROLE_PATHS: dict[str, list[str]] = {
    "ai engineer": ["AI Engineer", "MLOps Engineer", "Data Engineer"],
    "mlops engineer": ["MLOps Engineer", "AI Engineer", "Platform Engineer"],
    "fullstack engineer": ["Fullstack Engineer", "AI Product Engineer", "Cloud Engineer"],
    "devops engineer": ["DevOps Engineer", "Platform Engineer", "Cloud Engineer"],
    "data engineer": ["Data Engineer", "Analytics Engineer", "AI Engineer"],
}

ROADMAP_TEMPLATES: dict[str, list[tuple[int, str, str]]] = {
    "AI Engineer": [
        (1, "Python and Statistics Refresh", "Build comfort with production-grade Python and applied stats."),
        (2, "ML Fundamentals", "Train and evaluate regression/classification models."),
        (3, "Generative AI Basics", "Understand embeddings, prompts, and RAG patterns."),
        (4, "LLM App Build", "Ship a small FastAPI + vector-search assistant."),
        (5, "MLOps and Deployment", "Deploy and monitor model-backed APIs."),
        (6, "Portfolio and Interview Prep", "Document projects with measurable impact."),
    ],
    "Fullstack Engineer": [
        (1, "TypeScript Deep Dive", "Increase correctness and confidence in large frontend apps."),
        (2, "Modern React Patterns", "Use server/client boundaries and state architecture cleanly."),
        (3, "Backend API Engineering", "Design secure, testable FastAPI or Node APIs."),
        (4, "Data Layer and SQL", "Model relational data and optimize common queries."),
        (5, "Cloud Deployment", "Deploy full-stack apps with CI/CD pipelines."),
        (6, "System Design Practice", "Handle scaling, caching, and reliability tradeoffs."),
    ],
}

DEFAULT_ROADMAP = [
    (1, "Core Language Upgrade", "Solidify one in-demand language for your target path."),
    (2, "Framework Practice", "Build a real feature using a modern framework."),
    (3, "Data Foundations", "Use SQL and data modeling in project workflows."),
    (4, "Cloud and DevOps", "Ship and monitor a containerized service."),
    (5, "Portfolio Project", "Demonstrate end-to-end ownership in one public project."),
    (6, "Interview Alignment", "Translate project outcomes into role-specific narratives."),
]


def analyze_skills(payload: AnalyzeSkillsRequest) -> AnalyzeSkillsResponse:
    normalized_skills = _normalize_skills(payload.skills)
    if not normalized_skills:
        normalized_skills = ["Communication", "Problem Solving"]

    scores = [_score_skill(skill) for skill in normalized_skills]
    avg_score = int(round(mean(item.trend_score for item in scores)))
    diversity_bonus = min(10, len(normalized_skills) * 2)
    career_health_score = _clamp(avg_score + diversity_bonus)

    recommended_paths = _recommend_paths(normalized_skills, payload.target_role)
    roadmap = _build_roadmap(recommended_paths[0])
    trends = [_build_trend(skill, score.trend_score) for skill, score in zip(normalized_skills[:5], scores[:5])]

    return AnalyzeSkillsResponse(
        career_health_score=career_health_score,
        skill_scores=scores,
        recommended_paths=recommended_paths,
        roadmap=roadmap,
        trends=trends,
    )


def _normalize_skills(skills: list[str]) -> list[str]:
    seen: set[str] = set()
    normalized: list[str] = []
    for skill in skills:
        clean = " ".join(skill.split())
        if not clean:
            continue
        key = clean.lower()
        if key in seen:
            continue
        seen.add(key)
        normalized.append(clean)
    return normalized


def _score_skill(skill: str) -> SkillScore:
    key = skill.lower()
    trend_score = TREND_SCORES.get(key, 58)

    if trend_score <= 35:
        status = "obsolete"
        insight = "Demand is declining. Keep only if your niche strongly requires it."
    elif trend_score >= 70:
        status = "high_growth"
        insight = "Strong market momentum. Prioritize deeper project-based mastery."
    else:
        status = "stable"
        insight = "Moderate demand. Pair with newer skills to improve career resilience."

    return SkillScore(skill_name=skill, status=status, trend_score=trend_score, insight=insight)


def _recommend_paths(skills: list[str], target_role: str | None) -> list[str]:
    if target_role:
        lookup = target_role.lower().strip()
        if lookup in ROLE_PATHS:
            return ROLE_PATHS[lookup]

    skill_set = {item.lower() for item in skills}
    if {"python", "machine learning", "generative ai"} & skill_set:
        return ["AI Engineer", "MLOps Engineer", "Data Engineer"]
    if {"react", "next.js", "javascript", "typescript"} & skill_set:
        return ["Fullstack Engineer", "Frontend Engineer", "AI Product Engineer"]
    if {"docker", "kubernetes", "aws", "azure"} & skill_set:
        return ["DevOps Engineer", "Cloud Engineer", "Platform Engineer"]
    return ["Software Engineer", "Fullstack Engineer", "Data Engineer"]


def _build_roadmap(primary_path: str) -> list[RoadmapItem]:
    rows = ROADMAP_TEMPLATES.get(primary_path, DEFAULT_ROADMAP)
    return [RoadmapItem(week=week, title=title, outcome=outcome) for week, title, outcome in rows]


def _build_trend(skill_name: str, base_score: int) -> SkillTrend:
    today = datetime.now(timezone.utc)
    points: list[TrendPoint] = []

    slope = 2 if base_score >= 70 else -2 if base_score <= 35 else 0
    for delta in range(-5, 1):
        year, month = _shift_month(today.year, today.month, delta)
        label = f"{calendar.month_abbr[month]} {str(year)[-2:]}"
        jitter = _deterministic_jitter(skill_name, delta)
        offset_index = delta + 5
        value = _clamp(base_score + slope * (offset_index - 2) + jitter)
        points.append(TrendPoint(label=label, demand_score=value))

    return SkillTrend(skill_name=skill_name, points=points)


def _shift_month(year: int, month: int, delta: int) -> tuple[int, int]:
    absolute = year * 12 + (month - 1) + delta
    out_year = absolute // 12
    out_month = absolute % 12 + 1
    return out_year, out_month


def _deterministic_jitter(skill_name: str, delta: int) -> int:
    seed = f"{skill_name}:{delta}".encode("utf-8")
    digest = hashlib.md5(seed).hexdigest()
    return int(digest[:2], 16) % 7 - 3


def _clamp(value: int) -> int:
    return max(0, min(100, value))
