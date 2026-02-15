from __future__ import annotations

from app.schemas import AnalyzeSkillsRequest, ChatMessage, ChatResponse
from app.services.analysis import analyze_skills


def generate_chat_reply(
    message: str,
    profile_skills: list[str],
    target_role: str | None,
    history: list[ChatMessage] | None = None,
) -> ChatResponse:
    analysis = analyze_skills(AnalyzeSkillsRequest(skills=profile_skills, target_role=target_role))
    lower_message = message.lower()
    previous_user_messages = [item.content for item in (history or []) if item.role == "user"]
    recent_user_context = previous_user_messages[-1] if previous_user_messages else ""

    high_growth = [item.skill_name for item in analysis.skill_scores if item.status == "high_growth"]
    obsolete = [item.skill_name for item in analysis.skill_scores if item.status == "obsolete"]
    top_paths = ", ".join(analysis.recommended_paths[:2])

    if any(token in lower_message for token in ["transition", "switch", "move into"]):
        reply = (
            f"A strong transition path from your profile is: {top_paths}. "
            f"Start with Week 1 and Week 2 roadmap tasks, then build one visible portfolio project."
        )
    elif any(token in lower_message for token in ["obsolete", "outdated", "declining"]):
        if obsolete:
            reply = (
                f"These skills are at risk of obsolescence in your stack: {', '.join(obsolete)}. "
                "Keep them only for legacy contexts, and pair them with modern alternatives this month."
            )
        else:
            reply = "Your profile does not show strongly obsolete skills right now. Focus on expanding adjacent high-growth capabilities."
    elif any(token in lower_message for token in ["learn", "roadmap", "plan"]):
        first_steps = "; ".join(f"Week {item.week}: {item.title}" for item in analysis.roadmap[:3])
        reply = (
            "A focused learning roadmap for you is: "
            f"{first_steps}. Keep each week outcome-based with one tangible artifact."
        )
    else:
        growth_text = ", ".join(high_growth[:4]) if high_growth else "your strongest current skills"
        reply = (
            f"Your current career health score is {analysis.career_health_score}/100. "
            f"Priority growth skills: {growth_text}. Consider paths like {top_paths}."
        )

    if recent_user_context:
        reply = f"Considering your previous question ('{recent_user_context}'), {reply[0].lower()}{reply[1:]}"

    return ChatResponse(
        reply=reply,
        suggested_next_questions=[
            "Which 2 skills should I prioritize in the next 30 days?",
            "Can you convert my roadmap into daily goals?",
            "What project can prove this transition to recruiters?",
        ],
    )
