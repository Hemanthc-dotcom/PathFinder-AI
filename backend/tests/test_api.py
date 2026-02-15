from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_skills() -> None:
    payload = {"skills": ["Python", "React", "jQuery"], "target_role": "AI Engineer"}
    response = client.post("/api/analyze-skills", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert "career_health_score" in data
    assert len(data["skill_scores"]) == 3


def test_chat() -> None:
    payload = {
        "message": "How do I transition into AI?",
        "profile_skills": ["Python", "SQL", "React"],
        "history": [{"role": "user", "content": "I want to switch from frontend to AI."}],
    }
    response = client.post("/api/chat", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert "reply" in data
    assert isinstance(data["suggested_next_questions"], list)
    assert "previous question" in data["reply"].lower()


def test_upload_resume_txt() -> None:
    file_text = "Python React SQL 5 years experience Bachelor of Technology"
    files = {"file": ("resume.txt", file_text.encode("utf-8"), "text/plain")}
    response = client.post("/api/upload-resume", files=files)
    data = response.json()

    assert response.status_code == 200
    assert "parsed_profile" in data
    assert "quick_analysis" in data


def test_upload_resume_with_resume_field_alias() -> None:
    file_text = "Python React SQL 5 years experience Bachelor of Technology"
    files = {"resume": ("resume.txt", file_text.encode("utf-8"), "text/plain")}
    response = client.post("/api/upload-resume", files=files)

    assert response.status_code == 200


def test_legacy_upload_route() -> None:
    file_text = "Python React SQL 5 years experience Bachelor of Technology"
    files = {"resume": ("resume.txt", file_text.encode("utf-8"), "text/plain")}
    response = client.post("/upload", files=files)
    data = response.json()

    assert response.status_code == 200
    assert "skills" in data
    assert "career_health_score" in data


def test_dashboard() -> None:
    response = client.get("/api/dashboard", params={"target_role": "AI Engineer", "skills": "Python,React,SQL"})
    data = response.json()

    assert response.status_code == 200
    assert "stats" in data
    assert "skills" in data
    assert "role_demand" in data
    assert "roadmap_steps" in data


def test_refine_roadmap() -> None:
    payload = {
        "current_skills": ["Python", "React"],
        "target_role": "AI Engineer",
        "focus_areas": ["MLOps", "Cloud Architecture"],
    }
    response = client.post("/api/roadmap/refine", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert "message" in data
    assert isinstance(data["roadmap_steps"], list)
    assert len(data["roadmap_steps"]) > 0


def test_resources() -> None:
    response = client.get("/api/resources", params={"target_role": "AI Engineer", "skills": "Python,React"})
    data = response.json()

    assert response.status_code == 200
    assert "recommended_resources" in data
    assert len(data["recommended_resources"]) > 0
