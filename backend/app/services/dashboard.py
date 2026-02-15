from __future__ import annotations

from typing import Iterable

from app.schemas import (
    AnalyzeSkillsRequest,
    DashboardResponse,
    DashboardSkill,
    DashboardStat,
    LearningResource,
    RefineRoadmapResponse,
    RoleDemandItem,
    RoadmapStep,
)
from app.services.analysis import analyze_skills

SKILL_CATEGORY_MAP = {
    "python": "Data Science",
    "javascript": "Frontend",
    "typescript": "Frontend",
    "react": "Frontend",
    "next.js": "Frontend",
    "node.js": "Backend",
    "fastapi": "Backend",
    "django": "Backend",
    "sql": "Database",
    "postgresql": "Database",
    "mongodb": "Database",
    "docker": "DevOps",
    "kubernetes": "DevOps",
    "aws": "Cloud",
    "azure": "Cloud",
    "machine learning": "AI/ML",
    "generative ai": "AI/ML",
    "data analysis": "Analytics",
    "testing": "Quality",
    "git": "Engineering",
    "ci/cd": "DevOps",
}

TIMELINES = [
    "Month 1-2",
    "Month 3-4",
    "Month 5-6",
    "Month 7-8",
    "Month 9-10",
]

DEFAULT_DASHBOARD_SKILLS = ["React", "Python", "PostgreSQL", "AWS", "Docker", "Machine Learning"]

RESOURCE_CATALOG: dict[str, list[LearningResource]] = {
    "AI Engineer": [
        LearningResource(
            title="Hands-On Large Language Models",
            url="https://www.oreilly.com/library/view/hands-on-large-language/9781098150952/",
            resource_type="course",
            difficulty="intermediate",
            reason="Build practical LLM and RAG workflows relevant for AI product roles.",
        ),
        LearningResource(
            title="FastAPI Documentation",
            url="https://fastapi.tiangolo.com/",
            resource_type="documentation",
            difficulty="beginner",
            reason="Ship API-first AI services with clean request/response design.",
        ),
        LearningResource(
            title="Gemini API Documentation",
            url="https://ai.google.dev/gemini-api/docs",
            resource_type="documentation",
            difficulty="intermediate",
            reason="Understand production-ready prompting, embeddings, and model integration patterns.",
        ),
        LearningResource(
            title="Build an AI Career Mentor App",
            url="https://github.com/topics/llm-app",
            resource_type="project",
            difficulty="intermediate",
            reason="Portfolio-ready project idea aligned to your target transition.",
        ),
    ],
    "Fullstack Engineer": [
        LearningResource(
            title="Next.js Documentation",
            url="https://nextjs.org/docs",
            resource_type="documentation",
            difficulty="beginner",
            reason="Strengthen App Router and server/client boundary fundamentals.",
        ),
        LearningResource(
            title="TypeScript Handbook",
            url="https://www.typescriptlang.org/docs/",
            resource_type="documentation",
            difficulty="beginner",
            reason="Improve reliability and maintainability in large frontend codebases.",
        ),
        LearningResource(
            title="Fullstack Open",
            url="https://fullstackopen.com/en/",
            resource_type="course",
            difficulty="intermediate",
            reason="Deep, project-oriented fullstack practice from API to UI.",
        ),
        LearningResource(
            title="System Design Primer",
            url="https://github.com/donnemartin/system-design-primer",
            resource_type="article",
            difficulty="advanced",
            reason="Level up architecture and scaling discussions for interviews.",
        ),
    ],
    "DevOps Engineer": [
        LearningResource(
            title="Docker Documentation",
            url="https://docs.docker.com/",
            resource_type="documentation",
            difficulty="beginner",
            reason="Container fundamentals are foundational for modern DevOps workflows.",
        ),
        LearningResource(
            title="Kubernetes Documentation",
            url="https://kubernetes.io/docs/home/",
            resource_type="documentation",
            difficulty="intermediate",
            reason="Core orchestration patterns for resilient production deployments.",
        ),
        LearningResource(
            title="AWS Well-Architected Framework",
            url="https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html",
            resource_type="article",
            difficulty="advanced",
            reason="Use reliability/security/cost trade-offs in platform decisions.",
        ),
        LearningResource(
            title="Deploy a Monitoring Stack Project",
            url="https://github.com/topics/devops-project",
            resource_type="project",
            difficulty="intermediate",
            reason="Show practical impact with observability and incident-ready tooling.",
        ),
    ],
}

DEFAULT_RESOURCES: list[LearningResource] = [
    LearningResource(
        title="Roadmap.sh",
        url="https://roadmap.sh/",
        resource_type="article",
        difficulty="beginner",
        reason="Visual role roadmaps to sequence your learning path effectively.",
    ),
    LearningResource(
        title="freeCodeCamp Curriculum",
        url="https://www.freecodecamp.org/learn",
        resource_type="course",
        difficulty="beginner",
        reason="Hands-on guided learning to quickly close practical skill gaps.",
    ),
    LearningResource(
        title="Build in Public Portfolio Checklist",
        url="https://github.com/codecrafters-io/build-your-own-x",
        resource_type="project",
        difficulty="intermediate",
        reason="Project-based proof of skill is the fastest path to interview credibility.",
    ),
]


def build_dashboard(skills: list[str], target_role: str | None, user_name: str = "Alex") -> DashboardResponse:
    selected_skills = skills or DEFAULT_DASHBOARD_SKILLS
    analysis = analyze_skills(AnalyzeSkillsRequest(skills=selected_skills, target_role=target_role))

    dashboard_skills = [
        DashboardSkill(
            name=item.skill_name,
            level=item.trend_score,
            category=_category_for(item.skill_name),
            trending=item.status == "high_growth",
            status=item.status,
        )
        for item in analysis.skill_scores
    ]

    high_growth_count = sum(1 for item in analysis.skill_scores if item.status == "high_growth")
    market_label = _market_label(analysis.career_health_score)
    role_demand = _build_role_demand(analysis.recommended_paths, analysis.career_health_score)
    roadmap_steps = _build_roadmap_steps(analysis.roadmap)
    trend_data = _to_trend_rows(analysis.trends[:4])
    recommended_resources = suggest_resources(
        skills=[item.skill_name for item in analysis.skill_scores],
        target_role=analysis.recommended_paths[0] if analysis.recommended_paths else target_role,
    )
    primary_focus = ", ".join(item.skill_name for item in analysis.skill_scores if item.status == "high_growth") or "core engineering skills"

    stats = [
        DashboardStat(label="Career Match", value=f"{analysis.career_health_score}%", change="+4%", icon="target"),
        DashboardStat(label="Skills Analyzed", value=str(len(analysis.skill_scores)), change=f"+{high_growth_count}", icon="zap"),
        DashboardStat(label="Market Demand", value=market_label, change="Rising", icon="trending_up"),
        DashboardStat(label="Courses Suggested", value=str(len(analysis.roadmap) + 2), change="New", icon="book_open"),
    ]

    return DashboardResponse(
        user_name=user_name,
        headline=f"Welcome back, {user_name}",
        subtitle="Here is your AI-powered career dashboard. Let's build your future.",
        stats=stats,
        skills=dashboard_skills,
        trend_data=trend_data,
        role_demand=role_demand,
        roadmap_steps=roadmap_steps,
        recommended_resources=recommended_resources,
        ai_insight=(
            "Based on your profile and market signals, focus on "
            f"{primary_focus} to maximize transition opportunities."
        ),
    )


def refine_roadmap(current_skills: list[str], target_role: str | None, focus_areas: list[str]) -> RefineRoadmapResponse:
    merged = _dedupe([*current_skills, *focus_areas])
    dashboard = build_dashboard(skills=merged, target_role=target_role)
    focus_text = ", ".join(focus_areas) if focus_areas else "your selected skill profile"
    message = f"Roadmap refined with extra emphasis on {focus_text}."
    return RefineRoadmapResponse(message=message, roadmap_steps=dashboard.roadmap_steps)


def _category_for(skill_name: str) -> str:
    return SKILL_CATEGORY_MAP.get(skill_name.lower(), "General")


def _market_label(career_health_score: int) -> str:
    if career_health_score >= 80:
        return "High"
    if career_health_score >= 60:
        return "Medium"
    return "Low"


def _build_role_demand(paths: list[str], base_score: int) -> list[RoleDemandItem]:
    demand_rows: list[RoleDemandItem] = []
    for index, role in enumerate(paths[:6]):
        score = max(45, min(99, base_score + 8 - index * 4))
        demand_rows.append(RoleDemandItem(role=role, demand=score))
    return demand_rows


def _build_roadmap_steps(items: Iterable[object]) -> list[RoadmapStep]:
    steps: list[RoadmapStep] = []
    for index, item in enumerate(items, start=1):
        title = getattr(item, "title")
        outcome = getattr(item, "outcome")
        status = "complete" if index == 1 else "current" if index == 2 else "upcoming"
        timeline = TIMELINES[min(index - 1, len(TIMELINES) - 1)]
        steps.append(
            RoadmapStep(
                id=index,
                title=title,
                description=outcome,
                timeline=timeline,
                status=status,
                tasks=[
                    f"Study fundamentals for {title.lower()}",
                    f"Build one portfolio artifact for {title.lower()}",
                    "Document measurable outcomes and lessons learned",
                ],
            )
        )
    return steps


def _to_trend_rows(trends: list[object]) -> list[dict[str, str | int]]:
    if not trends:
        return []

    labels = [point.label for point in trends[0].points]
    rows: list[dict[str, str | int]] = []
    for label_index, label in enumerate(labels):
        row: dict[str, str | int] = {"month": label}
        for trend in trends:
            row[trend.skill_name] = trend.points[label_index].demand_score
        rows.append(row)
    return rows


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    items: list[str] = []
    for value in values:
        normalized = " ".join(value.split())
        key = normalized.lower()
        if not normalized or key in seen:
            continue
        seen.add(key)
        items.append(normalized)
    return items


def suggest_resources(skills: list[str], target_role: str | None) -> list[LearningResource]:
    role_key = (target_role or "").strip()
    role_resources = RESOURCE_CATALOG.get(role_key)
    if role_resources:
        return role_resources[:4]

    normalized = {item.lower() for item in skills}
    if {"python", "machine learning", "generative ai"} & normalized:
        return RESOURCE_CATALOG["AI Engineer"][:4]
    if {"react", "typescript", "next.js"} & normalized:
        return RESOURCE_CATALOG["Fullstack Engineer"][:4]
    if {"docker", "kubernetes", "aws", "azure"} & normalized:
        return RESOURCE_CATALOG["DevOps Engineer"][:4]

    return DEFAULT_RESOURCES[:4]
